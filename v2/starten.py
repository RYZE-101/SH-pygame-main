import pygame
from pygame.locals import *
from meinspiel import MeinSpiel

pygame.init()

Breite, Hoehe = 840, 840
Pixel = 60
FPS = 60

fenster = pygame.display.set_mode((Breite, Hoehe))
pygame.display.set_caption("Mein erstes Spiel")
clock = pygame.time.Clock()

spiel = MeinSpiel(Breite, Hoehe, Pixel)
game_over = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

            if event.key == K_SPACE and not game_over:
                spiel.schiessen()

    keys = pygame.key.get_pressed()

    if not game_over:
        spiel.bewege_spieler(keys)
        spiel.update()

        if spiel.player_hp <= 0:
            game_over = True

    fenster.fill((0, 0, 0))
    spiel.zeichnen(fenster)

    if game_over:
        font = pygame.font.SysFont(None, 80)
        txt = font.render("GAME OVER", True, (255, 0, 0))
        fenster.blit(txt, (Breite // 2 - 180, Hoehe // 2 - 40))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
