from cmd import Cmd

class MenuCmd(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = "UTTT/Menu: "
        self.commands = \
        "Commands -- \n\
        newgame -- begins a game of Ultimate Tic Tac Toe\n\
        rules -- display the rules of Ultimate Tic Tac Toe\n\
        exit -- exit the program"
        self.intro = "Ultimate Tic Tac Toe\n" + self.commands

    def do_newgame(self, args):
        newgame = GameCmd()
        newgame.cmdloop()

    def do_rules(self, args):
        pass

    def do_exit(self, args):
        return True

    do_EOF = do_exit


class GameCmd(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.commands = \
        "Commands --\n\
        choose [1-9] -- select a board (at start and when boards are filled)\n\
        mark [1-9] -- select a space on a board\n\
        show -- show all 9 boards in a grid\n\
        show [1-9] -- show a specific board\n\
        show scores -- show the players' scores\n\
        show commands -- list commands\n\
        menu -- return to the menu\n\
        exit -- exit the program\n"
        self.intro = "Ultimate Tic Tac Toe\n" + self.commands
        self.game = Game()
        self.chooseLock = False
        self.wonLock = False
        self.prompt = "UTTT/Game: "

    def do_choose(self, args):
        board = args.split()[0]
        if self.wonLock:
            print "***Game was won by Player %s.\n \
            Type \"menu\" to return to the menu or type \"newgame\" \
            for a new game."
            return
        if self.chooseLock:
            print "***You may not choose a board at this time."
            return
        try:
            board = int(board)
        except:
            print "***You must choose a number between 1-9"
        if board not in range(1,10):
            print "***You must choose a number between 1-9"
        else:
            if self.game.started and self.game.checkBoardFilled():
                print "***Board is full. Please choose another."
            else:
                print "Player %s has chosen board %s" % \
                (self.game.currentPlayer, board)
                print "Please choose a space with \"mark [1-9]\" now"
                self.game.board = board
                self.chooseLock = True
                self.game.started = True

    def do_mark(self, args):
        square = args.split()[0]
        if self.wonLock:
            print "***Game was won by Player %s.\n \
            Type \"exit\" to exit the program or type \"newgame\" \
            for a new game."
            return
        if not self.chooseLock:
            print "***Please choose a board with \"choose [1-9]\" first."
        else:
            try:
                square = int(square)
            except:
                print "***You must choose a number between 1-9"
            if square not in range(1,10):
                print "***You must choose a number between 1-9"
            elif self.game.checkSquareFilled(square):
                print "***Chosen space is not available.  \
                Please choose another."
            else:
                self.game.makeMove(square)

                if self.game.detectBoardWin():
                    print "Player %s has won board %s!" % \
                    (self.game.currentPlayer, self.game.board)

                    if self.game.detectPlayerWin():
                        print "Player %s has won the game!" % \
                        self.game.currentPlayer
                        self.wonLock = True

                self.game.board = square
                self.game.currentPlayer = 1 if self.game.currentPlayer == 2 \
                else 1

                if self.game.detectBoardFilled():
                    print "Player %s was sent to a full board and must choose \
                    a new one"
                    self.chooseLock = False

    def do_show(self, args):
        args = args.split()
        if len(args) > 1:
            print "***Incorrect number of arguments"
        elif len(args) == 0:
            self.game.multiBoard.show()
            return
        elif args[0] in range(1,10):
            self.game.multiBoard.getBoard(args[0]).show()
        else:
            if args[0] == "scores":
                print "Player 1 has won %s boards" % self.game.countWins(1)
                print "Player 2 has won %s boards" % self.game.countWins(2)
            elif args[0] == "commands":
                print self.commands

    def do_newgame(self, args):
        newgame = GameCmd()
        newgame.cmdloop()

    def do_menu(self, args):
        menu = MenuCmd()
        menu.cmdloop()

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
                for j in range(rRange[0], rRange[1]):
                    line += board.getSquare(j)
                    line += "  "
            return line

        for cRange in [[1,4], [4, 7], [7, 10]]:
            printRange = range(cRange[0], cRange[1])
            print " %s     %s     %s" \
                % (printRange[0], printRange[1], printRange[2])
            for rRange in [[1,4], [4, 7], [7, 10]]:
                print makeLine(cRange, rRange)
            print ""

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

    def show(self): 
        print "Board #%s" % self.boardNumber
        print " %s    %s    %s" % \
        (self.singleBoard[0], self.singleBoard[1], self.singleBoard[2])
        print " %s    %s    %s" % \
        (self.singleBoard[3], self.singleBoard[4], self.singleBoard[5])
        print " %s    %s    %s" % \
        (self.singleBoard[6], self.singleBoard[7], self.singleBoard[8])

class Game:
    def __init__(self):
        self.multiBoard = MultiBoard()
        self.started = False
        self.currentPlayer = 1
        self.board = None
        self.playerIcons = {1: "X", 2 : "O"}
        self.wins = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    def detectBoardWin(self):
        if self.wins[board]:
            return False
        rows = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8],
                [0,4,8], [2,4,6]]
        for row in rows:
            for square in row:
                if self.board.getSquare(square+1) \
                != self.playerIcons[self.currentPlayer]:
                    break
            else:
                self.wins[board] = self.currentPlayer
                return True
        return False

    def detectPlayerWin(self):
        if self.wins.values().count(self.currentPlayer) >= 5:
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

    # def runGame(self):
    #     # List options for the player
    #     # Ask the move they would like to make
    #     # Make the move
    #     # Return representation of board to console
    #     # If one player wins, print and return to menu
    #     self.showBoard()
    #     print "Player %s please choose a starting board" % self.currentPlayer
    #     boardChoice = raw_input()
    #     if boardChoice not in map(str, range(1,10)):
    #       print "That is not an available board.  Choices are 1 to 9"
    #       self.runGame()
    #     else:
    #         boardChoice = int(boardChoice)
    #         self.board = self.multiBoard.getBoard(boardChoice)
    #     while True:
    #         self.showBoard()
    #         print "The current board is %s" % self.board.getNumber()
    #         print "It is player %s's turn" % self.currentPlayer
    #         print "Please choose a square."

    #     square = raw_input()
    #     try:
    #         square = int(square)
    #     except:
    #         print "Input must be a number from 1 to 9"
    #         continue
    #     if square not in range(1,10):
    #         print "Input must be a number from 1 to 9"
    #         continue
    #     elif self.checkSquareFilled(square):
    #         print "Chosen square is not available"
    #         continue
    #     else:
    #         print "Player %s chooses square %s on board %s" % \
    #         (self.currentPlayer, square, self.board.getNumber())
    #         self.makeMove(square)
    #         if self.detectBoardWin():
    #             print "Player %s has won board %s" % (self.currentPlayer, 
    #             self.board.getNumber())
    #             self.wins[self.currentPlayer] += 1

    #     if self.wins[self.currentPlayer] >= 5:
    #         print "Player %s has won!" % self.currentPlayer
    #         break

    #     else:
    #         self.currentPlayer = 2 if self.currentPlayer == 1 else 1
    #         self.board = self.multiBoard.getBoard(square)

    # def showBoard(self):
    #     def makeLine(cRange, rRange):
    #         line = " "
    #         for i in range(cRange[0], cRange[1]):
    #             board = self.multiBoard.getBoard(i)
    #         for j in range(rRange[0], rRange[1]):
    #             line += board.getSquare(j)
    #             line += "  "
    #         return line

    #     for cRange in [[1,4], [4, 7], [7, 10]]:
    #         printRange = range(cRange[0], cRange[1])
    #         print " %s     %s     %s" \
    #             % (printRange[0], printRange[1], printRange[2])
    #         for rRange in [[1,4], [4, 7], [7, 10]]:
    #             print makeLine(cRange, rRange)
    #         print ""

if __name__ == "__main__":
    menucmd = MenuCmd()
    menucmd.cmdloop()