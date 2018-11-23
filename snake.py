# SNAKES GAME
# Use ARROW KEYS to play, SPACE BAR for pausing/resuming and Esc Key for exiting
# use https://gist.github.com/sanchitgangwar/2158089

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
import random
from random import randint
from thread import *
from threading import Thread
import time

class game:

    clients = {}
    def __init__(self):
        random.seed()


    def killSnake(self, addr, broadcast):
        # Erase snake
        for piece in self.clients[addr][0]:
            broadcast(piece[0], piece[1], ' ')
        # Remove client
        del self.clients[addr]


    def moveSnake(self, addr, move):
        try:
            client = self.clients[addr]
            snake = client[0]
            key = client[1]
            prevKey = client[2]
            prevKey = key           # atribui a atual pra anterior
            if( move == 65 and prevKey != KEY_RIGHT ):
                key = KEY_LEFT      # move pra esquerda
            if( move == 68 and prevKey != KEY_LEFT):
                key = KEY_RIGHT     # move pra direita
            if( move == 87 and prevKey != KEY_DOWN ):
                key = KEY_UP        # move pra cima
            if( move == 83 and prevKey != KEY_UP):
                key = KEY_DOWN      # move pra baixo
            
            newClient = []
            newClient.insert(0, snake)
            newClient.insert(1, key)
            newClient.insert(2, prevKey)
            self.clients[addr] = newClient
        except Exception as e: 
            pass


    def createSnake(self, addr):
        client = []
        rand1 = randint(0,10)
        rand2 = randint(0,10)
        client.insert(0, [[rand1,10], [rand1,9], [rand1,8]] )         # Initial snake co-ordinates
        
        client.insert(1, KEY_RIGHT)
        client.insert(2, KEY_RIGHT)
        self.clients[addr] = client 


    def gamethread(self, key, win, score, food, broadcast):
        keep_running = True
        while True:
            while keep_running:                                                  # While Esc key is not pressed
                win.border(0)
                win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # Printing 'Score' and
                win.addstr(0, 27, ' SNAKE ')                                   # 'SNAKE' strings

                
                for id, value in self.clients.items():
                
                    #recupera um cliente 
                    try:
                        client = self.clients[id]   
                    except:
                        break

                    # recupera o snake do cliente atual
                    snake = client[0]
                    # recupera a tecla clicada pelo cliente 
                    key = client[1]       
                    # recupera a tecla da iteracao passada
                    prevKey = client[2]
                                
                    # Increases the speed of Snake as its length increases
                    win.timeout(300) 
                    time.sleep(5)         
                    
                    #prevKey = key                                                 
                    event = win.getch()

                    snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])


                    # Exit if snake crosses the boundaries (Uncomment to enable)
                    if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: 
                        if len(self.clients.keys()) > 1:
                            self.killSnake(id, broadcast)
                        else:
                            keep_running = False
                        break


                    try:
                        if snake[0] == food:                                            # When snake eats the food
                            food = []
                            score += 1
                            while food == []:
                                food = [randint(1, 18), randint(1, 58)]                 # Calculating next food's coordinates
                                if food in snake: food = []
                            win.addch(food[0], food[1], '*')
                            broadcast(food[0], food[1], '*')
                        else:    
                            last = snake.pop()                                          # [1] If it does not eat the food, length decreases
                            win.addch(last[0], last[1], ' ')
                            broadcast(last[0], last[1], ' ')
                      

                        win.addch(snake[0][0], snake[0][1], '#')
                        broadcast(snake[0][0], snake[0][1], '#')
                    except:
                        # if there are more than one snakes, kill the snake
                        # if there is only one snake, end game
                        if len(self.clients.keys()) > 1:
                            self.killSnake(id, broadcast)
                        else:
                            keep_running = False
                        break
                    
                    
                    # atualiza valores no map do cliente
                    self.clients[id][0] = snake
                      

    def execute(self, broadcast):
        curses.initscr()
        win = curses.newwin(20, 60, 0, 0)  
        win.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        win.border(0)
        win.nodelay(1)

        score = 0

        food = [10,20]                                                     # First food co-ordinates
        
        win.addch(food[0], food[1], '*')                                   # Prints the food
        broadcast(food[0], food[1], '*')

        key = KEY_RIGHT
       
        processo=Thread(target=self.gamethread, args=(key, win, score, food, broadcast))  
        processo.start()

        #processo.join()
        curses.endwin()
        print("\nScore - " + str(score))
        print("http://bitemelater.in\n")