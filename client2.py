# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
import curses

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

while key != 27:

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
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048) 
            print message 
        else: 
            # send key pressed
            event = win.getch()
            key = key if event == -1 else event
            server.send(str(key))
server.close() 
