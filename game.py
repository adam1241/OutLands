import pygame
import sys

from level import Level
from settings import *
from debug import debug
from math import *
#import pygame.movie

#kiilimi

class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Outlands')

        #sounds
        self.main_sound = pygame.mixer.Sound('audio/main.ogg')
        self.main_sound2 = pygame.mixer.Sound('audio/akaza.mp3')
        self.main_sound3 = pygame.mixer.Sound('audio/intro.mp3')
        self.main_sound4 = pygame.mixer.Sound('audio/finalboss.mp3')
        self.main_sound.set_volume(0.5)
        self.main_sound2.set_volume(0.5)
        self.main_sound3.set_volume(0.5)
        self.main_sound4.set_volume(0.5)

        #zone d acces
        self.sound2_zone=False
        self.sound2_activated=False

        #variables d activation/ variable important
        self.main_sound.play(loops = -1)
        self.clock = pygame.time.Clock()
        self.game_active=True

        #generation images de GAME OVER ET ecran d attente
        self.player_stand = pygame.image.load('player/gameover_right_6.png').convert_alpha()
        self.player_stand_rect = self.player_stand.get_rect(center = (WIDTH/2,HEIGHT*5/8))
        self.test_font = pygame.font.Font('font/Pixeltype.ttf', 250)
        self.game_name = self.test_font.render('GAME OVER',False,(0, 9, 94))

        self.game_name_rect = self.game_name.get_rect(center = (WIDTH/2,HEIGHT*2/8))

        self.test_font_message = pygame.font.Font('font/Pixeltype.ttf', 150)
        self.game_message = self.test_font_message.render('You Looser',False,(0, 9, 94))
        self.game_message_rect = self.game_message.get_rect(center = (WIDTH/2,HEIGHT*4/8))

        self.test_font_message_0 = pygame.font.Font('font/Pixeltype.ttf', 250)
        self.game_message_0 = self.test_font_message_0.render('press enter to restart',False,(148, 201, 255))
        self.game_message_rect_0 = self.game_message_0.get_rect(center = (WIDTH/2,HEIGHT*7/8))

        #waiting screen
        self.test_font_message_0 = pygame.font.Font('font/Pixeltype.ttf', 150)
        self.game_message_0 = self.test_font_message_0.render('waiting the player to get trough',False,(0, 9, 94))
        self.game_message_rect_0 = self.game_message_0.get_rect(center = (WIDTH/2,HEIGHT*7/8))

        self.player_wait = pygame.image.load('wait.png').convert_alpha()
        self.player_wait_rect = self.player_stand.get_rect(center = (WIDTH/2,HEIGHT*1/2))

        #health
        self.health=100
        self.exp=0
        self.level_bar=1
        self.start_game=False
        self.screen_intro_index=0
        self.pas=False
        self.alpha1=0

        self.smth = None

        self.number_gameover=0
        self.intro=1
        self.ending=False
        self.ending_index=0
        self.passto_scene5=0

        self.level = Level(self,5,(0,0),1)


    def run(self):
        one_time=False
        one_time2=False
        one_time3=False
        one_time4=False
        while True:
            if pygame.time.get_ticks()-self.level.timer>=10000 :
                self.level.player.speed=20
                self.level.timer=0
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()
            if keys[pygame.K_l]:
                pygame.quit()
                sys.exit()
            if not self.start_game:
                self.screen.fill('black')
                if self.intro :
                    alpha=self.wave_value(1/10000,255,1,-pi*3/16)
                    print(alpha)
                    if alpha<=5:
                        one_time=True
                    if keys[pygame.K_RETURN]:
                        self.screen_intro_index=3
                        test_font= pygame.font.Font('font/Pixeltype.ttf', 50)
                    if self.screen_intro_index==0 and one_time:
                        
                        imt_stand = pygame.image.load('intro/imt.png').convert_alpha()
                        imt_stand.set_alpha(alpha)
                        imt_stand_rect = imt_stand.get_rect(center = (WIDTH/2,HEIGHT/2))
                        self.screen.blit(imt_stand,imt_stand_rect)
                        if alpha>=60:
                            one_time2=True
                        print(alpha,one_time2)
                        if alpha<=15 and one_time2:
                            self.screen_intro_index+=1
                    if self.screen_intro_index==1 :
                        
                        test_font= pygame.font.Font('font/Pixeltype.ttf', 50)
                        if alpha>=60:
                            self.pas =True
                        created =test_font.render('Created  by  :',False,'white')
                        created_rect= created.get_rect(center = (WIDTH/2,HEIGHT/2-200))
                        
                        std_0 = test_font.render('Adam  LAGSSAIBI',False,'white')
                        std_0_rect= std_0.get_rect(center = (WIDTH/2,HEIGHT/2-100))
                        
                        std_1 = test_font.render('Mohammed  El  Mehdi  Alaoui',False,'white')
                        std_1_rect= std_0.get_rect(center = (WIDTH/2,HEIGHT/2))
                        
                        std_2 = test_font.render('Amine  AIT  BENMESSAOUD',False,'white')
                        std_2_rect= std_0.get_rect(center = (WIDTH/2,HEIGHT/2+100))
                        
                        std_3 = test_font.render('Damien  BONNETON',False,'white')
                        std_3_rect= std_0.get_rect(center = (WIDTH/2,HEIGHT/2+200))
                        created.set_alpha(alpha)
                        std_0.set_alpha(alpha)
                        std_1.set_alpha(alpha)
                        std_2.set_alpha(alpha)
                        std_3.set_alpha(alpha)
                        self.screen.blit(created,created_rect)
                        self.screen.blit(std_0,std_0_rect)
                        self.screen.blit(std_1,std_1_rect)
                        self.screen.blit(std_2,std_2_rect)
                        self.screen.blit(std_3,std_3_rect)
                        if alpha>=60:
                            one_time3=True
                        if self.pas and alpha<=20 and one_time3:
                            self.screen_intro_index+=1
                            self.pas=False
                    if self.screen_intro_index==2 :
                        
                        test_font= pygame.font.Font('font/Pixeltype.ttf', 50)
                        if alpha>=50:
                            self.pas =True
                        created =test_font.render('Directed  by  :',False,'white')
                        created_rect= created.get_rect(center = (WIDTH/2,HEIGHT/2-200))
                        
                        std_0 = test_font.render('Gregory  SMITS',False,'white')
                        std_0_rect= std_0.get_rect(center = (WIDTH/2,HEIGHT/2-100))
                        created.set_alpha(alpha)
                        std_0.set_alpha(alpha)
                        self.screen.blit(created,created_rect)
                        self.screen.blit(std_0,std_0_rect)
                        if alpha>=60:
                            one_time4=True

                        if self.pas and alpha<=15 and one_time4:
                            self.screen_intro_index+=1
                            self.pas=False
                    if self.screen_intro_index==3 :
                        print(alpha)
                        if alpha>=254 or self.alpha1==255:
                            self.alpha1=255
                        print(alpha,'*')
                        imt_stand = pygame.image.load('intro/logo.png').convert_alpha()
                        if alpha>=254 or self.alpha1==255:imt_stand.set_alpha(self.alpha1)
                        else:imt_stand.set_alpha(alpha)
                        
                        imt_stand_rect = imt_stand.get_rect(center = (WIDTH/2,HEIGHT/2))
                        self.screen.blit(imt_stand,imt_stand_rect)
                        std_3 = test_font.render('Cliquez sur  ENTREZ  pour  commencer',False,'white')
                        std_3.set_alpha(self.wave_value(1/1000,255,1,-pi*3/16))
                        std_3_rect= std_3.get_rect(center = (WIDTH/2,HEIGHT/2+300))
                        self.screen.blit(std_3,std_3_rect)
                        if keys[pygame.K_RETURN] :
                            self.start_game=True
                            self.intro=False
                        
                    
                    pygame.display.update()
                    self.clock.tick(FPS)
                if self.ending:
                    self.screen.fill('black')
                    test_font= pygame.font.Font('font/Pixeltype.ttf', 150)
                    created =test_font.render("Merci d'avoir joue",False,'white')
                    created_rect= created.get_rect(center = (WIDTH/2,HEIGHT/2))
                    
                    alpha=self.wave_value(1/10000,255,1,-pi*3/16)
                    created.set_alpha(alpha)
                    self.screen.blit(created,created_rect)
                    print(self.ending_index,'4')
                    if  keys[pygame.K_RETURN] :
                        self.ending_index+=1
                    if self.ending_index>=10:
                        self.main_sound3.stop()
                        
                        self.level=Level(self,1,(0,0),1)
                        self.main_sound.play(loops = -1)
                        
                        self.start_game=True
                    pygame.display.update()
                    self.clock.tick(FPS)
            if self.game_active:
                if self.start_game:

               

                    self.screen.fill('black')

                    self.level.run(self,self.number_gameover)
                    #changement de maps
                    self.playerx = self.level.player.rect.centerx
                    self.playery = self.level.player.rect.centery
                    print(self.playerx ,self.playery )
                    if self.level.number == 5 :
                        self.main_sound.stop()
                        self.main_sound3.play(loops = -1)
                        if self.smth :
                            self.main_sound3.stop()
                            self.main_sound.play(loops = -1)
                            self.level = Level(self,1,(0,0),1)
                    if self.level.number == 1 and self.level.scene == 1 :
                        if self.playerx >= 5276 and self.playerx <= 5590 and self.playery == 7803 :
                            self.level = Level(self,1,(0,0),2)
                    if self.level.number == 1 and self.level.scene == 2 :
                        if self.playerx >= 1100 and self.playerx <= 1200 and self.playery >= 120 and self.playery <= 140 :
                            self.level = Level(self,1,(0,0),3)
                    if self.level.number == 1 and self.level.scene == 3 :

                            if not self.level.attackable_sprites :
                                if self.playerx >= 2100 and self.playerx <= 2256 and self.playery <= 374 :
                                    self.level = Level(self,2,(0,0),1)
                    if self.level.number == 2:
                        print(7)
                    if (self.playerx >= 3500 and self.playerx <= 4500) and (self.playery >= 4450 and self.playery <= 4700):
                            self.level = Level(self,3,(0,0))
                    if (self.playery<=12 and self.level.scene ==1  and self.level.number==3):
                        self.level = Level(self,3,(0,0),2)
                    elif (self.playery<=25 and self.level.scene ==2  and self.level.number==3):
                        self.level = Level(self,4,(0,0),1)
                    if (self.playerx>=2610 and self.playerx<=2748 ) and self.level.scene == 1 and self.level.number==4:
                        if self.playery >= 5500 and self.playery <= 5550 :
                            self.level = Level(self,4,(0,0),2)
                            self.playerx = 1336
                            self.playery = 2954
                    if self.level.scene == 2 and self.level.number==4:
                        if   self.playery >= 3100 :
                            self.screen.fill((69,174,116))
                            self.screen.blit(self.game_message_0,self.game_message_rect_0)
                            self.screen.blit(self.player_wait,self.player_wait_rect)
                            self.playery+=60
                        if self.playery >=3200:
                            self.level = Level(self,4,(2690,5650),1,1)
                    if (self.playerx>=22600 and self.playerx<=22808 ) and self.level.scene == 1 and self.level.number==4:
                        if self.level.boss_enemy.health<=0:
                            if self.playery >= 4900 and self.playery <= 5190 :
                                self.level = Level(self,4,(0,0),3)
                                self.playerx = 1624
                                self.playery = 2046
                    if (self.playerx>=2100 and self.playerx<=2200 ) and self.level.scene == 3 and self.level.number==4:
                        if  self.playery <= 1450 :
                            self.level = Level(self,4,(0,0),4)
                            self.playerx = 1016
                            self.playery = 1438
                    if (self.playerx>=1900 and self.playerx<=2200 ) and self.level.scene == 4 and self.level.number==4:
                        if  self.playery >= 3110 :
                            self.level = Level(self,4,(2150,1510),3)
                    if (self.playerx>=1900 and self.playerx<=2200 ) and self.level.scene == 4 and self.level.number==4:
                        if  self.playery <= 1780 :
                            self.level = Level(self,4,(0,0),5)
                    if (self.playerx>=1900 and self.playerx<=2200 ) and self.level.scene == 5 and self.level.number==4:
                        if  self.playery >= 3050 :
                            self.level = Level(self,4,(2000,1840),4)
                    if (self.playerx>=1900 and self.playerx<=2200 ) and self.level.scene == 5 and self.level.number==4:
                        if  self.playery <= 1760 :
                            self.level = Level(self,4,(0,0),6)
                    if (self.playerx>=2800 and self.playerx<=2990 ) and self.level.scene == 6 and self.level.number==4:
                        if  self.playery >= 4190 :
                            self.level = Level(self,4,(2000,1840),5)
                    if self.level.scene == 6 and self.level.number==4:
                        if  self.level.passez_scene7:
                            self.main_sound.stop()
                            self.main_sound4.play(loops = -1)
                            self.level = Level(self,4,(0,0),7)
                            
                    if self.level.scene == 7 and self.level.number==4:
                        if self.level.final_enemy.health<=0:
                                self.main_sound4.stop()
                                self.main_sound3.play(loops = -1)
                                self.level = Level(self,6,(0,0),1)
                    #if (self.playerx>=1500 and self.playerx<=1700 ) and self.level.scene == 7 and self.level.number==4:
                    #    if  self.playery >= 2070 :
                    #        self.level = Level(self,4,(2820,1450),6)
                    print(self.level.end_screen,'8')
                    if self.level.end_screen:
                        self.start_game=False
                        self.ending=True
                        
                    if self.number_gameover:
                        self.number_gameover=0
                    print(self.sound2_zone,'78954')
                    if self.sound2_zone:
                        self.sound2_activated=True
                        self.main_sound.stop()
                        self.main_sound2.play(loops = -1)
                    else:
                        if self.sound2_activated:
                            self.sound2_activated=False
                            self.main_sound2.stop()
                            self.main_sound.play(loops = -1)
                    pygame.display.update()
                    self.clock.tick(FPS)
            else:
                if keys[pygame.K_RETURN] :
                    self.game_active=True
                self.screen.fill((69,174,116))
                self.screen.blit(self.player_stand,self.player_stand_rect)
                self.screen.blit(self.game_name,self.game_name_rect)
                self.screen.blit(self.game_message,self.game_message_rect)
                if not keys[pygame.K_RETURN] :
                    alpha = self.wave_value(1/800,255,1,0)

                    self.game_message_0.set_alpha(alpha)
                    self.screen.blit(self.game_message_0,self.game_message_rect_0)
                    self.game_name_rect = self.game_name.get_rect(center = (WIDTH/2+self.wave_value(1/1600,255,0,0),HEIGHT*2/8))
                    self.game_message_rect = self.game_message.get_rect(center = (WIDTH/2+self.wave_value(1/2000,100,0,0),HEIGHT*4/8+self.wave_value(1/2000,100,0,pi/2)))
                self.number_gameover=1
                pygame.display.update()
                self.clock.tick(FPS)


    def wave_value(self,f,a,boolean,phase):
        if boolean:
            return a*abs(sin(2*pi*f*pygame.time.get_ticks()+phase))
        else:
            return a*(sin(2*pi*f*pygame.time.get_ticks()+phase))


game = Game()
game.run()
