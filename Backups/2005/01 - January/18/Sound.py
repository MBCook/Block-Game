import pygame

# Globals

global placeSound, forcedSound, badplaceSound
global badmoveSound, gameoverSound, removedSound, gothighSound
global soundEnabled

# The rest

def initSound():
    """Prepare the sound system by loading sounds and whatnot."""

    global placeSound, forcedSound, badplaceSound
    global badmoveSound, gameoverSound, removedSound, gothighSound
    global soundEnabled

    soundEnabled = False

    # Load up all our sounds

    placeSound = pygame.mixer.Sound("place.wav")
    forcedSound = pygame.mixer.Sound("forced.wav")
    badplaceSound = pygame.mixer.Sound("badplace.wav")
    badmoveSound = pygame.mixer.Sound("badmove.wav")
    gameoverSound = pygame.mixer.Sound("gameover.wav")
    removedSound = pygame.mixer.Sound("removed.wav")
    gothighSound = pygame.mixer.Sound("gothigh.wav")

    # Did it work?

    if ((placeSound != None) or (forcedSound != None) or
        (badplaceSound != None) or (badmoveSound != None) or
        (gameoverSound != None) or (removedSound != None) or
        (gothighSound != None)):
        soundEnabled = True
    else:
        print "Unable to load all sound files, sound disabled."

def playSound(theSound):
    """Play the sound for the given action"""

    global placeSound, forcedSound, badplaceSound
    global badmoveSound, gameoverSound, removedSound, gothighSound
    global soundEnabled

    if soundEnabled == False:
        return

    if theSound == "Place":
        placeSound.play()
    elif theSound == "Forced":
        forcedSound.play()
    elif theSound == "Bad Place":
        badplaceSound.play()
    elif theSound == "Bad Move":
        badmoveSound.play()
    elif theSound == "Game Over":
        gameoverSound.play()
    elif theSound == "Removed":
        removedSound.play()
    elif theSound == "Got High":
        gothighSound.play()
    else:
        print "Unable to play sound, unknown sound \"%s\"" % (theSound)
        
def stopAll():
    """Stop playing all sounds"""

    global soundEnabled

    if soundEnabled:
        pygame.mixer.stop()
