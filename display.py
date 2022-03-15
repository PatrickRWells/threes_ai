import py
import pygame
from logic import Grid 

class ThreesMainWindow:
    
    def __init__(self, game, *args, **kwrags):
        pygame.init()
        self.screen = pygame.display.set_mode([1000+200, 1000])
        self.running = True
        self._game = game
        self.setup_ui()

    def setup_ui(self, *args, **kwargs):
        self.MAIN_WIDTH = 600
        self.MAIN_HEIGHT = 800
        self.RIGHT_OFFSET = 200
        self.x1 = 200
        self.y1 = 100
        
        self._vertical_starts = [self.x1 + i*self.MAIN_WIDTH/4 for i in range(5)]
        self._horizontal_starts = [self.y1 + i*self.MAIN_HEIGHT/4 for i in range(5)]


        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (128, 128, 128), (self.x1,self.y1, self.MAIN_WIDTH,self.MAIN_HEIGHT))
        for v in self._vertical_starts:
            pygame.draw.line(self.screen, (0, 0,0), (v, self.y1), (v, self.y1+self.MAIN_HEIGHT))
        for h in self._horizontal_starts:
            pygame.draw.line(self.screen, (0, 0,0), (self.x1, h), (self.x1+self.MAIN_WIDTH, h))
    
    def cell_center(self, x,y):
        x_ = (self._vertical_starts[x] + self._vertical_starts[x+1])/2
        y_ = (self._horizontal_starts[y] + self._horizontal_starts[y+1])/2
        return x_, y_

    
    def paint_numbers(self):
        for index, val in enumerate(self._game._grid.grid):
            if val == 0:
                continue
            else:
                x,y = Grid.get_xy(index)
                xpix = self.x1 + (x+0.025)*self.MAIN_WIDTH/4
                ypix = self.y1 + (y+0.025)*self.MAIN_HEIGHT/4 
                s = NumberTile(self.MAIN_WIDTH/4, self.MAIN_HEIGHT/4, val)
                self.screen.blit(s, (xpix, ypix))
        
        
        
            

    def add_next(self):
        s = NumberTile(self.MAIN_WIDTH/8, self.MAIN_HEIGHT/8, self._game.next)
        x = self._vertical_starts[-1] + self.RIGHT_OFFSET
        y = self.MAIN_HEIGHT / 2
        self.screen.blit(s, (x,y))


    
    def run(self):
        self.paint_numbers()
        pygame.display.flip()
        self.add_next()

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running=False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self._game.swipeLeft()
                    if event.key == pygame.K_RIGHT:
                        self._game.swipeRight()
                    if event.key == pygame.K_UP:
                        self._game.swipeUp()
                    if event.key == pygame.K_DOWN:
                        self._game.swipeDown()
                    self.setup_ui()
                    self.paint_numbers()
                    self.add_next()
                    pygame.display.flip()


        pygame.quit()


def NumberTile(width, height, number):
    if number == 2:
        c = (255, 0, 0)
    elif number == 1:
        c = (0, 255, 255)
    else:
        c = (255, 255, 255)
    font = pygame.font.SysFont("Times", 30)

    main_surface = pygame.Surface((width*.95, height*.95))
    main_surface.fill(c)
    f = font.render(str(number), False, (0, 0, 0))
    main_surface.blit(f, (width/2, height/2))
    return main_surface



if __name__ == "__main__":

    from logic import Game
    g = Game(4)
    w = ThreesMainWindow(g)
    w.run()



