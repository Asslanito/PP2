import pygame
import math


def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    width, height = surface.get_size()
    stack = [(x, y)]
    while stack:
        curr_x, curr_y = stack.pop()
        if 0 <= curr_x < width and 0 <= curr_y < height:
            if surface.get_at((curr_x, curr_y)) == target_color:
                surface.set_at((curr_x, curr_y), new_color)
                stack.append((curr_x + 1, curr_y))
                stack.append((curr_x - 1, curr_y))
                stack.append((curr_y + 1, curr_x))  # Wait, fixed below


def flood_fill_fixed(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    width, height = surface.get_size()
    stack = [(x, y)]
    while stack:
        curr_x, curr_y = stack.pop()
        if 0 <= curr_x < width and 0 <= curr_y < height:
            if surface.get_at((curr_x, curr_y)) == target_color:
                surface.set_at((curr_x, curr_y), new_color)
                stack.append((curr_x + 1, curr_y))
                stack.append((curr_x - 1, curr_y))
                stack.append((curr_x, curr_y + 1))
                stack.append((curr_x, curr_y - 1))


def draw_rhombus(surf, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
    pygame.draw.polygon(surf, color, points, width)


def draw_right_triangle(surf, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surf, color, points, width)


def draw_equilateral_triangle(surf, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    side = abs(x2 - x1)
    height = int(side * math.sqrt(3) / 2)
    if y2 < y1: height = -height
    points = [(x1, y1), (x2, y1), ((x1 + x2) // 2, y1 + height)]
    pygame.draw.polygon(surf, color, points, width)