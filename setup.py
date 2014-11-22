from distutils.core import setup
import os

LOCALE_DIR= '/usr/share/locale'

locales = []
if os.path.exists('po/locale'):
    for lang in os.listdir('po/locale'):
        locales.append(os.path.join(lang, 'LC_MESSAGES'))

data_files = [("share/applications/", ["share/applications/mageiasync.desktop"]),
              ("share/icons/hicolor/scalable/apps", ["share/icons/mageiasync.svg"])
              ] + [(os.path.join(LOCALE_DIR, locale),
                            [os.path.join('po', 'locale', locale, 'mageiasync.mo')])
                            for locale in locales]

setup(
        name = 'mageiasync',
        version = '0.1.2',
        packages = ['mageiaSync'],
        scripts = ['mageiasync'],
        license = 'GNU General Public License v3 (GPLv3)',
        url = 'https://github.com/papoteur-mga/mageiaSync',
        description = 'This tool downloads ISO images from mirror or Mageia testing server.',
        long_description = 'This tool uses rsync with a GUI',
        platforms = ['Linux'],
        author = 'Papoteur',
        author_email = 'papoteur@mageialinux-online.org',
        maintainer = 'david_david',
        maintainer_email = 'david.david@mageialinux-online.org',
        data_files = data_files,
        )

