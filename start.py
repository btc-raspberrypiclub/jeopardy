"""
start.py

DESCRIPTION:
  This script should be used to invoke the game. It allows optional
  arguments to be passed to it that can override the settings in config.py
  if desired.
  
USAGE:
  To invoke the game with an option defined below, for example -w and
  --debug, use `python start.py -w --debug'

  To define a new option:
    1) Create a new constant in constants.py. Best practice is to 
       incrememnt the value by 1 for each new flag. 
       Example: (in constants.py) NEW_FLAG = 4
    2) Ensure this file imports the new flag
    3) In this file, add one or more argv mappings to optionsMap
       Example: optionsMap = { ..., '-n' : NEW_FLAG, '--new' : NEW_FLAG }
    4) If thew new option can override a setting found in config.py,
       it must do it prior to main being imported near the end of this file.
  

Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""
from sys import argv

from jeoparpy import config
from jeoparpy.constants import (DEBUG_FLAG, FULLSCREEN_FLAG, SKIP_INTRO_FLAG, 
    WINDOWED_FLAG, DRIVE_FLAG)

optionsMap = {
    '-d'           : DEBUG_FLAG,
    '--debug'      : DEBUG_FLAG,
    '-f'           : FULLSCREEN_FLAG,
    '--fullscreen' : FULLSCREEN_FLAG,
    '-s'           : SKIP_INTRO_FLAG,
    '--skip-intro' : SKIP_INTRO_FLAG,
    '-w'           : WINDOWED_FLAG,
    '--windowed'   : WINDOWED_FLAG,
    '--drive'      : DRIVE_FLAG,
}

if __name__ == '__main__':
    rawFlags = []

    # Loop over args, add all args to rawFlags unless it is -n or the arg after it
    i = 0
    while i < len(argv):
        if argv[i] == '-n':
            i += 1
            try:
                num = int(argv[i])
                if num < 3 or num > 5:
                    print("Please specify a number of players from 3 to 5")
                    print("Or, omit it and the number of players will default to 3")
                    exit(1)
            except ValueError:
                print(f'{argv[i]} is not a valid number')
                exit(1)

            config.PLAYER_NUM = num

        elif argv[i] in ('-h', '--help'):
            print('Sorry, the help flag has not been implemented yet')
            exit(0)

        elif argv[i] in optionsMap:
            rawFlags.append(optionsMap[argv[i]])

        i += 1

    # Get rid of duplicates
    flags = set(rawFlags)
    
    # Override config options if args provided
    if FULLSCREEN_FLAG in flags:
        config.FULLSCREEN = 1
    if WINDOWED_FLAG in flags:
        config.FULLSCREEN = 0
    if DEBUG_FLAG in flags:
        config.DEBUG = 1
    if DRIVE_FLAG in flags:
        config.DRIVE = True

    # main MUST be imported here, or config options may be imported
    # (via 'from config import X') prior to being overridden by argv 
    # options.
    from jeoparpy.selectMenu import *
    select_game()
    
    from jeoparpy.main import main
    main(*flags)
    print(config.DRIVE)
