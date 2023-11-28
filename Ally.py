import pygame
from settings import *
from entity import Entity
from support import *
class Ally(Entity):
    def __init__(self,ally_name,pos,groups,obstacle_sprites,map,sprite_type,id,status,dialogue_index):

        self.id=id
        # general setup
        super().__init__(groups)
        self.sprite_type = sprite_type
        
        # graphics setup
        self.import_graphics(ally_name)
        self.status = status
        self.frame_index=0
        self.frame_index2=0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        #movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        self.ismoving=False
        self.olddirectionx=-1
        self.direct=pygame.math.Vector2(WIDTH,HEIGHT).magnitude()

        self.distance = 0
        self.distance_vect=pygame.math.Vector2() 
        self.direction= pygame.math.Vector2() 
        self.dist_vect_sign= pygame.math.Vector2()
        self.directionx= pygame.math.Vector2() 
        self.num=0

        # stats
        self.ally_name = ally_name
        ally_info = ally_data[self.ally_name]
        self.health = ally_info['health']
        self.speed = ally_info['speed']
        self.resistance = ally_info['resistance']
        self.animation_speed = ally_info['animation_speed']
        #self.dialogue=dialogue[self.ally_name]

        #text
        self.dialogue_index=dialogue_index
        self.letter_index=0
        self.stop_editing=False

        self.display_surface = pygame.display.get_surface()

        self.background_color = (251, 251, 219)
        self.current_dialogue=dialogue[self.ally_name][self.dialogue_index]
        self.discution_pos=dialogue[self.ally_name][self.dialogue_index][-2]
        self.text=dialogue[self.ally_name][self.dialogue_index][0]
        self.ligne=0
        self.page=1
        self.previous_letters = ['' for i in range(100)]
        self.can_talk=True
        self.adding_text=True
        self.return_index=0
        self.lancez_bat=False
        self.lancez_dragon=False

        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 4500
        self.map=map
        self.end_screen=False

    def import_graphics(self,name):
        self.animations = {'idle_left':[] ,
                           'idle_right':[] }
        main_path = f'Graphics/{name}/'
        
        if 'fairy'in name:
            self.animations = {'down':[],'up':[],'right':[],'left':[]}
            for animation in self.animations.keys():
                self.animations[animation] = import_folder(main_path + animation +'/images/') 
        else:
            for animation in self.animations.keys():
                self.animations[animation] = import_folder(main_path + animation +'/images/') 

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

    def get_status(self,player,mode=1):
        if mode:
            self.distance = self.get_player_distance_direction(player)[0]
            self.distance_vect=self.get_player_distance_direction(player)[2]
            
            if self.map==4 :
                if 'fairy'in self.ally_name:
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
                else:
                        # movement input
                    if     self.direction[0]>0 and float(self.distance_vect[0])>200 :
                        self.status = 'idle_right'
                    elif    self.direction[0]<0 and float(self.distance_vect[0])>200:
                        self.status = 'idle_left'
                    elif     float(self.distance_vect[0])<200 and self.direction[1]>0 :
                        self.status = 'idle_right'
                    elif    self.direction[1]<0 and float(self.distance_vect[0])<200:
                        self.status = 'idle_right'
                    else:
                        self.status = 'idle_right'
        else:#follow path
            pass   
    def actions(self,player):
        if self.vulnerable:
            if self.ismoving or 'move' in self.status:
                self.direction = self.get_player_distance_direction(player)[1]
            else:
                self.direction = pygame.math.Vector2()
       

    def animate(self):
        
        animation = self.animations[self.status]
        self.frame_index = self.animation_speed +self.frame_index
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)


        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else :
            self.image.set_alpha(255)


    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.vulnerable :
            if current_time - self.hit_time >= self.invincibility_duration*3/8:
                self.vulnerable = True

    def get_damage(self,player,level):
        if self.vulnerable :
            self.direction = self.get_player_distance_direction(player)[1]
            if player.attacking :
                if  level.ui.frame_index!=8:
                    level.ui.frame_index+=1
                self.health -= player.get_full_weapon_damage()
                self.hit_time = pygame.time.get_ticks()
                self.vulnerable = False

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.dead=True

    def in_the_list(self,list):
        for enemy in list:
            if enemy.id==self.id:
                return True
        return False
    def update(self):
        if self.distance<=1100:
            
            self.near=True
            
            self.hit_reaction()
            self.animate()
            self.cooldowns()
            self.check_death()

    def ally_update(self,player,level):
        self.distance=self.get_player_distance_direction(player)[0]
        if self.distance<=1100:
            self.get_status(player)
            self.actions(player)
            self.move(self.speed)
            self.positionnement(level)
            self.Dialogue(player)
    def Dialogue(self,player):
        
        
        if self.can_talk:

            keys = pygame.key.get_pressed()

            if self.ally_name in ['fairy_princ','fairy_queen','king']:
                print(self.ally_name)
                if player.rect.centerx>=self.discution_pos[0][0] and player.rect.centerx<=self.discution_pos[0][1] :
                    if player.rect.centery>=self.discution_pos[1][0]  and player.rect.centery<=self.discution_pos[1][1] :
                        
                        player.discussing=True
                        player.Stop_moving=True
                        text_surf=pygame.Surface((WIDTH, HEIGHT/4))
                        text_surf.fill(self.background_color)
                        text_rect=text_surf.get_rect(topleft=(0,HEIGHT*3/4))
                        self.display_surface.blit(text_surf,text_rect)
                        text_message_0 = pygame.font.Font('font/Pixeltype.ttf', 80)
                        if self.adding_text:
                            
                            self.previous_letters[self.ligne]+=self.text[self.ligne][self.letter_index]
                        for line in range(self.ligne+1):
                            game_message_0 = text_message_0.render(self.previous_letters[line],False,(0, 9, 94))
                            game_message_rect_0 = game_message_0.get_rect(topleft = (WIDTH*1/7 ,HEIGHT*25/32+line*45))
                            self.display_surface.blit(game_message_0,game_message_rect_0)
                        
                        self.letter_index+=1
                        if self.letter_index>=len(self.text[self.ligne]):
                            self.letter_index=0
                            self.ligne+=1
                        if self.ligne>=len(self.text):
                            self.ligne-=1
                            self.letter_index=len(self.text[self.ligne])-1
                            self.adding_text=False
                        if keys[pygame.K_RETURN] :
                            self.return_index+=1
                            if self.return_index<12 :
                                if self.return_index>7:
                                
                                    self.previous_letters=self.text
                                    self.letter_index=len(self.text[self.ligne])-1
                                    self.adding_text=False
                                    self.ligne=len(self.text)-1
                            elif self.page< len(self.current_dialogue)-2:
                                if self.return_index>16:
                                    self.text=dialogue[self.ally_name][self.dialogue_index][self.page]
                                    self.page+=1
                                    self.return_index=0
                                    self.previous_letters = ['' for i in range(100)]
                                    self.letter_index=0
                                    self.adding_text=True
                                    self.ligne=0
                                


                            if self.page>= len(self.current_dialogue)-2:
                                if self.return_index==6 :
                                    self.can_talk=False
                                    if self.dialogue_index +1< len(dialogue[self.ally_name].keys()):
                                        self.dialogue_index+=1
                                        self.current_dialogue=dialogue[self.ally_name][self.dialogue_index]
                                    player.Stop_moving=False
                                    player.discussing=False
                                    self.return_index=0
                                    if self.ally_name=='fairy_queen'and self.dialogue_index==2:
                                        self.lancez_bat=True
                                    if self.ally_name=='king':
                                        self.lancez_dragon=True
                                    if self.ally_name=='fairy_queen'and self.dialogue_index==3:
                                        self.end_screen=True
                        self.animate_discution()
    
    def scale_surface(self,surface, scale_factor):
        # Calculate the new width and height based on the scale factor
        new_width = int(surface.get_width() * scale_factor)
        new_height = int(surface.get_height() * scale_factor)
        
        # Use pygame.transform.scale() to resize the surface
        scaled_surface = pygame.transform.scale(surface, (new_width, new_height))
        
        return scaled_surface
    
    def animate_discution(self):
            if self.ally_name=='fairy_princ' or self.ally_name=='fairy_queen':
                status='down'
            else:
                status='idle_right'

        #animation part 
            animation = self.animations[status]
            self.frame_index2 = self.animation_speed +self.frame_index2
            if self.frame_index2 >= len(animation):
                self.frame_index2 = 0
            self.image2 =self.scale_surface( animation[int(self.frame_index2)],4)
            self.rect2 = self.image.get_rect(center = (WIDTH*6/7 ,HEIGHT*25/32))
            self.display_surface.blit(self.image2, self.rect2)
    
    def positionnement(self,level):
        if self.ally_name=='fairy_princ' or self.ally_name=='fairy_queen':
            level.display_surface.blit(self.image,self.current_dialogue[-2])
        
        

    