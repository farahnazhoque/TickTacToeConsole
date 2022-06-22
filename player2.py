import socket
from gameboard import BoardClass


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    yn = "y"
    conn = ""
    while True:
        try:
            #HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
            #PORT = 5100  # Port to listen on (non-privileged ports are > 1023)
            HOST = input("What is the IP address: ")
            PORT = int(input("What is the port number: "))
            
            s.bind((HOST, PORT))
            s.listen()
      
            conn, addr = s.accept() #this is where the program will get stuck
                #until someone connects
            break
       
        except:
            print("connection problem..")
            yn = input("If you want to continue press y/Y or else N/n: ")
            if yn == "n" or yn == "N":
                break
                
    if yn.lower() == "y":
        with conn:
            username1 = conn.recv(1024).decode()
            print(username1)
            username2 = 'player2'

                    
            conn.sendall(username2.encode())
            gameBoard2 = BoardClass(userName=username2, lastUserName="Farahnaz", other = username1,
                                    numWins = 0, numLosses = 0, numTies = 0, numGames = 0, conn = conn, symbol = "O")
                
    else:
        print("The program exits.")
        

