import pygame
from pygame.locals import *
import random

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 75))
        self.surf.fill((55, 55, 55,))
        self.rect = self.surf.get_rect()
        self.xv = 0
        self.yv = 0
        self.allowJump = False
        self.level = None
        
    def movement(self, pressed_keys):
        if (pressed_keys[K_UP] or pressed_keys[K_w]) and self.allowJump == True:
            self.yv = -20
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.xv -= 3
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.xv += 3

        self.xv = self.xv * 0.9
        self.yv += 1
            
        self.rect.move_ip(self.xv, self.yv)

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            self.rect.x += self.xv * -1
            self.xv = 0

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            self.rect.y += self.yv * -1
            self.yv = 0

            
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen.get_width():
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()

        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        if len(platform_hit_list) > 0 or self.rect.bottom > screen.get_height() - 1:
            self.allowJump = True
        else:
            self.allowJump = False

class Sky(pygame.sprite.Sprite):
    def __init__(self):
        super(Sky, self).__init__()
        self.surf = pygame.Surface(screen.get_size())
        self.surf.fill((100, 100, 255))

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super(Platform, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((150, 150, 150))
        self.rect = self.image.get_rect()

class Level():
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.player = player

    def update(self):
        self.platform_list.update()

    def draw(self, screen):
        self.platform_list.draw(screen)

class Level1(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        level = [ [200, 900, 600, 500],
                  [200, 900, 0, 500],
                  [200, 50, 300, 300],
                  ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

screen = pygame.display.set_mode((800, 600),HWSURFACE|DOUBLEBUF|RESIZABLE)

sky = Sky()
player = Player()

players = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


Clock = pygame.time.Clock()
fps = 60

running = True
while running:

    Clock.tick(fps)

    level_list = []
    level_list.append(Level1(player))

    current_level_no = 0
    current_level = level_list[current_level_no]

    player.level = current_level
    
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        if event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.movement(pressed_keys)

    screen.blit(sky.surf, (0, 0))

    current_level.draw(screen)
    
    for entity in all_sprites:
        screen.blit(entity.surf, (entity.rect))
    
    pygame.display.flip()


pygame.quit()

