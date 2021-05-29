import random,pygame,sys
from pygame.locals import *

FPS=30# frames per second , the general speed of the program
WINDOWWIDTH=640 # size of window's width in pixels
WINDOWHEIGHT=480 # size of window's height in pixels
REVEALSPEED =8 # speed boxes sliding reaveals and covers
BOXSIZE = 40 # size of box height and width in pixels
GAPSIZE=10 # size of gap between boxes in pixels
BOARDWIDTH=10 # number of columns of icons
BOARDHEIGHT =7 # number of rows of icons
assert (BOARDWIDTH*BOARDHEIGHT) % 2 ==0, 'Board need to have even number of boxes for pair of matches'
XMARGIN = int ((WINDOWWIDTH-(BOARDWIDTH*(BOXSIZE+GAPSIZE)))/2)
YMARGIN = int ((WINDOWHEIGHT-(BOARDHEIGHT*(BOXSIZE+GAPSIZE)))/2)

GRAY=(100,100,100)
NAVYBLUE=(60,60,100)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW =(255,255,0)
ORANGE=(255,128,0)
PURPLE=(255,0,255)
CYAN=(0,255,255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR= WHITE
HIGHLIGHTCOLOR =BLUE
DONUT='donut'
SQUARE='square'
DIAMOND='diamond'
LINES='lines'
OVAL='oval'
ALLCOLORS=(RED,GREEN,BLUE,YELLOW,ORANGE,PURPLE,CYAN)
ALLSHAPES=(DONUT,SQUARE,DIAMOND,LINES,OVAL)
assert len(ALLCOLORS)* len(ALLSHAPES)*2>= BOARDWIDTH * BOARDHEIGHT, "BOARD IS TOO BIG FOR THE SHAPES AND COLOR DEFINED"
def main():
    global FPSCLOCK,DISPLAYSURF
    pygame.init()
    FPSCLOCK=pygame.time.Clock()
    DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    mousex =0; #used to store x coordinate of mouse event
    mousey=0; #used to store y coordinate of mouse event
    pygame.display.set_caption('Memory Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection =None # stores the (x,y) of the first box clicked

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)
    while True:
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) # drawing the windows 
        drawBoard(mainBoard,revealedBoxes)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mousex,mousey = event.pos


            elif event.type == MOUSEBUTTONUP:
                mousex , mousey = event.pos
                mouseClicked = True

            boxx,boxy = getBoxAtPixel(mousex,mousey)
            if boxx != None and boxy != None:
                # The mouse is currently over a box
                if not revealedBoxes[boxx][boxy]:
                    drawHighlightBox(boxx,boxy)


                if not revealedBoxes[boxx][boxy] and mouseClicked:
                    revealBoxesAnimation(mainBoard,[(boxx,boxy)])
                    revealedBoxes[boxx][boxy]= True #set box as revealed
                    if firstSelection == None: # the current boxx was the first box clicked
                        firstSelection = (boxx,boxy)

                    else: #the current box was the second box Clicked 
                        #Check if there is a match between the two icons 
                        icon1shape, icon1color = getShapeAndColor(mainBoard,firstSelection[0],firstSelection[1])
                        icon2shape, icon2color = getShapeAndColor(mainBoard,boxx,boxy)
                        if icon1shape != icon2shape or icon1color != icon2color :
                            #Icons don't match. Recover-up both selections.
                            pygame.time.wait(1000) # 1000 milliseconds = 1 second
                            coverBoxesAnimation(mainBoard,[(firstSelection[0],firstSelection[1]),(boxx,boxy)])
                            revealBoxes[firstSelection[0],firstSelection[1]]
                            revealBoxes[boxx][boxy]= False
                        elif hasWon(revealedBoxes): #check if all pairs found
                            gameWonAnimation(mainBoard)
                            pygame.time.wait(2000)

                            #Reset the board
                            mainBoard = getRandomizedBoard()
                            revealedBoxes = generateRevealedBoxesData(False)
                            # Show the fully unrevealed board for a second.
                            drawBoard(mainBoard, revealedBoxes)
                            pygame.display.update()
                            pygame.time.wait(1000)

                            #Replay the start game animation.

                            startGameAnimation(mainBoard)


                        firsitSelection= None #reset firstSelection variable



        pygame.display.update()
        FPSCLOCK.tick(FPS)
def generateRevealedBoxesData(val):
    revealedBoxes=[]
    for i in range(BOARDWIDTH):
        revealBoxes.append([val]*BOARDHEIGHT)

    return revealedBoxes

def getRandomizedBoard():
    # Get a list of every possible shape in every possible color
    icons=[]
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))
    
    random.shuffle(icons) # randomize the order of icons list

    numIconsUsed = int((BOARDWIDTH*BOARDHEIGHT)/2)
    icons= icons[:numIconsUsed] * 2 #make two of each
    random.shuffle(icons)


    # Create the board data Structure, with randomly placed icons

    board= []
    for x in range(BOARDWIDTH):
        column =[]
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]

        board.append(column)

    return board

def splitIntoGroupsOf(groupSize, theList):
    #splits a list into list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0,len(theList), groupSize):
        result.append(theList[i:i+groupSize])

    return result





