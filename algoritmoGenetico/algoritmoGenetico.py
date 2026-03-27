import pygame
import random

pygame.init()

# Pantalla
ANCHO, ALTO = 800, 400
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Algoritmo Genético competencia")

# Sprite (2x2)
hoja_sprites = pygame.image.load("player.png")
ANCHO_FRAME = hoja_sprites.get_width() // 2
ALTO_FRAME = hoja_sprites.get_height() // 2

frames = []
for fila in range(2):
    for col in range(2):
        frame = hoja_sprites.subsurface(
            (col * ANCHO_FRAME, fila * ALTO_FRAME, ANCHO_FRAME, ALTO_FRAME)
        )
        frame = pygame.transform.scale(frame, (30, 30))
        frames.append(frame)

# Colores
NEGRO = (0,0,0)
ROJO = (255,0,0)
VERDE = (0,255,0)

# Parámetros
TAM_POBLACION = 10
GENERACIONES = 10
TASA_MUTACION = 0.3
CANT_OBSTACULOS = 4
SUELO = ALTO - 50
FPS = 30

# Obstáculos
def crear_obstaculos():
    return [
        pygame.Rect(
            random.randint(250, ANCHO-50),
            SUELO - random.randint(20, 40),
            20,
            random.randint(20, 40)
        )
        for _ in range(CANT_OBSTACULOS)
    ]

# Genes
def crear_individuo():
    return {
        'velocidad': random.randint(2,6),
        'salto': random.randint(10,20),
        'distancia_salto': random.randint(20,80)
    }

def mutar(criatura):
    if random.random() < TASA_MUTACION:
        criatura['velocidad'] = max(1, min(10, criatura['velocidad'] + random.choice([-1,1])))
        criatura['salto'] = max(5, min(30, criatura['salto'] + random.choice([-1,1])))
        criatura['distancia_salto'] = max(10, min(100, criatura['distancia_salto'] + random.choice([-5,5])))
    return criatura

def cruce(padre1, padre2):
    return {
        'velocidad': random.choice([padre1['velocidad'], padre2['velocidad']]),
        'salto': random.choice([padre1['salto'], padre2['salto']]),
        'distancia_salto': random.choice([padre1['distancia_salto'], padre2['distancia_salto']])
    }

# Aptitud 
def aptitud(criatura, obstaculos):
    pos_x, pos_y = 50, SUELO
    vel_y = 0
    max_x = pos_x

    for _ in range(ANCHO):
        pos_x += criatura['velocidad']
        max_x = max(max_x, pos_x)

        # Salto 
        if pos_y == SUELO:
            for obs in obstaculos:
                if 0 < obs.x - pos_x < criatura['distancia_salto']:
                    vel_y = -criatura['salto']

        pos_y += vel_y
        vel_y += 1

        if pos_y > SUELO:
            pos_y = SUELO
            vel_y = 0

        # Choque usando el Rect del sprite
        criatura_rect = pygame.Rect(pos_x, pos_y-30, 30, 30)
        for obs in obstaculos:
            if criatura_rect.colliderect(obs):
                return max_x

        if pos_x > ANCHO:
            return max_x

    return max_x

# Inicializar población
poblacion = [crear_individuo() for _ in range(TAM_POBLACION)]
reloj = pygame.time.Clock()

for gen in range(GENERACIONES):

    obstaculos = crear_obstaculos()

    puntajes = [aptitud(c, obstaculos) for c in poblacion]
    indice_mejor = puntajes.index(max(puntajes))
    mejor = poblacion[indice_mejor]

    print(f"""
        Generación: {gen+1}
        Distancia: {puntajes[indice_mejor]}
        Velocidad: {mejor['velocidad']}
        Salto: {mejor['salto']}
        Distancia salto: {mejor['distancia_salto']}
    """)

    pos_x = [50]*TAM_POBLACION
    pos_y = [SUELO]*TAM_POBLACION
    vel_y = [0]*TAM_POBLACION
    choco = [False]*TAM_POBLACION

    indice_frame = [0]*TAM_POBLACION
    temporizador_frame = 0

    corriendo = True
    contador_frames = 0

    while corriendo and contador_frames < 200:
        reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Animación de frames
        temporizador_frame += 1
        if temporizador_frame % 5 == 0:
            for i in range(TAM_POBLACION):
                indice_frame[i] = (indice_frame[i] + 1) % 4

        # Fondo y suelo
        ventana.fill((135, 206, 235))
        pygame.draw.rect(ventana, NEGRO, (0, SUELO, ANCHO, ALTO-SUELO))

        # Dibujar obstáculos
        for obs in obstaculos:
            pygame.draw.rect(ventana, ROJO, obs)

        # Dibujar criaturas
        for i, c in enumerate(poblacion):

            if not choco[i]:
                pos_x[i] += c['velocidad']

                if pos_y[i] == SUELO:
                    for obs in obstaculos:
                        if 0 < obs.x - pos_x[i] < c['distancia_salto']:
                            vel_y[i] = -c['salto']

                pos_y[i] += vel_y[i]
                vel_y[i] += 1

                if pos_y[i] > SUELO:
                    pos_y[i] = SUELO
                    vel_y[i] = 0

                # Rect exacto de sprite
                criatura_rect = pygame.Rect(pos_x[i], pos_y[i]-30, 30, 30)
                for obs in obstaculos:
                    if criatura_rect.colliderect(obs):
                        choco[i] = True

            # Dibujar sprite
            ventana.blit(frames[indice_frame[i]], (pos_x[i], pos_y[i]-30))

            if choco[i]:
                pygame.draw.rect(ventana, ROJO, (pos_x[i], pos_y[i]-30, 30, 30), 2)
            elif i == indice_mejor:
                pygame.draw.rect(ventana, VERDE, (pos_x[i], pos_y[i]-30, 30, 30), 2)

        # Texto
        fuente = pygame.font.SysFont(None, 30)
        texto = fuente.render(f"Generación: {gen+1}", True, NEGRO)
        ventana.blit(texto, (10,10))

        pygame.display.update()
        contador_frames += 1

    # Evolución
    poblacion.sort(key=lambda c: aptitud(c, obstaculos), reverse=True)
    mejores = poblacion[:TAM_POBLACION//2]

    poblacion = [
        mutar(cruce(*random.sample(mejores, 2)))
        for _ in range(TAM_POBLACION)
    ]

pygame.quit()
print("Evolución completada!")