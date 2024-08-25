
import copy
import random
from BlockPieces import *

class Cell(object):
    def __init__(self):
        self.depth = self.ordinal = -1 # set by floodFill
        self.displayLabel = False
        self.isWall = "black"

def make2dList(rows, cols):
    a=[]
    for row in range(rows): a += [[0]*cols]
    return a


class Board(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rows = 17
        self.cols = 17
        self.pieceLimit = 14
        self.rowIncrement = 2

        self.color = "black"
        self.board = make2dList(self.rows, self.cols)
        self.chipTrueOrFalseList = [ ([False] * self.cols) for row in range(self.rows) ]
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col] = Cell()
        self.cellWidth = (width) // self.cols
        self.cellHeight = (height) // self.rows
        self.startRow = 8
        self.startCol = 8
        self.drawBorders()
        self.onBoard = []
        self.blocks = Blocks()
        self.pieceList = self.blocks.pieceList
        #self.createPiece(3, 3)
        self.floodFillOrder = []
        self.numOfBoardBlocks = self.getNumOfBoardBlocks()
        self.firstRowCol = 0
        self.firstRowCol = self.findFirstBlack()
        self.floodFill(self.firstRowCol[0], self.firstRowCol[1])
        #self.isLegal = True
        self.chipList = []
        self.createBoard()
        self.createChips()
        self.chipRadius = 7
        self.countdown = random.randint(20, 40)
        self.chipColor = "yellow"
        self.rotateOrNah = False
        #self.board = [ ([self.color] * self.cols) for row in range(self.rows) ]
        #self.chipTrueOrFalseList = [ ([False] * self.cols) for row in range(self.rows) ]


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


    def findFirstBlack(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if(self.board[row][col].isWall == "black"):
                    return (row, col)

    def getNumOfBoardBlocks(self):
        numBoard = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if(self.board[row][col].isWall == "black"):
                    numBoard += 1
        return numBoard

    def pointInGrid(self, x, y):
        # return True if (x, y) is inside the grid defined by data.
        return ((0 <= x <= self.width) and
                (0 <= y <= self.width))

    def getCell(self, x, y):
        # aka "viewToModel"
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not self.pointInGrid(x, y)):
            return (-1, -1)
        row = int((y) / self.speed)
        col = int((x) / self.speed)
        # triple-check that we are in bounds
        row = min(self.rows-1, max(0, row))
        col = min(self.cols-1, max(0, col))
        return (row, col)

    def getCellBounds(self, row, col):
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        gridWidth  = self.width
        gridHeight = self.width
        x0 = gridWidth * col / self.cols
        x1 = gridWidth * (col+1) / self.cols
        y0 = gridHeight * row / self.rows
        y1 = gridHeight * (row+1) / self.rows
        return (x0, y0, x1, y1)

    def clearLabels(self):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                cell.depth = cell.ordinal = -1
        self.floodFillOrder = [ ]

    def floodFill(self, row, col, depth=0):
        if ((row < 0) or (row >= self.rows) or
            (col < 0) or (col >= self.cols)):
            return # off-board!
        cell = self.board[row][col]
        if (cell.isWall == "blue"):
            return # hit a wall
        if (cell.depth >= 0):
            return # already been here

        # "fill" this cell
        cell.depth = depth
        cell.ordinal = len(self.floodFillOrder)
        self.floodFillOrder.append(cell)

        # then recursively fill its neighbors
        self.floodFill(row-1, col,   depth+1)
        self.floodFill(row+1, col,   depth+1)
        self.floodFill(row,   col-1, depth+1)
        self.floodFill(row,   col+1, depth+1)

    def isLegal(self, row, col, previousBoard):
        if(row == 10 and col == 0):
            return False
        if(row == 10 and col == 15):
            return False
        if(row == 10 and col == 16):
            return False
        if(row == 10 and col == 1):
            return False
        if((row - 1) > 0 and (col - 1) > 0 and (row + 1) < (self.rows - 1) and (col + 1 ) < self.cols - 1):
            if(previousBoard[row][col + 1].isWall == "blue" or previousBoard[row][col - 1].isWall == "blue" or previousBoard[row + 1][col].isWall == "blue" or previousBoard[row - 1][col].isWall == "blue"):
                return False
        if(len(self.floodFillOrder) != self.numOfBoardBlocks):
            return False
        return True

    def isComplete(self, pieceNum):
        return pieceNum == self.pieceLimit
    def createBoard(self, row = -2, col = -2, pieceNum = 0):
        if(self.isComplete(pieceNum)): return None
        isIllegal = False
        if(col >= self.cols - 1):
            row += self.rowIncrement
            col = 0
        else:
            col += 1

        self.clearLabels()
        # Try rotating it
        self.createPiece(row, col)
        self.firstRowCol = self.findFirstBlack()
        self.floodFill(self.firstRowCol[0], self.firstRowCol[1])
        self.numOfBoardBlocks = self.getNumOfBoardBlocks()
        previousPieceList = self.onBoard[-1]
        previousBoard = previousPieceList[2]
        for coordinate in previousPieceList[1]:
            row1 = coordinate[0]
            col1 = coordinate[1]
            if(self.isLegal(row1, col1, previousBoard) == False or previousBoard[row1][col1].isWall == "blue"):
                isIllegal = True
        if(isIllegal):
            previousPieceList = self.onBoard.pop()
            self.board = copy.deepcopy(previousBoard)
            self.clearLabels()
            self.firstRowCol = self.findFirstBlack()
            self.floodFill(self.firstRowCol[0], self.firstRowCol[1])
            self.numOfBoardBlocks = self.getNumOfBoardBlocks()

        else:
            pieceNum += 1

        temp = self.createBoard(row, col, pieceNum)
        if(temp != None):
            # Create and update chipList
            self.clearLabels()
            self.firstRowCol = self.findFirstBlack()
            row1 = self.firstRowCol[0]
            col1 = self.firstRowCol[1]
            self.floodFill(self.firstRowCol[0], self.firstRowCol[1])
            self.numOfBoardBlocks = self.getNumOfBoardBlocks()
            self.numOfBoardBlocks = self.getNumOfBoardBlocks()
            self.chipList = []
            self.createChips()
            self.chips = int(len(self.chipList))
            return # Don't need to return anything
        return None

    def rotatePiece(self, block):
        # Dimension:
        originalCols = len(block[0])
        originalRows = len(block)
        original2DValues = copy.deepcopy(block)

        # Update Piece:
        rotatedList = []
        for col in range(originalCols):
            currentCol = []
            for row in range (originalRows):
                currentCol.append(block[row][col])
            rotatedList.insert(0, currentCol)
        # Updates piece
        block = rotatedList
        return block


    def createPiece(self, row, col):
        coordinates = []
        randomblock = random.choice(self.pieceList)
        self.rotateOrNah = random.choice([True, False])
        if(self.rotateOrNah):
            randomblock = self.rotatePiece(randomblock)
        previousBoard = copy.deepcopy(self.board)
        for row2 in range(len(randomblock)):
            for col2 in range(len(randomblock[0])):
                if(randomblock[row2][col2]):
                    if(row + row2 < self.rows and col + col2 < self.cols):
                        self.board[row + row2][col + col2].isWall = "blue"
                        coordinates.append((row + row2, col + col2))
                        self.onBoard.append([randomblock, coordinates, previousBoard])
