import pygame
from config import *
import math
import random

class Spritesheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert()
    
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet, (0,0), (x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite    

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_move = 0
        self.y_move = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(3,2,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.tasks = [
            "Catch 5 Pokemons",
            "Win a Battle",
            "Visit the PokeCenter",
        ]
        self.current_task_index = 0
        self.display_task()

    def display_task(self):
        current_task = self.tasks[self.current_task_index]
        font = pygame.font.Font(None, 36)

        text = font.render(current_task, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.y - 20))
        self.game.screen.blit(text, text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: 
            self.current_task_index += 1
        if self.current_task_index == len(self.tasks):
            self.current_task_index = 0

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_move
        self.collide_blocks('x')
        self.rect.y += self.y_move
        self.collide_blocks('y')

        self.x_move = 0
        self.y_move = 0

        
        self.display_task()

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_move -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_move += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_move -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_move += PLAYER_SPEED
            self.facing = 'down'
    
    def collide_enemy(self,direction):
        hits = pygame.sprite.spritecollide(self,self.game.enemy_sprites,False)
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self,self.game.blocks, False)
            if hits:
                if self.x_move > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_move < 0:
                    self.rect.x = hits[0].rect.right
        
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self,self.game.blocks, False)
            if hits:
                if self.y_move > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_move < 0:
                    self.rect.y = hits[0].rect.bottom
        
    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self,self.game.blocks, False)
            if hits:
                if self.x_move > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_move < 0:
                    self.rect.x = hits[0].rect.right
        
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self,self.game.blocks, False)
            if hits:
                if self.y_move > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_move < 0:
                    self.rect.y = hits[0].rect.bottom
        
    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
        if self.facing == "down":
            if self.y_move == 0:
                self.image = self.game.character_spritesheet.get_sprite(3,2,self.width,self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >=3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_move == 0:
                self.image = self.game.character_spritesheet.get_sprite(3,34,self.width,self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >=3:
                    self.animation_loop = 1 

        if self.facing == "left":
            if self.x_move == 0:
                self.image = self.game.character_spritesheet.get_sprite(3,98,self.width,self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >=3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_move == 0:
                self.image = self.game.character_spritesheet.get_sprite(3,66,self.width,self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >=3:
                    self.animation_loop = 1  
        

class Block(pygame.sprite.Sprite):
    def __init__(self, game,x,y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960,448,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self,game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64,352,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y