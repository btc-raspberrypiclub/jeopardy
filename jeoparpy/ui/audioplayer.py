import pygame

from .resmaps import SOUNDS, CLUE_READS

###############################################################################
class AudioPlayer(object):
    """
    Inits and holds a dictionary of pygame.mixer.Sound objects,
    and provides basic functionality (play, stop, fadeout, etc.)
    by providing aliases to pygame.mixer functions.

    ATTRIBUTES:
      * sounds

    METHODS:
      * fadeout
      * play
      * set_volume
      * stop
      * stop_all
      * wait_until_sound_end
    """
    def __init__(self, namePathMap={}):
        """
        namePathMap expects key, value pairs of a descriptive
        name and a full path to a sound file. self.sounds
        will be built automatically from this, if provided.

        By default, creates one Sound object for each ditinct path.
        Thus, names pointing to the same path in namePathMap
        will result in names in self.sounds pointing to the same
        object.

        Users or Subclasses can alter how self.sounds is filled or
        its type, as long as it is indexable and its values are
        pygame.mixer.Sound objects.
        """
        self.sounds = {}

        if namePathMap is not None:
            self._soundset = {}
            for path in set(namePathMap.values()):
                self._soundset[path] = pygame.mixer.Sound(path)

            for name, path in namePathMap.items():
                self.sounds[name] = self._soundset[path]

    def fadeout(self, ms, name=None):
        """
        If 'name' provided, fades out that specific sound.
        Otherwise, fades out all sounds (alias to pygame.mixer.fadeout).
        """
        if name:
            try:
                self.sounds[name].fadeout(ms)
            except KeyError:
                raise MissingSoundError(name)
        else:
            pygame.mixer.fadeout(ms)

    def fadeout_all(self, ms):
        pygame.mixer.fadeout(ms)

    def play(self, name, loops=0, maxtime=0, fade_ms=0):
        try:
            self.sounds[name].play(loops, maxtime, fade_ms)
        except KeyError:
            raise MissingSoundError(name)

    def set_volume(self, name, vol):
        
        try:
            self.sounds[name].set_volume(vol)
        except KeyError:
            raise MissingSoundError(name)

    def stop(self, name):
        try:
            self.sounds[name].stop()
        except KeyError:
            raise MissingSoundError(name)

    def stop_all(self):
        """Alias to pygame.mixer.stop()"""
        pygame.mixer.stop()

    # TODO find a better way to accomplish this.
    # This version is very inconsistent
    def wait_until_sound_end(self, extraDelay=0):
        """
        Return control when pygame.mixer.get_busy returns False.

        If extraDelay given, pygame.time.wait will be called with
        extraDelay as the argument.
        """
        while pygame.mixer.get_busy():
            pass

        if extraDelay > 0:
            pygame.time.wait(extraDelay)

###############################################################################
class JeopAudioPlayer(AudioPlayer):
    """An AudioPlayer with JeoparPy sounds initialized."""
    def __init__(self):
        reads = {}
        for pos, path in CLUE_READS.items():
            key = pos + ('cr', )
            reads[key] = path
            
        super(JeopAudioPlayer, self).__init__(dict(SOUNDS, **reads))

###############################################################################
class MissingSoundError(Exception):
    def __init__(self, name):
        self.errVal = name

    def __str__(self):
        return ("Name %r does not refer to an existing sound " % self.errVal +
                "in this instance of AudioPlayer.sounds." )
