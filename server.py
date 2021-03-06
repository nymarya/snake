# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
from thread import *
from threading import Thread
import snake
from time import sleep


"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit() 

# takes the first argument from command prompt as IP address 
IP_address = str(sys.argv[1]) 

# takes second argument from command prompt as port number 
Port = int(sys.argv[2]) 

""" 
binds the server to an entered IP address and at the 
specified port number. 
The client must be aware of these parameters 
"""
server.bind((IP_address, Port)) 

""" 
listens for 100 active connections. This number can be 
increased as per convenience. 
"""
server.listen(100) 

list_of_clients = [] 

def clientthread(conn, addr): 

    # quando aceitar conexao, cria cobra
    game.createSnake(conn)

    while True: 
        try: 
            message = conn.recv(2048) 
            if message: 

                """prints the message and address of the 
                user who just sent the message on the server 
                terminal"""

                key = int(message)
                game.moveSnake(conn, key)
            else: 
                """message may have no content if the connection 
                is broken, in this case we remove the connection"""
                remove(conn) 

        except Exception as e: 
            continue

"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(pos1, pos2, message): 
    for client in list_of_clients: 
        try: 
            client[0].send(str(pos1) + "," + str(pos2) + "," + message +",") 
        except: 
            client[0].close() 
            game.killSnake(client[1], broadcast)
            # if the link is broken, we remove the client 
            remove(client[0])  

"""The following function simply removes the object 
from the list that was created at the beginning of 
the program"""
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 

while True: 

    # get instance of game
    game = snake.game()
    game.execute(broadcast)


    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    conn, addr = server.accept() 

    """Maintains a list of clients for ease of broadcasting 
    a message to all available people in the chatroom"""
    list_of_clients.append([conn, addr]) 


    # creates and individual thread for every user 
    # that connects 
    start_new_thread(clientthread,(conn,addr))     

#conn.close() 
server.close() 
