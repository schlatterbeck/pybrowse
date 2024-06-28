PKG=pybrowse
PY=pybrowse.py
SRC=Makefile $(PY)

ifeq (,${RELEASETOOL})
    RELEASETOOL=../releasetool
endif

VERSIONPY=Version.py
VERSIONTXT=VERSION
VERSION=$(VERSIONPY) $(VERSIONTXT)
README=README.rst
LASTRELEASE:=$(shell ../svntools/lastrelease -n)

all: $(VERSION)

$(VERSION): $(SRC)

clean:
	rm -f MANIFEST README.html default.css \
	    Version.py Version.pyc ${CHANGES} ${NOTES}
	rm -rf dist build

include ${RELEASETOOL}/Makefile-pyrelease
