# SNAKES GAME
# Use ARROW KEYS to play, SPACE BAR for pausing/resuming and Esc Key for exiting
# use https://gist.github.com/sanchitgangwar/2158089

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
import random
from random import randint
from thread import *
from threading import Thread


class game:
    def __init__(self):
        self.clients = {}
        random.seed()



    def createSnake(self, addr):
        client = []
        rand1 = randint(0,10)
        rand2 = randint(0,10)
        client.insert(0, [[rand1,10], [rand1,9], [rand1,8]] )         # Initial snake co-ordinates
        
        client.insert(1, KEY_RIGHT)
        client.insert(2, KEY_RIGHT)
        self.clients[addr] = client



    def gamethread(self, key, win, score, food, broadcast):
        
        while True:
            while key != 27:                                                  # While Esc key is not pressed
                win.border(0)
                win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # Printing 'Score' and
                win.addstr(0, 27, ' SNAKE ')                                   # 'SNAKE' strings

                
                for id, value in self.clients.items():
                
                    client = self.clients[id]

                    # recupera o snake do cliente atual
                    snake = client[0]
                    key = client[1]                                                    # Initializing values
                    prevKey = client[2]
                                
                        
                    win.timeout(300)          # Increases the speed of Snake as its length increases
                    
                    prevKey = key                                                  # Previous key pressed
                    event = win.getch()
                    #moves = [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT ]
                    #event = random.shuffle(moves)
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
                        broadcast(food[0], food[1], '*')
                    else:    
                        last = snake.pop()                                          # [1] If it does not eat the food, length decreases
                        win.addch(last[0], last[1], ' ')
                        broadcast(last[0], last[1], ' ')
                    
                    try:
                        win.addch(snake[0][0], snake[0][1], '#')
                        broadcast(snake[0][0], snake[0][1], '#')
                    except:
                        break

                    # atualiza valores no map do cliente
                    newClient = []
                    newClient.insert(0, snake)
                    newClient.insert(1, key)
                    newClient.insert(2, prevKey)
                    self.clients[id] = newClient
            break          

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


        key = KEY_RIGHT
       
        processo=Thread(target=self.gamethread, args=(key, win, score, food, broadcast))  
        processo.start()


        curses.endwin()
        print("\nScore - " + str(score))
        print("http://bitemelater.in\n")