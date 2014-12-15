"""
constants.py

DESCRIPTION:
  Defines constants required by multiple multiple modules and subpackages.


Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""
from os import pardir, path

from pygame.locals import USEREVENT

ROOT_PATH = path.abspath(path.join(path.dirname(__file__), pardir))

# Custom events
ANIMATIONEND = USEREVENT
ANSWER_TIMEOUT = USEREVENT + 1
AUDIOEND = USEREVENT + 2

# Flags corresponding to args that can be provided to start.py
# These must have distinct values
FULLSCREEN_FLAG = 0
WINDOWED_FLAG = 1
DEBUG_FLAG = 2
SKIP_INTRO_FLAG = 3
DRIVE_FLAG = 4
