class Game:
	def __init__(self):
		multiBoard = MultiBoard()
		wins = [None for i in range(0,9)]
		player1 = "X"
		player2 = "O"

	def detectWin(self, board, player):
		rows = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8],
				[0,4,8], [2,4,6]]
		for row in rows:
			for space in rows:
				if board[space] != player:
					break
			else:
				return True
		return False

	def makeMove(self, player, board, space):
		if multiBoard[]


