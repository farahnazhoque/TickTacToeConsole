
class BoardClass:
    
    """A simple class to note the updates and moves occurring within the game

    Attributes:
        userName (str): The usernames for players.
        otherUserName (str): This displays the username of the player against whom
        each player is playing.
        lastUserName (str): The username of the last player's turn.
        numWins (int): Number of times a player wins.
        numLosses (int): Number of times a player loses.
        numTies (int): Number of times neither players wins or loses.
        numGames (int): Number of games being started.
        conn (int): The connection between player1(client) and player2(server), defined.
        symbol (str): The move made by either player.

        """


    def __init__(self, userName = "", other = "", lastUserName = "", numWins = 0,
                 numLosses = 0, numTies = 0, numGames = 0, conn = 0,
                 symbol = "X"):
        """Make a BoardClass.

        Args:
            userName: The usernames for the players.
            otherUserName: This displays the username of the player against whom
            each player is playing.
            lastUserName: The username of the last player's turn.
            numWins: Number of times a player wins.
            numLosses: Number of times a player loses.
            numTies: Number of times neither player wins or loses.
            numGames: Number of games being started.
            conn: The connection between player1(client) and player2(server), defined.
            symbol: The move made by either player.

        """
        self._userName = userName
        self._otherUserName = other 
        self._lastUserName = lastUserName
        self._numWins = numWins
        self._numLosses = numLosses
        self._numTies = numTies
        self._numGames = numGames
        self._board = [['', '', ''],
                       ['', '', ''],
                       ['', '', '']]
        self._conn = conn
        self._symbol = symbol
        self.isRunning = True
        if symbol == "X".upper():
            self.askUser()
        elif symbol == "O".upper():
            self.receiveData()
        '''This is occurring simultaneously in two terminal.'''


    def updateGamesPlayed(self):
        """This will be incremented every time a new game starts
        and this function is called.
        """
        self._numGames += 1


    def resetGameBoard(self):
        """This function clears the game board by replacing the
        old one with a new, clear game board every time this function
        is called.
        """
        self._board = [['', '', ''],
                       ['', '', ''],
                       ['', '', '']]

    
    
    def askUser(self):
        """This function will first ask the server player for the placement of
        their move with X, and then send the data in bits to the client of the move,
        and it will go back and forth as in the end of the function we call the
        receiveData() function to gather and decode the data from the client
        player.
        """
    
        try:
            r = int(input('Enter a position r: '))
            c = int(input('Enter a position c: '))
            if self._board[r][c] != '':
                print('This is an invalid position. Please try again.')
                return self.askUser()
        except TypeError:
            print("Type error please enter an integer.")
            return self.askUser()
        except IndexError:
            print('Index is out of range. Please try again.')
            return self.askUser()
        except ValueError:
            print('Asked for an integer, got a string instead.')
            return self.askUser()

        except:
            print('Error: Please Try Again.')
            return self.askUser()

        '''Becuase it only sends in byte
        as strings, int are all python defines.
        '''
        #update the game board
        self.updateGameBoard(r,c, self._symbol)
        
        #send the data to other user
        data = str(r) + ',' + str(c)
        self._conn.sendall(data.encode())
        if self.isWinner() or self.boardIsFull():
            return self.restart()
        if self.isRunning:
            self.receiveData()
        

        '''Once the player provides the input it sends data and asks
        for data from the other player and it keeps on going back and forth.'''
        

    def restart(self):
        """The purpose of this function is to get input from player1
        whether or not they want to restart the game or not, and start the entire
        process if yes, or terminate the program if no.
        """
        self.updateGamesPlayed()

    
        if self._symbol == 'X':
            try:
                playAgain = input('Do you want to play again, Y/y or N/n: ')
                assert playAgain == 'Y' or playAgain == 'y' or playAgain == 'n' or playAgain == 'N'
                if playAgain == 'y' or playAgain == 'Y':
                    self._conn.sendall('Play Again'.encode())
                    self.resetGameBoard()
            
                    return self.askUser()
                        
                elif playAgain == 'n' or playAgain == "N":
                    self._conn.sendall('Fun Times'.encode())
                    self.printStats()
                    self.isRunning = False
                    return
            except AssertionError:
                print('Please enter y or n only.')
                self.restart()
            except:
                print('There was an error. Please try again.')
                self.restart()
                 
        else:
            print('Waiting for player 1 to decide...')
            playAgain = self._conn.recv(1024)
            playAgain=playAgain.decode()
            if playAgain == 'Play Again':
                print('Play Again')
                self.resetGameBoard()
                return self.receiveData()
            else:
                print(playAgain)
                self.printStats()

                 #closed it but still not closing
                return




    def receiveData(self):
        """This is called when the client player makes a move and is done when the
        server player also receives data from the client player. Here, we also
        check if a game has won or tied, in order to restart the game accordingly.
        """
        data = self._conn.recv(1024)
        data = data.decode()
        #converting it back to string
        data = data.split(",")
        r, c = int(data[0]), int(data[1])
        if self._symbol == "X".upper():
            self.updateGameBoard(r,c, "O".upper())
        elif self._symbol == "O".upper():
            self.updateGameBoard(r,c, "X".upper())


        if self.isWinner() or self.boardIsFull():
            return self.restart()
        self.askUser()

    def printBoard(self):
        """This function will print out the board everytime it has been updated
        by the updateGameBoard() function.
        """
        print()
        for row in self._board:
            for cell in row:
                if cell=='':
                    print("*", end='')
                else:
                    print(cell, end='')
            print()
    def updateGameBoard(self, r, c, symbol):
        """This function is called every time a player updates a move, and this
        updates it to the actual gameboard. Not only that, it also updates and
        checks the number of times a player has won or lost.
        It also checks which player made the last move, and updates the statistical
        data accordiningly.
        """
                
        self._board[r][c] = symbol
        self.printBoard()


        if self.isWinner():
            if symbol == self._symbol:
                self._lastUserName = self._userName
                self._numWins += 1

            else:
                self._numLosses += 1
                self._lastUserName = self._otherUserName
        elif self.boardIsFull():
            self._numTies += 1
            if symbol == self._symbol:
                self._lastUserName = self._userName
            else:
                self._lastUserName = self._otherUserName

                
            

        

    def isWinner(self):
        """This function checks if there is a win(or loss for the other player)
        and is called when it is time to update how many times each player
        has won or lost.
        """
        board = self._board
        for i in range(3):
            if board[i][0]==board[i][1]==board[i][2] and board[i][0]!='':
                return True
            if board[0][i]==board[1][i]==board[2][i] and board[0][i]!='':
                return True
        if board[0][0]==board[1][1]==board[2][2] and board[1][1]!='':
            return True
        if board[0][2]==board[1][1]==board[2][0] and board[1][1]!='':
            return True
        return False

    def printStats(self):
        """The purpose of this function is to print out the stats
        to both the players after a game is won/lost/tied.
        Prints the players user name
        Prints the user name of the last person to make a move
        prints the number of games
        Prints the number of wins
        Prints the number of losses
        Prints the number of ties

        """
        print('Username: ', self._userName)
        print('Username of the last player to make a move: ', self._lastUserName)
        print('Number of games played: ', self._numGames)
        print('Number of wins: ', self._numWins)
        print('Number of losses: ', self._numLosses)
        print('Number of ties: ', self._numTies)


    def boardIsFull(self):
        """This function checks if the gameboard is full or not, and returns
        true if it is and is called when it is time to update the number of
        ties.
        """
        board = self._board
        ties = False        
        count = 0
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != '':
                    count += 1
            
        if count == 9:
            ties = True

        return ties
        
    
        
        
