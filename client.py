# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
import curses
from thread import *
from threading import Thread
from time import sleep

def screenthread(rs,server,win):
    '''Thread that updates the window'''
    while True:
        if(rs[0] is not None):
            for socks in rs[0]: 
                if socks == server: 
                    message = server.recv(2048) 
                    data = str(message).split(',')
                    try:
                        win[0].addch(int(data[0]), int(data[1]), data[2])
                    except:
                        break

def sendthread(win,server, key):
    '''Thread that send te key stroke sginal to the server'''
    while True:
        prevKey = key
        event = win.getch()
        if( event != -1):
            key =  event
            # if key pressed changes
            if( key != prevKey):
                server.send(str(key))
                prevKey = key

#################################
## Begin client code
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
    print "Correct usage: script, IP address, port number"
    exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port))

curses.initscr()
win = curses.newwin(20, 60, 0, 0)  
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)
key = curses.KEY_RIGHT

read_sockets = None
rs = [read_sockets]
start_new_thread(screenthread,(rs,server,[win]))
start_new_thread(sendthread,(win,server, key))

while True:
    win.border(0)
    win.addstr(0, 2, 'Score :+ ')                # Printing 'Score' and
    win.addstr(0, 27, ' SNAKE ')
    win.getch()
    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, server] 

    """ There are two possible input situations. Either the 
    user wants to give manual input to send to other people, 
    or the server is sending a message to be printed on the 
    screen. Select returns from sockets_list, the stream that 
    is reader for input. So for example, if the server wants 
    to send a message, then the if condition will hold true 
    below.If the user wants to send a message, the else 
    condition will evaluate as true"""
    rs[0],write_socket, error_socket = select.select(sockets_list,[],[])
    

curses.endwin()
server.close() 