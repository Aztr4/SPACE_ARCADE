import pygame, random

#DIMENSIONES
ANCHO= 800
ALTO=600

#PALETA DE COLORES
MORADO= (46,60,148)
ROJO= (125,33,0)
LILA= (92,110,224)
VERDE_1 = (134,224,70)
VERDE2 = (95,148,58)
BLANCO =(255,255,255)
NEGRO =(0,0,0)

#Inicialización
pygame.init()
pygame.mixer.init()
pantalla= pygame.display.set_mode((ANCHO,ALTO))
pygame.display.set_caption("Space Arcade")
icono=pygame.image.load("Sprites_secundarios/P_prueba.png")
icono.set_colorkey(BLANCO)
pygame.display.set_icon(icono)
reloj = pygame.time.Clock()

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Sprites/PERSONAJE ESCALADO.png"). convert()
        self.image.set_colorkey(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO //2
        self.rect.bottom = ALTO - 10
        self.vel_x = 0
        self.vel_y =0
        self.barra = 100
    
    def update(self):
        self.vel_x = 0
        self.vel_y = 0
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_LEFT]:
            self.vel_x = -5
        if tecla[pygame.K_RIGHT]:
            self.vel_x = 5
        if tecla[pygame.K_UP]:
            self.vel_y = -5
        if tecla[pygame.K_DOWN]:
            self.vel_y = 5
        
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
        if self.rect.top < 0:
            self.rect.top = 0
            
    def disparo(self):
        bullet= Bullet(self.rect.centerx, self.rect.top)
        sprites.add(bullet)
        bullets.add(bullet)
        sonido_laser.play()
        
        
class Meteoros(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO -  self.rect.width)
        self.rect.y = random.randrange (-100,-40)
        self.vel_y = random.randrange (1,10)
        self.vel_x = random.randrange (-5,5)
    
    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.top > ALTO +10 or self.rect.left < -25 or self.rect.right > ANCHO +22:
            self.rect.x = random.randrange(ANCHO -  self.rect.width)
            self.rect.y = random.randrange (-150,-100)
            self.vel_y = random.randrange (1,8)

class Estrellas(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Sprites/estrella.png").convert()
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x= random.randrange(ANCHO - self.rect.width)
        self.rect.y= random.randrange(ALTO - self.rect.height)
        self.vel_y = random.randrange (1,10)
        self.vel_x = random.randrange (-5,5)
        
    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.top > ALTO +10 or self.rect.left < -25 or self.rect.right > ANCHO +22:
            self.rect.x = random.randrange(ANCHO -  self.rect.width)
            self.rect.y = random.randrange (-150,-100)
            self.vel_y = random.randrange (1,8)



class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("Sprites/laser1.png")
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy= -10
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def dibujar_texto(superficie, texto, dimensiones,x, y):
    fuente = pygame.font.SysFont("Broadway", dimensiones)
    superficie_txt= fuente.render(texto, False, BLANCO)
    txt_rect= superficie_txt.get_rect()
    txt_rect.midtop = (x,y)
    superficie.blit (superficie_txt, txt_rect)

def barra_vida(superficie_bar,x,y, porcentaje):
    LARGO_bar= 100
    ALTO_bar = 10
    calculo_barra= (porcentaje/100)* LARGO_bar
    borde = pygame.Rect(x,y, LARGO_bar, ALTO_bar)
    calculo_barra= pygame.Rect(x,y, calculo_barra, ALTO_bar)
    pygame.draw.rect(superficie_bar, ROJO, calculo_barra)
    pygame.draw.rect(superficie_bar, BLANCO, borde, 2)

Inicio= pygame.image.load ("Sprites/inicio.png").convert()

def pantalla_game_over():
    pantalla.blit(Inicio, [0,0])
    #dibujar_texto(pantalla, "SPACE ARCADE", 80, ANCHO//2, ALTO//4)
    #dibujar_texto(pantalla, "", 27, ANCHO //2, ALTO//2)
    #dibujar_texto(pantalla, "Presiona espacio para empezar", 20, ANCHO//2, ALTO * 3/4)
    pygame.display.flip()
    wait = True
    while wait:
        reloj.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    wait= False


         


meteor_images = []
meteor_list = ["Sprites/meteor_g1.png", "Sprites/meteor_g2.png", "Sprites/meteor_g3.png", "Sprites/meteor_g4.png",
				"Sprites/meteor_med1.png", "Sprites/meteor_med2.png", "Sprites/meteor_p1.png", "Sprites/meteor_p2.png",
				"Sprites/meteor_p3.png", "Sprites/meteor_p4.png"]
for img in meteor_list:
	meteor_images.append(pygame.image.load(img).convert())
    
    
##-------------EXPLOSION IMG-----------
explosion_anim= []
for a in range(9):
    file = "Sprites/regularExplosion0{}.png".format(a)
    img = pygame.image.load(file).convert()
    img.set_colorkey(NEGRO)
    img_scale = pygame.transform.scale(img, (70,70))
    explosion_anim.append(img_scale)

#Fondo
fondo = pygame.image.load ("Sprites/fondo.png").convert()

#Musica
sonido_laser= pygame.mixer.Sound("sonidos/laser5.ogg")
explosion_sound= pygame.mixer.Sound("sonidos/explosion.wav")
sonido_estrella= pygame.mixer.Sound("sonidos/sonido_plus.ogg")
pygame.mixer.music.load("sonidos/intergalactic_odyssey.ogg")
#pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=-1)

#Sprites-Sistema de Sonido

subir_sonido = pygame.image.load('sonidos/mas_volumen.png').convert()
subir_sonido.set_colorkey(NEGRO)
pygame.transform.scale(subir_sonido, (20,20))

bajar_sonido = pygame.image.load('sonidos/menos_volumen.png').convert()
bajar_sonido.set_colorkey(NEGRO)
pygame.transform.scale(bajar_sonido, (20,20))

sonido_mute = pygame.image.load('sonidos/mute_volumen.png').convert()
sonido_mute.set_colorkey(NEGRO)
pygame.transform.scale(sonido_mute, (20,20))

sonido_max = pygame.image.load('sonidos/max_volumen.png').convert()
sonido_max.set_colorkey(NEGRO)
pygame.transform.scale(sonido_max, (20,20))


#-----BUCLE-------------
game_over = True
ejecutar = True
while ejecutar:
    
    if game_over:
        
        pantalla_game_over()
        game_over = False
        
        #Grupos
        sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        estrella = pygame.sprite.Group()

    #instanciación
        jugador = Jugador()
        sprites.add(jugador)

        for i in range (10):
            meteor= Meteoros()
            sprites.add(meteor)
            meteor_list.add(meteor)
        
        for i in range(1):
            stars = Estrellas()
            sprites.add(stars)
            estrella.add(stars)
            
        score = 0
        
    reloj.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutar = False
    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jugador.disparo()
    
    sprites.update()
    
    #Colisiones Meteoro-Bala
    colision = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for i in colision:
        score += 10
        explosion_sound.play()
        explosion = Explosion(i.rect.center)
        sprites.add(explosion)
        meteor= Meteoros()
        sprites.add(meteor)
        meteor_list.add(meteor)
    
    #Colisiones meteoro-jugador
    colision = pygame.sprite.spritecollide(jugador, meteor_list, True)
    for n in colision:
        jugador.barra -=20
        meteor= Meteoros()
        sprites.add(meteor)
        meteor_list.add(meteor)
        if jugador.barra <=0:
            game_over = True
    
    
    #Colisiones estrella-jugador
    colision = pygame.sprite.spritecollide(jugador, estrella, True)
    for n in colision:
        score += 5
        if jugador.barra >=100:
            jugador.barra +=0
        else:
            jugador.barra +=15
        sonido_estrella.play()
        stars= Estrellas()
        sprites.add(stars)
        estrella.add(stars)
        
        
    pantalla.blit(fondo, (0,0))
    
    #CONTROL DE AUDIO
    
    tecla_s = pygame.key.get_pressed()
    #Baja volumen
    if tecla_s[pygame.K_KP_MINUS] and pygame.mixer.music.get_volume() > 0.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)
        pantalla.blit(bajar_sonido, (650, 20))
    elif tecla_s[pygame.K_KP_MINUS] and pygame.mixer.music.get_volume() == 0.0:
        pantalla.blit(sonido_mute, (650, 20))

    #Sube volumen
    if tecla_s[pygame.K_KP_PLUS] and pygame.mixer.music.get_volume() < 1.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.01)
        pantalla.blit(subir_sonido, (650, 20))
    elif tecla_s [pygame.K_KP_PLUS] and pygame.mixer.music.get_volume() == 1.0:
            pantalla.blit(sonido_max, (650, 20))

    #Desactivar sonido
    elif tecla_s[pygame.K_KP0]:
        pygame.mixer.music.set_volume(0.0)
        pantalla.blit(sonido_mute, (650, 20))

    #Reactivar sonido
    elif tecla_s[pygame.K_KP9]:
        pygame.mixer.music.set_volume(1.0)
        pantalla.blit(sonido_max, (650, 20))
    
    
    
    ###############################IMPRIMIR
    
    
    sprites.draw(pantalla)
    dibujar_texto(pantalla, str(score), 25, ANCHO//2, 10)
    barra_vida(pantalla, 5, 5, jugador.barra)  
    
    pygame.display.update()

    
    pygame.display.flip()
    
pygame.quit()
    
    
        
        
        



