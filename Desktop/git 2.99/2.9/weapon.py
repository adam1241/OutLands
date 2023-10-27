import pygame
class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]

        #graphique
        full_path = f'Graphics/Sword/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(16,16))

        #placement of the weapon
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
        elif direction == 'left' :
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))
        else :
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10,0))