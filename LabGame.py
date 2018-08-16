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
lightGreen = (130, 255, 130)
purple = (160, 10, 200)
lightGrey = (205, 205, 205)

#starting variables
displayWidth = 800
displayHeight = 600
screenColor = lightBlue
gravity = "D"
level = 4

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
        #gravity stuff
        if keys[pygame.K_UP]:
            self.newJump = False
        else:
            self.newJump = True
        if gravity == "D":
            #jumping
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
        elif gravity == "U":
            #jumping
            if self.newJump and not self.jumping and not self.falling and canMove(level, "D", self.locX, self.locY, self.width, self.height) and not self.blockedD:
                self.jumping = True
                self.jumpHeight = 0
            if keys[pygame.K_UP] and self.jumping and self.jumpHeight < 140 and canMove(level, "D", self.locX, self.locY, self.width, self.height) and not self.blockedD:
                self.locY += 1.25
                self.jumpHeight += 1.25
            if self.jumpHeight >= 140:
                self.jumping = False
                self.falling = True
            #falling
            if (upReleased() or not self.jumping or not (canMove(level, "D", self.locX, self.locY, self.width, self.height) and not self.blockedD)) and canMove(level, "U", self.locX, self.locY, self.width, self.height) and not self.blockedU:
                self.locY -= (0.01 + self.fallSpeed)
                self.fallSpeed += 0.005
                self.jumping = False
                self.falling = True
            if not canMove(level, "U", self.locX, self.locY, self.width, self.height) or self.blockedU:
                self.falling = False
                self.fallSpeed = 0
class Block(object):
    width = 80
    height = 80
    falling = False
    justPushedR = False
    justPushedL = False
    pushCount = 0
    fallSpeed = 0
    blockedR = False
    blockedL = False
    blockedU = False
    blockedD = False
    def __init__(self, locX, locY):
        self.locX = locX
        self.locY = locY
    def draw(self):
        pygame.draw.rect(screen, white, (self.locX, self.locY, self.width, self.height), 0)
        pygame.draw.rect(screen, lightGrey, (self.locX + 5, self.locY + 5, self.width - 10, self.height - 10), 0)
        pygame.draw.rect(screen, white, (self.locX + 20, self.locY + 20, self.width - 40, self.height - 40), 2)
    def movement(self):
        #falling
        if gravity == "D":
            if canMove(level, "D", self.locX, self.locY, self.width, self.height) and not self.blockedD and not self.headLand(player.locX, player.locY, player.width, player.height):
                self.locY += 0.01 + self.fallSpeed
                self.fallSpeed += 0.01
                self.falling = True
            else:
                self.fallSpeed = 0
                self.falling = False
        elif gravity == "U":
            if canMove(level, "U", self.locX, self.locY, self.width, self.height) and not self.blockedU and not self.headLand(player.locX, player.locY, player.width, player.height):
                self.locY -= (0.01 + self.fallSpeed)
                self.fallSpeed += 0.01
                self.falling = True
            else:
                self.fallSpeed = 0
                self.falling = False
        #pushing
            #player
        if keys[pygame.K_RIGHT] and not playerBlock("R", self.locX, self.locY, self.width, self.height) and canMove(level, "R", player.locX, player.locY, player.width, player.height) and not self.justPushedR and not self.falling and not self.blockedR and canMove(level, "R", self.locX, self.locY, self.width, self.height):
            self.locX += 0.5
            player.locX += 0.5
            self.justPushedR = True
            self.pushCount = 0
        if self.justPushedR == True and self.pushCount < 1:
            self.pushCount += 1
        else:
            self.justPushedR = False
        if keys[pygame.K_LEFT] and canMove(level, "L", player.locX, player.locY, player.width, player.height) and not playerBlock("L", self.locX, self.locY, self.width, self.height) and not self.justPushedL and not self.falling and not self.blockedL and canMove(level, "L", self.locX, self.locY, self.width, self.height) and canMove(level, "L", player.locX, player.locY, player.width, player.height):
            self.locX -= 0.5
            player.locX -= 0.5
            self.justPushedL = True
            self.pushCount = 0
        if self.justPushedL == True and self.pushCount < 1:
            self.pushCount += 1
        else:
            self.justPushedL = False
            #door
        for door in objects[level]:
            if isinstance(door, PlateDoor):
                if door.doorBlock("R", self.locX, self.locY, self.width, self.height) and canMove(level, "R", self.locX, self.locY, self.width, self.height):
                    self.locX += 1
                if door.doorBlock("L", self.locX, self.locY, self.width, self.height) and canMove(level, "L", self.locX, self.locY, self.width, self.height):
                    self.locX -= 1
                if door.doorBlock("U", self.locX, self.locY, self.width, self.height) and canMove(level, "U", self.locX, self.locY, self.width, self.height):
                    self.locY -= 1
                if door.doorBlock("D", self.locX, self.locY, self.width, self.height) and canMove(level, "D", self.locX, self.locY, self.width, self.height):
                    self.locY += 1
    def blockBlock(self, direction, locX, locY, width, height):
        if not (self.locX == locX and self.locY == locY):
            if direction == "R" and (self.locX + self.width == locX and locY - self.height < self.locY < locY + height):
                self.blockedR = True
            if direction == "L" and (self.locX == locX + width and locY - self.height < self.locY < locY + height):
                self.blockedL = True
            if direction == "U" and (locY + (height / 2) < self.locY <= locY + height and locX - self.width < self.locX < locX + width):
                self.blockedU = True
            if direction == "D" and (locY - self.height <= self.locY < locY + (height / 2) - self.height and locX - self.width < self.locX < locX + width):
                self.blockedD = True
                
    def headLand(self, playerLocX, playerLocY, playerWidth, playerHeight):
        if gravity == "D":
            if playerLocY <= self.locY + self.height <  playerLocY + (playerHeight / 2) and playerLocX - self.width < self.locX < playerLocX + playerWidth:
                return True
            else:
                return False
        elif gravity == "U":
            if playerLocY + playerHeight >= self.locY >  playerLocY + (playerHeight / 2) and playerLocX - self.width < self.locX < playerLocX + playerWidth:
                return True
            else:
                return False
        
class PlateDoor(object):
    plateWidth = 60
    plateHeight = 5
    triggered = False
    plateImageX = 0
    plateImageY = 0
    blockedR = False
    blockedL = False
    blockedU = False
    blockedD = False
    playBlockedR = False
    playBlockedL = False
    playBlockedU = False
    playBlockedD = False
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

        self.locX = doorStartX
        self.locY = doorStartY
    def draw(self):
        pygame.draw.rect(screen, black, (self.locX, self.locY, self.width, self.height), 0) #door
        pygame.draw.rect(screen, self.color, (self.locX + 5, self.locY + 5, self.width - 10, self.height - 10), 0) #door
        pygame.draw.rect(screen, self.color, (self.plateImageX, self.plateImageY, self.plateWidth, self.plateHeight), 0) #plate
    def triggerCheck(self, locX, locY, width, height):
        if self.plateLocY - height <= locY <= self.plateLocY + self.plateHeight and self.plateLocX - width < locX < self.plateLocX + self.plateWidth:
            self.triggered = True
    def doorBlock(self, direction, locX, locY, width, height):
        if direction == "R":
            if (self.locX + self.width == int(locX) and locY - self.height < self.locY < locY + height):
                if locX == player.locX and locY == player.locY and width == player.width and height == player.height:
                    self.playBlockedR = True
                else:
                    self.blockedR = True
                return True
            else:
                return False
        if direction == "L":
            if (self.locX == int(locX) + width and locY - self.height < self.locY < locY + height):
                if locX == player.locX and locY == player.locY and width == player.width and height == player.height:
                    self.playBlockedL = True
                else:
                    self.blockedL = True
                return True
            else:
                return False
        if direction == "U":
            if (locY + (height / 2) < self.locY <= locY + height and locX - self.width < self.locX < locX + width):
                if locX == player.locX and locY == player.locY and width == player.width and height == player.height:
                    self.playBlockedU = True
                else:
                    self.blockedU = True
                return True
            else:
                return False
        if direction == "D":
            if (locY - self.height <= self.locY < locY + (height / 2) - self.height and locX - self.width < self.locX < locX + width):
                if locX == player.locX and locY == player.locY and width == player.width and height == player.height:
                    self.playBlockedD = True
                else:
                    self.blockedD = True
                return True
            else:
                return False
    def triggerWork(self):
        self.blockedR = False
        self.blockedL = False
        self.blockedU = False
        self.blockedD = False
        self.playBlockedR = False
        self.playBlockedL = False
        self.playBlockedU = False
        self.playBlockedD = False
        for x in objects[level]:
            if isinstance(x, Block):
                self.doorBlock("R", x.locX, x.locY, x.width, x.height)
                self.doorBlock("L", x.locX, x.locY, x.width, x.height)
                self.doorBlock("U", x.locX, x.locY, x.width, x.height)
                self.doorBlock("D", x.locX, x.locY, x.width, x.height)
        self.doorBlock("R", player.locX, player.locY, player.width, player.height)
        self.doorBlock("L", player.locX, player.locY, player.width, player.height)
        self.doorBlock("U", player.locX, player.locY, player.width, player.height)
        self.doorBlock("D", player.locX, player.locY, player.width, player.height)
        if self.triggered:
            if self.locY > self.doorEndY and not self.blockedU and not self.playBlockedU:
                self.locY -= 1
            if self.locY < self.doorEndY and not self.blockedD and not self.playBlockedD:
                self.locY += 1
            if self.locX > self.doorEndX and not self.blockedL and not self.playBlockedL:
                self.locX -= 1
            if self.locX < self.doorEndX and not self.blockedR and not self.playBlockedR:
                self.locX += 1
            if self.pressDir == "D":
                self.plateImageY = self.plateLocY + self.plateHeight - 2
                self.plateImageX = self.plateLocX
            if self.pressDir == "U":
                self.plateImageY = self.plateLocY - self.plateHeight + 2
                self.plateImageX = self.plateLocX
        else:
            if self.locY > self.doorStartY and not self.blockedU:
                self.locY -= 1
            if self.locY < self.doorStartY and not self.blockedD:
                self.locY += 1
            if self.locX > self.doorStartX and not self.blockedL:
                self.locX -= 1
            if self.locX < self.doorStartX and not self.blockedR:
                self.locX += 1
            self.plateImageY = self.plateLocY
            self.plateImageX = self.plateLocX

gravSwapColor = lightGreen
class GravSwap(object):
    color = lightGreen
    newPress = False
    stillPress = True
    def __init__(self, rotation, locX, locY):
        self.rotation = rotation
        self.locX = locX
        self.locY = locY
    def draw(self):
        if self.rotation == "V":
            pygame.draw.line(screen, black, (self.locX, self.locY - 30), (self.locX, self.locY + 30), 8)
        elif self.rotation == "H":
            pygame.draw.line(screen, black, (self.locX - 30, self.locY), (self.locX + 30, self.locY), 8)
        pygame.draw.circle(screen, black, (self.locX, self.locY), 20, 0)
        pygame.draw.circle(screen, gravSwapColor, (self.locX, self.locY), 16, 0)
        pygame.draw.circle(screen, black, (self.locX, self.locY), 5, 0)
    def pressCheck(self):
        if keys[pygame.K_SPACE]:
            if self.stillPress:
                self.stillPress = False
                self.newPress = True
            else:
                self.newPress = False
        else:
            self.stillPress = True
            self.newPress = False
        if self.newPress and (self.locX - 20 - player.width <= player.locX <= self.locX + 20 and self.locY - 20 - player.height <= player.locY <= self.locY + 20):
            global gravity
            global screenColor
            global gravSwapColor
            if gravity == "D":
                gravity = "U"
                screenColor = lightGreen
                gravSwapColor = lightBlue
            elif gravity == "U":
                gravity = "D"
                screenColor = lightBlue
                gravSwapColor = lightGreen
            player.fallSpeed = 0
            for x in objects[level]:
                if isinstance(x, Block):
                    x.fallSpeed = 0

#functions
def drawLevel(level):
    screen.fill(screenColor)
    #objects
    for x in objects[level]:
        if isinstance(x, GravSwap):
            x.draw()
    player.draw()
    for x in objects[level]:
        if isinstance(x, (Block, PlateDoor)):
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
    elif level == 2:
        pygame.draw.rect(screen, black, (0, 520, displayWidth, 80), 0) #bottom
        pygame.draw.rect(screen, black, (0, 0, 40, 440), 0) #left wall
        pygame.draw.rect(screen, black, (40, 0, 760, 80), 0) #ceiling
        pygame.draw.rect(screen, black, (200, 240, 60, 280), 0) #peninsula 1
        pygame.draw.rect(screen, black, (220, 80, 140, 40), 0) #ceiling jump
        pygame.draw.rect(screen, black, (100, 240, 100, 40), 0) #catch block
        pygame.draw.rect(screen, black, (300, 240, 60, 230), 0) #peninsula 2
        pygame.draw.rect(screen, black, (300, 120, 30, 120), 0) #peninsula 2 small peice
        pygame.draw.rect(screen, black, (760, 80, 40, 320), 0) #right wall
        pygame.draw.rect(screen, black, (720, 340, 40, 40), 0) #step to exit
        pygame.draw.rect(screen, black, (510, 280, 100, 40), 0) #island
        pygame.draw.rect(screen, black, (720, 80, 40, 40), 0) #block stopper top right
        pygame.draw.rect(screen, black, (720, 480, 80, 40), 0) #block stopper bottom right
    elif level == 3:
        pygame.draw.rect(screen, black, (0, 520, displayWidth, 80), 0) #bottom
        pygame.draw.rect(screen, black, (0, 0, displayWidth, 180), 0) #ceiling
        pygame.draw.rect(screen, black, (0, 180, 40, 220), 0) #left wall
        pygame.draw.rect(screen, black, (0, 480, 80, 40), 0) #block stopper bottom left
        pygame.draw.rect(screen, black, (40, 180, 40, 40), 0) #block stopper top left
        pygame.draw.rect(screen, black, (470, 180, 30, 40), 0) #block stopper top right
        pygame.draw.rect(screen, black, (720, 480, 40, 40), 0) #block stopper bottom right
        pygame.draw.rect(screen, black, (470, 320, 30, 100), 0) #peninsula left half
        pygame.draw.rect(screen, black, (500, 180, 30, 240), 0) #peninsula right half
        pygame.draw.rect(screen, black, (215, 320, 100, 40), 0) #island
        pygame.draw.rect(screen, black, (760, 320, 40, 200), 0) #below exit
    elif level == 4:
        pygame.draw.rect(screen, black, (0, 520, displayWidth, 80), 0) #bottom
        pygame.draw.rect(screen, black, (0, 0, 760, 80), 0) #ceiling
        pygame.draw.rect(screen, black, (760, 0, 40, 400), 0) #right wall
        pygame.draw.rect(screen, black, (0, 80, 40, 320), 0) #left wall
        pygame.draw.rect(screen, black, (520, 360, 240, 40), 0) #peninsula
        pygame.draw.rect(screen, black, (360, 200, 320, 40), 0) #island
        pygame.draw.rect(screen, black, (320, 200, 40, 200), 0) #stair last
        pygame.draw.rect(screen, black, (280, 280, 40, 120), 0) #stair middle
        pygame.draw.rect(screen, black, (240, 320, 40, 80), 0) #stair first
        pygame.draw.rect(screen, black, (720, 300, 40, 60), 0) #block stopper bottom right
        pygame.draw.rect(screen, black, (720, 80, 40, 40), 0) #block stopper top right
        pygame.draw.rect(screen, black, (0, 480, 80, 40), 0) #block stopper bottom left
        pygame.draw.rect(screen, black, (40, 80, 40, 40), 0) #block stopper top left
        pygame.draw.rect(screen, black, (640, 140, 40, 60), 0) #block stopper top middle
        pygame.draw.rect(screen, black, (440, 240, 40, 40), 0) #jumping block
        pygame.draw.rect(screen, black, (360, 240, 80, 200), 0) #block jump preventer
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
    elif level == 1:
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
    elif level == 2:
        if direction == "R":
            if (locX + width == 100 and 240 - height < locY < 280) or (locX + width == 200 and 280 - height < locY) or (locX + width == 220 and 80 - height < locY < 120) or (locX + width == 300 and locY < 470) or (locX + width == 520 and 280 - height < locY < 320) or (locX + width == 720 and (340 - height < locY < 380 or locY < 120 or locY + height > 480)) or (locX + width == 760 and  locY < 400):
                return False
            else:
                return True
        if direction == "L":
            if (locX == 630 and 280 - height < locY < 320) or (locX == 360 and (220 - height < locY < 470 or locY < 120)) or (locX == 330 and 120 - height < locY < 240) or (locX == 260 and 240 - height < locY) or (locX == 40 and locY < 440):
                return False
            else:
                return True
        if direction == "U":
            if (430 < locY <= 470 and 300 - width < locX < 360) or (locY <= 440 and locX < 40) or (360 < locY <= 380 and locX > 720 - width) or (300 < locY <= 320 and 510 - width < locX < 610) or (260 < locY <= 280 and 100 - width < locX < 200) or (100 < locY <= 120 and (220 - width < locX < 360 or locX > 720 - width)) or (locY <= 80):
                return False
            else:
                return True
        if direction == "D":
            if (240 <= locY + height < 260 and (100 - width < locX < 260 or 330 - width < locX < 360)) or (280 <= locY + height < 300 and 510 - width < locX < 610) or (340 <= locY + height < 360 and locX > 720 - width) or (480 <= locY + height < 500 and locX + width > 720) or (locY + height >= 520):
                return False
            else:
                return True
    elif level == 3:
        if direction == "R":
            if (locX + width == 215 and 320 - height < locY < 360) or (locX + width == 470 and (320 - height < locY < 420 or locY < 220)) or (locX + width == 500 and locY < 320) or (locX + width == 720 and 480 - height < locY) or (locX + width == 760 and 320 - height < locY ):
                return False
            else:
                return True
        if direction == "L":
            if (locX == 530 and locY < 420) or (locX == 315 and 320 - height < locY < 360) or (locX == 80 and (480 - height < locY or locY < 220)) or (locX == 40 and locY < 400):
                return False
            else:
                return True
        if direction == "U":
            if (locY <= 400 and locX < 40) or (340 < locY <= 360 and 215 - width < locX < 315) or (200 < locY <= 220 and (470 - width < locX < 500 or locX < 80)) or (locY <= 180):
                return False
            else:
                return True
        if direction == "D":
            if (340 > locY + height >= 320 and (215 - width < locX < 315 or 470 - width < locX < 500)) or (340 > locY + height >= 320 and 760 - width < locX) or (500 > locY + height >= 480 and (720 - width < locX or locX < 80)) or (locY + height >= 520):
                return False
            else:
                return True
    elif level == 4:
        if direction == "R":
            if (locX + width == 240 and 320 - height < locY < 400) or (locX + width == 280 and 280 - height < locY < 320) or (locX + width == 320 and 200 - height < locY < 300) or (locX + width == 360 and 400 - height < locY < 440) or (locX + width == 400 and 400 - height < locY < 440) or (locX + width == 520 and 360 - height < locY < 400) or (locX + width == 640 and 140 - height < locY < 180) or (locX + width == 720 and (300 - height < locY < 360 or locY < 120)) or (locX + width == 760 and locY < 320):
                return False
            else:
                return True
        if direction == "L":
            if (locX == 680 and 140 - height < locY < 240) or (locX == 480 and 240 - height < locY < 280) or (locX == 440 and 240 - height < locY < 440) or (locX == 80 and (480 - height < locY or locY < 120)) or (locX == 40 and locY < 400):
                return False
            else:
                return True
        if direction == "U":
            if (420 < locY <= 440 and 360 - width < locX < 440) or (380 < locY <= 400 and (240 - width < locX < 400 or locX < 40 or locX > 520 - width)) or (240 < locY <= 280 and 440 - width < locX < 480) or (260 < locY <= 280 and 400 - width < locX < 440) or (220 < locY <= 240 and 400 - width < locX < 680) or (100 < locY <= 120 and (720 - width < locX or locX < 80)) or (locY <= 80):
                return False
            else:
                return True
        if direction == "D":
            if (160 > locY + height >= 140 and 640 - width < locX < 680) or (220 > locY + height >= 200 and 320 - width < locX < 680) or (300 > locY + height >= 280 and 280 - width < locX < 320) or (340 > locY + height >= 320 and 240 - width < locX < 280) or (320 > locY + height >= 300 and 720 - width < locX) or (380 > locY + height >= 360 and 520 - width < locX) or (500 > locY + height >= 480 and locX < 80) or (locY + height >= 520):
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
            if player.locX == locX + width and locY - player.height < player.locY < locY + height:
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

def winCheck():
    if player.locX < 0:
        player.locX += 0.5
    if player.locX > displayWidth + 2:
        global level
        level += 1
        global gravity
        global screenColor
        gravity = "D"
        screencolor = lightBlue
        player.locX = -60
        if level == 2:
            player.locY = 480
        elif level == 3 or level == 4:
            player.locY = 440

        
def upReleased():
    keyPressed = pygame.key.get_pressed()
    if keyPressed[pygame.K_UP]:
        return False
    else:
        return True

#set up
player = Player(purple, -60, 320, 20, 40)
if level == 2:
    player.locY = 480
if level == 3 or level == 4:
    player.locY = 440

objects0 = [Block(400, 300), Block(400, 200), GravSwap("V", 400, 570), PlateDoor(red, "D", 390, 495, 460, 520, 40, 80, 260, 520)]
objects1 = [Block(425, 320), PlateDoor(red, "D", 100, 515, 780, 280, 20, 80, 780, 200)]
objects2 = [Block(520, 440), GravSwap("V", 150, 490), GravSwap("V", 435, 490), GravSwap("V", 435, 110), GravSwap("V", 260, 150), PlateDoor(red, "U", 530, 80, 760, 400, 40, 80, 760, 320)]
objects3 = [Block(225, 440), Block(560, 440), GravSwap("V", 265, 390), GravSwap("V", 130, 210), PlateDoor(red, "D", 100, 515, 760, 180, 40, 140, 760, 40), PlateDoor(blue, "D", 235, 315, 470, 420, 60, 100, 470, 320)]
objects4 = [Block(320, 120), Block(110, 440), GravSwap("H", 730, 220), GravSwap("V", 430, 110), GravSwap("H", 70, 370), PlateDoor(red, "U", 120, 80, 520, 400, 40, 120, 320, 400), PlateDoor(blue, "D", 370, 515, 520, 80, 40, 120, 520, 240)]
objects5 = []
objects = [objects0, objects1, objects2, objects3, objects4, objects5]

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
    
    #player movement checks
    checksR = []
    checksL = []
    checksU = []
    checksD = []
    for x in objects[level]:
        if isinstance(x, (Block, PlateDoor)):
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

    #Grav swap stuff
    for x in objects[level]:
        if isinstance(x, GravSwap):
            x.pressCheck()
                
    #block stuff
    for block in objects[level]:
        if isinstance(block, Block):
            block.blockedR = False
            block.blockedL = False
            block.blockedU = False
            block.blockedD = False
            for obj in objects[level]:
                if isinstance(obj, (Block, PlateDoor)):
                    block.blockBlock("R", obj.locX, obj.locY, obj.width, obj.height)
                    block.blockBlock("L", obj.locX, obj.locY, obj.width, obj.height)
                    block.blockBlock("U", obj.locX, obj.locY, obj.width, obj.height)
                    block.blockBlock("D", obj.locX, obj.locY, obj.width, obj.height)
            block.movement()

    #plate stuff
    for plate in objects[level]:
        if isinstance(plate, PlateDoor):
            plate.triggered = False
            for block in objects[level]:
                if isinstance(block, Block):
                    plate.triggerCheck(block.locX, block.locY, block.width, block.height)
            plate.triggerCheck(player.locX, player.locY, player.width, player.height)
            plate.triggerWork()

    #player stuff
    player.movement()
    winCheck()
    
    drawLevel(level)

    
