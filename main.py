import csv
import json
import pygame
from constantes import *
from modulos import *


pygame.init()
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Mi Juego")
pygame.display.set_icon(ICONO_JUEGO)
pygame.draw.rect(ventana, COLOR_FONDO, IMG_FONDO.get_rect())

pygame.mixer.init()
sonido_fondo = pygame.mixer.Sound("assets/sounds/ghost-fight.mp3")
volumen = 0.045
sonido_fondo.set_volume(volumen)


fuente = pygame.font.Font("assets/fonts/napstablook.otf", 35)
#Bienvenida
texto1 = fuente.render("Bienvenido al EscapeRoom", True, COLOR_BLANCO, COLOR_NEGRO)
texto1_recta = texto1.get_rect()
texto1_recta.centerx = (ANCHO_VENTANA // 2)
texto1_recta.top = (ALTO_VENTANA // 12)

texto2 = fuente.render("de Programacion!", True, COLOR_BLANCO, COLOR_NEGRO)
texto2_recta = texto2.get_rect()
texto2_recta.centerx = (ANCHO_VENTANA // 2)
texto2_recta.top = (ALTO_VENTANA / 7)
#Cantidad partcipantes
fuente = pygame.font.Font("assets/fonts/napstablook.otf", 20)
texto_cant = fuente.render("Elija la cantidad de participantes", True, COLOR_BLANCO, COLOR_NEGRO)
texto_cant_recta = texto_cant.get_rect()
texto_cant_recta.centerx = (ANCHO_VENTANA / 2)
texto_cant_recta.top = (ALTO_VENTANA // 4)

#Boton
boton_listo = crear_boton(ventana, (350, 500), fuente=pygame.font.Font("assets/fonts/napstablook.otf", 30), texto="LISTO")
boton_R = crear_boton(ventana, (510, 250), fuente=pygame.font.Font("assets/fonts/napstablook.otf", 30), texto="->")
boton_L = crear_boton(ventana, (210, 250), fuente=pygame.font.Font("assets/fonts/napstablook.otf", 30), texto="<-")



corriendo = True
while corriendo:
    sonido_fondo.play(-1)  # Reproduce el sonido en bucle
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
    
    ventana.blit(IMG_FONDO, (0, 0))
    ventana.blit(texto1, texto1_recta)
    ventana.blit(texto2, texto2_recta)
    ventana.blit(texto_cant, texto_cant_recta)

    mouse_pos = pygame.mouse.get_pos()
    if boton_listo['rect'].collidepoint(mouse_pos):
       color_boton = COLOR_BLANCO
       print("COLISION")
    else:
       color_boton = COLOR_NEGRO
       

    if boton_R['rect'].collidepoint(mouse_pos):
       color_boton_R = COLOR_BLANCO
       print("COLISION")
    else:
       color_boton_R = COLOR_NEGRO
       
    
    if boton_L['rect'].collidepoint(mouse_pos):
       color_boton_L = COLOR_BLANCO
       print("COLISION")
    else:
       color_boton_L = COLOR_NEGRO
       
    
    dibujar(boton_listo)
    dibujar(boton_R)  
    dibujar(boton_L)

    pygame.display.flip()

    if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Botón izquierdo del mouse
                if boton_listo["rect"].collidepoint(evento.pos):
                    ()

sonido_fondo.stop()  
pygame.quit()