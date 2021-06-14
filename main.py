# Python 3.9.5

# Namespace project imports:
import colours  # My module - part of this program
import events  # My module - part of this program
import file_handling  # My module - part of this program

# Aliased namespace project imports:
import constants as c  # My module - part of this program

# Namespace imports:
import pygame
import platform

# Conditional imports:
try:
    import win32api
except ImportError:
    win32api_imported = False
    print("Could not import win32api a.k.a. pywin.")
else:
    win32api_imported = True

# Aliased imports:
from collections import namedtuple
from sys import exit
from random import randrange, choice
from time import sleep
from os import listdir
from os.path import isfile, join


def set_refresh_rate() -> int:
    try:
        device = win32api.EnumDisplayDevices()
        settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
        refresh_rate = settings.DisplayFrequency
    except NameError:
        refresh_rate = c.DEFAULT_REFRESH_RATE
        print("Defaulting to default refresh rate, as win32api a.k.a. pywin is not imported.")  # TODO remove once not needed

    return refresh_rate


def find_common_factors(number_one: int, number_two: int) -> list[int]:
    common_factors = []

    for number in range(1, min(number_one, number_two) + 1):
        if number_one % number == number_two % number == 0:
            common_factors.append(number)

    return common_factors


print(f"PLATFORM: {platform.system()}")  # TODO consider if this is the best place for this?
print(f"win32api_imported: {win32api_imported}")

# Pygame setup:
pygame.init()
pygame.display.set_caption(c.GAME_NAME)
game_clock = pygame.time.Clock()
pygame.mouse.set_visible(c.MOUSE_VISIBLE)

game_window = pygame.display.set_mode(c.RESOLUTION)

Resolution = namedtuple("Resolution", ("width", "height"))
final_resolution = Resolution(width=game_window.get_width(), height=game_window.get_height())


chosen_square_size = min(find_common_factors(*final_resolution), key=lambda number: abs(number - c.TARGET_SQUARE_SIZE))
chosen_square_size_tuple = (chosen_square_size, chosen_square_size)
print(f"TARGET SQUARE SIZE: {c.TARGET_SQUARE_SIZE}")
print(f"CHOSEN VALID SQUARE SIZE: {chosen_square_size}")

refresh_rate = set_refresh_rate()
print(f"DEFAULT REFRESH RATE: {c.DEFAULT_REFRESH_RATE}")
print(f"CHOSEN REFRESH RATE: {refresh_rate}")

# Be careful with which way around rows and columns are - tricky to think about:
num_rows = len(range(0, final_resolution.height, chosen_square_size))
num_columns = len(range(0, final_resolution.width, chosen_square_size))

score_font = pygame.font.Font(None, c.SCORE_FONT_SIZE)
large_menu_font = pygame.font.Font(None, c.LARGE_MENU_FONT_SIZE)
small_menu_font = pygame.font.Font(None, c.SMALL_MENU_FONT_SIZE)

default_theme = "matrix"
games_played = 0

# Load variations of game start sounds:
game_start_dir = "./Music and SFX/game start"
game_start_variations = [pygame.mixer.Sound(join(game_start_dir, file)) for file in listdir(game_start_dir)
                         if isfile(join(game_start_dir, file))]

# Load variations of bite sounds:
bite_sound_dir = "./Music and SFX/bite"
bite_sound_variations = [pygame.mixer.Sound(join(bite_sound_dir, file)) for file in listdir(bite_sound_dir)
                         if isfile(join(bite_sound_dir, file))]

# Load variations of game over sounds:
game_over_dir = "./Music and SFX/game over"
game_over_variations = [pygame.mixer.Sound(join(game_over_dir, file)) for file in listdir(game_over_dir)
                        if isfile(join(game_over_dir, file))]

# Load variations of menu confirm selection sounds:
menu_confirm_selection_dir = "./Music and SFX/menu confirm selection"
menu_confirm_selection_variations = [pygame.mixer.Sound(join(menu_confirm_selection_dir, file)) for file in listdir(menu_confirm_selection_dir)
                                     if isfile(join(menu_confirm_selection_dir, file))]

# Load variations of menu incorrect selection sounds:
menu_incorrect_selection_dir = "./Music and SFX/menu incorrect selection"
menu_incorrect_selection_variations = [pygame.mixer.Sound(join(menu_incorrect_selection_dir, file)) for file in listdir(menu_incorrect_selection_dir)
                                       if isfile(join(menu_incorrect_selection_dir, file))]

# Load variations of menu move selection sounds:
menu_move_selection_dir = "./Music and SFX/menu move selection"
menu_move_selection_variations = [pygame.mixer.Sound(join(menu_move_selection_dir, file)) for file in listdir(menu_move_selection_dir)
                                  if isfile(join(menu_move_selection_dir, file))]

# Load background music .wav files into pygame:
background_music_dir = "./Music and SFX/Music"
background_music_paths = [join(background_music_dir, file) for file in listdir(background_music_dir) if isfile(join(background_music_dir, file))]

# Set initial program-wide music and sound effects loudness from a settings file, or if not available, from defaults:
try:
    music_volume_choice = file_handling.load_settings()["music_volume_choice"]
except KeyError:
    music_volume_choice = c.DEFAULT_MUSIC_VOLUME

try:
    sound_effects_volume_choice = file_handling.load_settings()["sound_effects_volume_choice"]
except KeyError:
    sound_effects_volume_choice = c.DEFAULT_SOUND_EFFECTS_VOLUME


def play_game(player_name):
    # Adds +1 to global tally of the number of games played during this run of the program:
    increment_global_games_played()

    # If this is not the first game played this time, set a new theme for this playthrough:
    if games_played > 1:
        set_global_theme()

    # Set all repeating events:
    set_timed_events()

    # Draws an animation fading from previous menu to its background for a nice visual effect:
    draw_fade_out_effect()

    # Setup:
    game_paused = True if c.START_PAUSED else False

    event_check_collisions = True

    snake_initial_length = 2
    movement_direction = choice(("up", "down", "left", "right"))
    snake_positions = get_initial_snake_positions(snake_initial_length, movement_direction)

    walls_positions = set_walls_positions()
    food_position = set_food_position(snake_positions, walls_positions)

    # Play game starting sound effect, and start background music:
    choice(game_start_variations).play().set_volume(sound_effects_volume_choice)
    pygame.mixer.music.load(choice(background_music_paths))
    pygame.mixer.music.set_volume(music_volume_choice)
    pygame.mixer.music.play(-1)

    score = 0
    alpha = 0
    loop = 0  # TODO remove once not needed

    # Main game loop begins here:
    while True:
        loop += 1  # TODO remove once not needed
        print(f"Debug: Main game loop still running. Loop: {loop}")  # TODO remove once not needed

        # Event handler function:
        movement_direction, game_paused, event_move_signal = event_handler(movement_direction, game_paused, snake_positions, score, player_name)

        # Reset 'alpha' after unpausing, and unpause music playback:
        if not game_paused:
            alpha = 0

        # Main draw function:
        alpha = draw_objects(snake_positions, food_position, walls_positions, score, game_paused, alpha)

        # Move, update, etc:
        if not game_paused and event_move_signal:
            # Invert the 'event_move_signal' so it does not move again until next signal is received:
            move_snake(snake_positions, movement_direction)
            # If snaked move this tick, then check for collisions:
            event_check_collisions = True

        # Quit if game-ending collision detected:
        if event_check_collisions:
            # Invert the 'event_check_collisions' so it does not check again until next signal is received:
            event_check_collisions = not event_check_collisions
            food_position, score, game_paused = check_collisions(snake_positions, walls_positions, food_position, score, game_paused, player_name)

        pygame.display.update()
        game_clock.tick(refresh_rate)


def event_handler(movement_direction, game_paused, snake_positions, score, player_name):
    event_move_signal = False

    for event in pygame.event.get():
        # Check for quit signal:
        if event.type == pygame.QUIT:
            draw_game_over_menu(score, player_name)

        # Check for timed event signalling snake movement:
        elif event.type == events.SNAKE_MOVE_EVENT:
            event_move_signal = True

        # Check for user keyboard input:
        elif event.type == pygame.KEYDOWN:
            movement_direction, game_paused = parse_controls(event, movement_direction, game_paused, snake_positions, score, player_name)

    return movement_direction, game_paused, event_move_signal


def draw_objects(snake_positions, food_position, walls_positions, score, game_paused, alpha):
    # Calls the various object-drawing functions:
    game_window.fill(theme["background"])

    draw_snake(snake_positions)
    draw_food(food_position)
    draw_walls(walls_positions)

    draw_score(score)

    # Increment 'alpha' to allow fade in animation of pause overlay:
    if game_paused:
        draw_game_paused_overlay(alpha)
        alpha += c.GAME_PAUSED_OVERLAY_FADE_IN_SPEED

    return alpha


def draw_snake(snake_positions):
    for position in snake_positions:
        pygame.draw.rect(game_window, theme["snake"], (position, chosen_square_size_tuple))


def draw_food(food_position):
    pygame.draw.rect(game_window, theme["food"], (food_position, chosen_square_size_tuple))


def draw_walls(walls_positions):
    for position in walls_positions:
        pygame.draw.rect(game_window, theme["walls"], (position, chosen_square_size_tuple))


def draw_game_paused_overlay(alpha):
    dark_surface_alpha_final = alpha if alpha < c.DARK_SURFACE_ALPHA else c.DARK_SURFACE_ALPHA

    dark_surface = pygame.Surface(final_resolution)
    dark_surface.set_alpha(dark_surface_alpha_final)
    game_window.blit(dark_surface, (0, 0))

    draw_game_paused_text(alpha)


def draw_game_paused_text(alpha):
    score_alpha_final = alpha
    if score_alpha_final > c.SCORE_ALPHA:
        score_alpha_final = c.SCORE_ALPHA

    game_paused_string = "RESUME:  [ S P A C E ]"
    game_paused_text = score_font.render(game_paused_string, True, theme["text"])
    game_paused_text.set_alpha(score_alpha_final)

    # Center the 'paused' text, so that it is in the middle of the screen:
    target_rect_coordinates = game_paused_text.get_rect(center=(final_resolution.width // 2, final_resolution.height // 2))
    game_window.blit(game_paused_text, target_rect_coordinates)


def draw_score(score):
    score_text = score_font.render(str(score), True, theme["text"])
    score_text.set_alpha(c.SCORE_ALPHA)
    game_window.blit(score_text, (chosen_square_size * 2, chosen_square_size * 2))


def parse_controls(event, movement_direction, game_paused, snake_positions, score, player_name):
    # Setup:
    movement_strings = ("up", "down", "left", "right")
    function_strings = ("pause/unpause", )

    # First, maps the pygame key press event to an appropriate meaningful string. If no mapping, returns 'None':
    string = c.PRESSED_KEY_MAPPING.get(event.key)

    if string == "quit":
        draw_game_over_menu(score, player_name)
    elif string in movement_strings and not game_paused:
        movement_direction = movement_controls(string, movement_direction, snake_positions)
    elif string in function_strings:
        game_paused = function_controls(string, game_paused)

    # Some or all of these will be returned unchanged:
    return movement_direction, game_paused


def movement_controls(string, movement_direction, snake_positions):
    # Setup:
    new_movement_direction = string

    # Check that the new direction does not collide with snake's second element - fixes fast turn suicide bug:
    # Note, this will not work correctly if snake's length is less than 2:
    if new_movement_direction != get_second_element_relative_direction(snake_positions):
        return new_movement_direction

    # If new movement direction is not a valid choice, keep the current one:
    return movement_direction


def function_controls(string, game_paused):
    if string == "pause/unpause":
        if c.ALLOW_PAUSING:
            # Returns inverted pause value:
            return (not game_paused)
        else:
            # Returns 'False' every time - needs to be this explicit for 'START_PAUSED' to work correctly:
            return False


def move_snake(snake_positions, movement_direction):
    head_x_position, head_y_position = snake_positions[0]

    if movement_direction == "up":
        head_y_position -= chosen_square_size
    elif movement_direction == "down":
        head_y_position += chosen_square_size
    elif movement_direction == "left":
        head_x_position -= chosen_square_size
    elif movement_direction == "right":
        head_x_position += chosen_square_size

    new_head_position = (head_x_position, head_y_position)
    snake_positions.insert(0, new_head_position)
    del snake_positions[-1]


def set_food_position(snake_positions, walls_positions):
    # Keep generating new random positions until one meets all conditions:
    while True:
        new_food_position = (
            randrange(0, final_resolution.width, chosen_square_size),
            randrange(0, final_resolution.height, chosen_square_size)
        )

        # Ensure that the new food position is not instantly colliding:
        if new_food_position not in snake_positions and new_food_position not in walls_positions:
            return new_food_position


def set_walls_positions():
    walls_positions = []

    # Top and bottom:
    for left_x_pos in range(0, final_resolution.width, chosen_square_size):
        walls_positions.append((left_x_pos, 0))
        walls_positions.append((left_x_pos, final_resolution.height - chosen_square_size))

    # Left and right:
    for top_y_pos in range(0, final_resolution.height, chosen_square_size):
        walls_positions.append((0, top_y_pos))
        walls_positions.append((final_resolution.width - chosen_square_size, top_y_pos))

    # For sanity's sake, remove duplicates:
    walls = list(set(walls_positions))
    return walls


def check_collisions(snake_positions, walls_positions, food_position, score, game_paused, player_name):
    # Setup:
    walls_collision = tail_collision = False

    # Check for collisions:
    if snake_positions[0] in walls_positions:
        walls_collision = True

    if snake_positions[0] in snake_positions[1:]:
        tail_collision = True

    # If any of the above collision types occurred, then quit:
    if any((walls_collision, tail_collision)):
        draw_game_over_menu(score, player_name)

    # Check for food being eaten:
    if snake_positions[0] == food_position:
        # If eaten, extend the snake (for why this method, see: https://youtu.be/BPyGdbo8xxk?t=1518):
        snake_positions.append(snake_positions[-1])
        food_position = set_food_position(snake_positions, walls_positions)
        score += 1
        # Play a bite sound effect:
        choice(bite_sound_variations).play().set_volume(sound_effects_volume_choice)

    return food_position, score, game_paused


def get_second_element_relative_direction(snake_positions):
    # Setup:
    second_element_relative_direction = None

    # Check that the snake is longer than one, to avoid errors:
    if len(snake_positions) == 1:
        return second_element_relative_direction

    head_x_position, head_y_position = snake_positions[0]
    second_segment_x_position, second_segment_y_position = snake_positions[1]

    # Subtract the element-wise positions of second segment of snake from its head:
    horizontal_change = head_x_position - second_segment_x_position
    vertical_change = head_y_position - second_segment_y_position

    if horizontal_change == 0:
        # Up or down:
        if vertical_change > 0:
            second_element_relative_direction = "up"
        elif vertical_change < 0:
            second_element_relative_direction = "down"

    elif vertical_change == 0:
        # Left or right:
        if horizontal_change > 0:
            second_element_relative_direction = "left"
        elif horizontal_change < 0:
            second_element_relative_direction = "right"

    return second_element_relative_direction


def get_initial_snake_positions(snake_initial_length, movement_direction):
    if snake_initial_length < 2:
        raise ValueError("The 'snake_initial_length' variable must be an integer greater than one.")

    # Setup:
    initial_snake_positions = []

    # These numbers control the percentage of the play area that is a no-spawn zone. NOTE: Per-side so from 0.0 to 0.5, do not go >= 0.5
    horizontal_border_percentage_per_side = 0.4  # TODO these two might need changing so they work in a more logical 0.0 to 1.0 interval
    vertical_border_percentage_per_side = 0.4

    print(f"num_rows: {num_rows}")
    print(f"num_columns: {num_columns}")

    # Establish whether 'minimum_gap' of wall size + snake length is needed:
    if round(num_rows * horizontal_border_percentage_per_side) < 1 + snake_initial_length:
        minimum_gap = (1 + snake_initial_length)
    else:
        minimum_gap = 0

    print(f"minimum_gap: {minimum_gap}")

    # The actual calculations - takes into account 'do not spawn here' borders, the visible walls, and the snake's length:
    valid_rows = range(
        round(0 + (num_rows * horizontal_border_percentage_per_side)) + minimum_gap,
        round(num_rows - (num_rows * horizontal_border_percentage_per_side)) - minimum_gap
    )

    valid_columns = range(
        round(0 + (num_columns * vertical_border_percentage_per_side)) + minimum_gap,
        round(num_columns - (num_columns * vertical_border_percentage_per_side)) - minimum_gap
    )

    print(f"valid_rows: {valid_rows}")
    print(f"valid_columns: {valid_columns}")

    # Randomly pick where the snake begins, then get the next elements stepwise:
    for piece in range(snake_initial_length):
        next_position = None

        # If this will be the first - head - piece of the snake, choose a random place for it:
        if not initial_snake_positions:
            next_position = (choice(valid_columns) * chosen_square_size, choice(valid_rows) * chosen_square_size)

        # If this is a subsequent piece, make sure it attaches to the first one, in a direction opposite to movement:
        else:
            previous_position_x, previous_position_y = initial_snake_positions[piece - 1]

            if movement_direction == "up":
                next_position = (previous_position_x, previous_position_y + chosen_square_size)
            elif movement_direction == "down":
                next_position = (previous_position_x, previous_position_y - chosen_square_size)
            elif movement_direction == "left":
                next_position = (previous_position_x + chosen_square_size, previous_position_y)
            elif movement_direction == "right":
                next_position = (previous_position_x - chosen_square_size, previous_position_y)

        # If 'next_position' is not None, append it to the snake's positions:
        if next_position:
            initial_snake_positions.append(next_position)

    print(f"initial_snake_positions: {initial_snake_positions}")
    return initial_snake_positions


def set_timed_events():
    # Setup:
    snake_move_delay = 60

    # Timers:
    pygame.time.set_timer(events.SNAKE_MOVE_EVENT, events.SNAKE_MOVE_DELAY)


def draw_main_menu():
    """
    This function draws the main menu.
    The menu allows the user to choose from a number of options.
    """

    # Gradually fades from previous frame to background colour for a pleasing effect:
    draw_fade_out_effect()

    choice_index = 0
    menu_elements = [
        {
            "message": "PLAY",
            "action": draw_player_name_prompt,
            "colour": theme["menu_element_not_selected"],
            "position": (final_resolution.width // 2, final_resolution.height // 7 * 3),
        },

        {
            "message": "SCORES",
            "action": draw_scores_menu,
            "colour": theme["menu_element_not_selected"],
            "position": (final_resolution.width // 2, final_resolution.height // 7 * 4),
        },

        {
            "message": "OPTIONS",
            "action": draw_options_menu,
            "colour": theme["menu_element_not_selected"],
            "position": (final_resolution.width // 2, final_resolution.height // 7 * 5),
        },

        {
            "message": "QUIT",
            "action": quit_game,
            "colour": theme["menu_element_not_selected"],
            "position": (final_resolution.width // 2, final_resolution.height // 7 * 6),
        },
    ]

    alpha = 0

    # Main loop starts here:
    while True:
        alpha += c.MENU_FADE_IN_SPEED if alpha + c.MENU_FADE_IN_SPEED < 255 else 255

        game_window.fill(theme["background"])

        # Draw the static element 'game name', which should not be selectable or change colour:
        draw_static_menu_element(c.GAME_NAME.upper(), (final_resolution.width // 2, final_resolution.height // 7 * 1))

        # Draw each menu element from 'menu_elements':
        draw_dynamic_menu_elements(menu_elements, alpha)

        # Changes colour of 'selected' element:
        for index, menu_element in enumerate(menu_elements):
            # If element matches the selected element, then change its colour:
            if index == choice_index:
                menu_element["colour"] = theme["menu_element_selected"]
            # Otherwise, change the not matching elements to default colour to ensure they are not ghosting as selected:
            else:
                menu_element["colour"] = theme["menu_element_not_selected"]

        # Check for user input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    if choice_index > 0:
                        choice_index -= 1
                        # Play a sound effect associated with moving the selection:
                        choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)
                    else:
                        # Play a sound effect indicating an incorrect selection:
                        choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)


                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if choice_index < len(menu_elements) - 1:
                        choice_index += 1
                        # Play a sound effect associated with moving the selection:
                        choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)
                    else:
                        # Play a sound effect indicating an incorrect selection:
                        choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)


                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    # Play a sound effect confirming selection:
                    choice(menu_confirm_selection_variations).play().set_volume(sound_effects_volume_choice)
                    # Carry out an 'action' - call a function associated with selected element:
                    menu_elements[choice_index]["action"](
                        *menu_elements[choice_index].get("args", []),
                        **menu_elements[choice_index].get("kwargs", {})
                    )

        # Finally, update the display and wait until next tick:
        pygame.display.update()
        game_clock.tick(refresh_rate)


def draw_player_name_prompt():

    # Make two copies - one to be modified, and a second to compare to:
    player_name = default_answer = "WHAT IS YOUR NAME ?"
    explanation_text = "[BACKSPACE] TO REMOVE. [ENTER] TO CONFIRM."

    # Main loop:
    while True:
        game_window.fill(theme["background"])

        # Render the text and get its bounding rect:
        element_text = large_menu_font.render(player_name, True, theme["menu_element_not_selected"])
        element_text.set_alpha(255)
        element_text_rect = element_text.get_rect(center=(final_resolution.width // 2, final_resolution.height // 7 * 4))

        # Make a copy of the text rect to use as a base for the underscore rect:
        highlight_rect = element_text_rect.copy()  # 'copy' call is super important here, otherwise referring to old text rect
        highlight_rect.height = 10

        # Make sure the underscore is visible even without any text:
        if highlight_rect.width < c.LARGE_MENU_FONT_SIZE:
            highlight_rect.width = c.LARGE_MENU_FONT_SIZE

        # Align underscore so it is under the text input field:
        highlight_rect.midtop = element_text_rect.midbottom

        # Finally, draw the underscore to the game window, then blit the text:
        pygame.draw.rect(game_window, colours.get_complementary_colour(theme["background"]), highlight_rect)
        game_window.blit(element_text, element_text_rect)

        draw_static_menu_element(explanation_text, (final_resolution.width // 2, final_resolution.height // 7 * 6), font=small_menu_font)

        # Check for user input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)
                    # If user presses 'backspace' with default text displayed, remove all text for convenience:
                    if player_name == default_answer:
                        player_name = ""
                    # Otherwise, remove only one character, as expected:
                    else:
                        player_name = player_name[:-1]

                elif event.unicode.isalnum():
                    player_name += event.unicode
                    choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)

                elif event.key == pygame.K_SPACE:
                    player_name += " "
                    choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)

                elif event.key == pygame.K_RETURN:
                    # Check that user provided a name which is not the original prompt, empty, or whitespace only:
                    if player_name.strip() not in (default_answer, ""):
                        choice(menu_confirm_selection_variations).play().set_volume(sound_effects_volume_choice)
                        # Strip whitespaces on ends of player name, then run a new game with that name:
                        player_name = player_name.strip()
                        play_game(player_name)
                    else:
                        # Change prompt to alert user:
                        player_name = default_answer = "INPUT A UNIQUE NAME"
                        choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)

        pygame.display.update()
        game_clock.tick(refresh_rate)


def draw_scores_menu():

    # Gradually fades from previous frame to background colour for a pleasing effect:
    draw_fade_out_effect()

    # Load the scores from file, then sort them by score descending:
    saves = file_handling.load_saves()
    sorted_saves = sorted(saves, key=lambda save: save["score"], reverse=True)

    # Do some maths needed for displaying the scores:
    score_index = 0
    num_scores_per_page = 3
    total_num_scores = len(saves)
    range_score_indexes = range(0, total_num_scores)

    choice_index = 0
    menu_elements = [
        {
            "message": "PREVIOUS",
            "action": -1,
            "colour": theme["menu_element_not_selected"],
            "position": (final_resolution.width // 4 * 1, final_resolution.height // 7 * 2),
        },

        {
            "message": "NEXT",
            "action": +1,
            "colour": theme["menu_element_not_selected"],
            "position": (final_resolution.width // 4 * 3, final_resolution.height // 7 * 2),
        },

        {
            "message": "MAIN MENU",
            "action": draw_main_menu,
            "colour": theme["menu_element_not_selected"],
            "position": (final_resolution.width // 2, final_resolution.height // 7 * 6),
        },
    ]

    alpha = 0

    # Main loop starts here:
    while True:

        alpha += c.MENU_FADE_IN_SPEED if alpha + c.MENU_FADE_IN_SPEED < 255 else 255

        game_window.fill(theme["background"])

        # Draw the static element 'score', which should not be selectable or change colour:
        draw_static_menu_element("SCORES", (final_resolution.width // 2, final_resolution.height // 7 * 1))

        # Draw a black, semi-transparent bar below scores to make it visually nicer:
        scores_contrast_surface = pygame.Surface(final_resolution)
        scores_contrast_surface.fill(theme["background"])
        scores_contrast_alpha = alpha // 8 if alpha // 8 < 31 else 31
        scores_contrast_surface.set_alpha(scores_contrast_alpha)
        scores_contrast_rect = pygame.Rect((0, final_resolution.height // 7 * 3 - c.LARGE_MENU_FONT_SIZE / 2), (final_resolution.width, 440))
        pygame.draw.rect(scores_contrast_surface, (0, 0, 0), scores_contrast_rect)
        game_window.blit(scores_contrast_surface, (0, 0))

        # Draws the actual scores by going over them in 'num_scores_per_page' sized slices at a time, until user signal changes 'score_index', changing which slice is drawn:
        for save in range(score_index, (score_index + num_scores_per_page)):
            # Checks that the 'save' number is in 'range_score_indexes' to ensure terminal indexes are valid, to avoid downstream errors:
            if save in range_score_indexes:
                draw_static_menu_element(str(save + 1), (final_resolution.width // 6 * 2, final_resolution.height // 7 * (3 + save % 3)), alpha=alpha)
                draw_static_menu_element(sorted_saves[save]["player_name"], (final_resolution.width // 6 * 3, final_resolution.height // 7 * (3 + save % 3)), alpha=alpha)
                draw_static_menu_element(str(sorted_saves[save]["score"]), (final_resolution.width // 6 * 4, final_resolution.height // 7 * (3 + save % 3)), alpha=alpha)

        # Draw each menu element from 'menu_elements':
        draw_dynamic_menu_elements(menu_elements, alpha=alpha)

        # Changes colour of 'selected' element:
        for index, menu_element in enumerate(menu_elements):
            # If element matches the selected element, then change its colour:
            if index == choice_index:
                menu_element["colour"] = theme["menu_element_selected"]

            # Otherwise, change the element to default colour to ensure elements are not 'ghosting' colour as selected:
            else:
                menu_element["colour"] = theme["menu_element_not_selected"]

        # Check for user input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Up/w menu controls:
                if event.key in (pygame.K_UP, pygame.K_w):
                    if choice_index > 0:
                        choice_index -= 1
                        # Play a sound effect associated with moving the selection:
                        choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)
                    else:
                        # Play a sound effect indicating an incorrect selection:
                        choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)

                # Down/s menu controls:
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    if choice_index < len(menu_elements) - 1:
                        choice_index += 1
                        # Play a sound effect associated with moving the selection:
                        choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)
                    else:
                        # Play a sound effect indicating an incorrect selection:
                        choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)

                # Left/a menu controls - moves scores towards highest:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    if score_index - num_scores_per_page in range_score_indexes:
                        score_index -= num_scores_per_page
                        # Play a sound effect associated with moving the selection:
                        choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)
                    else:
                        # Play a sound effect indicating an incorrect selection:
                        choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)

                # Right/d menu controls - moves scores towards lowest:
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    if score_index + num_scores_per_page in range_score_indexes:
                        score_index += num_scores_per_page
                        # Play a sound effect associated with moving the selection:
                        choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)
                    else:
                        # Play a sound effect indicating an incorrect selection:
                        choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)

                # Enter/space menu controls - confirms selected menu element - carries out its action:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if choice_index in (0, 1):
                        # TODO add description of the two lines below
                        if score_index + menu_elements[choice_index]["action"] * num_scores_per_page in range_score_indexes:
                            score_index += menu_elements[choice_index]["action"] * num_scores_per_page
                            # Play a sound effect confirming selection:
                            choice(menu_confirm_selection_variations).play().set_volume(sound_effects_volume_choice)
                        else:
                            # Play a sound effect indicating an incorrect selection:
                            choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)
                    else:
                        # Play a sound effect confirming selection:
                        choice(menu_confirm_selection_variations).play().set_volume(sound_effects_volume_choice)
                        # Carry out an 'action' - call a function associated with selected element:
                        menu_elements[choice_index]["action"](
                            *menu_elements[choice_index].get("args", []),
                            **menu_elements[choice_index].get("kwargs", {})
                        )

        # Finally, update the display and wait until next tick:
        pygame.display.update()
        game_clock.tick(refresh_rate)


def draw_options_menu():
    global music_volume_choice, sound_effects_volume_choice

    # Gradually fades from previous frame to background colour for a pleasing effect:
    draw_fade_out_effect()

    choice_index = 0
    menu_elements = [
        {
            "message": f"MUSIC VOLUME:",
            "colour": theme["menu_element_not_selected"],
            "position": (final_resolution.width // 2, final_resolution.height // 7 * 3),
        },

        {
            "message": f"SOUND EFFECTS VOLUME:",
            "colour": theme["menu_element_not_selected"],
            "position": (final_resolution.width // 2, final_resolution.height // 7 * 4),
        },

        {
            "message": "MAIN MENU",
            "action": draw_main_menu,
            "colour": theme["menu_element_not_selected"],
            "position": (final_resolution.width // 2, final_resolution.height // 7 * 6),
        },
    ]

    alpha = 0

    # Main loop starts here:
    while True:
        alpha += c.MENU_FADE_IN_SPEED if alpha + c.MENU_FADE_IN_SPEED < 255 else 255

        game_window.fill(theme["background"])

        # Draw the static element 'score', which should not be selectable or change colour:
        draw_static_menu_element("OPTIONS", (final_resolution.width // 2, final_resolution.height // 7 * 1))
        draw_static_menu_element(f"{int(music_volume_choice * 100)} %", (final_resolution.width // 56 * 41, final_resolution.height // 7 * 3))
        draw_static_menu_element(f"{int(sound_effects_volume_choice * 100)} %", (final_resolution.width // 56 * 46, final_resolution.height // 7 * 4))

        # Draw each dynamic menu element from 'menu_elements':
        draw_dynamic_menu_elements(menu_elements, alpha=alpha)

        # Changes colour of 'selected' element:
        for index, menu_element in enumerate(menu_elements):
            # If element matches the selected element, then change its colour:
            if index == choice_index:
                menu_element["colour"] = theme["menu_element_selected"]

            # Otherwise, change the element to default colour to ensure elements are not 'ghosting' colour as selected:
            else:
                menu_element["colour"] = theme["menu_element_not_selected"]

        # Check for user input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    if choice_index > 0:
                        choice_index -= 1
                        # Play a sound effect confirming selection:
                        choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)
                    else:
                        # Play a sound effect indicating an incorrect selection:
                        choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)

                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if choice_index < len(menu_elements) - 1:
                        choice_index += 1
                        # Play a sound effect confirming selection:
                        choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)
                    else:
                        # Play a sound effect indicating an incorrect selection:
                        choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)

                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if choice_index == 0:
                        if music_volume_choice > 0:
                            # Decrease music volume:
                            music_volume_choice = round(music_volume_choice - 0.1, 2)
                            choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)
                        else:
                            # Play 'incorrect selection' sound effect:
                            choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)

                    elif choice_index == 1:
                        if sound_effects_volume_choice > 0:
                            # Decrease sound fx volume:
                            sound_effects_volume_choice = round(sound_effects_volume_choice - 0.1, 2)
                            choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)
                        else:
                            # Play 'incorrect selection' sound effect:
                            choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)

                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if choice_index == 0:
                        if music_volume_choice < 1:
                            # Increase music volume:
                            music_volume_choice = round(music_volume_choice + 0.1, 2)
                            choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)
                        else:
                            # Play 'incorrect selection' sound effect:
                            choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)

                    elif choice_index == 1:
                        if sound_effects_volume_choice < 1:
                            # Increase sound fx volume:
                            sound_effects_volume_choice = round(sound_effects_volume_choice + 0.1, 2)
                            choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)
                        else:
                            # Play 'incorrect selection' sound effect:
                            choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)

                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    # First, save the currently selected settings:  # TODO consider how does one cancel / apply settings?
                    file_handling.save_settings(music_volume_choice=music_volume_choice, sound_effects_volume_choice=sound_effects_volume_choice)

                    if "action" in menu_elements[choice_index]:
                        # Play a sound effect confirming selection. NOTE: Needs to be done before executing action:
                        choice(menu_confirm_selection_variations).play().set_volume(sound_effects_volume_choice)
                        # Carry out an 'action' - call a function associated with selected element:
                        menu_elements[choice_index]["action"](
                            *menu_elements[choice_index].get("args", []),
                            **menu_elements[choice_index].get("kwargs", {})
                        )
                    else:
                        # Play 'incorrect selection' sound effect:
                        choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)

        # Finally, update the display and wait until next tick:
        pygame.display.update()
        game_clock.tick(refresh_rate)


def draw_game_over_menu(score=0, player_name="Anonymous"):
    """
    This function draws the 'game over' menu.
    The menu displays the score using the game score passed as the 'score' argument.
    The menu allows the user to choose to either exit to main menu, or to play again.
    """

    # Play game over sound effect, and stop background music playback:
    choice(game_over_variations).play().set_volume(sound_effects_volume_choice)
    pygame.mixer.music.fadeout(500)

    # If score is not 0, then saves player's score in a local file:
    if score:
        file_handling.save_saves(score, player_name)

    # Wait a 'c.GAME_OVER_DELAY' seconds before quitting to let player realise what happened:
    if c.SLEEP_AFTER_GAME_OVER:
        sleep(c.GAME_OVER_DELAY)

    # Gradually fades from previous frame to background colour for a pleasing effect:
    draw_fade_out_effect()

    choice_index = 0
    menu_elements = [
        {
            "message": "PLAY AGAIN",
            "action": play_game,
            "args": [player_name, ],
            "colour": theme["menu_element_not_selected"],
            "position": (final_resolution.width // 2, final_resolution.height // 7 * 3),
        },

        {
            "message": "MAIN MENU",
            "action": draw_main_menu,
            "colour": theme["menu_element_not_selected"],
            "position": (final_resolution.width // 2, final_resolution.height // 7 * 5),
        },
    ]

    alpha = 0

    # Main loop starts here:
    while True:
        alpha += c.MENU_FADE_IN_SPEED if alpha + c.MENU_FADE_IN_SPEED < 255 else 255

        game_window.fill(theme["background"])

        # Draw the static element 'score', which should not be selectable or change colour:
        draw_static_menu_element(f"SCORE: {score}", (final_resolution.width // 2, final_resolution.height // 7 * 1), alpha=alpha)

        # Draw each menu element from 'menu_elements':
        draw_dynamic_menu_elements(menu_elements, alpha=alpha)

        # Changes colour of 'selected' element:
        for index, menu_element in enumerate(menu_elements):
            # If element matches the selected element, then change its colour:
            if index == choice_index:
                menu_element["colour"] = theme["menu_element_selected"]

            # Otherwise, change the element to default colour to ensure elements are not 'ghosting' colour as selected:
            else:
                menu_element["colour"] = theme["menu_element_not_selected"]

        # Check for user input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    if choice_index > 0:
                        choice_index -= 1
                        # Play a sound associated with moving a selection:
                        choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)
                    else:
                        # Play a sound effect indicating an incorrect selection:
                        choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)

                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if choice_index < len(menu_elements) - 1:
                        choice_index += 1
                        # Play a sound associated with moving a selection:
                        choice(menu_move_selection_variations).play().set_volume(sound_effects_volume_choice)
                    else:
                        # Play a sound effect indicating an incorrect selection:
                        choice(menu_incorrect_selection_variations).play().set_volume(sound_effects_volume_choice)

                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    # Play a sound effect confirming selection:
                    choice(menu_confirm_selection_variations).play().set_volume(sound_effects_volume_choice)
                    # Carry out an 'action' - call a function associated with selected element:
                    menu_elements[choice_index]["action"](
                        *menu_elements[choice_index].get("args", []),
                        **menu_elements[choice_index].get("kwargs", {})
                    )

        # Finally, update the display and wait until next tick:
        pygame.display.update()
        game_clock.tick(refresh_rate)


def draw_static_menu_element(message, position, alpha=255, font=large_menu_font):
    """
    When called, this function draws one 'static' element of a menu, based on 'message' and 'position' passed.
    Intended to be called only inside the main loop of a top level menu function.
    The optional keyword argument 'alpha' should be provided when creating fading in animation effect.
    """
    element_text = font.render(message, True, theme["menu_element_not_selected"])
    element_text.set_alpha(alpha)
    element_text_rect = element_text.get_rect(center=position)
    game_window.blit(element_text, element_text_rect)


def draw_dynamic_menu_elements(menu_elements, alpha=255, font=large_menu_font):
    """
    When called, this function draws the 'selectable' elements of a menu, based on elements passed in 'menu_elements'.
    Intended to be called only inside the main loop of a top level menu function.
    The optional keyword argument 'alpha' should be provided when creating fading in animation effect.
    """
    for menu_element in menu_elements:
        element_text = font.render(menu_element["message"], True, menu_element["colour"])
        element_text.set_alpha(alpha)
        element_text_rect = element_text.get_rect(center=menu_element["position"])
        game_window.blit(element_text, element_text_rect)


def draw_fade_out_effect():
    alpha = 0

    while alpha < 255:
        fade_surface = pygame.Surface(final_resolution)
        fade_surface.fill(theme["background"])
        fade_surface.set_alpha(alpha)

        game_window.blit(fade_surface, (0, 0))

        pygame.display.update()
        game_clock.tick(refresh_rate)

        alpha += c.MENU_FADE_OUT_SPEED


def set_global_theme(theme_to_set=None):
    """
    This function sets and changes the GLOBAL 'theme' variable.
    This is currently necessary for having different themes when playing again during the same run of the program.
    """
    global theme  # TODO be careful with global

    if theme_to_set is not None:
        theme = colours.themes[theme_to_set]
    else:
        theme = choice(list(colours.themes.values())) if c.PICK_RANDOM_THEME else colours.themes[default_theme]

    theme["menu_element_not_selected"] = colours.get_complementary_colour(theme["text"])
    theme["menu_element_selected"] = colours.get_complementary_colour(theme["background"])


def increment_global_games_played():
    """
    This function adds '+1' to the GLOBAL variable 'games_played'.
    This helps keep track for the purpose of not changing the theme between running the game and first playthrough.
    """
    global games_played

    games_played += 1


def quit_game():
    """
    This function un-initialises pygame and quits the program.
    """
    draw_fade_out_effect()

    pygame.quit()
    exit()


def find_common_factors(number_one, number_two):
    common_factors = []

    for number in range(1, min(number_one, number_two) + 1):
        if number_one % number == number_two % number == 0:
            common_factors.append(number)

    return common_factors




if __name__ == '__main__':
    set_global_theme()
    draw_main_menu()
