
import math

class Pacman(object):
    def __init__(self, x, y, board, speed, startRow, startCol, width):
        self.cx = x
        self.cy = y
        self.radius = 15
        self.change = self.radius // 12
        self.open = True
        self.dir = "Right"
        self.triangleCoord = []
        self.board = board
        self.speed = speed
        self.startRow = startRow
        self.startCol = startCol
        self.width = width
        self.rows = len(self.board)
        self.cols = len(self.board[0])

        self.score = 0 # increases everytime it eats a chip

    def drawPacMan(self, canvas):
        canvas.create_oval(self.cx - self.radius, self.cy - self.radius, self.cx + self.radius, self.cy + self.radius, fill = "yellow", outline = "yellow", width = 1)
        if(self.open):
            if(self.dir == "Up"):
                self.triangleCoord = [self.cx - self.radius - self.change, self.cy - self.radius - self.change, self.cx, self.cy, self.cx + self.radius + self.change, self.cy - self.radius - self.change]
                canvas.create_polygon(self.triangleCoord, fill = "black")
            elif(self.dir == "Left"):
                self.triangleCoord = [self.cx - self.radius - self.change, self.cy - self.radius - self.change, self.cx, self.cy, self.cx - self.radius - self.change, self.cy + self.radius + self.change]
                canvas.create_polygon(self.triangleCoord, fill = "black")
            elif(self.dir == "Down"):
                self.triangleCoord = [self.cx - self.radius - self.change, self.cy + self.radius + self.change, self.cx, self.cy, self.cx + self.radius + self.change, self.cy + self.radius + self.change]
                canvas.create_polygon(self.triangleCoord, fill = "black")
            elif(self.dir == "Right"):
                self.triangleCoord = [self.cx + self.radius + self.change, self.cy - self.radius - self.change, self.cx, self.cy, self.cx + self.radius + self.change, self.cy + self.radius + self.change]
                canvas.create_polygon(self.triangleCoord, fill = "black")

    # Only checks for collision with ghosts
    def isCollisionWithGhost(self, other):
        expectedDistance = self.radius + other.radius
        x1 = self.cx
        y1 = self.cy
        x2 = other.cx
        y2 = other.cy
        distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return (distance <= expectedDistance)

    def isCollisionWithChip(self, chip, radius, width):
        cx = chip[1] // self.speed
        cy = chip[0] // self.speed
        # cx = chip[0] + width
        # cy = chip[1] + width
        # expectedDistance = self.radius + radius
        x1 = self.cx // self.speed
        y1 = self.cy // self.speed
        # distance = math.sqrt((x1 - cx) ** 2 + (y1 - cy) ** 2)
        if(cx == x1 and cy == y1):
            return True
        else:
            return False
        #return (distance <= expectedDistance)

    # Only checks for collision with wall
    def isCollisionWithWall(self, board):
        for row in range(len(board)):
            for col in range(len(board)):
                if(board[row][col].isWall == "blue" and self.startRow == row and self.startCol == col):
                    return True
        return False

    def isCollisionWithGreenBall(self, other):
        return (self.startRow == other.startRow and self.startCol == other.startCol)

    def move(self, data):
        if(self.dir == "Stay"):
            self.cy == self.cy
            self.cx = self.cx
        elif(self.dir == "Up"):
            self.cy -= self.speed
            self.startRow -= 1
            if(self.isCollisionWithWall(self.board)):
                self.cy += self.speed
                self.startRow += 1
        elif(self.dir == "Down"):
            self.cy += self.speed
            self.startRow += 1
            if(self.isCollisionWithWall(self.board)):
                self.cy -= self.speed
                self.startRow -= 1
        elif(self.dir == "Left"):
            self.cx -= self.speed
            self.startCol -= 1
            if(self.isCollisionWithWall(self.board)):
                self.cx += self.speed
                self.startCol += 1
        elif(self.dir == "Right"):
            self.cx += self.speed
            self.startCol += 1
            if(self.isCollisionWithWall(self.board)):
                self.cx -= self.speed
                self.startCol -= 1
        self.startRow %= self.rows
        if(self.startRow == 10 and self.startCol == (len(self.board[0]) - 1)):
            self.startCol %= (self.cols + 2)
        elif(self.startRow == 10 and self.startCol == 0):
            self.startCol %= (self.cols + 2)
        else:
            self.cx %= self.width - 5
            self.startCol %= self.cols
        #self.cy %= self.width
        #if(self.cx - self.radius <= 0 or self.cx + self.radius >= data.width or self.cy - self.radius <= 0 or self.cy + self.radius >= data.height):


