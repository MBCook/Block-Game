import sys
import pygame
import Video
import GameBoard

# Globals

global theClock, theBoard

# The rest

def help():
    """Simple, print out what the keys do."""

    print ""
    print "Keys:"
    print ""
    print "c - Cycle through culling options"
    print "f - Print out the FPS"
    print "h - Display help (this)"
    print "l - Toggle lighting"
    print "p - Print light position"
    print "q/a - Increase/Decrease light X by 0.5"
    print "w/s - Increase/Decrease light Y by 0.5"
    print "e/d - Increase/Decrease light Z by 0.5"
    print ""
    print "esc - Quit"
    print ""

def main():

    global theClock, theBoard

    print ""

    pygame.init()

    pygame.display.set_mode((640, 480), pygame.OPENGL | pygame.DOUBLEBUF)

    Video.initThings(144, 136, 160)

    theClock = pygame.time.Clock()
    timeDelta = 0

    prepareBoard()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                checkKeys(event)
                
        draw(timeDelta)
        pygame.display.flip()
        timeDelta = theClock.tick(60)   # Limit ourselves to 60 FPS        

def prepareBoard():
    """Make a simple gameboard for testing purposes"""

    global theBoard

    theBoard = GameBoard.GameBoard(16, 15, 13, 12) # Magic square in bottom
                                                   #    right for no reason
    listOne = [1, 1, 100]
    listTwo = [1, 2, 100]
    listThree = [2, 3, 100]

    theBoard.setList(1, 0, listOne)
    theBoard.setList(2, 1, listTwo)
    theBoard.setList(3, 2, listThree)

def checkKeys(event):    
    """Check the keypresses to see if we care."""

    global theClock
    
    if event.key == pygame.K_ESCAPE:
        sys.exit()
    elif event.key == pygame.K_c:
        Video.changeCulling()
    elif event.key == pygame.K_h:
        help()
    elif event.key == pygame.K_l:
        Video.toggleLights()
    elif event.key == pygame.K_p:
        Video.moveLight(0, 0, 0)
    elif event.key == pygame.K_q:
        Video.moveLight(0.5, 0, 0)
    elif event.key == pygame.K_a:
        Video.moveLight(-0.5, 0, 0)
    elif event.key == pygame.K_w:
        Video.moveLight(0, 0.5, 0)
    elif event.key == pygame.K_s:
        Video.moveLight(0, -0.5, 0)
    elif event.key == pygame.K_e:
        Video.moveLight(0, 0, 0.5)
    elif event.key == pygame.K_d:
        Video.moveLight(0, 0, -0.5)
    elif event.key == pygame.K_f:
        print "FPS: %.1f" % (theClock.get_fps())

def draw(timeInMS):
    """Draw the scene for us"""

    global theBoard

    Video.sinkEm(theBoard, timeInMS)
    
    Video.startDrawing()

    Video.drawHolder(16, 15, 8, 8)
    Video.drawBlocksInBoard(theBoard, 16, 15, 8, 8)

    Video.finishDrawing()

if __name__ == "__main__":
    main()

