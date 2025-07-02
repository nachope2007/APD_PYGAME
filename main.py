import pygame
from constantes import *
from modulos import *

# Inicializar pygame
pygame.init()
pygame.mixer.init()

# Crear ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("EscapeRoom de Programacion")

if ICONO_JUEGO:
    pygame.display.set_icon(ICONO_JUEGO)

# Cargar sonidos

    sonido_fondo = pygame.mixer.Sound("assets/sounds/ghost-fight.mp3")
    sonido_fondo.set_volume(0.045)
    sonido_correcto = pygame.mixer.Sound("assets/sounds/sonido_correcto.mp3")
    sonido_incorrecto = pygame.mixer.Sound("assets/sounds/sonido_incorrecto.mp3")


# Configurar fuentes

    fuente_grande = pygame.font.Font("assets/fonts/napstablook.otf", 35)
    fuente_mediana = pygame.font.Font("assets/fonts/napstablook.otf", 24)
    fuente_chica = pygame.font.Font("assets/fonts/napstablook.otf", 18)


# Variables del juego
estado_juego = ESTADO_MENU
cantidad_jugadores = 1
jugador_actual = 0
jugadores = []
tiempo_restante = TIEMPO_POR_SALA
tiempo_transcurrido = 0
sala_actual = 0
intentos_actuales = 0
respuesta_seleccionada = ""
mostrar_resultado = False
tiempo_resultado = 0
resultados_finales = []

# Crear elementos de interfaz
# Botones del menú
boton_menos = crear_boton((210, 250), 50, 50, "<-", fuente_mediana)
boton_mas = crear_boton((510, 250), 50, 50, "->", fuente_mediana)
boton_listo = crear_boton((350, 350), 100, 50, "LISTO", fuente_mediana)

# Input para nombre
input_nombre = crear_input_box((250, 300), ANCHO_INPUT, ALTO_INPUT, fuente_mediana)

# Botones de opciones (sala de juego)
botones_opciones = []
for i in range(3):
    x = 50 + i * 250
    y = 400
    boton = crear_boton((x, y), 200, 50, "", fuente_chica)
    botones_opciones.append(boton)

# Botón continuar
boton_continuar = crear_boton((350, 500), 100, 50, "CONTINUAR", fuente_mediana)

# Botón volver al menú
boton_menu = crear_boton((350, 450), 150, 50, "VOLVER AL MENU", fuente_chica)

# Reloj para controlar FPS
reloj = pygame.time.Clock()

# Inicializar música de fondo
if sonido_fondo:
    sonido_fondo.play(-1)

# Bucle principal del juego
corriendo = True
tiempo_anterior = pygame.time.get_ticks()

while corriendo:
    tiempo_actual = pygame.time.get_ticks()
    dt = tiempo_actual - tiempo_anterior
    tiempo_anterior = tiempo_actual
    
    # Manejar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        
        # Eventos específicos por estado
        if estado_juego == ESTADO_MENU:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_menos['rect'].collidepoint(evento.pos):
                    cantidad_jugadores = max(NUMERO_MINIMO_JUGADORES, cantidad_jugadores - 1)
                elif boton_mas['rect'].collidepoint(evento.pos):
                    cantidad_jugadores = min(MAX_JUGADORES, cantidad_jugadores + 1)
                elif boton_listo['rect'].collidepoint(evento.pos):
                    estado_juego = ESTADO_INGRESO_NOMBRE
                    jugadores = []
        
        elif estado_juego == ESTADO_INGRESO_NOMBRE:
            manejar_evento_input(input_nombre, evento)
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_continuar['rect'].collidepoint(evento.pos) and input_nombre['texto'].strip():
                    jugador = inicializar_jugador(input_nombre['texto'].strip())
                    jugadores.append(jugador)
                    input_nombre['texto'] = ''
                    estado_juego = ESTADO_JUGANDO
                    tiempo_restante = TIEMPO_POR_SALA
                    sala_actual = 0
                    intentos_actuales = 0
                    mostrar_resultado = False
        
        elif estado_juego == ESTADO_JUGANDO and not mostrar_resultado:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, boton in enumerate(botones_opciones):
                    if boton['rect'].collidepoint(evento.pos):
                        respuesta = DESAFIOS[sala_actual]['opciones'][i]
                        procesar_respuesta(respuesta)
        
        elif estado_juego == ESTADO_RESULTADO_FINAL:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_continuar['rect'].collidepoint(evento.pos):
                    avanzar_jugador()
        
        elif estado_juego == ESTADO_TABLA_FINAL:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_menu['rect'].collidepoint(evento.pos):
                    reiniciar_juego()
    
    # Actualizar temporizador
    if estado_juego == ESTADO_JUGANDO and not mostrar_resultado:
        tiempo_restante -= dt / 1000.0
        if tiempo_restante <= 0:
            tiempo_restante = 0
            mostrar_resultado = True
            tiempo_resultado = pygame.time.get_ticks()
    
    # Manejar resultado de sala
    if mostrar_resultado and estado_juego == ESTADO_JUGANDO:
        if tiempo_actual - tiempo_resultado > 2000:  # Mostrar resultado por 2 segundos
            mostrar_resultado = False
            jugador = jugadores[jugador_actual]
            
            if jugador['sala_actual'] > sala_actual:  # Avanzó de sala
                sala_actual += 1
                intentos_actuales = 0
                tiempo_restante = TIEMPO_POR_SALA
                
                if sala_actual >= NUMERO_SALAS:  # Completó todas las salas
                    estado_juego = ESTADO_RESULTADO_FINAL
            else:  # No avanzó (se quedó sin intentos o tiempo)
                estado_juego = ESTADO_RESULTADO_FINAL
    
    # Dibujar según el estado
    if estado_juego == ESTADO_MENU:
        dibujar_menu()
    elif estado_juego == ESTADO_INGRESO_NOMBRE:
        dibujar_ingreso_nombre()
    elif estado_juego == ESTADO_JUGANDO:
        if mostrar_resultado:
            dibujar_resultado_sala()
        else:
            dibujar_sala_juego()
    elif estado_juego == ESTADO_RESULTADO_FINAL:
        dibujar_resultado_final()
    elif estado_juego == ESTADO_TABLA_FINAL:
        dibujar_tabla_final()
    
    # Actualizar pantalla
    pygame.display.flip()
    reloj.tick(60)

# Finalizar pygame
if sonido_fondo:
    sonido_fondo.stop()
pygame.quit()
