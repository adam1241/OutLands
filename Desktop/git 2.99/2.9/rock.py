import pygame
from entity import Entity
from support import *
from settings import *
class Rock(Entity):
    def __init__(self,pos, groups):
        super().__init__(groups)
        self.sprites = []
        self.animating = False
        self.sprites.append(pygame.image.load('Graphics/rocks/08_0.png'))
        self.sprites.append(pygame.image.load('Graphics/rocks/08_1.png'))
        self.sprites.append(pygame.image.load('Graphics/rocks/08_2.png'))
        self.sprites.append(pygame.image.load('Graphics/rocks/08_3.png'))
        self.sprites.append(pygame.image.load('Graphics/rocks/08.png'))

        self.animations = []
        self.frame_index = 0
        self.animation_speed = 0.05

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.hitbox = self.rect.inflate(0,0.5)


    def animate(self):
        if self.animating :
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.sprites):
                self.frame_index = 4

            self.image = self.sprites[int(self.frame_index)]

    def update(self):
        self.animate()

