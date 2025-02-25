import sys
import pygame
import random

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Screen dimensions
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Color Selection Game")

# Fonts
normal_font = pygame.font.Font(None, 74)
big_font = pygame.font.Font(None, 96)
button_font = pygame.font.Font(None, 50)
score_font = pygame.font.Font(None, 50)

# Game variables
num_choices = 2 # Customizable number of choices
min_num_choices = 1 # Minimum number of choices
max_num_choices = 5 # Maximum number of choices
square_size = WIDTH // max_num_choices - 10  # Square size based on max number of choices

# test button class
class button:
    def __init__(self, x, y, text, width=200, height=50, color="darkgreen"):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.text = button_font.render(text, True, (255, 255, 255))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, (self.x + 20, self.y + 10))

# Load sound effects
pygame.mixer.init()
title_sound = pygame.mixer.Sound("assets/title.wav")    
select_sound = pygame.mixer.Sound("assets/select.wav")  
well_done_sound = pygame.mixer.Sound("assets/well_done.wav")
click_sound = pygame.mixer.Sound("assets/mouse_click.wav")
right_sounds = [
    # pygame.mixer.Sound("assets/correct.wav"),
    pygame.mixer.Sound("assets/excellent.wav"),
    pygame.mixer.Sound("assets/good.wav"),
    pygame.mixer.Sound("assets/great.wav"),
    # pygame.mixer.Sound("assets/right.wav"),
    pygame.mixer.Sound("assets/verygood.wav"),
    pygame.mixer.Sound("assets/yes.wav")
    ]
wrong_sounds = [
    pygame.mixer.Sound("assets/bad.wav"),
    pygame.mixer.Sound("assets/no.wav"),
    pygame.mixer.Sound("assets/nogood.wav"),
    pygame.mixer.Sound("assets/notgood.wav"),
    pygame.mixer.Sound("assets/wrong.wav")
    ]

# Emojis
happy_face = pygame.image.load("assets/happy_face.png") 
sad_face = pygame.image.load("assets/red_sad_face.png")     
happy_face = pygame.transform.scale(happy_face, (200, 200))  
sad_face = pygame.transform.scale(sad_face, (200, 200))      

# Main game variable, color items
color_items = {}
color_items = {
    "black": { 
        "value" : (0, 0, 0),
        "sound" : pygame.mixer.Sound("assets/black.wav"),
        "toggle" : True
    },
    "white": { 
        "value" : (255, 255, 255),
        "sound" : pygame.mixer.Sound("assets/white.wav"),
        "toggle" : True
    },
    "red": { 
        "value" : (255, 0, 0),
        "sound" : pygame.mixer.Sound("assets/red.wav"),
        "toggle" : False
    },
    "green": { 
        "value" : (0, 255, 0),
        "sound" : pygame.mixer.Sound("assets/green.wav"),
        "toggle" : False
    },
    "blue": { 
        "value" : (0, 0, 255),
        "sound" : pygame.mixer.Sound("assets/blue.wav"),
        "toggle" : False
    },
    "yellow": { 
        "value" : (255, 255, 0),
        "sound" : pygame.mixer.Sound("assets/yellow.wav"),
        "toggle" : False
    },
    "purple": { 
        "value" : (128, 0, 128),
        "sound" : pygame.mixer.Sound("assets/purple.wav"),
        "toggle" : False
    },
    "pink": { 
        "value" : (255, 182, 193),
        "sound" : pygame.mixer.Sound("assets/pink.wav"),
        "toggle" : False
    }
}

COLOR_NAMES = list(color_items.keys())

def options_screen():
    global num_choices, toggles, force_correct_color

    # Option 2: Generate checkboxes
    opt_rect = {}
    force_opt_rect = {}
    opt_size = 50
    i = 0
    for acolor in COLOR_NAMES:
        opt_rect[acolor] = pygame.Rect((WIDTH - opt_size * 1.25 * len(COLOR_NAMES)) // 2 + (i * opt_size * 1.25), HEIGHT * 2 // 5, opt_size, opt_size)
        force_opt_rect[acolor] = pygame.Rect((WIDTH - opt_size * 1.25 * len(COLOR_NAMES)) // 2 + (i * opt_size * 1.25), HEIGHT * 3 // 5, opt_size, opt_size)
        i += 1

    # Event handling for options screen
    waiting = True
    while waiting:
        screen.fill((128, 128, 128))  # Grey background

        # Section 0: Options title
        title_text = normal_font.render("Options", True, (0, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        # Section 1. Option for number of choices
        choices_text = button_font.render(f"Number of choices: ", True, "white")
        screen.blit(choices_text, (WIDTH // 2 - choices_text.get_width() // 2, HEIGHT * 1 // 5 - 50))
        num_choices_text = button_font.render(f"{num_choices}", True, "darkred")
        screen.blit(num_choices_text, (WIDTH // 2 - num_choices_text.get_width() // 2, HEIGHT * 1 // 5))

        # Draw "+" button
        plus_button = button(WIDTH // 2 - 25 + 50, HEIGHT * 1 // 5, "+", 50, 50, "darkred")
        plus_button.draw()
        # Draw "-" button
        minus_button = button(WIDTH // 2 - 25 - 50, HEIGHT * 1 // 5, "-", 50, 50, "darkred")
        minus_button.draw()

        # Section 2. Option for available colors
        choices_text = button_font.render("Available colors: ", True, "white")
        screen.blit(choices_text, (WIDTH // 2 - choices_text.get_width() // 2, HEIGHT * 2 // 5 - 50))
        # Draw option checkboxes
        for acolor in COLOR_NAMES:
            pygame.draw.rect(screen, acolor, opt_rect[acolor], 4)
            if color_items[acolor]["toggle"]:
                # draw smaller box
                pygame.draw.rect(screen, acolor, opt_rect[acolor].inflate(-10, -10))
            pygame.draw.rect(screen, acolor, force_opt_rect[acolor], 4)
            if force_correct_color == acolor:
                # draw smaller box
                pygame.draw.rect(screen, acolor, force_opt_rect[acolor].inflate(-10, -10))

        # Section 3: Option to force only 1 possible right color
        only_choice_text = button_font.render("Only find color: ", True, "white")
        screen.blit(only_choice_text, (WIDTH // 2 - only_choice_text.get_width() // 2, HEIGHT * 3 // 5 - 50))

        # Section 4: Draw "OK" button
        ok_button = button(WIDTH // 2 - 100, HEIGHT * 4 // 5, "OK", 200, 50, "darkgreen")
        ok_button.draw()

        # Section 5: Draw "Quit" button
        quit_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Return to the title screen
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if plus_button.rect.collidepoint(x, y):
                    # Increase the number of choices
                    click_sound.play()
                    num_choices = min(num_choices + 1, max_num_choices)
                if minus_button.rect.collidepoint(x, y):
                    # Decrease the number of choices
                    click_sound.play()
                    num_choices = max(num_choices - 1, min_num_choices)
                for acolor in COLOR_NAMES:
                    if opt_rect[acolor].collidepoint(x, y):
                        click_sound.play()
                        color_items[acolor]["toggle"] = not color_items[acolor]["toggle"]
                        num_available_colors = sum(1 for item in color_items.values() if item["toggle"])
                        if num_available_colors < num_choices:
                            color_items[acolor]["toggle"] = not color_items[acolor]["toggle"]
                        if not color_items[acolor]["toggle"] and force_correct_color == acolor:
                            force_correct_color = None
                    if force_opt_rect[acolor].collidepoint(x, y):
                        click_sound.play()
                        if force_correct_color == acolor:
                            force_correct_color = None
                        elif color_items[acolor]["toggle"]:
                            force_correct_color = acolor
                if ok_button.rect.collidepoint(x, y):
                    # Return to the title screen
                    click_sound.play()
                    return
                if quit_button.rect.collidepoint(x, y):
                    # Quit the game
                    click_sound.play()
                    pygame.time.wait(500)
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()
        clock.tick(30)
#
def title_screen():
    global running
    waiting = True
    while waiting:
        # Display the title screen
        screen.fill((128, 128, 128))
        title_text = normal_font.render("Color Selection Game", True, (0, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
        start_button = button(WIDTH // 2 - 100, HEIGHT // 2 + 50, "Start", 200, 50)
        start_button.draw()
        option_button = button(WIDTH // 2 - 100, HEIGHT // 2 + 50 + 75, "Options", 200, 50)
        option_button.draw()
        quit_button = button(WIDTH // 2 - 100, HEIGHT // 2 + 50 + 150, "Quit", 200, 50, "darkred")
        quit_button.draw()
        pygame.display.flip()

        # Event handling for title screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_button.rect.collidepoint(x, y):
                    # Proceed to the next round
                    click_sound.play()
                    return True
                if option_button.rect.collidepoint(x, y):
                    # Switch to options screen
                    click_sound.play()
                    options_screen()
                if quit_button.rect.collidepoint(x, y):
                    click_sound.play()
                    pygame.quit()
                    sys.exit()
        clock.tick(30)
# 
def draw_screen():
    global correct_color, square_colors, square_positions, result, show_next_button, new_round, highlight_x, highlight_y
    screen.fill((128, 128, 128))  # Grey background

    # Display the score
    score_text = score_font.render(f"Question {question_num + 1: >2}", True, (0, 0, 0))
    screen.blit(score_text, (20, 20))

    # Display the color name to select
    game_text = normal_font.render(f"Find {correct_color.capitalize()}", True, "black")
    game_rect = pygame.Rect(WIDTH // 2 - game_text.get_width() // 2 - 2, 50 - 2, game_text.get_width() + 4, game_text.get_height() + 4)
    pygame.draw.rect(screen, "gold", game_rect.inflate(0, 0))
    screen.blit(game_text, (WIDTH // 2 - game_text.get_width() // 2, 50))

    # Draw the squares
    for i, pos in enumerate(square_positions):
        pygame.draw.rect(screen, color_items[square_colors[i]]["value"], (*pos, square_size, square_size))

    # Display result
    if result is not None:
        pygame.draw.rect(screen, "brown", (highlight_x - 10, highlight_y - 10, square_size + 20, square_size + 20),5)    
        result_text = big_font.render(result, True, pygame.Color("green" if result == "RIGHT !" else "red"))
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT - HEIGHT // 9))
        # Display emoji based on result
        if result == "RIGHT !":
            screen.blit(happy_face, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
        else:
            screen.blit(sad_face, (WIDTH // 2 - 100, HEIGHT // 2 + 50))

    # Draw the "Next" button if the round is over
    if show_next_button and not game_over:
        next_button.draw()

    # Draw the "Quit" button
    if not game_over:
        quit_button.draw()

    # Update the display
    pygame.display.flip()

    # Play sounds
    # if not show_next_button:
    if new_round:
        new_round = False
        pygame.time.delay(250)  # Delay for 1 second
        title_sound.play()  # Play title sound at the beginning of each round
        pygame.time.delay(500)
        color_items[correct_color]["sound"].play()  # Play correct color sound at the title screen
    return game_rect

# Function to generate square positions dynamically
def generate_square_positions(num_choices):
    positions = []
    # Dynamic layout for numbers of choices
    spacing = WIDTH // num_choices - square_size
    total_width = num_choices * square_size + (num_choices - 1) * spacing
    start_x = (WIDTH - total_width) // 2
    start_y = HEIGHT // 2 - square_size
    for i in range(num_choices):
        x = start_x + i * (square_size + spacing)
        y = start_y
        positions.append((x, y))
    return positions

# Function to generate squares with only one correct choice
def generate_squares(num_choices):
    really_available_colors = [c for c in COLOR_NAMES if color_items[c]["toggle"]]
    if force_correct_color:
        correct_color = force_correct_color
    else:
        correct_color = random.choice(really_available_colors)
    # Ensure the correct color is only present once
    incorrect_colors = random.sample([c for c in really_available_colors if c != correct_color], num_choices - 1)  # Pick incorrect colors
    square_colors = incorrect_colors + [correct_color]  # Combine incorrect and correct colors
    random.shuffle(square_colors)  # Shuffle to randomize positions
    return correct_color, square_colors

# Button definitions
next_button = button(WIDTH - 200 - 20, HEIGHT - 50 - 20, "Next", 200, 50)
quit_button = button(WIDTH - 200 - 20, 20, "Quit", 200, 50, "darkred")
new_game_button = button(WIDTH // 2 - 200 - 10, HEIGHT // 2 + 50, "New Game", 200, 50)
exit_game_button = button(WIDTH // 2 + 10, HEIGHT // 2 + 50, "Exit Game", 200, 50, "darkred")

# new game variables
question_num = 0
real_score = 0
target_question_num = 10
wrong_answer = False
force_correct_color = None
game_over = False
new_round = True

# title_screen()
options_screen()

# Main game loop
running = True
result = None
show_next_button = False
highlight_x, highlight_y = 0, 0

# Initialize the first question
square_positions = generate_square_positions(num_choices)
correct_color, square_colors = generate_squares(num_choices)

# Clear any lingering events
pygame.event.clear()  

while running:
    clock.tick(60)
    draw_screen()
    if game_over:
        # Display the game over screen
        pygame.time.delay(1000)
        screen.fill((128, 128, 128))
        # Display the final score
        final_score_text = score_font.render(f"Final Score: {round(real_score / 10 * 100)} %", True, pygame.Color("black"))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT * 1 // 5))
        # Display the well done message
        well_done_text = normal_font.render("Well Done!", True, pygame.color.Color("gold"))
        screen.blit(well_done_text, (WIDTH // 2 - well_done_text.get_width() // 2, HEIGHT // 2 - 50))
        well_done_sound.play()
        new_game_button.draw()
        exit_game_button.draw()
        pygame.display.flip()

        # Event handling for game over screen
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if new_game_button.rect.collidepoint(x, y):
                        # Reset the game
                        click_sound.play()
                        result = None
                        question_num = 0
                        real_score = 0
                        game_over = False
                        options_screen()
                        correct_color, square_colors = generate_squares(num_choices)
                        show_next_button = False
                        waiting = False
                    elif exit_game_button.rect.collidepoint(x, y):
                        click_sound.play()
                        running = False  # Exit the game
                        waiting = False
        continue

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # click next button to proceed to the next round
            if show_next_button and next_button.rect.collidepoint(x, y):
                # Proceed to the next round
                click_sound.play()
                show_next_button = False
                wrong_answer = False
                result = None
                correct_color, square_colors = generate_squares(num_choices)
                new_round = True
            # click quit button to exit the game
            elif quit_button.rect.collidepoint(x, y):
                click_sound.play()
                running = False  # Quit the game
            # click on the squares to select the color
            elif not show_next_button:
                for i, pos in enumerate(square_positions):
                    if pos[0] <= x <= pos[0] + square_size and pos[1] <= y <= pos[1] + square_size:
                        # set highlight pos for draw_screen()
                        highlight_x, highlight_y = pos
                        if square_colors[i] == correct_color:
                            result = "RIGHT !"
                            random.choice(right_sounds).play()
                            show_next_button = True
                            question_num += 1  # Increase score
                            if not wrong_answer:
                                real_score += 1 
                            if question_num >= target_question_num:
                                game_over = True
                            else:
                                next_button.draw()
                            pygame.display.flip()
                        else:
                            result = "WRONG !"
                            random.choice(wrong_sounds).play()
                            show_next_button = False
                            wrong_answer = True
                        break
    clock.tick(30)

# Quit pygame
pygame.quit()
