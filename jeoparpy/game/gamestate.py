"""
gamestate.py

DESCRIPTION:
  Includes Enum, GameState, StateSetError, and StateTransitionError classes, 
  described below.
  
  
Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""
from ..config import DEBUG

##############################################################################
class Enum(object):
    """
    Defines an enum-like object.
    A list of names is given which become the enum's elements.
    Elements' integer values assigned in order in which names are passed.

    Ex: days = Enum(('SUNDAY', 'MONDAY', 'TUESDAY'), 1)
        print days.SUNDAY -> '1'
        print days.MONDAY -> '2'
        print days.TUESDAY -> 3
    """
    def __init__(self, names, start=0):
        vals = range(start, start + len(names))
        self.__dict__ = dict(zip(names, vals))

class GameState(Enum):
    """
    The state of a game can be accessed and set from this object. Only one 
    state is allowed at any time. The purpose of a GameState object is to 
    provide a single object to pass around minimal information about the 
    current state of the game to whatever may need it (generally the UI).
    
    State names are passed to __init__, which then become attributes of the 
    class used to check and set the state. For example, if 'STATE1' and 
    'STATE2' are given, an instance of this class, gs, will have gs.STATE1 
    and gs.STATE2 attributes that can be used to check and set the state.
    
    Additional data about the state can be set and accessed with the
    'kwargs' attribute, which is a dictionary. 
    
    IMPORTANT NOTE: 'kwargs' is emptied every time the state is set to 
    prevent unnecessary or outdated data from lingering. The current arguments
    can be re-sent with gs.set(gs.NEW_STATE, **gs.kwargs), but this should
    be done with discretion.
    
    'kwargs' can be set in two ways:
      1) Directly, e.g. gameState.kwargs = {'arg':arg, ...}
      2) As **kwargs to the 'set' method, e.g. with 
         gameState.set(gameState.STATE, arg=value, arg2=value)
    
    EXAMPLE USAGE:
      gs = GameState('STATE1', 'STATE2', 'STATE3')
      
      # Set state
      gs.state = gs.STATE1
      
      # Compare state
      if gs.state == gs.STATE1:
          gs.state = gs.STATE2
          
      # Set kwargs
      gs.state = set(gs.STATE3, extraArg1=1, extraArg2=2)
      
      # Get kwargs
      extraArg1 = gs.state.kwargs['extraArg1']

    ATTRIBUTES:
      * kwargs
      * previous (read-only)
      * state
      
    METHODS:
      * set
    """
    def __init__(self, *stateNames):
        """
        Constructor. The names contained in 'stateNames' become the
        objects attribute names that define states (see Enum and/or this
        class's docstring).
        """
        super(GameState, self).__init__(stateNames)
        self._numStates = len(set(stateNames))
        self._state = None
        self._previous = None
        self.kwargs = {}

    def __repr__(self):
        if not self.kwargs:
            return repr(self.state)
        else:
            return '{0} {1}'.format(self.state, self.kwargs)
            
    def set(self, state, **kwargs):
        self.state = state  # Note state.setter clears self.kwargs to {} 
        self.kwargs.update(kwargs)
        
        if DEBUG and self.kwargs:
            print('State args set: {0}'.format(self.kwargs))
        
    def _verify_transition(self, newState):
        """
        state.setter calls this function to verify that a transition is 
        valid. If any custom transition rules are desired, they should be
        placed here (or an inheriting class should override this method).
        """
        if self._state == newState:
            raise StateTransitionError("Cannot transition a state to" +
                " itself.", self._state, newState)

    @property
    def previous(self):
        return self._previous
        
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        # Attempt cast to int
        try:
            val = int(val)
        except (ValueError, TypeError):
            raise StateSetError("'State' expects integer, not {0}.".format(
                type(val).__name__), val)

        # Verify state within valid range of defined states
        if val not in range(self._numStates):
            raise StateSetError("Set of 'State' attempted with value " +
                "that has no assigned state.", val)
        
        self._verify_transition(val)
        
        self._previous = self._state
        self._state = val
        self.kwargs = {}
        
        if DEBUG:
            print("State change: {0}".format(self))

class JeopGameState(GameState):
    """
    Defines the states for a JeoparPy game.

    This and GameData are the primary interfaces
    between the main module and the game logic.

    This also serves as a centralized means of communication
    between main and the UI modules.

    METHODS:
      * transition_state_immediate_linear
    """
    def __init__(self):
        #Define states
        states = (
            'BOARD_FILL',
            'WAIT_BOARD_FILL',
            'WAIT_CHOOSE_CLUE',
            'CLICK_CLUE',
            'WAIT_CLUE_OPEN',
            'CLUE_OPEN',
            'WAIT_CLUE_READ',
            'WAIT_TRIGGER_AUDIO',
            'PLAY_CLUE_AUDIO',
            'START_CLUE_TIMER',
            'WAIT_BUZZ_IN',
            'BUZZ_IN',
            'WAIT_ANSWER',
            'ANSWER_CORRECT',
            'ANSWER_INCORRECT',
            'ANSWER_TIMEOUT',
            'ANSWER_NONE',
            'DELAY',
            'GAME_END',
            'QUIT')
        
        super(JeopGameState, self).__init__(*states)

        #Define state ranges
        self.ANSWER = range(self.ANSWER_CORRECT, self.ANSWER_INCORRECT + 1)

        #Set initial state
        self.state = self.BOARD_FILL

    def transition_state_immediate_linear(self, gameData):
        """
        Handle any simple state transitions; i.e. those that always
        occur immediately and have a single next state (no branching).

        State transitions triggered by events, or whose next state
        branches on conditions occur elsewhere.
        """
        s = self
        
        if s.state == s.BOARD_FILL:
            s.state = s.WAIT_BOARD_FILL
            
        elif s.state == s.CLICK_CLUE:
            coords = s.kwargs['coords']
            s.set(s.WAIT_CLUE_OPEN, coords=coords)
            
        elif s.state == s.START_CLUE_TIMER:
            amount = s.kwargs['amount']
            s.set(s.WAIT_BUZZ_IN, amount=amount)

        elif s.state == s.PLAY_CLUE_AUDIO:
            column = s.kwargs['coords'][1]
            s.set(s.WAIT_BUZZ_IN, amount=gameData.amounts[column])

        elif s.state == s.BUZZ_IN:
            playerI = s.kwargs['playerI']
            amount = s.kwargs['amount']
            s.set(s.WAIT_ANSWER, playerI=playerI, amount=amount)

        elif s.state == s.ANSWER_CORRECT:
            s.state = s.DELAY

        elif s.state in (s.ANSWER_NONE, s.ANSWER_TIMEOUT, s.DELAY):
            s.state = s.WAIT_CHOOSE_CLUE

##############################################################################
class StateSetError(Exception):
    """
    Exception raised when a problem occurs setting State in GameState.
    """
    def __init__(self, msg='', errVal=None):
        self.msg = (msg if msg 
            else "An error occured when trying to set 'State.'")

        self.errVal = errVal

    def __str__(self):
        addendum = (" It is recommended to use the named constants " +
                    "defined in %s to set State." % __file__)
        if not self.errVal == None:
            addendum += " Bad value: %r" % self.errVal

        return self.msg + addendum

class StateTransitionError(Exception):
    """
    Exception raised on an invalid transition, e.g. after attempting 
    to transition from a state to the same state.
    """
    def __init__(self, msg='', previous=None, attempted=None):
        self.msg = (msg if msg 
            else "An error occured when transitioning states.")

        self.previous = previous
        self.attempted = attempted

    def __str__(self):
        addendum = ''
        if self.previous is not None and self.attempted is not None:
            addendum = ' Previous state: {0}; Attempted state: {1}'.format(
                self.previous, self.attempted)

        return self.msg + addendum
