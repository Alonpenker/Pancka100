#--modules--#
import pygame
from pygame.locals import *
import random
import os
#--setting up display--#
pygame.init()
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Pancka")
clock = pygame.time.Clock()
fps = 60
#--colors--#
black = (0, 0, 0)
white = (255, 255, 255)
red = (240, 15, 15)
green = (15, 240, 15)
blue = (15, 15, 240)
yellow = (240, 240, 15)
#--characters--#

class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.images_idle_right = []
        self.images_idle_left = []
        self.images_jump_right = []
        self.images_jump_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 7):
            img_right = pygame.image.load(
                os.path.join('images', f'player_run{num}.png'))
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        for num in range(1, 4):
            img_idle_right = pygame.image.load(
                os.path.join('images', f'player_idle{num}.png'))
            img_idle_right = pygame.transform.scale(img_idle_right, (40, 80))
            img_idle_left = pygame.transform.flip(img_idle_right, True, False)
            self.images_idle_right.append(img_idle_right)
            self.images_idle_left.append(img_idle_left)
        for num in range(1, 5):
            img_jump_right = pygame.image.load(os.path.join('images', f'player_jump{num}.png'))
            img_jump_right = pygame.transform.scale(img_jump_right, (50, 80))
            img_jump_left = pygame.transform.flip(img_jump_right, True, False)
            self.images_jump_right.append(img_jump_right)
            self.images_jump_left.append(img_jump_left)
        self.image = self.images_idle_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 1
        self.in_air = True

    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 5
        jump_strength = 18
        gravity_strength = 10

        # get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
            self.vel_y = -jump_strength
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_idle_right[self.index]
            if self.direction == -1:
                self.image = self.images_idle_left[self.index]

        # add gravity
        self.vel_y += 1
        if self.vel_y > gravity_strength:
            self.vel_y = gravity_strength
        dy += self.vel_y
        # handle animation
        if self.in_air == False:
            self.rect.width = 40
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
        else:
            self.rect.width = 50
            if -int(0.9*jump_strength) > self.vel_y >= -jump_strength:
                if self.direction == 1:
                    self.image = self.images_jump_right[0]
                if self.direction == -1:
                    self.image = self.images_jump_left[0]
            if -int(0.8*jump_strength) > self.vel_y >= -int(0.9*jump_strength):
                if self.direction == 1:
                    self.image = self.images_jump_right[1]
                if self.direction == -1:
                    self.image = self.images_jump_left[1]
            if -int(0.0*jump_strength) > self.vel_y >= -int(0.8*jump_strength):
                if self.direction == 1:
                    self.image = self.images_jump_right[2]
                if self.direction == -1:
                    self.image = self.images_jump_left[2]
            if gravity_strength >= self.vel_y >= int(0.0*jump_strength):
                if self.direction == 1:
                    self.image = self.images_jump_right[3]
                if self.direction == -1:
                    self.image = self.images_jump_left[3]
        self.in_air = True
        for platform in platform_group:
            #check for collision in x direction
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #check for collision in y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                
                #check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = platform.rect.bottom - self.rect.top
                    self.vel_y = 0
                #check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = platform.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False
            
        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        # draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, 8])
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
#--game variables--#
level1 = [[250,250,200],[0,130,150],[screen_width-150,130,150]]
player = Player(100, screen_height-30-110)
platform_group = pygame.sprite.Group()
for tile in level1:
    platform = Platform(tile[0],tile[1],tile[2])
    platform_group.add(platform)
ground = Platform(0,screen_height-30,screen_width)
platform_group.add(ground)

run = True
#--main loop--#
while run:
    clock.tick(fps)
    screen.fill(black)
    platform_group.draw(screen)
    player.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
