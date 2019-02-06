import sys, copy, array
import tetris_shape
class AI:
    def __init__(self, heightWeight, linesWeight, holesWeight, bumpinessWeight):
        self.heightWeight = heightWeight
        self.linesWeight = linesWeight
        self.holesWeight = holesWeight
        self.bumpinessWeight = bumpinessWeight
        self.depth = 2
    
    def bestMove(self, BOARD_DATA, index):
        best = [0, 0]
        bestScore = None
        score = None
        # board: middle, not rotated, not dropped
        board = copy.deepcopy(BOARD_DATA)       
        
        for rotation in range(4):
            while (board.getCurrentDirection() != rotation):
                # board: middle, rotated, not dropped
                board.rotateRight()
                print("rotating")
            # BD: far left, rotated, not dropped   
            BD = copy.deepcopy(board)
            while (BD.moveLeft()):
                pass  
            while(BD.moveRight()):
                # boardData: rotated, moved to right but not dropped
                boardData = copy.deepcopy(BD)
                # boardData: rotated, righted and dropped
                boardDataDropped = copy.deepcopy(boardData)
                while (boardDataDropped.moveDown(True)):
                    pass
                score = \
                    - self.heightWeight * boardDataDropped.aggregatedHeight() \
                    + self.linesWeight * boardDataDropped.lines() \
                    - self.holesWeight * boardDataDropped.holes() \
                    - self.bumpinessWeight * boardDataDropped.bumpiness()
                # if index == self.depth - 1:
                #     score = \
                #         - self.heightWeight * boardDataDropped.aggregatedHeight() \
                #         + self.linesWeight * boardDataDropped.lines() \
                #         - self.holesWeight * boardDataDropped.holes() \
                #         - self.bumpinessWeight * boardDataDropped.bumpiness()
                # else:
                #     score = self.bestMove(BOARD_DATA, index+1)
                if bestScore == None or score > bestScore:
                    bestScore = score
                    best[0] = rotation
                    best[1] = boardData.curX
                boardData.moveRight()
        sys.exit()
        return best
