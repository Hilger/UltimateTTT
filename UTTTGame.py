from UTTTMenu import Menu
from UTTTBoard import MultiBoard

class Game:
	def __init__(self):
		self.multiBoard = MultiBoard()
		self.currentPlayer = 1
		self.board = None
		self.playerIcons = {1: "X", 2 : "O"}
		self.wins = {1: 0, 2: 0}

	def detectBoardWin(self):
		rows = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8],
				[0,4,8], [2,4,6]]
		for row in rows:
			for space in rows:
				if self.board[space] != self.playerIcons(self.currentPlayer):
					break
			else:
				return True
		return False

	def checkBoardFilled(self):
		if any(map(lambda x: x == "-", 
		[self.board.getSpace(space) for space in range(1, 10)])):
			return False
		return True

	def checkSpaceFilled(self, space):
		if self.board.getSpace(space) != "-":
			return True
		return False

	def makeMove(self, space):
		if self.board.getSpace(space) != None:
			print "That space has already been taken!"
		else:
			self.board.changeSquare(player, square)

	def runGame():
		# List options for the player
		# Ask the move they would like to make
		# Make the move
		# Return representation of board to console
		# If one player wins, print and return to menu
		self.showBoard()
		print "Player %s please choose a board" % currentPlayer
		boardChoice = raw_input()
		if boardChoice not in map(str, range(1,10)):
			print "That is not an available board.  Choices are 1 to 9"
			self.runGame()
		else:
			self.board = multiBoard.getBoard(boardChoice)
		while True:
			self.showBoard()
			print "Please choose a space."

			space = raw_input()
			try:
				space = int(space)
			except:
				print "Input must be a number from 1 to 9"
				continue
			if space not in range(1,10):
				print "Input must be a number from 1 to 9"
				continue
			elif self.checkSpaceFilled(space):
				print "Chosen space is not available"
				continue
			else:
				"Player %s chooses space %s on board %s" % self.player, \
				space, self.board
				self.makeMove(space)
				if detectBoardWin():
					self.wins[currentPlayer]

			if self.wins[currentPlayer] >= 5:
				print "Player %s has won!" % self.currentPlayer
				break

			else:
				self.currentPlayer = 2 if self.currentPlayer == 1 else 1
				self.board = self.multiBoard.getBoard(space)

	def showBoard():
		def makeLine(cRange, rRange):
			line = " "
			for i in range(cRange[0], cRange[1]):
				board = self.multiBoard.getBoard(i)
				for j in range(rRange[0], rRange[1]):
					line += board.getSpace(j)
				line += " "
			return line

		for cRange in [[1,4], [4, 7], [5, 8]]:
			for rRange in [[1,4], [4, 7], [5, 8]]:
				print makeLine(cRange, rRange)






