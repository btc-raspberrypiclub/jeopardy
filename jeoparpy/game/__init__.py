"""
jeoparpy.game

DESCCRIPTION:
  The game subpackage contains the JeoparPy game logic and any constants 
  needed only within this package.

USAGE:
  Main should make direct use of only single instances of JeopGameState 
  (found in gamestate.py) and GameData. These two objects hold information
  about the game logic designed to be visible to and setable by outside 
  packages.
  
CUSTOMIZATION:
  See the "Customization" section of the README for details on how to
  alter the resource files from which the game data is built.
"""
from .gamedata import GameData
from .gamestate import JeopGameState
