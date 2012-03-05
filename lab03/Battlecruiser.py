import pygame, os, sys
from pygame.locals import *
from LaserBolt import LaserBolt

class Battlecruiser(pygame.sprite.Sprite):
    IMAGE_ASSET = "assets/battlecruiser.gif"
    DEBUG = False
    LASER_SOUND = "assets/laser.wav"
    EXPLODE_SOUND = "assets/death_explode.wav"

    '''A simple Battlecruiser class'''

    def load_sprite(self):
        '''Build pygame image from file |self.IMAGE_NAME|'''
        try:
            image = pygame.image.load(self.IMAGE_ASSET)
        except pygame.error, message:
            print("Can't load image {0} because {1}").format(self.IMAGE_ASSET, message)
            raise SystemExit, message
        return image.convert_alpha()

    def update(self, action = "NONE"):
        if action == "UP":
            self.y = self.y - 3
        elif action == "DOWN":
            self.y = self.y + 3
        elif action == "LEFT":
            self.x = self.x - 3
        elif action == "RIGHT":
            self.x = self.x + 3
        elif action == "FIRE":
            self.fire()

        # Update lasers
        for laser in self.lasers:
            laser.update()

    def fire(self):
        # Create a new |LaserBolt| at |(self.x, self.y)|
        new_bolt = LaserBolt(self.screen, self.x + self.image_w / 2, self.y  - 15)
        self.lasers.append(new_bolt)

        # Play laser sound
        self.laser_sound.play()

    def draw(self):
        if (self.DEBUG):
            print("Drawing Battlecruiser at {0} {1}").format(self.x, self.y)

        if not self.game_over: self.screen.blit(self.image, (self.x, self.y))
        if self.game_over:
            ending_font = self.font.render("Game over, man!", 1, (255, 0, 0))
            self.screen.blit(ending_font, (10, 50))

        # Draw lasers
        for laser in self.lasers:
            if laser.active:
                laser.draw()
            else:
                self.lasers.remove(laser)

    def explode(self):
        self.explode_sound.play()

        if self.DEBUG: print("Exploding")

        self.game_over = True

    def __init__(self, screen, x, y):
        self.font = pygame.font.Font(None, 36)
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = self.load_sprite()
        self.image_w, self.image_h = self.image.get_size()

        self.x = x
        self.y = y

        # Set up bounding box for image
        self.rect = self.image.get_rect()

        self.update_rect()

        self.active = True

        self.lasers = []

        self.laser_sound = pygame.mixer.Sound(self.LASER_SOUND)
        self.explode_sound = pygame.mixer.Sound(self.EXPLODE_SOUND)

        self.game_over = False
        
    def update_rect(self):
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w,
                                 self.y + self.image_h)


class BattlecruiserGame:
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

        self.battlecruiser = Battlecruiser(self.screen,
                                           self.SCREEN_WIDTH / 2,
                                           self.SCREEN_HEIGHT / 2)
        
        # Set up clock
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.seconds = 0
        pygame.time.set_timer(USEREVENT + 1, 1000) # Used to correctly implement seconds



    def run(self):
        while True: # for each frame
            self.handle_input()
            self.battlecruiser.update()
            
            self.clock.tick(self.FPS)
            self.screen.fill((0, 0, 0))

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

    BattlecruiserGame("Battlecruiser", 800, 600).run()
    