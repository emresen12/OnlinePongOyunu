import pygame
import sys



# Pygame başlat
pygame.init()

# Tam ekran mod
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = SCREEN.get_size()
pygame.display.set_caption("Pong - Glow Border Edition")

# Renkler
WHITE = (255, 255, 255)
BLACK = (10, 10, 30)

LEFT_PADDLE_COLOR = (243, 6, 6)
RIGHT_PADDLE_COLOR = (243, 6, 6)
LEFT_GLOW = (255, 0, 0)
RIGHT_GLOW = (255, 0, 0)
BORDER_COLOR = (0, 0, 255)

# FPS kontrolü
clock = pygame.time.Clock()
FPS = 60

# Raket boyutu ve hızı
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 10

# Top boyutu ve hızı
BALL_SIZE = 20
BALL_SPEED_X = 10
BALL_SPEED_Y = 10

# Raket pozisyonları
left_paddle = pygame.Rect(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 20, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Top pozisyonu
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Skorlar
left_score = 0
right_score = 0
font = pygame.font.SysFont("Arial", 36)

def reset_ball():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.center = (WIDTH//2, HEIGHT//2)
    BALL_SPEED_X *= -1
    BALL_SPEED_Y *= -1

def draw_glow_rect(surface, rect, color):
    for i in range(6, 0, -1):
        glow_rect = rect.inflate(i * 4, i * 4)
        alpha = max(20, 255 - i * 40)
        glow_surf = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        glow_surf.fill((*color, alpha))
        surface.blit(glow_surf, glow_rect.topleft)
    pygame.draw.rect(surface, color, rect)

def draw_glow_paddle(surface, rect, color, glow_color):
    draw_glow_rect(surface, rect, glow_color)
    pygame.draw.rect(surface, color, rect)

def draw_glow_border(surface, color, thickness=4):
    pygame.draw.rect(surface, color, pygame.Rect(0, 0, WIDTH, thickness))  # üst
    pygame.draw.rect(surface, color, pygame.Rect(0, HEIGHT - thickness, WIDTH, thickness))  # alt
    pygame.draw.rect(surface, color, pygame.Rect(0, 0, thickness, HEIGHT))  # sol
    pygame.draw.rect(surface, color, pygame.Rect(WIDTH - thickness, 0, thickness, HEIGHT))  # sağ

    for y in range(0, HEIGHT, 40):
        pygame.draw.rect(surface, color, pygame.Rect(WIDTH//2 - 2, y, 4, 20))

# Oyun döngüsü
running = True
while running:
    clock.tick(FPS)

    # Olaylar
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC ile çık
                running = False

    # Tuşlar
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED

    # Top hareketi
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # Üst-alt sınırlar
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y *= -1

    # Raket çarpışmaları
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        BALL_SPEED_X *= -1

    # Skor kontrolü
    if ball.left <= 0:
        right_score += 1
        reset_ball()
    if ball.right >= WIDTH:
        left_score += 1
        reset_ball()

    # Ekranı temizle
    SCREEN.fill(BLACK)

    draw_glow_border(SCREEN, BORDER_COLOR)
    draw_glow_paddle(SCREEN, left_paddle, LEFT_PADDLE_COLOR, LEFT_GLOW)
    draw_glow_paddle(SCREEN, right_paddle, RIGHT_PADDLE_COLOR, RIGHT_GLOW)
    pygame.draw.ellipse(SCREEN, (255, 255, 0), ball)

    left_text = font.render(f"{left_score}", True, WHITE)
    right_text = font.render(f"{right_score}", True, WHITE)
    SCREEN.blit(left_text, (WIDTH//4, 20))
    SCREEN.blit(right_text, (WIDTH * 3//4, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
