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
3. You may need to install dependencies. To do so, open a terminal, e.g. the command prompt on Windows, then enter each line:
```python
pip install pygame
pip install pywin  # Install this one only if you are on Windows
```
5. Run the 'main.py' file to start the game.


## Controls
- WSAD or arrow keys - movement direction
- SPACE - pause/unpause the game
- ENTER or SPACE in menus - confirm selection
- In 'options' and 'scores' menus, LEFT / RIGHT and A / D lets you toggle options.



## Known issues
- Not all resolutions will work at the moment :x:. Tested working :heavy_check_mark: at 1920 x 1080 and 2560 x 1080.
- Rarely, when starting a new game, the snake will not move from its initial position. Quitting to main menu and playing a new game fixes this. Bug origin being investigated.
- The snake's movement is not as fluid as it could be, as the snake moves only in fixed squares. Considering how to implement intermediate states being drawn. Ideas welcome.

## Version history
#### v. 0.3.1 - 14 June 2021
- Hotfix for an issue where the program would not run correctly on non-Windows platforms due to a
    platform-specific import. The program now utilises a conditional import to offer the best of both worlds.

#### v. 0.3.0 - 14 June 2021
- Added sound effects and music throughout the game, including in the menus:
    - There are four background music tunes right now, with one playing at random during each playthrough.
        - There are also multiple, slightly different variations of each sound effect, for sanity's sake.
    - Music pausing while the game is paused is temporarily disabled, as it was causing unexplained crashes.
        This functionality will be reinstated once the culprit is found.
    - Volume of music and sound effects can be changed independently by the user in the 'options' menu:
        - These loudness settings are permanently saved, and will be automatically used the next time the game runs.
-The game should now scale correctly to most resolutions, although some unusual resolutions may feature overly
    large or small game elements, especially text.
    - The game is still missing dynamic scaling of text to arbitrary resolutions - this is likely next on the list.
- The game now automatically detects monitor refresh rate (platform specific - should work on Windows), and sets
    an appropriately high refresh rate. If this is not possible, it defaults to 60 Hz.
- Re-written the code governing where a snake spawns at the beginning of a game to be cleaner and better.
- Reduced how close to the walls the snake can spawn - it will now spawn close to the middle every time.

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
Feel free to use with attribution (link to this repo).


## Credits
Music and most sound effects obtained from the fantastic site [ZapSplat](https://www.zapsplat.com/)  
Some sound effects from [freesound](https://freesound.org/)  
A few sound effects from [FreeSFX](https://freesfx.co.uk/Default.aspx)  



## Contact
:spider_web: [Find me here](https://linktr.ee/maciejjablonski)\
:e-mail: macjabko@gmail.com
