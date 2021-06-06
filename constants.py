# Python 3.9.5
import pygame

GAME_NAME = "Snake"

START_PAUSED = True
ALLOW_PAUSING = True
FULLSCREEN = True
MOUSE_VISIBLE = False
PICK_RANDOM_THEME = True
SLEEP_AFTER_GAME_OVER = True

FPS = 60
SECONDS_TO_SLEEP_AFTER_GAME_OVER = 1

ALTERNATIVE_RESOLUTION = (1920, 1080)  # TODO test a variety of resolutions
RESOLUTION = (0, 0) if FULLSCREEN else ALTERNATIVE_RESOLUTION

SQUARE_SIZE = 40  # TODO implement smart variable square size to suit different resolutions
SQUARE_SIZE_TUPLE = (SQUARE_SIZE, SQUARE_SIZE)

SCORE_FONT_SIZE = 70
SCORE_ALPHA = 100
LARGE_MENU_FONT_SIZE = 130
SMALL_MENU_FONT_SIZE = 50

DARK_SURFACE_ALPHA = 127

MENU_FADE_IN_SPEED = 6
MENU_FADE_OUT_SPEED = 6
GAME_PAUSED_OVERLAY_FADE_IN_SPEED = 6

SAVE_FILE_PATH = "./save.json"


PRESSED_KEY_MAPPING = {
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",

    pygame.K_w: "up",
    pygame.K_s: "down",
    pygame.K_a: "left",
    pygame.K_d: "right",

    pygame.K_SPACE: "pause/unpause",
    pygame.K_ESCAPE: "quit",
}

OPPOSITE_DIRECTIONS = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}



