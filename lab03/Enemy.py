import pygame, os, sys
from pygame.locals import *
from random import randint

class Enemy(pygame.sprite.Sprite):
    IMAGE_ALIVE = "assets/mutalisk.gif"
    IMAGE_EXPLOSION = "assets/laser_explosion.gif"
    DEBUG = False

    INIT_DX = 1
    INIT_DY = 1

    '''A simple Enemy class'''

    def load_sprite(self, image):
        '''Build pygame image from file |self.IMAGE_NAME|'''
        try:
            image = pygame.image.load(image)
        except pygame.error, message:
            print("Can't load image {0} because {1}").format(image, message)
            raise SystemExit, message
        return image.convert_alpha()

    def update(self, action = "NONE"):
        # Update position
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        # Update rect
        self.update_rect()

        if self.x <= 0 or self.x >= self.screen.get_width() - self.image_w:
            self.dx = -1 * self.dx
        if self.y <= 0 or self.y >= self.screen.get_height() - self.image_h:
            self.dy = -1 * self.dy

        # Update lasers
        if self.thePlayer:
            for laser in self.thePlayer.lasers:
                if self.DEBUG:
                    print("Self: {0}{1}").format(self.rect.topleft, self.rect.bottomright)
                    print("Laser: {0}{1}").format(laser.rect.topleft, laser.rect.bottomright)
                if pygame.sprite.collide_rect(self, laser):
                    self.hit_by_laser()
            if pygame.sprite.collide_rect(self, self.thePlayer):
                self.thePlayer.explode()

    def update_rect(self):
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w,
                                 self.y + self.image_h)

    def draw(self):
        if (self.DEBUG):
            print("Drawing Enemy at {0} {1}").format(self.x, self.y)

        self.screen.blit(self.image_alive if self.alive else self.image_dead,
                        (self.x, self.y))

        if not self.alive:
            self.kill()

    def hit_by_laser(self):
        self.image = self.image_dead
        self.alive = False

    def __init__(self, screen, x, y, player):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image_alive = self.load_sprite(self.IMAGE_ALIVE)
        self.image_dead = self.load_sprite(self.IMAGE_EXPLOSION)

        self.image = self.image_alive
        self.image_w, self.image_h = self.image.get_size()

        self.x = x
        self.y = y
        self.dx = self.INIT_DX
        self.dy = self.INIT_DY
        
        # Set up bounding box for image
        self.rect = self.image.get_rect()
        self.update_rect()

        self.active = True

        self.thePlayer = player # Reference to |Battlecruiser| object (with array of |.lasers|)

class EnemyGame:
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

        # Generate 10 enemies
        self.enemies = []
        for i in range(10):
            self.enemies.append(Enemy(self.screen, randint(0, self.SCREEN_WIDTH - 39), randint(0, self.SCREEN_HEIGHT - 82), None))

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
    print("Loading main")

    EnemyGame("Enemy", 800, 600).run()
    