import pygame
import sys
import math
pygame.init()

"""
ls
git commit -am "message"
git push

git add <filename>
"""
black = (  10,   10,   10)
white = (255, 255, 255)
blue = (  0,   0, 255)
green = (  0, 255,   0)
red = (200,   40,   40)
lightBlue = (103, 173, 255)
lightPurple = (255, 170, 205)
lightGreen = (130, 255, 130)
lightRed = (230,   60,   60)
purple = (180, 30, 230)
playerColor = (160, 10, 200)
lightGrey = (205, 205, 205)
orange = (255, 180, 40)

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

            #treadmill pushing
            for x in objects[level]:
                if isinstance(x, Treadmill):
                    if not playerBlock("D", x.locX, x.locY, x.width, x.height) and x.spinCount:
                        if x.rotation == "clock":
                            self.locX += 0.5
                        if x.rotation == "counter":
                            self.locX -= 0.5
                            
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
            #treadmill pushing
            for x in objects[level]:
                if isinstance(x, Treadmill):
                    if not playerBlock("U", x.locX, x.locY, x.width, x.height) and x.spinCount:
                        if x.rotation == "clock":
                            self.locX -= 0.5
                        if x.rotation == "counter":
                            self.locX += 0.5

        for wall in walls[level]:
                if wall.locY + wall.height - 20 < self.locY < wall.locY + wall.height and wall.locX - self.width < self.locX < wall.locX + wall.width:
                    self.locY = wall.locY + wall.height
                if wall.locY + 20 > self.locY + self.height > wall.locY and wall.locX - self.width < self.locX < wall.locX + wall.width:
                    self.locY = wall.locY - self.height

class Wall(object):
    def __init__(self, locX, locY, width, height):
        self.width = width
        self.height = height
        self.locX = locX
        self.locY = locY
        
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

            for x in objects[level]:
                if isinstance(x, Treadmill):
                    if not self.blockBlock("D", x.locX, x.locY, x.width, x.height) and x.spinCount:
                        if x.rotation == "clock":
                            self.locX -= 0.5
                        if x.rotation == "counter":
                            self.locX += 0.5
        elif gravity == "U":
            if canMove(level, "U", self.locX, self.locY, self.width, self.height) and not self.blockedU and not self.headLand(player.locX, player.locY, player.width, player.height):
                self.locY -= (0.01 + self.fallSpeed)
                self.fallSpeed += 0.01
                self.falling = True
            else:
                self.fallSpeed = 0
                self.falling = False
        for wall in walls[level]:
            if wall.locY + wall.height - 20 < self.locY < wall.locY + wall.height and wall.locX - self.width < self.locX < wall.locX + wall.width:
                self.locY = wall.locY + wall.height
            if wall.locY + 20 > self.locY + self.height > wall.locY and wall.locX - self.width < self.locX < wall.locX + wall.width:
                self.locY = wall.locY - self.height
            #treadmill pushing
            for x in objects[level]:
                if isinstance(x, Treadmill):
                    if not self.blockBlock("U", x.locX, x.locY, x.width, x.height) and x.spinCount:
                        if x.rotation == "clock":
                            self.locX += 0.5
                        if x.rotation == "counter":
                            self.locX -= 0.5
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
            if direction == "R":
                if (self.locX + self.width == locX and locY - self.height < self.locY < locY + height):
                    self.blockedR = True
                    return True
                else:
                    return False
            if direction == "L":
                if (self.locX == locX + width and locY - self.height < self.locY < locY + height):
                    self.blockedL = True
                    return True
                else:
                    return False
            if direction == "U":
                if (locY + (height / 2) < self.locY <= locY + height and locX - self.width < self.locX < locX + width):
                    self.blockedU = True
                    return True
                else:
                    return False
            if direction == "D":
                if (locY - self.height <= self.locY < locY + (height / 2) - self.height and locX - self.width < self.locX < locX + width):
                    self.blockedD = True
                    return True
                else:
                    return False
                
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

class Treadmill(object):
    height = 40
    spinState = 20
    cooldown = 0
    lineX1 = 0
    lineX2 = 0
    angle1 = 0
    angle2 = 0
    spinCount = False
    def __init__(self, rotation, locX, locY, width):
        self.rotation = rotation
        self.locX = locX
        self.locY = locY
        self.width = width
        self.numberLines = int((width - 40) / 20)
    def draw(self):
        pygame.draw.rect(screen, black, (self.locX + 20, self.locY, self.width - 40, 40), 0)
        pygame.draw.circle(screen, black, (self.locX + 20, self.locY + 20), 20, 0)
        pygame.draw.circle(screen, black, (self.locX + self.width - 20, self.locY + 20), 20, 0)
        

        if self.rotation == "clock":
            pygame.draw.rect(screen, lightRed, (self.locX + 20, self.locY + 10, self.width - 40, self.height - 20), 0)
            pygame.draw.circle(screen, lightRed, (self.locX + 20, self.locY + 20), 10, 0)
            pygame.draw.circle(screen, lightRed, (self.locX + self.width - 20, self.locY + 20), 10, 0)
            
            self.lineX1 = self.locX + self.spinState
            self.lineX2 = self.locX + self.width - self.spinState
            for x in range(self.numberLines):
                pygame.draw.line(screen, orange, (self.lineX1, self.locY), (self.lineX1, self.locY + 10), 2)
                self.lineX1 += 20
                pygame.draw.line(screen, orange, (self.lineX2, self.locY + 30), (self.lineX2, self.locY + 40), 2)
                self.lineX2 -= 20

            self.angle1 = math.pi + (self.spinState * -math.pi / 40)
            self.angle2 = self.angle1 - math.pi / 2
            pygame.draw.line(screen, orange, (self.locX + self.width - 20 + (10 * math.cos(self.angle1)), self.locY + 20 - (10 * math.sin(self.angle1))), (self.locX + self.width - 20 + (20 * math.cos(self.angle1)), self.locY + 20 - (20 * math.sin(self.angle1))), 2)
            pygame.draw.line(screen, orange, (self.locX + self.width - 20 + (10 * math.cos(self.angle2)), self.locY + 20 - (10 * math.sin(self.angle2))), (self.locX + self.width - 20 + (20 * math.cos(self.angle2)), self.locY + 20 - (20 * math.sin(self.angle2))), 2)
            pygame.draw.line(screen, orange, (self.locX + 20 - (10 * math.cos(self.angle1)), self.locY + 20 + (10 * math.sin(self.angle1))), (self.locX + 20 - (20 * math.cos(self.angle1)), self.locY + 20 + (20 * math.sin(self.angle1))), 2)
            pygame.draw.line(screen, orange, (self.locX + 20 - (10 * math.cos(self.angle2)), self.locY + 20 + (10 * math.sin(self.angle2))), (self.locX + 20 - (20 * math.cos(self.angle2)), self.locY + 20 + (20 * math.sin(self.angle2))), 2)
        if self.rotation == "counter":
            pygame.draw.rect(screen, purple, (self.locX + 20, self.locY + 10, self.width - 40, self.height - 20), 0)
            pygame.draw.circle(screen, purple, (self.locX + 20, self.locY + 20), 10, 0)
            pygame.draw.circle(screen, purple, (self.locX + self.width - 20, self.locY + 20), 10, 0)

            self.lineX1 = self.locX + self.width - self.spinState
            self.lineX2 = self.locX + self.spinState
            for x in range(self.numberLines):
                pygame.draw.line(screen, lightPurple, (self.lineX1, self.locY), (self.lineX1, self.locY + 10), 2)
                self.lineX1 -= 20
                pygame.draw.line(screen, lightPurple, (self.lineX2, self.locY + 30), (self.lineX2, self.locY + 40), 2)
                self.lineX2 += 20

            self.angle1 = -math.pi + (self.spinState * math.pi / 40)
            self.angle2 = self.angle1 + math.pi / 2
            pygame.draw.line(screen, lightPurple, (self.locX + self.width - 20 + (10 * math.cos(self.angle1)), self.locY + 20 - (10 * math.sin(self.angle1))), (self.locX + self.width - 20 + (20 * math.cos(self.angle1)), self.locY + 20 - (20 * math.sin(self.angle1))), 2)
            pygame.draw.line(screen, lightPurple, (self.locX + self.width - 20 + (10 * math.cos(self.angle2)), self.locY + 20 - (10 * math.sin(self.angle2))), (self.locX + self.width - 20 + (20 * math.cos(self.angle2)), self.locY + 20 - (20 * math.sin(self.angle2))), 2)
            pygame.draw.line(screen, lightPurple, (self.locX + 20 - (10 * math.cos(self.angle1)), self.locY + 20 + (10 * math.sin(self.angle1))), (self.locX + 20 - (20 * math.cos(self.angle1)), self.locY + 20 + (20 * math.sin(self.angle1))), 2)
            pygame.draw.line(screen, lightPurple, (self.locX + 20 - (10 * math.cos(self.angle2)), self.locY + 20 + (10 * math.sin(self.angle2))), (self.locX + 20 - (20 * math.cos(self.angle2)), self.locY + 20 + (20 * math.sin(self.angle2))), 2)
    def spin(self):
        self.cooldown += 1
        if self.cooldown == 10:
            if self.spinState == 40: 
                self.spinState = 20
            else:
                self.spinState += 1
            self.cooldown = 0

        self.spinCount = not self.spinCount

#functions
def drawLevel(level):
    screen.fill(screenColor)
    for x in objects[level]:
        if isinstance(x, GravSwap):
            x.draw()
    player.draw()
    for x in objects[level]:
        if isinstance(x, (Block, PlateDoor, Treadmill)):
            x.draw()
    for x in walls[level]:
        pygame.draw.rect(screen, black, (x.locX, x.locY, x.width, x.height), 0)
    pygame.display.update()
    
def canMove(level, direction, locX, locY, width, height):
        if direction == "R":
            checksR = []
            for wall in walls[level]:
                if locX + width == wall.locX and wall.locY - height < int(locY) < wall.locY + wall.height:
                    checksR.append(False)
                else:
                    checksR.append(True)
            if all(checksR) == True:
                return True
            else:
                return False
        if direction == "L":
            checksL = []
            for wall in walls[level]:
                if locX == wall.locX + wall.width and wall.locY - height < int(locY) < wall.locY + wall.height:
                    checksL.append(False)
                else:
                    checksL.append(True)
            if all(checksL) == True:
                return True
            else:
                return False
        if direction == "U":
            checksU = []
            for wall in walls[level]:
                if wall.locY + wall.height - 20 < locY <= wall.locY + wall.height and wall.locX - width < locX < wall.locX + wall.width:
                    checksU.append(False)
                else:
                    checksU.append(True)
            if all(checksU) == True:
                return True
            else:
                return False
        if direction == "D":
            checksD = []
            for wall in walls[level]:
                if (wall.locY + 20 > locY + height >= wall.locY and wall.locX - width < locX < wall.locX + wall.width) or (locX < 0 or locX > 800):
                    checksD.append(False)
                else:
                    checksD.append(True)
            if all(checksD) == True:
                return True
            else:
                return False
        

            
def playerBlock(direction, locX, locY, width, height):
        if direction == "R":
            if player.locX + player.width == locX and locY - player.height < int(player.locY) < locY + height:
                return False
            else:
                return True
        if direction == "L":
            if player.locX == locX + width and locY - player.height < int(player.locY) < locY + height:
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
        global gravity
        global screenColor
        global gravSwapColor
        level += 1
        gravity = "D"
        screenColor = lightBlue
        gravSwapColor = lightGreen
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
player = Player(playerColor, -60, 320, 20, 40)
if level == 2:
    player.locY = 480
if level == 3 or level == 4:
    player.locY = 440

walls0 = [Wall(300, 460, 200, 40), Wall(0, 580, 800, 20)]
walls1 = [Wall(0, 520, 800, 80), Wall(180, 300, 40, 140), Wall(0, 360, 80, 160), Wall(700, 360, 100, 160), Wall(370, 400, 75, 40), Wall(485, 400, 215, 120), Wall(370, 500, 115, 20), Wall(0, 0, 520, 300), Wall(520, 0, 300, 200), Wall(780, 200, 20, 80)]
walls2 = [Wall(0, 520, 800, 80), Wall(0, 0, 40, 440), Wall(40, 0, 760, 80), Wall(200, 240, 60, 280), Wall(220, 80, 140, 40), Wall(100, 240, 100, 40), Wall(300, 240, 60, 230), Wall(300, 120, 30, 120), Wall(760, 80, 40, 320), Wall(720, 340, 40, 40), Wall(510, 280, 100, 40), Wall(720, 80, 40, 40), Wall(720, 480, 80, 40)]
walls3 = [Wall(0, 520, 800, 80), Wall(0, 0, 760, 80), Wall(760, 0, 40, 400), Wall(0, 80, 40, 320), Wall(520, 360, 240, 40), Wall(360, 200, 320, 40), Wall(320, 200, 40, 200), Wall(280, 280, 40, 120), Wall(240, 320, 40, 80), Wall(720, 300, 40, 60), Wall(720, 80, 40, 40), Wall(0, 480, 80, 40), Wall(40, 80, 40, 40), Wall(640, 140, 40, 60), Wall(440, 240, 40, 40), Wall(360, 240, 80, 200)]
walls4 = [Wall(0, 520, 800, 80), Wall(0, 0, 800, 180), Wall(0, 180, 40, 220), Wall(0, 480, 80, 40), Wall(40, 180, 40, 40), Wall(470, 180, 30, 40), Wall(720, 480, 40, 40), Wall(470, 320, 30, 100), Wall(500, 180, 30, 240), Wall(215, 320, 100, 40), Wall(760, 320, 40, 200)]
walls5 = []
walls = [walls0, walls1, walls2, walls3, walls4, walls5]

objects0 = [Block(400, 300), GravSwap("V", 400, 570), Treadmill("counter", 140, 480, 120), Treadmill("clock", 200, 200, 400)]
objects1 = [Block(425, 320), PlateDoor(red, "D", 100, 515, 780, 280, 20, 80, 780, 200)]
objects2 = [Block(520, 440), GravSwap("V", 150, 490), GravSwap("V", 435, 490), GravSwap("V", 435, 110), GravSwap("V", 260, 150), PlateDoor(red, "U", 530, 80, 760, 400, 40, 80, 760, 320)]
objects3 = [Block(320, 120), Block(110, 440), GravSwap("H", 730, 220), GravSwap("V", 430, 110), GravSwap("H", 70, 370), PlateDoor(red, "U", 120, 80, 520, 400, 40, 120, 320, 400), PlateDoor(blue, "D", 370, 515, 520, 80, 40, 120, 520, 240)]
objects4 = [Block(225, 440), Block(560, 440), GravSwap("V", 265, 390), GravSwap("V", 190, 210), PlateDoor(red, "D", 100, 515, 760, 180, 40, 140, 760, 40), PlateDoor(blue, "D", 235, 315, 470, 420, 60, 100, 470, 320)]
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
    playerChecksR = []
    playerChecksL = []
    playerChecksU = []
    playerChecksD = []
    for x in objects[level]:
        if isinstance(x, (Block, PlateDoor, Treadmill)):
            playerChecksR.append(playerBlock("R", x.locX, x.locY, x.width, x.height))
            playerChecksL.append(playerBlock("L", x.locX, x.locY, x.width, x.height))
            playerChecksU.append(playerBlock("U", x.locX, x.locY, x.width, x.height))
            playerChecksD.append(playerBlock("D", x.locX, x.locY, x.width, x.height))
    if all(playerChecksR) == True:
        player.blockedR = False
    else:
        player.blockedR = True
    if all(playerChecksL) == True:
        player.blockedL = False
    else:
        player.blockedL = True
    if all(playerChecksU) == True:
        player.blockedU = False
    else:
        player.blockedU = True
    if all(playerChecksD) == True:
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
                if isinstance(obj, (Block, PlateDoor, Treadmill)):
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

    #treadmill stuff
    for x in objects[level]:
        if isinstance(x, Treadmill):
            x.spin()

    #player stuff
    player.movement()
    winCheck()
    
    drawLevel(level)

    
