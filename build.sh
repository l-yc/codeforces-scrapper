#!/bin/sh
cp codeforces-scrapper.py LICENSE ~/rpmbuild/SOURCES/
rpmbuild -ba codeforces-scrapper.spec
cp ~/rpmbuild/RPMS/noarch/codeforces-scrapper-0.1-1.fc29.noarch.rpm .
