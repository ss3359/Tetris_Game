
#Dependencies 
import math 
import random
import numpy as np 
import pandas as pd 
import pygame
import sys 
import os



#Initalize The Pygame Library
pygame.init()

# Constant Variables
WIDTH=300
HEIGHT=500
FPS=35
BLOCK=20
ROWS=(HEIGHT-120)//BLOCK
COLUMNS=WIDTH//BLOCK

# Colors 
WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
DARKGREEN = ( 0, 155, 0)
DARKGRAY = ( 40, 40, 40)
PURPLE = (128, 0, 128)
DARKBLUE=(0,0,139)
PINK=(231, 84, 128)
ORANGE=(255,165,0)
BGCOLOR = BLACK

#Game Settings (screen, clock, title)
WINDOW=pygame.display.set_mode((WIDTH,HEIGHT),pygame.NOFRAME)
CLOCK=pygame.time.Clock()
pygame.display.set_caption("Playing With Blocks!")

#Load/Store Images
SQUARE_IMAGES={
    1:pygame.image.load("IMAGES/1.png"),
    2:pygame.image.load("IMAGES/2.png"), 
    3:pygame.image.load("IMAGES/3.png"), 
    4:pygame.image.load("IMAGES/4.png"),
 
}


#Fonts
font1=pygame.font.SysFont("verdana",50)
font2=pygame.font.SysFont("verdana",15)

#Classes
#Shape Class    
class Shape: 
    VERSIONS={
        "I":[[1,5,9,13],[4,5,6,7]],
        "Z":[[4,5,9,10],[2,6,5,9]],
        "L":[[1,2,5,9],[0,4,5,6],[1,5,9,8],[4,5,6,10]],
        "S":[[6,7,9,10],[1,5,6,10]],
        "J":[[1,2,6,10],[5,6,7,9],[2,6,10,11],[3,5,6,7]],
        "T":[[1,4,5,6],[1,4,5,9],[4,5,6,9],[1,5,6,9]],
        "O":[[1,2,5,6]]
    }
    SHAPES=["I","Z","L","S","J","T","O"]

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.type=random.choice(self.SHAPES)
        self.shape=self.VERSIONS[self.type]
        self.color=random.randint(1,4)
        self.orientation=0
        
    def image(self): 
        return self.shape[self.orientation]
    #rotate method
    def rotate(self): 
        self.orientation=(self.orientation+1)%len(self.shape)


#Game Class
class Game:
    #Constructor
    def __init__(self,rows,columns):
        self.r=rows
        self.c=columns
        self.level=1
        self.score=0
        self.grid=[[0 for i in range(columns)] for j in range(rows)] 
        self.next=None
        self.end=False
        self.NewShape()
        pass
    # Make Grid 
    def MakeGrid(self): 
        for j in range(self.r+1): 
            pygame.draw.line(WINDOW,RED,(0,j*BLOCK),(WIDTH,j*BLOCK))
        for i in range(self.c+1): 
            pygame.draw.line(WINDOW,RED,(BLOCK*i,0),(BLOCK*i,HEIGHT-120))

    #Spawn A Shape
    def NewShape(self):
        if not self.next: 
            self.next=Shape(5,0)
        self.figure=self.next
        self.next=Shape(5,0)
    #Check For Collison 
    def collision(self): 
        for i in range(4): 
            for j in range(4): 
                if(i*4+j in self.figure.image()): 
                    block_row=i+self.figure.y
                    block_column=j+self.figure.x
                    if(block_row>=self.r or block_column>=self.c or block_column<0 or self.grid[block_row][block_column]>0): 
                        return True
        return False            


    #Freeze
    def Freeze(self):
        for i in range(4): 
            for j in range(4): 
                if(i*4+j in self.figure.image()): 
                    self.grid[i+self.figure.y][j+self.figure.x]=self.figure.color
            
        self.RemoveRow()
        self.NewShape()
        if(self.collision()):
            self.end=True 


         


    #Remove A Row
    def RemoveRow(self): 
        rerun=False
        for y in range(self.r-1,0,-1):
            completed=True
            for x in range(0,self.c,): 
                if(self.grid[y][x]==0):
                    completed=False
            if(completed):
                del self.grid[y]
                self.grid.insert(0,[0 for x in range(self.c)])
                self.score+=1
                if(self.score%10==0): 
                    self.level+=1
                rerun=True
        if(rerun): 
            self.RemoveRow()
        
    
    #Move Right 
    def MoveRight(self): 
        self.figure.x+=1
        if(self.collision()): 
            self.figure.x-=1

    #Move Left 
    def MoveLeft(self): 
        self.figure.x-=1
        if (self.collision()): 
            self.figure.x+=1

    #Move Down
    def MoveDown(self): 
        self.figure.y+=1
        if(self.collision()):
            self.figure.y-=1
            self.Freeze()

    #Freefall Method
    def FreeFall(self): 
        while(not self.collision()): 
            self.figure.y+=1
        self.figure.y-=1
        self.Freeze()

    #Rotate Shape
    def Rotate(self): 
        orientation=self.figure.orientation
        self.figure.rotate()
        if(self.collision()): 
            self.figure.orientation=orientation
    #Reset The Game
    def ResetGame(self): 
        PopUp=pygame.Rect(50,140,WIDTH-100,HEIGHT-350)
        pygame.draw.rect(WINDOW,BLACK,PopUp)
        pygame.draw.rect(WINDOW,PURPLE,PopUp,2)

        end=font2.render("Game Over", True,WHITE)
        option1=font2.render("Press r to restart", True,WHITE)
        option2=font2.render("Press q to quit", True,WHITE)
        WINDOW.blit(end,(PopUp.centerx-end.get_width()/2,PopUp.y+20))
        WINDOW.blit(option1,(PopUp.centerx-option1.get_width()/2,PopUp.y+80))
        WINDOW.blit(option2,(PopUp.centerx-option2.get_width()/2,PopUp.y+110))





                

#Game Loop
def main(): 
    run=True
    counter=0
    move=True
    SpacePressed=False
    Tetris=Game(ROWS,COLUMNS)
    while(run):
        WINDOW.fill(DARKBLUE)
        for event in pygame.event.get(): 
            if event.type==pygame.QUIT: 
                run=False
                sys.exit()

        keys=pygame.key.get_pressed()
        if(not Tetris.end): 
            if keys[pygame.K_LEFT]:
                Tetris.MoveLeft()
            elif keys[pygame.K_RIGHT]: 
                Tetris.MoveRight()
            elif keys[pygame.K_UP]: 
                Tetris.Rotate()
            elif keys[pygame.K_DOWN]:
                Tetris.MoveDown()
            elif keys[pygame.K_SPACE]: 
                SpacePressed=True
            if keys[pygame.K_r]: 
                Tetris.__init__(ROWS,COLUMNS)
        if(keys[pygame.K_ESCAPE] or keys[pygame.K_q]): 
            run=False

        counter+=1
        if(counter>=10000):
            counter=0
        if(move==True): 
            if(counter%(FPS//(Tetris.level*2))==0):
                if not Tetris.end: 
                    if SpacePressed: 
                        Tetris.FreeFall()
                        SpacePressed=False
                    else: 
                        Tetris.MoveDown()

        Tetris.MakeGrid()

        for x in range(ROWS): 
            for y in range(COLUMNS): 
                if(Tetris.grid[x][y]>0): 
                    value=Tetris.grid[x][y]
                    image=SQUARE_IMAGES[value]
                    WINDOW.blit(image,(y*BLOCK,x*BLOCK))
                    pygame.draw.rect(WINDOW,WHITE,(y*BLOCK,x*BLOCK,BLOCK,BLOCK),width=1)

        #Show Shape On The Screen
        if Tetris.figure:
            for i in range(4): 
                for j in range(4): 
                    if(i*4+j in Tetris.figure.image()):
                        shape=SQUARE_IMAGES[Tetris.figure.color]
                        x=BLOCK*(Tetris.figure.x+j)
                        y=BLOCK*(Tetris.figure.y+i)
                        WINDOW.blit(shape,(x,y))
                        pygame.draw.rect(WINDOW,GREEN,(x,y,BLOCK,BLOCK),width=1)
        
        #The panel Screen 
        if(Tetris.next):
            for i in range(4): 
                for j in range(4):
                    if(i*4+j in Tetris.next.image()): 
                        image=SQUARE_IMAGES[Tetris.next.color] 
                        x=BLOCK*(Tetris.next.x+j-4)
                        y=HEIGHT-100+BLOCK*(Tetris.next.y+i)
                        WINDOW.blit(image,(x,y))

        #end of game
        if(Tetris.end): 
            Tetris.ResetGame()

        #Score And Level
        score_text=font1.render(f"{Tetris.score}",True,WHITE)
        levels_text=font2.render(f"LEVEL: {Tetris.level}",True,WHITE)
        WINDOW.blit(score_text,(250-score_text.get_width()//2,HEIGHT-110))
        WINDOW.blit(levels_text,(250-levels_text.get_width()//2,HEIGHT-30))


        pygame.display.update()
        CLOCK.tick(FPS)

main()