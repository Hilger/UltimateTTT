class UTTTMenu:
	def __init__(self):
		pass

	def runMenu(self):
		user_input = raw_input().split()
		command = user_input[0]
		args = user_input[1:]
		
		if command in commands:
			self.commands[command](*args)
		else:
			print "Command not recognized"
		self.runMenu()

	def exit(self, *args):
		pass

	def newGame(self, *args):
		runGame()

	def newGamePlus(self, *args):
		pass

	def info(self, *args):
		pass

	commands = {
		"info" : info,
		"newgame" : newGame,
		"newgameplus" : newGamePlus,
		"exit" : exit,
	}