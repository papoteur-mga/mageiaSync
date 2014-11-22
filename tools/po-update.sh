#!/bin/sh

set -e

if test "$1" = "-h" -o "$1" = "--help"; then
	echo "Use: $0 [<language>]"
	echo "Run without arguments to update all translation files."
	exit 0
fi

cd "$(readlink -f "$(dirname "$0")/..")"

VERSION=(0.1.2)
DOMAIN=(mageiasync)

intltool-extract --type=gettext/ini share/applications/mageiasync.desktop.in

POT_DIR="$PWD/po"
test -d "$POT_DIR"

POT_FILE="$POT_DIR/$DOMAIN.pot"

/usr/bin/xgettext \
	--package-name "$DOMAIN" \
	--package-version "$VERSION" \
	--language=Python --from-code=UTF-8 --keyword=_ --keyword=N_ \
	--no-escape --add-location --sort-by-file \
	--add-comments=I18N \
	--output="$POT_FILE" \
	mageiasync/mageiasync.py \
	mageiasync/mageiaSyncDBprefs.py \
	mageiasync/mageiaSyncDBprefs.py \
	mageiasync/mageiaSyncDBrename.py \
	mageiasync/mageiaSyncDBupdate.py \
	mageiasync/mageiaSyncExt.py \
	mageiasync/mageiaSyncUI.py \
	mageiasync/mageiaSyncDBprefs.ui \
	mageiasync/mageiaSyncDBrename.ui \
	mageiasync/mageiaSyncDBupdate.ui \
	mageiasync/mageiaSyncUI.ui \
	share/applications/mageiasync.desktop.in.h

/bin/sed --in-place --expression="s/charset=CHARSET/charset=UTF-8/" "$POT_FILE"

intltool-merge --desktop-style po share/applications/mageiasync.desktop.in share/applications/mageiasync.desktop

rm -f share/applications/mageiasync.desktop.in.h

update_po() {
	local LL_CC="$1"
	local PO_FILE="$POT_DIR/$LL_CC.po"

        echo "Update $(basename "$PO_FILE"):"
	/usr/bin/msgmerge \
		--update --no-fuzzy-matching \
		--no-escape --add-location --sort-by-file \
		--lang="$LL_CC" \
		"$PO_FILE" "$POT_FILE"

	# /bin/sed --in-place --expression="s/Language: \\\\n/Language: $L_NAME\\\\n/" "$PO_FILE"
}

if test "$1"; then
	update_po "$1"
else
	for l in $(ls -1 "$POT_DIR"/*.po); do
		l="$(basename "$l")"
		update_po "${l%.po}"
	done
fi
