
import random
import copy
import math

class Cell(object):
    def __init__(self):
        self.depth = self.ordinal = -1 # set by floodFill
        self.displayLabel = False
        self.isWall = "black"

def make2dList(rows, cols):
    a=[]
    for row in range(rows): a += [[0]*cols]
    return a


class Level1(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rows = 17
        self.cols = 17
        self.color = "black"
        self.board = make2dList(self.rows, self.cols)
        self.chipTrueOrFalseList = [ ([False] * self.cols) for row in range(self.rows) ]
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col] = Cell()
        #self.board = [ ([self.color] * self.cols) for row in range(self.rows) ]
        self.cellWidth = (width) // self.cols
        self.cellHeight = (height) // self.rows
        self.startRow = 8
        self.startCol = 8
        self.chipList = []
        self.drawBorders()
        self.createChips()
        self.chipRadius = 7
        self.countdown = random.randint(20, 40)
        self.chipColor = "yellow"

    def drawBorders(self):
        for col in range(self.cols):
            self.board[0][col].isWall = "blue"
            self.board[len(self.board) - 1][col].isWall = "blue"

        for row in range(self.rows):
            self.board[row][0].isWall = "blue"
            self.board[row][len(self.board) - 1].isWall = "blue"

        self.board[7][7].isWall = "blue"
        self.board[7][9].isWall = "blue"
        self.board[7][10].isWall = "blue"
        self.board[7][6].isWall = "blue"
        self.board[8][6].isWall = "blue"
        self.board[8][10].isWall = "blue"
        self.board[9][8].isWall = "blue"
        self.board[9][7].isWall = "blue"
        self.board[9][9].isWall = "blue"
        self.board[9][6].isWall = "blue"
        self.board[9][10].isWall = "blue"
        # WrapAround
        self.board[10][len(self.board) - 1].isWall = "black"
        self.board[10][0].isWall = "black"
        # Hard coding the blocks
        self.board[1][1].isWall = "blue"
        self.board[1][8].isWall = "blue"
        self.board[2][14].isWall = self.board[2][15].isWall = "blue"
        self.board[3][15].isWall = "blue"
        self.board[3][3].isWall = self.board[3][7].isWall = self.board[3][8].isWall = self.board[3][9].isWall = self.board[3][12].isWall = "blue"
        self.board[4][1].isWall = self.board[4][2].isWall = self.board[4][3].isWall = self.board[4][4].isWall = self.board[4][7].isWall = self.board[4][8].isWall = self.board[4][9].isWall = self.board[4][11].isWall = self.board[4][12].isWall = "blue"
        self.board[5][3].isWall = self.board[5][12].isWall = "blue"
        self.board[6][14].isWall = "blue"
        self.board[7][3].isWall = self.board[7][14].isWall = "blue"
        self.board[8][2].isWall = self.board[8][3].isWall = "blue"
        self.board[9][3].isWall = "blue"
        self.board[10][13].isWall = self.board[10][14].isWall = "blue"
        self.board[11][2].isWall = self.board[11][3].isWall = self.board[11][13].isWall = "blue"
        self.board[12][7].isWall = self.board[12][8].isWall = self.board[12][9].isWall = self.board[12][13].isWall = "blue"
        self.board[13][8].isWall = self.board[13][3].isWall = "blue"
        self.board[14][1].isWall = self.board[14][2].isWall = self.board[14][3].isWall = self.board[14][4].isWall = self.board[14][8].isWall = self.board[14][12].isWall = "blue"
        self.board[15][10].isWall = self.board[15][11].isWall = self.board[15][12].isWall = self.board[15][13].isWall = "blue"

    def createChips(self):
        self.chipColor = "yellow"
        for row in range(self.rows):
            for col in range(self.cols):
                if(self.board[row][col].isWall == "black"):
                    if(row == self.startRow + 2 and col == self.startCol):
                        continue
                    else:
                        cx = self.cellWidth * (row)
                        cy = self.cellHeight * (col)
                        self.chipTrueOrFalseList[row][col] = True

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
                self.drawCell(canvas, row, col, self.board[row][col].isWall)

    def drawCell(self, canvas, row, col, color):
        canvas.create_rectangle(self.cellWidth * col, self.cellHeight*row, self.cellWidth*(col+1), self.cellHeight*(row + 1), fill = color, outline = color, width = 1)