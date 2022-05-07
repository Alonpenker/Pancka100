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
            img_jump_right = pygame.image.load(
                os.path.join('images', f'player_jump{num}.png'))
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
            # check for collision in x direction
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check for collision in y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                # check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = platform.rect.bottom - self.rect.top
                    self.vel_y = 0
                # check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = platform.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False
        # check for collision in screen edge
        if self.rect.x+dx < 0 or self.rect.x+self.rect.width+dx > screen_width:
            dx = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0
        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        # draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


class Enemy():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.images_jump_right = []
        self.images_jump_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 13):
            img_right = pygame.image.load(
                os.path.join('images', f'enemy1_run{num}.png'))
            if num > 2:
                img_right = pygame.transform.scale(img_right, (70, 70))
            else:
                img_right = pygame.transform.scale(img_right, (50, 70))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        for num in range(1, 7):
            img_jump_right = pygame.image.load(
                os.path.join('images', f'enemy1_jump{num}.png'))
            img_jump_right = pygame.transform.scale(img_jump_right, (50, 70))
            img_jump_left = pygame.transform.flip(img_jump_right, True, False)
            self.images_jump_right.append(img_jump_right)
            self.images_jump_left.append(img_jump_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.direction = -1
        self.in_air = True

    def update(self):
        dx = 0
        dy = 0
        walk_speed = 3
        walk_cooldown = 5
        jump_strength = 18
        gravity_strength = 10
        dx += walk_speed*self.direction
        self.counter += 1
        # check if there is platform nearby from both sides
        for platform in platform_group:
            if 55 >= (self.rect.x-platform.rect.x-platform.rect.width) >= 50 and self.rect.y > platform.rect.y and 0 <= self.rect.y-platform.rect.y <= 60 and self.direction == -1 and self.in_air == False:
                choice = random.randint(0, 2)
                if choice == 1:  # every time jump is possible the enemy decide randomly if to take the jump or not
                    self.vel_y = -jump_strength
                    self.jumped = True
            if 55 >= (platform.rect.x-self.rect.x-self.rect.width) >= 50 and self.rect.y > platform.rect.y and 0 <= self.rect.y-platform.rect.y <= 60 and self.direction == 1 and self.in_air == False:
                choice = random.randint(0, 2)
                if choice == 1:
                    self.vel_y = -jump_strength
                    self.jumped = True
        # add gravity
        self.vel_y += 1
        if self.vel_y > gravity_strength:
            self.vel_y = gravity_strength
        dy += self.vel_y
        # handle animation
        if self.in_air == False:
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.index == 0:
                    self.rect.width = 50
                    if self.rect.x+20 < screen_width-walk_speed:
                        self.rect.x += 20
                    else:
                        self.rect.x += 20
                        self.direction = -1
                        dx = walk_speed*self.direction-20
                elif self.index == 2:
                    self.rect.width = 70
                    if self.rect.x-20 > walk_speed:
                        self.rect.x -= 20
                    else:
                        self.rect.x -= 20
                        self.direction = 1
                        dx = walk_speed*self.direction+20
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
            if -int(0.7*jump_strength) > self.vel_y >= -int(0.8*jump_strength):
                if self.direction == 1:
                    self.image = self.images_jump_right[2]
                if self.direction == -1:
                    self.image = self.images_jump_left[2]
            if -int(0.6*jump_strength) > self.vel_y >= -int(0.7*jump_strength):
                if self.direction == 1:
                    self.image = self.images_jump_right[3]
                if self.direction == -1:
                    self.image = self.images_jump_left[3]
            if -int(0.5*jump_strength) > self.vel_y >= -int(0.6*jump_strength):
                if self.direction == 1:
                    self.image = self.images_jump_right[4]
                if self.direction == -1:
                    self.image = self.images_jump_left[4]
            if gravity_strength >= self.vel_y >= int(0.5*jump_strength):
                if self.direction == 1:
                    self.image = self.images_jump_right[5]
                if self.direction == -1:
                    self.image = self.images_jump_left[5]
        self.in_air = True
        for platform in platform_group:
            # check for collision in x direction
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check for collision in y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = platform.rect.bottom - self.rect.top
                    self.vel_y = 0
                # check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = platform.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False
        # check for collision the edge of the screen
        if self.rect.x+dx < walk_speed or self.rect.x+self.width+dx > screen_width-walk_speed:
            self.direction = self.direction*-1
        # update enemy coordinates
        self.rect.x += dx
        self.rect.y += dy
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


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 11):
            img = pygame.image.load(os.path.join('images', f'coin{num}.png'))
            img = pygame.transform.scale(img, (40, 40))
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.points = 0

    def update(self):
        animation_cooldown = 5
        #check for collision with player
        if player.rect.colliderect(self.rect):
            self.points += 1
            print(self.points)
            self.index = 0
            self.counter = 0
            random_choice = random.choice(level1_coin_placement)
            while random_choice[0] == self.rect.x and random_choice[1] == self.rect.y:
                random_choice = random.choice(level1_coin_placement)
            self.rect.x, self.rect.y = random_choice[0], random_choice[1]
        # handle animation
        if self.counter > animation_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            if self.index<5:
                self.rect.x += 1
            else:
                self.rect.x -= 1
            self.image = self.images[self.index]
        self.counter += 1
        #change width according to index number
        self.rect.width = int(1.12*self.index**2-11.2*self.index+40)
        self.image = pygame.transform.scale(self.image, (self.rect.width, 40))
        # draw coin onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


#--game variables--#
level1_platform_placement = [[250, 250, 200], [0, 130, 150], [screen_width-150, 130, 150]]
level1_coin_placement = [(100, screen_height-30-50),
                         (screen_width-100, screen_height-30-50),
                         (screen_width/2-20, screen_height-30-50),
                         (screen_width/2-20, 200), (100, 80),(screen_width-100,80)]
player = Player(100, screen_height-30-110)
enemy = Enemy(600, screen_height-30-80)
random_choice = random.choice(level1_coin_placement)
while random_choice[0] == 100 and random_choice[1] == screen_height-30-50:
    random_choice = random.choice(level1_coin_placement)
coin = Coin(random_choice[0],random_choice[1])
platform_group = pygame.sprite.Group()
for tile in level1_platform_placement:
    platform = Platform(tile[0], tile[1], tile[2])
    platform_group.add(platform)
ground = Platform(0, screen_height-30, screen_width)
platform_group.add(ground)

run = True
#--main loop--#
while run:
    clock.tick(fps)
    screen.fill(black)
    platform_group.draw(screen)
    coin.update()
    enemy.update()
    player.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()