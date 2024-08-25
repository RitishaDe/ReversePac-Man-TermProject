
import random


class Cell(object):
    def __init__(self):
        self.depth = self.ordinal = -1 # set by floodFill
        self.displayLabel = False
        self.isWall = "black"

def make2dList(rows, cols):
    a=[]
    for row in range(rows): a += [[0]*cols]
    return a
#
# def init(data):
#     data.rows = 4
#     data.cols = 6
#     data.cells = make2dList(data.rows, data.cols)
#     data.gridSize = min(data.width, data.height)
    # for row in range(data.rows):
    #     for col in range(data.cols):
    #         data.cells[row][col] = Cell()
    # data.floodFillIndex = 0
    # data.displayOrdinals = False
    # data.floodFillOrder = [ ]
    # data.numOfBoardBlocks = getNumOfBoardBlocks(data)




class BlankBoard(object):
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
                        self.chipList.append([cx, cy, self.chipColor])
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