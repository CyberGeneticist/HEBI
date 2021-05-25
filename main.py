# Python 3.9.5

# Project imports:
import colours  # My module - part of this program
import events  # My module - part of this program
import constants as c  # My module - part of this program

# Total imports:
import pygame

# Aliased imports:
from collections import namedtuple
from sys import exit
from random import randrange, choice
from time import sleep


# Pygame setup:
pygame.init()
pygame.display.set_caption(c.GAME_NAME)
game_clock = pygame.time.Clock()
pygame.mouse.set_visible(c.MOUSE_VISIBLE)

game_window = pygame.display.set_mode(c.RESOLUTION)

Resolution = namedtuple("Resolution", ("width", "height"))
final_resolution = Resolution(width=game_window.get_width(), height=game_window.get_height())

num_rows = len(range(0, final_resolution.width, c.SQUARE_SIZE))
num_columns = len(range(0, final_resolution.height, c.SQUARE_SIZE))

score_font = pygame.font.Font(None, c.SCORE_FONT_SIZE)
quit_game_font = pygame.font.Font(None, c.QUIT_GAME_FONT_SIZE)

chosen_theme = "matrix"
games_played = 0


def play_game():
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

    score = 0
    alpha = 0

    # Main game loop begins here:
    while True:

        # Event handler function:
        movement_direction, game_paused, event_move_signal = event_handler(movement_direction, game_paused, snake_positions, score)

        # Reset 'alpha' after unpausing:
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
            food_position, score, game_paused = check_collisions(snake_positions, walls_positions, food_position, score, game_paused)

        pygame.display.update()
        game_clock.tick(c.FPS)


def event_handler(movement_direction, game_paused, snake_positions, score):
    event_move_signal = False

    for event in pygame.event.get():
        # Check for quit signal:
        if event.type == pygame.QUIT:
            draw_game_over_menu(score)

        # Check for timed event signalling snake movement:
        elif event.type == events.SNAKE_MOVE_EVENT:
            event_move_signal = True

        # Check for user keyboard input:
        elif event.type == pygame.KEYDOWN:
            movement_direction, game_paused = parse_controls(event, movement_direction, game_paused, snake_positions, score)

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
        pygame.draw.rect(game_window, theme["snake"], (position, c.SQUARE_SIZE_TUPLE))


def draw_food(food_position):
    pygame.draw.rect(game_window, theme["food"], (food_position, c.SQUARE_SIZE_TUPLE))


def draw_walls(walls_positions):
    for position in walls_positions:
        pygame.draw.rect(game_window, theme["walls"], (position, c.SQUARE_SIZE_TUPLE))


def draw_game_paused_overlay(alpha):
    dark_surface_alpha_final = alpha
    if dark_surface_alpha_final > c.DARK_SURFACE_ALPHA:
        dark_surface_alpha_final = c.DARK_SURFACE_ALPHA

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
    game_window.blit(score_text, (c.SQUARE_SIZE * 2, c.SQUARE_SIZE * 2))


def parse_controls(event, movement_direction, game_paused, snake_positions, score):
    # Setup:
    movement_strings = ("up", "down", "left", "right")
    function_strings = ("pause/unpause", )

    # First, maps the pygame key press event to an appropriate meaningful string. If no mapping, returns 'None':
    string = c.PRESSED_KEY_MAPPING.get(event.key)

    if string == "quit":
        draw_game_over_menu(score)
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
        head_y_position -= c.SQUARE_SIZE
    elif movement_direction == "down":
        head_y_position += c.SQUARE_SIZE
    elif movement_direction == "left":
        head_x_position -= c.SQUARE_SIZE
    elif movement_direction == "right":
        head_x_position += c.SQUARE_SIZE

    new_head_position = (head_x_position, head_y_position)
    snake_positions.insert(0, new_head_position)
    del snake_positions[-1]


def set_food_position(snake_positions, walls_positions):
    # Keep generating new random positions until one meets all conditions:
    while True:
        new_food_position = (
            randrange(0, final_resolution.width, c.SQUARE_SIZE),
            randrange(0, final_resolution.height, c.SQUARE_SIZE)
        )

        # Ensure that the new food position is not instantly colliding:
        if new_food_position not in snake_positions and new_food_position not in walls_positions:
            return new_food_position


def set_walls_positions():
    walls_positions = []

    # Top and bottom:
    for left_x_pos in range(0, final_resolution.width, c.SQUARE_SIZE):
        walls_positions.append((left_x_pos, 0))
        walls_positions.append((left_x_pos, final_resolution.height - c.SQUARE_SIZE))

    # Left and right:
    for top_y_pos in range(0, final_resolution.height, c.SQUARE_SIZE):
        walls_positions.append((0, top_y_pos))
        walls_positions.append((final_resolution.width - c.SQUARE_SIZE, top_y_pos))

    # For sanity's sake, remove duplicates:
    walls = list(set(walls_positions))
    return walls


def check_collisions(snake_positions, walls_positions, food_position, score, game_paused):
    # Setup:
    walls_collision = tail_collision = False

    # Check for collisions:
    if snake_positions[0] in walls_positions:
        walls_collision = True

    if snake_positions[0] in snake_positions[1:]:
        tail_collision = True

    # If any of the above collision types occurred, then quit:
    if any((walls_collision, tail_collision)):
        draw_game_over_menu(score)

    # Check for food being eaten:
    if snake_positions[0] == food_position:
        # If eaten, extend the snake (for why this method, see: https://youtu.be/BPyGdbo8xxk?t=1518):
        snake_positions.append(snake_positions[-1])
        food_position = set_food_position(snake_positions, walls_positions)
        score += 1

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
    border_divisor = 5

    # Calculates the rounded-down number of rows and columns which are in 'border_percentage' outside edges of the screen:
    horizontal_border = num_rows // border_divisor
    vertical_border = num_columns // border_divisor

    # Gets numbers of rows and columns which are in the 'border' area:
    possible_rows = range(0 + vertical_border, num_rows - vertical_border)
    possible_columns = range(0 + horizontal_border, num_columns - horizontal_border)

    for piece in range(snake_initial_length):
        # If this will be the first - head - piece of the snake, choose a random place for it:
        if not initial_snake_positions:
            next_position = (choice(possible_rows) * c.SQUARE_SIZE, choice(possible_columns) * c.SQUARE_SIZE)

        # If this is a subsequent piece, make sure it attaches to the first one, in a direction opposite to movement:
        else:
            previous_position_x, previous_position_y = initial_snake_positions[piece - 1]

            if movement_direction == "up":
                next_position = (previous_position_x, previous_position_y + c.SQUARE_SIZE)
            elif movement_direction == "down":
                next_position = (previous_position_x, previous_position_y - c.SQUARE_SIZE)
            elif movement_direction == "left":
                next_position = (previous_position_x + c.SQUARE_SIZE, previous_position_y)
            elif movement_direction == "right":
                next_position = (previous_position_x - c.SQUARE_SIZE, previous_position_y)

        initial_snake_positions.append(next_position)

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
            "action": play_game,
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
        draw_dynamic_menu_elements(menu_elements, alpha=alpha)

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
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_UP, pygame.K_w):
                if choice_index > 0:
                    choice_index -= 1

            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_DOWN, pygame.K_s):
                if choice_index < len(menu_elements) - 1:
                    choice_index += 1

            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                # Carry out an 'action' - call a function associated with selected element:
                menu_elements[choice_index]["action"]()

        # Finally, update the display and wait until next tick:
        pygame.display.update()
        game_clock.tick(c.FPS)


def draw_scores_menu():  # TODO add 'scores' features

    # Gradually fades from previous frame to background colour for a pleasing effect:
    draw_fade_out_effect()

    choice_index = 0
    menu_elements = [
        {
            "message": "PREVIOUS",
            "action": print,  # TODO add action
            "colour": theme["menu_element_not_selected"],
            "position": (final_resolution.width // 4 * 1, final_resolution.height // 7 * 2),
        },

        {
            "message": "NEXT",
            "action": print,  # TODO add action
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
        draw_static_menu_element("WORK IN PROGRESS", (final_resolution.width // 2, final_resolution.height // 7 * 4))

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
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_UP, pygame.K_w):
                if choice_index > 0:
                    choice_index -= 1

            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_DOWN, pygame.K_s):
                if choice_index < len(menu_elements) - 1:
                    choice_index += 1

            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                # Carry out an 'action' - call a function associated with selected element:
                menu_elements[choice_index]["action"]()

        # Finally, update the display and wait until next tick:
        pygame.display.update()
        game_clock.tick(c.FPS)


def draw_options_menu():  # TODO add 'options' features

    # Gradually fades from previous frame to background colour for a pleasing effect:
    draw_fade_out_effect()

    choice_index = 0
    menu_elements = [
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
        draw_static_menu_element("WORK IN PROGRESS", (final_resolution.width // 2, final_resolution.height // 7 * 4))

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
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_UP, pygame.K_w):
                if choice_index > 0:
                    choice_index -= 1

            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_DOWN, pygame.K_s):
                if choice_index < len(menu_elements) - 1:
                    choice_index += 1

            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                # Carry out an 'action' - call a function associated with selected element:
                menu_elements[choice_index]["action"]()

        # Finally, update the display and wait until next tick:
        pygame.display.update()
        game_clock.tick(c.FPS)


def draw_game_over_menu(score=0):
    """
    This function draws the 'game over' menu.
    The menu displays the score using the game score passed as the 'score' argument.
    The menu allows the user to choose to either exit to main menu, or to play again.
    """

    if c.SLEEP_AFTER_GAME_OVER:
        sleep(c.SECONDS_TO_SLEEP_AFTER_GAME_OVER)

    # Gradually fades from previous frame to background colour for a pleasing effect:
    draw_fade_out_effect()

    choice_index = 0
    menu_elements = [
        {
            "message": "PLAY AGAIN",
            "action": play_game,
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
        draw_static_menu_element(f"SCORE: {score}", (final_resolution.width // 2, final_resolution.height // 7 * 1), alpha)

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
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_UP, pygame.K_w):
                if choice_index > 0:
                    choice_index -= 1

            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_DOWN, pygame.K_s):
                if choice_index < len(menu_elements) - 1:
                    choice_index += 1

            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                # Carry out an 'action' - call a function associated with selected element:
                menu_elements[choice_index]["action"]()

        # Finally, update the display and wait until next tick:
        pygame.display.update()
        game_clock.tick(c.FPS)


def draw_static_menu_element(message, position, alpha=255):
    """
    When called, this function draws one 'static' element of a menu, based on 'message' and 'position' passed.
    Intended to be called only inside the main loop of a top level menu function.
    The optional keyword argument 'alpha' should be provided when creating fading in animation effect.
    """
    element_text = quit_game_font.render(message, True, theme["menu_element_not_selected"])
    element_text.set_alpha(alpha)
    element_text_rect = element_text.get_rect(center=position)
    game_window.blit(element_text, element_text_rect)


def draw_dynamic_menu_elements(menu_elements, alpha=255):
    """
    When called, this function draws the 'selectable' elements of a menu, based on elements passed in 'menu_elements'.
    Intended to be called only inside the main loop of a top level menu function.
    The optional keyword argument 'alpha' should be provided when creating fading in animation effect.
    """
    for menu_element in menu_elements:
        element_text = quit_game_font.render(menu_element["message"], True, menu_element["colour"])
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
        game_clock.tick(c.FPS)

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
        theme = choice(list(colours.themes.values())) if c.PICK_RANDOM_THEME else colours.themes[chosen_theme]

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




if __name__ == '__main__':
    set_global_theme()
    draw_main_menu()
