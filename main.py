import pygame, sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1280
screen_height = 960

# Colors
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)
blue = (0, 0, 255)
red = (255, 0, 0)

# Screen setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PingPongDD')

# Game objects
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# Load and scale ball image
try:
    ball_image = pygame.image.load('HEIC TO PNG Image.png')
    ball_image = pygame.transform.scale(ball_image, (30, 30))
except pygame.error as e:
    print(f"Unable to load image: {e}")
    pygame.quit()
    sys.exit()

# Load sounds
pygame.mixer.init()
try:
    collision_sound = pygame.mixer.Sound('28_1 3.mp3')
    score_sound = pygame.mixer.Sound('M4A to MP3 28 1 4.mp3')
except pygame.error as e:
    print(f"Unable to load sound: {e}")
    collision_sound = None
    score_sound = None

# Speeds
ball_speed_x = 7 * (-1 if pygame.time.get_ticks() % 2 == 0 else 1)
ball_speed_y = 7 * (-1 if pygame.time.get_ticks() % 2 == 0 else 1)
player_speed = 0
opponent_speed = 7
ball_speed_increment = 0.1

# Scores
player_score = 0
opponent_score = 0
winning_score = 10
font = pygame.font.Font(None, 74)

# Clock
clock = pygame.time.Clock()

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x = 7 * (-1 if pygame.time.get_ticks() % 2 == 0 else 1)
    ball_speed_y = 7 * (-1 if pygame.time.get_ticks() % 2 == 0 else 1)
    pygame.time.wait(1000)  # Add a 1-second delay

def handle_events():
    global player_speed
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                player_speed += 7
            if event.key == K_UP:
                player_speed -= 7
        if event.type == KEYUP:
            if event.key == K_DOWN:
                player_speed -= 7
            if event.key == K_UP:
                player_speed += 7

def move_ball():
    global ball_speed_x, ball_speed_y, player_score, opponent_score
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
        if collision_sound:
            collision_sound.play()
    if ball.left <= 0:
        player_score += 1
        if score_sound:
            score_sound.play()
        reset_ball()
    if ball.right >= screen_width:
        opponent_score += 1
        if score_sound:
            score_sound.play()
        reset_ball()

def move_player():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def move_opponent():
    if opponent.centery < ball.centery:
        opponent.y += opponent_speed
    if opponent.centery > ball.centery:
        opponent.y -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def check_collisions():
    global ball_speed_x, ball_speed_y
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
        ball_speed_x += ball_speed_increment if ball_speed_x > 0 else -ball_speed_increment
        ball_speed_y += ball_speed_increment if ball_speed_y > 0 else -ball_speed_increment
        if collision_sound:
            collision_sound.play()

def draw_objects():
    screen.fill(bg_color)
    pygame.draw.rect(screen, blue, player)
    pygame.draw.rect(screen, red, opponent)
    screen.blit(ball_image, ball.topleft)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

def display_scores():
    player_text = font.render(str(player_score), True, light_grey)
    screen.blit(player_text, (screen_width / 2 + 20, 20))
    opponent_text = font.render(str(opponent_score), True, light_grey)
    screen.blit(opponent_text, (screen_width / 2 - 60, 20))

def check_winner():
    if player_score >= winning_score:
        winner_text = font.render("Player Wins!", True, light_grey)
        screen.blit(winner_text, (screen_width / 2 - 200, screen_height / 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()
    elif opponent_score >= winning_score:
        winner_text = font.render("Opponent Wins!", True, light_grey)
        screen.blit(winner_text, (screen_width / 2 - 200, screen_height / 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

# Main game loop
while True:
    handle_events()
    move_ball()
    move_player()
    move_opponent()
    check_collisions()
    draw_objects()
    display_scores()
    check_winner()
    pygame.display.flip()
    clock.tick(60)