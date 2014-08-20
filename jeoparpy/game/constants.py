"""
constants.py

DESCRIPTION:
  Defines constants required by multiple game modules.


Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""
from os import path

from ..constants import ROOT_PATH

file = open(path.join(ROOT_PATH, 'jeoparpy', 'dir.txt'), 'r')
directory = file.readline()

_textPath = path.join(ROOT_PATH, 'games', directory, '')

AMOUNTS_PATH = _textPath + 'amounts.txt'
CLUES_PATH = _textPath + 'clues.txt'
CATEGORIES_PATH = _textPath + 'categories.txt'
PLAYERS_PATH = _textPath + 'players.txt'
