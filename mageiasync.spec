%define module	mageiasync
%define gitname	mageiaSync

Name:		python-%{module}
Version:	0.1.2
Release:	%mkrel 1
Summary:	A frontend to rsync for Mageia usage
License:	GPLv3
Group:		Development/Python
URL:		https://github.com/papoteur-mga/mageiaSync
Source0:	https://github.com/papoteur-mga/mageiaSync/archive/%{gitname}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python-setuptools

Requires:	python-qt5-core
Requires:	python-qt5-gui
Requires:	python-qt5-widgets
Requires:	rsync

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
#Requires:	rsync

#%description -n python3-%{module}
#A frontend to rsync for Mageia usage.
#This is the Python 3 build of %{module}.

#---------------------------------------------------------------------------

%prep
%setup -q -n %{gitname}-%{version}

#cp -a . %{py3dir}

%build
#pushd %{py3dir}
#%{__python3} setup.py build
#popd

%{__python} setup.py build

%install
#pushd %{py3dir}
#%{__python3} setup.py install --root=%{buildroot} --skip-build
#mv %{buildroot}%{_bindir}/%{module} %{buildroot}%{_bindir}/python3-%{module}
#popd

%{__python} setup.py install --root=%{buildroot} --skip-build

%files
%doc CHANGELOG LICENSE README.md
%{_bindir}/%{module}
%{_datadir}/applications/%{module}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{module}.svg
%{python_sitelib}/%{gitname}
%{python_sitelib}/%{module}-%{version}-py%{pyver}.egg-info

#%files -n python3-%{module}
#%doc CHANGELOG LICENSE README.md
#%{_bindir}/python3-%{module}
#%{_datadir}/applications/%{module}.desktop
#%{_iconsdir}/hicolor/scalable/apps/%{module}.svg
#%{python3_sitelib}/%{gitname}
#%{python3_sitelib}/%{module}-%{version}-py%{py3ver}.egg-info
