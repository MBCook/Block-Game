import GameBoard
from OpenGL.GL import *
from OpenGL.GLU import *

global doCulling, doLights, cullWhich
global lx, ly, lz

def drawBlocksInBoard(theBoard, w, h, wb, hb):
    """This draws the given game board. Easy routine"""

    x = y = z = color = 0
    theTuple = 0, 0, 0

    for j in range(h):
        z = hb + 8 * j
        for i in range(w):
            x = wb + 8 * i
            theList = theBoard.getList(i, j)
            if (theList[0] >= 1):
                if (theList[0] == 1):
                    y = 0
                else:
                    y = -4 * ((100.0 - theList[2]) / 100.0)
                color = theList[1]
                drawBlockForBoard(x, y, z, color)

def sinkEm(theBoard, timeInMS):
    """Sink the pieces that need it. When they reach 0, they get killed."""

    for j in range(theBoard.getHeight()):
        for i in range(theBoard.getWidth()):
            tempList = theBoard.getList(i, j)
            if (tempList[0] == 2):
                tempList[2] = tempList[2] - ((timeInMS / 1500.0) * 100)
                if tempList[2] < 0:
                    tempList[2] = 100
                    tempList[0] = 0
                theBoard.setList(i, j, tempList)

def changeCulling():

    """Toggle culling between none, front, and back"""

    global doCulling, cullWhich
    
    if cullWhich == 0:
        print "Now culling back face..."
        cullWhich = 1
        doCulling = 1
    elif cullWhich == 1:
        print "Now culling front face..."
        cullWhich = 2
        doCulling = 1
    else:
        print "No longer culling..."
        cullWhich = 0
        doCulling = 0
    if doCulling:
        glEnable(GL_CULL_FACE)
        if cullWhich == 1:
            glCullFace(GL_BACK)
        elif cullWhich == 2:
            glCullFace(GL_FRONT)
    else:
        glDisable(GL_CULL_FACE)

def initThings(w, h, above):
    """Ways to set up OpenGL to do things the way I want"""

    global doLights, doCulling, cullWhich
    global lx, ly, lz

    doLights = 0
    doCulling = 1
    cullWhich = 2

    lx = -1.0
    ly = 0.5
    lz = 1.5

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, 640.0 / 480.0, 150, 170.0)
    glTranslate(-w / 2.0, h / 2.0, -above)
    glRotatef(90, 1, 0, 0)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_FLAT)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_NORMALIZE)

    glEnable(GL_BLEND)          # This turns on line and polygon antialiasing
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_POLYGON_SMOOTH) # Polygon doesn't seem to work in my implementation

    toggleLights()  # This will turn lights on by default
    changeCulling() # This will display that culling is off

def toggleLights():

    """Toggle lighting on and off"""

    global doLights, lx, ly, lz

    if doLights == 1:
        doLights = 0
        glDisable(GL_LIGHTING)
        print "Lighting turned off..."
    else:

        print "Lighting turned on..."

        doLights = 1

        glEnable(GL_LIGHTING)

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (1.0, 1.0, 1.0, 1.0))

        glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.75, 0.75, 0.75, 1.0))
        glLightfv(GL_LIGHT1, GL_POSITION, (lx, ly, lz, 0.0))
        glEnable(GL_LIGHT1)

def moveLight(x, y, z):

    """Move the light to the position specified"""

    global lx, ly, lz

    if x == 0 and y == 0 and z == 0:
        print "The light is at " + lightPos()
    else:
        lx += x
        ly += y
        lz += z

        tempString = "Moved the light by "
        tempString += "(%.1f, %.1f, %.1f) to " % (x, y, z)
        tempString += lightPos()

        glLightfv(GL_LIGHT1, GL_POSITION, (lx, ly, lz, 0.0))

        print tempString
        
def lightPos():

    """Return a string with the position of the light in it"""

    global lx, ly, lz

    tempString = "(%.1f, %.1f, %.1f)" % (lx, ly, lz)

    return tempString    

def startDrawing():
    """Resets the OpenGL state the way I want it and prepares the camera"""

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def finishDrawing():
    glFlush()

def drawReference(x, y, z):

    """Draw a little reference market"""

    glPushMatrix()

    glColor3f(1.0, 0.0, 0.0)

    glBegin(GL_LINES)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(x, y, z)
    glVertex3f(x + 1.0, y, z)
    glEnd()

    glColor3f(0.0, 1.0, 0.0)

    glBegin(GL_LINES)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(x, y, z)
    glVertex3f(x, y + 1.0, z)
    glEnd()

    glColor3f(0.0, 0.0, 1.0)

    glBegin(GL_LINES)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(x, y, z)
    glVertex3f(x, y, z + 1.0)
    glEnd()

    glPopMatrix()

def drawHolder(w, h, wb, hb, mx = 0, my = 0):
    """Draws the box that holds the blocks for w by h blocks

    Blocks are expected to be 8x8x4

    A border of wb units on the l/r sides, hb on the t/b sides
    Magic square is at mx, my and is 3x3

    Drawn with lower left corner of everything at origin"""

    th = 8 * h
    tw = 8 * w

    # First we draw the holder
    
    glColor3f(0.390625, 0.1953125, 0)   # This is (100, 50, 0) - A nice brown

    glBegin(GL_QUADS)                   # Start drawing

    glNormal3f(0.0, 1.0, 0.0)

    glVertex3f(0, 0, hb)                # First the left "stage"
    glVertex3f(0, 0, hb + th)
    glVertex3f(wb, 0, hb + th)
    glVertex3f(wb, 0, hb)

    glNormal3f(1.0, 0.0, 0.0)

    glVertex3f(wb, 0, hb + th)          # This is the left side
    glVertex3f(wb, -4, hb + th)
    glVertex3f(wb, -4, hb)
    glVertex3f(wb, 0, hb)

    glNormal3f(0.0, 1.0, 0.0)

    glVertex3f(wb, -4, hb + th)         # This is the bottom of the box
    glVertex3f(wb + tw, -4, hb + th)
    glVertex3f(wb + tw, -4, hb)
    glVertex3f(wb, -4, hb)

    glNormal3f(-1.0, 0.0, 0.0)

    glVertex3f(wb + tw, -4, hb + th)    # This is the right side
    glVertex3f(wb + tw, 0, hb + th)
    glVertex3f(wb + tw, 0, hb)
    glVertex3f(wb + tw, -4, hb)

    glNormal3f(0.0, 1.0, 0.0)

    glVertex3f(wb + tw, 0, hb + th)     # This is the right stage
    glVertex3f(2 * wb + tw, 0, hb + th)
    glVertex3f(2 * wb + tw, 0, hb)
    glVertex3f(wb + tw, 0, hb)

    glNormal3f(0.0, 1.0, 0.0)

    glVertex3f(0, 0, 2 * hb + th)       # Draw the bottom stage
    glVertex3f(2 * wb + tw, 0, 2 * hb + th)
    glVertex3f(2 * wb + tw, 0, hb + th)
    glVertex3f(0, 0, hb + th)

    glNormal3f(0.0, 1.0, 0.0)

    glVertex3f(0, 0, hb)                # Draw the bottom stage
    glVertex3f(2 * wb + tw, 0, hb)
    glVertex3f(2 * wb + tw, 0, 0)
    glVertex3f(0, 0, 0)

    glNormal3f(0.0, 0.0, 1.0)

    glVertex3f(wb, 0, hb + th)          # Draw the bottom side
    glVertex3f(wb + tw, 0, hb + th)
    glVertex3f(wb + tw, -4, hb + th)
    glVertex3f(wb, -4, hb + th)

    glNormal3f(0.0, 0.0, -1.0)

    glVertex3f(wb, 0, hb)               # Draw the top side
    glVertex3f(wb, -4, hb)
    glVertex3f(wb + tw, -4, hb)
    glVertex3f(wb + tw, 0, hb)

    glEnd()

    # Now we draw the magic square

    glColor3f(0.78125, 0.390625, 0)     # This is (200, 100, 0) - A light version of brown

    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, -1.0)

    glVertex3f(mx * 8 + wb, -3.99, my * 8 + hb)
    glVertex3f(mx * 8 + wb, -3.99, my * 8 + hb + 3 * 8)
    glVertex3f(mx * 8 + wb + 3 * 8, -3.99, my * 8 + hb + 3 * 8)
    glVertex3f(mx * 8 + wb + 3 * 8, -3.99, my * 8 + hb)

    glEnd()

    # Now we draw the lines    

    glColor3f(0.0, 0.0, 0.0)

    glBegin(GL_LINES)

    for i in range(w + 1):
        glVertex3f(wb + i * 8, -3.98, hb)
        glVertex3f(wb + i * 8, -3.98, hb + h * 8)

    for i in range(h + 1):
        glVertex3f(wb, -3.98, hb + i * 8)
        glVertex3f(wb + w * 8, -3.98, hb + i * 8)

    glEnd()

    # Done with this

def drawPiece(x, y, angle, piece, color, wb, hb):
    """Given a piece (which is just a 9 element array), draw it"""

    # We are ignoring the angle for now, because of problems with the normal
    #   pointing in the wrong direction after rotation. Will have to restructure
    #   the drawing stuff to add arbitrary rotation later.

    glPushMatrix()

    glTranslatef(x + wb + 12, 4, y + hb + 12)
#    glRotate(angle, 0.0, -1.0, 0.0)    

    for j in range(3):
        for i in range(3):
            if (piece[j * 3 + i] >= 1):
                drawBlockForPiece(i, 0, j, color)

    glPopMatrix()

def drawBlockForBoard(x, y, z, color):
    """Draws a block at x, y, z with the correct color

    Colors: 1  - Red
            2  - Blue
            3  - Green
            4+ - Other colors

    Block is 8 by 8 by 4, with a taper on the top.
    This is used for drawing the board."""

    if color == 0:
        return  # No piece, just a safeguard
    elif color == 1:
        glColor3f(0.75, 0.0, 0.0)
    elif color == 2:
        glColor3f(0.0, 0.75, 0.0)
    elif color == 3:
        glColor3f(0.0, 0.0, 0.75)
    elif color == 4:
        glColor3f(0.75, 0.75, 0.0)
    elif color == 5:
        glColor3f(0.0, 0.75, 0.75)
    elif color == 6:
        glColor3f(0.75, 0.0, 0.75)
    else:
        glColor3f(0.75, 0.75, 0.75)

    glPushMatrix()

    glTranslatef(x, y, z)

    glBegin(GL_QUADS)  # Start rendering things

    glNormal3f(-1.0, 0.0, 0.0)

    glVertex3f(0, -4, 0)    # First the left side of the block
    glVertex3f(0, -1, 0)
    glVertex3f(0, -1, 8)
    glVertex3f(0, -4, 8)

    glNormal3f(-1.0, 1.0, 0.0)

    glVertex3f(0, -1, 8)    # Left side taper
    glVertex3f(1, 0, 7)
    glVertex3f(1, 0, 1)
    glVertex3f(0, -1, 0)

    glNormal3f(0.0, 1.0, 0.0)

    glVertex3f(1, 0, 7)     # Center
    glVertex3f(7, 0, 7)
    glVertex3f(7, 0, 1)
    glVertex3f(1, 0, 1)

    glNormal3f(1.0, 1.0, 0.0)

    glVertex3f(7, 0, 7)     # Right side taper
    glVertex3f(8, -1, 8)
    glVertex3f(8, -1, 0)
    glVertex3f(7, 0, 1)

    glNormal3f(1.0, 0.0, 0.0)

    glVertex3f(8, -1, 8)    # Right side
    glVertex3f(8, -4, 8)
    glVertex3f(8, -4, 0)
    glVertex3f(8, -1, 0)

    glNormal3f(0.0, 0.0, -1.0)

    glVertex3f(0, -4, 8)    # Bottom side
    glVertex3f(8, -4, 8)
    glVertex3f(8, -1, 8)
    glVertex3f(0, -1, 8)

    glNormal3f(0.0, 1.0, -1.0)

    glVertex3f(0, -1, 8)    # Bottom taper
    glVertex3f(8, -1, 8)
    glVertex3f(7, 0, 7)
    glVertex3f(1, 0, 7)

    glNormal3f(0.0, 1.0, 1.0)

    glVertex3f(8, -1, 0)    # Top taper
    glVertex3f(0, -1, 0)
    glVertex3f(1, 0, 1)
    glVertex3f(7, 0, 1)

    glNormal3f(0.0, 0.0, 1.0)

    glVertex3f(0, -4, 0)    # Top side
    glVertex3f(8, -4, 0)
    glVertex3f(8, -1, 0)
    glVertex3f(0, -1, 0)

    glEnd()

    glPopMatrix()

    # Done with this

def drawBlockForPiece(x, y, z, color):
    """Draws a block at x, y, z with the correct color

    Colors: 1  - Red
            2  - Blue
            3  - Green
            4+ - Other colors

    Block is 8 by 8 by 4, with a taper on the top.
    This is used for drawin the piece."""

    if color == 0:
        return  # No piece, just a safeguard
    elif color == 1:
        glColor3f(0.75, 0.0, 0.0)
    elif color == 2:
        glColor3f(0.0, 0.75, 0.0)
    elif color == 3:
        glColor3f(0.0, 0.0, 0.75)
    elif color == 4:
        glColor3f(0.75, 0.75, 0.0)
    elif color == 5:
        glColor3f(0.0, 0.75, 0.75)
    elif color == 6:
        glColor3f(0.75, 0.0, 0.75)
    else:
        glColor3f(0.75, 0.75, 0.75)

    glPushMatrix()

    newX = 0
    newZ = 0

    if x == 0:
        newX = -12
    elif x == 1:
        newX = -4
    elif x == 2:
        newX = 4

    if z == 0:
        newZ = -12
    elif z == 1:
        newZ = -4
    elif z == 2:
        newZ = 4
        
    glTranslatef(newX, 0, newZ)

    glBegin(GL_QUADS)  # Start rendering things

    glNormal3f(-1.0, 0.0, 0.0)

    glVertex3f(0, -4, 0)    # First the left side of the block
    glVertex3f(0, -1, 0)
    glVertex3f(0, -1, 8)
    glVertex3f(0, -4, 8)

    glNormal3f(-1.0, 1.0, 0.0)

    glVertex3f(0, -1, 8)    # Left side taper
    glVertex3f(1, 0, 7)
    glVertex3f(1, 0, 1)
    glVertex3f(0, -1, 0)

    glNormal3f(0.0, 1.0, 0.0)

    glVertex3f(1, 0, 7)     # Center
    glVertex3f(7, 0, 7)
    glVertex3f(7, 0, 1)
    glVertex3f(1, 0, 1)

    glNormal3f(1.0, 1.0, 0.0)

    glVertex3f(7, 0, 7)     # Right side taper
    glVertex3f(8, -1, 8)
    glVertex3f(8, -1, 0)
    glVertex3f(7, 0, 1)

    glNormal3f(1.0, 0.0, 0.0)

    glVertex3f(8, -1, 8)    # Right side
    glVertex3f(8, -4, 8)
    glVertex3f(8, -4, 0)
    glVertex3f(8, -1, 0)

    glNormal3f(0.0, 0.0, -1.0)

    glVertex3f(0, -4, 8)    # Bottom side
    glVertex3f(8, -4, 8)
    glVertex3f(8, -1, 8)
    glVertex3f(0, -1, 8)

    glNormal3f(0.0, 1.0, -1.0)

    glVertex3f(0, -1, 8)    # Bottom taper
    glVertex3f(8, -1, 8)
    glVertex3f(7, 0, 7)
    glVertex3f(1, 0, 7)

    glNormal3f(0.0, 1.0, 1.0)

    glVertex3f(8, -1, 0)    # Top taper
    glVertex3f(0, -1, 0)
    glVertex3f(1, 0, 1)
    glVertex3f(7, 0, 1)

    glNormal3f(0.0, 0.0, 1.0)

    glVertex3f(0, -4, 0)    # Top side
    glVertex3f(8, -4, 0)
    glVertex3f(8, -1, 0)
    glVertex3f(0, -1, 0)

    glEnd()

    glPopMatrix()

    # Done with this
