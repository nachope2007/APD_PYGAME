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

def dibujar_texto(ventana, texto, fuente, color, pos):
    """Dibuja texto en una posición específica"""
    texto_superficie = fuente.render(texto, True, color)
    ventana.blit(texto_superficie, pos)

def formatear_tiempo(segundos):
    """Convierte segundos a formato MM:SS"""
    tiempo_segundos = int(tiempo_segundos)

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