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
pygame.display.set_icon(pygame.image.load(os.path.join('images', 'player1_idle1.png')))
clock = pygame.time.Clock()
fps = 60
#--colors--#
black = (0, 0, 0)
white = (255, 255, 255)
red = (240, 15, 15)
green = (15, 240, 15)
blue = (15, 15, 240)
yellow = (240, 240, 15)
purple = (157, 0, 222)
#--fonts--#
font16 = pygame.font.Font("Mangaka.otf", 32)
font32 = pygame.font.Font("Mangaka.otf", 32)
font64 = pygame.font.Font("Mangaka.otf", 64)
font128 = pygame.font.Font("Mangaka.otf", 128)
#--text--#
titleText = font128.render("Pancka", 1, white)
loseText = font128.render("YOU LOSE", 1, white)
winText = font128.render("YOU WON", 1, white)
resetText = font32.render("press 'R' to reset", 1, white)
escapeText = font32.render("press 'Esc' to return to home page", 1, white)
dashText = font16.render("dash available", 1, purple)
#--characters--#


class Player():
    def __init__(self, x, y, type):
        self.images_right = []
        self.images_left = []
        self.images_idle_right = []
        self.images_idle_left = []
        self.images_jump_right = []
        self.images_jump_left = []
        self.images_dash_right = []
        self.images_dash_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 7):
            img_right = pygame.image.load(
                os.path.join('images', f'player{type}_run{num}.png'))
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        for num in range(1, 4):
            img_idle_right = pygame.image.load(
                os.path.join('images', f'player{type}_idle{num}.png'))
            img_idle_right = pygame.transform.scale(img_idle_right, (40, 80))
            img_idle_left = pygame.transform.flip(img_idle_right, True, False)
            self.images_idle_right.append(img_idle_right)
            self.images_idle_left.append(img_idle_left)
        for num in range(1, 5):
            img_jump_right = pygame.image.load(
                os.path.join('images', f'player{type}_jump{num}.png'))
            img_jump_right = pygame.transform.scale(img_jump_right, (50, 80))
            img_jump_left = pygame.transform.flip(img_jump_right, True, False)
            self.images_jump_right.append(img_jump_right)
            self.images_jump_left.append(img_jump_left)
        for num in range(1, 5):
            img_dash_right = pygame.image.load(
                os.path.join('images', f'dash{num}.png'))
            img_dash_right = pygame.transform.scale(img_dash_right, (50, 80))
            img_dash_left = pygame.transform.flip(img_dash_right, True, False)
            self.images_dash_right.append(img_dash_right)
            self.images_dash_left.append(img_dash_left)
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
        self.super = False
        self.super_cooldown = 0
        self.super_counter = 0

    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 5
        dash_cooldown = 60
        dash_speed = 15
        jump_strength = 18
        gravity_strength = 10

        # get keypresses if game is not over
        if loseCondition == False and winCondition == False:
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
            if key[pygame.K_s] and self.super == False and self.super_cooldown >= dash_cooldown:
                self.super = True
                self.super_cooldown = 0
                self.super_counter = 0
                self.vel_y = 0
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_idle_right[self.index]
                if self.direction == -1:
                    self.image = self.images_idle_left[self.index]

        # add gravity only if player not in dash
        if self.super == False:
            self.vel_y += 1
            if self.vel_y > gravity_strength:
                self.vel_y = gravity_strength
            dy += self.vel_y
        # handle animation if game is not over
        if loseCondition == False and winCondition == False:
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
            # if player in dash change pic
            if self.super == True:
                if self.direction == 1:
                    self.image = self.images_dash_right[0]
                if self.direction == -1:
                    self.image = self.images_dash_left[0]
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
        # handle the movement if super
        if self.super:
            # ignore any previous movement if player is in super
            dx = 0
            if self.super_counter < 10:
                dx += dash_speed*self.direction
                self.super_counter += 1
            else:
                self.super = False
        else:
            if self.super_cooldown < dash_cooldown:
                self.super_cooldown += 1
        # check for collision in screen edge
        if self.rect.x+dx < 0 or self.rect.x+self.rect.width+dx > screen_width:
            dx = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0
        # update player coordinates if game is not over
        if loseCondition == False and winCondition == False:
            self.rect.x += dx
            self.rect.y += dy

        # draw player onto screen
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        screen.blit(self.image, self.rect)
        # draw dash info only if game is not over
        if loseCondition == False and winCondition == False:
            dash_x = 20
            dash_y = 20
            if 0 <= self.super_cooldown <= 0.25*dash_cooldown:
                screen.blit(pygame.transform.scale(
                    player.images_dash_right[3], (40, 40)), (dash_x, dash_y))
            if 0.25*dash_cooldown <= self.super_cooldown <= 0.5*dash_cooldown:
                screen.blit(pygame.transform.scale(
                    player.images_dash_right[2], (40, 40)), (dash_x, dash_y))
            if 0.5*dash_cooldown <= self.super_cooldown <= 0.75*dash_cooldown:
                screen.blit(pygame.transform.scale(
                    player.images_dash_right[1], (40, 40)), (dash_x, dash_y))
            if 0.75*dash_cooldown <= self.super_cooldown <= 1*dash_cooldown:
                screen.blit(pygame.transform.scale(
                    player.images_dash_right[0], (40, 40)), (dash_x, dash_y))
                screen.blit(dashText, (dash_x+40, dash_y+6))


class Enemy():
    def __init__(self, x, y, level):
        self.images_right = []
        self.images_left = []
        self.images_jump_right = []
        self.images_jump_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 13):
            img_right = pygame.image.load(os.path.join(
                'images', f'enemy{level}_run{num}.png'))
            img_right = pygame.transform.scale(img_right, (50, 70))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        for num in range(1, 7):
            img_jump_right = pygame.image.load(
                os.path.join('images', f'enemy{level}_jump{num}.png'))
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
        self.jumped = False

    def update(self):
        global loseCondition
        dx = 0
        dy = 0
        walk_speed = 3
        walk_cooldown = 5
        jump_strength = 18
        gravity_strength = 10
        dx += walk_speed*self.direction
        self.counter += 1
        # add gravity
        self.vel_y += 1
        if self.vel_y > gravity_strength:
            self.vel_y = gravity_strength
        dy += self.vel_y
        # handle animation if game is not over
        if loseCondition == False and winCondition == False:
            if self.in_air == False:
                if self.counter > walk_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images_right):
                        self.index = 0
                    if self.rect.x+20 < screen_width-walk_speed:
                        self.rect.x += 20
                    else:
                        self.rect.x += 20
                        self.direction = -1
                        dx = walk_speed*self.direction-20
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
                    self.jumped = False
        # check if there is platform nearby from both sides
        for platform in platform_group:
            if 55 >= (self.rect.x-platform.rect.x-platform.rect.width) >= 50 and self.rect.y > platform.rect.y and 0 <= self.rect.y-platform.rect.y <= 60 and self.direction == -1 and self.in_air == False and self.jumped == False:
                choice = random.randint(0, 2)
                if choice == 1:  # every time jump is possible the enemy decide randomly if to take the jump or not
                    self.vel_y = -jump_strength
                    self.jumped = True
                    break
            if 55 >= (platform.rect.x-self.rect.x-self.rect.width) >= 50 and self.rect.y > platform.rect.y and 0 <= self.rect.y-platform.rect.y <= 60 and self.direction == 1 and self.in_air == False and self.jumped == False:
                choice = random.randint(0, 2)
                if choice == 1:
                    self.vel_y = -jump_strength
                    self.jumped = True
                    break
        # check for collision the edge of the screen
        if self.rect.x+dx < walk_speed or self.rect.x+self.width+dx > screen_width-walk_speed:
            self.direction = self.direction*-1
        # update enemy coordinates if game is not over
        if loseCondition == False and winCondition == False:
            self.rect.x += dx
            self.rect.y += dy
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        # check for collision with player while not in dash
        if player.rect.colliderect(self.rect) and player.super == False:
            loseCondition = True


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, level):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface([width, 8])
        # self.image.fill(blue)
        self.image = pygame.image.load(
            os.path.join('images', f'platform{level}.png'))
        self.image = pygame.transform.scale(self.image, (width, 8))
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
        # check for collision with player
        if player.rect.colliderect(self.rect):
            self.points += 1
            self.index = 0
            self.counter = 0
            random_choice = random.choice(coin_placement)
            while random_choice[0] == self.rect.x and self.rect.y-5 <= random_choice[1] <= self.rect.y + 5:
                random_choice = random.choice(coin_placement)
            self.rect.x, self.rect.y = random_choice[0], random_choice[1]
        # handle animation if game is not over
        if loseCondition == False and winCondition == False:
            if self.counter > animation_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                if self.index < 5 and self.index % 2 == 0:
                    self.rect.y -= 1
                elif self.index >= 5 and self.index % 2 == 0:
                    self.rect.y += 1
                elif self.index == 9:
                    self.rect.y += 1
                self.image = self.images[self.index]
            self.counter += 1
        # draw coin onto screen
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

    def check(self):
        if self.points >= level1_score and game_mode == "1":
            return True
        elif self.points >= level2_score and game_mode == "2":
            return True
        else:
            return False


class Button():
    def __init__(self, x, y, text):
        self.image = pygame.image.load(os.path.join('images', 'button.png'))
        self.image = pygame.transform.scale(self.image, (150, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text
        self.clicked = False

    def draw(self, unlock):
        action = False
        image = self.image.copy()
        newColor = (20, 20, 20, 50)
        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == True and self.clicked == False:
                action = True
                self.clicked = True
            else:  # make image lighter when hover the button
                # add in new RGB values
                image.fill(newColor[0:3], None, pygame.BLEND_RGBA_ADD)
        else:  # return the image to normal if not
            image = self.image
        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False
        # draw button
        screen.blit(image, self.rect)
        screen.blit(font32.render(self.text, 1, white),
                    (self.rect.x + 35, self.rect.y + 15))
        # if level is locked make button darker
        if unlock == False:
            darker_image = image.copy()
            darker_image.fill((0, 0, 0, 150))
            screen.blit(darker_image, (self.rect.x, self.rect.y))
        return action


class Button2():
    def __init__(self, x, y, type):
        self.type = type
        self.images_idle = []
        for num in range(1, 4):
            img_idle_right = pygame.image.load(
                os.path.join('images', f'player{type}_idle{num}.png'))
            img_idle_right = pygame.transform.scale(img_idle_right, (30, 60))
            self.images_idle.append(img_idle_right)
        self.images_run = []
        for num in range(1, 7):
            img_run_right = pygame.image.load(
                os.path.join('images', f'player{type}_run{num}.png'))
            img_run_right = pygame.transform.scale(img_run_right, (30, 60))
            self.images_run.append(img_run_right)
        self.image = self.images_idle[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.index = 0
        self.counter = 0

    def draw(self, unlock, choice):
        action = False
        animation_cooldown = 5
        border = 2
        # handle animation if chosen
        if unlock == True and choice == self.type:
            self.counter += 1
            if self.counter > animation_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_run):
                    self.index = 0
                self.image = self.images_run[self.index]
        elif unlock == True and choice != self.type:
            self.image = self.images_idle[0]
        image = self.image.copy()
        newColor = (20, 20, 20, 50)
        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == True and self.clicked == False:
                action = True
                self.clicked = True
            else: 
                # make border larger
                border = 4
        else:  # return the border to normal if not
            border = 2
        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False
        # if character is locked make character darker
        if unlock == False:
            darker_image = self.images_idle[0].copy()
            darker_image.fill((0, 0, 0, 150))
            darker_image = pygame.transform.scale(
                darker_image, (self.rect.width+20, self.rect.height+20))
            screen.blit(darker_image, (self.rect.x-10, self.rect.y-10))
            pygame.draw.rect(screen, black, (self.rect.x-10,
                             self.rect.y-10, self.rect.width+20, self.rect.height+20), 2)
        else:
            pygame.draw.rect(screen, white, (self.rect.x-10, self.rect.y -
                             10, self.rect.width+20, self.rect.height+20), border)
            if choice == self.type:
                lighter_image = self.images_idle[0].copy()
                lighter_image.fill((255, 255, 255, 150))
                lighter_image = pygame.transform.scale(lighter_image, (self.rect.width+20, self.rect.height+20))
                screen.blit(lighter_image, (self.rect.x-10, self.rect.y-10))
            screen.blit(image, (self.rect.x, self.rect.y))
        return action
#--function--#

def reset():
    global player, enemies, coin, platform_group, background, coin_placement, loseCondition, winCondition
    if game_mode == "home":
        background = pygame.image.load(
            os.path.join('images', 'background0.jpg'))
        background = pygame.transform.scale(
            background, (screen_width, screen_height))
    if game_mode == "1":
        level1_platform_placement = [[250, 250, 200], [
            0, 130, 150], [screen_width-150, 130, 150]]
        coin_placement = [(100, screen_height-30-50),
                          (screen_width-100, screen_height-30-50),
                          (screen_width/2-20, screen_height-30-50),
                          (screen_width/2-20, 200), (100, 80), (screen_width-100, 80)]
        player = Player(100, screen_height-30-110, player_type)
        enemies = []
        enemy = Enemy(600, screen_height-30-80, 1)
        enemies.append(enemy)
        random_choice = random.choice(coin_placement)
        while random_choice[0] == 100 and random_choice[1] == screen_height-30-50:
            random_choice = random.choice(coin_placement)
        coin = Coin(random_choice[0], random_choice[1])
        platform_group = pygame.sprite.Group()
        for tile in level1_platform_placement:
            platform = Platform(tile[0], tile[1], tile[2], 1)
            platform_group.add(platform)
        ground = Platform(0, screen_height-30, screen_width, 1)
        platform_group.add(ground)
        background = pygame.image.load(
            os.path.join('images', 'background1.jpg'))
        background = pygame.transform.scale(
            background, (screen_width, screen_height))
    if game_mode == "2":
        level2_platform_placement = [[270, 80, 160], [0, 190, 170],
                                     [screen_width-170, 190, 170], [270, 270, 160]]
        coin_placement = [(100, screen_height-30-50),
                          (screen_width-100, screen_height-30-50),
                          (screen_width/2-20, screen_height-30-50),
                          (screen_width/2-20, 220), (100, 140), (screen_width-100, 140), (screen_width/2-20, 30)]
        player = Player(100, screen_height-30-110, player_type)
        enemies = []
        enemy = Enemy(600, 110, 2)
        enemy2 = Enemy(100, 110, 2)
        enemy2.direction = 1
        enemies.append(enemy)
        enemies.append(enemy2)
        random_choice = random.choice(coin_placement)
        while random_choice[0] == 100 and random_choice[1] == screen_height-30-50:
            random_choice = random.choice(coin_placement)
        coin = Coin(random_choice[0], random_choice[1])
        platform_group = pygame.sprite.Group()
        for tile in level2_platform_placement:
            platform = Platform(tile[0], tile[1], tile[2], 2)
            platform_group.add(platform)
        ground = Platform(0, screen_height-30, screen_width, 2)
        platform_group.add(ground)
        background = pygame.image.load(
            os.path.join('images', 'background2.jpg'))
        background = pygame.transform.scale(
            background, (screen_width, screen_height))
    loseCondition = False
    winCondition = False

#--other game variables--#
loseCondition = False
winCondition = False
game_mode = "home"
level1_score = 5
level2_score = 10
player_type = 1
levels_completed = set()
button1 = Button(screen_width/2 - 75, screen_height/2-30, "LEVEL 1")
button2 = Button(screen_width/2 - 75, screen_height/2+40, "LEVEL 2")
player1_button = Button2(screen_width/2 + 45, screen_height-80, 1)
player2_button = Button2(screen_width/2 - 15, screen_height-80, 2)
player3_button = Button2(screen_width/2 - 75, screen_height-80, 3)
reset()
run = True
#--main loop--#
while run:
    if game_mode == "home":
        clock.tick(fps)
        screen.blit(background, (0, 0))
        screen.blit(titleText, (screen_width/2-160, 50))
        if button1.draw(True):
            game_mode = "1"
            reset()
        if button2.draw(1 in levels_completed) and (1 in levels_completed) == True:
            game_mode = "2"
            reset()
        if player1_button.draw(True, player_type):
            player_type = 1
        if player2_button.draw(1 in levels_completed, player_type) and (1 in levels_completed) == True:
            player_type = 2
        if player3_button.draw(2 in levels_completed, player_type) and (2 in levels_completed) == True:
            player_type = 3
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    else:
        clock.tick(fps)
        screen.fill(black)
        screen.blit(background, (0, 0))
        platform_group.draw(screen)
        coin.update()
        for enemy in enemies:
            enemy.update()
        player.update()
        pointsText = font64.render(str(coin.points), 1, white)
        screen.blit(pointsText, (screen_width/2-17, 20))
        if loseCondition == True:
            screen.blit(loseText, (screen_width/2-200, screen_height/2-50))
            screen.blit(resetText, (screen_width/2-80, screen_height/2+60))
            screen.blit(escapeText, (screen_width/2-170, screen_height/2+120))
        if coin.check() == True:
            winCondition = True
            levels_completed.add(int(game_mode))
            screen.blit(winText, (screen_width/2-200, screen_height/2-50))
            screen.blit(resetText, (screen_width/2-80, screen_height/2+60))
            screen.blit(escapeText, (screen_width/2-180, screen_height/2+120))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (loseCondition == True or winCondition == True):
                    reset()
                if event.key == pygame.K_ESCAPE and (loseCondition == True or winCondition == True):
                    game_mode = "home"
                    reset()

    pygame.display.update()

pygame.quit()