from OpenGL.GL import *
from OpenGL.GLU import *

global doCulling, doLights, cullWhich
global lx, ly, lz

def changeCulling():

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

    lx = -1.0   # This position was expiramentally determined for
    ly = 0.5    #   the test stage of 4, 3, 8, 8 because I liked
    lz = 1.5    #   the way it looked. Need to find a way to calc it.

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, 640.0 / 480.0, 0.1, 100.0)
    glTranslate(-w / 2.0, h / 2.0, -above)
    glRotatef(90, 1, 0, 0)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_NORMALIZE)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)

    toggleLights()  # This will turn lights on by default
    changeCulling() # This will display that culling is off

def toggleLights():

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

    global lx, ly, lz

    tempString = "(%.1f, %.1f, %.1f)" % (lx, ly, lz)

    return tempString    

def startDrawing():
    """Resets the OpenGL state the way I want it and prepares the camera"""

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def finishDrawing():
    glFlush()

def drawReference(x, y, z):

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

def drawHolder(w, h, wb, hb):
    """Draws the box that holds the blocks for w by h blocks

    Blocks are expected to be 8x8x4

    A border of wb units on the l/r sides, hb on the t/b sides

    Drawn with lower left corner of everything at origin"""

    th = 8 * h
    tw = 8 * w
    
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

    # Done with this

def drawBlock(x, y, z, color):
    """Draws a block at x, y, z with the correct color

    Colors: 1 - Red
            2 - Blue
            3 - Green

    Block is 8 by 8 by 4, with a taper on the top"""

    if color == 1:
        glColor3f(0.75, 0.0, 0.0)
    elif color == 2:
        glColor3f(0.0, 0.75, 0.0)
    else:
        glColor3f(0.0, 0.0, 0.75)

    glBegin(GL_QUADS)  # Start rendering things

    glNormal3f(-1.0, 0.0, 0.0)

    glVertex3f(x + 0, y + -4, z + 0)    # First the left side of the block
    glVertex3f(x + 0, y + -1, z + 0)
    glVertex3f(x + 0, y + -1, z + 8)
    glVertex3f(x + 0, y + -4, z + 8)

    glNormal3f(-1.0, 1.0, 0.0)

    glVertex3f(x + 0, y + -1, z + 8)    # Left side taper
    glVertex3f(x + 1, y + 0, z + 7)
    glVertex3f(x + 1, y + 0, z + 1)
    glVertex3f(x + 0, y + -1, z + 0)

    glNormal3f(0.0, 1.0, 0.0)

    glVertex3f(x + 1, y + 0, z + 7)     # Center
    glVertex3f(x + 7, y + 0, z + 7)
    glVertex3f(x + 7, y + 0, z + 1)
    glVertex3f(x + 1, y + 0, z + 1)

    glNormal3f(1.0, 1.0, 0.0)

    glVertex3f(x + 7, y + 0, z + 7)     # Right side taper
    glVertex3f(x + 8, y + -1, z + 8)
    glVertex3f(x + 8, y + -1, z + 0)
    glVertex3f(x + 7, y + 0, z + 1)

    glNormal3f(1.0, 0.0, 0.0)

    glVertex3f(x + 8, y + -1, z + 8)    # Right side
    glVertex3f(x + 8, y + -1, z + 0)
    glVertex3f(x + 8, y + -4, z + 0)
    glVertex3f(x + 8, y + -4, z + 8)

    glNormal3f(0.0, 0.0, -1.0)

    glVertex3f(x + 0, y + -4, z + 8)    # Bottom side
    glVertex3f(x + 8, y + -4, z + 8)
    glVertex3f(x + 8, y + -1, z + 8)
    glVertex3f(x + 0, y + -1, z + 8)

    glNormal3f(0.0, 1.0, -1.0)

    glVertex3f(x + 0, y + -1, z + 8)    # Bottom taper
    glVertex3f(x + 8, y + -1, z + 8)
    glVertex3f(x + 7, y + 0, z + 7)
    glVertex3f(x + 1, y + 0, z + 7)

    glNormal3f(0.0, 1.0, 1.0)

    glVertex3f(x + 8, y + -1, z + 0)    # Top taper
    glVertex3f(x + 0, y + -1, z + 0)
    glVertex3f(x + 1, y + 0, z + 1)
    glVertex3f(x + 7, y + 0, z + 1)

    glNormal3f(0.0, 0.0, 1.0)

    glVertex3f(x + 0, y + -4, z + 0)    # Top side
    glVertex3f(x + 8, y + -4, z + 0)
    glVertex3f(x + 8, y + -1, z + 0)
    glVertex3f(x + 0, y + -1, z + 0)

    glEnd()

    # Done with this