# Python 3.9.5
from collections import namedtuple
from random import randint

Colour = namedtuple("Colour", ("red", "green", "blue"))  # TODO rename element names

themes = {
    "randomised": {  # This randomises at the time of import, which means it stays the same for the run of the program.
        "background": Colour(randint(0, 255), randint(0, 255), randint(0, 255)),
        "snake": Colour(randint(0, 255), randint(0, 255), randint(0, 255)),
        "food": Colour(randint(0, 255), randint(0, 255), randint(0, 255)),
        "walls": Colour(randint(0, 255), randint(0, 255), randint(0, 255)),
        "text": Colour(randint(0, 255), randint(0, 255), randint(0, 255)),
    },

    "pink": {
        "background": Colour(244, 194, 194),
        "snake": Colour(255, 57, 136),
        "food": Colour(252, 15, 192),
        "walls": Colour(231, 84, 128),
        "text": Colour(255, 255, 255),
    },

    "emma first": {
        "background": Colour(244, 194, 194),
        "snake": Colour(164, 244, 208),
        "food": Colour(92, 235, 170),
        "walls": Colour(229, 99, 153),
        "text": Colour(255, 255, 255),
    },

    "wild orchid": {
        "background": Colour(214, 107, 160),
        "snake": Colour(229, 169, 169),
        "food": Colour(244, 228, 186),
        "walls": Colour(175, 77, 152),
        "text": Colour(157, 247, 229),
    },

    "blue": {
        "background": Colour(19, 64, 116),
        "snake": Colour(11, 37, 69),
        "food": Colour(141, 169, 196),
        "walls": Colour(19, 49, 92),
        "text": Colour(238, 244, 237),
    },

    "striking red and orange": {
        "background": Colour(222, 60, 75),
        "snake": Colour(251, 245, 243),
        "food": Colour(226, 132, 19),
        "walls": Colour(196, 40, 71),
        "text": Colour(0, 0, 34),
    },

    "matrix": {
        "background": Colour(2, 2, 4),
        "snake": Colour(32, 72, 41),
        "food": Colour(34, 180, 85),
        "walls": Colour(128, 206, 135),
        "text": Colour(146, 229, 161),
    },

    "emi": {
        "background": Colour(242, 181, 212),
        "snake": Colour(123, 223, 242),
        "food": Colour(239, 247, 246),
        "walls": Colour(247, 214, 224),
        "text": Colour(178, 247, 239),
    },

    "ugly": {
        "background": Colour(60, 22, 66),
        "snake": Colour(8, 99, 117),
        "food": Colour(175, 252, 65),
        "walls": Colour(29, 211, 176),
        "text": Colour(178, 255, 158),
    },

    "hazy pastel": {
        "background": Colour(231, 198, 255),
        "snake": Colour(255, 214, 255),
        "food": Colour(200, 182, 255),
        "walls": Colour(187, 208, 255),
        "text": Colour(184, 192, 255),
    },

    "snazzy yellow on dark": {
        "background": Colour(0, 8, 20),
        "snake": Colour(255, 214, 10),
        "food": Colour(255, 195, 0),
        "walls": Colour(0, 29, 61),
        "text": Colour(0, 53, 102),
    },

    "greens and blues": {
        "background": Colour(199, 249, 204),
        "snake": Colour(87, 204, 153),
        "food": Colour(56, 163, 165),
        "walls": Colour(34, 87, 122),
        "text": Colour(128, 237, 153),
    },
}


def get_complementary_colour(colour):
    # This function expects an (r, g, b) tuple as 'colour' argument:
    if min(colour) < 0 or max(colour) > 255:
        raise ValueError("'colour' argument in 'get_complementary_colour' should be an (r, g, b) tuple with each element an int from 0 to 255 inclusive.")

    complementary_colour = tuple(255 - subcolour for subcolour in colour)
    return complementary_colour
