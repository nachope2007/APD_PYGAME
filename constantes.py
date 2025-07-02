import pygame

# COLORES
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_ROJO = (255, 0, 0)
COLOR_VERDE = (0, 255, 0)
COLOR_AZUL = (0, 0, 255)
COLOR_GRIS = (128, 128, 128)
COLOR_AMARILLO = (255, 255, 0)
COLOR_CELESTE = (0, 255, 255)
COLOR_MAGENTA = (255, 0, 255)

# CONFIGURACIÓN VENTANA
ANCHO_VENTANA = 800
ALTO_VENTANA = 600

# IMÁGENES Y RECURSOS

ICONO_JUEGO = pygame.image.load("assets/images/icono_juego.jpg")
IMG_FONDO = pygame.image.load("assets/images/fondo.jpg")
IMG_PUERTA_CERRADA = pygame.image.load("assets/images/puerta_cerrada.png")
IMG_PUERTA_ABIERTA = pygame.image.load("assets/images/puerta_abierta.png")
IMG_GANADOR = pygame.image.load("assets/images/ganador.png")
IMG_PERDEDOR = pygame.image.load("assets/images/perdedor.png")


# CONFIGURACIÓN DE JUEGO
MAX_JUGADORES = 10
NUMERO_MINIMO_JUGADORES = 1
NUMERO_SALAS = 4
MAX_INTENTOS = 2
TIEMPO_POR_SALA = 30  # segundos

# PUNTAJES POR SALA
PUNTUACION_SALA_1 = 10
PUNTUACION_SALA_2 = 20
PUNTUACION_SALA_3 = 30
PUNTUACION_SALA_4 = 40

# DESAFÍOS DEL JUEGO
DESAFIOS = [
    {
        "pregunta": "¿Cuál es el resultado de len('Python')?",
        "opciones": ["5", "6", "7"],
        "respuesta": "6",
        "puntaje": PUNTUACION_SALA_1
    },
    {
        "pregunta": "Dada la lista nums = [3,1,4,1,5], ¿cuál es sorted(nums)?",
        "opciones": ["[1,1,3,4,5]", "[3,1,4,1,5]", "[5,4,3,1,1]"],
        "respuesta": "[1,1,3,4,5]",
        "puntaje": PUNTUACION_SALA_2
    },
    {
        "pregunta": "Dada mat = [[1,2],[3,4]], ¿qué valor tiene mat[1][0]?",
        "opciones": ["1", "2", "3"],
        "respuesta": "3",
        "puntaje": PUNTUACION_SALA_3
    },
    {
        "pregunta": "¿Cuál es el resultado de not(True and False) or False?",
        "opciones": ["True", "False", "None"],
        "respuesta": "True",
        "puntaje": PUNTUACION_SALA_4
    }
]

# ESTADOS DEL JUEGO
ESTADO_MENU = 0
ESTADO_INGRESO_NOMBRE = 1
ESTADO_JUGANDO = 2
ESTADO_RESULTADO_SALA = 3
ESTADO_RESULTADO_FINAL = 4
ESTADO_TABLA_FINAL = 5

# COLORES DE INTERFAZ
COLOR_FONDO = (20, 20, 40)
COLOR_BOTON = (100, 100, 150)
COLOR_BOTON_HOVER = (150, 150, 200)
COLOR_TEXTO_BOTON = COLOR_BLANCO
COLOR_CORRECTO = (0, 200, 0)
COLOR_INCORRECTO = (200, 0, 0)

# CONFIGURACIONES DE INPUT
ANCHO_INPUT = 300
ALTO_INPUT = 40