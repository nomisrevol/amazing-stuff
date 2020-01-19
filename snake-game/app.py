import sys
import pygame

from food import Food
from snake import Snake

WINDOW_SIZE = 500
SNAKE_SIZE = 10

window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Snake Game")
fps = pygame.time.Clock()

score = 0

snake = Snake()
food = Food()


def game_over():
    pygame.quit()
    sys.exit()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.change_direction_to("RIGHT")
            if event.key == pygame.K_LEFT:
                snake.change_direction_to("LEFT")
            if event.key == pygame.K_DOWN:
                snake.change_direction_to("DOWN")
            if event.key == pygame.K_UP:
                snake.change_direction_to("UP")
    foodPosition = food.create_food()
    if snake.move(foodPosition):
        score = score + 1
        food.set_food_on_screen(False)

    window.fill(pygame.Color(255, 255, 255))
    pygame.draw.rect(window, pygame.Color(255, 255, 0),
                     pygame.Rect(foodPosition[0], foodPosition[1], SNAKE_SIZE, SNAKE_SIZE))
    for pos in snake.get_body():
        pygame.draw.rect(window, pygame.Color(255, 255, 0), pygame.Rect(pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))
    if snake.check_collision():
        game_over()
    pygame.display.set_caption("Score: " + str(score))
    pygame.display.flip()
    fps.tick(24)
