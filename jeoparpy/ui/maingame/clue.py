"""
clue.py

DESCRIPTION:
    Contains the Clue class, described below.


Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""
import pygame

from .jeopgamesfc import JeopGameSurface
from .util import Timer
from ..constants import JEOP_BLUE
from ..resmaps import FONTS, IMAGES
from ..util import (autofit_text, draw_centered_textblock, draw_textblock,
                    fit_image, get_size_textblock, restrict_fontsize, scale)
from ...config import CLUE_TIMEOUT_MS
from ...constants import ANSWER_TIMEOUT

##############################################################################
class ClueTimer(Timer):
    """
    Automatically posts ANSWER_TIMEOUT to the event queue if CLUE_TIMEOUT_MS
    pass since the START_CLUE_TIMER state was reached.
    
    Clue should call update() on every frame from its update() method.
    """
    def __init__(self):
        super(ClueTimer, self).__init__(CLUE_TIMEOUT_MS, ANSWER_TIMEOUT)
    
    def update(self, gameState):
        gs = gameState
        
        if gs.state == gs.START_CLUE_TIMER:
            self.start()
        elif gs.state == gs.BUZZ_IN:
            self.reset()
            
        super(ClueTimer, self).update()

###############################################################################
class Clue(JeopGameSurface):
    """
    Defines a surface containing a written JeoparPy clue.
    
    ATTRIBUTES:
      * dirty

    METHODS:
      * draw_clue
      * update
    """
    def __init__(self, size):
        super(Clue, self).__init__(size)
        self._maxFontSize = scale(51, size[1], 720)
        self._defaultFont = pygame.font.Font(FONTS['clue'], self._maxFontSize)
        self.dirty = False
        
        # Timer will be None if CLUE_TIMEOUT_MS None or <= 0
        self._timer = ClueTimer() if CLUE_TIMEOUT_MS > 0 else None
        
    def draw_clue(self, clueLines, img=None):
        self.fill(JEOP_BLUE)

        if img:
            textBounds = tuple(s*x for s, x in zip((.9, .66), self.size))
            text = self._draw_clue_text(clueLines, textBounds)
            self._draw_clue_and_image(text, img)
        else:
            text = self._draw_clue_text(clueLines)
            textrect = text.get_rect()
            textrect.center = self.rect.center
            self.blit(text, textrect)
            
    def update(self, gameState, gameData):
        gs = gameState
        
        if self._timer is not None:
            self._timer.update(gameState)

        if gs.state == gs.CLUE_OPEN:
            cat, clue = gs.kwargs['coords']
            img = self._get_media((cat, clue))
            self.draw_clue(gameData.clues[cat][clue], img)
            self.dirty = True

    def _draw_clue_and_image(self, textsfc, img):
        textrect = textsfc.get_rect()
        spacer = scale(10, self.size[1], 720)
        imgBounds = (.98*self.size[0], self.size[1] - (3*spacer + textrect.h))
        img = fit_image(img, imgBounds)
        imgrect = img.get_rect()

        allrect = pygame.Rect(0, 0, self.rect.w,
                              3*spacer + textrect.h + imgrect.h)
        allrect.center = self.rect.center

        textrect.centerx = self.rect.centerx
        textrect.y = spacer + allrect.y

        imgrect.centerx = self.rect.centerx
        imgrect.y = allrect.y + 2*spacer + textrect.h

        self.blit(textsfc, textrect)
        self.blit(img, imgrect)
                   
    def _draw_clue_text(self, clueLines, bounds=None):
        if len(clueLines) == 1:
            if not bounds:
                bounds = tuple(.85*x for x in self.size)
            clueLines, font = autofit_text(FONTS['clue'], self._maxFontSize,
                                           clueLines[0], bounds)
        else:
            if not bounds:
                bounds = tuple(.95*x for x in self.size)
            fsize = restrict_fontsize(FONTS['clue'], self._maxFontSize,
                                      clueLines, bounds)
            font = pygame.font.Font(FONTS['clue'], fsize)

        size = get_size_textblock(clueLines, font, 0)
        sfc = pygame.Surface(size)
        sfc.fill(JEOP_BLUE)
            
        draw_centered_textblock(sfc, clueLines, font, (255, 255, 255), 0,
                                scale(4, self.size[1], 720))

        return sfc
        
    def _get_media(self, coords):
        if coords in IMAGES:
            img = pygame.image.load(IMAGES[coords]).convert()
            scaledSize = (scale(x, self.size[1], 720)
                          for x in img.get_size())
            return pygame.transform.smoothscale(img, tuple(scaledSize))

        return None
        