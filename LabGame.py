import pygame
import sys
pygame.init()

"""
ls
git add <filename>

git commit -am "message"
git push
"""
black = (  10,   10,   10)
white = (255, 255, 255)
blue =  (  0,   0, 255)
green = (  0, 255,   0)
red =   (200,   40,   40)
lightBlue = (103, 173, 255)
lightGreen = (103, 255, 103)
purple = (200, 10, 240)
lightGrey = (205, 205, 205)

#starting variables
displayWidth = 800
displayHeight = 600
screenColor = lightBlue
level = 0

#classes
class Player(object):
    jumping = False
    falling = False
    newJump = True
    jumpHeight = 0
    fallSpeed = 0
    blockedR = False
    blockedL = False
    blockedU = False
    blockedD = False
    def __init__(self, color, locX, locY, width, height):
        self.color = color
        self.width = width
        self.height = height
        self.locX = locX
        self.locY = locY
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.locX, self.locY, self.width, self.height,), 0)
    def movement(self):
        keys = pygame.key.get_pressed()
        #walking
        if keys[pygame.K_RIGHT] and canMove(level, "R", self.locX, self.locY, self.width, self.height) and not self.blockedR:
            self.locX += 0.5
        if keys[pygame.K_LEFT] and canMove(level, "L", self.locX, self.locY, self.width, self.height) and not self.blockedL:
            self.locX -= 0.5
        #jumping
        if keys[pygame.K_UP]:
            if self.newJump:
                self.newJump = False
        else:
            self.newJump = True
        if self.newJump and not self.jumping and not self.falling and canMove(level, "U", self.locX, self.locY, self.width, self.height) and not self.blockedU:
            self.jumping = True
            self.jumpHeight = 0
        if keys[pygame.K_UP] and self.jumping and self.jumpHeight < 140 and canMove(level, "U", self.locX, self.locY, self.width, self.height) and not self.blockedU:
            self.locY -= 1.25
            self.jumpHeight += 1.25
        if self.jumpHeight >= 140:
            self.jumping = False
            self.falling = True
        #falling
        if (upReleased() or not self.jumping or not (canMove(level, "U", self.locX, self.locY, self.width, self.height) and not self.blockedU)) and canMove(level, "D", self.locX, self.locY, self.width, self.height) and not self.blockedD:
            self.locY += 0.01 + self.fallSpeed
            self.fallSpeed += 0.005
            self.jumping = False
            self.falling = True
        if not canMove(level, "D", self.locX, self.locY, self.width, self.height) or self.blockedD:
            self.falling = False
            self.fallSpeed = 0
class Block(object):
    width = 80
    height = 80
    color = lightGrey
    falling = False
    fallSpeed = 0
    def __init__(self, locX, locY):
        self.locX = locX
        self.locY = locY
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.locX, self.locY, self.width, self.height), 0)
    def movement(self):
        #falling
        if canMove(level, "D", self.locX, self.locY, self.width, self.height) and not self.headLand(player.locX, player.locY, player.width, player.height):
            self.locY += 0.01 + self.fallSpeed
            self.fallSpeed += 0.01
            self.falling = True
        else:
            self.fallSpeed = 0
            self.falling = False
        #pushing
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and not self.falling and player.blockedR and canMove(level, "R", self.locX, self.locY, self.width, self.height):
            self.locX += 0.25
            player.locX += 0.25
        if keys[pygame.K_LEFT] and not self.falling and player.blockedL and canMove(level, "L", self.locX, self.locY, self.width, self.height):
            self.locX -= 0.25
            player.locX -= 0.25
    def playerBlock(self, direction, playerLocX, playerLocY, playerWidth, playerHeight):
        if direction == "R":
            if playerLocX + playerWidth == self.locX and self.locY - playerHeight < playerLocY < self.locY + self.height:
                return False
            else:
                return True
        if direction == "L":
            if playerLocX == self.locX + self.width and self.locY - playerHeight < playerLocY < self.locY + self.width:
                return False
            else:
                return True
        if direction == "U":
            if self.locY + (self.height / 2) < playerLocY <= self.locY + self.height and self.locX - playerWidth < playerLocX < self.locX + self.width:
                return False
            else:
                return True
        if direction == "D":
            if self.locY - playerHeight <= playerLocY < self.locY + (self.height / 2) - playerHeight and self.locX - playerWidth < playerLocX < self.locX + self.width:
                return False
            else:
                return True
    def headLand(self, playerLocX, playerLocY, playerWidth, playerHeight):
        if playerLocY <= self.locY + self.height <  playerLocY + (playerHeight / 2) and playerLocX - self.width < self.locX < playerLocX + playerWidth:
            return True
        else:
            return False

#functions
def drawLevel(level):
    screen.fill(screenColor)
    #objects
    player.draw()
    for block in blocks[level]:
        block.draw()
    #level
    if level == 0:
        pygame.draw.rect(screen, black, (300, 500, 200, 20), 0)
    elif level == 1:
        pygame.draw.rect(screen, black, (0, 520, displayWidth, 80), 0) #bottom
        pygame.draw.rect(screen, black, (180, 300, 40, 140), 0) #peninsula
        pygame.draw.rect(screen, black, (0, 380, 80, 140), 0) #starting platform
        pygame.draw.rect(screen, black, (700, 360, 100, 160), 0) #below exit
        pygame.draw.rect(screen, black, (370, 400, 75, 40), 0) #island
        pygame.draw.rect(screen, black, (485, 400, 75, 40), 0) #island adjacent
        pygame.draw.rect(screen, black, (560, 400, 140, 120), 0) #island to exit
        pygame.draw.rect(screen, black, (370, 500, 40, 20), 0) #block stopper
        pygame.draw.rect(screen, black, (0, 0, 520, 300), 0) #top middle/ left
        pygame.draw.rect(screen, black, (520, 0, 300, 200), 0) #top right
        pygame.draw.rect(screen, black, (780, 200, 20, 80), 0) #above exit
        pygame.draw.rect(screen, red, (780, 280, 20, 80), 0) #exit door
        pygame.draw.rect(screen, red, (100, 515, 60, 5), 0) #pressure plate
    pygame.display.update()
def canMove(level, direction, locX, locY, width, height):
    if level == 0:
        if direction == "R":
            if locX >= displayWidth - width or 300 == locX + width  and 500 - height < locY < 520 :
                return False
            else:
                return True
        if direction == "L":
            if locX <= 0 or locX == 500 and 500 - height < locY < 520:
                return False
            else:
                return True
        if direction == "U":
            if locY <= 0 or 510 < locY <= 520 and 300 - width < locX < 500:
                return False
            else:
                return True
        if direction == "D":
            if locY >= displayHeight - height or 500 - height <= locY < 520 - height and 300 - width < locX < 500:
                return False
            else:
                return True
def upReleased():
    keyPressed = pygame.key.get_pressed()
    if keyPressed[pygame.K_UP]:
        return False
    else:
        return True

#set up
player = Player(purple, 0, 340, 20, 40)

blocks0 = [Block(450, 100), Block(300, 100)]
blocks1 = [Block(425, 320)]
blocks = [blocks0, blocks1]

screen = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("LabGame")
drawLevel(level)

#gamegame
while True:

    #quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();
            break

    #block stuff
    for block in blocks[level]:
        checksR = []
        checksL = []
        checksU = []
        checksD = []
        checksR.append(block.playerBlock("R", player.locX, player.locY, player.width, player.height))
        checksL.append(block.playerBlock("L", player.locX, player.locY, player.width, player.height))
        checksU.append(block.playerBlock("U", player.locX, player.locY, player.width, player.height))
        checksD.append(block.playerBlock("D", player.locX, player.locY, player.width, player.height))
    if all(checksR) == True:
        player.blockedR = False
    else:
        player.blockedR = True
    if all(checksL) == True:
        player.blockedL = False
    else:
        player.blockedL = True
    if all(checksU) == True:
        player.blockedU = False
    else:
        player.blockedU = True
    if all(checksD) == True:
        player.blockedD = False
    else:
        player.blockedD = True
        
    for block in blocks[level]:
        block.movement()
    #player stuff
    player.movement()

    drawLevel(level)

    
