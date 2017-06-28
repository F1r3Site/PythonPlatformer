import pygame
from pygame.locals import *
import random

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((55, 55, 55,))
        self.rect = self.surf.get_rect()
        self.xv = 0
        self.yv = 0
        self.allowJump = False
        self.level = None
        
        self.scrollX = 0
        
    def movement(self, pressed_keys):
        if (pressed_keys[K_UP] or pressed_keys[K_w]) and self.allowJump == True:
            self.yv = -20
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.xv -= 1
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.xv += 1

        self.xv = self.xv * 0.92
        self.yv += 1

        self.rect.move_ip(self.xv, self.yv)

        for block in self.level.platform_list:
            if self.rect.bottom-5 <= block.rect.top and self.rect.bottom+5 >= block.rect.top and self.rect.left <= block.rect.right and self.rect.right >= block.rect.left or self.rect.bottom > screen.get_height() - 1:
                self.allowJump = True
            else:
                self.allowJump = False

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            self.rect.y += self.yv * -1.1
            self.yv = 0

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.xv >= 0:
                self.rect.x += self.xv * -1
            else:
                self.rect.x += self.xv * -1.2
            self.xv = 0
            
        if self.rect.left < 200:
            self.rect.left = 200
            self.scrollX += self.xv
        elif self.rect.right > screen.get_width() - 200:
            self.rect.right = screen.get_width() - 200
            self.scrollX += self.xv
        if self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()

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

class ExitLevel(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super(ExitLevel, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 50, 50))
        self.rect = self.image.get_rect()

class Level():
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.exit_list = pygame.sprite.Group()
        self.player = player

    def update(self):
        self.platform_list.update()
        self.exit_list.update()

    def draw(self, screen):
        self.platform_list.draw(screen)
        self.exit_list.draw(screen)
        

class Level1(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        level = [ [200, 50, 600, 500],
                  [200, 50, 900, 400],
                  [200, 50, 1200, 300],
                  [200, 50, 1800, 300],
                  [200, 50, 2100, 200],
                  [200, 50, 2400, 100],
                  [200, 60, 3000, 400],
                  ]

        levelExit = [ [50, 50, 3075, 325],
                      [50, 50, 0, 500],
                      ]

        for lExit in levelExit:
            block = ExitLevel(lExit[0], lExit[1])
            block.rect.x = lExit[2] - player.scrollX
            block.rect.y = lExit[3]
            block.player = self.player
            self.exit_list.add(block)

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2] - player.scrollX
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Level2(Level):
    def __init__(self, player):
        
        Level.__init__(self, player)

        level = [ [25, 100, 300, 450],
                  [25, 100, 500, 400],
                  [400, 50, 800, 300],
                  [25, 25, 1300, 300],
                  [25, 25, 1400, 300],
                  [25, 25, 1500, 300],
                  
                ]

        levelExit = [ [50, 50, 0, 500], ]

        for lExit in levelExit:
            block = ExitLevel(lExit[0], lExit[1])
            block.rect.x = lExit[2] - player.scrollX
            block.rect.y = lExit[3]
            block.player = self.player
            self.exit_list.add(block)

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2] - player.scrollX
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)            

screen = pygame.display.set_mode((800, 600))

sky = Sky()
player = Player()
level = Level

players = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


Clock = pygame.time.Clock()
fps = 60

current_level_no = 0

running = True
while running:

    Clock.tick(fps)

    level_list = []
    level_list.append(Level1(player))
    level_list.append(Level2(player))

    current_level = level_list[current_level_no]

    if pygame.sprite.spritecollideany(player, current_level.exit_list):
        current_level_no += 1
        player.rect.x = 200
        player.rect.y = 0
        player.scrollX = 0
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

