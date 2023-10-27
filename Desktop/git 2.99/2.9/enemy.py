import pygame
from settings import *
from entity import Entity
from support import *
class Enemy(Entity):
    def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,map,sprite_type,id):

        self.id=id
        # general setup
        super().__init__(groups)
        self.sprite_type = sprite_type

        # graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle_left'
        if monster_name=='dark_fairy':
            self.status = 'down'
        elif monster_name=='bat': 
            self.status = 'left'
        elif monster_name=='ghost'or monster_name=='boss' or monster_name=='boss_ally' or monster_name=='knight2'or monster_name=='knight3'or monster_name=='gardien_eau'or monster_name=='demon'or monster_name=='dragon1' or monster_name == 'squelance':
            self.status = 'idle_left'
        self.frame_index=0

        

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        #movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        self.ismoving=False
        self.olddirectionx=-1
        self.direct=pygame.math.Vector2(WIDTH,HEIGHT).magnitude()

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        self.animation_speed = monster_info['animation_speed']
        self.near_distance=monster_info['near_distance']

        #player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 10 ########important when you change the speed of the game!!!!!
        self.damage_player = damage_player

        #invinsibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 4500

        # distance between enemy and player
        self.distance = 0
        self.distance_vect=pygame.math.Vector2() 
        self.direction= pygame.math.Vector2() 
        self.dist_vect_sign= pygame.math.Vector2()
        self.directionx= pygame.math.Vector2() 
        self.num=0

        #list of enemies
        self.enemy_list=[]
        #sound
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        #game_over
        self.game_over_index=0
        self.counter = 0

        self.map=map
        self.near=False#if the enemies is near enough to the player to be shown on the screen
        self.dead=False#True if the enemy is not yet dead
    def __eq__(self, other):
        if isinstance(other, Enemy):
            return self.id == other.id
        return False
    def __hash__(self):
        return hash(self.id)

    def import_graphics(self,name):
        self.animations = {'idle_left':[] , 'move_left':[] ,'attack_left':[],
                           'idle_right':[] , 'move_right':[] ,'attack_right':[]}
        main_path = f'Graphics/{name}/'
        
        if name=='dark_fairy':
            self.animations = {'down':[],'up':[],'right':[],'left':[],}
            for animation in self.animations.keys():
                self.animations[animation] = import_folder(main_path + animation +'/images/')

        elif name=='bat': 
            self.animations = {'right':[],'left':[]}
            for animation in self.animations.keys():
                self.animations[animation] = import_folder(main_path + animation+'/images/')  
        elif name=='ghost' or name=='boss'or name=='boss_ally'or name=='knight2'or name=='knight3'or name=='gardien_eau'or name=='demon'or name=='dragon1' or name == 'squelance':
            self.animations = {'idle_right':[],'idle_left':[],'right':[],'left':[],'right_attack':[],'left_attack':[],
            'left_damage':[],'right_damage':[],'left_game_over':[],'right_game_over':[]}
            for animation in self.animations.keys():
                if name == 'squelance' :
                    self.animations[animation] = import_folder(main_path + animation)
                else :
                    self.animations[animation] = import_folder(main_path + animation+'/images/')
            
        else:
            for animation in self.animations.keys():
                if name == 'lv1_boss' or name== 'phontom':
                    folder = import_folder(main_path + animation)
                    for image in  folder :
                        image2 = self.scale_surface(image,4)
                        self.animations[animation].append(image2)
                else :
                    self.animations[animation] = import_folder(main_path + animation)
        

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        self.distance_vect=player_vec - enemy_vec
        self.distance = (self.distance_vect).magnitude()
        self.dist_vect_sign[0]=self.distance_vect[0]
        self.dist_vect_sign[1]=self.distance_vect[1]
        self.distance_vect[0]=abs(self.distance_vect[0])
        self.distance_vect[1]=abs(self.distance_vect[1])

        if self.vulnerable:
            if self.distance > 0  :
                self.direction = (player_vec - enemy_vec).normalize()
            else:
                self.direction = pygame.math.Vector2()

        return (self.distance,self.direction,self.distance_vect,self.dist_vect_sign)

    def get_status(self,player):
        self.distance = self.get_player_distance_direction(player)[0]
        self.distance_vect=self.get_player_distance_direction(player)[2]
        if self.vulnerable:
            self.direction= self.get_player_distance_direction(player)[1]
        if self.map==4 or self.monster_name=='boss_ally' or self.monster_name == 'squelance':
            if self.vulnerable:
		

                if self.distance <= self.attack_radius and self.can_attack:
                    if  'attack' not in self.status:
                        self.frame_index = 0
                    if self.monster_name=='dark_fairy':
                            # movement input
                        if     self.direction[0]>0 and float(self.distance_vect[0])>200 :
                            self.status = 'right'
                        elif    self.direction[0]<0 and float(self.distance_vect[0])>200:
                            self.status = 'left'
                        elif     float(self.distance_vect[0])<200 and self.direction[1]>0 :
                            self.status = 'down'
                        elif    self.direction[1]<0 and float(self.distance_vect[0])<200:
                            self.status = 'up'
                        else:
                            self.status = 'down'
                    if self.monster_name=='bat':
                        if     self.direction[0]>0 :
                            self.status = 'right'
                        elif    self.direction[0]<0:
                            self.status = 'left'
                        else:
                            self.status = 'left'
                    if self.monster_name=='ghost': 
                        if     self.direction[0]>0 :
                            self.status = 'right_attack'
                            self.olddirection=self.direction[0]
                        elif    self.direction[0]<0:
                            self.status = 'left_attack'
                            self.olddirection=self.direction[0]
                        elif     self.direction[0]==0 and self.olddirectionx<0 :
                            self.status = 'left_attack'
                        elif     self.direction[0]==0 and self.olddirectionx>0 :
                            self.status = 'right_attack'
                        else:
                            self.status = 'right_attack'
                    if self.monster_name=='boss'or self.monster_name=='boss_ally' or self.monster_name=='knight2'or self.monster_name=='knight3'or self.monster_name=='gardien_eau'or self.monster_name=='demon'or self.monster_name=='dragon1' or self.monster_name == 'squelance':
                        if     self.direction[0]>0 :
                            self.status = 'right_attack'
                            self.olddirection=self.direction[0]
                        elif    self.direction[0]<0:
                            self.status = 'left_attack'
                            self.olddirection=self.direction[0]
                        elif     self.direction[0]==0 and self.olddirectionx<0 :
                            self.status = 'left_attack'
                        elif     self.direction[0]==0 and self.olddirectionx>0 :
                            self.status = 'right_attack'
                        else:
                            self.status = 'right_attack'
                    
                
                elif self.distance <= self.notice_radius:
                    self.ismoving=True
                    if self.monster_name=='dark_fairy':
                            # movement input
                        if     self.direction[0]>0 :
                            self.status = 'right'
                        elif    self.direction[0]<0:
                            self.status = 'left'
                        elif     self.direction[0]==0 and self.direction[1]>0 :
                            self.status = 'down'
                        elif    self.direction[0]==0 and self.direction[1]<0 :
                            self.status = 'up'
                        else:
                            self.status = 'down'
                    if self.monster_name=='bat':
                        if     self.direction[0]>0 :
                            self.status = 'right'
                        elif    self.direction[0]<0:
                            self.status = 'left'
                        else:
                            self.status = 'left'
                    if self.monster_name=='ghost': 
                        if     self.direction[0]>0 :
                            self.status = 'right'
                            self.olddirection=self.direction[0]
                        elif    self.direction[0]<0:
                            self.status = 'left'
                            self.olddirection=self.direction[0]
                        elif     self.direction[0]==0 and self.olddirectionx<0 :
                            self.status = 'left'
                        elif     self.direction[0]==0 and self.olddirectionx>0 :
                            self.status = 'right'
                        else:
                            self.status = 'right'
                    if self.monster_name=='boss'or self.monster_name=='boss_ally'or self.monster_name=='knight2'or self.monster_name=='knight3'or self.monster_name=='gardien_eau'or self.monster_name=='demon'or self.monster_name=='dragon1' or self.monster_name == 'squelance':
                        if     self.direction[0]>0 :
                            self.status = 'right'
                            self.olddirection=self.direction[0]
                        elif    self.direction[0]<0:
                            self.status = 'left'
                            self.olddirection=self.direction[0]
                        elif     self.direction[0]==0 and self.olddirectionx<0 :
                            self.status = 'left'
                        elif     self.direction[0]==0 and self.olddirectionx>0 :
                            self.status = 'right'
                        else:
                            self.status = 'right'
                    
                
                else:
                    if self.monster_name=='dark_fairy':
                            # movement input
                        if     self.direction[0]>0 :
                            self.status = 'right'
                        elif    self.direction[0]<0:
                            self.status = 'left'
                        elif     self.direction[0]==0 and self.direction[1]>0 :
                            self.status = 'down'
                        elif    self.direction[1]<0 and self.direction[0]==0:
                            self.status = 'up'
                        else:
                            self.status = 'down'
                    if self.monster_name=='bat':
                        if     self.direction[0]>0 :
                            self.status = 'right'
                        elif    self.direction[0]<0:
                            self.status = 'left'
                        else:
                            self.status = 'left'
                    if self.monster_name=='ghost': 
                        if     self.direction[0]>0 :
                            self.status = 'idle_right'
                            self.olddirection=self.direction[0]
                        elif    self.direction[0]<0:
                            self.status = 'idle_left'
                            self.olddirection=self.direction[0]
                        elif    self.direction[0]==0 and self.olddirectionx<0 :
                            self.status = 'idle_left'
                        elif     self.direction[0]==0 and self.olddirectionx>0 :
                            self.status = 'idle_right'
                        else:
                            self.status = 'idle_right'
                    if self.monster_name=='boss'or self.monster_name=='boss_ally'or self.monster_name=='knight2'or self.monster_name=='knight3'or self.monster_name=='gardien_eau'or self.monster_name=='demon'or self.monster_name=='dragon1' or self.monster_name == 'squelance':
                        if     self.direction[0]>0 :
                            self.status = 'idle_right'
                            self.olddirection=self.direction[0]
                        elif    self.direction[0]<0:
                            self.status = 'idle_left'
                            self.olddirection=self.direction[0]
                        elif     self.direction[0]==0 and self.olddirectionx<0 :
                            self.status = 'idle_left'
                        elif     self.direction[0]==0 and self.olddirectionx>0 :
                            self.status = 'idle_right'
                        else:
                            self.status = 'idle_right'
            else:
                if self.monster_name=='boss'or self.monster_name=='ghost'or self.monster_name=='boss_ally'or self.monster_name=='knight2'or self.monster_name=='knight3'or self.monster_name=='gardien_eau'or self.monster_name=='demon'or self.monster_name=='dragon1' or self.monster_name == 'squelance':
                    if     self.dist_vect_sign[0]>0:
                        self.status = 'right_damage'
                    else:
                        self.status = 'left_damage'
        else:
            if self.distance <= self.attack_radius and self.can_attack:
                if self.status != 'attack_left' and self.status != 'attack_right' :
                    self.frame_index = 0
                    if player.rect.x < self.rect.x :
                        self.status = 'attack_left'
                    else :
                        self.status = 'attack_right'
            elif self.distance <= self.notice_radius:
                if player.rect.x < self.rect.x:
                    self.status = 'move_left'
                else :
                    self.status = 'move_right'
            else :
                if player.rect.x < self.rect.x:
                    self.status = 'idle_left'
                else :
                    self.status = 'idle_right'
        if self.health<=0: 
            if self.counter == 0 :
                self.death_direction = self.direction[0]
                print(self.death_direction)
                self.counter += 1
            self.game_over_index+=1
            if self.monster_name=='ghost'or self.monster_name=='boss'or self.monster_name=='knight2'or self.monster_name=='knight3'or self.monster_name=='gardien_eau'or self.monster_name == 'squelance':
                if -100 > self.death_direction or 0<self.death_direction<100:
                    self.status='left_game_over'
                else:
                    self.status='right_game_over'

    def actions(self,player):
        if  'attack' in self.status or self.distance<=self.near_distance :
            if self.vulnerable:
                self.attack_time = pygame.time.get_ticks()
                if not self.monster_name=='boss_ally':
                    self.damage_player(self.attack_damage,self.attack_type)
            if not self.can_attack:
                self.attack_time = pygame.time.get_ticks()
        if self.vulnerable:
            if self.ismoving or 'move' in self.status:
                self.direction = self.get_player_distance_direction(player)[1]
            else:
                self.direction = pygame.math.Vector2()
       

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        
        if  self.frame_index >= len(animation):
            if 'attack' in self.status :
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        if self.monster_name=='gardien_eau'or self.monster_name=='demon':
            self.image = animation[int(self.frame_index)]
            self.image=self.scale_surface(self.image , 3)
            self.rect = self.image.get_rect(center = self.hitbox.center)
        if self.monster_name == 'squelance' :
            self.image = self.scale_surface(self.image,2)
            self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else :
            self.image.set_alpha(255)


    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown :
                self.can_attack = True
        if not self.vulnerable :
            if current_time - self.hit_time >= self.invincibility_duration*3/8:
                self.vulnerable = True

    def get_damage(self,player,level):
        if self.vulnerable :
            self.direction = self.get_player_distance_direction(player)[1]
            if player.attacking :
                if ('right' in player.status and 'left' in self.status) or ('left' in player.status and 'right' in self.status) :
                    if  level.ui.frame_index!=8:
                        level.ui.frame_index+=1
                    self.health -= player.get_full_weapon_damage()
                    player.exp+=1
                    if player.exp>60: 
                        player.level_bar+=2
                        player.exp=0
                    level.game.exp=player.exp
                    level.game.level_bar=player.level_bar
                    self.hit_time = pygame.time.get_ticks()
                    self.vulnerable = False
    def get_damage_by_8th(self,eight,level):
        if self.vulnerable :
            self.direction = self.get_player_distance_direction(eight)[1]
            if 'attack'in eight.status :
                if ('right' in eight.status and 'left' in self.status) or ('left' in eight.status and 'right' in self.status) :
                    if  level.ui.frame_index!=8:
                        level.ui.frame_index+=1
                    self.health -= eight.attack_damage
                    self.hit_time = pygame.time.get_ticks()
                    self.vulnerable = False
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
    def check_death(self):
        if self.health <= 0:
            if self.monster_name=='ghost'or self.monster_name=='boss'or self.monster_name=='knight2'or self.monster_name=='knight3'or self.monster_name=='gardien_eau'or self.monster_name=='demon'or self.monster_name=='dragon1' or self.monster_name == 'squelance':
                if self.game_over_index>=15:
                    self.kill()
            else:
                self.kill()
            self.dead=True
    def in_the_list(self,list):
        for enemy in list:
            if enemy.id==self.id:
                return True
        return False
    def scale_surface(self,surface, scale_factor):
        # Calculate the new width and height based on the scale factor
        new_width = int(surface.get_width() * scale_factor)
        new_height = int(surface.get_height() * scale_factor)
        
        # Use pygame.transform.scale() to resize the surface
        scaled_surface = pygame.transform.scale(surface, (new_width, new_height))
        
        return scaled_surface
    def update(self):
        if self.distance<=1100:
            self.near=True
            self.hit_reaction()
            self.animate()
            self.cooldowns()
            self.check_death()

    def enemy_update(self,player):
        self.distance=self.get_player_distance_direction(player)[0]
        if self.distance<=1100:
            self.get_status(player)
            if self.distance<=self.notice_radius:
                self.actions(player)
                self.move(self.speed)
