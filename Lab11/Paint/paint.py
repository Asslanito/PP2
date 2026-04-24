import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    drawing_mode = 'pen'
    color = (255, 0, 0)
    points = []
    start_pos = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: drawing_mode = 'rect'
                if event.key == pygame.K_c: drawing_mode = 'circle'
                if event.key == pygame.K_p: drawing_mode = 'pen'
                if event.key == pygame.K_e: drawing_mode = 'eraser'
                if event.key == pygame.K_s: drawing_mode = 'square'
                if event.key == pygame.K_t: drawing_mode = 'right_tri'
                if event.key == pygame.K_u: drawing_mode = 'equi_tri'
                if event.key == pygame.K_h: drawing_mode = 'rhombus'
                if event.key == pygame.K_1: color = (255, 0, 0)
                if event.key == pygame.K_2: color = (0, 255, 0)
                if event.key == pygame.K_3: color = (0, 0, 255)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if drawing_mode in ['rect', 'circle', 'square', 'right_tri', 'equi_tri', 'rhombus']:
                    start_pos = event.pos
                else:
                    points.append(('pen' if drawing_mode == 'pen' else 'eraser', event.pos, color if drawing_mode == 'pen' else (0,0,0)))

            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                if drawing_mode in ['pen', 'eraser']:
                    points.append((drawing_mode, event.pos, color if drawing_mode == 'pen' else (0,0,0)))

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing_mode in ['rect', 'circle', 'square', 'right_tri', 'equi_tri', 'rhombus'] and start_pos:
                    points.append((drawing_mode, start_pos, event.pos, color))
                    start_pos = None

        screen.fill((0, 0, 0))

        def draw_shape(mode, start, end, col, surf):
            x1, y1 = start
            x2, y2 = end
            if mode == 'rect':
                r = pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))
                pygame.draw.rect(surf, col, r, 2)
            elif mode == 'circle':
                rd = int(math.hypot(x1 - x2, y1 - y2))
                pygame.draw.circle(surf, col, (x1, y1), rd, 2)
            elif mode == 'square':
                side = max(abs(x1 - x2), abs(y1 - y2))
                r = pygame.Rect(min(x1, x2), min(y1, y2), side, side)
                pygame.draw.rect(surf, col, r, 2)
            elif mode == 'right_tri':
                pygame.draw.polygon(surf, col, [(x1, y1), (x1, y2), (x2, y2)], 2)
            elif mode == 'equi_tri':
                side = x2 - x1
                h = int(side * math.sqrt(3) / 2)
                pygame.draw.polygon(surf, col, [(x1, y1), (x2, y1), ((x1 + x2) // 2, y1 - h)], 2)
            elif mode == 'rhombus':
                mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
                pygame.draw.polygon(surf, col, [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)], 2)

        for p in points:
            if p[0] == 'pen': pygame.draw.circle(screen, p[2], p[1], 5)
            elif p[0] == 'eraser': pygame.draw.circle(screen, (0, 0, 0), p[1], 20)
            else: draw_shape(p[0], p[1], p[2], p[3], screen)

        if start_pos:
            draw_shape(drawing_mode, start_pos, pygame.mouse.get_pos(), color, screen)

        pygame.display.flip()
        clock.tick(60)

main()