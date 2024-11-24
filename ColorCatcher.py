import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game settings
FPS = 60
BASKET_WIDTH = 100
BASKET_HEIGHT = 20
BASKET_COLOR = BLACK
OBJECT_COLORS = [RED, GREEN, BLUE, YELLOW]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Color Catcher")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Game variables
basket_x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
basket_y = SCREEN_HEIGHT - BASKET_HEIGHT - 10
basket_speed = 10
score = 0
target_color = random.choice(OBJECT_COLORS)
falling_objects = []
falling_speed = 4
missed_objects = 0
MAX_MISSED = 10  # Max missed objects before game over
WINNING_SCORE = 50  # Score required to win

# Create a falling object
def create_falling_object():
    x = random.randint(0, SCREEN_WIDTH - 30)
    y = -30
    color = random.choice(OBJECT_COLORS)
    return {"x": x, "y": y, "color": color}

# Draw the basket
def draw_basket(x, y):
    pygame.draw.rect(screen, BASKET_COLOR, (x, y, BASKET_WIDTH, BASKET_HEIGHT))

# Draw a falling object
def draw_object(obj):
    pygame.draw.circle(screen, obj["color"], (obj["x"], obj["y"]), 15)

# Display score and target color
def display_info():
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    target_text = font.render("Catch This Color:", True, BLACK)
    screen.blit(target_text, (10, 40))

    pygame.draw.circle(screen, target_color, (150, 50), 15)

# Pause the game for win or game-over screens
def display_end_screen(message, color):
    screen.fill(WHITE)
    end_text = font.render(message, True, color)
    restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)
    screen.blit(end_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    return "restart"
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    sys.exit()

# Main game loop
def main():
    global basket_x, score, target_color, missed_objects, falling_objects, falling_speed

    # Reset game variables
    basket_x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
    score = 0
    target_color = random.choice(OBJECT_COLORS)
    falling_objects = []
    missed_objects = 0
    falling_speed = 4  # Reset falling speed

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move basket with keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - BASKET_WIDTH:
            basket_x += basket_speed

        # Add new falling objects
        if random.randint(1, 40) == 1:  # Spawn objects less frequently
            falling_objects.append(create_falling_object())

        # Update falling objects
        for obj in falling_objects[:]:
            obj["y"] += falling_speed
            # Check for collision with basket
            if (
                basket_y < obj["y"] + 15 < basket_y + BASKET_HEIGHT
                and basket_x < obj["x"] < basket_x + BASKET_WIDTH
            ):
                if obj["color"] == target_color:
                    score += 10
                else:
                    score -= 5
                falling_objects.remove(obj)
            # Remove objects that fall off the screen
            elif obj["y"] > SCREEN_HEIGHT:
                if obj["color"] == target_color:  # Only increment missed_objects for target color
                    missed_objects += 1
                falling_objects.remove(obj)

        # Winning condition
        if score >= WINNING_SCORE:
            result = display_end_screen("You Win!", GREEN)
            if result == "restart":
                main()  # Restart the game

        # Game over condition
        if missed_objects >= MAX_MISSED:
            result = display_end_screen("Game Over!", RED)
            if result == "restart":
                main()  # Restart the game

        # Draw everything
        draw_basket(basket_x, basket_y)
        for obj in falling_objects:
            draw_object(obj)
        display_info()

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
