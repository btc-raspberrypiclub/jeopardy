#Select Game Menu
#By Tyler Spadgenske

import pygame, sys, os
from pygame.locals import *
from constants import ROOT_PATH

pygame.init()

WINDOWWIDTH = 600
WINDOWHIEGHT = 500
os.environ ['SDL_VIDEO_WINDOW_POS'] = 'center'
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHIEGHT), 0, 32)
pygame.display.set_caption('Select Game')
mainClock = pygame.time.Clock()

class Select_Game():
    def __init__(self, screen):
        self.BLUE = (18,38,109)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (217, 164, 31)
        self.screen = screen
        self.color = [self.BLUE, self.BLUE, self.BLUE, self.BLUE]
        self.options = []
        self.clicked = None
        #Setup select game text
        pygame.Surface.set_alpha(self.screen)
        self.jeopFont = pygame.font.Font(os.path.join(ROOT_PATH, 'res', 'fonts', 'gyparody.ttf'), 53)
        self.selectText = self.jeopFont.render('Select Game', True, self.WHITE)
        self.selectRect = self.selectText.get_rect()
        self.selectRect.centerx = 300
        self.selectRect[1] = 70
               
        #Setup Background Image
        self.backgroundImage = pygame.image.load(os.path.join(ROOT_PATH,'res', 'images', 'introbg.png'))
        self.backgroundRect = self.backgroundImage.get_rect()
        self.backgroundRect.centerx = 300
        self.backgroundRect.centery = 250

    def main(self, event=None):
        self.screen.blit(self.backgroundImage, self.backgroundRect)

        self.screen.blit(self.selectText, self.selectRect)
        
        #Blit Selection
        self.get_options()
        self.blitBlocks(self.options, event)

        return self.clicked

    def get_options(self):
        self.options = os.listdir(os.path.join(ROOT_PATH, 'games'))
        self.options.remove('README.txt')
        self.games = len(self.options)
        if self.games > 4:
            self.games = 4
        if self.games < 1:
            print 'You must have a game in the /games directory!'
            pygame.quit()
            sys.exit()

    def save(self, clicked):
        file = open(os.path.join(ROOT_PATH, 'jeoparpy', 'dir.txt'), 'w')
        file.write(clicked)
        file.close()
        
    def blitBlocks(self, options, event = None):
        for i in range(0, self.games):          
            self.optionText = self.jeopFont.render(options[i], True, self.WHITE, self.BLUE)
            self.optionRect = self.optionText.get_rect()
            self.optionRect.centerx = 300
            self.optionRect.centery = i * 53 + 200

            if event != None:
                if event.type == MOUSEMOTION:
                    if i == 0:
                        if event.pos[0] > 300 - self.optionRect.width / 2  and event.pos[0] < 300 - self.optionRect.width / 2  + self.optionRect.width and event.pos[1] > 174 and event.pos[1] < 226:
                            self.color[0] = self.YELLOW
                        else:
                            self.color[0] = self.BLUE
                    if i == 1:
                        if event.pos[0] > 300 - self.optionRect.width / 2  and event.pos[0] < 300 - self.optionRect.width / 2  + self.optionRect.width and event.pos[1] > 227 and event.pos[1] < 280:
                            self.color[1] = self.YELLOW
                        else:
                            self.color[1] = self.BLUE
                    if i == 2:
                        if event.pos[0] > 300 - self.optionRect.width / 2  and event.pos[0] < 300 - self.optionRect.width / 2  + self.optionRect.width and event.pos[1] > 280 and event.pos[1] < 333:
                            self.color[2] = self.YELLOW
                        else:
                            self.color[2] = self.BLUE
                    if i == 3:
                        if event.pos[0] > 300 - self.optionRect.width / 2  and event.pos[0] < 300 - self.optionRect.width / 2  + self.optionRect.width and event.pos[1] > 333 and event.pos[1] < 386:
                            self.color[3] = self.YELLOW
                        else:
                            self.color[3] = self.BLUE

                if event.type == MOUSEBUTTONDOWN:
                    if i == 0:
                        if event.pos[0] > 300 - self.optionRect.width / 2  and event.pos[0] < 300 - self.optionRect.width / 2  + self.optionRect.width and event.pos[1] > 174 and event.pos[1] < 226:
                            self.clicked = self.options[i]
                    if i == 1:
                        if event.pos[0] > 300 - self.optionRect.width / 2  and event.pos[0] < 300 - self.optionRect.width / 2  + self.optionRect.width and event.pos[1] > 227 and event.pos[1] < 280:
                            self.clicked = self.options[i]
                    if i == 2:
                        if event.pos[0] > 300 - self.optionRect.width / 2  and event.pos[0] < 300 - self.optionRect.width / 2  + self.optionRect.width and event.pos[1] > 280 and event.pos[1] < 333:
                            self.clicked = self.options[i]
                    if i == 3:
                        if event.pos[0] > 300 - self.optionRect.width / 2  and event.pos[0] < 300 - self.optionRect.width / 2  + self.optionRect.width and event.pos[1] > 333 and event.pos[1] < 386:
                            self.clicked = self.options[i]
                            
            self.optionText = self.jeopFont.render(options[i], True, self.WHITE, self.color[i])
            self.optionRect = self.optionText.get_rect()
            self.optionRect.centerx = 300
            self.optionRect.centery = i * 53 + 200

            self.screen.blit(self.optionText, self.optionRect)

def select_game():
    select = Select_Game(windowSurface)
    select.get_options()
    clicked = None
    while True:
        select.main()
        for event in pygame.event.get():
            clicked = select.main(event)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if clicked != None:
            break
        pygame.display.update()
        mainClock.tick()

    select.save(clicked)
    pygame.quit()

if __name__ == '__main__':
    select_game()
