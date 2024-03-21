"""
util.py

DESCRIPTION:
  Functions and classes common to multiple ui modules and subpackages.

Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""
import sys

import pygame
from pygame.locals import *

from ..util import to_numeric

###############################################################################
class _Size(tuple):
    """
    WARNING: Designed for use only in this module.

    A subclass of tuple that redefines the default comparison operators of
    tuple; The given comparison between EVERY element and its corresponding
    element in the compared tuple must return True for the comparison on
    the Size objects to return True.

    Examples (assume all are _Size objects):
      (1, 1) < (2, 2) --> True
      (1, 2) < (2, 2) --> False
      (1, 2) <= (2, 2) --> True
      (3, 1) < (2, 2) --> False
    """
    def __ge__(self, other):
        for i, n in enumerate(self):
            if n < other[i]:
                return False

        return True

    def __le__(self, other):
        for i, n in enumerate(self):
            if n > other[i]:
                return False

        return True

    def __gt__(self, other):
        for i, n in enumerate(self):
            if n <= other[i]:
                return False

        return True
    
    def __lt__(self, other):
        for i, n in enumerate(self):
            if n >= other[i]:
                return False

        return True

###############################################################################
def autofit_text(fontPath, fontSize, text, bounds, spacing=0):
    """
    Fit a length of text into a block whose size is defined by 'bounds'.
    Lines of text will contain as many words as will fit the width of
    'bounds' when rendered with font defined by fontPath and fontSize.
    The font size of the entire block is then scaled to guarantee the block's
    height fits within that of bounds.

    Return lines of text to render and the pygame.font.Font object with
    which to render them. It is recommended to then call one of the
    draw_textblock functions in this module with the returned values.
    """
    lines = []
    words = text.split(' ')
    font = pygame.font.Font(fontPath, fontSize)

    # Create lines; lines contain as many words as will fit within width
    # of bounds.
    while words:
        line = words.pop(0)
        while (words and
               font.size(line)[0] + font.size(' ' + words[0])[0] <= bounds[0]):
            line += ' ' + words.pop(0)
            
        lines.append(line)

    # Call restrict_fontsize again to guarantee height of textblock defined
    # by lines does not exceed height of bounds.
    fontSize = restrict_fontsize(fontPath, fontSize, lines, bounds, spacing)

    return (lines, pygame.font.Font(fontPath, fontSize))

def draw_centered_textblock(sfc, lines, font, color, spacing=0,
                            shadowOffset=None, textAlignCenter=True):
    """
    Blit lines of text in 'lines' argument centered onto surface 'sfc.'
    Return pygame.Rect of drawn block relative to sfc.
    """
    blockRect = pygame.Rect((0, 0), get_size_textblock(lines, font, spacing))
    blockRect.center = sfc.get_rect().center

    return draw_textblock(sfc, lines, font, color, blockRect.topleft,
                          textAlignCenter, spacing, shadowOffset)
        
def draw_centered_textline(sfc, text, font, color, shadowOffset=None):
    """
    Blit line of text in 'text' argument centered onto surface 'sfc.'
    Return pygame.Rect of drawn line relative to sfc.
    """
    rect = pygame.Rect((0, 0), font.size(text))
    rect.center = sfc.get_rect().center
    draw_textline(sfc, text, font, color, rect, shadowOffset)

    return rect

def draw_textblock(sfc, lines, font, color, pos, centerx=False,
                   spacing=0, shadowOffset=None):
    """
    Blit lines of text in 'lines' argument centered onto surface 'sfc.'
    Return pygame.Rect of drawn block relative to sfc.
    """
    blockRect = pygame.Rect(pos, get_size_textblock(lines, font, spacing))
    lineH = font.get_linesize()

    for i, line in enumerate(lines):
        rect = pygame.Rect((0, 0), font.size(line))
        if centerx:
            rect.centerx = blockRect.centerx
        else:
            rect.x = blockRect.x
        rect.y = blockRect.y + lineH*i

        draw_textline(sfc, line, font, color, rect, shadowOffset)

    return blockRect

def draw_textline(sfc, text, font, color, rect, shadowOffset=None):
    """
    Blit text in 'text' onto surface 'sfc.'
    Use position of 'rect' (top left) to position blit.
    """
    s = text
    doShadow = shadowOffset is not None
    text = font.render(s, 1, color)

    if doShadow:
        shadow, shadRect = shadow_text(s, rect, font, shadowOffset)
        sfc.blit(shadow, shadRect)

    sfc.blit(text, rect)

def fit_image(img, bounds):
    """
    Return img smoothscaled to be within size given by 'bounds.'
    'img' is unchanged if it is not larger than bounds in either dimension.
    """
    rect = img.get_rect()
    wscalar = float(bounds[0]) / rect.w
    hscalar = float(bounds[1]) / rect.h

    scalar = min(wscalar, hscalar)
    if scalar < 1:
        scaledSize = tuple(int(scalar*x) for x in rect.size)
        img = pygame.transform.smoothscale(img, scaledSize)

    return img

def get_anim_data(goalTime, distance, globalFPSLimit):
    """
    Return number of frames, step size (in pixels), and FPS limit that will
    translate a surface 'distance' pixels in as close to 'goalTime' seconds
    as possible.
    
    Returned FPS limit guaranteed to not exceed globalFPSLimit.
    A negative 'distance' will result in a negative step size.
    """
    step = 1
    maxNumFrames = int(goalTime * globalFPSLimit)

    while abs(distance / step) > maxNumFrames:
        step += 1

    if distance < 0:
        step = -step
        
    numFrames = distance / step

    return numFrames, step, int(round(numFrames / goalTime))
    
def get_size_textblock(lines, font, spacing):
    """
    Return dimensions needed to render 'lines' of text
    in passed font, with 'spacing' pixels between each line.
    """
    blockW = 0
    blockH = 0

    if isinstance(lines, str):
        lines = [lines]

    for line in lines:
        w, h = font.size(line)
        blockW = max(blockW, w)
        blockH += h + spacing

    return (blockW, blockH)

def restrict_fontsize(fontPath, size, lines, bounds, spacing=0):
    """
    Return largest font size <= 'size' for which a block of text given by
    'lines,' rendered with font given by 'fontName,' is guaranteed to not
    exceed size given by 'bounds' in either dimension.

    'spacing' is the amount of space in pixels between each line.
    """
    bounds = _Size(bounds)
    while not _Size(get_size_textblock(lines,
                                       pygame.font.Font(fontPath, size),
                                       spacing)) < bounds:
        size -= 1

    return size

def scale(n, rel, comp):
    return int(n * (rel / float(comp)))

def shadow_text(msg, srcRect, font, offset, color=(0, 0, 0)):
    """
    Return surface and rect of shadowed text.
    Shadow is positioned 'offset' pixels right and down from srcRect.
    'msg' is string to shadow.
    """
    shadText = font.render(msg, 1, color)
    rect = shadText.get_rect()

    rect.x = srcRect.x + offset
    rect.y = srcRect.y + offset
    
    return shadText, rect

def wait_for_keypress(key=None):
    """
    By default, return control when any key is pressed.
    If one key constant or list is passed, return only when 
    one of those keys is pressed.
    """
    if not key == None and not isinstance(key, collections.Iterable):
        key = [key]

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if key and event.key in key:
                    return
                elif not key:
                    return

            if event.type == QUIT:
                sys.exit()

        pygame.event.pump()
        
###############################################################################
class BorderedBox(pygame.Surface):
    """
    A pygame.Surface box with a customizable border.

    ATTRIBUTES:
      * borderColor
      * borderWidths
      * fillColor
      * rect
      * size (read-only)

    METHODS:
      * copy
      * redraw
    """
    def __init__(self, size, fillColor, borderW, borderColor):
        """
        'borderW' can be an int for equal borders,
        or a 4-tuple defining widths for (top, right, bottom, left).
        """
        super(BorderedBox, self).__init__(size)
        
        self._size = size
        self.fillColor = fillColor
        self.borderColor = borderColor
        self.borderWidths = borderW
        self.rect = self.get_rect()

        self.redraw()

    def copy(self):
        b = BorderedBox(self.size, self.fillColor,
                        self.borderWidths, self.borderColor)
        b.rect = self.rect.copy()
        
        return b

    def redraw(self):
        """
        Redraw box. Must be called after altering any attributes
        for changes to be reflected on surface.
        If there was any text on the box, it will be erased;
        call draw_centered_text again to redraw it.
        """
        tb, rb, bb, lb = self.borderWidths
        w, h = self.size
        
        self.fill(self.borderColor)
        inner = pygame.Surface((w - rb - lb,
                                h - tb - bb))
        inner.fill(self.fillColor)
        self.blit(inner, (lb, tb))

    @property
    def borderWidths(self):
        return self._borderWs

    @borderWidths.setter
    def borderWidths(self, val):
        ws = []
        
        if not hasattr(val, '__iter__'):
            val = 4*[val]

        try:
            for i in range(4):
                ws.append(to_numeric(val[i]))
        except IndexError:
            raise BorderError("'borderW' contains ")
        except (TypeError, ValueError):
            raise BorderError()

        self._borderWs = tuple(ws)

    @property
    def size(self):
        return self._size
    
###############################################################################
class BorderError(Exception):
    pass
