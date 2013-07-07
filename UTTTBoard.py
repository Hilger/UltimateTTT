class MultiBoard:
    def __init__(self):
        self.multiBoard = [SingleBoard() for i in range(0,9)]

    def changeBoard(player, board, square):
        self.multiBoard[board-1].changeSquare(player, square)

    def getBoard(board):
        return self.multiBoard[board]

class SingleBoard:
    def __init__(self):
        self.singleBoard = [None for i in range(0,9)]

    def changeSquare(player, square):
        self.singleBoard[square-1] = [player]

    def getSquare(square):
        return self.singleBoard(square)



