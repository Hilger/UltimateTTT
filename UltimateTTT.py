from cmd import Cmd

class GameCmd(Cmd):
    """GameCmd is a command line application that interacts with the
    Ultimate Tic Tac Toe game.  It provides methods to the user to play the
    game, as well to start a new game, exit the game, and to show information
    related to the game."""

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
        show current -- show current board and player\n\
        show players -- show player icons\n\
        newgame -- start a new game\n\
        exit -- exit the program"

        self.intro = "ULTIMATE TIC TAC TOE\n\n" + self.commands + \
        "\n\n --Please start by choosing the first board to be played on\n"

        self.rules = \
        """
        Ultimate Tic Tac Toe is a game in which 2 players play a modified \n
        version of Tic Tac Toe in which there are 9 individual Tic Tac Toe \n
        boards arranged in a grid rather than a single individual board.\n
        \n
        The grid is arranged as so:
        \n
        Board 1    Board 2    Board 3
        \n
        Board 4    Board 5    Board 6
        \n
        Board 7    Board 8    Board 9
        \n
        Additionally, any move that a player makes sends his opponent to \n
        the board that matches the index of the square that he has selected. \n
        For example, selecting square 1 on any board will send the other \n
        player to board 1. \n
        \n
        To choose a board, as in the beginning of the game or when a player\n
        is sent to an already full board, use the command "choose [1-9]." \n
        Otherwise, to mark a square on the currently selected board, use \n
        the command "mark [1-9]."\n
        \n
        Winning the game requires you to win three board in a row, whether \n
        horizontally, vertically, or diagonally.
        """

        self.game = Game()
        self.chooseLock = False
        self.wonLock = False
        self.drawLock = False
        self.prompt = "UTTT/Game: "

    def do_choose(self, args):
        if self.wonLock:
            print "***Game was won by Player %s.\n" % self.game.currentPlayer + \
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
                  " \"mark [1-9]\" to mark a square instead."
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
            if self.game.started and self.game.checkBoardFilled(board):
                print "***Board is full. Please choose another."
            else:
                self.do_show(str(board))
                print "Player %s has chosen board %s" % \
                      (self.game.currentPlayer, board)
                print "Please choose a space with \"mark [1-9]\" now"
                self.game.board = self.game.multiBoard.getBoard(board)
                self.chooseLock = True
                self.game.started = True

    def do_mark(self, args):
        if self.wonLock:
            print "***Game was won by Player %s.\n" % self.game.currentPlayer + \
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
            print "***Chosen space is not available. Please choose another."
        else:
            self.game.makeMove(square)
            self.do_show(args="")
            print "Player %s chose square %s on board %s" \
                   % (self.game.currentPlayer, square,
                      self.game.board.getNumber())

            if self.game.detectBoardWin():
                print "Player %s has won board %s!" % \
                      (self.game.currentPlayer, self.game.board.getNumber())
                self.game.wins[self.game.board.getNumber()] \
                    = self.game.currentPlayer

            elif self.game.detectBoardDraw() and self.game.board.getNumber()\
            not in self.game.draws \
            and not self.game.wins[self.game.board.getNumber()]:
                print "Board %s has ended in a draw" \
                       % self.game.board.getNumber()
                self.game.draws.append(self.game.board.getNumber())

            if self.game.detectPlayerWin(self.game.currentPlayer):
                print "Player %s has won the game!" % \
                      self.game.currentPlayer
                print "The winning row was on boards %s, %s and %s" % \
                      self.game.getBoardWinRow()
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
            print "Current board: %s" % self.game.board.getNumber()
            print "It is now player %s's turn" % self.game.currentPlayer

            if self.game.checkBoardFilled(self.game.board.getNumber()):
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
                print self.rules
            elif args[0] == "current":
                if self.game.started:
                    print "It is player %s's turn" % self.game.currentPlayer
                    print "Current board: %s" % self.game.board.getNumber()
                else:
                    print "Game has not started yet"
            elif args[0] == "players":
                print "Player 1: X"
                print "Player 2: O"
            else:
                print "***Argument to show is invalid"

    def do_newgame(self, args):
        newgame = GameCmd()
        newgame.cmdloop()

    def do_exit(self, args):
        return True

    do_EOF = do_exit

class MultiBoard:
    """An instance of a multi-board contains 9 individual single Tic
    Tac Toe boards, and contains methods for manipulating those boards."""

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
    """
    An instance of a single board represented as an array of 9 items from 1-9.
    The array represents the Tic Tac Toe board with the top left square
    represented by index 1 and the bottom right square represented by index 9.
    The array contains either "-" for empty, "X" for player 1, or "O" for
    player 2.
    """

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

    def countSquaresFilled(self):
        return 9 - self.singleBoard.count("-")

    def getEmptySquare(self):
        for i,j in enumerate(self.singleBoard):
            if j == "-":
                return i+1

    def show(self):
        print "Board #%s\n" % self.boardNumber
        print " %s    %s    %s\n" % \
              (self.singleBoard[0], self.singleBoard[1], self.singleBoard[2])
        print " %s    %s    %s\n" % \
              (self.singleBoard[3], self.singleBoard[4], self.singleBoard[5])
        print " %s    %s    %s\n" % \
              (self.singleBoard[6], self.singleBoard[7], self.singleBoard[8])

class Game:
    """The game module contains the game state, including the grid of
    individual Tic Tac Toe boards, the current Player, the boards won by
    each player, and the boards drawn."""

    def __init__(self):
        self.multiBoard = MultiBoard()
        self.started = False
        self.currentPlayer = 1
        self.board = None
        self.playerIcons = {0 : "-", 1 : "X", 2 : "O"}
        self.wins = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        self.draws = []

    def detectBoardWin(self):
        # Manually check each row to see if the player has reached a three
        # in a row
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
                    return True
        return False

    def detectBoardDraw(self):
        # If there are less than 8 spaces filled the board is still winnable
        # If there are 9 spaces filled and no one has won, it's a draw
        # Otherwise, it fills the empty space with each player and checks
        # if either player wins. If neither wins, the game is a draw.
        if self.board.countSquaresFilled() == 9:
            if not self.detectBoardWin():
                return True
        elif self.board.countSquaresFilled() == 8:
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
        # The method here to determine a draw is to fill all the empty squares
        # with each player.  If neither player can still win then the game
        # is a draw.
        emptyBoards = []
        for i in range(1,10):
            if i not in self.draws and not self.wins[i]:
                emptyBoards.append(i)
        for empty in emptyBoards:
            self.wins[empty] = 1
        if self.detectPlayerWin(1):
            for empty in emptyBoards:
                self.wins[empty] = 0
            return False
        for empty in emptyBoards:
            self.wins[empty] = 2
        if self.detectPlayerWin(2):
            for empty in emptyBoards:
              self.wins[empty] = 0
            return False
        for empty in emptyBoards:
            self.wins[empty] = 0
        return True

    def detectPlayerWin(self, player):
        # Manually checks each of the 8 possible rows to determine if a player
        # has reached 3 in a row
        currentPlayerWins = [k for k,v in self.wins.iteritems() \
                             if v == player]
        rows = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8],
                [0,4,8], [2,4,6]]
        for row in rows:
            for square in row:
                if square + 1 not in currentPlayerWins:
                    break
            else:
                return True
        return False

    def getBoardWinRow(self):
        # Returns the winning board row as a tuple
        currentPlayerWins = [k for k,v in self.wins.iteritems() \
                     if v == self.currentPlayer]
        rows = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8],
                [0,4,8], [2,4,6]]
        for row in rows:
            for square in row:
                if square + 1 not in currentPlayerWins:
                    break
            else:
                return tuple([i + 1 for i in row])
        return None # Shouldn't ever happen

    def countWins(self, player):
        return self.wins.values().count(player)

    def checkBoardFilled(self, board):
        board = self.multiBoard.getBoard(board)
        if any(map(lambda x: x == "-",
        [board.getSquare(square) for square in range(1, 10)])):
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
            return ", ".join(map(str,self.draws))
        return ""

    def getWinsString(self, player):
        playerWins = \
        map(str, [k for k,v in self.wins.items() if v == player])
        if playerWins:
            return ", ".join(playerWins)
        return ""

    def getRemainingString(self):
        remaining = \
        map(str,[i for i in range(1,10) if i not in self.draws \
            and i not in \
            [k for k,v in self.wins.items() if v in [1,2]]])
        if remaining:
            return ", ".join(remaining)
        return ""


def test():

    # TEST 1 - DETECT DRAWN GAME
    game = Game()
    game.draws = [2, 5, 7, 9]
    assert game.detectDrawnGame() == True
    assert game.detectPlayerWin(1) == False
    assert game.detectPlayerWin(2) == False

    # TEST 2 - DETECT WON GAME
    game = Game()
    game.wins = {1:1,2:1,3:1,4:0,5:0,6:0,7:0,8:0,9:0}
    assert game.detectPlayerWin(1) == True
    assert game.detectPlayerWin(2) == False
    assert game.detectDrawnGame() == False

    # TEST 3 - DETECT DRAWN BOARD
    game = Game()
    game.board = game.multiBoard.getBoard(1)
    game.board.singleBoard = ["-","O","X","X","X","O","O","X","O"]
    game.currentPlayer = 1
    assert game.detectBoardDraw() == True
    assert game.detectBoardWin() == False

    # TEST 4 - DETECT WON BOARD
    game = Game()
    game.board = game.multiBoard.getBoard(1)
    game.board.singleBoard = ["X","X","X","-","-","-","-","-","-"]
    game.currentPlayer = 1
    assert game.detectBoardDraw() == False
    assert game.detectBoardWin() == True

    game.currentPlayer = 2
    assert game.detectBoardDraw() == False
    assert game.detectBoardWin() == False

    # TESTS PASS
    print "Tests pass"


if __name__ == "__main__":
    game = GameCmd()
    game.cmdloop()