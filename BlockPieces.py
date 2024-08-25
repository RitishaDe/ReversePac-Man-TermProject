
class Blocks(object):
    def __init__(self):
        self.single = [[True]]
        self.cross = [[False, False, True, False], [True, True, True, True], [False, False, True, False]]
        #self.cross2 = [[False, True, False], [False, True, False], [True, True, True], [False, True, False]]
        #self.block = [[True, True, True], [True, True, True]]
        self.tetris = [[False, True], [True, True], [False, True]]
        #self.tPiece = [[ True,  True, True ],[False,  True,  False ], [False, True, False]]
        self.twoBlock = [[True], [True]]
        self.lPiece = [[ False, False,  True ],[  True,  True,  True ]]
        self.shiftedT = [[False, False, True, False], [True, True, True, True]]
        self.halfL = [[True, True], [False, True]]
        self.pieceList = [self.single, self.cross, self.tetris, self.twoBlock, self.lPiece, self.shiftedT, self.halfL]