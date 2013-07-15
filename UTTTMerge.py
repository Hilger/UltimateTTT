from cmd import Cmd

class GameCmd(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.commands = \
        "Commands --\n\
        choose [1-9] -- select a board (at start and when boards are filled)\n\
        mark [1-9] -- select a space on a board\n\
        show -- show all 9 boards in a grid\n\
        show [1-9] -- show a specific board\n\
        show rules -- show the rules of Ultimate Tic Tac Toe\n\
        show scores -- show the players' scores\n\
        show commands -- list commands\n\
        newgame -- start a new game\n\
        exit -- exit the program"
        self.intro = "ULTIMATE TIC TAC TOE\n\n" + self.commands + \
        "\n\n --Please start by choosing the first board to be played on\n"
        self.game = Game()
        self.chooseLock = False
        self.wonLock = False
        self.drawLock = False
        self.prompt = "UTTT/Game: "

    def do_choose(self, args):
        if self.wonLock:
            print "***Game was won by Player %s.\n" + \
            "Type \"exit\" to exit the program or type \"newgame\"" +\
            " for a new game."
            return
        if self.drawLock:
            print "***Game ended in a draw\n" + \
            "Type \"exit\" to exit the program or type \"newgame\"" + \
            " for a new game."
            return
        if self.chooseLock:
            print "***You may not choose a board at this time. Use" + \
            " \"mark[1-9]\" to mark a square instead."
            return
        if not args:
            print "***choose command must include a number" \
            + "between 1-9 as an argument"
            return
        else:
            board = args.split()[0] 
        try:
            board = int(board)
        except:
            print "***You must choose a number between 1-9"
            return
        if board not in range(1,10):
            print "***You must choose a number between 1-9"
        else:
            if self.game.started and self.game.checkBoardFilled():
                print "***Board is full. Please choose another."
            else:
                print "Player %s has chosen board %s" % \
                (self.game.currentPlayer, board)
                print "Please choose a space with \"mark [1-9]\" now"
                self.game.board = self.game.multiBoard.getBoard(board)
                self.chooseLock = True
                self.game.started = True

    def do_mark(self, args):
        if self.wonLock:
            print "***Game was won by Player %s.\n" + \
            "Type \"exit\" to exit the program or type \"newgame\"" +\
            " for a new game."
            return
        if self.drawLock:
            print "***Game ended in a draw\n" + \
            "Type \"exit\" to exit the program or type \"newgame\"" + \
            " for a new game."
            return
        if not self.chooseLock:
            print "***Please choose a board with \"choose [1-9]\" first."
            return
        if not args:
            print "***mark command must include a number between" + \
            " 1-9 as an argument"
            return
        square = args.split()[0]
        try:
            square = int(square)
        except:
            print "***You must choose a number between 1-9"
            return
        if square not in range(1,10):
            print "***You must choose a number between 1-9"
        elif self.game.checkSquareFilled(square):
            print "***Chosen space is not available.  \
            Please choose another."
        else:
            self.game.makeMove(square)
            self.do_show(args="")

            if self.game.detectBoardWin():
                print "Player %s has won board %s!" % \
                (self.game.currentPlayer, self.game.board.getNumber())

            elif self.game.detectBoardDraw() and self.game.board.getNumber()\
            not in self.game.draws:
                print "Board %s has ended in a draw" % self.game.board
                self.game.draws.append(self.game.board.getNumber())

            if self.game.detectPlayerWin():
                print "Player %s has won the game!" % \
                self.game.currentPlayer
                print "Final score -- Player 1: %s, Player 2: %s, Draws: %s" \
                % (self.game.countWins(1), self.game.countWins(2), 
                   len(self.game.draws))
                self.wonLock = True
                return

            elif self.game.detectDrawnGame():
                print "Game has ended in a draw"
                print "Final score -- Player 1: %s, Player 2: %s, Draws: %s" \
                % (self.game.countWins(1), self.game.countWins(2), 
                   len(self.game.draws))
                self.drawLock = True
                return

            self.game.board = self.game.multiBoard.getBoard(square)
            self.game.currentPlayer = 1 if self.game.currentPlayer == 2 \
            else 2

            if self.game.checkBoardFilled():
                print "Player %s was sent to a full board" \
                % self.game.currentPlayer + " and must choose a new one"
                self.chooseLock = False

    def do_show(self, args):
        args = args.split()
        if len(args) > 1:
            print "***Incorrect number of arguments"
        elif len(args) == 0:
            self.game.multiBoard.show()
            return
        try:
            args[0] = int(args[0])
            if args[0] in range(1,10):
                self.game.multiBoard.getBoard(args[0]).show()
            else:
                print "***Number must be between 1-9"
        except:
            if args[0] == "scores":
                print "Player 1 won boards: " + self.game.getWinsString(1) 
                print "Player 2 won boards: " + self.game.getWinsString(2)
                print "Drawn boards: " + self.game.getDrawsString()
                print "Remaining boards: " + self.game.getRemainingString()
                if self.game.countWins(1) > self.game.countWins(2):
                    print "Player 1 is winning %s-%s" % \
                    (self.game.countWins(1), self.game.countWins(2))
                elif self.game.countWins(2) > self.game.countWins(1):
                    print "Player 2 is winning %s-%s" % \
                    (self.game.countWins(2), self.game.countWins(1))
                else:
                    print "Game is tied %s-%s" % \
                    (self.game.countWins(2), self.game.countWins(1))
            elif args[0] == "commands":
                print self.commands
            elif args[0] == "rules":
                pass
            else:
                print "***Argument to show is invalid"

    def do_newgame(self, args):
        newgame = GameCmd()
        newgame.cmdloop()

    def do_exit(self, args):
        return True

    do_EOF = do_exit

class MultiBoard:
    def __init__(self):
        self.multiBoard = [SingleBoard(i) for i in range(1,10)]

    def changeBoard(self, player, board, square):
        self.multiBoard[board-1].changeSquare(player, square)

    def getBoard(self, board):
        return self.multiBoard[board-1]

    def show(self):
        def makeLine(cRange, rRange):
            line = " "
            for i in range(cRange[0], cRange[1]):
                board = self.getBoard(i)
                innerline = ""
                for j in range(rRange[0], rRange[1]):
                    innerline += board.getSquare(j)
                    innerline += " "
                line += innerline
                line += "   "
            return line

        for cRange in [[1,4], [4, 7], [7, 10]]:
            printRange = range(cRange[0], cRange[1])
            print " %s        %s        %s" \
                % (printRange[0], printRange[1], printRange[2])
            for rRange in [[1,4], [4, 7], [7, 10]]:
                print makeLine(cRange, rRange)
            print ""

class SingleBoard:
    def __init__(self, n):
        self.singleBoard = ["-" for i in range(1,10)]
        self.playerIcons = {0: "-", 1: "X", 2 : "O"}
        self.boardNumber = n

    def changeSquare(self, player, square):
        self.singleBoard[square-1] = self.playerIcons[player]
    
    def getSquare(self, square):
        return self.singleBoard[square-1]

    def getNumber(self):
        return self.boardNumber

    def countSpacesFilled(self):
        return 9 - singleBoard.count("-")

    def getEmptySquare(self):
        for i,j in enumerate(self.singleBoard):
            if j == "-":
                return i

    def show(self): 
        print "Board #%s\n" % self.boardNumber
        print " %s    %s    %s\n" % \
        (self.singleBoard[0], self.singleBoard[1], self.singleBoard[2])
        print " %s    %s    %s\n" % \
        (self.singleBoard[3], self.singleBoard[4], self.singleBoard[5])
        print " %s    %s    %s\n" % \
        (self.singleBoard[6], self.singleBoard[7], self.singleBoard[8])

class Game:
    def __init__(self):
        self.multiBoard = MultiBoard()
        self.started = False
        self.currentPlayer = 1
        self.board = None
        self.playerIcons = {0 : "-", 1 : "X", 2 : "O"}
        self.wins = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        self.draws = []

    def detectBoardWin(self):
        if self.wins[self.board.getNumber()]:
            return False
        rows = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8],
                [0,4,8], [2,4,6]]
        for row in rows:
            for square in row:
                if self.board.getSquare(square+1) \
                != self.playerIcons[self.currentPlayer]:
                    break
            else:
                self.wins[self.board] = self.currentPlayer
                return True
        return False

    def detectBoardDraw(self):
        if self.board.countSpacesFilled() == 9:
            if not self.detectBoardWin():
                return True
        elif self.board.countSpacesfilled() == 8:
            emptysquare = self.board.getEmptySquare()
            self.board.changeSquare(1, emptysquare)
            if self.detectBoardWin():
                self.board.changeSquare(0, emptysquare)
                return False
            self.board.changeSquare(2, emptysquare)
            if self.detectBoardWin():
                self.board.changeSquare(0, emptysquare)
                return False
            self.board.changeSquare(0, emptysquare)
            return True
        return False

    def detectDrawnGame(self):
        if self.countWins(1) == self.countwins(2) and \
        len(self.draws) + self.countWins(1) + self.countWins(2) == 9:
            return True
        return False 

    def detectPlayerWin(self):
        if self.wins.values().count(self.currentPlayer) > \
        (9 - len(self.draws)_ / 2: 
            return True
        return False

    def countWins(self, player):
        return self.wins.values().count(player)

    def checkBoardFilled(self):
        if any(map(lambda x: x == "-", 
        [self.board.getSquare(square) for square in range(1, 10)])):
            return False
        return True

    def checkSquareFilled(self, square):
        if self.board.getSquare(square) != "-":
            return True
        return False

    def makeMove(self, square):
        self.board.changeSquare(self.currentPlayer, square)

    def getDrawsString(self):
        if self.draws:
            return ", ".join(self.draws)
        return "None"

    def getWinsString(self, player):
        playerWins = [k for k,v in self.items() if v == player]
        if playerWins:
            return ", ".join(playerWins)
        return "None"

    def getRemainingString(self):
        remaining = [i for i in range(1,10) if i not in self.draws
            and i not in [k for k,v in self.items() if v == player]
        if remaining:
            return ", ".join(remaining)
        return "None"

if __name__ == "__main__":
    game = GameCmd()
    game.cmdloop()