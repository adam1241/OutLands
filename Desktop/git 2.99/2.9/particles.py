import pygame
from support import import_folder
from random import choice 

class AnimationPlayer:
	def __init__(self,level):
		self.frames = {
			'projectile_left': import_folder('Graphics/projectile/left'),
			'projectile_right': import_folder('Graphics/projectile/right'),
			}
	
	def reflect_images(self,frames):
		new_frames = []

		for frame in frames:
	 		flipped_frame = pygame.transform.flip(frame,True,False)
	 		new_frames.append(flipped_frame)
		return new_frames

	def create_projectile_left(self,pos,groups,level):
	 	animation_frames = self.frames['projectile_left']
	 	ParticleEffect(pos,animation_frames,groups,1,level)
	
	def create_projectile_right(self,pos,groups,level):
	 	animation_frames = self.frames['projectile_right']
	 	ParticleEffect(pos,animation_frames,groups,-1,level)
		


class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self,pos,animation_frames,groups,direction,level):
		super().__init__(groups)
		self.frame_index = 0
		self.animation_speed = 0.15
		self.frames = animation_frames
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.hitbox = self.rect
		self.direction = direction
		self.level = level

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]
			self.rect.centerx += self.direction*20
	def damage(self) :
		for enemy in self.level.attackable_sprites :
			if self.rect.colliderect(enemy.rect) :
				enemy.health -= 10
				enemy.vulnerable = False
				enemy.can_attack = False
				enemy.attack_time = pygame.time.get_ticks()
				enemy.hit_time = pygame.time.get_ticks()
	def update(self):
		self.animate()
		self.damage()
