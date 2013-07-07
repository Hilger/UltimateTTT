class Game:
	def __init__(self):
		self.multiBoard = MultiBoard()
		self.player1wins = 0
		self.player2wins = 0
		self.currentPlayer = 1
		self.board = None
		self.playerIcons = {1: "X", 2 : "O"}

	def detectBoardWin(self, player, board):
		rows = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8],
				[0,4,8], [2,4,6]]
		for row in rows:
			for space in rows:
				if self.board[space] != self.playerIcons(self.currentPlayer):
					break
			else:
				return True
		return False

	def checkFilled(self, board):
		if any(self.board == "-"):
			return False
		return True

	def makeMove(self, player, board, space):
		board = multiBoard.getBoard(board)
		if board.getSpace(space) != None:
			print "That space has already been taken!"
		else:
			board.changeSquare(player, square)

	def runGame():
		# List options for the player
		# Ask the move they would like to make
		# Make the move
		# Return representation of board to console
		# If one player wins, print and return to menu
		self.listOptions()
		print "Player %s please choose a board" % currentPlayer
		boardChoice = raw_input()
		if boardChoice not in map(str, range(1,10)):
			print "That is not an available board.  Choices are 1 to 9"
			self.runGame()
		else:
			self.board = multiBoard.getBoard(boardChoice)

