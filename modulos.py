import pygame
import json
import csv
from constantes import *

def leer_csv(nombre_archivo):
    salas = []
    with open(nombre_archivo, newline='', encoding='utf-8') as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            sala = {
                "acertijo": fila["acertijo"],
                "respuesta": fila["respuesta"],
                "puntaje": int(fila["puntaje"])
            }
            salas.append(sala)
    return salas

def validar_texto_vacio(mensaje):
    texto = input(mensaje)
    texto = texto.strip()  # Elimina espacios en blanco al principio y al final
    while texto == "":
        # Si el texto está vacío, solicita nuevamente
        print("El texto no puede estar vacío. Intenta de nuevo.")
        texto = input(mensaje)
        texto = texto.strip()
    return texto 

def validar_int_en_rango (mensaje : str , min : int , max : int = None)->int:
    numero = int(input(mensaje))
    if max is None:
        es_valido = numero >= min
    else:
        es_valido = numero >= min and numero <= max
    while not es_valido:
        # Si el número no está en el rango, solicita nuevamente
        print("Debes ingresar un número entero válido entre", min, "y", max if max is not None else "infinito")
        numero = int(input(mensaje))
        if max is None:
            es_valido = numero >= min
        else:
            es_valido = numero >= min and numero <= max
    return numero

def jugar_salas(salas, nombre):
    puntajes = [0, 0, 0, 0]
    completo = True
    salas_superadas = 0
    idx = 0
    while idx < len(salas) and completo:
        sala = salas[idx]
        acierto = False
        intentos = 1
        while intentos <= 2 and not acierto:
            respuesta = input(f"{nombre} - {sala['acertijo']}\nIntento {intentos}: ").strip()
            if respuesta == sala['respuesta']:
                print("¡Correcto!")
                puntajes[idx] = sala['puntaje']
                salas_superadas += 1
                acierto = True
            else:
                print("Incorrecto.")
            intentos += 1
        if not acierto:
            completo = False
        idx += 1
    resultados_jugador = {
        "nombre": nombre,
        "puntajes": puntajes,
        "completo": completo,
        "salas_superadas": salas_superadas
    }
    return resultados_jugador
def guardar_resultados(resultados, archivo):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4)

def cargar_resultados(archivo):
    with open(archivo, "r", encoding="utf-8") as f:
        json.load(f)
    return archivo 

def mostrar_tabla_resultados(resultados):
    print("\nTabla de Resultados:")
    print(f"{'Jugador':<15}{'Sala 1':<8}{'Sala 2':<8}{'Sala 3':<8}{'Sala 4':<8}{'Total':<8}{'Estado':<12}")
    for r in resultados:
        puntajes = r['puntajes']
        total = 0
        for p in puntajes:
            total += p
        estado = "Completó"
        if not r['completo']:
            estado = "No completó"
        print(f"{r['nombre']:<15}{puntajes[0]:<8}{puntajes[1]:<8}{puntajes[2]:<8}{puntajes[3]:<8}{total:<8}{estado:<12}")

def mostrar_resultados_torneo(resultados):
    # Mayor puntaje total
    max_puntaje = None
    for r in resultados:
        total = 0
        for p in r['puntajes']:
            total += p
        if max_puntaje is None or total > max_puntaje:
            max_puntaje = total
    ganadores = []
    for r in resultados:
        total = 0
        for p in r['puntajes']:
            total += p
        if total == max_puntaje:
            ganadores.append(r['nombre'])
    print("\nMayor puntaje total (" + str(max_puntaje) + "):  ", end="")
    primero = True
    for nombre in ganadores:
        if not primero:
            print(", ", end="")
        print(nombre, end="")
        primero = False

    # Quienes llegaron más lejos
    max_salas = None
    for r in resultados:
        if max_salas is None or r['salas_superadas'] > max_salas:
            max_salas = r['salas_superadas']
    mas_lejos = []
    for r in resultados:
        if r['salas_superadas'] == max_salas:
            mas_lejos.append(r['nombre'])
    print("Quienes llegaron más lejos (" + str(max_salas) + " salas): ", end="")
    primero = True
    for nombre in mas_lejos:
        if not primero:
            print(", ", end="")
        print(nombre, end="")
        primero = False

    # No superaron la primer sala
    no_superaron_primera = []
    for r in resultados:
        if r['salas_superadas'] == 0:
            no_superaron_primera.append(r['nombre'])
    if len(no_superaron_primera) > 0:
        print("No superaron la primer sala: ", end="")
        primero = True
        for nombre in no_superaron_primera:
            if not primero:
                print(", ", end="")
            print(nombre, end="")
            primero = False
        print()
    else:
        print("Todos superaron la primer sala.")


def mostrar_texto(pantalla, fuente, texto, x, y, color):
    texto_renderizado = fuente.render(texto, True, color)
    pantalla.blit(texto_renderizado, (x, y))


def crear_boton(ventana, posicion, fuente=None, texto=None, fondo=None):
    boton = {}
    boton['ventana'] = ventana
    boton['posicion'] = posicion
    boton['texto'] = texto
    boton['fuente'] = fuente
        
    if fondo is None:
        sup_fondo = pygame.draw.rect(ventana, (0, 0, 0), (0, 0, 100, 100))  # Fondo
    else:
        sup_fondo = pygame.draw.rect(fondo)

    sup_fondo = pygame.Surface((100, 50))  # Tamaño del botón
    sup_fondo.fill(COLOR_BLANCO)  # Color de fondo del botón
    boton['fondo'] = sup_fondo

    rect = boton['fondo'].get_rect()
    rect.topleft = posicion
    boton['rect'] = rect
    
    return boton

# Función para dibujar el botón
def dibujar(boton):
    ventana = boton["ventana"]
    ventana.blit(boton['fondo'], boton['posicion'])
    if boton['texto'] is not None:
        texto = boton['fuente'].render(boton['texto'], True, (0, 0, 0))
        rect_texto = texto.get_rect(center=boton['rect'].center)
        ventana.blit(texto, rect_texto)
