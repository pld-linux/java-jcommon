#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_without	tests		# don't build and run tests
#
%include	/usr/lib/rpm/macros.java
Summary:	Common library for Object Refinery Projects
Summary(pl.UTF-8):	Biblioteka wspólna dla projektów Object Refinery
Name:		jcommon
Version:	1.0.12
Release:	0.2
Epoch:		0
License:	LGPL
Group:		Development/Languages/Java
Source0:	http://dl.sourceforge.net/jfreechart/%{name}-%{version}.tar.gz
# Source0-md5:	7fbb41dfcf6dba36f10ec7d89d1dd3f7
URL:		http://www.jfree.org/jcommon/index.html
BuildRequires:	ant
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	junit
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Collection of classes used by Object Refinery Projects, for example
jfreechart.

%description -l pl.UTF-8
Zbiór klas używanych przez projekty Object Refinery, jak na przykład
jfreechart.

%package test
Summary:	Test tasks for %{name}
Summary(pl.UTF-8):	Zadania testowe dla pakietu %{name}
Group:		Development/Languages/Java
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	junit

%description test
All test tasks for %{name}.

%description test -l pl.UTF-8
Wszystkie zadania testowe dla pakietu %{name}.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja Javadoc do pakietu %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l fr.UTF-8
Javadoc pour %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja Javadoc do pakietu %{name}.

%prep
%setup -q
# remove all binary libs
find . -name '*.jar' | xargs rm -v

%build
export CLASSPATH=$(build-classpath junit)
export LC_ALL=en_US # source code not US-ASCII
%ant -f ant/build.xml -Dbuildstable=true -Dproject.outdir=. -Dbasedir=. \
	compile %{?with_tests:compile-junit-tests} %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d $RPM_BUILD_ROOT%{_javadir}
install %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
%if %{with tests}
install lib/%{name}-%{version}-junit.jar $RPM_BUILD_ROOT%{_javadir}
ln -s %{name}-%{version}-junit.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-junit.jar
%endif

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc README.txt
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar

%if %{with tests}
%files test
%defattr(644,root,root,755)
%{_javadir}/%{name}-%{version}-junit.jar
%{_javadir}/%{name}-junit.jar
%endif

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif
