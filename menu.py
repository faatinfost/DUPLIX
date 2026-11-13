import pygame
import sys
from config import WIDTH, HEIGHT, DARK, CYAN, PINK, WHITE, GOLD


def run_menu(screen, clock, font_title, font_btn, best_score):
    """Возвращает 'play', 'exit' или 'quit' (если закрыли окно)"""
    play_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 60)
    exit_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 60)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "play"
                if event.key == pygame.K_ESCAPE:
                    return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_rect.collidepoint(mouse_pos):
                    return "play"
                if exit_rect.collidepoint(mouse_pos):
                    return "exit"

        # --- Отрисовка ---
        screen.fill(DARK)

        # Логотип (пульсирует)
        title_text = font_title.render("DUPLIX", True, CYAN)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # Твой рекорд
        best_text = font_btn.render(f"BEST: {best_score}", True, GOLD)
        best_rect = best_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 60))
        screen.blit(best_text, best_rect)

        # Кнопка PLAY (меняет цвет при наведении)
        play_color = CYAN if play_rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(screen, play_color, play_rect, 2, border_radius=10)
        play_text = font_btn.render("PLAY", True, play_color)
        screen.blit(play_text, play_text.get_rect(center=play_rect.center))

        # Кнопка EXIT
        exit_color = PINK if exit_rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(screen, exit_color, exit_rect, 2, border_radius=10)
        exit_text = font_btn.render("EXIT", True, exit_color)
        screen.blit(exit_text, exit_text.get_rect(center=exit_rect.center))

        pygame.display.flip()
        clock.tick(60)


def run_pause_menu(screen, clock, fonts):
    """Возвращает 'resume', 'restart', 'menu' или 'exit'"""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Черный полупрозрачный фон

    resume_rect = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 - 80, 240, 60)
    restart_rect = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2, 240, 60)
    menu_rect = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 80, 240, 60)

    font_btn = fonts['btn']
    font_title = fonts['title']

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    return "resume"  # Esc или Enter продолжают игру
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resume_rect.collidepoint(mouse_pos): return "resume"
                if restart_rect.collidepoint(mouse_pos): return "restart"
                if menu_rect.collidepoint(mouse_pos): return "menu"

        # Отрисовка
        screen.blit(overlay, (0, 0))

        title_text = font_title.render("PAUSED", True, WHITE)
        screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150)))

        # Кнопка Resume
        res_color = CYAN if resume_rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(screen, res_color, resume_rect, 2, border_radius=10)
        res_text = font_btn.render("RESUME", True, res_color)
        screen.blit(res_text, res_text.get_rect(center=resume_rect.center))

        # Кнопка Restart
        rst_color = GOLD if restart_rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(screen, rst_color, restart_rect, 2, border_radius=10)
        rst_text = font_btn.render("RESTART", True, rst_color)
        screen.blit(rst_text, rst_text.get_rect(center=restart_rect.center))

        # Кнопка Menu
        menu_color = PINK if menu_rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(screen, menu_color, menu_rect, 2, border_radius=10)
        menu_text = font_btn.render("MAIN MENU", True, menu_color)
        screen.blit(menu_text, menu_text.get_rect(center=menu_rect.center))

        pygame.display.flip()
        clock.tick(60)