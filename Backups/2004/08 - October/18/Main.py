import sys
import pygame
import Video

# Globals

global theClock

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

    global theClock

    print ""

    pygame.init()

    pygame.display.set_mode((640, 480), pygame.OPENGL | pygame.DOUBLEBUF)

    Video.initThings(144, 136, 160)

    theClock = pygame.time.Clock()
    timeDelta = 0

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                checkKeys(event)
                
        draw(timeDelta)
        pygame.display.flip()
        timeDelta = theClock.tick(60)   # Limit ourselves to 60 FPS        

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
    
    Video.startDrawing()
    Video.drawHolder(16, 15, 8, 8)
    #Video.drawReference(8, 1, 8)   Too small to be seen, so we don't draw
    Video.drawBlock(16, 0, 8, 1)
    Video.drawBlock(20, 0, 16, 2)
    Video.drawBlock(24, 0, 24, 3)
    Video.finishDrawing()

if __name__ == "__main__":
    main()

