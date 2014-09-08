%define module	mageiasync

Name:		python-%{module}
Version:	0.1
Release:	%mkrel 1
Summary:	A frontend to rsync for Mageia usage
License:	GPLv3
Group:		Development/Python
URL:		https://github.com/papoteur-mga/mageiaSync
Source0:	https://github.com/papoteur-mga/mageiaSync/archive/mageiaSync-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python3-setuptools

Requires:	python-qt5-core
Requires:	python-qt5-gui
Requires:	python-qt5-widgets

%description
A frontend to rsync for Mageia usage.

#---------------------------------------------------------------------------

#%package -n	python3-%{module}
#Summary:	A frontend to rsync for Mageia usage
#Group:		Development/Python
#BuildArch:	noarch
#BuildRequires:	python3-setuptools

#Requires:	python3-qt5-core
#Requires:	python3-qt5-gui
#Requires:	python3-qt5-widgets

#%description -n python3-%{module}
#A frontend to rsync for Mageia usage.
#This is the Python 3 build of %{module}.

#---------------------------------------------------------------------------

%prep
%setup -q -n mageiaSync-%{version}

#cp -a . %{py3dir}

%build
#pushd %{py3dir}
#%{__python3} setup.py build
#popd

%{__python3} setup.py build

%install
#pushd %{py3dir}
#%{__python3} setup.py install --root=%{buildroot} --skip-build
#mv %{buildroot}%{_bindir}/livestreamer %{buildroot}%{_bindir}/python3-livestreamer
#popd

%{__python3} setup.py install --root=%{buildroot} --skip-build

%files
%doc README.rst LICENSE
%{_bindir}/%{module}
%{_datadir}/applications/%{module}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{module}.svg
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-%{version}-py%{py3ver}.egg-info

#%files -n python3-%{module}
#%doc README.rst LICENSE
#%{_bindir}/python3-%{module}
#%{_datadir}/applications/%{module}.desktop
#%{_iconsdir}/hicolor/scalable/apps/%{module}.svg
#%{python3_sitelib}/%{module}
#%{python3_sitelib}/%{module}-%{version}-py%{py3ver}.egg-info