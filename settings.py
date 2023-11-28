FPS = 60
import pygame 
pygame.init()
from math import *
# game setup
info = pygame.display.Info()
WIDTH    = info.current_w
HEIGHT   = info.current_h
TILESIZE = 32

weapon_data = {
    'gem_blue' : {'cooldown':100,'damage':15,'graphic':'gems/gem_blue'},
    'gem_blue2' : {'cooldown':250,'damage':30,'graphic':'gems/gem_blue2'},
    'gem_green2' : {'cooldown':250,'damage':30,'graphic':'gems/gem_green2'},
    'gem_pink' : {'cooldown':100,'damage':15,'graphic':'gems/gem_pink'},
    'gem_red' : {'cooldown':100,'damage':15,'graphic':'gems/gem_red'},
    'gem_redorange' : {'cooldown':250,'damage':30,'graphic':'gems/gem_redorange'},
    'gem_green' : {'cooldown':100,'damage':15,'graphic':'gems/gem_green'},
    'gem_purpel' : {'cooldown':250,'damage':30,'graphic':'gems/gem_purpel'},
    'gem_orange' : {'cooldown':100,'damage':15,'graphic':'gems/gem_orange'},
    
}

lvl1_obj = {
    'coin' : {'type':'auto_collect', 'graphic':'Graphics/coin.jpg' },
    'weapon' : {'type':'weapon','graphic':'NinjaAdventure/Items/Weapons/Lance2/Sprite.png'}

}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'public-pixel-font/PublicPixel-z84yD.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# magic
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'Graphics/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'Graphics/heal/heal.png'}}

# enemy
monster_data = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'audio/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360,'animation_speed':0.8,'near_distance':200},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'audio/slash.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400,'animation_speed':0.8,'near_distance':200},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'audio/slash.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350,'animation_speed':0.8,'near_distance':200},
	'squeleton': {'health': 100,'exp':120,'damage':10,'attack_type': 'slash', 'attack_sound':'audio/slash.wav', 'speed': 2, 'resistance': 3, 'attack_radius': 30, 'notice_radius': 240,'animation_speed':0.8,'near_distance':60},
	'flying_rock': {'health': 150,'exp':0,'damage':0,'attack_type': 'none', 'attack_sound':'audio/slash.wav', 'speed': 0, 'resistance': 3, 'attack_radius': 0, 'notice_radius' : 0,'animation_speed':0.8,'near_distance':200},
	'Tower': {'health': 150,'exp':0,'damage':0,'attack_type': 'none', 'attack_sound':'audio/slash.wav', 'speed': 0, 'resistance': 3, 'attack_radius': 0, 'notice_radius' : 0,'animation_speed':0.8,'near_distance':200},
	'dragon': {'health' : 300 , 'exp': 100, 'damage': 10, 'attack_type': 'firebreath', 'attack_sound': 'audio/slash.wav','speed': 0.05, 'resistance': 3, 'attack_radius': 180, 'notice_radius': 500,'animation_speed':0.8,'near_distance':200},
	'ghost': {'health': 100,'exp':1,'damage':15,'attack_type': 'slash', 'attack_sound':'audio/slash.wav',
                           'speed': 11, 'resistance':100 , 'attack_radius': 25, 'notice_radius': 600,'animation_speed':0.7,'near_distance':30},
    'dark_fairy': {'health': 30,'exp':0,'damage':2,'attack_type': 'claw',  'attack_sound':'audio/slash.wav',
                            'speed': 6, 'resistance': 30, 'attack_radius': 10, 'notice_radius': 250,'animation_speed':0.2,'near_distance':60},
    'bat': {'health': 120,'exp':2,'damage':20,'attack_type': 'thunder', 'attack_sound':'audio/slash.wav',
                            'speed': 9, 'resistance': 3, 'attack_radius': 90, 'notice_radius': 1000,'animation_speed':0.8,'near_distance':200},
    'boss': {'health': 300,'exp':10,'damage':30,'attack_type': 'leaf_attack', 'attack_sound':'audio/slash.wav', 
                           'speed': 12, 'resistance': 60, 'attack_radius': 140,'notice_radius': 1000,'animation_speed':0.5,'near_distance':80},
    'phontom' : {'health': 300,'exp':10,'damage':30,'attack_type': 'leaf_attack', 'attack_sound':'audio/slash.wav', 
                           'speed': 12, 'resistance': 60, 'attack_radius': 140,'notice_radius': 1000,'animation_speed':0.5,'near_distance':80},
    'boss_ally': {'health': 300,'exp':10,'damage':300,'attack_type': 'leaf_attack', 'attack_sound':'audio/slash.wav', 
                           'speed': 12, 'resistance': 60, 'attack_radius': 140,'notice_radius': 100000,'animation_speed':0.5,'near_distance':80},
    'lv1_boss' : {'health': 300,'exp':10,'damage':30,'attack_type': 'leaf_attack', 'attack_sound':'audio/slash.wav', 
                           'speed': 12, 'resistance': 60, 'attack_radius': 140,'notice_radius': 1000,'animation_speed':0.5,'near_distance':80},
    'dragon1' : {'health': 700,'exp':10,'damage':30,'attack_type': 'leaf_attack', 'attack_sound':'audio/slash.wav', 
                           'speed': 5, 'resistance': 60, 'attack_radius': 140,'notice_radius': 1000,'animation_speed':0.2,'near_distance':80},
    'demon' : {'health': 300,'exp':10,'damage':30,'attack_type': 'leaf_attack', 'attack_sound':'audio/slash.wav', 
                           'speed':5, 'resistance': 60, 'attack_radius': 140,'notice_radius': 1000,'animation_speed':0.2,'near_distance':80},
    'gardien_eau' : {'health': 300,'exp':10,'damage':30,'attack_type': 'leaf_attack', 'attack_sound':'audio/slash.wav', 
                           'speed':5, 'resistance': 60, 'attack_radius': 140,'notice_radius': 1000,'animation_speed':0.2,'near_distance':80},
    'knight2' : {'health': 70,'exp':10,'damage':30,'attack_type': 'leaf_attack', 'attack_sound':'audio/slash.wav', 
                           'speed': 7, 'resistance': 60, 'attack_radius': 140,'notice_radius': 1000,'animation_speed':0.2,'near_distance':80},
    'knight3' : {'health': 90,'exp':10,'damage':30,'attack_type': 'leaf_attack', 'attack_sound':'audio/slash.wav', 
                           'speed': 7, 'resistance': 60, 'attack_radius': 140,'notice_radius': 1000,'animation_speed':0.2,'near_distance':80},
    'squelance' : {'health': 50,'exp':10,'damage':10,'attack_type': 'leaf_attack', 'attack_sound':'audio/slash.wav', 
                           'speed': 7, 'resistance': 30, 'attack_radius': 70,'notice_radius': 100,'animation_speed':0.1,'near_distance':80},

}
ally_data={
    'fairy_green':{'health': 9000,'damage':30, 'attack_sound':'../audio/attack/slash.wav', 
                           'speed': 7, 'animation_speed':0.2,'text':[],'resistance':30
            },
    'fairy_princ':{'health': 9000,'damage':30, 'attack_sound':'../audio/attack/slash.wav', 
                           'speed': 7, 'animation_speed':0.2,'text':[],'resistance':30
            },
    'fairy_queen':{'health': 9000,'damage':30, 'attack_sound':'../audio/attack/slash.wav', 
                           'speed': 7, 'animation_speed':0.2,'resistance':30},
    'fairy_queen':{'health': 9000,'damage':30, 'attack_sound':'../audio/attack/slash.wav', 
                           'speed': 7, 'animation_speed':0.2,'resistance':30
                           },
    'king':{'health': 9000,'damage':30, 'attack_sound':'../audio/attack/slash.wav', 
    'speed': 7, 'animation_speed':0.2,'resistance':30},
    'fille':{'health': 9000,'damage':30, 'attack_sound':'../audio/attack/slash.wav', 
                           'speed': 7, 'animation_speed':0.2,'resistance':30},
    'knight3':{'health': 9000,'damage':30, 'attack_sound':'../audio/attack/slash.wav', 
                           'speed': 7, 'animation_speed':0.2,'resistance':30}


}
#dialogue est structuree comme ca: {'ally_name':{numero_dialogue:[[ligne_0_page_0,ligne_1_page_0],[ligne_0_page_1,ligne_1_page_1],[surface_declanchement_discution],position de l'allier pendant ce dialogie n numero_dialogue]}}
dialogue={
    'fairy_princ':{0:[['Salut! ,  t  a  l  air  un  peu  fort,  je ',
                      ' m  appel  Lizaje  suis  une  fee,  je  suis ',
                      ' perdu,  j  ai  peur  que les  fantoms  m  attaquent.'],
                      ['Peut  tu  m  aider  .  Oh!  genial,  je me  ',
                      'rapelle que  prenait toujours  le nord  au  debut,'],
                      [
                      'peut tu te  deriger  vers  le sud,je  vais  te  suivre'],
                      [(1900,2000),(1400,1700)],(1984, 1504)],
                    1:[['oh  ! quand j ai vu l arbre je me suis presse ',
                      'de courrir, desole .Voici l arbre des fees. Est ce',
                      ' que je peut te demander une faveur On a un grand ',
                      'problem: notre jardin est attaque par des monstres ',
                      'et nous les fees sont trops faible pour combattre.'],
                      [
                      'ils ont prit le control de presque plus la moitie du jardin',
                      'je viens de parler a maman, et je lui est dit que t etait fort',
                      'Elle veut discuter avec toi, elle t attend a l interieur.'
                      'for  you  !!!!'],
                      [(2000,3600),(5700,6000)],(2665, 6015)],
                    2:[['j ai parle avec maman, elle a dit:',
                        'T  a  l  air  tres fort  en  effet...',
                      'peut  tu  sauver  notre  jardin  en  battant  le',
                      'monstre ultime  du  cristal  et  en  redescandant',
                      'le chateau. en  echange  je  te  donne  cette  ',
                      'gemme,  elle  generera un  bouclier pour te proteger',
                        'des  monstres,  utilise ',
                      ],
                      ['la  bien. Encore une chose, il y a des fees qui ont',
                       'ete touche par le virus qui se propage, ne leur',
                       'fait pas de mal s il te plait, il sont de bonnes',
                       'personnes, utilise le bouclier pour te proteger.'],
                       ['...  BONNE CHANCE.'],
                      
                      [(2400,2900),(5700,6000)],(1344, 1792)]},
    'fairy_queen':{0:[["L'histoire se deroule dans une majestueuse capitale",
                        "d'un vaste empire, ou un destin extraordinaire atte-",
                        "nd notre jeune heros. Depuis la recente disparition ",
                        "de l'empereur, son fils aine a herite du trone. Nous ",
                        "suivons les pas d'un courageux petit garcon vivant "
                        ],
                        [
                        "avec sa soeur et leur mere, dans une modeste demeure",
                        "qui abrite egalement un bar en peripherie de la ville."
                        ],
                        ["Un jour, un mysterieux carrosse s'arrete devant la",
                        "porte du restaurant.A son bord, un individu a l'allure",
                        "noble et fortunee penetre a l'interieur pour engager ",
                        "une conversation confidentielle avec la mere et la " ,
                        "fille. Apres son depart, il est revele que le nouvel",
                        ],
                        [
                        "empereur souhaite epouser la jeune fille, les pressant",
                        "d'accepter cette proposition. Toutefois, mefiante,",
                        "la fille choisit de rester proche des siens."
                        ],
                        ["Le lendemain, l'empereur en personne se presente",
                        "avec ses puissants gardes pour emmener de force ",
                        "la jeune fille, ne lui laissant aucun repit pour",
                        "reflechir. Malgre les efforts desesperes du petit",
                        "garcon pour l'arreter, il se retrouve impuissant"
                        ],
                        [
                        "face a la puissance des gardes imperiaux. Avant de",
                        "partir, l'empereur lance d'une voix sinistre : ",
                        "Si tu veux que ta famille reste en vie, epouse-moi",
                        "sans poser de question. Un desastre s'abat sur la maison."
                        ],
                        ["Le lendemain, il est annonce que le mariage aura", 
                        "lieu dans une ville lointaine. Le jeune garcon ",
                        "entame son periple vers cette destination, apres",
                        "avoir fait ses adieux emouvants a sa mere. "
                        ],
                        ["Preparez-vous a une quete epique remplie de ",
                        "dangers, de mysteres et de revelations surprenantes !"],
                        [(0,20000),(0,20000)],(2110, 1700)],
                    1:[['oh!  regarder qui voila!!  je  t  attendais...  Merci Beaucoup ',
                      'd avoir  sauver  ma  fille  adore ,  je suis  la  reine  de ce ',
                      'jardin.  Notre  jardin  a  ete  envahit  par des  monstres  a ',
                      'cause  du  roi.  Au  centre  du  jardin  se trouvait  un ',
                      'chateau dans lequel  etait enfoui un cristal sacre, le roi  '],
                      [
                      'etaitvenu  pour  lever  le chateau  dans  le ciel pour   ',
                      'avoir  leplus beau  des  marriages,  on  l  a  empeche ',
                      'de  faire cela. '],
                      ['car  cela  rendra  le cristal  instable,  mais il  n a pas  ',
                      'ecoute,  maintenant  le  cristal  produit  des  monstres ',
                      'des tenebres  qui  envahissent tout  le jardin. Nous  on  est ',
                      'faible,  on ne  peut rien  y  faire ,  c  est  pourquoi  ',
                      'nous avonsbesoin  de quelqu un de  fort. Voyons  si  tu '],
                      ['es pret  a  affronter  les monstres. Soit  pret  on va  ',
                      'lacher  un monctre  que  nous  avons  capture...'],
                      [(1200,1500),(1900,2240)],(2665, 6015)],
                    2:[['T  a  l  air  tres fort  en  effet...',
                      'peut  tu  sauver  notre  jardin  en  battant  le  monstre  ',
                      'ultime  du  cristal  et  en  redescandant  le chateau. ',
                      'en  echange  je  te  donne  cette  gemme,  elle  generera',
                      'un  bouclier pour te proteger  des  monstres,  utilise ',
                      ],
                      ['la  bien. Encore une chose, il y a des fees qui ont',
                       'ete touche par le virus qui se propage, ne leur',
                       'fait pas de mal s il te plait, il sont de bonnes',
                       'personnes, utilise le bouclier pour te proteger.'],
                       ['...  BONNE CHANCE.'],
                      
                      [(1200,1500),(1900,2240)],(1344, 1792)],
                      #(2110,1876)
                    3:[['Apres avoir remporte la bataille contre le dragon,',
                      'le jeune garcon recupera la derniere gemme que ce',
                      'dernier portait. Cette gemme etait precieuse, la',
                      'derniere de son espece. Cependant, sa joie fut de',
                      'courte duree lorsque sa soeur, blessee lors du combat,'],
                      [
                      'succomba a ses blessures. Accable de tristesse et de',
                      'melancolie, le garcon contemplait les neuf gemmes qui',
                      'brillaient devant lui, disposees de maniere ',
                      'mysterieuse. Soudain, elles emirent une lueur',
                      'eclatante et accorderent un voeu au jeune heros.'],
                      ['Le coeur brise, le garcon formula le souhait de',
                      'ramener sa soeur a la vie. A sa grande surprise,',
                      'sa soeur s eveilla et ils furent submerges de bonheur.'
                      ],
                      ['La derniere gemme, celle qui avait le pouvoir de',
                      'deplacer les objets, restaura le chateau dans',
                      'le jardin et stabilisa le cristal.  Ensemble,',
                      'le garcon et sa soeur  rentrerent chez eux. Ils',
                      'retrouverent une vie paisible et heureuse a cote'],
                      ['de leur mere, cherissant chaque instant passe',
                      'ensemble. Les gemmes devinrent des souvenirs',
                      'precieux de leur incroyable aventure.'],
                      ['Ainsi, ils vecurent heureux jusqu a la fin de',
                      'leurs jours, portant en eux les lecons',
                      'apprises et la force puisee dans leur',
                      'lien familial.'],
                      [(0,20000),(0,20000)],(2665, 6015)]},
                      

                    #
                    #   
                    # 
                    #  
                    #  
                    #   
                    # 
                    #  

                    #
                    #  
                    #  
                    #  lien familial.
    'fairy_green':{0:[[],[]]},
    'king':       {0:[['GRRR... tu m a suivit jusqu ici pour saboter',
                       'mon magnifique marriage, tu va gouter a ma colere',
                       'affronte donc mon dragon.'], [(2700,2990),(1400,1800)],(2665, 6015)]},
    'knight3':{0:[[],[]]},
    'fille':{0:[[],[]]}

}


