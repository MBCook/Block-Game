import sys
import pygame
import Video
import GameBoard
import math
import Pieces
import EventQueue

# Globals

global theClock, theBoard, thePiece
global pieceX, pieceY, idealX, idealY
global borderWidth, borderHeight
global theEventQueue

# The rest

def help():
    """Simple, print out what the keys do."""

    print ""
    print "Keys:"
    print "-----"
    print ""
    print "     c - Cycle through culling options"
    print "     f - Print out the FPS"
    print "     h - Display help (this)"
    print "     l - Toggle lighting"
    print "     p - Print light position"
    print "   q/a - Increase/Decrease light X by 0.5"
    print "   w/s - Increase/Decrease light Y by 0.5"
    print "   e/d - Increase/Decrease light Z by 0.5"
    print "arrows - Move the piece in play"
    print "   z/x - Rotate the piece (counter)clockwise"
    print " space - Place the piece"
    print ""
    print "esc - Quit"
    print ""

def main():

    global theClock, theBoard, thePiece
    global pieceX, pieceY, idealX, idealY
    global boardWidth, boardHeight
    global borderWidth, borderHeight
    global theEventQueue, timeDelta

    print ""

    pieceX = pieceY = idealX = idealY = 0.0

    boardWidth = 16
    boardHeight = 15
    borderWidth = 8
    borderHeight = 8

    angle = idealAngle = 0  # Angle is degrees rotated clockwise

    thePiece = Pieces.piecesArray[7]    # Temporary piece

    pygame.init()

    pygame.display.set_mode((640, 480), pygame.OPENGL | pygame.DOUBLEBUF)

    Video.initThings(boardWidth * 8 + borderWidth * 2,
                     boardHeight * 8 + borderHeight * 2,
                     160)

    theClock = pygame.time.Clock()
    timeDelta = 0

    prepareBoard()

    theEventQueue = EventQueue.EventQueue()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                theEventQueue.addToQueue("Program", "Quit")
            elif event.type == pygame.KEYDOWN:
                checkKeys(event)      

        theEventQueue.addToQueue("Gamestate", "Update Piece Position")
        theEventQueue.addToQueue("Video", "Redraw Buffer")
        theEventQueue.addToQueue("Video", "Swap Buffers")
        theEventQueue.addToQueue("Program", "Tick Clock")
        
        runThroughQueue()

def runThroughQueue():

    global timeDelta, theEventQueue, theClock
    global idealX, idealY, boardWidth, boardHeight

    while theEventQueue.isEmpty() == 0:
        type, info = theEventQueue.getFromQueue()
        if type == "Gamestate":
            if info == "Update Piece Position":
                updatePiecePosition(timeDelta)
            else:
                print "Unknown %s event '%s' disgarded." % (type, info)
        elif type == "Input":
            if info == "Move Piece Down":
                idealY += 8.0
                if (idealY > (boardHeight  - 3) * 8.0):
                    idealY = (boardHeight  - 3) * 8.0
            elif info == "Move Piece Left":
                idealX -= 8.0
                if (idealX < 0.0):
                    idealX = 0.0
            elif info == "Move Piece Right":
                idealX += 8.0
                if (idealX > (boardWidth  - 3) * 8.0):
                    idealX = (boardWidth  - 3) * 8.0
            elif info == "Move Piece Up":
                idealY -= 8.0
                if (idealY < 0.0):
                    idealY = 0.0
            elif info == "Place Piece":
                pass    # This is where we place the piece
            elif info == "Rotate Clockwise":
                idealAngle += 90
                if (idealAngle >= 360):
                    idealAngle -= 360
            elif info == "Rotate Counterclockwise":
                idealAngle -= 90
                if (idealAngle < 0):
                    idealAngle += 360
            else:
                print "Unknown %s event '%s' disgarded." % (type, info)
        elif type == "Program":
            if info == "Help":
                help()
            elif info == "Print FPS":
                 print "FPS: %.1f" % (theClock.get_fps())
            elif info == "Quit":
                sys.exit()
            elif info == "Tick Clock":
                timeDelta = theClock.tick(60)   # Limit ourselves to 60 FPS  
            else:
                print "Unknown %s event '%s' disgarded." % (type, info)
        elif type == "Video":
            if info == "Change Culling":
                Video.changeCulling()
            elif info == "Decrease Light X":
                Video.moveLight(-0.5, 0, 0)
            elif info == "Decrease Light Y":
                Video.moveLight(0, -0.5, 0)
            elif info == "Decrease Light Z":
                Video.moveLight(0, 0, -0.5)
            elif info == "Increase Light X":
                Video.moveLight(0.5, 0, 0)
            elif info == "Increase Light Y":
                Video.moveLight(0, 0, 0.5)
            elif info == "Increase Light Z":
                Video.moveLight(0, 0, 0.5)
            elif info == "Print Light Position":
                Video.moveLight(0, 0, 0)
            elif info == "Redraw Buffer":
                draw(timeDelta)
            elif info == "Swap Buffers":
                pygame.display.flip()
            elif info == "Toggle Lights":
                Video.toggleLights()
            else:
                print "Unknown %s event '%s' disgarded." % (type, info)
        else:
            print "Event of unknown type '%s' with info '%s' disgarded." % (type, info)

    return # Done here    

def updatePiecePosition(timeDelta):
    """Move the piece closer to it's ideal position"""

    global pieceX, pieceY, idealX, idealY    

    if ((pieceX == idealX) and (pieceY == idealY)):
        return  # If the piece is in the right spot, do nothing!

    pieceX = idealX # Just move the piece where it should be, ignore the rest
    pieceY = idealY #   for now.

    return

    if timeDelta == 0:
        return  # Speeds things up, no need to calculate stuff
    if (pieceX == idealX) and (pieceY == idealY):
        return  # No need to move, and prevents a divide by 0

    timeToMove = 125.0    # Piece can move two blocks (16 units) every 125 ms

    xDiff = idealX - pieceX
    yDiff = idealY - pieceY

    diffDist = xDiff * xDiff + yDiff * yDiff
    diffDist = math.sqrt(diffDist)

    # Are we going to get to the point this cycle?

    if (diffDist <= (16.0 * (timeDelta / timeToMove))):
        # Yes! So just move us there and save us some calculations
        pieceX = idealX
        pieceY = idealY
        return

    # OK, this next part is not black magic. It's the origional position plus the change.
    # The change is equal to 8 (maximum movement rate) * the percentage (to keep it from
    #   moving too fast, you see this as timedelta/timeToMove) times sin or cos
    #   (_diff / diffDist) so that even when moving diagonol, we still don't go too fast.

    if xDiff != 0:
        pieceX = pieceX + ((timeDelta / timeToMove) * 8 * (xDiff / diffDist))
    if yDiff != 0:
        pieceY = pieceY + ((timeDelta / timeToMove) * 8 * (yDiff / diffDist))

    # OK, we've moved. Now let's just hope this works. (edit: it does!)

def prepareBoard():
    """Make a simple gameboard for testing purposes"""

    global theBoard

    theBoard = GameBoard.GameBoard()    # 16x15, secret square at 0,0. This is the default
    
    listOne = [1, 1, 100]
    listTwo = [1, 2, 100]
    listThree = [1, 3, 100]

    theBoard.setList(5, 5, listOne)
    theBoard.setList(6, 6, listTwo)
    theBoard.setList(7, 7, listThree)

def checkKeys(event):    
    """Check the keypresses to see if we care."""

    global theEventQueue
    
    if event.key == pygame.K_ESCAPE:
        theEventQueue.addToQueue("Program", "Quit")
    elif event.key == pygame.K_c:
        theEventQueue.addToQueue("Video", "Change Culling")
    elif event.key == pygame.K_h:
        theEventQueue.addToQueue("Program", "Help")
    elif event.key == pygame.K_l:
        theEventQueue.addToQueue("Video", "Toggle Lights")
    elif event.key == pygame.K_p:
        theEventQueue.addToQueue("Video", "Print Light Position")
    elif event.key == pygame.K_q:
        theEventQueue.addToQueue("Video", "Increase Light X")
    elif event.key == pygame.K_a:
        theEventQueue.addToQueue("Video", "Decrease Light X")
    elif event.key == pygame.K_w:
        theEventQueue.addToQueue("Video", "Increase Light Y")
    elif event.key == pygame.K_s:
        theEventQueue.addToQueue("Video", "Decrease Light Y")
    elif event.key == pygame.K_e:
        theEventQueue.addToQueue("Video", "Increase Light Z")
    elif event.key == pygame.K_d:
        theEventQueue.addToQueue("Video", "Decrease Light Z")
    elif event.key == pygame.K_f:
        theEventQueue.addToQueue("Program", "Print FPS")
    elif event.key == pygame.K_UP:
        theEventQueue.addToQueue("Input", "Move Piece Up")
    elif event.key == pygame.K_DOWN:
        theEventQueue.addToQueue("Input", "Move Piece Down")
    elif event.key == pygame.K_LEFT:
        theEventQueue.addToQueue("Input", "Move Piece Left")
    elif event.key == pygame.K_RIGHT:
        theEventQueue.addToQueue("Input", "Move Piece Right")
    elif event.key == pygame.K_SPACE:
        theEventQueue.addToQueue("Input", "Place Piece")
    elif event.key == pygame.K_z:
        theEventQueue.addToQueue("Input", "Rotate Counterclockwise")
    elif event.key == pygame.K_x:
        theEventQueue.addToQueue("Input", "Rotate Clockwise")

def draw(timeInMS):
    """Draw the scene for us"""

    global theBoard, thePiece, pieceX, pieceY
    global boardWidth, boardHeight
    global borderWidth, borderHeight

    Video.sinkEm(theBoard, timeInMS)
    
    Video.startDrawing()

    Video.drawHolder(boardWidth, boardHeight, borderWidth, borderHeight)
    Video.drawBlocksInBoard(theBoard, boardWidth, boardHeight,
                            borderWidth, borderHeight)
    Video.drawPiece(pieceX, pieceY, thePiece, 4, borderWidth, borderHeight)

    Video.finishDrawing()

if __name__ == "__main__":
    main()

