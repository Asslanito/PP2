import pygame
import datetime
import math
from tools import flood_fill_fixed as flood_fill, draw_rhombus, draw_right_triangle, draw_equilateral_triangle

pygame.init()
W, H = 1000, 700
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Pygame Paint Application")
canvas = pygame.Surface((W, H))
canvas.fill((255, 255, 255))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

running = True
tool = "pencil"
color = (0, 0, 0)
thickness = 2
drawing = False
start_pos = (0, 0)
last_pos = (0, 0)
typing = False
text_str = ""
text_pos = (0, 0)

while running:
    screen.fill((200, 200, 200))
    screen.blit(canvas, (0, 0))
    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if typing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    txt_surf = font.render(text_str, True, color)
                    canvas.blit(txt_surf, text_pos)
                    typing = False
                    text_str = ""
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text_str = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_str = text_str[:-1]
                else:
                    text_str += event.unicode
            continue

        if event.type == pygame.KEYDOWN:
            # Сохранение
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                name = datetime.datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, name)

            # Размер кисти
            if event.key == pygame.K_1: thickness = 2
            if event.key == pygame.K_2: thickness = 5
            if event.key == pygame.K_3: thickness = 10

            # Выбор инструмента (ИСПРАВЛЕНО)
            if event.key == pygame.K_p: tool = "pencil"
            if event.key == pygame.K_l: tool = "line"
            if event.key == pygame.K_r: tool = "rect"
            if event.key == pygame.K_c: tool = "circle"
            if event.key == pygame.K_e: tool = "eraser"
            if event.key == pygame.K_f: tool = "fill"
            if event.key == pygame.K_t: tool = "text"
            if event.key == pygame.K_q: tool = "square"
            if event.key == pygame.K_a: tool = "right_tri"
            if event.key == pygame.K_w: tool = "eq_tri"
            if event.key == pygame.K_d: tool = "rhombus"

            # Цвета
            if event.key == pygame.K_v: color = (255, 0, 0)
            if event.key == pygame.K_g: color = (0, 255, 0)
            if event.key == pygame.K_b: color = (0, 0, 255)
            if event.key == pygame.K_k: color = (0, 0, 0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if tool == "fill":
                flood_fill(canvas, event.pos[0], event.pos[1], color)
            elif tool == "text":
                typing = True
                text_pos = event.pos
                text_str = ""
            else:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if tool == "line":
                    pygame.draw.line(canvas, color, start_pos, pos, thickness)
                elif tool == "rect":
                    r = pygame.Rect(start_pos, (pos[0] - start_pos[0], pos[1] - start_pos[1]))
                    r.normalize()
                    pygame.draw.rect(canvas, color, r, thickness)
                elif tool == "circle":
                    r = int(math.hypot(pos[0] - start_pos[0], pos[1] - start_pos[1]))
                    pygame.draw.circle(canvas, color, start_pos, r, thickness)
                elif tool == "square":
                    side = max(abs(pos[0] - start_pos[0]), abs(pos[1] - start_pos[1]))
                    s_rect = pygame.Rect(start_pos[0], start_pos[1], side, side)
                    pygame.draw.rect(canvas, color, s_rect, thickness)
                elif tool == "right_tri":
                    draw_right_triangle(canvas, color, start_pos, pos, thickness)
                elif tool == "eq_tri":
                    draw_equilateral_triangle(canvas, color, start_pos, pos, thickness)
                elif tool == "rhombus":
                    draw_rhombus(canvas, color, start_pos, pos, thickness)
                drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == "pencil":
                pygame.draw.line(canvas, color, last_pos, pos, thickness)
                last_pos = pos
            elif tool == "eraser":
                pygame.draw.line(canvas, (255, 255, 255), last_pos, pos, thickness * 5)
                last_pos = pos

    # Отрисовка превью (чтобы видеть фигуру пока тянешь мышь)
    if drawing:
        if tool == "line":
            pygame.draw.line(screen, color, start_pos, pos, thickness)
        elif tool == "rect":
            r = pygame.Rect(start_pos, (pos[0] - start_pos[0], pos[1] - start_pos[1]))
            r.normalize()
            pygame.draw.rect(screen, color, r, thickness)
        elif tool == "circle":
            r = int(math.hypot(pos[0] - start_pos[0], pos[1] - start_pos[1]))
            pygame.draw.circle(screen, color, start_pos, r, thickness)
        elif tool == "square":
            side = max(abs(pos[0] - start_pos[0]), abs(pos[1] - start_pos[1]))
            s_rect = pygame.Rect(start_pos[0], start_pos[1], side, side)
            pygame.draw.rect(screen, color, s_rect, thickness)
        elif tool == "right_tri":
            draw_right_triangle(screen, color, start_pos, pos, thickness)
        elif tool == "eq_tri":
            draw_equilateral_triangle(screen, color, start_pos, pos, thickness)
        elif tool == "rhombus":
            draw_rhombus(screen, color, start_pos, pos, thickness)

    if typing:
        txt_render = font.render(text_str + "|", True, color)
        screen.blit(txt_render, text_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()