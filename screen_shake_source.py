
#using this implement screen shake when health==1 in game
import pygame
import random
import sys

# 1. Initialize Pygame and Setup Window
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Screen Shake Example")
clock = pygame.time.Clock()

# 2. Create the Render Buffer
# All game elements are drawn on this surface first
game_buffer = pygame.Surface((WIDTH, HEIGHT))

# Screen Shake Variables
shake_timer = 0
shake_intensity = 0

def trigger_shake(duration, intensity):
    global shake_timer, shake_intensity
    shake_timer = duration      # Number of frames the shake lasts
    shake_intensity = intensity  # Maximum pixel offset

# Game Loop
running = True
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Trigger a shake for 20 frames with an 8-pixel max offset
                trigger_shake(20, 10)

    # 3. Draw Game Elements onto the BUFFER (Not the main screen)
    game_buffer.fill((30, 30, 40))  # Background color
    
    # Draw a test object (a centered square) to visualize the shake
    pygame.draw.rect(game_buffer, (255, 100, 100), (WIDTH//2 - 50, HEIGHT//2 - 50, 100, 100))

    # 4. Process Screen Shake Logic
    offset_x = 0
    offset_y = 0
    
    if shake_timer > 0:
        # Pick a random offset within the intensity range
        offset_x = random.randint(-shake_intensity, shake_intensity)
        offset_y = random.randint(-shake_intensity, shake_intensity)
        shake_timer -= 1  # Countdown the timer

    # 5. Clear Main Screen and Blit Buffer with the Offset
    screen.fill((0, 0, 0))  # Clears any artifacts left behind by the shift
    screen.blit(game_buffer, (offset_x, offset_y))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
