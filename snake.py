from numpy.lib import add_newdoc_ufunc
import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
pygame.init() #initiate all the model correctly
font = pygame.font.Font('arial.ttf',30)


# after each game, agent can reset the game

# reward for agent

# transfer play(action) to direction

# keep track of the game_iteration

# check collision function




class Direction(Enum): #inherit from Enum
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4 


Point = namedtuple('Point','x, y')
BLOCKSIZE =20
SPEED = 5

#rbg colors
WHITE = (255,255,255)
RED = (200,0,0)
BLUE1= (0,0,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)




class SnakeGameAI:
    def __init__(self,w=640,h=480): #constructor:The __init__ method can be called when an object is created from the class, and access is required to initialize the attributes of the class
                                    #default value for w and h
        self.w = w
        self.h = h

        #initial display
        self.display = pygame.display.set_mode((self.w,self.h)) #Initialize a window or screen for display
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock() # set the clock
        
        self.reset()


    def reset(self):
        #initial game state
        self.direction = Direction.RIGHT # initial direction is move to the right
        self.head = Point(self.w/2,self.h/2) # initial position of the head
        self.snake = [self.head, Point(self.head.x - BLOCKSIZE, self.head.y),
                    Point(self.head.x-(2*BLOCKSIZE),self.head.y)]
        self.score = 0
        self.food = None
        self._place_food() #ramdomly place the food
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCKSIZE) // BLOCKSIZE) *BLOCKSIZE # so x would be multipels of the blocksize
        y = random.randint(0, (self.h-BLOCKSIZE) // BLOCKSIZE) *BLOCKSIZE
        self.food = Point(x,y)
        if self.food in self.snake: #make sure the food and snake not overlap
            self._place_food()




    def play_step(self,action):
        self.frame_iteration +=1
        #collect the user input
        for event in pygame.event.get(): #get all the user event
            if event.type ==pygame.QUIT:
                pygame.quit()
                quit()  #quit the python program
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT:
            #         self.direction = Direction.LEFT
            #     elif event.key == pygame.K_RIGHT:
            #         self.direction = Direction.RIGHT
            #     elif event.key == pygame.K_UP:
            #         self.direction = Direction.UP
            #     elif event.key == pygame.K_DOWN:
            #         self.direction = Direction.DOWN  
        #move
        self._move(action)
        self.snake.insert(0,self.head) #insert a new head in the begining

        #check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake): # if collision or no response
            game_over = True
            reward = -10
            return reward, game_over, self.score


        #place new food or just move 
        if self.head == self.food:
            self.score +=1
            reward =10
            self._place_food() # if collide with food ,then dont remove the last piece of snake
        else:
            self.snake.pop() #remove the last piece of snake while it moving
        #update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)


        #return game over and score
        game_over = False
        return reward, game_over, self.score
    

    def is_collision(self,point=None):
        if point is None:
            point = self.head
        #if hits boundary
        if point.x > self.w-BLOCKSIZE or point.x <0 or point.y > self.h-BLOCKSIZE or point.y<0:
            return True
        
        #hit itself
        if point in self.snake[1:]:
            return True
        
        return False


    def _update_ui(self):
        self.display.fill(BLACK)

        for p in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(p.x,p.y,BLOCKSIZE,BLOCKSIZE)) #draw the snake
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(p.x+4, p.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCKSIZE, BLOCKSIZE)) #draw the food
        
        text = font.render("Score: "+ str(self.score),True,WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip() # update display service to the screen


    def _move(self,action):
        # go straight, turn left, turn right
        clock_wise = [Direction.RIGHT, Direction.DOWN,Direction.LEFT,Direction.UP]
        index = clock_wise.index(self.direction)

        if np.array_equal(action,[1,0,0]):
            new_direction = clock_wise[index]  #go straight

        elif np.array_equal(action,[0,1,0]):
            new_direction = clock_wise[(index+1)%4]  #go right
        else:
            new_direction = clock_wise[(index-1)%4]  #go left

        self.direction = new_direction

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCKSIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCKSIZE
        elif self.direction == Direction.UP:
            y -= BLOCKSIZE
        elif self.direction == Direction.DOWN:
            y += BLOCKSIZE

        self.head = Point(x,y)
    
# if __name__ == '__main__': # is used to execute some code only if the file was run directly, and not imported
#     game = SnakeGameAI()
    
#     #game loop
#     while True:
#         game_over, score =game.play_step()

#         if game_over == True:
#             break 

    
#     print('Final Score: ', score)
#     pygame.quit()