import sys

class Menu:
	def __init__(self):
		self.commands = {
		"info" : info,
		"newgame" : newGame,
		"newgameplus" : newGamePlus,
		"exit" : exit,
		}

	def runMenu(self):
		user_input = raw_input().split()
		command = user_input[0].lower()

		if command in commands:
			self.commands[command]()
		else:
			print "Command not recognized"

		self.runMenu()

	def exit(self):
		sys.exit()

	def newGame(self):
		game = Game()
		game.runGame()

	def newGamePlus(self):
		pass

	def info(self):
		pass
