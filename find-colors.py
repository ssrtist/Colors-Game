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
    "black": (0, 0, 0),
    "white": (255, 255, 255),
}
COLOR_NAMES = list(COLORS.keys())

# Fonts
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Sound effects
pygame.mixer.init()
sounds = {}
title_sound = pygame.mixer.Sound("assets/title.wav")      # Replace with your title sound file
select_sound = pygame.mixer.Sound("assets/select.wav")      # Replace with your wrong sound file
correct_sound = pygame.mixer.Sound("assets/right.wav")  # Replace with your correct sound file
wrong_sound = pygame.mixer.Sound("assets/wrong.wav")      # Replace with your wrong sound file
sounds["red"] = pygame.mixer.Sound("assets/red.wav")          # Replace with your red sound file
sounds["green"] = pygame.mixer.Sound("assets/green.wav")      # Replace with your green sound file
sounds["blue"] = pygame.mixer.Sound("assets/blue.wav")        # Replace with your blue sound file
sounds["yellow"] = pygame.mixer.Sound("assets/yellow.wav")    # Replace with your yellow sound file
sounds["purple"] = pygame.mixer.Sound("assets/purple.wav")    # Replace with your purple sound file
sounds["orange"] = pygame.mixer.Sound("assets/orange.wav")    # Replace with your orange sound file
sounds["black"] = pygame.mixer.Sound("assets/black.wav")      # Replace with your black sound file
sounds["white"] = pygame.mixer.Sound("assets/white.wav")      # Replace with your white sound file

# Emojis
happy_face = pygame.image.load("assets/happy_face.png")  # Replace with your happy face image
sad_face = pygame.image.load("assets/sad_face.png")      # Replace with your sad face image
happy_face = pygame.transform.scale(happy_face, (200, 200))  # Resize if needed
sad_face = pygame.transform.scale(sad_face, (200, 200))      # Resize if needed

# Game variables
square_size = 100
num_choices = 2  # Customizable number of choices

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

# 
def draw_screen():
#def draw_screen():
    global correct_color, square_colors, square_positions, result, show_next_button
    screen.fill((128, 128, 128))  # Grey background

    # Display the color name to select
    text = font.render(f"Find {correct_color.capitalize()}", True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

    # Draw the squares
    for i, pos in enumerate(square_positions):
        pygame.draw.rect(screen, COLORS[square_colors[i]], (*pos, square_size, square_size))

    # Display result
    if result is not None:
        result_text = font.render(result, True, pygame.Color("green" if result == "Right!" else "red"))
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT - 50))
        show_next_button = True
        # Display emoji based on result
        if result == "Right!":
            screen.blit(happy_face, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
        else:
            screen.blit(sad_face, (WIDTH // 2 - 100, HEIGHT // 2 + 50))

    # Draw the "Next" button if the round is over
    if show_next_button:
        pygame.draw.rect(screen, (0, 128, 0), next_button_rect)  # Green button
        screen.blit(next_button_text, (next_button_x + 20, next_button_y + 10))

    # Draw the "Quit" button
    pygame.draw.rect(screen, (255, 0, 0), quit_button_rect)  # Red button
    screen.blit(quit_button_text, (quit_button_x + 20, quit_button_y + 10))


# Initialize the first question
previous_color = None
square_positions = generate_square_positions(num_choices)
correct_color, square_colors = generate_squares(num_choices, previous_color)

# Button variables
button_width, button_height = 150, 50

# "Next" button
next_button_x = WIDTH - button_width - 20
next_button_y = HEIGHT - button_height - 20
next_button_rect = pygame.Rect(next_button_x, next_button_y, button_width, button_height)
next_button_text = button_font.render("Next", True, (255, 255, 255))

# "Quit" button
quit_button_x = WIDTH - button_width - 20
quit_button_y = 20
quit_button_rect = pygame.Rect(quit_button_x, quit_button_y, button_width, button_height)
quit_button_text = button_font.render("Quit", True, (255, 255, 255))

# Main game loop
running = True
result = None
show_next_button = False
# Play title sound at the beginning of the game
draw_screen()
pygame.display.flip()
title_sound.play()
pygame.time.delay(1000)  # Delay for 1 second
sounds[correct_color].play()  # Play correct color sound at the title screen
pygame.time.delay(1000)  # Delay for 2 seconds
pygame.event.clear()  # Clear any lingering events

while running:
    draw_screen()
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if show_next_button and next_button_rect.collidepoint(x, y):
                # Proceed to the next round
                show_next_button = False
                result = None
                previous_color = correct_color
                correct_color, square_colors = generate_squares(num_choices, previous_color)
                screen.fill((128, 128, 128))  # Grey background
                draw_screen()
                pygame.display.flip()
                title_sound.play()  # Play title sound at the beginning of each round
                pygame.time.delay(1000)  # Delay for 1 second
                sounds[correct_color].play()  # Play correct color sound at the title screen
                pygame.time.delay(1000)  # Delay for 1 second
            elif quit_button_rect.collidepoint(x, y):
                running = False  # Quit the game
            else:
                for i, pos in enumerate(square_positions):
                    if pos[0] <= x <= pos[0] + square_size and pos[1] <= y <= pos[1] + square_size:
                        if square_colors[i] == correct_color:
                            result = "Right!"
                            correct_sound.play()  # Play correct sound effect
                            show_next_button = True
                        else:
                            result = "Wrong!"
                            wrong_sound.play()  # Play wrong sound effect
                            show_next_button = True
                        break

    pygame.display.flip()

# Quit pygame
pygame.quit()