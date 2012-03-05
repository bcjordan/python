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
                                           self.SCREEN_HEIGHT / 2)

        # Generate 10 enemies
        self.enemies = []
        for i in range(10):
            self.enemies.append(Enemy(self.screen, randint(0, self.SCREEN_WIDTH), randint(0, self.SCREEN_HEIGHT), self.battlecruiser))

        # Set up clock
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.seconds = 0
        pygame.time.set_timer(USEREVENT + 1, 1000) # Used to correctly implement seconds

    def run(self):
        while True: # for each frame
            self.handle_input()
            for enemy in self.enemies:
                enemy.update()
            self.battlecruiser.update()

            self.clock.tick(self.FPS)
            self.screen.fill((255, 255, 255))

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

            for enemy in self.enemies:
                enemy.draw()
            self.battlecruiser.draw()

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
    print("Loading main")

    Game("Enemy", 800, 600).run()
