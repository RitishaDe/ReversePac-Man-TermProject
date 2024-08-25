
import copy
import random
import math

class Ghost(object):
    def __init__(self, cx, cy, color, board, speed, startRow, startCol, chipList, width, filename):
        self.cx = cx
        self.cy = cy
        self.radius = 15
        self.color = color
        self.board = board
        self.speed = speed
        self.startRow = startRow
        self.startCol = startCol
        self.chipList = chipList
        self.width = width
        self.dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        self.diagonals = [(-1, -1), (1, 1), (-1, 1), (1, -1)]
        self.rows = len(self.board)
        self.cols = len(self.board[0])
        self.dir = ""
        self.filename = filename
    def drawGhost(self, canvas, data):
        canvas.create_image(self.cx, self.cy,image= self.filename)

        #canvas.create_oval(self.cx - self.radius, self.cy - self.radius, self.cx + self.radius, self.cy + self.radius, fill = self.color, outline = self.color, width = 1)


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
        #if(self.cx - self.radius <= 0 or self.cx + self.radius >= data.width or self.cy - self.radius <= 0 or self.cy + self.radius >= data.height):
        #if(self.cx // self.speed == 10 and self.cy // self.speed = )
        self.startRow %= self.rows
        if(self.startRow == 10 and self.startCol == (len(self.board[0]) - 1)):
            self.startCol %= (self.cols + 2)
        elif(self.startRow == 10 and self.startCol == 0):
            self.startCol %= (self.cols + 2)
        else:
            self.cx %= self.width - 5
            self.startCol %= self.cols
    # Only checks for collision with wall
    def isCollisionWithWall(self, board):
        for row in range(len(board)):
            for col in range(len(board)):
                if(board[row][col].isWall == "blue" and self.startRow == row and self.startCol == col):
                    return True
        return False

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

    def goToNearestChip(self, board, row, col, directions = None, diagonals = None, n = 1):
        if(directions == None):
            dirs = copy.deepcopy(self.dirs)
        else:
            dirs = copy.deepcopy(directions)
        if(diagonals == None):
            diags = copy.deepcopy(self.diagonals)
        else:
            diags = copy.deepcopy(diagonals)
        directions = copy.deepcopy(dirs)
        diagonals = copy.deepcopy(diags)
        if(len(directions) == 0 or len(diagonals) == 0):
            possibleDirs = []
            for dir in self.dirs:
                rowChange = dir[0]
                colChange = dir[1]
                checkRow = row + dir[0]
                checkRow %= self.rows
                checkCol = col + dir[1]
                if(checkRow == 10 and checkCol == ((self.cols) -1)):
                    checkCol %= (self.cols + 2)
                elif(checkRow == 10 and checkCol == 0):
                    checkCol %= self.cols + 2
                else:
                    self.cx %= self.width
                    checkCol %= self.cols
                if(board.board[checkRow][checkCol].isWall == "black"):
                    possibleDirs.append(dir)
                    #print(possibleDirs)
            return random.choice(possibleDirs)
            #         return (dir[1] * -1, dir[0] * -1)
            # return random.choice(self.dirs)
            # print(self.color)
            # print(possibleDirs)
            #return possibleDirs
            # #random.choice(possibleDirs)
        random.shuffle(dirs)
        for dir in dirs:
            checkRow = row + dir[0]*n
            checkRow %= self.rows
            checkCol = col + dir[1]*n
            if(checkRow == 10 and checkCol == ((self.cols) -1)):
                checkCol %= (self.cols + 2)
            elif(checkRow == 10 and checkCol == 0):
                checkCol %= self.cols + 2
            else:
                self.cx %= self.width
                checkCol %= self.cols
            if(board.chipTrueOrFalseList[checkRow][checkCol] == True):
                # found a chip
                return dir
            elif(board.board[checkRow][checkCol].isWall == "blue"):
                # found a blue block
                directions.remove(dir)
            elif(len(directions) == 1):
                return directions[0]
        random.shuffle(diags)
        for diagonal in diags:
            checkRow = row + diagonal[0]*n
            checkRow %= self.rows
            checkCol = col
            if(checkRow == 10 and checkCol == ((self.cols) -1)):
                checkCol %= (self.cols + 2)
            elif(checkRow == 10 and checkCol == 0):
                checkCol %= self.cols + 2
            else:
                self.cx %= self.width
                checkCol %= self.cols
            if(board.chipTrueOrFalseList[checkRow][checkCol] == True):
                # found a chip
                return dir
            elif(board.board[checkRow][checkCol].isWall == "blue"):
                # found a blue block
                diagonals.remove(diagonal)
            elif(len(directions) == 1):
                return (diagonal[0], 0)
        temp = self.goToNearestChip(board, row, col, directions, diagonals, n + 1)
        if(temp != None):
            # print(self.color)
            # print(temp)
            return temp
        return None

