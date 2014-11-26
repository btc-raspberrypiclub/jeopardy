"""
resmaps.py

DESCRIPTION:
  Provides maps that link descriptive names
  to absolute paths to resource files.

  If changes are made to resource file or folder names,
  this is the only file that needs to be updated,
  assuming the names by which the files are referred are not
  altered in this file.


Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""
from os import path

from ..constants import ROOT_PATH

_fontPath = path.join(ROOT_PATH, 'res', 'fonts', '')
_imgPath = path.join(ROOT_PATH, 'res', 'images', '')
_sndPath = path.join(ROOT_PATH, 'res', 'sounds', '')
_cluesPath = path.join(ROOT_PATH, 'res', 'sounds', 'clues', '')

###############################################################################
# INSTRUCTIONS TO ADD YOUR OWN IMAGES:
#=======================================
# To use your own image file in a clue, it must be added to IMAGES below.
#
# 1) Place your image file in the <jeoparpy root>/res/images folder.
#
# 2) Take note of your image's name and file extension.
#    Note that .png files are recommended, but several other common formats
#    are supported.
#
# 3) Add a line inside the brackets of IMAGES below in the following format:
#        (column, row) : _imgPath + 'filename.ext',
#
#    3a) (column, row) is the location on the game board of the desired clue.
#         Note that both are 0-based, so coordinates of the upper-left clue
#         are (0, 0). See the chart below for a visual example.
#
#    3b) Replace 'filename.ext' (don't remove the quotes) with the
#        filename and extension of your image.
#
# 4) Make sure to delete the sample lines below
#    (those that assign 'test_img.png'). 
#
#
# For a 5x5 board, these are the (column, row) values:
#        CATEGORY | CATEGORY | CATEGORY | CATEGORY | CATEGORY
#       ----------|----------|----------|----------|----------
#         (0, 0)  |  (1, 0)  |  (2, 0)  |  (3, 0)  |  (4, 0)
#         (0, 1)  |  (1, 1)  |  (2, 1)  |  (3, 1)  |  (4, 1)
#         (0, 2)  |  (1, 2)  |  (2, 2)  |  (3, 2)  |  (4, 2)
#         (0, 3)  |  (1, 3)  |  (2, 3)  |  (3, 3)  |  (4, 3)
#         (0, 4)  |  (1, 4)  |  (2, 4)  |  (3, 4)  |  (4, 4)


# WARNING: If creating your own game, delete the sample lines in this
#          dictionary. If not using clue images, change the line
#          below to: IMAGES = {}
IMAGES = {}

###############################################################################
# INSTRUCTIONS TO ADD YOUR OWN RECORDED CLUE READINGS OR AUDIO CLUES:
#====================================================================
# To use your own recorded clue readings, their audio files must be added
# to CLUES_READS below, using the following instructions.
#
# To have an audio clue, add your audio file to SOUNDS below, using the
# following instructions.
#
# 1) Your audio must be at a sample rate of 22050 Hz, and must be
#    a .wav or .ogg file (the latter is a limitation of Pygame).
#
# 2) Place audio files for clue readings in <jeoparpy root>/res/sounds/clues/
#    Place audio files for audio clues in <jeoparpy root>/res/sounds/
#
# 3) For clue readings, add a line to CLUE_READS below in the following format:
#        (column, row) : _cluesPath + 'filename.ext',
#
#    For audio clues, add a line to SOUNDS below in the following format:
#        (column, row) : _sndPath + 'filename.ext',
#
#    3a) (column, row) is the location on the game board of the desired clue.
#         Note that both are 0-based, so coordinates of the upper-left clue
#         are (0, 0). See the chart in the IMAGES instructions above
#         for help.
#
#    3b) Replace 'filename.ext' (don't remove the quotes) with the
#        filename and extension of your audio file.
#
# 4) Make sure to delete the sample lines below
#    (those that assign 'sample_read.ogg' or 'sample_music.ogg'). 
#


# WARNING: If creating your own game, delete the sample lines in this
#          dictionary. If not using audio clue readings, change the line
#          below to: CLUE_READS = {}
CLUE_READS = {}

# WARNING: If creating your own game, delete the sample lines in this
#          dictionary. If not using audio clues, change the line below
#          to: SOUNDS = {}
SOUNDS = {}



###############################################################################
# WARNING: Alter anything below at your own risk.
FONTS = {'title'    : _fontPath + 'gyparody.ttf',
         'rules'    : _fontPath + 'korinab.ttf',
         'category' : _fontPath + 'impact.ttf',
         'amount'   : _fontPath + 'impact.ttf',
         'congrats' : _fontPath + 'gyparody.ttf',
         'team1'    : _fontPath + 'team1.ttf',
         'team2'    : _fontPath + 'team2.ttf',
         'team3'    : _fontPath + 'team3.ttf',
         'score'    : _fontPath + 'korinna-extrabold.ttf',
         'clue'     : _fontPath + 'korinab.ttf',
         'subtitle' : _fontPath + 'impact.ttf',
         'credits'  : _fontPath + 'korinab.ttf'
        }

IMAGES.update({'introBG'     : _imgPath + 'introbg.png',
               'rPanelBG'    : _imgPath + 'podiabg.png',
               'podium'      : _imgPath + 'podium.png',
               'highlight'   : _imgPath + 'highlight.png',
               'lamonster'   : _imgPath + 'livvy.png',
               'podtimer'    : _imgPath + 'timer.png'
               })

SOUNDS.update({'intro'     : _sndPath + 'intro.ogg',
          'fill'      : _sndPath + 'fill.ogg',
          'buzz'      : _sndPath + 'buzz.ogg',
          'wrong'     : _sndPath + 'wrong.wav',
          'outoftime' : _sndPath + 'outoftime.wav',
          'end'       : _sndPath + 'end.ogg',
          'applause'  : _sndPath + 'applause.wav'
          })
