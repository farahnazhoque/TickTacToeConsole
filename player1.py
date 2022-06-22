# echo-client.py
from gameboard import BoardClass
import socket

yn = 'y'
while True:
    try:
        host = input('Please enter the username/IP Address for the player you wish to play with: ')
        port = int(input('Please enter the port for the player you wish to play with: '))
        HOST =  host  # The server's hostname or IP address
        PORT = port  # The port used by the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            s.connect((HOST, PORT))
            userName1 = input('Please enter a valid username with no special characters: ')
            while not userName1.isalnum():
                print("Error: No special characters can be used. Please enter again.")
                userName1 = input('Please enter a valid username with no special characters: ')
                        
            s.sendall(userName1.encode())
            username2 = s.recv(1024).decode()
            print(username2)
            gameBoard1 = BoardClass(userName=userName1, lastUserName= "Ali", other = username2, 
                                                    numWins = 0, numLosses = 0, numTies = 0, numGames = 0,
                                                    conn = s, symbol = "X")
            if not gameBoard1.isRunning:
                break
    
    except:
        print("connection problem..")
        yn = input("If you want to continue press y/Y or else N/n: ")
        if yn == "n" or yn == "N":
            break

