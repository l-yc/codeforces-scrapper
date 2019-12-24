Name:           codeforces-scrapper
Version:        0.1
Release:        1%{?dist}
Summary:        GUI to search for codeforces user by handle

License:        MIT
URL:            https://github.com/l-yc/%{name}

Requires:       python3 python3-tkinter python3-requests python3-pillow python3-pillow-tk

BuildArch:      noarch

%description
GUI to search for codeforces user by handle

%prep


%build


%install
mkdir -p %{buildroot}/%{_bindir}
install -m 0755 %{_sourcedir}/%{name}.py %{buildroot}/%{_bindir}/%{name}


%files
#%license LICENSE
%{_bindir}/%{name}
