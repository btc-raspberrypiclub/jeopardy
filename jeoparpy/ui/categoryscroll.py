"""
categoryscroll.py

DESCRIPTION:
  Functions implementing part of the JeoparPy introduction sequence where
  category names scroll by, holding on each name for a set amount of time.

USAGE:
  Main should only need to call do_scroll.


Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""

import pygame

from .config import CATEGORY_HOLD_TIME
from .constants import JEOP_BLUE
from .resmaps import FONTS
from .util import (autofit_text, BorderedBox, draw_centered_textblock,
                  get_anim_data, shadow_text)
from ..config import FPS_LIMIT
from ..util import chunker

###############################################################################
def do_scroll(screen, clock, categories):
    """
    Draws a bordered box with a category name inside, holds for an amount
    of time (defined by CATEGORY_HOLD_TIME), and scrolls to next category.
    This process is repeated until all categories have been shown.

    'categories' expects container of category name strings.
    'screen' must be the primary pygame display surface.
    """
    scrSize = screen.get_size()
    boxes = tuple(_build_box(scrSize, c) for c in categories)
    numFrames, step, fpsLimit = get_anim_data(1.0, scrSize[0], FPS_LIMIT)

    #Hold on each box, then scroll
    for box, nextBox in chunker(boxes, 2, True):
        _blit_to_screen_and_update(screen, box)
        pygame.time.delay(CATEGORY_HOLD_TIME)
        _animate_scroll(screen, scrSize, clock, box, nextBox, step, fpsLimit)

    #Draw final box and hold
    _blit_to_screen_and_update(screen, boxes[-1])
    pygame.time.delay(CATEGORY_HOLD_TIME)
                        
###############################################################################
def _animate_scroll(screen, scrSize, clock, box1, box2, step, fpsLimit):
    """
    Scrolls box to the left, filling in space with box2 until
    box2 fills the screen. The boxes must be surfaces.
    'step' is the amount in pixels to shift the boxes on
    each animation step.
    """
    w, h = scrSize
    offset = step

    while offset <= w:
        #Update showing areas
        area1 = pygame.Rect(offset, 0, w - offset, h)
        area2 = pygame.Rect(0, 0, offset, h)

        #Blit and update
        screen.blit(box1, (0, 0), area1)
        screen.blit(box2, (w - offset, 0), area2)
        pygame.display.update()

        #Increment offset and tick clock/fps limiter
        offset += step
        clock.tick_busy_loop(fpsLimit) 

def _blit_to_screen_and_update(screen, sfc):
    screen.blit(sfc, (0, 0))
    pygame.display.update()

def _build_box(size, category):
    """
    Return surface containing centered category text and a black border.
    'size' is size of surface to create.
    """
    borderW = _scale(33, size[1])
    box = BorderedBox(size, JEOP_BLUE, borderW, (0, 0, 0))
    
    lines, font = autofit_text(FONTS['category'], _scale(150, size[1]),
                               category, tuple(.8*x for x in size))

    draw_centered_textblock(box, lines, font,
                            (255, 255, 255), 0, _scale(7, size[1]))

    return box

def _scale(n, rel):
    return  int(n * (rel / 720.0))

###############################################################################
if __name__ == '__main__':
    #Test run
    pygame.init()
    categories=('cat 1', 'cat 2', 'cat 3')
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    screen.fill((0, 0, 0))
    do_scroll(screen, clock, categories)
