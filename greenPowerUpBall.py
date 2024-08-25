# add it by half of cols - 1
# same for cols
# if outof bounds, reverse it
# if touched, score increased by 10 points
# if touched maybe u move faster?
# move every eight seconds

# Gotta make a legal method to check if it is in box otherwise switch gears
# just switch row and col at that point

import math

class GreenBall(object):
    def __init__(self, cols, width, board, cx, cy, PacManRow, PacManCol):
        self.cols = cols
        self.width = width
        self.halfCols = self.cols // 2
        self.cx = cx
        self.cy = cy
        self.board = board
        self.startRow = PacManRow
        self.startCol = PacManCol
        #print("pacManRow", self.PacManRow, "col", self.PacManCol, "own row", self.startRow, "own col", self.startCol)
        self.radius = 40
        self.updateCoordinates(PacManRow, PacManCol)

    # My own drawStar code from Hw2-2
    def drawGreenBall(self, canvas):
        centerX = self.cx
        centerY = self.cy
        diameter = self.radius
        numPoints = 5
        color = "DarkOrchid1"
        points = []
        returnedTuple = (0,0) # coordinates for each point
        outerR = diameter * (1/2)
        innerR = ((3/8) * diameter) * (1/2)
        angleIncrement = (math.pi * 2) / (numPoints * 2) # angle change
        currentAngle = math.pi / 2 # starting point
        for point in range(numPoints * 2): # loops through all points
            if(numPoints % 2 == 1):
                currentAngle+= angleIncrement # next angle
            if(point % 2 == 0): # even (odd)
                x = centerX - outerR * math.cos(currentAngle)  + (self.width //2)
                y = centerY + outerR * math.sin(currentAngle)  + (self.width //2)
                returnedTuple = (x, y)
            else: # odd (inner)
                x = centerX - innerR * math.cos(currentAngle)  + (self.width //2)
                y = centerY + innerR * math.sin(currentAngle)  + (self.width //2)
                returnedTuple = (x, y)
            if(numPoints % 2 == 0):
                currentAngle+= angleIncrement # next angle
            points.append(returnedTuple)
        canvas.create_oval(centerX - (diameter//2) + (self.width //2), centerY - (diameter//2) + (self.width //2), centerX + (diameter//2)+ (self.width //2), centerY + (diameter//2) + (self.width //2), fill = "bisque")
        canvas.create_polygon(points, fill = color)

    def isLegal(self, row, col, board):
        return board[row][col].isWall != "blue"


    def updateCoordinates(self, PacManRow, PacManCol):
        # Top half of board
        # small cx
        if(PacManRow // self.halfCols < 1):
            self.startRow = PacManRow + 3
            #self.cy = self.cy + (5*self.width)
        else:
            # bigger cx
            self.startRow = PacManRow - 3
            #self.cy = abs(self.cy - (5*self.width))

        if(PacManCol // self.halfCols < 1):
            self.startCol = PacManCol + 3
            #self.cx = self.cx + (5*self.width)

        else:
            self.startCol = PacManCol - 3
            #self.cx = abs(self.cx - (5*self.width))
        self.cy = (self.width * self.startRow)
        self.cx = (self.width * self.startCol)
        return self.isLegal(self.startRow, self.startCol, self.board)