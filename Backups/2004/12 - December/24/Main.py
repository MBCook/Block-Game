import sys
import pygame
import Video
import GameBoard
import math
import Pieces
import EventQueue
import RotateBlocks
import random

# Globals

global theClock, theBoard, thePiece, thePieceColor
global pieceX, pieceY, idealX, idealY
global borderWidth, borderHeight, extraBorder
global theEventQueue, theScore, theMultiplyer

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

    global theClock, theBoard, thePiece, thePieceColor
    global pieceX, pieceY, idealX, idealY
    global boardWidth, boardHeight
    global borderWidth, borderHeight, extraBorder
    global theEventQueue, timeDelta, theScore, theMultiplyer

    print ""

    boardWidth = 16
    boardHeight = 15
    borderWidth = 8
    borderHeight = 8
    extraBorder = 35

    pieceX = pieceY = idealX = idealY = 0.0

    theScore = 0
    theMultiplyer = 1

    random.seed()

    pygame.init()

    pygame.display.set_mode((640, 480), pygame.OPENGL | pygame.DOUBLEBUF)

    Video.initThings(boardWidth * 8 + borderWidth * 2 + extraBorder,
                     boardHeight * 8 + borderHeight * 2,
                     160)

    theClock = pygame.time.Clock()
    timeDelta = 0

    theEventQueue = EventQueue.EventQueue()

    theEventQueue.addToQueue("Gamestate", "Get New Board")
    theEventQueue.addToQueue("Gamestate", "Get New Piece")
    theEventQueue.addToQueue("Score", "Reset Score")

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
    global theBoard, thePiece, thePieceColor
    global theScore, theMultiplyer

    while theEventQueue.isEmpty() == 0:
        type, info, tuple = theEventQueue.getFromQueue()
        if type == "Gamestate":
            if info == "Check For Squares":
                squareList = theBoard.findSquaresToRemove()

                if len(squareList) > 0:
                    # Squares were found, mark 'em dead.
                    # Note that by putting "Done With Blocks" on the event queue
                    #   now, it will be executed AFTER the block scores are added
                    for i in range(len(squareList)):
                        dataTuple = (i + 1) * 100
                        theEventQueue.addToQueueFront("Score", "Block Found", dataTuple)
                        (x, y) = squareList[i]
                        theBoard.markSquareAsDead(x, y)
            elif info == "Get New Board":
                prepareBoard()
            elif info == "Get New Piece":
                idealX = idealY = pieceX = pieceY = 0.0
                thePiece = Pieces.getPiece()
                thePieceColor = random.randint(1, 7)
            elif info == "Update Piece Position":
                updatePiecePosition(timeDelta)
            else:
                print "Unknown %s event '%s' disregarded." % (type, info)
        elif type == "Input":
            if info == "Move Piece Down":

                xLoc = int(idealX / 8.0)
                yLoc = int(idealY / 8.0)

                if (yLoc <= (boardHeight - 3)):
                    if (theBoard.checkForCollision(xLoc, yLoc + 1, thePiece)  <= 0):
                        idealY += 8.0
                    else:
                        theEventQueue.addToQueueFront("Notification", "Can't Move")
                else:
                    theEventQueue.addToQueueFront("Notification", "Can't Move")
            elif info == "Move Piece Left":

                xLoc = int(idealX / 8.0)
                yLoc = int(idealY / 8.0)

                if (xLoc >= 0):
                    if (theBoard.checkForCollision(xLoc - 1, yLoc, thePiece) <= 0):
                        idealX -= 8.0
                    else:
                        theEventQueue.addToQueueFront("Notification", "Can't Move")
                else:
                    theEventQueue.addToQueueFront("Notification", "Can't Move")
            elif info == "Move Piece Right":

                xLoc = int(idealX / 8.0)
                yLoc = int(idealY / 8.0)

                if (xLoc <= (boardWidth - 3)):
                    if (theBoard.checkForCollision(xLoc + 1, yLoc, thePiece) <= 0):
                        idealX += 8.0
                    else:
                        theEventQueue.addToQueueFront("Notification", "Can't Move")
                else:
                    theEventQueue.addToQueueFront("Notification", "Can't Move")
            elif info == "Move Piece Up":

                xLoc = int(idealX / 8.0)
                yLoc = int(idealY / 8.0)

                if (yLoc >= 0):
                    if (theBoard.checkForCollision(xLoc, yLoc - 1, thePiece) <= 0):
                        idealY -= 8.0
                    else:
                        theEventQueue.addToQueueFront("Notification", "Can't Move")
                else:
                    theEventQueue.addToQueueFront("Notification", "Can't Move")
            elif info == "Place Piece":

                # First we get the x,y of the piece
                
                xLoc = int(idealX / 8.0)
                yLoc = int(idealY / 8.0)

                if theBoard.checkForCollision(xLoc, yLoc, thePiece) == 0:
                    theBoard.placePiece(xLoc, yLoc, thePiece, thePieceColor)
                    theEventQueue.addToQueueFront("Score", "Placed Piece")
                    theEventQueue.addToQueueFront("Gamestate", "Get New Piece")
                    theEventQueue.addToQueueFront("Gamestate", "Check For Squares")
                else:
                    theEventQueue.addToQueueFront("Notification", "Can't Place")
            elif info == "Rotate Clockwise":
                xLoc = int(idealX / 8.0)
                yLoc = int(idealY / 8.0)
                tempPiece = RotateBlocks.rotateRight(thePiece)
                if (theBoard.checkForCollision(xLoc, yLoc, tempPiece) <= 0):
                    thePiece = tempPiece
                else:
                    theEventQueue.addToQueueFront("Notification", "Can't Move")
            elif info == "Rotate Counterclockwise":
                xLoc = int(idealX / 8.0)
                yLoc = int(idealY / 8.0)
                tempPiece = RotateBlocks.rotateLeft(thePiece)
                if (theBoard.checkForCollision(xLoc, yLoc, tempPiece) <= 0):
                    thePiece = tempPiece
                else:
                    theEventQueue.addToQueueFront("Notification", "Can't Move")
            else:
                print "Unknown %s event '%s' disregarded." % (type, info)
        elif type == "Notification":
            if info == "Can't Move":
                pass
            elif info == "Can't Place":
                pass
            elif info == "Out Of Time":
                pass
            elif info == "Piece Placed":
                pass
            elif info == "Squares Removed":
                pass
            else:
                print "Unknown %s event '%s' disregarded." % (type, info)
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
                print "Unknown %s event '%s' disregarded." % (type, info)
        elif type == "Score":
            if info == "Block Found":
                if tuple == None:
                    theScore = theScore + 100 * theMultiplyer
                else:
                    theScore = theScore + tuple * theMultiplyer
            elif info == "Placed Piece":
                theScore = theScore + 5
            elif info == "Reset Score":
                theScore = 0
                theMultiplyer = 1
            else:
                print "Unknown %s event '%s' disregarded." % (type, info)
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
            elif info == "Sink Blocks":
                Video.sinkEm(theBoard, timeDelta)
            elif info == "Swap Buffers":
                pygame.display.flip()
            elif info == "Toggle Lights":
                Video.toggleLights()
            else:
                print "Unknown %s event '%s' disregarded." % (type, info)
        else:
            print "Event of unknown type '%s' with info '%s' disregarded." % (type, info)

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
    """Prepare a new game board."""

    global theBoard

    theBoard = GameBoard.GameBoard()    # 16x15, secret square at 0,0. This is the default

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

    global theBoard, thePiece, pieceX, pieceY, thePieceColor
    global boardWidth, boardHeight
    global borderWidth, borderHeight, extraBorder
    global theScore

    Video.sinkEm(theBoard, timeInMS)
    
    Video.startDrawing()

    Video.drawHolder(boardWidth, boardHeight, borderWidth, borderHeight, extraBorder)
    Video.drawBlocksInBoard(theBoard, boardWidth, boardHeight,
                            borderWidth, borderHeight)

    Video.drawPiece(pieceX, pieceY, thePiece, thePieceColor,
                    borderWidth, borderHeight)

    Video.drawInfo(theScore, 0, 0)
    Video.finishDrawing()

if __name__ == "__main__":
    main()

