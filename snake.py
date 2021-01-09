import pygame
import random
from enum import Enum
from collections import namedtuple
pygame.init() #initiate all the model correctly
font = pygame.font.Font('arial.ttf',30)



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




class SnakeGame:
    def __init__(self,w=640,h=480): #constructor:The __init__ method can be called when an object is created from the class, and access is required to initialize the attributes of the class
                                    #default value for w and h
        self.w = w
        self.h = h

        #initial display
        self.display = pygame.display.set_mode((self.w,self.h)) #Initialize a window or screen for display
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock() # set the clock
        
        #initial game state
        self.direction = Direction.RIGHT # initial direction is move to the right
        self.head = Point(self.w/2,self.h/2) # initial position of the head
        self.snake = [self.head, Point(self.head.x - BLOCKSIZE, self.head.y),
                    Point(self.head.x-(2*BLOCKSIZE),self.head.y)]
        self.score = 0
        self.food = None
        self._place_food() #ramdomly place the food

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCKSIZE) // BLOCKSIZE) *BLOCKSIZE # so x would be multipels of the blocksize
        y = random.randint(0, (self.h-BLOCKSIZE) // BLOCKSIZE) *BLOCKSIZE
        self.food = Point(x,y)
        if self.food in self.snake: #make sure the food and snake not overlap
            self._place_food()




    def play_step(self):
        #collect the user input
        for event in pygame.event.get(): #get all the user event
            if event.type ==pygame.QUIT:
                pygame.quit()
                quit()  #quit the python program
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN  
        #move
        self._move(self.direction)
        self.snake.insert(0,self.head) #insert a new head in the begining

        #check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score


        #place new food or just move 
        if self.head == self.food:
            self.score +=1
            self._place_food() # if collide with food ,then dont remove the last piece of snake
        else:
            self.snake.pop() #remove the last piece of snake while it moving
        #update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)


        #return game over and score
        game_over = False
        return game_over, self.score
    

    def _is_collision(self):
        #if hits boundary
        if self.head.x > self.w-BLOCKSIZE or self.head.x <0 or self.head.y > self.h-BLOCKSIZE or self.head.y<0:
            return True
        
        #hit itself
        if self.head in self.snake[1:]:
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


    def _move(self,direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCKSIZE
        elif direction == Direction.LEFT:
            x -= BLOCKSIZE
        elif direction == Direction.UP:
            y -= BLOCKSIZE
        elif direction == Direction.DOWN:
            y += BLOCKSIZE

        self.head = Point(x,y)
    
if __name__ == '__main__': # is used to execute some code only if the file was run directly, and not imported
    game = SnakeGame()
    
    #game loop
    while True:
        game_over, score =game.play_step()

        if game_over == True:
            break 

    
    print('Final Score: ', score)
    pygame.quit()