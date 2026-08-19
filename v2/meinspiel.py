import pygame
import random

class MeinSpiel:
    def __init__(self, breite, hoehe, pixel):
        self.breite = breite
        self.hoehe = hoehe
        self.pixel = pixel

        # Bilder laden
        self.grass = pygame.transform.scale(
            pygame.image.load("Bilder/Grass.jpg").convert(),
            (pixel, pixel)
        )
        self.player_img = pygame.transform.scale(
            pygame.image.load("Bilder/Stalin.jpg").convert_alpha(),
            (pixel, pixel)
        )
        self.mob_img = pygame.transform.scale(
            pygame.image.load("Bilder/mob.png").convert_alpha(),
            (pixel, pixel)
        )
        self.fireball_img = pygame.transform.scale(
            pygame.image.load("Bilder/feuerball.png").convert_alpha(),
            (24, 24)
        )

        # Spieler
        self.player_x = breite // 2
        self.player_y = hoehe // 2
        self.player_speed = 4
        self.player_hp = 100
        self.last_dir = (1, 0)  # Start: nach rechts

        # Projektile
        self.fireballs = []
        self.fireball_speed = 10
        self.fireball_damage = 25
        self.fireball_range = 400

        # Mobs
        self.mobs = []
        self.mob_hp = 50
        self.mob_speed = 1.4
        self.mob_damage = 10
        self.mob_attack_cooldown = 30
        self.mob_spawn_timer = 0
        self.mob_spawn_delay = 60

    def bewege_spieler(self, keys):
        dx = 0
        dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = 1
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = 1

        if dx != 0 or dy != 0:
            self.last_dir = (dx, dy)
            self.player_x += dx * self.player_speed
            self.player_y += dy * self.player_speed

        self.player_x = max(0, min(self.breite - self.pixel, self.player_x))
        self.player_y = max(0, min(self.hoehe - self.pixel, self.player_y))

    def schiessen(self):
        dx, dy = self.last_dir
        if dx == 0 and dy == 0:
            dx = 1

        fb_x = self.player_x + self.pixel // 2 - 12
        fb_y = self.player_y + self.pixel // 2 - 12

        self.fireballs.append({
            "x": fb_x,
            "y": fb_y,
            "dx": dx,
            "dy": dy,
            "dist": 0
        })
        
        

    def update_fireballs(self):
        for fb in self.fireballs[:]:
            fb["x"] += fb["dx"] * self.fireball_speed
            fb["y"] += fb["dy"] * self.fireball_speed
            fb["dist"] += self.fireball_speed

            if fb["dist"] >= self.fireball_range:
                self.fireballs.remove(fb)
                continue

            if fb["x"] < -30 or fb["x"] > self.breite + 30 or fb["y"] < -30 or fb["y"] > self.hoehe + 30:
                self.fireballs.remove(fb)

    def mob_spawnen(self):
        seite = random.randint(0, 3)

        if seite == 0:
            x = 0
            y = random.randint(0, self.hoehe - self.pixel)
        elif seite == 1:
            x = self.breite - self.pixel
            y = random.randint(0, self.hoehe - self.pixel)
        elif seite == 2:
            x = random.randint(0, self.breite - self.pixel)
            y = 0
        else:
            x = random.randint(0, self.breite - self.pixel)
            y = self.hoehe - self.pixel

        # nicht zu nah am Spieler spawnen
        if abs(x - self.player_x) < 120 and abs(y - self.player_y) < 120:
            return

        mob = {
            "x": float(x),
            "y": float(y),
            "hp": self.mob_hp,
            "attack_timer": 0
        }
        self.mobs.append(mob)

    def update_mobs(self):
        for mob in self.mobs[:]:
            dx = self.player_x - mob["x"]
            dy = self.player_y - mob["y"]
            dist = (dx * dx + dy * dy) ** 0.5

            if dist > 0:
                mob["x"] += self.mob_speed * dx / dist
                mob["y"] += self.mob_speed * dy / dist

            mob["attack_timer"] += 1

            mob_rect = pygame.Rect(int(mob["x"]), int(mob["y"]), self.pixel, self.pixel)
            player_rect = pygame.Rect(self.player_x, self.player_y, self.pixel, self.pixel)

            if mob_rect.colliderect(player_rect):
                if mob["attack_timer"] >= self.mob_attack_cooldown:
                    self.player_hp -= self.mob_damage
                    mob["attack_timer"] = 0

    def kollisionscheck(self):
        for fb in self.fireballs[:]:
            fb_rect = pygame.Rect(int(fb["x"]), int(fb["y"]), 24, 24)

            for mob in self.mobs[:]:
                mob_rect = pygame.Rect(int(mob["x"]), int(mob["y"]), self.pixel, self.pixel)
                if fb_rect.colliderect(mob_rect):
                    mob["hp"] -= self.fireball_damage
                    if fb in self.fireballs:
                        self.fireballs.remove(fb)
                    if mob["hp"] <= 0 and mob in self.mobs:
                        self.mobs.remove(mob)
                    break

    def update(self):
        self.mob_spawn_timer += 1
        if self.mob_spawn_timer >= self.mob_spawn_delay:
            self.mob_spawnen()
            self.mob_spawn_timer = 0

        self.update_fireballs()
        self.update_mobs()
        self.kollisionscheck()

    def zeichnen(self, fenster):
        for x in range(0, self.breite, self.pixel):
            for y in range(0, self.hoehe, self.pixel):
                fenster.blit(self.grass, (x, y))

        fenster.blit(self.player_img, (self.player_x, self.player_y))

        for mob in self.mobs:
            fenster.blit(self.mob_img, (int(mob["x"]), int(mob["y"])))

        for fb in self.fireballs:
            fenster.blit(self.fireball_img, (int(fb["x"]), int(fb["y"])))

        font = pygame.font.SysFont(None, 32)
        hp_text = font.render(f"HP: {self.player_hp}", True, (255, 255, 255))
        fenster.blit(hp_text, (10, 10))
