"""
podiapanel.py

DESCRIPTION:
    Contains the PodiaPanel class and its utility classes,
    described in detail below.


Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""
import pygame

from .jeopgamesfc import JeopGameSurface
from .podium import Podium
from ..resmaps import FONTS, IMAGES


class PodiaPanel(JeopGameSurface):
    """
    The JeoparPy panel containing the three player podiums.
    When initialized, a background image, and the three podia
    with player names and $0 are drawn.
    A 'highlight' ability exists for when players buzz in.

    Calling the update() function on every frame with a GameState and
    GameData object will automatically update the surface as needed.

    The surface should be redrawn when its 'dirty' attribute is True;
    the caller is responsible for resetting it to False.

    INHERITED ATTRIBUTES:
      * baseImg
      * dirty
      * rect
      * size (read-only)

    METHODS:
      * update
    """
    def __init__(self, size, gameData):
        """
        Initialize the panel with a background and the three podia with 
        team names and scores of '$0'
        """
        super(PodiaPanel, self).__init__(size)
        scalar = self._init_background()
        self._podia = self._init_podia(gameData, scalar)
        self.dirty = 1
        self._podia.draw(self)
        
    def update(self, gameState, gameData):
        """
        Update all visuals on the surface. If any changes were made,
        set 'dirty' to True. This method should be called once per frame.
        """
        self._podia.update(gameState, gameData)
        for p in self._podia:
            if p.dirty:
                self.blit(p.image, p.rect)
                p.dirty = 0
                self.dirty = 1

        if gameState.state == gameState.DELAY:
            pygame.time.wait(500)
            

    def _init_background(self):
        img = pygame.image.load(IMAGES['rPanelBG']).convert()
        sizeScalar = float(self.size[1]) / img.get_size()[1]
        img = pygame.transform.scale(img, self.size)
        self.blit(img, (0, 0))

        return sizeScalar

    def _init_podia(self, gameData, scalar):
        podia = pygame.sprite.OrderedUpdates()
        img = pygame.image.load(IMAGES['podium']).convert_alpha()
        nameBounds = pygame.Rect(90, 107, 102, 105)
        fonts = (('team1', 42), ('team2', 33), ('team3', 40))
        fonts = tuple((FONTS[n], s) for n,s in fonts)

        for i in xrange(3):
            p = Podium(i, img, scalar, gameData.players[i].name,
                       fonts[i], nameBounds, podia)

        return self._position_podia(podia)

    def _position_podia(self, podia):
        ph = podia.sprites()[0].rect.h
        padding = (self.size[1] - 3*ph) / 4
        y = padding

        for p in podia:
            p.rect.centerx = self.rect.centerx
            p.rect.y = y
            y += ph + padding

        return podia
