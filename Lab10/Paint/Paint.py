import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    radius = 15
    drawing_mode = 'pen'
    color = (255, 0, 0)

    points = []
    start_pos = None

    while True:
        pressed_keys = pygame.key.get_pressed()
        alt_held = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
        ctrl_held = pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held: return
                if event.key == pygame.K_F4 and alt_held: return
                if event.key == pygame.K_r: drawing_mode = 'rect'
                if event.key == pygame.K_c: drawing_mode = 'circle'
                if event.key == pygame.K_p: drawing_mode = 'pen'
                if event.key == pygame.K_e: drawing_mode = 'eraser'
                if event.key == pygame.K_1: color = (255, 0, 0)
                if event.key == pygame.K_2: color = (0, 255, 0)
                if event.key == pygame.K_3: color = (0, 0, 255)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if drawing_mode in ['rect', 'circle']:
                    start_pos = event.pos
                else:
                    points.append(('pen' if drawing_mode == 'pen' else 'eraser', event.pos,
                                   color if drawing_mode == 'pen' else (0, 0, 0)))

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if drawing_mode in ['pen', 'eraser']:
                        points.append((drawing_mode, event.pos, color if drawing_mode == 'pen' else (0, 0, 0)))

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing_mode in ['rect', 'circle'] and start_pos:
                    points.append((drawing_mode, start_pos, event.pos, color))
                    start_pos = None

        screen.fill((0, 0, 0))

        for p in points:
            if p[0] == 'pen':
                pygame.draw.circle(screen, p[2], p[1], 5)
            elif p[0] == 'eraser':
                pygame.draw.circle(screen, (0, 0, 0), p[1], 20)
            elif p[0] == 'rect':
                x1, y1 = p[1]
                x2, y2 = p[2]
                rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))
                pygame.draw.rect(screen, p[3], rect, 2)
            elif p[0] == 'circle':
                x1, y1 = p[1]
                x2, y2 = p[2]
                r = int(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)
                pygame.draw.circle(screen, p[3], (x1, y1), r, 2)

        if start_pos:
            curr_pos = pygame.mouse.get_pos()
            if drawing_mode == 'rect':
                rect = pygame.Rect(min(start_pos[0], curr_pos[0]), min(start_pos[1], curr_pos[1]),
                                   abs(start_pos[0] - curr_pos[0]), abs(start_pos[1] - curr_pos[1]))
                pygame.draw.rect(screen, color, rect, 2)
            elif drawing_mode == 'circle':
                r = int(((start_pos[0] - curr_pos[0]) ** 2 + (start_pos[1] - curr_pos[1]) ** 2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, r, 2)

        pygame.display.flip()
        clock.tick(60)


main()