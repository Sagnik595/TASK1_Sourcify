import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

sw = 564
sh = 636

screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption('Flappy Bird')
f = pygame.font.SysFont('Comic Sans MS', 50)
white = (255, 255, 255)

gs = 0
ss = 4
flying = False
game_over = False
pg = 150
pf = 1500
lp = pygame.time.get_ticks() - pf
sc = 0
pp = False

bg = pygame.image.load('bg.png')
ground_img = pygame.image.load('ground.png')
button_img = pygame.image.load('restart.png')


def dt(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


def reset_game():
	pg.empty()
	flappy.rect.x = 100
	flappy.rect.y = int(sh / 2)
	sc = 0
	return sc


class Bird(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		for num in range(1, 4):
			img = pygame.image.load(f'bird{num}.png')
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.vel = 0
		self.clicked = False

	def update(self):

		if flying == True:
			self.vel += 0.5
			if self.vel > 8:
				self.vel = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.vel)

		if game_over == False:
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				self.vel = -10
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False
			self.counter += 1
			fc = 5
			if self.counter > fc:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
			self.image = self.images[self.index]
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
		else:
			self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('pipe.png')
		self.rect = self.image.get_rect()
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(pg / 2)]
		if position == -1:
			self.rect.topleft = [x, y + int(pg / 2)]

	def update(self):
		self.rect.x -= ss
		if self.rect.right < 0:
			self.kill()


class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True
		screen.blit(self.image, (self.rect.x, self.rect.y))
		return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(sh / 2))

bird_group.add(flappy)

button = Button(sw // 2 - 50, sh // 2 - 100, button_img)

run = True
while run:
	clock.tick(fps)

	screen.blit(bg, (0,0))

	bird_group.draw(screen)
	bird_group.update()
	pipe_group.draw(screen)

	screen.blit(ground_img, (gs, 550))

	if len(pipe_group) > 0:
		if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
			and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
			and pp == False:
			pp = True
		if pp == True:
			if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
				sc += 1
				pp = False

	dt(str(sc), f, white, int(sw / 2), 20)

	if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
		game_over = True

	if flappy.rect.bottom >= 768:
		game_over = True
		flying = False

	if game_over == False and flying == True:
		time_now = pygame.time.get_ticks()
		if time_now - lp > pf:
			ph = random.randint(-100, 100)
			btm_pipe = Pipe(sw, int(sh / 2) + ph, -1)
			top_pipe = Pipe(sw, int(sh / 2) + ph, 1)
			pipe_group.add(btm_pipe)
			pipe_group.add(top_pipe)
			lp = time_now
		gs -= ss
		if abs(gs) > 35:
			gs = 0
		pipe_group.update()

	if game_over == True:
		if button.draw() == True:
			game_over = False
			sc = reset_game()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
			flying = True

	pygame.display.update()

pygame.quit()
