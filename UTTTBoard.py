class MultiBoard:
    def __init__(self):
        self.multiBoard = [SingleBoard() for i in range(0,9)]

    def changeBoard(self, player, board, square):
        self.multiBoard[board-1].changeSquare(player, square)

    def getBoard(self, board):
        return self.multiBoard[board-1]

class SingleBoard:
    def __init__(self):
        self.singleBoard = ["-" for i in range(0,9)]

    def changeSquare(self, player, square):
        self.singleBoard[square-1] = [player]

    def getSquare(self, square):
        return self.singleBoard[square-1]

