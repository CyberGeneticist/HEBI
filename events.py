# Python 3.9.5
import pygame

# Controls the delay between snake moves:
SNAKE_MOVE_EVENT = pygame.USEREVENT + 1  # The +1 or generally '+integer' is used to create unique instances - that is my best guess
SNAKE_MOVE_DELAY = 60  # Milliseconds - greater delay means slower snake
