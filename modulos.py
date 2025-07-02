import pygame
import json
from constantes import *

def crear_boton(posicion, ancho, alto, texto, fuente, color_fondo=COLOR_BOTON):
    """Crea un diccionario que representa un botón"""
    boton = {
        'rect': pygame.Rect(posicion[0], posicion[1], ancho, alto),
        'texto': texto,
        'fuente': fuente,
        'color_fondo': color_fondo,
        'color_hover': COLOR_BOTON_HOVER,
        'activo': False
    }
    return boton

def dibujar_boton(ventana, boton, mouse_pos):
    """Dibuja un botón en la ventana"""
    color = boton['color_hover'] if boton['rect'].collidepoint(mouse_pos) else boton['color_fondo']
    pygame.draw.rect(ventana, color, boton['rect'])
    pygame.draw.rect(ventana, COLOR_BLANCO, boton['rect'], 2)
    
    texto_superficie = boton['fuente'].render(boton['texto'], True, COLOR_TEXTO_BOTON)
    texto_rect = texto_superficie.get_rect(center=boton['rect'].center)
    ventana.blit(texto_superficie, texto_rect)

def crear_input_box(posicion, ancho, alto, fuente):
    """Crea un campo de entrada de texto"""
    input_box = {
        'rect': pygame.Rect(posicion[0], posicion[1], ancho, alto),
        'texto': '',
        'fuente': fuente,
        'activo': False,
        'color_inactivo': COLOR_GRIS,
        'color_activo': COLOR_BLANCO
    }
    return input_box

def dibujar_input_box(ventana, input_box):
    """Dibuja un campo de entrada de texto"""
    color = input_box['color_activo'] if input_box['activo'] else input_box['color_inactivo']
    pygame.draw.rect(ventana, color, input_box['rect'], 2)
    
    texto_superficie = input_box['fuente'].render(input_box['texto'], True, COLOR_BLANCO)
    ventana.blit(texto_superficie, (input_box['rect'].x + 5, input_box['rect'].y + 5))

def manejar_evento_input(input_box, evento):
    """Maneja los eventos de entrada de texto"""
    if evento.type == pygame.MOUSEBUTTONDOWN:
        input_box['activo'] = input_box['rect'].collidepoint(evento.pos)
    
    if evento.type == pygame.KEYDOWN and input_box['activo']:
        if evento.key == pygame.K_BACKSPACE:
            input_box['texto'] = input_box['texto'][:-1]
        else:
            input_box['texto'] += evento.unicode

def dibujar_texto_centrado(ventana, texto, fuente, color, y):
    """Dibuja texto centrado horizontalmente en la ventana"""
    texto_superficie = fuente.render(texto, True, color)
    x = (ANCHO_VENTANA - texto_superficie.get_width()) // 2
    ventana.blit(texto_superficie, (x, y))

def dibujar_pregunta_con_saltos(ventana, pregunta, fuente, color, y_inicial):
    """Dibuja una pregunta respetando los saltos de línea \n"""
    lineas = pregunta.split('\n')
    y_actual = y_inicial
    
    for linea in lineas:
        dibujar_texto_centrado(ventana, linea, fuente, color, y_actual)
        y_actual += fuente.get_height() + 5
    
    return y_actual

def dibujar_texto(ventana, texto, fuente, color, pos):
    """Dibuja texto en una posición específica"""
    texto_superficie = fuente.render(texto, True, color)
    ventana.blit(texto_superficie, pos)

def formatear_tiempo(segundos):
    """Convierte segundos a formato MM:SS"""
    segundos = int(segundos)  # Cambié tiempo_segundos por segundos
    minutos = segundos // 60
    segundos = segundos % 60
    return f"{minutos:02d}:{segundos:02d}"

def guardar_resultados_json(resultados, archivo="resultados.json"):
    """Guarda los resultados del juego en un archivo JSON"""
    data = {
        'jugadores': resultados,
        'total_jugadores': len(resultados)
    }
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def calcular_puntaje_total(puntajes):
    """Calcula el puntaje total sumando todos los puntajes"""
    total = 0
    for puntaje in puntajes:
        total += puntaje
    return total

def obtener_ganadores_puntaje(resultados):
    """Obtiene los jugadores con mayor puntaje"""
    #if not resultados:
    #    return []
    
    max_puntaje = 0
    for jugador in resultados:
        puntaje_total = calcular_puntaje_total(jugador['puntajes'])
        if puntaje_total > max_puntaje:
            max_puntaje = puntaje_total
    
    ganadores = []
    for jugador in resultados:
        if calcular_puntaje_total(jugador['puntajes']) == max_puntaje:
            ganadores.append(jugador['nombre'])
    
    return ganadores, max_puntaje

def obtener_mas_lejos(resultados):
    """Obtiene los jugadores que llegaron más lejos"""    
    max_sala = 0
    for jugador in resultados:
        if jugador['sala_actual'] > max_sala:
            max_sala = jugador['sala_actual']
    
    mas_lejos = []
    for jugador in resultados:
        if jugador['sala_actual'] == max_sala:
            mas_lejos.append(jugador['nombre'])
    
    return mas_lejos, max_sala

def obtener_no_superaron_primera(resultados):
    """Obtiene los jugadores que no superaron la primera sala"""
    no_superaron = []
    for jugador in resultados:
        if jugador['sala_actual'] == 0:
            no_superaron.append(jugador['nombre'])
    
    return no_superaron

def crear_rectangulo_con_borde(ventana, rect, color_fondo, color_borde, grosor_borde=2):
    """Crea un rectángulo con borde"""
    pygame.draw.rect(ventana, color_fondo, rect)
    pygame.draw.rect(ventana, color_borde, rect, grosor_borde)

# Función para dibujar el menú principal
def dibujar_menu(ventana, cantidad_jugadores, fuente_grande, fuente_mediana, boton_menos, boton_mas, boton_listo):
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
def dibujar_ingreso_nombre(ventana, input_nombre, fuente_mediana, jugador_actual, boton_continuar):
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
def dibujar_sala_juego(ventana, jugadores, jugador_actual, sala_actual, tiempo_restante, intentos_actuales, botones_opciones, fuente_grande, fuente_mediana):
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
def dibujar_resultado_sala(ventana, jugadores, jugador_actual, sala_actual, fuente_grande, fuente_mediana, IMG_PUERTA_ABIERTA, IMG_PUERTA_CERRADA, sonido_correcto, sonido_incorrecto):
    ventana.fill(COLOR_FONDO)
    ventana.blit(IMG_FONDO, (0, 0))
    
    jugador = jugadores[jugador_actual]
    
    if jugador['sala_actual'] > sala_actual:  # Respondió correctamente
        dibujar_texto_centrado(ventana, "CORRECTO!", fuente_grande, COLOR_CORRECTO, 200)
        dibujar_texto_centrado(ventana, f"Ganaste {DESAFIOS[sala_actual]['puntaje']} puntos", fuente_mediana, COLOR_BLANCO, 250)
        ventana.blit(IMG_PUERTA_ABIERTA, (350, 300))
        
    else:  # Se quedó sin intentos
        dibujar_texto_centrado(ventana, "INCORRECTO!", fuente_grande, COLOR_INCORRECTO, 200)
        dibujar_texto_centrado(ventana, "Se acabaron los intentos", fuente_mediana, COLOR_BLANCO, 250)
        
        ventana.blit(IMG_PUERTA_CERRADA, (350, 300))

# Función para dibujar resultado final del jugador
def dibujar_resultado_final(ventana, jugadores, jugador_actual, fuente_grande, fuente_mediana, IMG_GANADOR, IMG_PERDEDOR, boton_continuar):
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
def dibujar_tabla_final(ventana, resultados_finales, fuente_grande, fuente_mediana, fuente_chica, boton_menu):
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
def procesar_respuesta(respuesta, jugadores, jugador_actual, sala_actual, sonido_correcto, sonido_incorrecto):
    """Procesa la respuesta del jugador y retorna el estado actualizado"""
    jugador = jugadores[jugador_actual]
    desafio = DESAFIOS[sala_actual]
    
    mostrar_resultado = False
    nuevos_intentos = 0
    
    if respuesta == desafio['respuesta']:
        # Respuesta correcta
        jugador['puntajes'][sala_actual] = desafio['puntaje']
        jugador['sala_actual'] += 1
        
        sonido_correcto.play()
        
        mostrar_resultado = True
        
        # Verificar si completó todas las salas
        if jugador['sala_actual'] >= NUMERO_SALAS:
            jugador['completo'] = True
    else:
        # Respuesta incorrecta
        nuevos_intentos = 1
        
        sonido_incorrecto.play()
    
    return mostrar_resultado, nuevos_intentos

# Función para avanzar al siguiente jugador o finalizar
def avanzar_jugador(jugadores, jugador_actual, cantidad_jugadores, input_nombre, resultados_finales):
    """Procesa el avance al siguiente jugador"""
    resultados_finales.append(jugadores[jugador_actual].copy())
    jugador_actual += 1
    
    if jugador_actual >= cantidad_jugadores:
        # Terminar juego
        guardar_resultados_json(resultados_finales)
        return ESTADO_TABLA_FINAL, jugador_actual
    else:
        # Siguiente jugador
        input_nombre['texto'] = ''
        return ESTADO_INGRESO_NOMBRE, jugador_actual

# Función para reiniciar juego
def reiniciar_juego(input_nombre):
    """Reinicia todos los valores del juego"""
    input_nombre['texto'] = ''
    
    # Retornar los valores iniciales
    return {
        'estado_juego': ESTADO_MENU,
        'cantidad_jugadores': 1,
        'jugador_actual': 0,
        'jugadores': [],
        'tiempo_restante': TIEMPO_POR_SALA,
        'sala_actual': 0,
        'intentos_actuales': 0,
        'mostrar_resultado': False,
        'resultados_finales': []
    }
