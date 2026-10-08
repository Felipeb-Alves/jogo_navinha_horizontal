import random
import sys
import pygame

# Inicialização do Pygame
pygame.init()
pygame.font.init()

# Configurações da Tela (Paisagem/Horizontal)
LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Navinha - Com Obstáculos Maiores")

# Cores
BRANCO = (255, 255, 255)
PRETO = (10, 10, 30)
AZUL = (0, 150, 255)
VERMELHO = (255, 60, 60)
AMARELO = (255, 255, 0)
VERDE = (50, 205, 50)
CINZA = (120, 120, 130)
CINZA_ESCURO = (70, 70, 80)

# Relógio para controle de FPS
relogio = pygame.time.Clock()
FPS = 60

# Fonte de texto
FONTE = pygame.font.SysFont("arial", 22)
FONTE_FIM = pygame.font.SysFont("arial", 48, bold=True)


class Jogador(pygame.sprite.Sprite):

  def __init__(self):
    super().__init__()
    self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.polygon(self.image, AZUL, [(0, 0), (40, 20), (0, 40)])
    pygame.draw.polygon(self.image, AMARELO, [(10, 10), (30, 20), (10, 30)])

    self.rect = self.image.get_rect()
    self.rect.left = 50
    self.rect.centery = ALTURA // 2
    self.velocidade = 6
    self.vidas = 3

  def update(self):
    teclas = pygame.key.get_pressed()
    if (
        teclas[pygame.K_LEFT] or teclas[pygame.K_a]
    ) and self.rect.left > 0:
      self.rect.x -= self.velocidade
    if (
        teclas[pygame.K_RIGHT] or teclas[pygame.K_d]
    ) and self.rect.right < LARGURA:
      self.rect.x += self.velocidade
    if (
        teclas[pygame.K_UP] or teclas[pygame.K_w]
    ) and self.rect.top > 0:
      self.rect.y -= self.velocidade
    if (
        teclas[pygame.K_DOWN] or teclas[pygame.K_s]
    ) and self.rect.bottom < ALTURA:
      self.rect.y += self.velocidade


class Tiro(pygame.sprite.Sprite):

  def __init__(self, x, y):
    super().__init__()
    self.image = pygame.Surface((14, 6))
    self.image.fill(AMARELO)
    self.rect = self.image.get_rect()
    self.rect.left = x
    self.rect.centery = y
    self.velocidade = 10

  def update(self):
    self.rect.x += self.velocidade
    if self.rect.left > LARGURA:
      self.kill()


class Inimigo(pygame.sprite.Sprite):

  def __init__(self, velocidade_extra=0):
    super().__init__()
    self.image = pygame.Surface((35, 35), pygame.SRCALPHA)
    pygame.draw.rect(self.image, VERMELHO, (5, 5, 25, 20), border_radius=4)
    pygame.draw.rect(self.image, BRANCO, (10, 8, 6, 6))
    pygame.draw.rect(self.image, BRANCO, (10, 21, 6, 6))

    self.rect = self.image.get_rect()
    self.rect.x = random.randint(LARGURA + 20, LARGURA + 100)
    self.rect.y = random.randint(0, ALTURA - self.rect.height)
    self.velocidade = random.randint(3, 5) + velocidade_extra

  def update(self):
    self.rect.x -= self.velocidade
    if self.rect.right < 0:
      self.kill()


class Obstaculo(pygame.sprite.Sprite):
  """Obstáculo maior apenas para desviar (tiros passam direto)"""

  def __init__(self):
    super().__init__()
    # Tamanho aumentado para 45 de largura e 100 de altura
    self.image = pygame.Surface((45, 100), pygame.SRCALPHA)
    pygame.draw.rect(self.image, CINZA, (0, 0, 45, 100), border_radius=8)
    pygame.draw.rect(
        self.image, CINZA_ESCURO, (5, 5, 35, 90), border_radius=6
    )

    self.rect = self.image.get_rect()
    self.rect.x = random.randint(LARGURA + 20, LARGURA + 150)
    self.rect.y = random.randint(0, ALTURA - self.rect.height)
    self.velocidade = random.randint(4, 6)

  def update(self):
    self.rect.x -= self.velocidade
    if self.rect.right < 0:
      self.kill()


# Grupos de Sprites
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()
tiros = pygame.sprite.Group()

# Instanciando o Jogador
jogador = Jogador()
todos_sprites.add(jogador)

# Variáveis do Jogo e Placares
pontos = 0
recorde = 0
rodando = True
game_over = False

# Eventos customizados para criar inimigos e obstáculos
ADICIONAR_INIMIGO = pygame.USEREVENT + 1
ADICIONAR_OBSTACULO = pygame.USEREVENT + 2

pygame.time.set_timer(ADICIONAR_INIMIGO, 1500)
pygame.time.set_timer(ADICIONAR_OBSTACULO, 2500)  # Intervalo ajustado para o tamanho maior

# Loop Principal do Jogo
while rodando:
  relogio.tick(FPS)

  for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
      rodando = False

    elif evento.type == pygame.KEYDOWN:
      if evento.key == pygame.K_SPACE and not game_over:
        tiro = Tiro(jogador.rect.right, jogador.rect.centery)
        todos_sprites.add(tiro)
        tiros.add(tiro)
      elif evento.key == pygame.K_r and game_over:
        # Reiniciar o jogo
        game_over = False
        pontos = 0
        jogador.vidas = 3
        jogador.rect.left = 50
        jogador.rect.centery = ALTURA // 2
        # Limpar todos os elementos da tela
        for i in inimigos:
          i.kill()
        for o in obstaculos:
          o.kill()
        for t in tiros:
          t.kill()
        pygame.time.set_timer(ADICIONAR_INIMIGO, 1500)
        pygame.time.set_timer(ADICIONAR_OBSTACULO, 2500)

    elif evento.type == ADICIONAR_INIMIGO and not game_over:
      novo_intervalo = max(400, 1500 - (pontos * 10))
      pygame.time.set_timer(ADICIONAR_INIMIGO, int(novo_intervalo))

      bonus_vel = pontos // 50
      inimigo = Inimigo(velocidade_extra=bonus_vel)
      todos_sprites.add(inimigo)
      inimigos.add(inimigo)

    elif evento.type == ADICIONAR_OBSTACULO and not game_over:
      obstaculo = Obstaculo()
      todos_sprites.add(obstaculo)
      obstaculos.add(obstaculo)

  if not game_over:
    todos_sprites.update()

    # Colisão 1: Tiros vs Inimigos (Destrói o inimigo e o tiro)
    colisoes_tiro_inimigo = pygame.sprite.groupcollide(
        tiros, inimigos, True, True
    )
    for colisao in colisoes_tiro_inimigo:
      pontos += 10

    # Colisão 2: Inimigos vs Jogador
    colisoes_jogador_inimigo = pygame.sprite.spritecollide(
        jogador, inimigos, True
    )
    if colisoes_jogador_inimigo:
      jogador.vidas -= 1

    # Colisão 3: Obstáculos vs Jogador
    colisoes_jogador_obstaculo = pygame.sprite.spritecollide(
        jogador, obstaculos, True
    )
    if colisoes_jogador_obstaculo:
      jogador.vidas -= 1

    # Checa Game Over
    if jogador.vidas <= 0:
      game_over = True
      pygame.time.set_timer(ADICIONAR_INIMIGO, 0)
      pygame.time.set_timer(ADICIONAR_OBSTACULO, 0)
      if pontos > recorde:
        recorde = pontos

  # Renderização
  TELA.fill(PRETO)
  todos_sprites.draw(TELA)

  # Textos do HUD
  texto_pontos = FONTE.render(f"Pontos: {pontos}", True, BRANCO)
  texto_recorde = FONTE.render(f"Recorde: {recorde}", True, AMARELO)
  texto_vidas = FONTE.render(f"Vidas: {jogador.vidas}", True, VERDE)

  TELA.blit(texto_pontos, (15, 15))
  TELA.blit(texto_recorde, (15, 45))
  TELA.blit(texto_vidas, (15, 75))

  if game_over:
    superficie_fim = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    superficie_fim.fill((0, 0, 0, 180))
    TELA.blit(superficie_fim, (0, 0))

    msg_game_over = FONTE_FIM.render("FIM DE JOGO", True, VERMELHO)
    msg_pontos_finais = FONTE.render(
        f"Sua Pontuação: {pontos}", True, BRANCO
    )
    msg_recorde_tela = FONTE.render(
        f"Maior Pontuação: {recorde}", True, AMARELO
    )
    msg_reiniciar = FONTE.render(
        "Pressione 'R' para Reiniciar ou ESC para sair", True, BRANCO
    )

    TELA.blit(
        msg_game_over,
        (LARGURA // 2 - msg_game_over.get_width() // 2, ALTURA // 2 - 90),
    )
    TELA.blit(
        msg_pontos_finais,
        (
            LARGURA // 2 - msg_pontos_finais.get_width() // 2,
            ALTURA // 2 - 30,
        ),
    )
    TELA.blit(
        msg_recorde_tela,
        (LARGURA // 2 - msg_recorde_tela.get_width() // 2, ALTURA // 2 + 10),
    )
    TELA.blit(
        msg_reiniciar,
        (LARGURA // 2 - msg_reiniciar.get_width() // 2, ALTURA // 2 + 70),
    )

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_ESCAPE]:
      rodando = False

  pygame.display.flip()

pygame.quit()
sys.exit()