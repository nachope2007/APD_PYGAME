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

# Función para dibujar el menú principal
def dibujar_menu():
    ventana.fill(COLOR_FONDO)
    ventana.blit(IMG_FONDO, (0, 0))
    
    # Título
    dibujar_texto_centrado(ventana, "Bienvenido al EscapeRoom", fuente_grande, COLOR_BLANCO, 50)
    dibujar_texto_centrado(ventana, "de Programacion!", fuente_grande, COLOR_BLANCO, 90)
    
    # Cantidad de participantes
    dibujar_texto_centrado(ventana, "Elija la cantidad de participantes", fuente_mediana, COLOR_BLANCO, 150)
    dibujar_texto_centrado(ventana, str(cantidad_jugadores), fuente_grande, COLOR_BLANCO, 260)
    
    # Botones
    mouse_pos = pygame.mouse.get_pos()
    dibujar_boton(ventana, boton_menos, mouse_pos)
    dibujar_boton(ventana, boton_mas, mouse_pos)
    dibujar_boton(ventana, boton_listo, mouse_pos)

# Función para dibujar ingreso de nombre
def dibujar_ingreso_nombre():
    ventana.fill(COLOR_FONDO)
    ventana.blit(IMG_FONDO, (0, 0))
    
    # Título
    dibujar_texto_centrado(ventana, f"INGRESE EL NOMBRE DEL", fuente_mediana, COLOR_BLANCO, 150)
    dibujar_texto_centrado(ventana, f"PARTICIPANTE {jugador_actual + 1}:", fuente_mediana, COLOR_BLANCO, 180)
    
    # Input de nombre
    dibujar_input_box(ventana, input_nombre)
    
    # Botón continuar (solo si hay texto)
    if input_nombre['texto'].strip():
        mouse_pos = pygame.mouse.get_pos()
        dibujar_boton(ventana, boton_continuar, mouse_pos)

# Función para dibujar la sala de juego
def dibujar_sala_juego():
    ventana.fill(COLOR_FONDO)
    ventana.blit(IMG_FONDO, (0, 0))
    
    # Información superior
    dibujar_texto(ventana, f"SALA {sala_actual + 1}", fuente_grande, COLOR_BLANCO, (50, 20))
    dibujar_texto(ventana, f"TIMER: {formatear_tiempo(tiempo_restante)}", fuente_mediana, COLOR_BLANCO, (50, 60))
    dibujar_texto(ventana, f"VIDAS: {MAX_INTENTOS - intentos_actuales}", fuente_mediana, COLOR_BLANCO, (50, 90))
    
    # Información del jugador
    jugador = jugadores[jugador_actual]
    puntaje_total = calcular_puntaje_total(jugador['puntajes'])
    dibujar_texto(ventana, f"JUGADOR: {jugador['nombre']}", fuente_mediana, COLOR_BLANCO, (400, 20))
    dibujar_texto(ventana, f"PUNTOS: {puntaje_total}", fuente_mediana, COLOR_BLANCO, (400, 50))
    
    # Pregunta
    desafio = DESAFIOS[sala_actual]
    dibujar_pregunta_con_saltos(ventana, desafio['pregunta'], fuente_mediana, COLOR_BLANCO, 170)
    
    # Opciones
    mouse_pos = pygame.mouse.get_pos()
    for i, boton in enumerate(botones_opciones):
        boton['texto'] = desafio['opciones'][i]
        dibujar_boton(ventana, boton, mouse_pos)
    
    # Imagen de puerta (si está disponible)
    ventana.blit(IMG_PUERTA_CERRADA, (690, 250))

# Función para dibujar resultado de sala
def dibujar_resultado_sala():
    ventana.fill(COLOR_FONDO)
    ventana.blit(IMG_FONDO, (0, 0))
    
    jugador = jugadores[jugador_actual]
    
    if jugador['sala_actual'] > sala_actual:  # Respondió correctamente
        dibujar_texto_centrado(ventana, "CORRECTO!", fuente_grande, COLOR_CORRECTO, 200)
        dibujar_texto_centrado(ventana, f"Ganaste {DESAFIOS[sala_actual]['puntaje']} puntos", fuente_mediana, COLOR_BLANCO, 250)
        
        if IMG_PUERTA_ABIERTA:
            ventana.blit(IMG_PUERTA_ABIERTA, (350, 300))
    else:  # Se quedó sin intentos
        dibujar_texto_centrado(ventana, "INCORRECTO!", fuente_grande, COLOR_INCORRECTO, 200)
        dibujar_texto_centrado(ventana, "Se acabaron los intentos", fuente_mediana, COLOR_BLANCO, 250)
        
        ventana.blit(IMG_PUERTA_CERRADA, (350, 300))

# Función para dibujar resultado final del jugador
def dibujar_resultado_final():
    ventana.fill(COLOR_FONDO)
    ventana.blit(IMG_FONDO, (0, 0))
    
    jugador = jugadores[jugador_actual]
    puntaje_total = calcular_puntaje_total(jugador['puntajes'])
    
    if jugador['completo']:
        dibujar_texto_centrado(ventana, "FELICITACIONES!", fuente_grande, COLOR_CORRECTO, 150)
        dibujar_texto_centrado(ventana, "LOGRASTE ESCAPAR", fuente_mediana, COLOR_BLANCO, 200)
        
        if IMG_GANADOR:
            ventana.blit(IMG_GANADOR, (300, 250))
    else:
        dibujar_texto_centrado(ventana, "LO SIENTO...", fuente_grande, COLOR_INCORRECTO, 150)
        dibujar_texto_centrado(ventana, "NO LOGRASTE ESCAPAR", fuente_mediana, COLOR_BLANCO, 200)
        
        if IMG_PERDEDOR:
            ventana.blit(IMG_PERDEDOR, (300, 250))
    
    dibujar_texto_centrado(ventana, f"PUNTUACION: {puntaje_total}", fuente_mediana, COLOR_BLANCO, 400)
    
    # Botón continuar
    mouse_pos = pygame.mouse.get_pos()
    dibujar_boton(ventana, boton_continuar, mouse_pos)

# Función para dibujar tabla final
# Función para dibujar tabla final
def dibujar_tabla_final():
    ventana.fill(COLOR_FONDO)
    
    dibujar_texto_centrado(ventana, "GRACIAS POR JUGAR!", fuente_grande, COLOR_BLANCO, 30)
    
    # Tabla de resultados
    y = 80
    dibujar_texto_centrado(ventana, "TABLA DE RESULTADOS", fuente_mediana, COLOR_BLANCO, y)
    y += 40
    
    # Títulos de las columnas
    dibujar_texto(ventana, "NOMBRE", fuente_chica, COLOR_AMARILLO, (50, y))
    dibujar_texto(ventana, "PUNTOS", fuente_chica, COLOR_AMARILLO, (180, y))
    dibujar_texto(ventana, "SALA 1", fuente_chica, COLOR_AMARILLO, (280, y))
    dibujar_texto(ventana, "COMPLETO", fuente_chica, COLOR_AMARILLO, (380, y))
    y += 30
    
    # Línea separadora (opcional)
    pygame.draw.line(ventana, COLOR_BLANCO, (50, y-5), (450, y-5), 1)
    
    # Datos de los jugadores
    for jugador in resultados_finales:
        puntaje_total = calcular_puntaje_total(jugador['puntajes'])
        primera_sala = "SI" if jugador['sala_actual'] > 0 else "NO"
        completo = "SI" if jugador['completo'] else "NO"
        
        # Nombre (limitado a 10 caracteres)
        nombre_corto = jugador['nombre'][:10] if len(jugador['nombre']) > 10 else jugador['nombre']
        dibujar_texto(ventana, nombre_corto, fuente_chica, COLOR_BLANCO, (50, y))
        
        # Puntaje
        dibujar_texto(ventana, str(puntaje_total), fuente_chica, COLOR_BLANCO, (180, y))
        
        # Primera sala (con color)
        color_primera = COLOR_CORRECTO if primera_sala == "SI" else COLOR_INCORRECTO
        dibujar_texto(ventana, primera_sala, fuente_chica, color_primera, (280, y))
        
        # Completó (con color)
        color_completo = COLOR_CORRECTO if completo == "SI" else COLOR_INCORRECTO
        dibujar_texto(ventana, completo, fuente_chica, color_completo, (380, y))
        
        y += 25
    
    # Resultados del torneo
    y += 20
    dibujar_texto_centrado(ventana, "RESULTADOS DEL TORNEO:", fuente_mediana, COLOR_BLANCO, y)
    y += 30
    
    # Mayor puntaje
    ganadores, max_puntaje = obtener_ganadores_puntaje(resultados_finales)
    texto_ganadores = ", ".join(ganadores)
    dibujar_texto(ventana, f"Mayor puntaje ({max_puntaje}): {texto_ganadores}", fuente_chica, COLOR_BLANCO, (50, y))
    y += 25
    
    # Llegaron más lejos
    mas_lejos, max_sala = obtener_mas_lejos(resultados_finales)
    texto_lejos = ", ".join(mas_lejos)
    dibujar_texto(ventana, f"Llegaron mas lejos ({max_sala} salas): {texto_lejos}", fuente_chica, COLOR_BLANCO, (50, y))
    y += 25
    
    # No superaron primera sala
    no_superaron = obtener_no_superaron_primera(resultados_finales)
    if no_superaron:
        texto_no_superaron = ", ".join(no_superaron)
        dibujar_texto(ventana, f"No superaron primera sala: {texto_no_superaron}", fuente_chica, COLOR_BLANCO, (50, y))
    
    # Botón volver al menú
    mouse_pos = pygame.mouse.get_pos()
    dibujar_boton(ventana, boton_menu, mouse_pos)

# Función para inicializar nuevo jugador
def inicializar_jugador(nombre):
    return {
        'nombre': nombre,
        'puntajes': [0, 0, 0, 0],
        'sala_actual': 0,
        'completo': False
    }

# Función para procesar respuesta
def procesar_respuesta(respuesta):
    global intentos_actuales, mostrar_resultado, tiempo_resultado
    
    jugador = jugadores[jugador_actual]
    desafio = DESAFIOS[sala_actual]
    
    if respuesta == desafio['respuesta']:
        # Respuesta correcta
        jugador['puntajes'][sala_actual] = desafio['puntaje']
        jugador['sala_actual'] += 1
        
        if sonido_correcto:
            sonido_correcto.play()
        
        mostrar_resultado = True
        tiempo_resultado = pygame.time.get_ticks()
        
        # Verificar si completó todas las salas
        if jugador['sala_actual'] >= NUMERO_SALAS:
            jugador['completo'] = True
    else:
        # Respuesta incorrecta
        intentos_actuales += 1
        
        if sonido_incorrecto:
            sonido_incorrecto.play()
        
        if intentos_actuales >= MAX_INTENTOS:
            mostrar_resultado = True
            tiempo_resultado = pygame.time.get_ticks()

# Función para avanzar al siguiente jugador o finalizar
def avanzar_jugador():
    global jugador_actual, estado_juego, sala_actual, intentos_actuales, tiempo_restante
    
    resultados_finales.append(jugadores[jugador_actual].copy())
    jugador_actual += 1
    
    if jugador_actual >= cantidad_jugadores:
        # Terminar juego
        estado_juego = ESTADO_TABLA_FINAL
        guardar_resultados_json(resultados_finales)
    else:
        # Siguiente jugador
        estado_juego = ESTADO_INGRESO_NOMBRE
        input_nombre['texto'] = ''
        sala_actual = 0
        intentos_actuales = 0
        tiempo_restante = TIEMPO_POR_SALA

# Función para reiniciar juego
def reiniciar_juego():
    global estado_juego, cantidad_jugadores, jugador_actual, jugadores, tiempo_restante
    global sala_actual, intentos_actuales, mostrar_resultado, resultados_finales
    
    estado_juego = ESTADO_MENU
    cantidad_jugadores = 1
    jugador_actual = 0
    jugadores = []
    tiempo_restante = TIEMPO_POR_SALA
    sala_actual = 0
    intentos_actuales = 0
    mostrar_resultado = False
    resultados_finales = []
    input_nombre['texto'] = ''

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
