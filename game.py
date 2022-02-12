#--modules--#
import pygame
import random
#--setting up display--#
pygame.init()
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Pancka")
#--colors--#
black = (0, 0, 0)
white = (255, 255, 255)
red = (240, 15, 15)
green = (15, 240, 15)
blue = (15, 15, 240)
yellow = (240, 240, 15)
#--characters--#


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([32, 32])
        self.image.fill(yellow)
        self.rect = self.image.get_rect()


#--game variables--#
all_sprites_list = pygame.sprite.Group()
player = Player()
player.rect.x = 300
player.rect.y = 340
all_sprites_list.add(player)
clock = pygame.time.Clock()
running = True
#--main loop--#
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    key = pygame.key.get_pressed()
    if key[pygame.K_a] or key[pygame.K_LEFT]:
        if player.rect.x < -60:
            player.rect.x = 700
        player.rect.x -= 5
    elif key[pygame.K_d] or key[pygame.K_RIGHT]:
        if player.rect.x > 700:
            player.rect.x = - 60
        player.rect.x += 5
    screen.fill(black)
    all_sprites_list.draw(screen)
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
