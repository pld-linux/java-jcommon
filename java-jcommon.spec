#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_with	tests		# don't build tests

%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif

%include	/usr/lib/rpm/macros.java
%define		srcname		jcommon
Summary:	Common library for Object Refinery Projects
Summary(pl.UTF-8):	Biblioteka wspólna dla projektów Object Refinery
Name:		java-jcommon
Version:	1.0.16
Release:	1
License:	LGPL
Group:		Libraries/Java
Source0:	http://downloads.sourceforge.net/jfreechart/%{srcname}-%{version}.tar.gz
# Source0-md5:	5fb774c225cdc7d15a99c9702031ae05
URL:		http://www.jfree.org/jcommon/index.html
BuildRequires:	ant
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{?with_java_sun:BuildRequires:	java-sun}
BuildRequires:	jpackage-utils >= 0:1.5
%{?with_tests:BuildRequires:	junit}
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Collection of classes used by Object Refinery Projects, for example
jfreechart.

%description -l pl.UTF-8
Zbiór klas używanych przez projekty Object Refinery, jak na przykład
jfreechart.

%package test
Summary:	Test tasks for %{srcname}
Summary(pl.UTF-8):	Zadania testowe dla pakietu %{srcname}
Group:		Development/Languages/Java
Requires:	%{srcname} = %{epoch}:%{version}-%{release}
Requires:	junit

%description test
All test tasks for %{srcname}.

%description test -l pl.UTF-8
Wszystkie zadania testowe dla pakietu %{srcname}.

%package javadoc
Summary:	Javadoc for %{srcname}
Summary(pl.UTF-8):	Dokumentacja Javadoc do pakietu %{srcname}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{srcname}.

%description javadoc -l fr.UTF-8
Javadoc pour %{srcname}.

%description javadoc -l pl.UTF-8
Dokumentacja Javadoc do pakietu %{srcname}.

%prep
%setup -q -n %{srcname}-%{version}
# remove all binary libs
find . -name '*.jar' | xargs rm -v

%build
%if %{with tests}
CLASSPATH=$(build-classpath junit)
%endif
%ant -f ant/build.xml -Dbuildstable=true -Dproject.outdir=. -Dbasedir=. \
	compile %{?with_tests:compile-junit-tests} %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d $RPM_BUILD_ROOT%{_javadir}
install %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar
%if %{with tests}
install lib/%{srcname}-%{version}-junit.jar $RPM_BUILD_ROOT%{_javadir}
ln -s %{srcname}-%{version}-junit.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-junit.jar
%endif

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -pr javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc README.txt
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%if %{with tests}
%files test
%defattr(644,root,root,755)
%{_javadir}/%{srcname}-%{version}-junit.jar
%{_javadir}/%{srcname}-junit.jar
%endif

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
