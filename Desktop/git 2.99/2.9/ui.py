import pygame
from settings import *
from support import *

class UI:
	def __init__(self):

		# general
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

		# bar setup
		self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
		self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)
		#index of gem
		self.frame_index=7

		# convert weapon dictionary
		self.weapon_graphics = []
		for weapon in weapon_data.values():
			path = weapon['graphic']
			weapon_list = import_folder(path)
			weapon_list=weapon_list[5:]+weapon_list[0:5]
			
			weapon = weapon_list[self.frame_index].convert_alpha()
			self.weapon_graphics.append(weapon_list)
		# convert magic dictionary
		self.magic_graphics = []
		for magic in magic_data.values():
			magic = pygame.image.load(magic['graphic']).convert_alpha()
			self.magic_graphics.append(magic)

		self.HEALTH_COLOR ='#000000'


	def refresh_gem(self) :
		weapon = self.weapon_graphics[self.frame_index].convert_alpha()
		


	def show_bar(self,current,max_amount,bg_rect,color,health):
		ratio = current / max_amount
		if health:
			if ratio>=0.6:
				self.HEALTH_COLOR ='#1eff78'
			if ratio<0.6 and ratio>=0.25:
				self.HEALTH_COLOR ='#ffb709'
			if ratio<0.25:
				self.HEALTH_COLOR ='#dd0000'
		# draw bg

		pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

		# converting stat to pixel
		ratio = current / max_amount
		current_width = bg_rect.width * ratio
		current_rect = bg_rect.copy()
		current_rect.width = current_width

		# drawing the bar
		if health:
			pygame.draw.rect(self.display_surface,self.HEALTH_COLOR,current_rect)
		else:
			pygame.draw.rect(self.display_surface,color,current_rect)
		pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)

	def show_exp(self,exp):
		text_surf = self.font.render('EXP: LEV '+str(int(exp)),False,TEXT_COLOR)
		x = self.display_surface.get_size()[0] - 20
		y = self.display_surface.get_size()[1] - 20
		text_rect = text_surf.get_rect(bottomright = (x,y))

		pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
		self.display_surface.blit(text_surf,text_rect)
		pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

	def selection_box(self,left,top, has_switched):
		bg_rect = pygame.Rect(left,top,(3/2)*ITEM_BOX_SIZE,(3/2)*ITEM_BOX_SIZE)
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
		if has_switched:
			pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
		else:
			pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
		return bg_rect

	def weapon_overlay(self,weapon_index,has_switched):
		bg_rect = self.selection_box(10,HEIGHT-140,has_switched)
		weapon_surf = self.weapon_graphics[weapon_index][self.frame_index]
		if self.frame_index==8:
			alpha= self.wave_value(1/1600,255,1,0)
			weapon_surf.set_alpha(alpha)
		weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

		self.display_surface.blit(weapon_surf,weapon_rect)
	def magic_overlay(self,magic_index,has_switched):
		bg_rect = self.selection_box(140,HEIGHT-140,has_switched)
		magic_surf = self.magic_graphics[magic_index]
		magic_rect = magic_surf.get_rect(center = bg_rect.center)

		self.display_surface.blit(magic_surf,magic_rect)
	def wave_value(self,f,a,boolean,phase):
		if boolean:
			return a*abs(sin(2*pi*f*pygame.time.get_ticks()+phase))
		else:
			return a*(sin(2*pi*f*pygame.time.get_ticks()+phase))

	def display(self,player):


		self.show_bar(player.health,player.stats['health'],self.health_bar_rect,self.HEALTH_COLOR,1)
		self.show_bar(player.exp,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR,0)

		self.show_exp(player.level_bar)

		self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)
		self.magic_overlay(player.magic_index,not player.can_switch_magic)
