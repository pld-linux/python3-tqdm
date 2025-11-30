#
# Conditional build:
%bcond_with	tests	# unit tests (get stuck on builders)

Summary:	Fast, Extensible Progress Meter
Summary(pl.UTF-8):	Szybki, rozszerzalny wskaźnik postępu
Name:		python3-tqdm
Version:	4.67.1
Release:	1
License:	MPL v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/tqdm/
Source0:	https://files.pythonhosted.org/packages/source/t/tqdm/tqdm-%{version}.tar.gz
# Source0-md5:	aca803dd7ac5c4ae233977aff41b7f7c
URL:		https://pypi.org/project/tqdm/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools >= 1:42
BuildRequires:	python3-setuptools_scm >= 3.4
BuildRequires:	python3-wheel
%if %{with tests}
# optional
#BuildRequires:	python3-nbval
BuildRequires:	python3-pytest >= 6
BuildRequires:	python3-pytest-asyncio >= 0.24
BuildRequires:	python3-pytest-timeout
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Fast, Extensible Progress Meter.

%description -l pl.UTF-8
Szybki, rozszerzalny wskaźnik postępu.

%prep
%setup -q -n tqdm-%{version}

# shebang is useless in completion file
%{__sed} -i -e '1s,.*/usr/bin/env bash.*,,' tqdm/completion.sh

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_asyncio.plugin,pytest_timeout" \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__mv} $RPM_BUILD_ROOT%{_bindir}/tqdm{,-3}
ln -sf tqdm-3 $RPM_BUILD_ROOT%{_bindir}/tqdm

install -d $RPM_BUILD_ROOT{%{bash_compdir},%{_mandir}/man1}
%{__mv} $RPM_BUILD_ROOT%{py3_sitescriptdir}/tqdm/completion.sh $RPM_BUILD_ROOT%{bash_compdir}/tqdm
%{__mv} $RPM_BUILD_ROOT%{py3_sitescriptdir}/tqdm/tqdm.1 $RPM_BUILD_ROOT%{_mandir}/man1

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -pr examples $RPM_BUILD_ROOT%{_examplesdir}/python3-tqdm-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENCE README.rst
%attr(755,root,root) %{_bindir}/tqdm-3
%{_bindir}/tqdm
%{py3_sitescriptdir}/tqdm
%{py3_sitescriptdir}/tqdm-%{version}.dist-info
%{bash_compdir}/tqdm
%{_mandir}/man1/tqdm.1*
%{_examplesdir}/python3-tqdm-%{version}
