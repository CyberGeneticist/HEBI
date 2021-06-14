# Python 3.9.5
import pygame

GAME_NAME = "Snake"

START_PAUSED = True
ALLOW_PAUSING = True
FULLSCREEN = True
MOUSE_VISIBLE = False
PICK_RANDOM_THEME = True
SLEEP_AFTER_GAME_OVER = True

DEFAULT_REFRESH_RATE = 60
GAME_OVER_DELAY = 1

ALTERNATIVE_RESOLUTION = (1280, 720)  # TODO test a variety of resolutions
RESOLUTION = (0, 0) if FULLSCREEN else ALTERNATIVE_RESOLUTION

TARGET_SQUARE_SIZE = 50

SCORE_FONT_SIZE = 70
SCORE_ALPHA = 100
LARGE_MENU_FONT_SIZE = 130
SMALL_MENU_FONT_SIZE = 50

DARK_SURFACE_ALPHA = 127

MENU_FADE_IN_SPEED = 6
MENU_FADE_OUT_SPEED = 6
GAME_PAUSED_OVERLAY_FADE_IN_SPEED = 6

DEFAULT_MUSIC_VOLUME = 0.5
DEFAULT_SOUND_EFFECTS_VOLUME = 0.8

SAVE_FILE_PATH = "./save.json"
SETTINGS_FILE_PATH = "./settings.json"


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



