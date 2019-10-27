import pygame
from constants import *
import random
from math import sqrt
from pygame import mixer

############
#INIT SETUP#
############

#INIT
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))

#WINDOW CAPTION AND ICON
pygame.display.set_caption('Images/Space Invaders')
ufo_icon=pygame.image.load('Images/ufo.png')
pygame.display.set_icon(ufo_icon)

#BACKGROUND
space_background=pygame.image.load('Images/space_background.jpg')

#MUSIC
mixer.music.load('Images/background.mp3')
mixer.music.play(-1)

#PLAYER
spaceship_icon=pygame.image.load('Images/spaceship.png')
def player(x,y):
	screen.blit(spaceship_icon,(x,y))

#ALIEN
red_alien_icon=[]
red_alien_x=[]
red_alien_y=[]
red_alien_x_change=[]
red_alien_y_change=[]
num_of_enemies=6
red_alien_icon1=pygame.image.load('Images/red_alien.ico')
for i in range(0,num_of_enemies):
	red_alien_icon.append(pygame.image.load('Images/red_alien.ico'))
	red_alien_x.append(random.randint(0,800-red_alien_icon1.get_size()[0]))
	red_alien_y.append(random.randint(0+red_alien_icon1.get_size()[1],150))
	red_alien_x_change.append(2)
	red_alien_y_change.append(32)

def red_alien(x,y):
	screen.blit(red_alien_icon[i],(x,y))

#BULLET
bullet_icon=pygame.image.load('Images/bullet.png')
def fire_bullet(x,y):
	global bullet_state
	bullet_state="fire"
	screen.blit(bullet_icon,(x+16,y+10))

#CHECK COLLISION
def check_collision(red_alien_x,red_alien_y,bullet_x,bullet_y):
	dist=sqrt((red_alien_x-bullet_x)**2+(red_alien_y-bullet_y)**2)
	if dist<27:
		return True	
	return False

#SCORE
score=0
font = pygame.font.Font('freesansbold.ttf',32)
def show_score(x,y):
	score_val=font.render("score: "+str(score),True,WHITE)
	screen.blit(score_val,(x,y))

def game_over(score_val):
	end_game=font.render("GAME OVER",True,RED)
	end_game2=font.render("Your Final Score is: "+ str(score_val),True,RED)
	screen.blit(end_game,(270,250))
	screen.blit(end_game2,(200,280))


################
#MAIN GAME LOOP#
################

running = True
game_end=False
while running:
	for event in pygame.event.get():

		#TERMINATE WINDOW
		if event.type == pygame.QUIT:
			running = False

		#CHECKING KEYSTROKES
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				player_x_change = -2.5
			if event.key == pygame.K_RIGHT:
				player_x_change = 2.5
			if event.key == pygame.K_UP:
				player_y_change = -2.5
			if event.key == pygame.K_DOWN:
				player_y_change = 2.5

			if event.key == pygame.K_SPACE:
				if bullet_state is "ready":
					#bullet_sound=mixer.Sound('Images/laser_shot.wav')
					#bullet_sound.play()
					bullet_x=player_x
					bullet_y=player_y
					fire_bullet(player_x,bullet_y)
					

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				player_x_change=0
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
			 	player_y_change=0


	#GAME WINDOW MANIPULATION
	screen.fill(BLACK)
	
	#Background Image
	screen.blit(space_background,(0,0))
	
	##############
	####PLAYER####
	##############

	#Player Positions
	player_x+=player_x_change
	player_y+=player_y_change
	#PLAYER BOUNDARIES
	if player_x<0:
		player_x=0
	elif player_x>=(screen_width-spaceship_icon.get_size()[0]):
		player_x=(screen_width-spaceship_icon.get_size()[0])
	if player_y<0:
		player_y=0
	elif player_y>=(screen_height-spaceship_icon.get_size()[1]):
		player_y=(screen_height-spaceship_icon.get_size()[1])
	
	#############
	####ALIEN####
	#############

	for i in range(0,num_of_enemies):
		#ENEMY POSITIONS
		red_alien_x[i]+=red_alien_x_change[i]
		#ENEMY BOUNDARIES
		if red_alien_x[i]<0:
			red_alien_x_change[i]=2
			red_alien_y[i]+=red_alien_y_change[i]
		elif red_alien_x[i]>=(screen_width-red_alien_icon1.get_size()[0]):
			red_alien_x_change[i]=-2
			red_alien_y[i]+=red_alien_y_change[i]

		#################
		####COLLISION####
		#################

		#CHECK COLLISIONS
		collision = check_collision(red_alien_x[i],red_alien_y[i],bullet_x,bullet_y)
		if collision:
			explosion_sound=mixer.Sound('Images/explosion.wav')
			explosion_sound.play()
			bullet_y=player_y
			bullet_state="ready"
			score+=1
			#print(score)
			red_alien_x[i]=random.randint(0,800-red_alien_icon1.get_size()[0])
			red_alien_y[i]=random.randint(0+red_alien_icon1.get_size()[1],150)

		red_alien(red_alien_x[i],red_alien_y[i])

		#################
		####GAME OVER####
		#################
		player_collision = check_collision(red_alien_x[i],red_alien_y[i],player_x,player_y)
		
		for j in range(0,len(red_alien_x_change)):
			if player_collision or red_alien_y[j]>=800:
				red_alien_x_change[j]=0
				red_alien_y_change[j]=0
				bullet_x_change=0
				bullet_y_change=0
				player_x_change=0
				player_y_change=0
				bullet_state="ready"
				game_end=True
				game_over_sound=mixer.Sound('Images/game_over.wav')
				game_over_sound.play()
	if game_end==True:
		game_over(score)
		


	##############
	####BULLET####
	##############

	#BULLET MOVEMENT
	if bullet_state is "fire":
		fire_bullet(bullet_x,bullet_y)
		bullet_y-=bullet_y_change

	if bullet_y<=-32:
		bullet_y=player_y
		bullet_state="ready"

	
	player(player_x,player_y)
	show_score(text_x,text_y)

	pygame.display.update()
