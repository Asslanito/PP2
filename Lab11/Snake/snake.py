import pygame
import time
import random

pygame.init()

WHITE, YELLOW, BLACK, RED, GREEN = (255, 255, 255), (255, 255, 102), (0, 0, 0), (213, 50, 80), (0, 255, 0)
WIDTH, HEIGHT = 600, 400
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block = 10
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def display_info(score, level):
    value = score_font.render(f"Score: {score} Level: {level}", True, YELLOW)
    dis.blit(value, [0, 0])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [WIDTH / 6, HEIGHT / 3])


def spawn_food(snake_list):
    while True:
        fx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
        fy = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
        if [fx, fy] not in snake_list:
            weight = random.choice([1, 1, 1, 3])
            return fx, fy, weight, time.time()


def gameLoop():
    game_over = False
    game_close = False
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_c, y1_c = 0, 0
    snake_List = []
    Length_of_snake = 1
    score, level, speed = 0, 1, 15
    foodx, foody, food_w, food_time = spawn_food(snake_List)

    while not game_over:
        while game_close:
            dis.fill(BLACK)
            message("You Lost! Press C-Play Again or Q-Quit", RED)
            display_info(score, level)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: game_over = True; game_close = False
                    if event.key == pygame.K_c: gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_c == 0:
                    x1_c, y1_c = -snake_block, 0
                elif event.key == pygame.K_RIGHT and x1_c == 0:
                    x1_c, y1_c = snake_block, 0
                elif event.key == pygame.K_UP and y1_c == 0:
                    y1_c, x1_c = -snake_block, 0
                elif event.key == pygame.K_DOWN and y1_c == 0:
                    y1_c, x1_c = snake_block, 0

        if time.time() - food_time > 5:
            foodx, foody, food_w, food_time = spawn_food(snake_List)

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0: game_close = True
        x1 += x1_c
        y1 += y1_c
        dis.fill(BLACK)

        f_color = GREEN if food_w == 1 else RED
        f_size = snake_block if food_w == 1 else snake_block + 4
        pygame.draw.rect(dis, f_color, [foodx, foody, f_size, f_size])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake: del snake_List[0]
        for x in snake_List[:-1]:
            if x == snake_Head: game_close = True

        for segment in snake_List:
            pygame.draw.rect(dis, WHITE, [segment[0], segment[1], snake_block, snake_block])

        display_info(score, level)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            score += food_w
            Length_of_snake += food_w
            level = (score // 5) + 1
            speed = 15 + (level * 2)
            foodx, foody, food_w, food_time = spawn_food(snake_List)

        clock.tick(speed)
    pygame.quit()
    quit()


gameLoop()