import pygame
from pygame.locals import *
from time import sleep
from random import randint
from os import listdir

class MilhouseGame:
    GAME_WIDTH = 500
    GAME_HEIGHT = 500

    WHITE = (255, 255, 255, 0)
    bg_color = WHITE

    INIT_SPEED_X = 20
    INIT_SPEED_Y = 10
    
    GAME_TITLE = "Milhouse Rage"

    def __init__(self):
        # Initialize pygame
        pygame.init()

        self.window = pygame.display.set_mode((self.GAME_WIDTH, self.GAME_HEIGHT))
        pygame.display.set_caption(self.GAME_TITLE)

        self.surface = pygame.display.get_surface()

        self.sprites = []

        # Add every png in current directory
        for f in listdir('./'):
            if f.endswith('.png'): # Could also use glob.glob('*.png')
                sprite = pygame.image.load("{0}".format(f))
                self.sprites.append({
                    'sprite': sprite,
                    'pos': (randint(0,self.GAME_WIDTH - sprite.get_width()),
                            randint(0,self.GAME_HEIGHT - sprite.get_height())),
                    'speed': (self.INIT_SPEED_X, self.INIT_SPEED_Y)
                })

    def run(self):
        self.game_loop()

    def draw(self):
        """Takes sprites, a dictionary of images to positions"""

        self.surface.fill(self.bg_color)

        for sprite in self.sprites:
            self.surface.blit(sprite['sprite'], sprite['pos'])

        pygame.display.flip()

    def game_loop(self):
        # Game loop
        for i in range(1, 200):
            # Randomize background
            if(randint(1,15) == 3):
                self.bg_color = (randint(0,255), randint(0,255), randint(0,255), 0)

            for sprite in self.sprites:
                # Bounce (reverse velocity) if on edge
                (x, y) = sprite['pos']
                (x_speed, y_speed) = sprite['speed']
                (width, height) = sprite['sprite'].get_size()

                if x <= 0 or x >= self.GAME_WIDTH - width:
                    x_speed = -1 * x_speed
                if y <= 0 or y >= self.GAME_HEIGHT - height:
                    y_speed = -1 * y_speed


                x = x + x_speed
                y = y + y_speed

                print("f{0}:\tx{1}\ty{2}\tspeed({3},{4})\tbg{4}").format(i, x, y, x_speed,
                                                                      y_speed, self.bg_color)

                sprite['speed'] = (x_speed, y_speed)
                sprite['pos'] = (x, y)

            self.draw()

if __name__ == "__main__":
    game = MilhouseGame()
    game.run()