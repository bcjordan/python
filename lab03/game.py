from Enemy import Enemy
from Battlecruiser import Battlecruiser
import pygame, os, sys
from pygame.locals import *
from random import randint

class Game:
    DEBUG = False

    def __init__(self, title, screen_width, screen_height):
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

        # Generate Battlecruiser
        self.battlecruiser = Battlecruiser(self.screen,
                                           self.SCREEN_WIDTH / 2,
                                           self.SCREEN_HEIGHT * 5 / 7)

        # Generate 10 enemies
        self.enemies = []
        for i in range(10):
            self.enemies.append(Enemy(self.screen, randint(0, self.SCREEN_WIDTH), randint(0, self.SCREEN_HEIGHT - 300), self.battlecruiser))

        # Add all sprites to group
        self.sprites = pygame.sprite.Group(self.battlecruiser, self.enemies)

        # Set up clock
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.seconds = 0
        pygame.time.set_timer(USEREVENT + 1, 1000) # Used to correctly implement seconds

    def run(self):
        while True: # for each frame
            self.handle_input()
            for sprite in self.sprites:
                sprite.update()

            self.clock.tick(self.FPS)
            self.screen.fill((255, 255, 255))

            for sprite in self.sprites:
                sprite.draw()

            score = (11 - len(self.sprites)) * 100
            ending_font = self.font.render("Score: {0}".format(score), 1, (0, 0, 255))
            self.screen.blit(ending_font, (10, 10))

            pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
                elif event.key == K_LEFT:
                    self.battlecruiser.update("LEFT")
                elif event.key == K_RIGHT:
                    self.battlecruiser.update("RIGHT")
                elif event.key == K_UP:
                    self.battlecruiser.update("UP")
                elif event.key == K_DOWN:
                    self.battlecruiser.update("DOWN")
                elif event.key == K_SPACE:
                    self.battlecruiser.update("FIRE")
            elif event.type == USEREVENT + 1:
                self.seconds += 1

    def quit(self):
        quit()


if __name__ == "__main__":
    print("Loading game window...")

    Game("The Battle for Ram Aras", 800, 600).run()
