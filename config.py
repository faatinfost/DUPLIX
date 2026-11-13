import pygame

# --- Настройки окна и графики ---
N = 4
TILE_SIZE = 110
GAP = 10
TOP_PANEL = 100

WIDTH = N * TILE_SIZE + (N + 1) * GAP
HEIGHT = WIDTH + TOP_PANEL

# --- Цвета ---
DARK = (15, 16, 32)
EMPTY = (27, 29, 58)
WHITE = (255, 255, 255)
CYAN = (50, 255, 193)
PINK = (255, 77, 109)
GOLD = (255, 215, 0)

# --- Тряска ---
SHAKE_MAGNITUDE = 6
SHAKE_DECAY = -0.6
SHAKE_STOP = 1.0

# --- Игровые константы ---
NEW_TILES = [2] * 9 + [4]

DIRS = {
    pygame.K_LEFT: 3, pygame.K_RIGHT: 1, pygame.K_UP: 0, pygame.K_DOWN: 2,
    pygame.K_a: 3, pygame.K_d: 1, pygame.K_w: 0, pygame.K_s: 2,
}