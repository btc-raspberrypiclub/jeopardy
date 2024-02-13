"""
congrats.py

DESCRIPTION:
  Contains the functions that implement the congratulatory
  message part of the JeoparPy outro sequence.

USAGE:
  Main should call only do_congrats.
  

Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file..
"""
import pygame

from .constants import JEOP_BLUE
from .resmaps import FONTS
from .util import scale

def do_congrats(screen, clock, winners, audioPlayer):
    """
    Fade out the last image on the screen, draw a congratulatory message,
    then draw the names of the winning players.
    """
    lastScreen = screen.copy()
    w, h = size = lastScreen.get_size()
    sfc = pygame.Surface(size)

    _fade_in_sfc(screen, sfc, clock, 2.0)
    audioPlayer.play('applause')
    congratsBottom = _animate_congrats(screen, sfc)
    winnersRect = _draw_winners(sfc, congratsBottom + 20, winners)

    screen.blit(sfc, (0, 0))
    pygame.display.update(winnersRect)
    audioPlayer.wait_until_sound_end(1000)
    
def _animate_congrats(screen, sfc):
    """
    Animate a congratulations message, drawing one character at a time
    and waiting a short time.

    Return y-value, the bottom of the drawn text string.
    """
    word = 'CONGRATULATIONS!'
    sfcRect = sfc.get_rect()
    font = pygame.font.Font(FONTS['congrats'], scale(150, sfcRect.h, 768))
    rect = pygame.Rect((0, 0), font.size(word))
    rect.centerx = sfcRect.centerx
    rect.y = sfcRect.y + int(.20*sfcRect.h)
    x, y = rect.topleft

    for c in word:
        char = font.render(c, 1, (255, 255, 255), JEOP_BLUE)
        sfc.blit(char, (x, y))

        screen.blit(sfc, (0, 0))
        pygame.display.update(rect)
        pygame.time.delay(100)
        x += char.get_size()[0]

    return rect.bottom

def _draw_winners(sfc, startY, winners):
    """
    Blit the names of the winners, in their respective fonts, onto sfc.
    'startY' is the y-value of the position at which the first name
    will be drawn.
    If there are multiple winners, draw them in order.

    Return pygame.Rect representing area in which names were drawn.
    """
    sfcRect = sfc.get_rect()
    rect = pygame.Rect(0, startY, sfcRect.w, sfcRect.h - startY)
    y = startY 

    for i, name in winners:
        fName = 'team' + str(i + 1)
        font = pygame.font.Font(FONTS[fName], scale(120, sfcRect.h, 768))
        text = font.render(name, 1, (255, 255, 255), JEOP_BLUE)
        tRect = text.get_rect()
        tRect.centerx = rect.centerx
        tRect.y = y

        sfc.blit(text, tRect)
        y += tRect.h + 5

    return rect

# TODO Abstract into generic function
def _fade_in_sfc(screen, sfc, clock, time):
    """
    Fade in 'sfc' over 'time' (in seconds), essentially fading out
    the last image on 'screen.'
    """
    lastScreen = screen.copy()
    fpsGoal = int(255.0 / time) # frames to draw / time to spend in secs
    sfc.fill(JEOP_BLUE)
    
    for alpha in xrange(256):
        sfc.set_alpha(alpha)
        screen.blit(lastScreen, (0, 0))
        screen.blit(sfc, (0, 0))
        
        pygame.display.update()
        clock.tick_busy_loop(fpsGoal)
