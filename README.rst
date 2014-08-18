==================
JeoparPy! v0.9.4.1
==================

********
CONTENTS
********

1. `General Info`_
2. Setup_
3. Controls_
4. `Quick Start`_
5. `Optional Arguments`_
6. `Detailed Instructions`_

  a. `How to Host a Game`_
  b. `Customization`_

7. `Known Issues`_
8. Legal_


.. _`General Info`:

************
GENERAL INFO
************

WHAT JEOPARPY IS
================

JeoparPy allows users to customize and host a game 
that includes all the sights, sounds, and excitement
of a TV quiz show! (...that is legally distinguishable 
from any such show).

It is ideal for use in a classroom setting, or as a party/shower game.

WHAT JEOPARPY IS NOT
====================

JeoparPy does NOT include any pre-made sets of categories and clues,
except for placeholders to aid in formatting your own.
It is instead only designed to be used to host custom games that the 
user creates.


GAME DESCRIPTION
================

Three individuals or teams compete for the highest score,
attained by correctly answering questions.
Generally, the questions posed to the players are phrased
as "answers," to which the player must provide the correct
"question," using terminology such as "What is \_\_\_?" or "Who is \_\_\_?".

Users can customize category names, clues, player names, and dollar amounts.
An image can be used to accompany a clue.

By mapping controllers to the buzz-in keys, players can buzz themselves in.
For example, the author used Bluetooth to sync Wiimotes 
to the PC. Doing this is up to the user, as instructions to 
do so are beyond the scope of this document.

One user must "host" a game by choosing clues and telling the game whether
players answered correctly or incorrectly.


.. _Setup:

*****
SETUP
*****

The following are required to run JeoparPy:

* Python 2.7 (http://www.python.org/download/)
* Pygame (http://www.pygame.org/download.shtml)

Please note that the game has only been tested with:

* Python 2.7.3 32-bit
* Pygame 1.9.2 32-bit

JeoparPy has been tested on the following platforms:

* Windows 7 64-bit
* Ubuntu 10.10
* Xubuntu 13.10
  
Prior to first run:
===================
Open file ``<jeoparpy root>/jeoparpy/config.py`` and set your preferred 
display resolution. Follow the instructions in the file.


.. _Controls:  

********
CONTROLS
********

For more detailed instructions on how/when to use these controls, 
see the Instructions section below.

* LEFT-CLICK: Opens a clue if a clue box is clicked on the main game board.
* 1/2/3:      These keys are used to buzz in the corresponding player.
* SPACEBAR:   Press when a clue is answered correctly
* BACKSPACE:  Press when a clue is answered incorrectly
* END:        Press when time runs out on a clue to close it
* Q:          Press to trigger the end of the game and the credits.
* SHIFT+Q:    Press to close the game immediately. 


.. _`Quick Start`:

***********
QUICK START
***********

0. Read the "Setup" and "Controls" sections of this document.

1. Clone the JeoparPy repository 
   (``git clone git://github.com/adambeagle/jeoparpy.git`` at the command 
   line) or click "Download ZIP" at 
   `JeoparPy's Github page <http://github.com/adambeagle/jeoparpy>`_ and 
   unzip the downloaded .zip file.

2. On Windows, double-click ``Start_JeoparPy.bat`` to run the game. 
   On Linux, run ``start.py`` in the root folder. Ideally, run it 
   optimized using ``python -OO start.py``. Assuming no changes have
   been made to the files in ``res/`` the game will run with sample
   questions showcasing the available clue types.


.. _Optional Arguments:

******************
OPTIONAL ARGUMENTS
******************

There are several optional arguments that can be passed to ``start.py``:

* ``-f`` or ``--fullscreen`` will force the game to run in fullscreen mode.
  This overrides the ``FULLSCREEN`` setting in ``jeoparpy/config.py``.
    
* ``-w`` or ``-windowed`` will force the game to run in windowed mode.
  This overrides both the ``FULLSCREEN`` setting in 
  ``jeoparpy/config.py`` and the ``-f`` or ``-fullscreen`` arguments
  if either is also passed.
    
* ``-s`` or ``--skip-intro`` will skip the intro sequences (title sequence,
  rules screen, and category scroll) and open the game at the main game
  board. This may be useful when testing customized games.

* ``-d`` or ``--debug`` will turn debug mode on. Typical users should not need 
  this option.
  
Example usage: ``python start.py -f -s`` would run the game in fullscreen,
skipping the intro sequences.


.. _`Detailed Instructions`:

*********************
DETAILED INSTRUCTIONS
*********************

.. _`How to Host a Game`:

**WARNING:** *It is important that a game host read these instructions. 
The game is designed to have a seamless presentation to the players, 
thus instructions for its use do not appear onscreen.*

HOW TO HOST A GAME
==================
To start the game, run ``start.py`` located in the same folder as this
document. On Windows, run ``Start_JeoparPy.bat``, also located in the 
root directory.

Upon starting, an introduction will be played. 
When the subtitle appears, press any key to display the rules screen.

To exit the rules screen, press any key.

The categories will now scroll by, requiring no input.

The main game screen will then be displayed, and an animation will play 
filling in the dollar amounts.

At any point during the primary game, Shift+Q can be pressed to 
immediately exit the game. Pressing only 'Q' will trigger the 
end-of-game animations and credits.

You now have control of the mouse. Click a clue box to display it.

If an audio reading of the clicked clue is available, it is played 
immediately, and players can not buzz in until it has finished playing.

When a clue box is open, a player is buzzed in by pressing their corresponding
number on the keyboard. Example: To buzz-in player 2, press '2' on your 
keyboard. It is recommended to map a controller of some kind to these keys.

When a player is buzzed in, one of three things can happen:

* Press spacebar if the player answers correctly. The clue will be closed and
  the game board will return.
* Press 'Backspace' if the player answers incorrectly. Another player can now 
  buzz in. The player that answered incorrectly can not buzz in again on the 
  same question.
* A player fails to answer within the time limit (note the timer at the top
  of a podium after a player buzzes in). This has the same end result as
  pressing 'backspace' above.

If the ``CLUE_TIMEOUT_MS`` option is set the clue will automatically close 
after the amount of time set if no player has buzzed in. If no timeout time is
provided, press 'End' to close the clue and return to the game board if no one
is going to answer. See the instructions in ``jeoparpy/config.py`` for
information about how the clue timer works, as it has specific behavior for
audio clues or clues with audio readings.

Any clue previously opened can be reopened. 
So, if a clue is clicked by mistake, press 'End.' Its dollar amount will be 
cleared off the board, but it can be reopened and a player can win its amount 
as normal. This method can be used to correct mistakes in scoring, though 
money can not be subtracted from a player's total at this point.

When you wish to end the game (usually when all clues have been completed), 
press 'Q.' This will trigger a 'Congratulations' message to the winner(s), 
and then display the game credits. Alternatively, Shift+Q will quit the game 
immediately.

No input is necessary once the end-of-game animations are triggered, but if 
you wish to quit the game during the credits, you can press 'Q.' The game will
close automatically after the credits.


.. _Customization:

CUSTOMIZATION
=============

*Note: It is recommended that the game be run once as-is to view the 
example questions and to ensure the game runs without any problems.*

Display/General game settings:
------------------------------
* Located in ``<jeoparpy root>/jeoparpy/config.py`` are settings for 
  screen resolution and toggling fullscreen display, as well as general 
  game settings such as the answer time limit.

Clues/Categories/Edition Title/Player Names/Clue Amounts/Rules:
---------------------------------------------------------------
* The files for these are all located in ``<jeoparpy root>/games/``
* In each folder of the games directory there is a game.
* Each file has sample data included.
* Rename a folder in the games directory to rename a game.
* Maximum of four (4) games. Minimum of one (1) game.
* Instructions for each are found in ``/games/<game>/INSTRUCTIONS.txt``
  
Clue Audio/Images
-----------------
* Follow the instructions in ``<jeoparpy root>/jeoparpy/ui/resmaps.py``
  to add your own images/audio to clues, or use an audio reading for a clue.
    

	
.. _`Knownn Issues`:

************
KNOWN ISSUES
************

1. When in windowed mode, moving the game window at certain times 
   (primarily during portions of the intro sequences) may cause the game 
   to freeze momentarily.
	 

.. _Legal:
 
*****
LEGAL
*****

All code contained in this package
Copyright (C) 2013 Adam Beagle - All Rights Reserved

You may use, distribute, and modify this code under the 
terms of the GNU General Public License, 
viewable at http://opensource.org/licenses/GPL-3.0

No copyright infringement is intended with the use of any file contained 
within this package. The use of any copyrighted works in this program was 
done under the Fair Use doctrine, however any infringing file will gladly 
be removed and replaced upon request. This program is non-commercial and 
was created for educational purposes.
