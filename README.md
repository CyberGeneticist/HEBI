# HEBI
## What is HEBI ?
#### Hebi is Japanese :japan: for snake :snake:.
\
HEBI is a Snake-like **game** :video_game: built with Python and [pygame](https://github.com/pygame).

HEBI started its life as a learning project, expanding upon learning from [Teclado](https://www.teclado.com/)'s 30 Days of Python course.

HEBI features a classic Snake gameplay, with original twists.


#### Unique features include:
- Variable themes which change on every playthrough, guaranteeing a fresh experience each time.
- Convenient ability to pause the gameplay.
- Pleasant animations between menus.
- More coming!


## How to install and use
1. If you do not have it installed already, download Python version 3.9 or newer from [Python Official Website](https://www.python.org/downloads/).
2. Copy/download this repository.
3. Run the 'main.py' file to start the game.


## Controls
- WSAD or arrow keys - movement direction
- SPACE - pause/unpause the game
- ENTER or SPACE in menus - confirm selection



## Known issues
##### As of v. 0.1.0:
- Not all resolutions will work at the moment :x:. Tested working :heavy_check_mark: at 1920 x 1080 and 2560 x 1080.
- Rarely, when starting a new game, the snake will not move from its initial position. Quitting to main menu and playing a new game fixes this. Bug origin being investigated.
- The snake's movement is not as fluid as it could be, as the snake moves only in fixed squares. Considering how to implement intermediate states being drawn. Ideas welcome.

## Version history
#### v. 0.2.0 - 6 June 2021
- The main change is the addition of a score system:
  - The game now prompts the user for a name, which it associates with the score for that run (or multiple consecutive runs if 'play again' selected after dying).
  - The game now keeps a copy of all user name-score associations in a JSON file:
    - In the future, this will likely be encrypted or obfuscated to make it harder to alter the scores.
  - The 'scores' menu option now has an early implementation, allowing players to view all previous scores, in a descending order.

#### v. 0.1.0 - 25 May 2021
- Initial release.
- Game in playable state.
- Some key functionality awaits implementation. These include, but are not limited to:
  - Support for any common resolution and refresh rate.
  - Music and sound effects.
  - 'Scores' and 'Options' sections, including permanent storage of scores.
  - A wider selection of themes.


## License
_Work in progress_


## Contact
[Find me here](https://linktr.ee/maciejjablonski)\
or email me at :e-mail: macjabko@gmail.com
