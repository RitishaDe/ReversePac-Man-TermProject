from GhostClass import *
from PacManClass import *
from RandomizedBoardClass import *
from Level1Board import *
from BlankBoard import *
from BlockPieces import *
from greenPowerUpBall import *

from tkinter import *

# Initializes data
def init(data):
    #data.TakeInName = True
    data.UserMode = False
    data.board = Board(data.width, data.width)
    data.cols = data.board.cols
    data.rows = data.board.rows
    data.speed = data.board.cellWidth
    data.startRow = data.board.startRow
    data.startCol = data.board.startCol
    data.color = "black"
    # Pac-Man starts two rows down
    data.cardImages = []
    filename = "redGhostImage(Custom).gif"
    data.cardImages.append(PhotoImage(file=filename))
    filename = "blueGhostImage(Custom).gif"
    data.cardImages.append(PhotoImage(file=filename))
    filename = "pinkGhostImage(Custom).gif"
    data.cardImages.append(PhotoImage(file=filename))
    filename = "yellowGhostImage(Custom).gif"
    data.cardImages.append(PhotoImage(file=filename))
    filename = "whiteGhost.gif"
    data.cardImages.append(PhotoImage(file=filename))
    data.PacMan = Pacman(data.width//2, data.width //2 + data.speed * 2 , data.board.board, data.speed, data.startRow + 2, data.startCol, data.width)
    data.timer = 0
    data.RedGhost = Ghost(data.width//2, data.width//2, "red", data.board.board, data.speed, data.startRow, data.startCol, data.board.chipList, data.width, data.cardImages[0])
    data.BlueGhost = Ghost(data.width//2, data.width//2, "blue", data.board.board, data.speed, data.startRow, data.startCol, data.board.chipList, data.width, data.cardImages[1])
    data.PinkGhost = Ghost(data.width//2, data.width//2, "pink", data.board.board, data.speed, data.startRow, data.startCol, data.board.chipList, data.width, data.cardImages[2])
    data.YellowGhost = Ghost(data.width//2, data.width//2, "yellow", data.board.board, data.speed, data.startRow, data.startCol, data.board.chipList, data.width, data.cardImages[3])
    data.GhostList = [data.RedGhost, data.BlueGhost, data.PinkGhost, data.YellowGhost]

    data.dirs = ["Right", "Left", "Down", "Up"]
    data.on = True
    data.GameOn = False
    data.ghostScores = 0
    data.countdown = data.board.countdown
    data.winOrLose = ""
    data.gameOver = False
    data.chips = int(len(data.board.chipList))
    data.chipReq = int(len(data.board.chipList) * 0.7)
    #print(data.chipReq)
    data.pauseGhosts = False
    data.ghostColors = ["red", "blue", "pink", "yellow"]
    data.start = True
    data.UserStart = False
    data.UserEnd = True
    data.UserDuring = False
    data.floodFillOrder = []
    data.numOfBoardBlocks = getNumOfBoardBlocks(data)
    data.firstRowCol = 0
    data.firstRowCol = findFirstBlack(data)
    floodFill(data, data.firstRowCol[0], data.firstRowCol[1])
    data.help = False
    data.displayGreenBall = False
    data.GreenBall = GreenBall(data.cols, data.speed, data.board.board, data.PacMan.cx, data.PacMan.cy, data.PacMan.startRow, data.PacMan.startCol)
    data.GreenBall.updateCoordinates(data.PacMan.startRow, data.PacMan.startCol)
    #print(data.GreenBall.startRow)


def findFirstBlack(data):
    for row in range(data.rows):
        for col in range(data.cols):
            if(data.board.board[row][col].isWall == "black"):
                return (row, col)

def getNumOfBoardBlocks(data):
    numBoard = 0
    for row in range(data.rows):
        for col in range(data.cols):
            if(data.board.board[row][col].isWall == "black"):
                numBoard += 1
    return numBoard


# Used from lecture notes
# https://www.cs.cmu.edu/~112-n19/index.html
def pointInGrid(x, y, data):
    # return True if (x, y) is inside the grid defined by data.
    return ((0 <= x <= data.width) and
            (0 <= y <= data.width))


# Used from lecture notes
# https://www.cs.cmu.edu/~112-n19/index.html
def getCell(x, y, data):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(x, y, data)):
        return (-1, -1)
    # gridWidth  = data.width
    # gridHeight = data.width
    # cellWidth  = gridWidth / data.cols
    # cellHeight = gridHeight / data.rows
    row = int((y) / data.speed)
    col = int((x) / data.speed)
    # triple-check that we are in bounds
    row = min(data.rows-1, max(0, row))
    col = min(data.cols-1, max(0, col))
    return (row, col)


# Used from lecture notes
# https://www.cs.cmu.edu/~112-n19/index.html
def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width
    gridHeight = data.width
    x0 = gridWidth * col / data.cols
    x1 = gridWidth * (col+1) / data.cols
    y0 = gridHeight * row / data.rows
    y1 = gridHeight * (row+1) / data.rows
    return (x0, y0, x1, y1)


# Used from lecture notes
# https://www.cs.cmu.edu/~112-n19/index.html
def clearLabels(data):
    for row in range(data.rows):
        for col in range(data.cols):
            cell = data.board.board[row][col]
            cell.depth = cell.ordinal = -1
    data.floodFillOrder = [ ]


# Used from lecture notes
# https://www.cs.cmu.edu/~112-n19/index.html
def floodFill(data, row, col, depth=0):
    if ((row < 0) or (row >= data.rows) or
        (col < 0) or (col >= data.cols)):
        return # off-board!
    cell = data.board.board[row][col]
    if (cell.isWall == "blue"):
        return # hit a wall
    if (cell.depth >= 0):
        return # already been here

    # "fill" this cell
    cell.depth = depth
    cell.ordinal = len(data.floodFillOrder)
    data.floodFillOrder.append(cell)

    # then recursively fill its neighbors
    floodFill(data, row-1, col,   depth+1)
    floodFill(data, row+1, col,   depth+1)
    floodFill(data, row,   col-1, depth+1)
    floodFill(data, row,   col+1, depth+1)

def isLegal(data, row, col):
    if(row == 7 and col == 7):
        return False
    if(row == 7 and col == 9):
        return False
    if(row == 7 and col == 10):
        return False
    if(row == 7 and col == 6):
        return False
    if(row == 8 and col == 6):
        return False
    if(row == 8 and col == 10):
        return False
    if(row == 9 and col == 8):
        return False
    if(row == 9 and col == 7):
        return False
    if(row == 9 and col == 9):
        return False
    if(row == 9 and col == 6):
        return False
    if(row == 9 and col == 10):
        return False
    if(row == 8 and col == 6):
        return False
    if(row == 7 and col == 8):
        return False
    if(row == 8 and col == 7):
        return False
    if(row == 8 and col == 8):
        return False
    if(row == 8 and col == 9):
        return False
    if(row == 10 and col == 8):
        return False
    if(row == 6 and col == 8):
        return False
    if(row == 10 and col == 0):
        return False
    if(row == 10 and col == 15):
        return False
    if(row == 10 and col == 16):
        return False
    if(row == 10 and col == 1):
        return False
    if(len(data.floodFillOrder) != data.numOfBoardBlocks):
        return False
    return True


def mousePressed(event, data):
    # use event.x and event.y*
    # Used from lecture notes
    # https://www.cs.cmu.edu/~112-n19/index.html
    clearLabels(data)


    if(data.UserMode and data.UserDuring):
        col = event.x // data.speed
        row = event.y // data.speed
        if(data.board.board[row][col].isWall == "blue"):
            data.board.board[row][col].isWall = "black"
            data.firstRowCol = findFirstBlack(data)
            # Used from lecture notes
            # https://www.cs.cmu.edu/~112-n19/index.html
            floodFill(data, data.firstRowCol[0], data.firstRowCol[1])
        else:
            data.board.board[row][col].isWall = "blue"
            data.firstRowCol = findFirstBlack(data)
            # Used from lecture notes
            # https://www.cs.cmu.edu/~112-n19/index.html
            floodFill(data, data.firstRowCol[0], data.firstRowCol[1])

        data.numOfBoardBlocks = getNumOfBoardBlocks(data)
        if(isLegal(data, row, col) == False):
            data.board.board[row][col].isWall = "black"
            data.firstRowCol = findFirstBlack(data)

            # Used from lecture notes
            # https://www.cs.cmu.edu/~112-n19/index.html
            floodFill(data, data.firstRowCol[0], data.firstRowCol[1])


        data.numOfBoardBlocks = getNumOfBoardBlocks(data)
        data.board.chipList = []
        data.board.createChips()
        data.chips = int(len(data.board.chipList))

def drawScoreCountDownBoard(canvas, data):
     canvas.create_text(data.width//2, data.height - 25, text = "PacMan: " + str(data.PacMan.score) + "  Time Left: " + str(data.countdown) + " sec" + "  Ghosts: " + str(data.ghostScores), fill = "white", font = "System 17")

def keyPressed(event, data):
    # use event.char and event.keysym

    if(event.keysym == "r"):
        init(data)
    if(event.keysym == "u"):
        data.UserMode = True
        data.UserStart = True
        data.UserEnd = False
        data.GameOn = False
        data.startRow = data.board.startRow
        data.startCol = data.board.startCol
        # Pac-Man starts two rows down
        data.timer = 0
        data.ghostScores = 0
        data.countdown = data.board.countdown
        data.winOrLose = ""
        data.chips = int(len(data.board.chipList))
        data.chipReq = int(len(data.board.chipList) * 0.75)
        data.board = BlankBoard(data.width, data.width)
        data.PacMan = Pacman(data.width//2, data.width //2 + data.speed * 2 , data.board.board, data.speed, data.startRow + 2, data.startCol, data.width)
        data.RedGhost = Ghost(data.width//2, data.width//2, "red", data.board.board, data.speed, data.startRow, data.startCol, data.board.chipList, data.width, data.cardImages[0])
        data.BlueGhost = Ghost(data.width//2, data.width//2, "blue", data.board.board, data.speed, data.startRow, data.startCol, data.board.chipList, data.width, data.cardImages[1])
        data.PinkGhost = Ghost(data.width//2, data.width//2, "pink", data.board.board, data.speed, data.startRow, data.startCol, data.board.chipList, data.width, data.cardImages[2])
        data.YellowGhost = Ghost(data.width//2, data.width//2, "yellow", data.board.board, data.speed, data.startRow, data.startCol, data.board.chipList, data.width, data.cardImages[3])
        data.GhostList = [data.RedGhost, data.BlueGhost, data.PinkGhost, data.YellowGhost]

    if (event.keysym == "h"):
        data.help = not data.help

    if(event.keysym == "e" and data.UserMode):
        data.UserMode = False
        data.UserEnd = True
        data.UserStart = False
        data.UserDuring = False
        data.firstRowCol = findFirstBlack(data)

        # Used from lecture notes
        # https://www.cs.cmu.edu/~112-n19/index.html
        floodFill(data, data.firstRowCol[0], data.firstRowCol[1])

        data.numOfBoardBlocks = getNumOfBoardBlocks(data)
        data.board.chipList = []
        data.board.createChips()
        data.chips = int(len(data.board.chipList))
    if(event.keysym == "t" and data.UserMode):
        data.UserStart = False
        data.UserDuring = True
    if(data.GameOn):
        if(event.keysym == "p"):
            data.on = not data.on
        if(event.keysym != "p" and event.keysym != "h" and event.keysym != "s" and event.keysym != "r" and event.keysym != "u" and event.keysym != "e" and event.keysym != "t"):
            data.PacMan.dir = event.keysym
    if(event.keysym == "s" and data.UserEnd):
        data.GameOn = True
        data.start = False


# Checks where the row of the chip is
# If down, call down move function x amount of times
# If up, ^^^^^^^
# Checks where col is

def drawUserModeInstructions(canvas, data):
    cx = data.width //2
    cy = data.width //2
    radius1 = data.width //2
    radius = data.width //4
    canvas.create_rectangle(cx - radius1, cy - radius, cx + radius1, cy + radius, fill = "black")
    canvas.create_text(cx, cy - 100, text = "User Mode Instructions:", fill = "white", font = "System 18")
    canvas.create_text(cx, cy - 60, text = "Press t to start drawing", fill = "blue violet", font = "System 18")
    canvas.create_text(cx, cy - 20, text = "Press e to end drawing", fill = "cornflower blue", font = "System 18")
    canvas.create_text(cx, cy + 20, text = "Press h for instructions", fill = "light coral", font = "System 18")
    canvas.create_text(cx, cy + 60, text = "Click anywhere on the board to create a cell", fill = "cyan", font = "System 18")
    canvas.create_text(cx, cy + 100, text = "Click on cell again to make it disappear", fill = "cyan", font = "System 18")

def drawInstructions(canvas, data):
    cx = data.width //2
    cy = data.width //2
    radius1 = data.width //2
    radius = data.width //4
    canvas.create_rectangle(cx - radius1, cy - radius, cx + radius1, cy + radius, fill = "black")
    canvas.create_text(cx, cy - 125, text = "Instructions:", fill = "white", font = "System 20")
    #canvas.create_ text(cx, cy - 30, text = "Your goal is to keep the ghosts from eating " + str(data.chips) + " chips before time is up!", fill = "green", font = "System 18")
    canvas.create_text(cx, cy - 90, text = "Eat the ghosts to keep them from eating", fill = "cornflower blue", font = "System 17")
    canvas.create_text(cx, cy - 60, text = "%d" % data.chips + " chips before time is up!", fill = "cornflower blue", font = "System 17")
    canvas.create_text(cx, cy - 20, text = "Increase your own score by eating", fill = "blue violet", font = "System 17")
    canvas.create_text(cx, cy + 10, text = "as many chips as possible!", fill = "blue violet", font = "System 17")
    canvas.create_text(cx, cy + 50, text = "Press “s” to start and “p” to pause", fill = "light coral", font = "System 17")
    canvas.create_text(cx, cy + 90, text = "Press u to create your own board!", fill = "cyan", font = "System 17")
    canvas.create_text(cx, cy + 125, text = "Press h for instructions", fill = "dark orchid", font = "System 17")

def drawGameOver(canvas, data):
    cx = data.width //2
    cy = data.width //2
    radius1 = data.width //2
    radius = data.width //5
    canvas.create_rectangle(cx - radius1, cy - radius, cx + radius1, cy + radius, fill = "black")
    if(data.winOrLose == "Lose"):
        canvas.create_text(cx, cy - 40, text = "YOU LOST!", fill = "firebrick1", font = "System 20")
    if(data.winOrLose == "Win"):
        canvas.create_text(cx, cy - 40, text = "YOU WON! :)", fill = "medium spring green", font = "System 20")
    canvas.create_text(cx, cy, text = "Score: " + str(data.PacMan.score), fill = "aquamarine", font = "System 18")
    canvas.create_text(cx, cy + 40, text = "Press r to play again!", fill = "magenta3", font = "System 20")

def gameOver(data):
    if(data.countdown == 0):
        data.GameOn = False
        data.gameOver = True
    if(data.PacMan.score == int(data.chips * 0.5)):
        data.GameOn = False
        data.gameOver = True
        data.winOrLose = "Win"
    if(data.PacMan.score == int(data.chips * 0.2)):
        data.pauseGhosts = True
    if(data.PacMan.score == int(data.chips * 0.1) or data.PacMan.score == int(data.chips * 0.4)):
        if(data.GreenBall.updateCoordinates(data.PacMan.startRow, data.PacMan.startCol)):
            data.displayGreenBall = True
    if((len(data.board.chipList) == 0 or len(data.board.chipList) < (data.chipReq - data.ghostScores)) and data.ghostScores != data.chipReq):
        data.GameOn = False
        data.gameOver = True
        data.winOrLose = "Win"
    if (data.ghostScores >= data.chipReq):
        data.GameOn = False
        data.gameOver = True
        data.winOrLose = "Lose"
    if(data.countdown == 0 and data.ghostScores <= data.chipReq):
        data.GameOn = False
        data.gameOver = True
        data.winOrLose = "Win"

def timerFired(data):
    gameOver(data)
    if(data.GameOn):
        # if(data.displayOrdinals):
        #     data.floodFillIndex += 1
        if(data.on):
            data.timer += 1
            if(data.timer % 100 == 0):
                data.pauseGhosts = False
            counter = 0
            for ghost in data.GhostList:
                ghost.filename = data.cardImages[counter]
                counter += 1
            if(data.timer % 10 == 0):
                data.countdown -= 1
            data.PacMan.open = not data.PacMan.open
            data.PacMan.move(data)
            #print(data.displayGreenBall)
            if(data.timer % 50 == 0):
                data.GreenBall.updateCoordinates(data.PacMan.startRow, data.PacMan.startCol)
                #data.displayGreenBall == True
            if(data.PacMan.isCollisionWithGreenBall(data.GreenBall)):
                data.displayGreenBall = False
                data.PacMan.score += 10
            for ghost in data.GhostList:
                dir = ghost.goToNearestChip(data.board, ghost.startRow, ghost.startCol)

                ghost.dir = dir
                if(dir == (0, 1)):
                    ghost.dir = "Right"
                elif(dir == (0, -1)):
                    ghost.dir = "Left"
                elif(dir == (-1, 0)):
                    ghost.dir = "Up"
                elif(dir == (1, 0)):
                    ghost.dir = "Down"
                if(data.pauseGhosts):
                    for ghost in data.GhostList:
                        ghost.filename = data.cardImages[4]
                if(data.pauseGhosts != True):
                    ghost.move(data)
                for chip in data.board.chipList:
                    if(ghost.isCollisionWithChip(chip, data.board.chipRadius, data.speed)):
                        data.board.chipList.remove(chip)
                        data.board.chipTrueOrFalseList[ghost.startRow][ghost.startCol] = False
                        data.ghostScores += 1
                        break;
                if(data.PacMan.isCollisionWithGhost(ghost)):
                    # eat the ghost + restart its position
                    ghost.startRow = data.startRow
                    ghost.startCol = data.startCol
                    ghost.cx = data.width//2
                    ghost.cy = data.width//2
                # Check is collision with a chip and eat it
            for chip in (data.board.chipList):
                if(data.PacMan.isCollisionWithChip(chip, data.board.chipRadius, data.speed)):
                    data.board.chipList.remove(chip)
                    data.PacMan.score += 1
                    break;
                    # Check if collision with any chip and eat it and increase score


def redrawAll(canvas, data):
    data.board.drawBoard(canvas)
    drawScoreCountDownBoard(canvas, data)
    if(data.UserStart or (data.help and data.UserMode)):
        drawUserModeInstructions(canvas, data)
    if(data.UserDuring and len(data.floodFillOrder) != data.numOfBoardBlocks):
        cx = data.width //2
        cy = data.width //2
        radius1 = data.width //2
        radius = data.width //12
        canvas.create_rectangle(cx - radius1, cy - radius, cx + radius1, cy + radius, fill = "black")
        canvas.create_text(data.width//2, data.width // 2, text = "Not A Valid Space / Board, please try again!", fill = "white", font = "System 17 bold")

    if(data.UserEnd):
        data.PacMan.drawPacMan(canvas)
        data.board.drawChips(canvas)
        for ghost in data.GhostList:
            ghost.drawGhost(canvas, data)
        if(data.displayGreenBall):
            data.GreenBall.drawGreenBall(canvas)
        if(data.start or (data.help and data.UserMode == False)):
            drawInstructions(canvas, data)
        if(data.gameOver and data.winOrLose != ""):
            drawGameOver(canvas, data)

# Used from lecture notes
# https://www.cs.cmu.edu/~112-n19/index.html
def runPacMan(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='black', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
runPacMan(600, 650)
