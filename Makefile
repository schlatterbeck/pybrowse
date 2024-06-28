PKG=pybrowse
PY=pybrowse.py __init__.py
SRC=Makefile setup.py $(PY:%.py=pybrowse/%.py) $(README) README.html

ifeq (,${RELEASETOOL})
    RELEASETOOL=../releasetool
endif

VERSIONPY=pybrowse/Version.py
VERSIONTXT=VERSION
VERSION=$(VERSIONPY) $(VERSIONTXT)
README=README.rst
LASTRELEASE:=$(shell ../svntools/lastrelease -n)

all: $(VERSION)

$(VERSION): $(SRC)

clean:
	rm -f MANIFEST README.html default.css \
	    ${VERSION} pybrowse/Version.pyc ${CHANGES} ${NOTES}
	rm -rf dist build *.egg-info __pycache__ pybrowse/__pycache__

include ${RELEASETOOL}/Makefile-pyrelease
