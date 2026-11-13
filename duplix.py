import pygame
import random
import sys
import os
from config import *
from logic import turn, slide, move_logic
from tile import Tile
from menu import run_menu  # <-- ДОБАВИТЬ
from menu import run_menu, run_pause_menu

# Импортируем наши новые модули
from config import *
from logic import turn, slide, move_logic
from tile import Tile

# --- Синхронизация логики и графических объектов ---
def update_tiles_positions(board_matrix, tile_objects, k):
    index_board = [[[] for _ in range(N)] for _ in range(N)]
    for obj in tile_objects:
        c = int((obj.target_x - GAP) / (TILE_SIZE + GAP))
        r = int((obj.target_y - GAP - TOP_PANEL) / (TILE_SIZE + GAP))
        index_board[c][r].append(obj)

    for _ in range(k):
        index_board = turn(index_board)

    for col_idx in range(N):
        row = index_board[col_idx]
        filtered = [cell for cell in row if cell]
        i = 0
        while i < len(filtered) - 1:
            if filtered[i][0].value == filtered[i + 1][0].value:
                filtered[i + 1][0].next_value = filtered[i + 1][0].value * 2
                filtered[i][0].merged = True
                filtered[i + 1].extend(filtered[i])
                filtered.pop(i)
            i += 1
        index_board[col_idx] = filtered + [[]] * (N - len(filtered))

    for _ in range(4 - k):
        index_board = turn(index_board)

    new_objects = []
    for c in range(N):
        for r in range(N):
            for obj in index_board[c][r]:
                obj.set_target(c, r)
                new_objects.append(obj)
    return new_objects

def add_new_tile(board_matrix, tile_objects):
    free = [(x, y) for x in range(N) for y in range(N) if board_matrix[x][y] == 0]
    if free:
        x, y = random.choice(free)
        val = random.choice(NEW_TILES)
        board_matrix[x][y] = val
        tile = Tile(x, y, val)
        tile.scale = 0.0
        tile_objects.append(tile)

def load_best_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            content = f.read().strip()
            if content.isdigit():
                return int(content)
    return 0

def save_best_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# --- Главная функция игры ---
def run_game(screen, clock, fonts, best_score):
    font_go_sub = fonts['go_sub']
    font_score_title = fonts['score_title']
    font_score_val = fonts['score_val']
    font_gameover = fonts['gameover']
    font_tile_big = fonts['tile_big']
    font_tile_small = fonts['tile_small']

    # --- Звуки ---
    audio_ok = pygame.mixer.get_init() is not None
    if audio_ok:
        try:
            SOUND_MOVE = pygame.mixer.Sound("sounds/move.mp3")
            SOUND_GAMEOVER = pygame.mixer.Sound("sounds/gameover.mp3")
            SOUND_RESTART = pygame.mixer.Sound("sounds/restart.mp3")
            SOUND_INVALID = pygame.mixer.Sound("sounds/invalid.wav")
            SOUND_MERGE = pygame.mixer.Sound("sounds/merge.mp3")

            SOUND_MOVE.set_volume(0.2)
            SOUND_GAMEOVER.set_volume(0.5)
            SOUND_RESTART.set_volume(0.4)
            SOUND_INVALID.set_volume(0.3)
            SOUND_MERGE.set_volume(0.4)
        except (FileNotFoundError, pygame.error) as e:
            print(f"Ошибка загрузки звука: {e}. Играем без звука.")
            audio_ok = False
    if not audio_ok:
        SOUND_MOVE = SOUND_GAMEOVER = SOUND_RESTART = SOUND_INVALID = SOUND_MERGE = None

    best_score = load_best_score()
    move_queue = []
    board = [[0] * N for _ in range(N)]
    tile_objects = []
    score = 0
    alive = True
    animating = False

    go_alpha = 0
    go_timer = 0
    go_y = HEIGHT + 50
    sub_y = HEIGHT + 120
    target_go_y = HEIGHT // 2 + TOP_PANEL // 2 - 40
    target_sub_y = target_go_y + 65
    restarting = False
    go_vel = 0
    sub_vel = 0
    shake_offset = [0.0, 0.0]
    pending_merge = 0
    muted = False

    add_new_tile(board, tile_objects)
    add_new_tile(board, tile_objects)

    while True:
        any_moved = False
        for obj in tile_objects:
            if not restarting and obj.update():
                any_moved = True

        if animating and not any_moved:
            animating = False
            tile_objects = [obj for obj in tile_objects if not obj.merged]
            add_new_tile(board, tile_objects)

            if pending_merge and audio_ok and not muted:
                SOUND_MERGE.play()
                pending_merge = 0

            was_alive = alive
            alive = any(move_logic(board, i)[0] != board for i in range(4))
            if was_alive and not alive:
                move_queue.clear()
                if audio_ok and not muted:
                    SOUND_GAMEOVER.play()

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                SOUND_RESTART.stop()
            if event.type == pygame.QUIT:
                save_best_score(best_score)
                return "exit"

            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if audio_ok: pygame.mixer.pause()  # Замирают все звуки
                        action = run_pause_menu(screen, clock, fonts)

                        if action == "resume":
                            if audio_ok: pygame.mixer.unpause()
                            move_queue.clear()  # Очищаем очередь, чтобы игрок не сделал случайный ход
                        elif action == "restart":
                            if audio_ok: pygame.mixer.unpause()
                            # Сброс игры прямо здесь
                            board = [[0] * N for _ in range(N)]
                            tile_objects = []
                            move_queue.clear()
                            score = 0
                            alive = True
                            animating = False
                            restarting = False
                            shake_offset = [0.0, 0.0]
                            pending_merge = 0
                            add_new_tile(board, tile_objects)
                            add_new_tile(board, tile_objects)
                        elif action in ("menu", "exit"):
                            save_best_score(best_score)
                            return action
                        continue  # Важно! Пропускаем остальную обработку событий, пока были в паузе


                if event.key == pygame.K_m:
                    muted = not muted
                    continue
                if alive:
                    k = DIRS.get(event.key)
                    if k is not None and len(move_queue) < 2:
                        move_queue.append(k)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and not restarting:
                    restarting = True
                    go_vel = -9
                    sub_vel = -6
                    if audio_ok and not muted:
                        SOUND_RESTART.play()
                        pygame.time.set_timer(pygame.USEREVENT + 1, 2000, loops=1)

        if not animating and alive and move_queue:
            k = move_queue.pop(0)
            new_board, gain = move_logic(board, k)
            if new_board != board:
                tile_objects = update_tiles_positions(board, tile_objects, k)
                board = new_board
                score += gain
                if score > best_score:
                    best_score = score

                pending_merge = 1 if any(obj.next_value != obj.value for obj in tile_objects) else 0
                if audio_ok and not muted and not pending_merge:
                    SOUND_MOVE.play()

                animating = True
            else:
                move_queue.clear()
                dir_vecs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
                dx, dy = dir_vecs[k]
                shake_offset[0] = dx * SHAKE_MAGNITUDE
                shake_offset[1] = dy * SHAKE_MAGNITUDE
                if audio_ok and not muted:
                    SOUND_INVALID.play()

        if shake_offset[0] != 0 or shake_offset[1] != 0:
            shake_offset[0] *= SHAKE_DECAY
            shake_offset[1] *= SHAKE_DECAY
            if abs(shake_offset[0]) < SHAKE_STOP: shake_offset[0] = 0
            if abs(shake_offset[1]) < SHAKE_STOP: shake_offset[1] = 0

        screen.fill(DARK)

        sx, sy = int(shake_offset[0]), int(shake_offset[1])
        for c in range(N):
            for r in range(N):
                rect = pygame.Rect(
                    c * (TILE_SIZE + GAP) + GAP + sx,
                    r * (TILE_SIZE + GAP) + GAP + TOP_PANEL + sy,
                    TILE_SIZE, TILE_SIZE
                )
                pygame.draw.rect(screen, EMPTY, rect, border_radius=8)

        for obj in sorted(tile_objects, key=lambda x: not x.merged):
            obj.draw(screen, font_tile_big, font_tile_small, sx, sy)

        score_title = font_score_title.render("SCORE", True, WHITE)
        score_val = font_score_val.render(str(score), True, CYAN)
        screen.blit(score_title, (GAP + 10, 20))
        screen.blit(score_val, (GAP + 10, 50))

        best_title = font_score_title.render("BEST", True, GOLD)
        best_val = font_score_val.render(str(best_score), True, GOLD)
        screen.blit(best_title, best_title.get_rect(topright=(WIDTH - GAP - 10, 20)))
        screen.blit(best_val, best_val.get_rect(topright=(WIDTH - GAP - 10, 50)))

        if not alive:
            if restarting:
                go_y += go_vel
                go_vel += 1.4
                sub_y += sub_vel
                sub_vel += 1.4
                go_alpha = max(0, go_alpha - 12)
                for obj in tile_objects:
                    obj.scale = max(0.0, obj.scale - 0.08)

                if go_y > HEIGHT + 100 and all(obj.scale <= 0 for obj in tile_objects):
                    board = [[0] * N for _ in range(N)]
                    tile_objects = []
                    move_queue = []
                    save_best_score(best_score)
                    score = 0
                    alive = True
                    animating = False
                    restarting = False
                    go_alpha = 0
                    go_timer = 0
                    go_y = HEIGHT + 50
                    sub_y = HEIGHT + 120
                    shake_offset = [0.0, 0.0]
                    pending_merge = 0
                    add_new_tile(board, tile_objects)
                    add_new_tile(board, tile_objects)
            else:
                go_timer += 1
                if go_alpha < 195:
                    go_alpha = min(go_alpha + 8, 195)
                if go_y > target_go_y:
                    go_y -= max(2, (go_y - target_go_y) * 0.15)
                if go_timer > 25 and sub_y > target_sub_y:
                    sub_y -= max(2, (sub_y - target_sub_y) * 0.15)

            overlay = pygame.Surface((WIDTH, HEIGHT - TOP_PANEL))
            overlay.set_alpha(go_alpha)
            overlay.fill(DARK)
            screen.blit(overlay, (0, TOP_PANEL))

            go_text = font_gameover.render("GAME OVER", True, PINK)
            screen.blit(go_text, go_text.get_rect(center=(WIDTH // 2, int(go_y))))

            if go_timer > 25:
                best_go = font_go_sub.render(f"BEST: {best_score}", True, GOLD)
                screen.blit(best_go, best_go.get_rect(center=(WIDTH // 2, int(sub_y))))

                hint_go = font_go_sub.render("Press ENTER to restart", True, WHITE)
                screen.blit(hint_go, hint_go.get_rect(center=(WIDTH // 2, int(sub_y) + 42)))

        pygame.display.flip()
        clock.tick(60)


def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Duplix")
    clock = pygame.time.Clock()

    # Загружаем шрифты ОДИН РАЗ для всего приложения
    FONT_FILE = "FredokaOneCyrillic-Regular.ttf"
    fonts = {
        'go_sub': pygame.font.Font(FONT_FILE, 26),
        'score_title': pygame.font.Font(FONT_FILE, 22),
        'score_val': pygame.font.Font(FONT_FILE, 32),
        'gameover': pygame.font.Font(FONT_FILE, 54),
        'tile_big': pygame.font.Font(FONT_FILE, 42),
        'tile_small': pygame.font.Font(FONT_FILE, 32),
        'title': pygame.font.Font(FONT_FILE, 72),  # Новый большой шрифт для меню
        'btn': pygame.font.Font(FONT_FILE, 36)  # Шрифт для кнопок
    }

    best_score = load_best_score()

    while True:
        # Запускаем меню
        action = run_menu(screen, clock, fonts['title'], fonts['btn'], best_score)

        if action == "exit":
            break

        if action == "play":
            # Запускаем игру. Если игрок нажал Esc — вернется "menu", если крестик — "exit"
            result = run_game(screen, clock, fonts, best_score)
            best_score = load_best_score()  # Обновляем рекорд после игры

            if result == "exit":
                break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
