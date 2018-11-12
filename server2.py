# Python program to implement server side of chat room. 
import socket, pickle
import select 
import sys 
from thread import *
from threading import Thread
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
    print "Correct usage: script, IP address, port number"
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

curses.initscr()
win = curses.newwin(20, 60, 0, 0)  
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

key = KEY_RIGHT                                                    # Initializing values
score = 0

snake = [[4,10], [4,9], [4,8]] 
snake1 = [[6,10], [6,9], [6,8]]                                     # Initial snake co-ordinates
food = [10,20]
win.addch(food[0], food[1], '*')

def gamethread(key, win, score, food, snake):
    """"""
    print("a")
    while True:
        while key != 27:                                                   # While Esc key is not pressed
            win.border(0)
            win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # Printing 'Score' and
            win.addstr(0, 27, ' SNAKE ')                                   # 'SNAKE' strings
            win.timeout(150 - (len(snake)/5 + len(snake)/10)%120)          # Increases the speed of Snake as its length increases
            
            prevKey = key                                                  # Previous key pressed
            event = win.getch()
            key = key if event == -1 else event 


            if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If an invalid key is pressed
                key = prevKey


            # If snake runs over itself
            #if snake[0] in snake[1:]: break
            if abs(key-prevKey) != 1 or not(min(key, prevKey) != KEY_UP and max(key, prevKey) != KEY_LEFT):
                # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
                # This is taken care of later at [1].
                snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

            else:
                key = prevKey
                snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

            # Exit if snake crosses the boundaries (Uncomment to enable)
            if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: break


            if snake[0] == food:                                            # When snake eats the food
                food = []
                score += 1
                while food == []:
                    food = [randint(1, 18), randint(1, 58)]                 # Calculating next food's coordinates
                    if food in snake: food = []
                win.addch(food[0], food[1], '*')
            else:    
                last = snake.pop()                                          # [1] If it does not eat the food, length decreases
                win.addch(last[0], last[1], ' ')
            
            win.addch(snake[0][0], snake[0][1], '#')

        
            broadcast(pickle.dumps(win))

        curses.endwin()


def clientthread(conn, addr): 

    # sends a message to the client whose user object is conn 
    conn.send("Welcome to this chatroom!") 

    while True:
            try:
                message = conn.recv(2048) 
                if message: 

                    """prints the message and address of the 
                    user who just sent the message on the server 
                    terminal"""
                    # print "<" + addr[0] + "> " + message 

                    # Calls broadcast function to send message to all 
                    #message_to_send = "<" + addr[0] + "> " + message 
                    #broadcast(message_to_send, conn) 

                else: 
                    """message may have no content if the connection 
                    is broken, in this case we remove the connection"""
                    remove(conn) 
                
                
            except: 
                continue

"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message): 
    if clients!=connection: 
        try: 
            clients.send(message) 
        except: 
            clients.close() 

            # if the link is broken, we remove the client 
            remove(clients) 

"""The following function simply removes the object 
from the list that was created at the beginning of 
the program"""
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 

processo=Thread(target=gamethread, args=(key, win, score, food, snake))  
processo.start()
'''
while True: 

    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    conn, addr = server.accept() 

    """Maintains a list of clients for ease of broadcasting 
    a message to all available people in the chatroom"""
    list_of_clients.append(conn) 

    # prints the address of the user that just connected 
    print addr[0] + " connected"

    # creates and individual thread for every user 
    # that connects 
    start_new_thread(clientthread,(conn,addr))
     
'''

#conn.close() 
server.close() 
