PKG=pybrowse
PY=pybrowse.py
SRC=Makefile $(PY)

ifeq (,${RELEASETOOLS})
    RELEASETOOLS=../releasetools
endif

VERSIONPY=Version.py
VERSION=$(VERSIONPY)
LASTRELEASE:=$(shell ../svntools/lastrelease -n)

all: $(VERSION)

$(VERSION): $(SRC)

clean:
	rm -f MANIFEST README.html default.css \
	    Version.py Version.pyc ${CHANGES} ${NOTES}
	rm -rf dist build

include ${RELEASETOOLS}/Makefile-sf
