# Copyright (c) Moshe Zadka
# See LICENSE for details.
import os
import sys

up = os.path.dirname(os.path.dirname(__file__))
sys.path.append(up)

import middlefield

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]
master_doc = 'index'
project = 'Middlefield'
copyright = '2018, Moshe Zadka'
author = 'Moshe Zadka'
version = middlefield.__version__
release = middlefield.__version__
