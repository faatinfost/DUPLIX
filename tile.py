import pygame
from math import log2
from colorsys import hsv_to_rgb
from config import TILE_SIZE, GAP, TOP_PANEL, DARK

class Tile:
    def __init__(self, col, row, value):
        self.value = value
        self.next_value = value
        self.x = col * (TILE_SIZE + GAP) + GAP
        self.y = row * (TILE_SIZE + GAP) + GAP + TOP_PANEL
        self.target_x = self.x
        self.target_y = self.y
        self.merged = False
        self.scale = 1.0

    def set_target(self, col, row):
        self.target_x = col * (TILE_SIZE + GAP) + GAP
        self.target_y = row * (TILE_SIZE + GAP) + GAP + TOP_PANEL

    def update(self, speed=35):
        moved = False
        if self.scale < 1.0:
            self.scale = min(1.0, self.scale + 0.15)
            moved = True
        if self.x < self.target_x:
            self.x = min(self.x + speed, self.target_x)
            moved = True
        elif self.x > self.target_x:
            self.x = max(self.x - speed, self.target_x)
            moved = True
        if self.y < self.target_y:
            self.y = min(self.y + speed, self.target_y)
            moved = True
        elif self.y > self.target_y:
            self.y = max(self.y - speed, self.target_y)
            moved = True

        dist_x = abs(self.x - self.target_x)
        dist_y = abs(self.y - self.target_y)
        if dist_x <= speed and dist_y <= speed:
            if self.value != self.next_value:
                self.value = self.next_value
        return moved

    def get_color(self):
        h = (.55 + log2(self.value) * 0.07) % 1
        r, g, b = hsv_to_rgb(h, 0.7, 1.0)
        return (int(r * 255), int(g * 255), int(b * 255))

    def draw(self, screen, font_big, font_small, ox=0, oy=0):
        if self.scale <= 0.05:
            return
        cur_size = int(TILE_SIZE * self.scale)
        offset = (TILE_SIZE - cur_size) // 2
        rect = pygame.Rect(int(self.x) + offset + ox, int(self.y) + offset + oy, cur_size, cur_size)
        pygame.draw.rect(screen, self.get_color(), rect, border_radius=max(1, int(8 * self.scale)))
        if self.scale > 0.4:
            text_font = font_big if self.value < 1000 else font_small
            text_surface = text_font.render(str(self.value), True, DARK)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)