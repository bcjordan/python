import pygame
from pygame.locals import *
from time import sleep
from random import randint
from os import listdir

class MilhouseGame:
    DEBUG = False

    GAME_WIDTH = 500
    GAME_HEIGHT = 500

    WHITE = (255, 255, 255, 0)
    BLACK = (0, 0, 0, 0)

#    bg_color = lambda self: self.bg_color()
    bg_color = lambda self: (randint(0, 255), randint(0, 255), randint(0, 255), 0)

    INIT_SPEED_X = 5
    INIT_SPEED_Y = 5

    X_ACCEL = 1.5
    Y_ACCEL = 1.5

    QUIT_KEYS = {K_ESCAPE, K_q}
    PAUSE_KEYS = {K_SPACE}

    IMAGES_LOCATION = './'

    GAME_TITLE = "Milhouse Rage"

    def __init__(self):
        # Initialize pygame
        pygame.init()

        self.window = pygame.display.set_mode((self.GAME_WIDTH, self.GAME_HEIGHT))
        pygame.display.set_caption(self.GAME_TITLE)

        self.surface = pygame.display.get_surface()

        self.paused = False
        
        self.sprites = []
        self.mouse = (self.GAME_WIDTH / 2, self.GAME_HEIGHT / 2)
        self.mouse_down = False

        self.direction = {}
        for d in ["up", "down", "left", "right"]: self.direction[d] = False

        # Add every png in current directory
        for f in listdir(self.IMAGES_LOCATION):
            if f.endswith('.png') or f.endswith('.jpeg') or f.endswith('.jpg'): # Could also use glob.glob('*.png')
                try:
                    sprite = pygame.image.load("{0}{1}".format(self.IMAGES_LOCATION, f))
                    self.sprites.append({
                        'sprite': sprite,
                        'pos': (randint(0,self.GAME_WIDTH - sprite.get_width()),
                                randint(0,self.GAME_HEIGHT - sprite.get_height())),
                        'speed': (self.INIT_SPEED_X, self.INIT_SPEED_Y)
                    })
                    print("File {0} loaded").format(f)
                except: print("File load for {0} failed.").format(f)
                finally: False

    def pause(self):
        self.paused = not self.paused

    def quit(self):
        sys.exit(0)
        pygame.quit()

    def run(self):
        self.game_loop()

    def draw(self):
        """Takes sprites, a dictionary of images to positions"""

        self.surface.fill(self.bg_color())

        for sprite in self.sprites:
            self.surface.blit(sprite['sprite'], sprite['pos'])

        pygame.draw.circle(self.surface, self.WHITE, self.mouse, 10)

        pygame.display.flip()

    def update(self):
        for sprite in self.sprites:
            # Bounce (reverse velocity) if on edge
            (x, y) = sprite['pos']
            (x_speed, y_speed) = sprite['speed']
            (width, height) = sprite['sprite'].get_size()

            if x <= 0 or x >= self.GAME_WIDTH - width:
                x_speed = -1 * x_speed
            if y <= 0 or y >= self.GAME_HEIGHT - height:
                y_speed = -1 * y_speed

            # Update speed of first sprite based on keydowns
            for (direction, on) in self.direction.iteritems():
                if direction == "up":    y_speed = y_speed + self.Y_ACCEL
                if direction == "down":  y_speed = y_speed - self.Y_ACCEL
                if direction == "right": x_speed = x_speed + self.X_ACCEL
                if direction == "left":  x_speed = x_speed - self.X_ACCEL

            x = x + x_speed
            y = y + y_speed

            if self.DEBUG: print("\tx{1}\ty{2}\tspeed({3},{4})\tbg{4}")\
                                  .format(x, y, x_speed, y_speed, self.bg_color())
            sprite['speed'] = (x_speed, y_speed)
            sprite['pos'] = (x, y)

    def keyboard_input(self, events):
        """Function to handle key events and quit"""
        for event in events:
            print(event)

            self.mouse = pygame.mouse.get_pos()
            self.mouse_down = pygame.mouse.get_pressed()
            
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN:
                if self.DEBUG: print("KEYDOWN {0}").format(event.key)
                if event.key in self.QUIT_KEYS:
                    quit()
                if event.key in self.PAUSE_KEYS:
                    self.pause()
                if event.key == K_UP:    self.direction = {'up': True}
                if event.key == K_DOWN:  self.direction = {'down': True}
                if event.key == K_LEFT:  self.direction = {'left': True}
                if event.key == K_RIGHT: self.direction = {'right': True}
            elif event.type == KEYUP:
                if self.DEBUG: print("KEYUP {0}").format(event.key)
                if event.key == K_UP:    self.direction = {'up': False}
                if event.key == K_DOWN:  self.direction = {'down': False}
                if event.key == K_LEFT:  self.direction = {'left': False}
                if event.key == K_RIGHT: self.direction = {'right': False}

    def game_loop(self):
        """Game loop"""
        while(True):
            self.keyboard_input(pygame.event.get())
            if(not self.paused):
                self.update()
                self.draw()

if __name__ == "__main__":
    game = MilhouseGame()
    game.run()