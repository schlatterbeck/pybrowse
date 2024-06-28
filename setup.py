#!/usr/bin/env python
# Copyright (C) 2010-24 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA
# ****************************************************************************

import os.path
from setuptools import setup

if os.path.exists ("VERSION"):
    with open ("VERSION", 'r', encoding="utf8") as f:
        __version__ = f.read ().strip ()
else:
    __version__ = '0+unknown'

with open ('README.rst', encoding = 'utf-8') as f:
    description = f.read ()

license = 'MIT License'

setup \
    ( name             = "pybrowse"
    , version          = __version__
    , description      = "webrowse replacement: send html or text to browser"
    , long_description = ''.join (description)
    , license          = license
    , author           = "Ralf Schlatterbeck"
    , author_email     = "rsc@runtux.com"
    , install_requires = ['rsclib']
    , packages         = ['pybrowse']
    , package_dir      = { 'pybrowse' : '' }
    , platforms        = 'Any'
    , entry_points     = dict
        ( console_scripts = ['pybrowse=pybrowse.pybrowse:main']
        )
    )
