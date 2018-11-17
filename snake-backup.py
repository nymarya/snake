# SNAKES GAME
# Use ARROW KEYS to play, SPACE BAR for pausing/resuming and Esc Key for exiting
# use https://gist.github.com/sanchitgangwar/2158089

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint


class game:



    def __init__(self):
        self.clients = {}

    


    def createSnake(self, addr):
        snake = [[4,10], [4,9], [4,8]]
        key = KEY_RIGHT
        prevKey = key
        client = [ snake, prevKey, key ]
        self.clients[addr] = client


    def execute(self):
        curses.initscr()
        win = curses.newwin(20, 60, 0, 0)  
        win.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        win.border(0)
        win.nodelay(1)

        key = KEY_RIGHT                                                    # Initializing values
        score = 0

        self.createSnake(1)
        
        food = [10,20]                                                     # First food co-ordinates
        win.addch(food[0], food[1], '*')                                   # Prints the food
        

        while key != 27:
            win.border(0)
            win.addstr(0, 2, 'Score : ' + str(score) + ' ')                   # Printing 'Score' and
            win.addstr(0, 27, ' SNAKE ')                                      # 'SNAKE' strings
            #win.timeout(150 - (len(self.snake)/5 + len(self.snake)/10)%120)   # Increases the speed of Snake as its length increases
            
            event = win.getch()
            
            # verifica para cada cliente
            for key, value in self.clients.items():
                snake = value[0] # recupera snake do jogador
                
                value[1] = value[2]                              # Previous key pressed
                value[2] = value[2] if event == -1 else event
                
                if value[2] not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If an invalid key is pressed
                    value[2] = value[1]

                
                if snake[0] in snake[1:]: break
                # If snake runs over itself
                if abs(value[2]-value[1]) != 1 or not(min(value[2], value[1]) != KEY_UP and max(value[2], value[1]) != KEY_LEFT):
                # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
                # This is taken care of later at [1].
                    snake.insert(0, [snake[0][0] + (value[2] == KEY_DOWN and 1) + (value[2] == KEY_UP and -1), snake[0][1] + (value[2] == KEY_LEFT and -1) + (value[2] == KEY_RIGHT and 1)])

                '''else:
                    value[2] = value[1]
                    snake.insert(0, [snake[0][0] + (value[2] == KEY_DOWN and 1) + (value[2] == KEY_UP and -1), snake[0][1] + (value[2] == KEY_LEFT and -1) + (value[2] == KEY_RIGHT and 1)])
                '''

                # Exit if snake crosses the boundaries (Uncomment to enable)
                if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: break


                '''
                if value[0][0] == food:                                            # When snake eats the food
                    food = []
                    score += 1
                    while food == []:
                        food = [randint(1, 18), randint(1, 58)]                 # Calculating next food's coordinates
                        if food in value[0]: food = []
                    win.addch(food[0], food[1], '*')
                else:    
                    last = snake.pop()                                          # [1] If it does not eat the food, length decreases
                    win.addch(last[0], last[1], ' ')
                '''
                
                win.addch(snake[0][0], snake[0][1], '#')




        curses.endwin()
        print("\nScore - " + str(score))
        print("http://bitemelater.in\n")
        
        
    '''
    def game_snake(self):
        


            prevKey = key                                                  # Previous key pressed
            
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
            '''

