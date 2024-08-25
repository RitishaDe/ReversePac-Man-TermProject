

from GhostClass import *
from PacManClass import *

class Level1(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rows = 17
        self.cols = 17
        self.color = "black"
        self.board = [ ([self.color] * self.cols) for row in range(self.rows) ]
        self.cellWidth = (width) // self.cols
        self.cellHeight = (height) // self.rows
        self.startRow = 8
        self.startCol = 8
        self.chipList = []
        self.drawBorders()
        self.createChips()
        self.chipRadius = 7
        self.countdown = 120
        self.chipColor = "yellow"

    def drawBorders(self):
        for col in range(self.cols):
            self.board[0][col] = "blue"
            self.board[len(self.board) - 1][col] = "blue"

        for row in range(self.rows):
            self.board[row][0] = "blue"
            self.board[row][len(self.board) - 1] = "blue"

        self.board[7][7] = "blue"
        self.board[7][9] = "blue"
        self.board[7][10] = "blue"
        self.board[7][6] = "blue"
        self.board[8][6] = "blue"
        self.board[8][10] = "blue"
        self.board[9][8] = "blue"
        self.board[9][7] = "blue"
        self.board[9][9] = "blue"
        self.board[9][6] = "blue"
        self.board[9][10] = "blue"

    def createChips(self):
        self.chipColor = "yellow"
        for row in range(self.rows):
            for col in range(self.cols):
                if(self.board[row][col] == "black"):
                    if(row == self.startRow + 2 and col == self.startCol):
                        continue
                    else:
                        cx = self.cellWidth * (row)
                        cy = self.cellHeight * (col)
                        self.chipList.append([cx, cy, self.chipColor])

    def drawChips(self, canvas):
        for chip in self.chipList:
            cx = chip[1]
            cy = chip[0]
            color = chip[2]
            radius = self.cellWidth//2
            canvas.create_oval(cx - self.chipRadius + radius , cy - self.chipRadius + radius, cx + self.chipRadius + radius, cy + self.chipRadius + radius, fill = color, outline = color, width = 1)

    def drawBoard(self, canvas):
        self.drawBorders()
        for row in range(self.rows):
            for col in range(self.cols):
                self.drawCell(canvas, row, col, self.board[row][col])

    def drawCell(self, canvas, row, col, color):
        canvas.create_rectangle(self.cellWidth * col, self.cellHeight*row, self.cellWidth*(col+1), self.cellHeight*(row + 1), fill = color, outline = color, width = 1)


from tkinter import *

# Initializes data
def init(data):
    data.UserMode = False
    data.board = Level1(data.width, data.width)
    data.speed = data.board.cellWidth
    data.startRow = data.board.startRow
    data.startCol = data.board.startCol
    # Pac-Man starts two rows down
    data.PacMan = Pacman(data.width//2, data.width //2 + data.speed * 2 , data.board.board, data.speed, data.startRow + 2, data.startCol, data.width)
    data.timer = 0
    data.RedGhost = Ghost(data.width//2, data.width//2, "red", data.board.board, data.speed, data.startRow, data.startCol, data.board.chipList, data.width)
    data.BlueGhost = Ghost(data.width//2, data.width//2, "blue", data.board.board, data.speed, data.startRow, data.startCol, data.board.chipList, data.width)
    data.PinkGhost = Ghost(data.width//2, data.width//2, "pink", data.board.board, data.speed, data.startRow, data.startCol, data.board.chipList, data.width)
    data.YellowGhost = Ghost(data.width//2, data.width//2, "yellow", data.board.board, data.speed, data.startRow, data.startCol, data.board.chipList, data.width)
    data.GhostList = [data.RedGhost, data.BlueGhost, data.PinkGhost, data.YellowGhost]
    data.dirs = ["Right", "Left", "Down", "Up"]
    data.on = True
    data.GameOn = False
    data.ghostScores = 0
    data.countdown = data.board.countdown
    data.winOrLose = ""
    data.gameOver = False
    data.chips = int(len(data.board.chipList))
    data.chipReq = int(len(data.board.chipList) * 0.75)
    data.pauseGhosts = False
    data.ghostColors = ["red", "blue", "pink", "yellow"]
    data.start = True
    data.UserStart = False
    data.UserEnd = True
    data.UserDuring = False

def mousePressed(event, data):
    # use event.x and event.y*
    if(data.UserMode and data.UserDuring):
        col = event.x // data.speed
        row = event.y // data.speed
        if(data.board.board[row][col] == "blue"):
            data.board.board[row][col] = "black"
        else:
            data.board.board[row][col] = "blue"
        data.board.chipList = []
        data.board.createChips()

def drawScoreCountDownBoard(canvas, data):
     canvas.create_text(data.width//2, data.height - 25, text = "PacMan: " + str(data.PacMan.score) + "  Time Left: " + str(data.countdown) + "sec" + "  Ghosts: " + str(data.ghostScores), fill = "white", font = "System 17")

def drawUserModeInstructions(canvas, data):
    canvas.create_text(data.width)

def keyPressed(event, data):
    # use event.char and event.keysym
    if(event.keysym == "r"):
        init(data)
    if(event.keysym == "u"):
        data.UserMode = True
        data.UserStart = True
        data.UserEnd = False
    if(event.keysym == "e"):
        data.UserMode = False
        data.UserEnd = True
    if(event.keysym == "t"):
        data.UserStart = False
        data.UserDuring = True
    if(data.GameOn):
        if(event.keysym == "p"):
            data.on = not data.on
        if(event.keysym != "p" and event.keysym != "s" and event.keysym != "r" and event.keysym != "u" and event.keysym != "e" and event.keysym != "t"):
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
    radius = data.width //5
    canvas.create_rectangle(cx - radius1, cy - radius, cx + radius1, cy + radius, fill = "black")
    canvas.create_text(cx, cy - 20, text = "User Mode Instructions:", fill = "white", font = "System 18")
    canvas.create_text(cx, cy, text = "Click anywhere on the board to create a cell", fill = "cyan", font = "System 18")
    canvas.create_text(cx, cy + 20, text = "Click on cell again to make it disappear", fill = "cyan", font = "System 18")

def drawInstructions(canvas, data):
    cx = data.width //2
    cy = data.width //2
    radius1 = data.width //2
    radius = data.width //5
    canvas.create_rectangle(cx - radius1, cy - radius, cx + radius1, cy + radius, fill = "black")
    canvas.create_text(cx, cy - 95, text = "Instructions:", fill = "white", font = "System 20")
    #canvas.create_ text(cx, cy - 30, text = "Your goal is to keep the ghosts from eating " + str(data.chips) + " chips before time is up!", fill = "green", font = "System 18")
    canvas.create_text(cx, cy - 60, text = "Your goal is to keep the ghost", fill = "cornflower blue", font = "System 17")
    canvas.create_text(cx, cy - 30, text = "from eating " + str(data.chips) + " chips before time is up!", fill = "cornflower blue", font = "System 17")
    canvas.create_text(cx, cy + 10 , text = "Increase your own score by eating", fill = "blue violet", font = "System 17")
    canvas.create_text(cx, cy + 40, text = "as many chips as possible!", fill = "blue violet", font = "System 17")
    canvas.create_text(cx, cy + 80, text = "Press “s” to start and “p” to pause", fill = "light coral", font = "System 17")

def drawGameOver(canvas, data):
    cx = data.width //2
    cy = data.width //2
    radius1 = data.width //2
    radius = data.width //5
    canvas.create_rectangle(cx - radius1, cy - radius, cx + radius1, cy + radius, fill = "black")
    if(data.winOrLose == "Lose"):
        canvas.create_text(cx, cy - 40, text = "YOU LOSE!", fill = "red2", font = "System 20")
    if(data.winOrLose == "Win"):
        canvas.create_text(cx, cy - 40, text = "YOU WIN!", fill = "medium spring green", font = "System 20")
    canvas.create_text(cx, cy, text = "Score: " + str(data.PacMan.score), fill = "aquamarine", font = "System 18")
    canvas.create_text(cx, cy + 40, text = "Press r to play again!", fill = "dark orange", font = "System 20")

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
    if (data.ghostScores == data.chipReq):
        data.GameOn = False
        data.gameOver = True
        data.winOrLose = "Lose"
    if(data.countdown == 0 and data.ghostScores != data.chipReq):
        data.GameOn = False
        data.gameOver = True
        data.winOrLose = "Win"

def timerFired(data):
    gameOver(data)
    if(data.GameOn):
        if(data.on):
            data.timer += 1
            if(data.timer % 100 == 0):
                data.pauseGhosts = False
            counter = 0
            for ghost in data.GhostList:
                ghost.color = data.ghostColors[counter]
                counter += 1
            if(data.timer % 10 == 0):
                data.countdown -= 1
            data.PacMan.open = not data.PacMan.open

                # print(ghost.color)
                # roWcoL = ghost.findNearChip()
                # row = roWcoL [0]
                # col = roWcoL [1]
                # print(roWcoL)
                # colDistance = 0
                # rowDistance = 0
                # dirRow = None
                # dirCol = ""
                # print(ghost.cx // data.speed)
                # print(ghost.cy // data.speed)
                # if(row == ghost.cx // data.speed):
                #     dirRow = "Stay"
                # if(col == ghost.cy // data.speed):
                #     dirCol = "Stay"
                # if (row < (ghost.cx // data.speed)):
                #     # Then the chip is at the top
                #     rowDistance = abs((ghost.cx // data.speed) - row)
                #     dirRow = "Up"
                # if (row > (ghost.cx // data.speed)):
                #     rowDistance = abs(row - (ghost.cx // data.speed))
                #     dirRow = "Down"
                # if (col < (ghost.cy // data.speed)):
                #     # Then the chip is at the Left
                #     colDistance = abs((ghost.cy // data.speed) - col)
                #     dirCol = "Left"
                # if (col > (ghost.cy // data.speed)):
                #     colDistance = abs(col - (ghost.cy // data.speed))
                #     dirCol = "Right"
                # if( rowDistance == colDistance):
                #     ghost.dir = dirRow
                # elif(rowDistance == 0):
                #     ghost.dir = dirCol
                # elif(colDistance == 0):
                #     ghost.dir = dirRow
                # elif(colDistance < rowDistance):
                #     ghost.dir = colDir
                # elif(rowDistance < colDistance):
                #     ghost.dir = rowDir
                # print(ghost.dir)
            # for chip in (data.board.chipList):
            #     print("row", chip[1] // data.speesd)
            #     print("col", chip[0] // data.speed)
            for ghost in data.GhostList:
                # bestChip = None
                # bestPath = 0
                # for chip in data.board.chipList:
                #     chipRow = chip[1] // data.speed
                #     chipCol = chip[0] // data.speed
                #     if(bestChip == None and bestPath == 0):
                #         bestChip = chip
                #         bestPath = ghost.findChip(chipRow, chipCol)
                #     elif(bestPath == None):
                #         continue
                #     elif(bestPath >= ghost.findChip(chipRow, chipCol)):
                #         bestChip = chip
                #         bestPath = ghost.findChip(chipRow, chipCol)
                # dir = bestPath
                # if(dir == (0, 1)):
                #     ghost.dir = "Right"
                # elif(dir == (0, -1)):
                #     ghost.dir = "Left"
                # elif(dir == (-1, 0)):
                #     ghost.dir = "Up"
                # elif(dir == (1, 0)):
                #     ghost.dir = "Down"
                ghost.dir = random.choice(data.dirs)
                if(data.pauseGhosts):
                    for ghost in data.GhostList:
                        ghost.color = "white"
                if(data.pauseGhosts != True):
                    ghost.move(data)
                for chip in data.board.chipList:
                    if(ghost.isCollisionWithChip(chip, data.board.chipRadius, data.speed)):
                        data.board.chipList.remove(chip)
                        data.ghostScores += 1
                        break;
                if(data.PacMan.isCollisionWithGhost(ghost)):
                    # eat the ghost + restart its position
                    ghost.startRow = data.startRow
                    ghost.startCol = data.startCol
                    ghost.cx = data.width//2
                    ghost.cy = data.width//2
                # Check is collision with a chip and eat it
            data.PacMan.move(data)
            for chip in (data.board.chipList):
                if(data.PacMan.isCollisionWithChip(chip, data.board.chipRadius, data.speed)):
                    data.board.chipList.remove(chip)
                    data.PacMan.score += 1
                    break;
                    # Check if collision with any chip and eat it and increase score
            for chip in data.board.chipList:
                for ghost in data.GhostList:
                    if(ghost.isCollisionWithChip(chip, data.board.chipRadius, data.speed)):
                        data.board.chipList.remove(chip)
                        data.ghostScores += 1
                        break;

def redrawAll(canvas, data):
    data.board.drawBoard(canvas)
    drawScoreCountDownBoard(canvas, data)
    if(data.UserStart):
        drawUserModeInstructions(canvas, data)
    if(data.UserEnd):
        data.PacMan.drawPacMan(canvas)
        data.board.drawChips(canvas)
        for ghost in data.GhostList:
            ghost.drawGhost(canvas, data)
        if(data.start):
            drawInstructions(canvas, data)
        if(data.gameOver):
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
