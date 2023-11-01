%global bundle  org.apache.felix.scr

Name:          felix-scr
Version:       2.1.16
Release:       6%{?dist}
Summary:       Apache Felix Service Component Runtime (SCR)
License:       ASL 2.0
URL:           http://felix.apache.org/documentation/subprojects/apache-felix-service-component-runtime.html

Source0:       http://archive.apache.org/dist/felix/%{bundle}-%{version}-source-release.tar.gz

# Don't embed deps, use import-package instead
Patch0: 0001-Use-import-package-instead-of-embedding-dependencies.patch

# Drop dep on kxml/xpp, use the system SAX implementation instead
Patch1: 0002-Drop-the-dependencies-on-kxml-xpp3.patch

# SCL-specific sources
Source100: osgi.cmpn.tar.gz

BuildArch:     noarch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:felix-parent:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.felix:org.apache.felix.gogo.runtime)
BuildRequires:  mvn(org.osgi:osgi.annotation)
BuildRequires:  mvn(org.osgi:osgi.cmpn)
BuildRequires:  mvn(org.osgi:osgi.core)

%description
Implementation of the OSGi Declarative Services Specification Version 1.3 (R6).

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{bundle}-%{version}
%patch0 -p1
%patch1 -p1

# All these OSGi deps are provided in the compendium jar
%pom_add_dep org.osgi:osgi.cmpn:7.0.0:provided
%pom_remove_dep org.osgi:org.osgi.service.component
%pom_remove_dep org.osgi:org.osgi.service.cm
%pom_remove_dep org.osgi:org.osgi.service.log
%pom_remove_dep org.osgi:org.osgi.service.metatype
%pom_remove_dep org.osgi:org.osgi.namespace.extender
%pom_remove_dep org.osgi:org.osgi.util.promise
%pom_remove_dep org.osgi:org.osgi.util.function

# Many test deps are not in Fedora
%pom_xpath_remove "pom:project/pom:dependencies/pom:dependency[pom:scope='test']"
%pom_remove_dep org.ops4j.base:
%pom_remove_plugin :maven-failsafe-plugin

# Animal sniffer is unnecessary since we always know JRE level on Fedora
%pom_remove_dep :animal-sniffer-annotations
sed -i -e '/IgnoreJRERequirement/d' src/main/java/org/apache/felix/scr/impl/manager/ThreadDump.java

%mvn_file : felix/%{bundle}

# Extract SCL-specific sources
tar xf %{SOURCE100}

%build
# No test deps availables e.g org.ops4j.pax.url:pax-url-wrap
%mvn_build --xmvn-javadoc -f -- -Dfelix.java.version=7

%install
%mvn_install

%files -f .mfiles
%doc changelog.txt
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 2.1.16-6
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue Jun 16 2020 Jie Kang <jkang@redhat.com> - 2.1.16-5
- Build javadoc with --xmvn-javadoc

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Mat Booth <mat.booth@redhat.com> - 2.1.16-3
- Drop requirement on kxml and xpp, patch to use the JDK SAX implementation
  instead

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 06 2019 Mat Booth <mat.booth@redhat.com> - 2.1.16-1
- Update to latest upstream release for OSGi R7 support

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Mat Booth <mat.booth@redhat.com> - 2.0.14-2
- Rebuilt

* Thu Apr 26 2018 Mat Booth <mat.booth@redhat.com> - 2.0.14-1
- Update to latest upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Roland Grunberg <rgrunber@redhat.com> - 2.0.12-1
- Update to latest upstream release.
- Resolves rhbz#1455048.

* Fri Jun 16 2017 Mat Booth <mat.booth@redhat.com> - 2.0.10-2
- Remove SCL macros forbidden in Fedora
- Avoid bundling org.osgi classes

* Tue May 16 2017 Mat Booth <mat.booth@redhat.com> - 2.0.10-1
- Update to latest upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 02 2017 Mat Booth <mat.booth@redhat.com> - 2.0.8-1
- Update to latest upstream release
- Regenerate BRs and ensure there is an R on kxml
- Actually use license macro

* Thu Feb 04 2016 Severin Gehwolf <sgehwolf@redhat.com> - 1.6.2-6
- Add dep on xpp3 since it's now unbundled from kxml2. See RHBZ#1299774.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep 10 2015 jkang@redhat.com - 1.6.2-4
- SCL-ize package

* Wed Jul 08 2015 jkang@redhat.com - 1.6.2-3
- Added LICENSE and NOTICE files

* Wed Jun 17 2015 Jie Kang <jkang@redhat.com> - 1.6.2-2
- Changed to vcs source as tarball no longer available

* Sun Oct 06 2013 gil cattaneo <puntogil@libero.it> 1.6.2-1
- initial rpm