"""
credits.py

DESCRIPTION:
  Contains the classes and functions that implement JeoparPy credits.
  Includes classes CreditLine, CreditImage, MultiCreditLine,
  and SimpleCreditLine.

USAGE:
  Main should call only do_credits.
  

Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file..
"""
from sys import exit as sysexit

import pygame
from pygame.locals import QUIT, KEYDOWN, K_q

from .constants import JEOP_BLUE
from .resmaps import FONTS, IMAGES
from .util import get_anim_data, scale, shadow_text

###############################################################################
class CreditLine(pygame.sprite.DirtySprite):
    """
    Defines a DirtySprite for a line of text in a credit sequence.
    
    Should be used as a base class; if not, caller must initialize
    'image' and 'rect' attributes.

    ATTRIBUTES:
      * dirty
      * image
      * rect

    METHODS:
      * update
    """
    def __init__(self, *groups):
        super(CreditLine, self).__init__(*groups)
        self.dirty = 0
        self.image = None
        self.rect = None

    def update(self, step, scrH):
        """
        Move line in y by step. A positive step will move line
        down, a negative will move it up.

        The height of the screen, 'scrH' is used to set the dirty
        attribute; if the sprite is outside the bounds of the screen,
        it will not be drawn.
        """
        self.dirty = 0
        self.rect.y += step

        if self.rect.y <= scrH and self.rect.bottom >= 0:
            self.dirty = 1

###############################################################################
class CreditImage(CreditLine):
    """
    """
    def __init__(self, image, *groups):
        super(CreditImage, self).__init__(*groups)

        self.image = image.convert()
        self.rect = self.image.get_rect()

###############################################################################
class MultiCreditLine(CreditLine):
    """
    Defines a sprite for a single position and name section
    of a credits sequence.
    
    Either position or name can consist of multiple lines and
    will be drawn like so:
      Position    Name 1               Multi-    Name
                  Name 2        Line Position

    Usage: After initialization, set 'rect' to start position then
      call update() on every frame.
    """
    def __init__(self, width, font, position, name, *groups):
        """
        To appear on multiple lines, position and/or name must be
        a tuple, with each intended line an element.

        If position or name is a string, it will be rendered as
        a single line.
        """
        super(MultiCreditLine, self).__init__(*groups)
        if isinstance(position, basestring):
            position = (position, )
        if isinstance(name, basestring):
            name = (name, )
        
        self.image = self._create_line(width, font, position, name)
        self.rect = self.image.get_rect()
        self.dirty = 0

    #TODO This function badly needs refactoring
    def _create_line(self, width, font, position, name):
        """Return surface with credit text blitted on it."""
        spacer = pygame.Rect(0, 0, int(0.08*width), 1)
        spacer.centerx = int(width / 2)
        lineH = font.get_linesize()

        position = [(font.render(s, 1, (200, 200, 200)), s)
                    for s in position]
        name = [(font.render(s, 1, (255, 255, 255)), s)
                for s in name]

        position = [(s, s.get_rect(), text) for s, text in position]
        name = [(s, s.get_rect(), text) for s, text in name]

        sfc = pygame.Surface((width, lineH * max((len(position), len(name)))))
        sfc.fill(JEOP_BLUE)

        for i, (s, rect, text) in enumerate(position):
            rect.right = spacer.left
            rect.top = i*lineH
            sfc.blit(s, rect)

        for i, (s, rect, text) in enumerate(name):
            rect.left = spacer.right
            rect.top = i*lineH
            shadow, shadRect = shadow_text(text, rect, font,
                                           scale(3, width, 1024))

            sfc.blit(shadow, shadRect)
            sfc.blit(s, rect)

        return sfc

###############################################################################
class SimpleCreditLine(CreditLine):
    """
    Defines a line of text in a credits sequence that is a single
    string, all of the same font.
    
    Usage: After initialization, set 'rect' to start position then
      call update() on every frame.
    """
    def __init__(self, font, text, color, bgColor, shadowOffset, *groups):
        """If shadowOffset is 0 or None, no shadow will be drawn."""
        super(SimpleCreditLine, self).__init__(*groups)
        
        if shadowOffset:
            size = list(font.size(text))
            size[1] += shadowOffset
            self.image = pygame.Surface(size)
            self.image.fill(bgColor)
            line = font.render(text, 1, color)
            rect = line.get_rect()
            shadow, shadRect = shadow_text(text, rect, font, shadowOffset)
            self.image.blit(shadow, shadRect)
            self.image.blit(line, (0, 0))
        else:                        
            self.image = font.render(text, 1, color, bgColor)
            
        self.rect = self.image.get_rect()

###############################################################################
positions = ('Programmer/Designer', 'Programmer',
             'Research',
             'Research Assistant',
             'Writer',
             'Writing Consultant',
             'Legal Counsel',
             'Play Testers',
             ('Executive in', 'Charge of Play Testing'),
             ('Executive in Charge of', 'Chocolate Dipped Peanuts'),
             'Video/Photo Test Model',
             'Assistant to Ms. Madill',
             'Assistant to Mr. Madill'
             )

names = ('Adam Beagle','Tyler Spadgenske',
         'Claire Madill',
         "Starla 'Kitty Kitty' Warla",
         'Adam Beagle',
         'Claire Madill',
         'Claire Madill',
         ('Gary Madill', 'Lori Madill'),
         ('', "Toulouse 'Woosy' Madill"),
         ('', 'Adam Beagle'),
         'Livvy Lamont',
         "Giselle 'Zelly Poo Poo' Madill",
         "Presley 'Chadwick' Madill"
         )

final = ('Catering by',
         'Mancinos of Alpena, MI',
         '',
         '',
         '',
         'Brought to you by',
         'Lamonster Solutions',
         )

def do_credits(screen, clock, audioPlayer, fpsLimit):
    """Main should call this function to initiate the credit scroll."""
    scrRect = screen.get_rect()
    lineW = int(.75*scrRect.w)
    font = pygame.font.Font(FONTS['credits'], scale(30, lineW, 1024))
    lines = pygame.sprite.Group()
    startY = scrRect.h + 1
    spacer = scale(50, lineW, 1024) #Y-space between lines

    startY = _build_multi_lines(lines, font, startY, spacer, lineW, scrRect)
    finalLineBottom = _build_final_lines(lines, font,
                                         startY + scale(100, lineW, 1024),
                                         lineW,scrRect)
    
    numFrames, step, fpsLimit = get_anim_data(33.2, -1*finalLineBottom,
                                              fpsLimit)
    
    pygame.event.clear()
    audioPlayer.play('end')
    _scroll_credits(screen, scrRect, clock, lines, numFrames, step, fpsLimit)

    _blit_thanks(screen, 'Thanks for playing!', font, scrRect, lineW)
    pygame.time.delay(5000)
    pygame.quit()
    exit()

def _blit_thanks(screen, text, font, scrRect, lineW):
    thanks = font.render(text, 1, (255, 255, 255))
    rect = thanks.get_rect()
    rect.center = scrRect.center
    shadow, shadRect = shadow_text(text, rect, font, scale(3, lineW, 1024))
    
    screen.blit(shadow, shadRect)
    screen.blit(thanks, rect)
    pygame.display.update()

def _build_final_lines(group, font, startY, lineW, scrRect):
    """
    Build final line sprites and adds them to 'group.'
    Return final line's rect.bottom.
    """
    for s in final:
        if isinstance(s, pygame.Surface):
            line = CreditImage(s, group)
        else:
            line = SimpleCreditLine(font, s, (255, 255, 255),
                                      JEOP_BLUE, scale(4, lineW, 1024), group)

        line.rect.y = startY
        line.rect.centerx = scrRect.centerx
        finalLineBottom = line.rect.bottom
        startY = line.rect.bottom + scale(5, lineW, 1024)

    return finalLineBottom
    
def _build_multi_lines(group, font, startY, spacer, lineW, scrRect):
    """
    Build credit line sprites (from position and name), and add them to 
    'group.'

    Return y-value at which to start placing any further lines.
    """
    for pos, name in zip(positions, names):
        line = MultiCreditLine(lineW, font, pos, name, group)
        line.rect.y = startY
        line.rect.centerx = scrRect.centerx

        startY = line.rect.bottom + spacer

    return startY

def _scroll_credits(screen, scrRect, clock, lines, numFrames, step, fpsLimit):
    screen.fill(JEOP_BLUE)
    bg = screen.copy()
    
    for frame in xrange(numFrames):
        lines.update(step, scrRect.h)
        lines.clear(screen, bg)
        lines.draw(screen)
        pygame.display.update()
        clock.tick_busy_loop(fpsLimit)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                                      event.key == K_q):
                sysexit(1)
                
        pygame.event.pump()
