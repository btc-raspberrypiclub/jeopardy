#Jeopardy Pi Edition
Version 0.1.0 Beta

##Software Quick Start for Raspberry Pi
1. Flash the latest edition of Raspbian to your Raspberry Pi.
2. Update your Raspberry Pi with the commands `sudo apt-get update` and `sudo apt-get upgrade`
3. Clone the JeoparPy code with the command `sudo git clone https://github.com/spadgenske/JeoparPy.git
4. In the home JeoparPy directory start the software for the first time with the command `sudo start.py`

The software should start up for you to mess around with.

#Setup Your Own Game
JeoparPy does not come with any set(s) of questions/catagories so you must add them in. </br>

1. Navigate to the games directory with the command `cd JeoparPy/games`</br>
2. Each of the four directories in this directory are games. Rename one of them to the name you desire. (For 
example, "American History")</br>
3. Enter the game directory you just renamed. Open the file `players.txt`</br>
4. Each line of the file is a player/team name. Change a line to change the name. Save the file.<br/>
5. Open the file `clues.txt`</br>
6. Every line is a question. The first 5 lines are for the first category. The next 5 lines are for the second 
catagory and so on.</br>
7. Close and save the file. Finally open the `catgories.txt` file. Each line of this file is a category. Change
at will.</br>

HOW TO HOST A GAME
==================
To start the game, run ``start.py`` located in the `/home/pi/JeoparPy` directory.

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
keyboard. It is recommended to map a controller of some kind to these keys. <a href="https://github.com/spadgenske/Jeopardy#connecting-hardware">See Connecting Hardware</a>

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

#Connecting Hardware
Coming Soon!

