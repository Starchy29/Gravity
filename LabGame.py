import pygame
import sys
pygame.init()

"""
ls
git commit -am "message"
git push

git add <filename>
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
    justPushedR = False
    justPushedL = False
    pushCount = 0
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
        if keys[pygame.K_RIGHT] and not self.justPushedR and not self.falling and not playerBlock("R", self.locX, self.locY, self.width, self.height) and canMove(level, "R", self.locX, self.locY, self.width, self.height) and canMove(level, "R", player.locX, player.locY, player.width, player.height):
            self.locX += 0.5
            player.locX += 0.5
            self.justPushedR = True
            self.pushCount = 0
        if self.justPushedR == True and self.pushCount < 1:
            self.pushCount += 1
        else:
            self.justPushedR = False

        if keys[pygame.K_LEFT] and not self.justPushedL and not self.falling and not playerBlock("L", self.locX, self.locY, self.width, self.height) and canMove(level, "L", self.locX, self.locY, self.width, self.height) and canMove(level, "L", player.locX, player.locY, player.width, player.height):
            self.locX -= 0.5
            player.locX -= 0.5
            self.justPushedL = True
            self.pushCount = 0
        if self.justPushedL == True and self.pushCount < 1:
            self.pushCount += 1
        else:
            self.justPushedL = False
    def headLand(self, playerLocX, playerLocY, playerWidth, playerHeight):
        if playerLocY <= self.locY + self.height <  playerLocY + (playerHeight / 2) and playerLocX - self.width < self.locX < playerLocX + playerWidth:
            return True
        else:
            return False
class PlateDoor(object):
    plateWidth = 60
    plateHeight = 5
    locX = 0
    locY = 0
    plateImageX = 0
    plateImageY = 0
    def __init__(self, color, pressDir, plateLocX, plateLocY, doorStartX, doorStartY, doorWidth, doorHeight, doorEndX, doorEndY):
        self.color = color
        self.pressDir = pressDir
        self.plateLocX = plateLocX
        self.plateLocY = plateLocY
        self.doorStartX = doorStartX
        self.doorStartY = doorStartY
        self.width = doorWidth
        self.height = doorHeight
        self.doorEndX = doorEndX
        self.doorEndY = doorEndY
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.locX, self.locY, self.width, self.height), 0) #door
        pygame.draw.rect(screen, self.color, (self.plateImageX, self.plateImageY, self.plateWidth, self.plateHeight), 0) #plate
    def triggerCheck(self, locX, locY, width, height):
        if self.plateLocY - height <= locY <= self.plateLocY + self.plateHeight and self.plateLocX - width < locX < self.plateLocX + self.plateWidth:
            self.locX = self.doorEndX
            self.locY = self.doorEndY
            if self.pressDir == "D":
                self.plateImageY = self.plateLocY + self.plateHeight - 2
                self.plateImageX = self.plateLocX
            if self.pressDir == "U":
                self.plateLocY -= self.plateHeight
                self.plateImageX = self.plateLocX
        else:
            self.plateImageY = self.plateLocY
            self.plateImageX = self.plateLocX
            self.locX = self.doorStartX
            self.locY = self.doorStartY
        
#functions
def drawLevel(level):
    screen.fill(screenColor)
    #objects
    player.draw()
    for x in objects[level]:
        x.draw()
    #level
    if level == 0:
        pygame.draw.rect(screen, black, (300, 500, 200, 20), 0)
    elif level == 1:
        pygame.draw.rect(screen, black, (0, 520, displayWidth, 80), 0) #bottom
        pygame.draw.rect(screen, black, (180, 300, 40, 140), 0) #peninsula
        pygame.draw.rect(screen, black, (0, 360, 80, 160), 0) #starting platform
        pygame.draw.rect(screen, black, (700, 360, 100, 160), 0) #below exit
        pygame.draw.rect(screen, black, (370, 400, 75, 40), 0) #island
        pygame.draw.rect(screen, black, (485, 400, 215, 120), 0) #island to exit
        pygame.draw.rect(screen, black, (370, 500, 115, 20), 0) #block stopper
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
    if level == 1:
        if direction == "R":
            if (locX + width == 180 and locY < 440) or (locX + width == 370 and (400 - height < locY < 440 or 500 - height < locY)) or (locX + width == 485 and 400 - height < int(locY)) or (locX + width == 700 and 360 < locY + height) or (locX + width == 780 and 280 > locY):
                return False
            else:
                return True
        if direction == "L":
            if (locX == 520 and 300 > locY) or (locX == 445 and 400 - height < int(locY) < 440) or (locX == 220 and locY < 440) or (locX == 80 and locY + height > 360):
                return False
            else:
                return True
        if direction == "U":
            if (420 < locY <= 440 and (180 - width < locX < 220 or 370 - width < locX < 445)) or (locY <= 300 and locX < 520) or (locY <= 280 and locX + width > 780) or (locY <= 200 and 520 - width < locX):
                return False
            else:
                return True
        if direction == "D":
            if (locY + height >= 360 and (locX + width > 700 or locX < 80)) or (420 >= locY + height > 400 and (locX + width > 485 or 370 - width < locX < 445)) or (locY + height >= 500 and 370 - width < locX) or (locY + height >= 520 ):
                return False
            else:
                return True

def playerBlock(direction, locX, locY, width, height):
        if direction == "R":
            if player.locX + player.width == locX and locY - player.height < player.locY < locY + height:
                return False
            else:
                return True
        if direction == "L":
            if player.locX == locX + width and locY - player.height < player.locY < locY + width:
                return False
            else:
                return True
        if direction == "U":
            if locY + (height / 2) < player.locY <= locY + height and locX - player.width < player.locX < locX + width:
                return False
            else:
                return True
        if direction == "D":
            if locY - player.height <= player.locY < locY + (height / 2) - player.height and locX - player.width < player.locX < locX + width:
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
player = Player(purple, 0, 320, 20, 40)

objects0 = [Block(400, 300), PlateDoor(red, "D", 320, 495, 230, 460, 20, 80, 230, 520)]
objects1 = [Block(425, 320)]
objects = [objects0, objects1]

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

    keys = pygame.key.get_pressed()
    
    #player blocked checks
    checksR = []
    checksL = []
    checksU = []
    checksD = []
    for x in objects[level]:
        checksR.append(playerBlock("R", x.locX, x.locY, x.width, x.height))
        checksL.append(playerBlock("L", x.locX, x.locY, x.width, x.height))
        checksU.append(playerBlock("U", x.locX, x.locY, x.width, x.height))
        checksD.append(playerBlock("D", x.locX, x.locY, x.width, x.height))
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
 
    for x in objects[level]:
        if isinstance(x, Block):
            x.movement()
    for plate in objects[level]:
        if isinstance(plate, PlateDoor):
            for block in objects[level]:
                if isinstance(block, Block):
                    plate.triggerCheck(block.locX, block.locY, block.width, block.height)
            plate.triggerCheck(player.locX, player.locY, player.width, player.height)

    player.movement()
    
    drawLevel(level)

    
