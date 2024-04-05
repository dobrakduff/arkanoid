import random
import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60

PADDLE_W = 300
PADDLE_H = 35
PADDLE_SPEED = 15

BALL_RADIUS = 20
BALL_SPEED = 5
BALL_RECT = int(BALL_RADIUS * 2 ** 0.5)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

paddle = pygame.Rect(WIDTH // 2 - PADDLE_W // 2, HEIGHT - PADDLE_H - 10, PADDLE_W, PADDLE_H)
ball = pygame.Rect(random.randrange(BALL_RECT, WIDTH - BALL_RECT), HEIGHT // 2, BALL_RECT, BALL_RECT)
dx, dy = 1, -1

block_list = [pygame.Rect(50 + 120 * i, 20 + 70 * j, 100, 50) for i in range(6) for j in range(4)]


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((0, 0, 0))

    for block in block_list:
        pygame.draw.rect(screen, pygame.Color('white'), block)

    pygame.draw.rect(screen, pygame.Color('pink'), paddle)
    pygame.draw.circle(screen, pygame.Color('orange'), ball.center, BALL_RADIUS)

    ball.x += BALL_SPEED * dx
    ball.y += BALL_SPEED * dy

    if ball.centerx < BALL_RADIUS or ball.centerx > WIDTH - BALL_RADIUS:
        dx = -dx
    if ball.centery < BALL_RADIUS:
        dy = -dy
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)

    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)

    if ball.bottom > HEIGHT:
        print('GAME OVER!')
        pygame.quit()
        exit()
    elif not len(block_list):
        print('WIN!!!')
        pygame.quit()
        exit()

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= PADDLE_SPEED
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += PADDLE_SPEED

    pygame.display.flip()
    clock.tick(FPS)
