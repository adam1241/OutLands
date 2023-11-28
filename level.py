import pygame
from support import *
from tile import Tile
from player import Player
from random import choice
from weapon import Weapon
from ui import UI
from enemy import Enemy
from debug import debug
from rock import Rock
from Object_level import Object_level
from math import *
from settings import *
from Ally import *

class Level:

    def __init__(self,main,level_number,init=(0,0),scene_number=1,version=0):
        #timer for  geme 3
        self.timer=0
        # surface principale
        self.player = None
        self.enemy=None
        self.display_surface = pygame.display.get_surface()
        # types des sprites :
        self.visible_sprites = YSortCameraGroup(level_number,scene_number)
        self.obstacle_sprites = pygame.sprite.Group()
        self.obstacle_sprites_ennemie=pygame.sprite.Group()
        self.anything=pygame.sprite.Group()
        #attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.attacker_sprites =pygame.sprite.Group()
        self.nothing=pygame.sprite.Group()
        #objets à prendre
        self.level_objects = pygame.sprite.Group()
        #roches
        self.rock_sprites = pygame.sprite.Group()
        #boss
        self.boss_sprite = pygame.sprite.Group()
        #level data
        self.number = level_number
        self.scene = scene_number
        self.init=init
        self.get_bat=False#lancer l ennemie du monde 4 scene 2
        #point de depart dans differents scene après mort           
        if self.number==1 and self.scene==1: 
            self.initial_point=(984,670)
        if self.number==1 and self.scene==3: 
            self.initial_point=(2200,3038)
        if self.number==2 and self.scene==1:
            self.initial_point=(60*16,40*16)
        if self.number==3 and self.scene == 1: 
            self.initial_point=(5004,1410)
        if self.number==3 and self.scene == 2: 
            self.initial_point=(934,1556)
        if self.number==4: 
            if self.scene==1:
                self.initial_point=(1056,1536)
            if self.scene==2:
                self.initial_point=(1336,3000)
            if self.scene==3:
                self.initial_point=(2136,2046)
            if self.scene==4:
                self.initial_point=(2040,2974)
            if self.scene==5:
                self.initial_point=(2040,2974)
            if self.scene==7:
                self.initial_point=(1424,1181)
        self.game=main
        #user interface
        if level_number == 5 or level_number == 6:
            self.ui = None
        else : 
            self.ui = UI()
        #shield
        self.shield=None
        self.shield_timer=0
        self.coef=180
        #stuff of the 8th gemme
        self.enemy_list=[]#list of enmies on the screen that the monster of the 8th gem can attack
        self.near_enemy_list=[]
        self.killed=[]
        self.current_enemy=None#the nemie that should be attacked by the monster of the 8th gemme
        self.enemy8th=None#the monster of the 8th gem
        print(self.game.exp)
        #bat
        self.special_enemy=None
        self.sepecial_ally=None
        self.final_enemy=None
        self.boss_enemy=None
        #end screen declancheur.
        self.end_screen=False
        #dragon1
        self.passez_scene7=False
        # creation de la map
        if level_number==5:
            self.create_intro_end(0)
        if level_number==6:
            self.create_intro_end(3)
        if level_number == 1:
            if scene_number == 1:
                self.create_map1_scene1()
            if scene_number == 2:
                self.create_map1_scene2()
            if scene_number == 3 :
                self.create_map1_scene3()
        if level_number == 2:
            self.create_map2()
        if level_number == 3: #This is Amine level (it will have also a slight modification on the size of the tiles)
            if scene_number == 1:
                self.create_map3()
            if scene_number == 2:
                self.create_map3_scene2()
            if scene_number == 3:
               self.create_map3_scene3()
        # creation de la map4
        if level_number==4:
            if scene_number == 1 and not version:
                self.create_map4_scene1()
            if scene_number == 1 and  version:
                self.create_map4_scene1_2()
            if scene_number == 2:
                self.create_map4_scene2()
            if scene_number == 3 :
                self.create_map4_scene3()
            if scene_number == 4 :
                self.create_map4_scene4()
            if scene_number == 5 :
                self.create_map4_scene5()
            if scene_number == 6 :
                self.create_map4_scene6()
            if scene_number == 7 :
                self.create_map4_scene7()
            
        #music
        self.weapon_hit_sound = pygame.mixer.Sound('audio/hit.wav')
        self.weapon_hit_sound.set_volume(0.2)
        self.sound2_zone=False

    #def create_special():
      #  self.sepecial_ally=
    def create_intro_end(self,dialogue_index) :
        self.player = Player((2080,1876),
                                [self.visible_sprites,self.attacker_sprites],
                                self.obstacle_sprites,
                                self.create_attack,
                                self.destroy_attack,
                                self.create_magic,self.game.health,self.game.exp,self.game.level_bar,map=5)

        self.ally = Ally('fairy_queen',(2080, 1700),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_princ878','down',dialogue_index)
        Ally('fairy_green',(1910, 1800),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_princ878','up',0)
        Ally('fairy_green',(1950, 1900),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_princ878','up',0)
        Ally('fairy_green',(2000, 1800),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_princ878','up',0)
        Ally('fairy_green',(2020, 1900),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_princ878','up',0)
        Ally('fairy_green',(2090, 1800),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_princ878','up',0)
        Ally('fairy_green',(2100, 1890),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_princ878','up',0)
        Ally('fairy_green',(2140, 1850),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_princ878','up',0)
        Ally('fairy_green',(2100, 1950),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_princ878','up',0)
        Ally('fairy_green',(2160, 1800),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_princ878','up',0)
        Ally('fairy_green',(2200, 1800),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_princ878','up',0)
        
    def create_map1_scene1(self):
        TILESIZE = 32
        layouts = {
            'grass' : import_csv_layout('real level/CSV/Level_1 map_grass.csv'),
            'plants': import_csv_layout('real level/CSV/Level_1 map_plants.csv'),
            'house': import_csv_layout('real level/CSV/Level_1 map_House.csv'),

            'boundary': import_csv_layout('real level/CSV/Level_1 map_Trees.csv'),
            'rocks': import_csv_layout('real level/CSV/Level_1 map_Rocks.csv'),
            'water_rocks' : import_csv_layout('real level/CSV/Level_1 map_water rocks.csv'),
            'wood' : import_csv_layout('real level/CSV/Level_1 map_Wood.csv'),
            'player' : import_csv_layout('real level/CSV/Level_1 map_player.csv'),
            'ennemies' : import_csv_layout('real level\CSV\Level_1 map_ennemies.csv')
        }
        i = 0
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        #test
                        if style == 'boundary' or style == 'rocks' or style == 'wood' or style== 'house':
                            Tile((x, y), [self.obstacle_sprites,self.obstacle_sprites_ennemie], 'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'player' and i==0:
                            self.player = Player((60*16,40*16),
                                                 [self.visible_sprites,self.attacker_sprites],
                                                 self.obstacle_sprites,
                                                 self.create_attack,
                                                 self.destroy_attack,
                                                 self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                            i = 1                   
                        if style == 'ennemies' :
                            if col == '4150' :
                                monster_name = 'dragon'
                                group = [self.visible_sprites,self.attackable_sprites]
                            elif col == '3308' :
                                monster_name = 'squelance'
                                group = [self.visible_sprites,self.attackable_sprites]
                            else :
                                monster_name = 'flying_rock'
                                group = [self.visible_sprites,self.attackable_sprites,self.obstacle_sprites]

                            Enemy(monster_name, (x,y), group, self.obstacle_sprites_ennemie, self.damage_player,1,'enemy',monster_name+str(x+y))


                            
                        if style == 'water_rocks' :
                            Tile((x, y), [self.obstacle_sprites,self.obstacle_sprites_ennemie], 'invisible',pygame.Surface((TILESIZE,TILESIZE)))

    def create_map1_scene2(self):
        TILESIZE = 16*4
        layouts = {
            'floor' : import_csv_layout("real level/CSV/First gym/interior_floor.csv"),
            'meubles': import_csv_layout("real level/CSV/First gym/interior_meubles.csv"),
            'tapis': import_csv_layout("real level/CSV/First gym/interior_Tapis.csv"),
            'wall': import_csv_layout("real level/CSV/First gym/interior_wall.csv"),
            'player' : import_csv_layout('real level/CSV/First gym/interior_player.csv')
        }
        i = 0
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        #test
                        if style == 'meubles' or style == 'wall' :
                            Tile((x, y), [self.obstacle_sprites,self.obstacle_sprites_ennemie], 'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'player' and col == '163':
                            
                            self.player = Player((x,y),
                                                 [self.visible_sprites,self.attacker_sprites],
                                                 self.obstacle_sprites,
                                                 self.create_attack,
                                                 self.destroy_attack,
                                                 self.create_magic,self.game.health,self.game.exp,self.game.level_bar)

                            i = 1

    def create_map1_scene3(self):
        TILESIZE = 32
        layouts = {
            'grass': import_csv_layout("real level/CSV/boss/mini_boss_grass.csv"),
            'wall': import_csv_layout("real level/CSV/boss/mini_boss_mur.csv"),
            'rocks': import_csv_layout("real level/CSV/boss/mini_boss_rocks.csv"),
            'sol': import_csv_layout('real level/CSV/boss/mini_boss_sol.csv'),
            'player' : import_csv_layout('real level/CSV/boss/mini_boss_player.csv'),
            'boss' : import_csv_layout('real level/CSV/boss/mini_boss_boss.csv')
        }
        i = 0
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'wall' :
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'wall',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'player' and row != 0  :
                            
                            self.player = Player((x, y),
                                                 [self.visible_sprites,self.attacker_sprites],
                                                 self.obstacle_sprites,
                                                 self.create_attack,
                                                 self.destroy_attack,
                                                 self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                        if style == 'boss' :
                            if col == '1' :
                                self.enemy=Enemy('lv1_boss', (x,y), [self.visible_sprites,self.attackable_sprites], self.obstacle_sprites_ennemie, self.damage_player,1,'enemy','lv1_boss'+str(x+y))
                                if self.enemy  :
                                    self.enemy_list.append(self.enemy)

 
                        
                            
    def create_map2(self):
        TILESIZE = 32
        layouts = {
            'grass' : import_csv_layout('Level 2\BIGMAP_Surface.csv'),
            'ennemi' : import_csv_layout('Level 2\BIGMA_Ennemi.csv'),

            'boundary': import_csv_layout('Level 2\BIGMAP_Trees.csv'),
            'player' : import_csv_layout('real level/CSV/Level_1 map_player.csv'),

        }
        i = 0
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        #test
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites,self.obstacle_sprites_ennemie], 'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'player' and i==0:
                            self.player = Player((60*16,40*16),
                                                 [self.visible_sprites,self.attacker_sprites],
                                                 self.obstacle_sprites,
                                                 self.create_attack,
                                                 self.destroy_attack,
                                                 self.create_magic,self.game.health,self.game.exp,self.game.level_bar) 

                            i = 1
                        if style == 'ennemi' :
                            if col == '56':
                            
                                self.enemy=Enemy('raccoon', (x, y),[self.visible_sprites, self.attackable_sprites],self.obstacle_sprites_ennemie, self.damage_player,2,'enemy','bamboo'+str(x+y))
                            if col == '10':
                            
                                self.enemy=Enemy('squeleton', (x, y),[self.visible_sprites, self.attackable_sprites],self.obstacle_sprites_ennemie, self.damage_player,2,'enemy','bamboo'+str(x+y))
                            if self.enemy  :
                                self.enemy_list.append(self.enemy)
    def create_map3(self):
        TILESIZE = 60
        layouts = {
            "boundary": import_csv_layout("Graphics/passage/files_collision_boundaries.csv"),
            "grass": import_csv_layout("Graphics/passage/files_collision_movable.csv"),
            "object": import_csv_layout("Graphics/passage/files_collision_object.csv"),
            "entities": import_csv_layout("Graphics/passage/files_collision_entities.csv"),
        }
        graphics = {
            "grass": import_folder("Graphics/grass"),
            "objects": import_folder("Graphics/objects"),
        }

        # row gives us y position
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):

                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile(
                                (x, y),
                                [self.obstacle_sprites,self.obstacle_sprites_ennemie],
                                "invisible",
                                pygame.Surface((TILESIZE,TILESIZE))
                            )

                        if style == "entities":
                            if col == "68":
                                self.player = Player(
                                    (x,y),
                                    [self.visible_sprites,self.attacker_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,self.game.health,self.game.exp,self.game.level_bar
                                )
                            else:
                                if col == "4":
                                    monster_name = "squeleton"
                                #elif col == "391":
                                 #   monster_name = "spirit"
                                #elif col == "31":
                                 #   monster_name = "raccoon"
                                #else:
                                  #  monster_name = "squid"
                                self.enemy=Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites_ennemie,
                                    self.damage_player,
                                    # self.destroy_attack,
                                    # self.create_magic,
                                    self.number,'enemy',monster_name+str(x+y)
                                )
                                if self.enemy  :
                                    self.enemy_list.append(self.enemy)
    def create_map3_scene2(self):
        TILESIZE = 60
        layouts = {
            "boundary": import_csv_layout("Graphics/boss_map/boss_obstacle.csv"),
            "grass": import_csv_layout("Graphics/boss_map/boss_movable.csv"),
            "entities": import_csv_layout("Graphics/boss_map/boss_entities.csv"),
        }
        graphics = {
            "grass": import_folder("Graphics/grass"),
            "objects": import_folder("Graphics/objects"),
        }

        # row gives us y position
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):

                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile(
                                (x, y),
                                [self.obstacle_sprites,self.obstacle_sprites_ennemie],
                                "invisible",
                                pygame.Surface((TILESIZE,TILESIZE))
                            )

                        if style == "entities":
                            if col == "16":
                                self.player = Player(
                                    (x,y),
                                    [self.visible_sprites,self.attacker_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,self.game.health,self.game.exp,self.game.level_bar
                                )
                            else:
                                if col == "305":
                                    monster_name = "phontom"
                                #elif col == "391":
                                 #   monster_name = "spirit"
                                #elif col == "31":
                                 #   monster_name = "raccoon"
                                #else:
                                  #  monster_name = "squid"
                                self.enemy=Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites_ennemie,
                                    self.damage_player,
                                    # self.destroy_attack,
                                    # self.create_magic,
                                    self.number,'enemy',monster_name+str(x+y)
                                )
                                if self.enemy  :
                                    self.enemy_list.append(self.enemy)
    def create_map4_scene1(self):
        TILESIZE=32
        layouts = {
            'boundary': import_csv_layout('map_csv/scene1/fairy_floor_blocks_bare.csv'),
            'entities': import_csv_layout('map_csv/scene1/fairy_Entity_pos_0.csv')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'entities':
                            if col == '0':
                                if not(self.init[0] or self.init[1]):
                                    self.player = Player(
                                        (x,y),
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                                else:
                                    self.player = Player(
                                        self.init,
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                            elif col == '1575':
                               
                                Ally('fairy_princ',(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_princ'+str(x+y),'left',0)
                            elif col=='1617':
                                Ally('fairy_princ',(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_princ'+str(x+y),'left',1)
                            elif col == '1578':Ally('fairy_green',(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_green'+str(x+y),'left',0)
                            else:
                                
                                if col == '1':
                                    monster_name = 'ghost'
                                    self.enemy=Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player,self.number,'enemy',monster_name+str(x+y))
                                elif col == '4': 
                                    monster_name = 'dark_fairy'
                                    self.enemy=Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player,self.number,'enemy',monster_name+str(x+y))
                                elif col == '2': 
                                    monster_name ='bat'
                                    self.enemy=Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player,self.number,'enemy',monster_name+str(x+y))
                                
                                elif col == '5':
                                    monster_name = 'boss'
                                    self.boss_enemy=Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player,self.number,'enemy',monster_name+str(x+y))
                                    self.enemy_list.append(self.boss_enemy)
                                
                                if self.enemy  :
                                    self.enemy_list.append(self.enemy)#si le joueur active la huitieme gemme on selectionne les enmies proches
    def create_map4_scene1_2(self):
        TILESIZE=32
        layouts = {
            'boundary': import_csv_layout('map_csv/scene1/fairy_floor_blocks_bare.csv'),
            'entities': import_csv_layout('map_csv/scene1/fairy_Entity_pos_0.csv')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'entities':
                            if col == '0':
                                if not(self.init[0] or self.init[1]):
                                    self.player = Player(
                                        (x,y),
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                                else:
                                    self.player = Player(
                                        self.init,
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                            
                            elif col=='1617':
                                Ally('fairy_princ',(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_princ'+str(x+y),'left',2)
                            elif col == '1578':Ally('fairy_green',(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_green'+str(x+y),'left',0)
                            else:
                                
                                if col == '1':
                                    monster_name = 'ghost'
                                    self.enemy=Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player,self.number,'enemy',monster_name+str(x+y))
                                elif col == '4': 
                                    monster_name = 'dark_fairy'
                                    self.enemy=Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player,self.number,'enemy',monster_name+str(x+y))
                                elif col == '2': 
                                    monster_name ='bat'
                                    self.enemy=Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player,self.number,'enemy',monster_name+str(x+y))
                                
                                elif col == '5':
                                    monster_name = 'boss'
                                    self.boss_enemy=Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player,self.number,'enemy',monster_name+str(x+y))
                                    self.enemy_list.append(self.boss_enemy)
                                
                                if self.enemy  :
                                    self.enemy_list.append(self.enemy)#si le joueur active la huitieme gemme on selectionne les enmies proches
    def create_map4_scene2(self):
        TILESIZE=32
        layouts = {
            'boundary': import_csv_layout('map_csv/scene2/tree._floor_blocks.csv'),
            'entities': import_csv_layout('map_csv/scene2/tree._pos.csv')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'entities':
                            if col == '1536':
                                if not (self.init[0] or self.init[1]):
                                    self.player = Player(
                                        (x,y),
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                                else:
                                    self.player = Player(
                                        self.init,
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                            elif col == '1530':Ally('fairy_green',(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_green'+str(x+y),'down',0)
                            elif col == '1528':
                                self.special_ally=Ally('fairy_queen',(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally','fairy_queen'+str(x+y),'down',1)
                                
                            else:
                                #if col == '1': monster_name = 'ghost'
                                #elif col == '4': monster_name = 'dark_fairy'
                                if col == '1532': 
                                    if self.get_bat:
                                        monster_name ='bat'
                                    
                                        self.enemy=Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player,self.number,'enemy',monster_name+str(x+y))
                                    
                                        if self.enemy  :
                                            self.enemy_list.append(self.enemy)#si le joueur active la huitieme gemme on selectionne les enmies proches
    def create_map4_scene3(self):
        TILESIZE=32
        layouts = {
            'boundary': import_csv_layout('map_csv/scene3/chateaux_floor_blocks.csv'),
            'entities': import_csv_layout('map_csv/scene3/chateaux_perso.csv')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'entities':
                            if col == '1536':
                                if not(self.init[0] or self.init[1]):
                                    self.player = Player(
                                        (x,y),
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                                else:
                                    self.player = Player(
                                        self.init,
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                            else:
                                if col == '1534': 
                                    monster_name = 'knight2'
                                    self.enemy=Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player,self.number,'enemy',monster_name+str(x+y))
                                
                                    if self.enemy  :
                                        self.enemy_list.append(self.enemy)#si le joueur active la huitieme gemme on selectionne les enmies proches
                                
                                
    def create_map4_scene4(self):
        TILESIZE=32
        layouts = {
            'boundary': import_csv_layout('map_csv/scene4/etage1_floor_blocks.csv'),
            'entities': import_csv_layout('map_csv/scene4/etage1_pos.csv')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'entities':
                            if col == '1536':
                                if not(self.init[0] or self.init[1]):
                                    self.player = Player(
                                        (x,y),
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                                else:
                                    self.player = Player(
                                        self.init,
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                            else:
                                if col == '1530': 
                                    monster_name = 'knight3'
                                    self.enemy=Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player,self.number,'enemy',monster_name+str(x+y))
                                
                                    if self.enemy  :
                                        self.enemy_list.append(self.enemy)#si le joueur active la huitieme gemme on selectionne les enmies proches
                                
    def create_map4_scene5(self):
        TILESIZE=32
        layouts = {
            'boundary': import_csv_layout('map_csv/scene5/etage2_floor_blocks.csv'),
            'entities': import_csv_layout('map_csv/scene5/etage2_pos.csv')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'entities':
                            if col == '1536':
                                
                                if not(self.init[0] or self.init[1]):
                                    
                                    self.player = Player(
                                        (x,y),
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                                else:
                                    
                                    self.player = Player(
                                        self.init,
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                            else:
                                if col == '1530': 
                                    monster_name = 'gardien_eau'
                                    self.enemy=Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player,self.number,'enemy',monster_name+str(x+y))

                                if col == '1534': 
                                    monster_name = 'demon'
                                    self.enemy=Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player,self.number,'enemy',monster_name+str(x+y))
                            
                                if self.enemy  :
                                    self.enemy_list.append(self.enemy)#si le joueur active la huitieme gemme on selectionne les enmies proches
                        
    def create_map4_scene6(self):
        TILESIZE=32
        layouts = {
            'boundary': import_csv_layout('map_csv/scene6/roof_floor_blocks.csv'),
            'entities': import_csv_layout('map_csv/scene6/roof_pos.csv')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'entities':
                            if col == '1536':
                                if not(self.init[0] or self.init[1]):
                                    self.player = Player(
                                        (x,y),
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                                else:
                                    self.player = Player(
                                        self.init,
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                            else:
                                if col == '1532': monster_name = 'king'
                                elif col == '1530': monster_name = 'fille'
                                elif col == '1534': monster_name ='knight3'
                                
                                
                                Ally(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.number,'ally',monster_name+str(x+y),'idle_right',0)
    def create_map4_scene7(self):
        TILESIZE=32
        layouts = {
            'boundary': import_csv_layout('map_csv/scene7/sky_floorblocks.csv'),
            'entities': import_csv_layout('map_csv/scene7/sky_pos.csv')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'entities':
                            if col == '1536':
                                if not(self.init[0] or self.init[1]):
                                    self.player = Player(
                                        (x,y),
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                        self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                                else:
                                    self.player = Player(
                                        self.init,
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                        self.destroy_attack,
                                        self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
                            else:
                                if col == '1532': 
                                    monster_name = 'dragon1'
                                    self.final_enemy=Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player,self.number,'enemy',monster_name+str(x+y))
                                
                                    if self.final_enemy  :
                                        self.enemy_list.append(self.final_enemy)#si le joueur active la huitieme gemme on selectionne les enmies proches
                                
  

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])

    def create_magic(self,style,strength,cost):
        print(style)
        print(strength)
        print(cost)

    def destroy_attack(self):
        if self.current_attack != None:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        
        if self.attacker_sprites and self.player.attacking:
            
            for attack_sprite in self.attacker_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites :
                    
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player,self)
                        

    def eight_attack_logic(self):
        
        if self.attacker_sprites and 'attack' in self.enemy8th.status:#################################################################################
            
            for attack_sprite in self.attacker_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites :
                    
                    for target_sprite in collision_sprites:
                        if type(target_sprite).__name__=='Enemy':
                            target_sprite.get_damage_by_8th(self.enemy8th,self)

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable and not self.player.attacking:
            self.game.health-=amount
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.weapon_hit_sound.play()
            #spawn particles


    def collect_object(self):
        if self.level_objects:
            keys = pygame.key.get_pressed()
            collision = pygame.sprite.spritecollide(self.player,self.level_objects,False)
            for object in collision :
                if object.sprite_type == 'auto_collect' :
                    object.kill()
                elif object.sprite_type == 'press_to_collect' :
                    self.player_instructions()
                    if keys[pygame.K_r]:
                        object.kill()
                        self.player.inventory.append(object)


    def player_instructions(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Press R to collect", True, 'white')
        self.display_surface.blit(text, (WIDTH/2-100, 100))

    def boss_1(self):
        if self.boss_sprite :
            if self.player.rect.centerx >= 3960 and self.player.rect.centery <= 1698 :
                for rock in self.rock_sprites :
                    rock.animating = True
                    self.obstacle_sprites.add(rock)
        else :
            for rock in self.rock_sprites:
                rock.kill()



    def run(self,main,num):
		# update and draw the game
        if self.number == 5 :
            if self.ally :
                main.smth = not self.ally.can_talk
            else :
                print("erreur")
        if num:
            self.player.kill()
            self.player = Player(
                                    self.initial_point,
                                    [self.visible_sprites,self.attacker_sprites],
                                    self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,self.game.health,self.game.exp,self.game.level_bar)
            self.player.game_over=False
            self.game.health=100
            self.player.health=100
            self.player.game_over_screen=False
            self.player.status='right'
            #self.player.rect.topleft=self.initial_point
        if self.player.activate7:
            self.coef-=0.5
            alpha= ((0.6*self.wave_value2(1/1600,255,0,0))/153)*40+self.coef
            
            self.shield.image.set_alpha(alpha)
            self.shield.rect.centerx=self.player.rect.centerx-10
            self.shield.rect.centery=self.player.rect.centery
            self.shield.hitbox.centerx=self.player.rect.centerx-10
            self.shield.hitbox.centery=self.player.rect.centery
            
        if ((pygame.time.get_ticks()-self.shield_timer))>10000 and self.player.activate7:
            self.player.activate7=False
            self.shield.kill()
            self.coef=180

        

        self.visible_sprites.custom_draw(self.player)
        self.player.input(self)
        self.visible_sprites.update()
        self.visible_sprites.enemy_ally_update(self.player,self)
        main.sound2_zone=self.sound2_zone
        
        self.player_attack_logic()
        if self.player.activate8:
            self.eight_attack_logic()
        if self.number != 5 and self.number != 6 :
            self.ui.display(self.player)
        self.collect_object()
        if self.player.game_over_screen:
            main.game_active=False
    def wave_value2(self,f,a,boolean,phase):
        if boolean:
            return a*abs(sin(2*pi*f*pygame.time.get_ticks()+phase))
        else:
            return a*(sin(2*pi*f*pygame.time.get_ticks()+phase))

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, level_number, scene_number=1):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        #bat
        self.index_one_time=0
        self.index_one_time2=0
        # floor
        if level_number == 5 or level_number == 6 :
            image = pygame.image.load('Graphics\map.png')
            tr_image = pygame.transform.scale(image,(4000,4000))
            self.floor_surface = tr_image.convert()
        if level_number == 1:
            if scene_number == 1:
                image = pygame.image.load('real level/Level_1 map.png')
                tr_image = pygame.transform.scale(image,(10240,11264))
                self.floor_surface = tr_image.convert()
            if scene_number == 2:
                image = pygame.image.load('real level/gym1-1.png')
                tr_image = pygame.transform.scale(image,(768*4,521*4))
                self.floor_surface = tr_image.convert()
            if scene_number == 3:
                image = pygame.image.load('real level/mini_boss.png')
                tr_image = pygame.transform.scale(image,(2048*2,1536*2))
                self.floor_surface = tr_image.convert()
        if level_number == 2:
            self.floor_surface = pygame.image.load('Level 2\BIGMAP.png').convert()
        if level_number == 3:
            if scene_number == 1:
                self.floor_surface = pygame.image.load("Graphics\passage\map.png").convert()
            if scene_number == 2:
                image = pygame.image.load("Graphics/boss_map/map.png").convert() 
                tr_image = pygame.transform.scale(image,(480*3.75,480*3.75))
                self.floor_surface = tr_image.convert()   
        if level_number == 4:
            if scene_number == 1:
                self.floor_surface = pygame.image.load('maps/fairy.png').convert()
            if scene_number == 2:
                self.floor_surface = pygame.image.load('maps/tree1.png').convert()
            if scene_number == 3:
                self.floor_surface = pygame.image.load('maps/chateaux1.png').convert()
            if scene_number == 4:
                self.floor_surface = pygame.image.load('maps/etage11.png').convert()
            if scene_number == 5:
                self.floor_surface = pygame.image.load('maps/etage2.png').convert()
            if scene_number == 6:
                self.floor_surface = pygame.image.load('maps/roof.png').convert()
            if scene_number == 7:
                self.floor_surface = pygame.image.load('maps/sky.png').convert()
        

        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_ally_update(self, player,level):

        
        for enemy_inex in range(len(level.enemy_list)):# extraire les enemies les plus proche
            
            if level.enemy_list[enemy_inex].distance>0 and level.enemy_list[enemy_inex].distance<=1100 and level.enemy_list[enemy_inex] not in level.near_enemy_list and level.enemy_list[enemy_inex]!=level.current_enemy and level.enemy_list[enemy_inex] not in level.killed  :
                 
                 level.near_enemy_list.append(level.enemy_list[enemy_inex])
                 
                 
        enemy_inex=0
        Taille_near_enemy_list=len(level.near_enemy_list)
        while enemy_inex <Taille_near_enemy_list:#eliminer les ennemies qui sont devenu loin
            if level.near_enemy_list[enemy_inex].distance>1100  or level.near_enemy_list[enemy_inex].in_the_list(level.killed)  :
                 level.near_enemy_list.pop(enemy_inex)
                 Taille_near_enemy_list-=1
            else: 
                enemy_inex+=1
        #on trie maintenant ces enemies par ordre de proximité
        if len(level.near_enemy_list)>1:
            for i in range(len(level.near_enemy_list)):
                min=level.near_enemy_list[i].distance
                min_index=i
                for j in range(i,len(level.near_enemy_list)):
                    
                    if level.near_enemy_list[j].distance<min:
                        min=level.near_enemy_list[j].distance
                        min_index=j
                level.near_enemy_list[i],level.near_enemy_list[min_index]=level.near_enemy_list[min_index],level.near_enemy_list[i]
        if level.near_enemy_list and level.current_enemy!=None:
            if level.current_enemy.distance>level.near_enemy_list[0].distance:
                a=level.current_enemy
                level.current_enemy=level.near_enemy_list[0]
                level.near_enemy_list[0]=a
        enemy_sprites=[]
        ally_sprites=[]
        for sprite in self.sprites():
            if hasattr(sprite, 'sprite_type'):
                if (sprite.sprite_type == 'enemy'):
                    enemy_sprites.append(sprite)
                if (sprite.sprite_type == 'ally'):
                    ally_sprites.append(sprite)
        if  level.current_enemy==None:
                if level.near_enemy_list:
                    level.current_enemy=level.near_enemy_list.pop(0)
        
        if  level.current_enemy!=None and level.current_enemy.distance>1100: 
            level.current_enemy=None
        if level.near_enemy_list==[]and  level.enemy8th!=None and level.current_enemy==None:
            player.activate8=False
            level.enemy8th.kill()
        #if level.current_enemy!= None:
        if level.current_enemy!= None and level.current_enemy.dead :
                level.killed.append(level.current_enemy)
                level.current_enemy=None
        for enemy in enemy_sprites:  
            enemy.enemy_update(player)
            if enemy.monster_name=='boss' :
                print(enemy.distance,'963369')
                if enemy.health<200:
                    level.boss_enemy=enemy
                if enemy.distance<=3500:
                    level.sound2_zone=True
                elif enemy.distance>3500:
                    level.sound2_zone=False
        
        for ally in ally_sprites:
            ally.ally_update(player,self)
            if ally.ally_name=='fairy_queen' and level.scene!=2:
                level.end_screen=level.ally.end_screen
            if ally.lancez_bat:
                if self.index_one_time==0:
                    self.index_one_time+=1

                    monster_name ='bat'
                                    
                    level.special_enemy=Enemy(monster_name,(1300,2000),[level.visible_sprites,level.attackable_sprites],level.nothing,level.damage_player,level.number,'enemy',monster_name+str(1300+2000))
            
                    if level.enemy  :
                        level.enemy_list.append(level.special_enemy)#si le joueur active la huitieme gemme on selectionne les enmies proches
            if ally.lancez_dragon:
                level.passez_scene7=True
                

            
        
        if player.activate8:
            if player.activate8!=None and level.current_enemy!=None:
                level.enemy8th.enemy_update(level.current_enemy)
            if pygame.time.get_ticks()-level.shield_timer>=10000 and level.enemy8th and player.activate8:
                    player.activate8=False
                    level.enemy8th.kill()