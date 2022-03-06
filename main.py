import pygame #install pip
from pygame.locals import *
from sys import exit
from cores import *
import android

sprite_sheet = pygame.image.load('sprites/shipsall.gif') # https://opengameart.org/content/spaceships-1

class Nave(pygame.sprite.Sprite):
	def __init__(self, enemy=False, super=False):
		pygame.sprite.Sprite.__init__(self)
		if not enemy:
			self.image = sprite_sheet.subsurface((64,128),(64,64))
		else:
			self.image = sprite_sheet.subsurface((128,128),(64,64))
			self.image = pygame.transform.flip(self.image, 0, 1)
		self.image = pygame.transform.scale(self.image, (largura_tela//10, largura_tela//10))
		self.rect = self.image.get_rect()
		if not enemy:
			self.rect.midbottom = (largura_tela//2, altura_tela//20*15)
		else:
			self.rect.midbottom = (largura_tela//2, altura_tela//20*2)
		self.enemy = enemy
		self._life = 100 if not super else 500
	
	
	def mover(self, m_vel):
		self.rect.left += m_vel
		if self.enemy:
			self.rect.top += ((altura_tela/20)/fps)
		
	
	def atirar(self):
		snd_shoot.play()
		return Projétil(self.rect.midtop[0], self.rect.midtop[1], self.enemy) if not self.enemy else Projétil(self.rect.midbottom[0], self.rect.midbottom[1], self.enemy)
	
	
	def vida(self, dano=0):
		if dano > 0:
			snd_hit.play()
		elif dano < 0:
			pass
		self._life -= dano
		return self._life


class Projétil(pygame.sprite.Sprite):
	def __init__(self, left, top, enemy=False, especial=False):
		pygame.sprite.Sprite.__init__(self)
		self.image = sprite_sheet.subsurface((128,64),(32,64))
		self.image = pygame.transform.scale(self.image, (16,32))
		if enemy:
			self.image = pygame.transform.flip(self.image,0,1)
		self.rect = self.image.get_rect()
		self._vel = 15 if enemy else -15
		self.dano = 100 if especial else 25
		self.enemy = enemy
		self.rect.left = left
		self.rect.top = top
		
	
	def mover(self):
		self.rect.top += self._vel
		
class Coracao(pygame.sprite.Sprite):
	def __init__(self, tam_heal=25):
		pygame.sprite.Sprite.__init__(self)
		self.image = sprite_sheet.subsurface((0,128),(64,64))
		self.image = pygame.transform.flip(self.image,0,1)
		self.image = pygame.transform.scale(self.image,(64,32))
		self.rect = self.image.get_rect()
		self._vel = 5
		self.dano = tam_heal
		self.rect.left = largura_tela//2
		self.rect.top = 0
		self.enemy = True


	def mover(self):
		self.rect.top += self._vel
		


def controle():
	return pygame.draw.polygon(tela,BRANCO, ((largura_tela//10*2, altura_tela//20*15), (largura_tela//10*8, altura_tela//20*15),(largura_tela//10*9, altura_tela//20*16),(largura_tela//10*8, altura_tela//20*17),(largura_tela//10*2, altura_tela//20*17),(largura_tela//10, altura_tela//20*16)))


def fim_de_jogo():
	global pontuação
	global ni
	global nj
	global msg_ponto
	snd_game_over.play()
	nj.kill()
	while True:
		tela.fill(PRETO)
		ni.rect.top += ((altura_tela/5)/fps)
		todas_sprites.draw(tela)
		pygame.display.flip()
		if ni.rect.top > altura_tela:
			break
		tela.fill(PRETO)
	fim = True
	msg_fim = FONTE.render('FIM DE JOGO', True, VERMELHO)
	msg_fim_rect = tela.blit(msg_fim,((largura_tela//2)-(msg_fim.get_width()//2), altura_tela//2))
	tela.blit(msg_ponto, ((largura_tela//2)-(msg_ponto.get_width()//2), (altura_tela//2) + msg_fim.get_height()))
	pygame.display.flip()
	while fim:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
			if event.type == KEYDOWN:
				if event.key == K_r:
					fim = False
			if event.type == MOUSEBUTTONDOWN:
				if msg_fim_rect.collidepoint(event.pos):
					fim = False
	todos_tiros.empty()
	todas_sprites.empty()
	pontuação = 0
	nj = Nave()
	ni = Nave(enemy=True)
	todas_sprites.add(nj, ni)
	snd_game_over.stop()


pygame.init()#INICIALIZA O MODULO
relogio = pygame.time.Clock()

#Ajustes da tela
tela = pygame.display.set_mode()
largura_tela = tela.get_width()
altura_tela = tela.get_height()
print(f'Largura (X): {largura_tela}')
print(f'Altura (Y): {altura_tela}')
fps = 60

#HUD
FONTE_PADRAO = pygame.font.get_default_font()
FONTE = pygame.font.SysFont(FONTE_PADRAO, largura_tela//10)
FONTEp = pygame.font.SysFont(FONTE_PADRAO, largura_tela//20)

###AUDIO### - https://themushroomkingdom.net/media/smw/wav
snd_shoot = pygame.mixer.Sound('sounds/shoot.wav') #smw_lava_bubble.wav
snd_hit = pygame.mixer.Sound('sounds/hit.wav') #smw_shell_ricochet.wav
snd_dies = pygame.mixer.Sound('sounds/nave_dies.wav') #smw_swooper_no_echo.wav
snd_game_over = pygame.mixer.Sound('sounds/game_over.wav')
snd_life = pygame.mixer.Sound('sounds/life_catch.mp3')
snd_new_life = pygame.mixer.Sound('sounds/life.wav')

todas_sprites = pygame.sprite.Group()
todos_tiros = pygame.sprite.Group()
nj = Nave()
ni = Nave(enemy=True)
todas_sprites.add(nj, ni)

novo_coracao = None
pontuação = 0
contador = 0
vel = 10
vel_i = vel * 0.8

while True:
	msg_ponto = FONTEp.render(f'Score: {pontuação}', True, AZUL)
	msg_vida_jogador = FONTEp.render(f'Player Life: {nj.vida()}', True,VERDE)
	msg_vida_inimigo = FONTEp.render(f'Enemy Life: {ni.vida()}', True, OURO)
	msg_vida_em_inimigo = FONTEp.render(str(ni.vida()),True,VERMELHO)
	
	
	relogio.tick(fps)
	tela.fill(PRETO)
	l1 = tela.blit(msg_ponto,(0, 0))
	l2 = tela.blit(msg_vida_inimigo,(0, l1.bottom))
	tela.blit(msg_vida_jogador,(0, l2.bottom))
	tela.blit(msg_vida_em_inimigo,(largura_tela//2, ni.rect.top-FONTEp.get_height()))

	controle()
	nj.mover(vel)
	ni.mover(vel_i)
	
	if nj.rect.right == largura_tela:
		vel = -vel
	elif nj.rect.right > largura_tela:
		nj.rect.right = largura_tela-1
		vel = -vel
	elif nj.rect.left == 0:
		vel = -vel
	elif nj.rect.left < 0:
		nj.rect.left = 1
		vel = -vel
		
	if ni.rect.right == largura_tela:
		vel_i = -vel_i
	elif ni.rect.right > largura_tela:
		ni.rect.right = largura_tela-1
		vel_i = -vel_i
	elif ni.rect.left == 0:
		vel_i = -vel_i
	elif ni.rect.left < 0:
		ni.rect.left = 1
		vel_i = -vel_i
	
	
	#eventos de interação (controles)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				vel = -vel #mudar direcao
				todos_tiros.add(nj.atirar())
		if event.type == MOUSEBUTTONDOWN:
			if controle().collidepoint(event.pos):
				vel = -vel
				todos_tiros.add(nj.atirar())

	for tiro in todos_tiros:
		if tiro.rect.bottom < 0 or tiro.rect.top > altura_tela//20*17:
			todos_tiros.remove(tiro)
		elif not tiro.enemy and tiro.rect.colliderect(ni.rect):
			snd_hit.play()
			todos_tiros.remove(tiro)
			ni.vida(tiro.dano)
			if ni.vida() <= 0:
				todas_sprites.remove(ni)
				pontuação += 1
				ni = Nave(enemy=True)
				ni.vida(-tiro.dano*pontuação)
				todas_sprites.add(ni)
		elif tiro.enemy and tiro.rect.colliderect(nj.rect):
			snd_hit.play()
			todos_tiros.remove(tiro)
			nj.vida(tiro.dano)
			if nj.vida() <= 0:
				fim_de_jogo()
		else:
			tiro.mover()
	contador += 1
	if contador == fps:
		contador = 0
		todos_tiros.add(ni.atirar())
	
	if pontuação > 0 and pontuação%3 == 0 and novo_coracao is None:
		snd_new_life.play()
		novo_coracao = Coracao(25)
	if novo_coracao is not None:
		todos_tiros.add(novo_coracao)
		if novo_coracao.rect.colliderect(nj.rect):
			nj.vida(-novo_coracao.dano)
			snd_life.play()
			novo_coracao.kill()
			novo_coracao = None
		elif novo_coracao.rect.bottom > altura_tela//20*17:
			novo_coracao.kill()
			novo_coracao = None
			
	if ni.rect.bottom > nj.rect.top or nj.vida() <= 0:
		fim_de_jogo()
	
	todas_sprites.draw(tela)
	todos_tiros.draw(tela)
	pygame.display.flip()
