import pygame
import random

pygame.init()
pygame.font.init()

#initial parameters/settings
snakeColor = (255,255,0)
appleColor = (0,200,0)
screenColor = (0,0,0)
screenWidth = 800
screenHeight = 800
numOfTiles = 20
tileW = screenWidth / numOfTiles
tileH = screenHeight / numOfTiles
x = 10
y = 10


#creates a screen with specified dimensions 
screen = pygame.display.set_mode((screenWidth, screenHeight))
screen.fill(screenColor)


def drawTile(x,y,w,h,color):
    """ A function that draws a rectangle with specified x,y & width,height & color """
    pygame.draw.rect(screen, color, (x, y, w, h))
    pygame.display.update()




class snake:

    def __init__(self, positionArr, color,gameOn):
        self.positionArr = positionArr
        self.color = color
        self.gameOn = gameOn
    
    def setDirection(self, direction):
        self.direction = direction

    def setTailCord(self,cord):
        self.tailCord = cord

    def drawSnake(self):
        """Draws the snake by itterating over every element in the positionArr"""
        #Erases the previous tail off the screen
        drawTile(self.tailCord[0] * tileW ,self.tailCord[1] * tileH ,tileW,tileH, screenColor)

        #Draws the head of the snake with an "eye"
        drawTile(self.positionArr[0][0] * tileW ,self.positionArr[0][1] * tileH ,tileW,tileH, self.color)
        drawTile(self.positionArr[0][0] * tileW ,self.positionArr[0][1] * tileH ,tileW * 0.3,tileH * 0.3, (80,80,80))

        #Draws the body
        for position in self.positionArr[1:]:
            drawTile(position[0] * tileW ,position[1] * tileH ,tileW,tileH, self.color)


    def detectCollision(self):
        """Checks if the snake hit itself or the bounds and changes gameOn var based on that condition"""

        #Looks if the x-cord is out of bounds and then the same for y-cord
        if self.positionArr[0][0] > numOfTiles - 1 or self.positionArr[0][0] < 0:
            self.gameOn = False
        elif self.positionArr[0][1] > numOfTiles - 1 or self.positionArr[0][1] < 0:
            self.gameOn = False

        #Loops through the array and checks if the head of the snake hit any of the body
        for position in self.positionArr[1:]:
            if position == self.positionArr[0]:
                self.gameOn = False
        



    def move(self):
        """ Moves snake according to the direction given
            The basic logic is that we remove the tail and place it as the new head of the snake
        """
        if self.direction == "UP":
            if len(self.positionArr) != 1:
                self.setTailCord(self.positionArr.pop()) # this line is to keep  track of what to erase for the draw method
                headCord = list(self.positionArr[0])
                headCord[1] -= 1
                self.positionArr.insert(0, headCord)
            else:
                self.positionArr[0][1] -= 1
            self.detectCollision()
        if self.direction == "DOWN":
            if len(self.positionArr) != 1:
                self.setTailCord(self.positionArr.pop())
                headCord = list(self.positionArr[0])
                headCord[1] += 1
                self.positionArr.insert(0, headCord)
            else:
                self.positionArr[0][1] += 1
            self.detectCollision()
        if self.direction == "RIGHT":
            if len(self.positionArr) != 1:
                self.setTailCord(self.positionArr.pop())
                headCord = list(self.positionArr[0])
                headCord[0] += 1
                self.positionArr.insert(0, headCord)
            else:
                self.positionArr[0][0] += 1
            self.detectCollision()
        if self.direction == "LEFT":
            if len(self.positionArr) != 1:
                self.setTailCord(self.positionArr.pop())
                headCord = list(self.positionArr[0])
                headCord[0] -= 1
                self.positionArr.insert(0, headCord)
            else:
                self.positionArr[0][0] -= 1
            self.detectCollision()

    def grow(self):
        """ Adds a new element to position array for the snake"""
        #Takes the tail of the snake and adds it as a new element to the array
        lastCord = list(self.positionArr[-1])
        self.positionArr.append(lastCord)



    
listCords = [[8,10],[9,10],[10,10]] #initial snake array
mySnake = snake(listCords, snakeColor, True)
mySnake.setTailCord([0,0]) #this is there to avoid undefined variable problem (not a clean solution)
mySnake.drawSnake()
mySnake.setDirection("UP")


class apple:

    def spawn(self):
        """ Picks a random location for the apple"""

        self.fairLocation = False

        #Keeps selecting random x and y cords until they fit the parameters
        while not self.fairLocation:
            self.x = random.randint(0,numOfTiles - 1)
            self.y = random.randint(0,numOfTiles - 1)

            #Loops over snake array to check if the proposed cords would be inside the snake
            for position in mySnake.positionArr:
                if self.x == position[0] and self.y == position[1]:
                    self.fairLocation = False
                    break
            else:
                self.fairLocation = True

    def draw(self):
        """ Draws the apple"""
        drawTile(self.x * tileW,self.y * tileH,tileW,tileH,appleColor)


myApple = apple()
myApple.spawn()


def detectSnakeEating():
    """Checks if the snake "ate" the apple"""

    #If the location of the snake head is at the apple make the snake grow and spawn a new apple
    if mySnake.positionArr[0][0] == myApple.x and mySnake.positionArr[0][1] == myApple.y:
        mySnake.grow()
        myApple.spawn()


#Game loop
while True:
    # Process player inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        #keyboard presses check
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and mySnake.direction != "RIGHT":
                mySnake.setDirection("LEFT")
            elif event.key == pygame.K_w and mySnake.direction != "DOWN":
                mySnake.setDirection("UP")
            elif event.key == pygame.K_s and mySnake.direction != "UP":
                mySnake.setDirection("DOWN")
            elif event.key == pygame.K_d and mySnake.direction != "LEFT":
                mySnake.setDirection("RIGHT")
    if mySnake.gameOn:
        # waits some time, accelerates as the snake gets longer
        pygame.time.wait(150 - (len(mySnake.positionArr) * 3)) 
        mySnake.move()
        mySnake.drawSnake()
        detectSnakeEating()
        myApple.draw()

    # if game is over display a "game over" message with your score(snake length)
    else:
        screen.fill(screenColor)
        my_font = pygame.font.SysFont("Comic Sans MS", 30)
        gameOver = my_font.render("Game Over!", False, (255,255,255))
        screen.blit(gameOver, (screenWidth / 2.5, screenHeight / 2.5))
        score = my_font.render("Score: " + str(len(mySnake.positionArr)), False, (255,255,255))
        screen.blit(score, (screenWidth / 2.5, screenHeight / 2.25))
        pygame.display.update()