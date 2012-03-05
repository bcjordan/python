import pygame, os, sys
from pygame.locals import *
import random

class LaserBolt(pygame.sprite.Sprite):
    DEBUG = False
    IMAGE_ASSET = "assets/laser.gif"
    VELOCITY = 2 # Pixels per timestep

    def __init__(self, screen, x, y):
        self.screen = screen
        self.image = self.load_sprite()
        self.image_w, self.image_h = self.image.get_size()

        self.x = x
        self.y = y

        # Set up bounding box for image
        self.rect = self.image.get_rect()
        self.update_rect()

        self.active = True

    def update_rect(self):
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w,
                                 self.y + self.image_h)

    def load_sprite(self):
        '''Build pygame image from file |self.IMAGE_NAME|'''
        try:
            image = pygame.image.load(self.IMAGE_ASSET)
        except pygame.error, message:
            print("Can't load image {0} because {1}").format(self.IMAGE_ASSET, message)
            raise SystemExit, message
        return image.convert_alpha()

    def update(self):
        self.y = self.y - self.VELOCITY

        if(self.y <= 0):
            self.active = False

        self.update_rect()

    def draw(self):
        if(self.DEBUG):
            print("Drawing LaserBolt at {0} {1}").format(self.x, self.y)

        if(self.active):
            self.screen.blit(self.image, (self.x, self.y))

class LaserBoltGame:
    DEBUG = True

    def __init__(self, title, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        # Initialize Pygame
        pygame.init()

        # Set up screen
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height

        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(title) # Set the window bar title
        self.screen = pygame.display.get_surface() # This is where images are displayed

        # Set up font
        self.font = pygame.font.Font(None, 36)

        self.laserbolts = []

        # Set up clock
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.seconds = 0
        pygame.time.set_timer(USEREVENT + 1, 1000) # Used to correctly implement seconds


    def run(self):
        while True: # for each frame
            self.handle_input()

            self.clock.tick(self.FPS)
            self.screen.fill((0, 0, 0))

            for laser in self.laserbolts:
                laser.update()
                laser.draw()

            if (pygame.time.get_ticks() % 10 == 0):
                self.laserbolts.append(LaserBolt(self.screen, random.randint(0, self.SCREEN_WIDTH), self.SCREEN_HEIGHT))

            if(self.DEBUG):
                time_display = self.font.render("Time: " + str(self.clock.get_time()), 1, (0, 0, 0))
                rawtime_display = self.font.render("Raw Time: " + str(self.clock.get_rawtime()), 1, (0, 0, 0))
                fps_display = self.font.render("FPS: " + str(self.clock.get_fps()), 1, (0, 0, 0))
                pygame_total_ticks_display = self.font.render("Pygame Ticks (total): " + str(pygame.time.get_ticks()), 1, (0, 0, 0))
                seconds_display = self.font.render("Seconds: " + str(self.seconds), 1, (0, 0, 0))
                self.screen.blit(time_display, (10, 10))
                self.screen.blit(rawtime_display, (10, 35))
                self.screen.blit(fps_display, (10, 60))
                self.screen.blit(pygame_total_ticks_display, (10, 85))
                self.screen.blit(seconds_display, (10, 110))

            pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
            elif event.type == USEREVENT + 1:
                self.seconds += 1

    def quit(self):
        quit()



if __name__ == "__main__":
    

    LaserBoltGame("LaserBolts", 800, 600).run()

    # Init new game and add a laserbolt