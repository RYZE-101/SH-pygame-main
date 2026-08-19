# Importieren u. initialisieren der Pygame-Bibliothek
from meinspiel import MeinSpiel
import pygame
from pygame.locals import *
pygame.init()


# Variablen/KONSTANTEN setzen
Breite, Hoehe = 840, 840
Pixel = 60
FelderX, FelderY = int(Breite / Pixel), int(Hoehe / Pixel)
FPS  = 60
SCHWARZ = ( 0, 0, 0)
WEISS   = ( 255, 255, 255)
pyGameBilder = []

# Bilder aus meinSpiel werden für pygame vorbereitet
meinSpiel = MeinSpiel(FelderX, FelderY)
for fname in meinSpiel.bilder:
    pyGameBilder.append(pygame.image.load(fname))

#Anfangskonfiguration für das Spielfeld wird geladen
meinSpiel.anfangsKonfiguration()

# Definieren und Öffnen eines neuen Fensters
fenster = pygame.display.set_mode((Breite, Hoehe))
pygame.display.set_caption("Mein erstes Spiel")
clock = pygame.time.Clock()

# Schleife Hauptprogramm
while True:
    # Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        # Beenden bei [ESC] oder [X]
        if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
            pygame.quit()

    # Spiellogik
        if event.type==KEYDOWN:
            meinSpiel.tasteGedrueckt(event.key)
            print("ok")


    # Spielfeld löschen
    for x in range(FelderX):
        for y in range(FelderY):  
            fenster.blit(pyGameBilder[meinSpiel.spielfeld[x][y]],(x*Pixel,y*Pixel))

    # Spielfeld/figuren zeichnen

    # Fenster aktualisieren
    pygame.display.flip()
    clock.tick(FPS)