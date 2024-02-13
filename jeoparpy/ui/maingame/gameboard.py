"""
gameboard.py

DESCRIPTION:
    Contains the GameBoard class, described below.


Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""
from random import shuffle

import pygame

from .jeopgamesfc import JeopGameSurface
from ..constants import JEOP_BLUE
from ..resmaps import FONTS
from ..util import (autofit_text, BorderedBox, draw_centered_textblock,
                    draw_centered_textline, scale)
from ...constants import ANIMATIONEND


class GameBoard(JeopGameSurface):
    """
    The primary JeoparPy game board: categories and clue amounts on a grid.
    
    INHERITED ATTRIBUTES:
        * baseImg
        * dirty
        * rect
    """
    def __init__(self, size, gameData):
        super(GameBoard, self).__init__(size)
        self.fill((0, 0, 0))

        self._boxes = self._init_boxes(len(gameData.categories),
                                         len(gameData.amounts) + 1)

        self._blit_categories(gameData.categories)
        self._draw_all_boxes()
        
        self.baseImg = self.copy()

    def get_clicked_clue(self, clickPos):
        """
        Return 2-tuple (row, column) of clicked clue if the click position
        is inside a clue's rect, otherwise return None.
        """
        for c, col in enumerate(self._boxes):
            for r, box in enumerate(col[1:]):
                if box.rect.collidepoint(clickPos):
                    return (c, r)

        return None

    def update(self, gameState, gameData):
        gs = gameState

        if gs.state == gs.BOARD_FILL:
            self._amtFont = pygame.font.Font(FONTS['amount'], self._scale(48))
            self._coordsStack = [(c, r) for c in xrange(len(self._boxes))
                                for r in xrange(len(self._boxes[0]) - 1)]
            shuffle(self._coordsStack)
            
        elif gs.state == gs.WAIT_BOARD_FILL:
            if self._coordsStack:
                c, r = self._coordsStack.pop()
                box = self._boxes[c][r + 1]
                
                self._blit_amount(box, gameData.amounts[r])
                self.blit(box, box.rect)
                self.dirty = True
                pygame.time.wait(135)
            else:
                pygame.event.post(pygame.event.Event(ANIMATIONEND))

        elif gs.state == gs.CLUE_OPEN:
            c, r = gs.kwargs['coords']
            box = self._boxes[c][r + 1]
            box.redraw()
            self.blit(box, box.rect)
            
        elif gs.state in (gs.DELAY, gs.ANSWER_TIMEOUT, gs.ANSWER_NONE):
            self.dirty = True

    def _blit_amount(self, box, amount):
        bounds = tuple(.8*x for x in box.size)
        font = autofit_text(FONTS['amount'], self._scale(48),
                            str(amount), bounds)[1]
        
        draw_centered_textline(box, '$' + str(amount),
                               font, (217, 164, 31), 4)

    def _blit_categories(self, categories):
        shadowOffset = self._scale(3)
        bounds = tuple(.9*x for x in self._boxes[0][0].size)
        
        for i, c in enumerate(categories):
            lines, font = autofit_text(FONTS['category'], self._scale(32),
                                           c, bounds)
                                       
            draw_centered_textblock(self._boxes[i][0], lines, font,
                                    (255, 255, 255), 0, shadowOffset)

    def _draw_all_boxes(self):
        for col in self._boxes:
            for box in col:
                self.blit(box, box.rect)

    def _init_boxes(self, nCols, nRows):
        boxes = []
        size = self.rect.size
        boxW = size[0] / nCols
        boxH = size[1] / nRows
        borderW = max(self._scale(2), 1)
        catBottomBorder = 3*borderW
        rightEdgeBorder = 3*borderW

        clueBox = BorderedBox((boxW, boxH), JEOP_BLUE,
                          borderW, (0, 0, 0))

        catBox = BorderedBox((boxW, boxH), JEOP_BLUE,
                             (borderW, borderW, catBottomBorder, borderW),
                             (0, 0, 0))

        for col in xrange(nCols):
            colBoxes = []

            if col == nCols - 1:
                clueBox.borderWidths = (borderW, rightEdgeBorder,
                                        borderW, borderW)
                catBox.borderWidths = (borderW, rightEdgeBorder,
                                       catBottomBorder, borderW)
                clueBox.redraw()
                catBox.redraw()

            catBox.rect.topleft = (boxW*col, 0)
            colBoxes.append(catBox.copy())

            for row in xrange(1, nRows):
                clueBox.rect.topleft = (boxW*col, boxH*row)
                colBoxes.append(clueBox.copy())

            boxes.append(tuple(colBoxes))
        
        return tuple(boxes)

    def _init_grid(self, nCols, nRows):
        return tuple(rects)

    def _scale(self, n):
        return int(n * self.rect.height / 720.0)

    @property
    def boxSize(self):
        return self._boxes[0][0].size
