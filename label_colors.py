import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Selection Game")

# Colors
COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128),
    "orange": (255, 165, 0),
}
COLOR_NAMES = list(COLORS.keys())

# Fonts
font = pygame.font.Font(None, 74)

# Sound effects
pygame.mixer.init()
correct_sound = pygame.mixer.Sound("correct.wav")  # Replace with your correct sound file
wrong_sound = pygame.mixer.Sound("wrong.wav")      # Replace with your wrong sound file

# Game variables
square_size = 100
num_choices = 4  # Customizable number of choices

# Function to generate square positions dynamically
def generate_square_positions(num_choices):
    positions = []
    if num_choices == 4:
        # Default layout for 4 choices
        positions = [
            (WIDTH // 4 - square_size // 2, HEIGHT // 2 - square_size // 2),
            (3 * WIDTH // 4 - square_size // 2, HEIGHT // 2 - square_size // 2),
            (WIDTH // 4 - square_size // 2, 3 * HEIGHT // 4 - square_size // 2),
            (3 * WIDTH // 4 - square_size // 2, 3 * HEIGHT // 4 - square_size // 2),
        ]
    else:
        # Dynamic layout for other numbers of choices
        spacing = 20  # Space between squares
        total_width = num_choices * square_size + (num_choices - 1) * spacing
        start_x = (WIDTH - total_width) // 2
        start_y = HEIGHT // 2 - square_size // 2
        for i in range(num_choices):
            x = start_x + i * (square_size + spacing)
            y = start_y
            positions.append((x, y))
    return positions

# Function to generate squares with only one correct choice
def generate_squares(num_choices, previous_color=None):
    # Ensure the new correct color is different from the previous one
    if previous_color:
        available_colors = [c for c in COLOR_NAMES if c != previous_color]
        correct_color = random.choice(available_colors)
    else:
        correct_color = random.choice(COLOR_NAMES)
    
    # Ensure the correct color is only present once
    incorrect_colors = random.sample([c for c in COLOR_NAMES if c != correct_color], num_choices - 1)  # Pick incorrect colors
    square_colors = incorrect_colors + [correct_color]  # Combine incorrect and correct colors
    random.shuffle(square_colors)  # Shuffle to randomize positions
    return correct_color, square_colors

# Initialize the first question
previous_color = None
square_positions = generate_square_positions(num_choices)
correct_color, square_colors = generate_squares(num_choices, previous_color)

# Main game loop
running = True
result = None
while running:
    screen.fill((255, 255, 255))  # White background

    # Display the color name to select
    text = font.render(f"Select {correct_color}", True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

    # Draw the squares
    for i, pos in enumerate(square_positions):
        pygame.draw.rect(screen, COLORS[square_colors[i]], (*pos, square_size, square_size))

    # Display result
    if result is not None:
        result_text = font.render(result, True, (0, 0, 0))
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT - 100))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i, pos in enumerate(square_positions):
                if pos[0] <= x <= pos[0] + square_size and pos[1] <= y <= pos[1] + square_size:
                    if square_colors[i] == correct_color:
                        result = "Correct!"
                        correct_sound.play()  # Play correct sound effect
                        # Generate a new question, ensuring the new color is different from the previous one
                        previous_color = correct_color
                        correct_color, square_colors = generate_squares(num_choices, previous_color)
                    else:
                        result = "Wrong!"
                        wrong_sound.play()  # Play wrong sound effect
                    break

    pygame.display.flip()

# Quit pygame
pygame.quit()