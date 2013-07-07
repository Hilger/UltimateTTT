class MultiBoard:
    def __init__(self):
        self.multiBoard = [SingleBoard(i) for i in range(1,10)]

    def changeBoard(self, player, board, square):
        self.multiBoard[board-1].changeSquare(player, square)

    def getBoard(self, board):
        return self.multiBoard[board-1]

class SingleBoard:
    def __init__(self, n):
        self.singleBoard = ["-" for i in range(1,10)]
        self.playerIcons = {1: "X", 2 : "O"}
        self.boardNumber = n

    def changeSquare(self, player, square):
        self.singleBoard[square-1] = self.playerIcons[player]

    def getSquare(self, square):
        return self.singleBoard[square-1]

    def getNumber(self):
        return self.boardNumber

