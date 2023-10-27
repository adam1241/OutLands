import pygame
from tile import Tile


class Object_level(Tile):
    def __init__(self,pos, groups,sprite_type,surface):
        if not (sprite_type == 'auto_collect' or sprite_type == 'press_to_collect') :
            raise TypeError("la classe Object_level n'admet que deux types de sprites")


        super().__init__(pos, groups,sprite_type,surface)
        self.type = sprite_type

        def collect(self):
                self.kill()


