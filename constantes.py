import pygame
#COLORES
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_ROJO = (255, 0, 0)
COLOR_VERDE = (0, 255, 0)
COLOR_AZUL = (0, 0, 255)
COLOR_GRIS = (128, 128, 128)
COLOR_AMARILLO = (255, 255, 0)
COLOR_CELESTE = (0, 255, 255)
COLOR_MAGENTA = (255, 0, 255)

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
ICONO_JUEGO = pygame.image.load("assets/images/icono_juego.jpg")
#FUENTE = pygame.font.Font("assets/fonts/napstablook.otf")
IMG_FONDO = pygame.image.load("assets/images/fondo.jpg")
LEFT_TEXTO = 140
TOP_TEXTO = 430
ANCHO_BOTON = 90
ALTO_BOTON = 50
POS_TOP_BOTON = 200
POS_LEFT_BOTON = 230
ANCHO_PUNTOS = 90
ALTO_PUNTOS = 50
POS_TOP_PUNTOS = 280
POS_LEFT_PUNTOS = 230
DIRECCION_R = 0
DIRECCION_L = 1
TIEMPO = 0
SEGUNDOS = 30
JUGANDO = 0
POS_PREGUNTA = (20,300)
POS_RESPUESTA_A = (20,400)
POS_RESPUESTA_B = (310,400)
POS_RESPUESTA_C = (600,400)
POS_TIMER = (100,100)

MAX_JUGADORES = 10
NUMERO_MINIMO_JUGADORES = 1
NUMERO_SALAS = 4
MAX_INTENTOS = 2

PUNTUACION_SALA_1 = 10
PUNTUACION_SALA_2 = 20
PUNTUACION_SALA_3 = 30
PUNTUACION_SALA_4 = 40

DESAFIOS = [
    ("¿Cuál es el resultado de 2 + 2 * 2?", "6"),
    ("¿Qué palabra reservada en Python se usa para definir una función?", "def"),
    ("¿Cómo se llama el operador lógico que representa 'y' en Python?", "and"),
    ("¿Qué imprime: print(3 * 'ab')?", "ababab"),
]

PUNTOS = [10, 20, 30, 40]

COLOR_FONDO = (0, 0, 0)