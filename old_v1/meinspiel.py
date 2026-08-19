import pygame
class MeinSpiel:
    bilder = ["Bilder/Grass.jpg","Bilder/megaAK.jpg"]
    spielfeld = [] 

    def __init__(self, felderX, felderY):
        for x in range(felderX):
            self.spielfeld.append([])
            for y in range(felderY):
                self.spielfeld[x].append(0)

    def anfangsKonfiguration(self):
        self.spielfeld[5][5] = 1
        
    def tasteGedrueckt(self, taste):
        if pygame.K_w == taste:
           print(taste)

