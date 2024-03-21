"""
clueanimation.py

DESCRIPTION:
    Contains the OpenClueAnimation class, described in detail below.


Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""
import pygame

from ..constants import JEOP_BLUE
from ...constants import ANIMATIONEND

###############################################################################
class OpenClueAnimation(pygame.sprite.DirtySprite):
    """
    A sprite that animates a clue box filling up the screen.

    ATTRIBUTES:
      * dirty
      * image
      * rect

    METHODS:
      * update
    """
    def __init__(self, startSize, endRect, fps):
        """
        'eventcode' is pygame event type value for an event
        that signals this sprites animation has concluded.
        """
        super(OpenClueAnimation, self).__init__()
        self.rect = pygame.Rect((0, 0), startSize) # Positioned in _init_rects
        self.dirty = 0
        
        size = self.rect.size
        self.image = pygame.Surface(size)
        self.image.fill(JEOP_BLUE)
        
        self._startSize = size
        self._startRect = None  # See _init_rects()
        self._moveAmts = None   # See _init_rects()
        self._endRect = endRect
        self._eventCode = ANIMATIONEND
        self._frameGoal = self._get_frame_goal(fps, 0.5)
        self._frame = 0

    def update(self, gameState, gameData):
        """Update the sprite based on the current game state/data"""
        gs = gameState

        if gs.state == gs.CLICK_CLUE:
            self._init_rects(gs.kwargs['coords'])
            
        if gs.state == gs.WAIT_CLUE_OPEN:
            if self._is_animation_done():
                self._reset()
                pygame.event.post(pygame.event.Event(self._eventCode))
            else:
                self._step_animation()
                self.dirty = True

    def _get_completion_percent(self):
        """Return percent of animation complete as float"""
        return float(self._frame) / self._frameGoal
            
    def _get_frame_goal(self, fps, goalTime):
        """
        Return number of frames necesary to accomplish animation in
        'goalTime' seconds based on fps.
        """
        return int(fps * goalTime)

    def _init_rects(self, clueCoords):
        """
        Initialize three attributes:
          self.rect, from clue coordinates and known start size
          self._startRect, a copy of self.rect in its initial state
          self._dii
        """
        sw, sh = self._startSize
        x = 0
        y = sh # Compensates for category row

        x = sw * clueCoords[0]
        y += sh * clueCoords[1]

        self.rect = pygame.Rect(x, y, sw, sh)
        self._startRect = self.rect.copy()

        self._moveAmts = tuple(self._endRect[i] - self.rect[i]
                               for i in range(4))

    def _is_animation_done(self):
        return self._frame == self._frameGoal

    def _reset(self):
        """Reset sprite to prepare for next clue opened."""
        self._frame = 0
        self._startRect = None
        self.rect = None
        self._moveAmts = None

    def _step_animation(self):
        """Do one step of opening animation."""
        self._frame += 1
        perc = self._get_completion_percent()
        
        for i, c in enumerate(self.rect):
            self.rect[i] = int(self._startRect[i] + perc * self._moveAmts[i])
                    
        self.image = pygame.transform.scale(self.image, self.rect.size)
