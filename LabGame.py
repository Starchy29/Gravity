from datetime import datetime
import time
import pygame
import sys
import math


"""
ls
git commit -am "message"
git push

git add <filename>
"""
black = (10, 10, 10)
white = (255, 255, 255)
blue = (  20, 20, 230)
green = (20, 225, 20)
red = (200, 40, 40)
yellow = (230, 230, 20)
lightBlue = (103, 173, 255)
lightPurple = (255, 170, 205)
lightGreen = (130, 255, 130)
lightRed = (230, 60, 60)
purple = (180, 30, 230)
playerColor = (160, 10, 200)
lightGrey = (205, 205, 205)
orange = (255, 180, 40)

#starting variables
displayWidth = 800
displayHeight = 600
screenColor = lightBlue
gravity = "D"
level = 0

#classes
class Player(object):
    jumping = False
    falling = False
    newJump = True
    jumpHeight = 0
    fallSpeed = 0
    startX = 0
    startY = 0
    canMoveR = True
    canMoveL = True
    canMoveU = True
    canMoveD = True
    def __init__(self, color, locX, locY, width, height):
        self.color = color
        self.width = width
        self.height = height
        self.locX = locX
        self.locY = locY
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.locX, self.locY, self.width, self.height), 0)
    def movement(self):
        #block checks
        self.canMoveR = canMove("R", self, (Block, Treadmill, PlateDoor), True)
        self.canMoveL = canMove("L", self, (Block, Treadmill, PlateDoor), True)
        self.canMoveU = canMove("U", self, (Block, Treadmill, PlateDoor), True)
        self.canMoveD = canMove("D", self, (Block, Treadmill, PlateDoor), True)

        self.startX = self.locX
        self.startY = self.locY
        
        #walking
        if keys[pygame.K_RIGHT] and self.canMoveR:
            self.locX += 0.5
        if keys[pygame.K_LEFT] and self.canMoveL:
            self.locX -= 0.5
        #gravity stuff
        self.newJump = False if keys[pygame.K_UP] else True
        if gravity == "D":
            #jumping
            if self.newJump and not self.jumping and not self.falling and self.canMoveU:
                self.jumping = True
                self.jumpHeight = 0
            if keys[pygame.K_UP] and self.jumping and self.jumpHeight < 140 and self.canMoveU:
                self.locY -= 1.25
                self.jumpHeight += 1.25
            if self.jumpHeight >= 140:
                self.jumping = False
                self.falling = True

            #falling
            if (upReleased() or not self.jumping or not self.canMoveU) and self.canMoveD:
                self.locY += 0.01 + self.fallSpeed
                self.fallSpeed += 0.005
                self.jumping = False
                self.falling = True
            if not self.canMoveD:
                self.falling = False
                self.fallSpeed = 0
                            
        elif gravity == "U":
            #jumping
            if self.newJump and not self.jumping and not self.falling and self.canMoveD:
                self.jumping = True
                self.jumpHeight = 0
            if keys[pygame.K_UP] and self.jumping and self.jumpHeight < 140 and self.canMoveD:
                self.locY += 1.25
                self.jumpHeight += 1.25
            if self.jumpHeight >= 140:
                self.jumping = False
                self.falling = True
            #falling
            if (upReleased() or not self.jumping or not self.canMoveD) and self.canMoveU:
                self.locY -= (0.01 + self.fallSpeed)
                self.fallSpeed += 0.005
                self.jumping = False
                self.falling = True
            if not self.canMoveU:
                self.falling = False
                self.fallSpeed = 0

        #Y correcttion
        for wall in walls[level]:
            if wall.locY < self.locY + self.height < wall.locY + wall.height / 2 and wall.locX - self.width < self.locX < wall.locX + wall.width:
                self.locY = wall.locY - self.height
            if wall.locY + wall.height / 2 < self.locY  < wall.locY + wall.height and wall.locX - self.width < self.locX < wall.locX + wall.width:
                self.locY = wall.locY + wall.height
        for x in objects[level]:
            if isinstance(x, (Block, Treadmill, PlateDoor)):
                if x.locY < self.locY + self.height < x.locY + x.height / 2 and x.locX - self.width < self.locX < x.locX + x.width:
                    self.locY = x.locY - self.height
                if x.locY + x.height / 2 < self.locY  < x.locY + x.height and x.locX - self.width < self.locX < x.locX + x.width:
                    self.locY = x.locY + x.height
        #offscreen pushing
        if self.locX < 0:
            self.locX += 0.5
            
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
    pushCount = False
    fallSpeed = 0
    startX = 0
    startY = 0
    canMoveR = False
    canMoveL = False
    canMoveU = False
    canMoveD = False
    spinning = False
    def __init__(self, locX, locY):
        self.locX = locX
        self.locY = locY
    def draw(self):
        pygame.draw.rect(screen, white, (self.locX, self.locY, self.width, self.height), 0)
        pygame.draw.rect(screen, lightGrey, (self.locX + 5, self.locY + 5, self.width - 10, self.height - 10), 0)
        pygame.draw.rect(screen, white, (self.locX + 20, self.locY + 20, self.width - 40, self.height - 40), 2)
    def update(self):
        #block checks
        self.canMoveR = canMove("R", self, (Block, Treadmill, PlateDoor, Player), True)
        self.canMoveL = canMove("L", self, (Block, Treadmill, PlateDoor, Player), True)
        self.canMoveU = canMove("U", self, (Block, Treadmill, PlateDoor, Player), True)
        self.canMoveD = canMove("D", self, (Block, Treadmill, PlateDoor, Player), True)

        self.startX = self.locX
        self.startY = self.locY
        
        #falling
        if gravity == "D":
            if self.canMoveD:
                self.locY += 0.01 + self.fallSpeed
                self.fallSpeed += 0.01
                self.falling = True
            else:
                self.fallSpeed = 0
                self.falling = False

        elif gravity == "U":
            if self.canMoveU:
                self.locY -= (0.01 + self.fallSpeed)
                self.fallSpeed += 0.01
                self.falling = True
            else:
                self.fallSpeed = 0
                self.falling = False

        #Y correcttion
        for wall in walls[level]:
            if wall.locY < self.locY + self.height < wall.locY + wall.height / 2 and wall.locX - self.width < self.locX < wall.locX + wall.width:
                self.locY = wall.locY - self.height
            if wall.locY + wall.height / 2 < self.locY  < wall.locY + wall.height and wall.locX - self.width < self.locX < wall.locX + wall.width:
                self.locY = wall.locY + wall.height
        for x in objects[level]:
            if isinstance(x, (Block, Treadmill, PlateDoor)) and not (x.locX == self.locX and x.locY == self.locY and x.height == self.height and x.width == self.width):
                if x.locY < self.locY + self.height < x.locY + x.height / 2 and x.locX - self.width < self.locX < x.locX + x.width:
                    self.locY = x.locY - self.height
                if x.locY + x.height / 2 < self.locY  < x.locY + x.height and x.locX - self.width < self.locX < x.locX + x.width:
                    self.locY = x.locY + x.height
        
    #pushing
        #player
        self.pushCount = not self.pushCount
        if keys[pygame.K_RIGHT] and self.pushCount and not self.falling and not self.spinning and self.canMoveR and oneBlock("R", player, self):
            self.locX += 0.5
        if keys[pygame.K_LEFT] and self.canMoveL and self.pushCount and not self.spinning and not self.falling and oneBlock("L", player, self):
            self.locX -= 0.5
        #door
        for door in objects[level]:
            if isinstance(door, PlateDoor):
                if oneBlock("R", door, self) and self.canMoveR and door.movingR:
                    self.locX += 1
                elif oneBlock("L", door, self) and self.canMoveL and door.movingL:
                    self.locX -= 1
                elif oneBlock("U", door, self) and self.canMoveU and door.movingU:
                    self.locY -= 1
                elif oneBlock("D", door, self) and self.canMoveD and door.movingD:
                    self.locY += 1
        self.spinning = False
            
class PlateDoor(object):
    plateWidth = 60
    plateHeight = 5
    triggered = False
    trigStart = False
    canMoveR = False
    canMoveL = False
    canMoveU = False
    canMoveD = False
    movingR = False
    movingL = False
    movingU = False
    movingD = False
    def __init__(self, color, pressDir, plateLocX, plateLocY, doorStartX, doorStartY, doorWidth, doorHeight, doorEndX, doorEndY):
        self.color = color
        self.pressDir = pressDir
        self.plateLocX = plateLocX
        self.plateLocY = plateLocY
        self.plateImageY = plateLocY
        self.doorStartX = doorStartX
        self.doorStartY = doorStartY
        self.width = doorWidth
        self.height = doorHeight
        self.doorEndX = doorEndX
        self.doorEndY = doorEndY
        self.locX = doorStartX
        self.locY = doorStartY
        self.startX = self.locX
        self.startY = self.locY
        
    def draw(self):
        pygame.draw.rect(screen, black, (self.locX, self.locY, self.width, self.height), 0) #door
        pygame.draw.rect(screen, self.color, (self.locX + 5, self.locY + 5, self.width - 10, self.height - 10), 0) #door
        pygame.draw.rect(screen, self.color, (self.plateLocX, self.plateImageY, self.plateWidth, self.plateHeight), 0) #plate
        
    def triggerCheck(self, x):
        if self.plateLocY - x.height <= x.locY <= self.plateLocY + 5 and self.plateLocX - x.width < x.locX < self.plateLocX + self.plateWidth:
            self.triggered = True
    
    def update(self):
        self.trigStart = self.triggered
        self.triggered = False
        for block in objects[level]:
                if isinstance(block, Block):
                    self.triggerCheck(block)
        self.triggerCheck(player)

        self.movingR = False
        self.movingL = False
        self.movingU = False
        self.movingD = False

        self.canMoveR = canMove("R", self, (Block, Player), False)
        self.canMoveL = canMove("L", self, (Block, Player), False)
        self.canMoveU = canMove("U", self, (Block, Player), False)
        self.canMoveD = canMove("D", self, (Block, Player), False)

        self.startX = self.locX
        self.startY = self.locY
        
        if self.triggered:
            if self.locY > self.doorEndY:
                self.movingU = True
                if self.canMoveU:
                    self.locY -= 1
            if self.locY < self.doorEndY:
                self.movingD = True
                if self.canMoveD:
                    self.locY += 1
            if self.locX > self.doorEndX:
                self.movingL = True
                if self.canMoveL:
                    self.locX -= 1
            if self.locX < self.doorEndX:
                self.movingR = True
                if self.canMoveR:
                    self.locX += 1

            self.plateHeight = 2
            if self.pressDir == "D":
                self.plateImageY = self.plateLocY + 3         
        else:
            if self.locY > self.doorStartY:
                self.movingU = True
                if self.canMoveU:
                    self.locY -= 1
            if self.locY < self.doorStartY:
                self.movingD = True
                if self.canMoveD:
                    self.locY += 1
            if self.locX > self.doorStartX:
                self.movingL = True
                if self.canMoveL:
                    self.locX -= 1
            if self.locX < self.doorStartX:
                self.movingR = True
                if self.canMoveR:
                    self.locX += 1

            self.plateImageY = self.plateLocY
            self.plateHeight = 5

        #player pushing
        if oneBlock("R", self, player) and player.canMoveR and self.movingR:
            player.locX += 1
        elif oneBlock("L", self, player) and player.canMoveL and self.movingL:
            player.locX -= 1
        elif oneBlock("U", self, player) and player.canMoveU and self.movingU:
            player.locY -= 1
        elif oneBlock("D", self, player) and player.canMoveD and self.movingD:
            player.locY += 1

gravSwapColor = lightGreen
class GravSwap(object):
    color = lightGreen
    newPress = False
    pressed = False
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
        
    def update(self):
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
            self.pressed = True
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
        else:
            self.pressed = False

class Treadmill(object):
    height = 40
    spinState = 20
    cooldown = 0
    lineX1 = 0
    lineX2 = 0
    angle1 = 0
    angle2 = 0
    spinCount = False
    color = black
    def __init__(self, rotation, locX, locY, width):
        self.rotation = rotation
        self.locX = locX
        self.locY = locY
        self.width = width
        self.numberLines = int((width - 40) / 20)
        self.lineColor = orange if self.rotation == "clock" else lightPurple
    def draw(self):
        pygame.draw.rect(screen, black, (self.locX + 20, self.locY, self.width - 40, self.height), 0)
        pygame.draw.circle(screen, black, (self.locX + 20, self.locY + 20), 20, 0)
        pygame.draw.circle(screen, black, (self.locX + self.width - 20, self.locY + 20), 20, 0)
        self.color = lightRed if self.rotation == "clock" else purple
        pygame.draw.rect(screen, self.color, (self.locX + 20, self.locY + 10, self.width - 40, self.height - 20), 0)
        pygame.draw.circle(screen, self.color, (self.locX + 20, self.locY + 20), 10, 0)
        pygame.draw.circle(screen, self.color, (self.locX + self.width - 20, self.locY + 20), 10, 0)
    def drawLines(self, color):
        if self.rotation == "clock":
            self.lineX1 = self.locX + self.spinState
            self.lineX2 = self.locX + self.width - self.spinState
            for x in range(self.numberLines):
                pygame.draw.line(screen, color, (self.lineX1, self.locY), (self.lineX1, self.locY + 10), 1)
                self.lineX1 += 20
                pygame.draw.line(screen, color, (self.lineX2, self.locY + 30), (self.lineX2, self.locY + 39), 1)
                self.lineX2 -= 20

            self.angle1 = math.pi + (self.spinState * -math.pi / 40)
            self.angle2 = self.angle1 - math.pi / 2
            pygame.draw.line(screen, color, (self.locX + self.width - 20 + (10 * math.cos(self.angle1)), self.locY + 20 - (10 * math.sin(self.angle1))), (self.locX + self.width - 20 + (19 * math.cos(self.angle1)), self.locY + 20 - (19 * math.sin(self.angle1))), 1)
            pygame.draw.line(screen, color, (self.locX + self.width - 20 + (10 * math.cos(self.angle2)), self.locY + 20 - (10 * math.sin(self.angle2))), (self.locX + self.width - 20 + (19 * math.cos(self.angle2)), self.locY + 20 - (19 * math.sin(self.angle2))), 1)
            pygame.draw.line(screen, color, (self.locX + 20 - (10 * math.cos(self.angle1)), self.locY + 20 + (10 * math.sin(self.angle1))), (self.locX + 20 - (20 * math.cos(self.angle1)), self.locY + 20 + (19 * math.sin(self.angle1))), 1)
            pygame.draw.line(screen, color, (self.locX + 20 - (10 * math.cos(self.angle2)), self.locY + 20 + (10 * math.sin(self.angle2))), (self.locX + 20 - (20 * math.cos(self.angle2)), self.locY + 20 + (19 * math.sin(self.angle2))), 1)
        elif self.rotation == "counter":
            self.lineX1 = self.locX + self.width - self.spinState
            self.lineX2 = self.locX + self.spinState
            for x in range(self.numberLines):
                pygame.draw.line(screen, color, (self.lineX1, self.locY), (self.lineX1, self.locY + 10), 1)
                self.lineX1 -= 20
                pygame.draw.line(screen, color, (self.lineX2, self.locY + 30), (self.lineX2, self.locY + 39), 1)
                self.lineX2 += 20

            self.angle1 = -math.pi + (self.spinState * math.pi / 40)
            self.angle2 = self.angle1 + math.pi / 2
            pygame.draw.line(screen, color, (self.locX + self.width - 20 + (10 * math.cos(self.angle1)), self.locY + 20 - (10 * math.sin(self.angle1))), (self.locX + self.width - 20 + (19 * math.cos(self.angle1)), self.locY + 20 - (19 * math.sin(self.angle1))), 1)
            pygame.draw.line(screen, color, (self.locX + self.width - 20 + (10 * math.cos(self.angle2)), self.locY + 20 - (10 * math.sin(self.angle2))), (self.locX + self.width - 20 + (19 * math.cos(self.angle2)), self.locY + 20 - (19 * math.sin(self.angle2))), 1)
            pygame.draw.line(screen, color, (self.locX + 20 - (10 * math.cos(self.angle1)), self.locY + 20 + (10 * math.sin(self.angle1))), (self.locX + 20 - (19 * math.cos(self.angle1)), self.locY + 20 + (19 * math.sin(self.angle1))), 1)
            pygame.draw.line(screen, color, (self.locX + 20 - (10 * math.cos(self.angle2)), self.locY + 20 + (10 * math.sin(self.angle2))), (self.locX + 20 - (19 * math.cos(self.angle2)), self.locY + 20 + (19 * math.sin(self.angle2))), 1)

    def spinImage(self):
        self.cooldown += 1
        if self.cooldown == 10:
            if self.spinState == 40: 
                self.spinState = 20
            else:
                self.spinState += 1
            self.cooldown = 0

    def update(self):
        self.spinCount = not self.spinCount
        if gravity == "U":
            for x in objects[level]:
                if isinstance(x, Block):

                    self.locX += 20
                    self.width -= 40
                    if oneBlock("U", x, self):
                        x.spinning = True
                    self.locX -= 20
                    self.width +=40
                    
                    if oneBlock("U", x, self) and self.spinCount:
                        if self.rotation == "clock" and x.canMoveL:
                            x.locX -= 0.5
                        elif self.rotation == "counter" and x.canMoveR:
                            x.locX += 0.5

            if oneBlock("U", player, self) and self.spinCount:
                        if self.rotation == "clock" and player.canMoveL:
                            player.locX -= 0.5
                        elif self.rotation == "counter" and player.canMoveR:
                            player.locX += 0.5
        elif gravity == "D":
            for x in objects[level]:
                if isinstance(x, Block):

                    self.locX += 20
                    self.width -= 40
                    if oneBlock("D", x, self):
                        x.spinning = True
                    self.locX -= 20
                    self.width +=40
                    
                    if oneBlock("D", x, self) and self.spinCount:
                        if self.rotation == "clock" and x.canMoveR:
                            x.locX += 0.5
                        elif self.rotation == "counter" and x.canMoveL:
                            x.locX -= 0.5
            if oneBlock("D", player, self) and self.spinCount:
                        if self.rotation == "clock" and player.canMoveR:
                            player.locX += 0.5
                        elif self.rotation == "counter" and player.canMoveL:
                            player.locX -= 0.5
#functions
def drawLevel():
    screen.fill(screenColor)
    for x in objects[level]:
        x.draw()
    player.draw()
    for x in walls[level]:
        pygame.draw.rect(screen, black, (x.locX, x.locY, x.width, x.height), 0)

redrawers = []
def reDraw():
    dirtRects = []
    global redrawers
    redrawers = []
    rewallers = []
    if player.startX != player.locX or player.startY != player.locY:
            dirtRects.append((player.locX, player.locY, player.width, player.height))
            dirtRects.append((player.startX, player.startY, player.width, player.height))
            pygame.draw.rect(screen, screenColor, (player.startX, player.startY, player.width, player.height), 0)
            gravCover(player)
            redrawers.append(player)
            plateCover(player)
    for x in objects[level]:
        if isinstance(x, Block) and (x.startX != x.locX or x.startY != x.locY):
            dirtRects.append((x.locX, x.locY, x.width, x.height))
            dirtRects.append((x.startX, x.startY, x.width, x.height))
            pygame.draw.rect(screen, screenColor, (x.startX, x.startY, x.width, x.height), 0)
            gravCover(x)
            redrawers.append(x)
            plateCover(x)
        elif isinstance(x, Treadmill):
            dirtRects.append((x.locX, x.locY, x.width, x.height)) #expand this part
            
            x.drawLines(black)
            x.spinImage()
            x.drawLines(x.lineColor)
        elif isinstance(x, PlateDoor):
            if x.startX != x.locX or x.startY != x.locY: #door
                dirtRects.append((x.startX, x.startY, x.width, x.height))
                dirtRects.append((x.locX, x.locY, x.width, x.height))
                pygame.draw.rect(screen, screenColor, (x.startX, x.startY, x.width, x.height), 0)
                gravCover(x)
                redrawers.append(x)
                plateCover(x)
                for wall in walls[level]:
                    if (wall.locX - x.width < x.locX < wall.locX + wall.width and wall.locY - x.height < x.locY < wall.locY + wall.height) or (wall.locX - x.width < x.startX < wall.locX + wall.width and wall.locY - x.height < x.startY < wall.locY + wall.height):
                        rewallers.append(wall)
            if x.trigStart != x.triggered: #plate
                if x.triggered:
                    pygame.draw.rect(screen, screenColor, (x.plateLocX, x.plateLocY, x.plateWidth, 5), 0)
                elif x.pressDir == "D":
                    pygame.draw.rect(screen, screenColor, (x.plateLocX, x.plateLocY + 3, x.plateWidth, 2), 0)
                elif x.pressDir == "U":
                    pygame.draw.rect(screen, screenColor, (x.plateLocX, x.plateLocY, x.plateWidth, 2), 0)
                dirtRects.append((x.plateLocX, x.plateLocY, x.plateWidth, 5))
                redrawers.append(x)
        elif isinstance(x, GravSwap) and x.pressed:
            drawLevel()
            pygame.display.update()
            return
    for x in redrawers:
        x.draw()
    for wall in rewallers:
        pygame.draw.rect(screen, black, (wall.locX, wall.locY, wall.width, wall.height), 0)
    pygame.display.update(dirtRects)
    
def gravCover(y):
    for x in objects[level]:
        if isinstance(x, GravSwap) and x.locX - 30 - y.width <= y.locX <= x.locX + 30 and x.locY - 30 - y.height <= y.locY <= x.locY + 32:
            x.draw()

def plateCover(y):
    for x in objects[level]:
        if isinstance(x, PlateDoor) and x.plateLocX - y.width <= y.locX <=  x.plateLocX + x.plateWidth and x.plateImageY - y.height <= y.locY <=  x.plateImageY + x.plateHeight + 1:
            global redrawers
            redrawers.append(x)

def oneBlock(direction, test, block):
    if direction == "R":
        if int(test.locX) + test.width == int(block.locX) and block.locY - test.height < test.locY < block.locY + block.height:
            return True
        else:
            return False
    if direction == "L":
        if int(test.locX) == int(block.locX) + block.width and block.locY - test.height < test.locY < block.locY + block.height:
            return True
        else:
            return False
    if direction == "U":
        if block.locY + (block.height / 2) < test.locY <= block.locY + block.height and block.locX - test.width < test.locX < block.locX + block.width:
            return True
        else:
            return False
    if direction == "D":
        if block.locY - test.height <= test.locY < block.locY + (block.height / 2) - test.height and block.locX - test.width < test.locX < block.locX + block.width:
            return True
        else:
            return False
        
def canMove(direction, test, blockers, wallBlock):
    objects[level].append(player)
    blockChecks = []
    for x in objects[level]:
        if isinstance(x, blockers) and not (test.locX == x.locX and test.locY == x.locY and test.width == x.width and test.height == x.height):
            blockChecks.append(oneBlock(direction, test, x))
    if wallBlock:
        for wall in walls[level]:
            blockChecks.append(oneBlock(direction, test, wall))
    objects[level].remove(player)
    if (direction == "L" and test.locX == 0) or (direction == "D" and test.locX < 0):
        blockChecks.append(True)  
    if any(blockChecks) == True:
        return False
    else:
        return True
        
def winCheck():
    if player.locX > displayWidth + 2:
        global level
        global gravity
        global screenColor
        global gravSwapColor
        level += 1
        gravity = "D"
        screenColor = lightBlue
        gravSwapColor = lightGreen

        spawnSpot()
        drawLevel()
        pygame.display.update()
        
def upReleased():
    keyPressed = pygame.key.get_pressed()
    if keyPressed[pygame.K_UP]:
        return False
    else:
        return True

def spawnSpot():
    if level > 0:
        player.locX = 0
    if level == 1:
        player.locY = 320
    if level == 2:
        player.locY = 480
    if level == 3 or level == 4 or level == 5:
        player.locY = 440
    
#set up
player = Player(playerColor, 200, 420, 20, 40)
spawnSpot()

walls0 = [Wall(300, 460, 200, 40), Wall(0, 0, 800, 40), Wall(0, 580, 800, 20)]
walls1 = [Wall(0, 520, 800, 80), Wall(180, 300, 40, 140), Wall(0, 360, 80, 160), Wall(700, 360, 100, 160), Wall(370, 400, 75, 40), Wall(485, 400, 215, 120), Wall(370, 500, 115, 20), Wall(0, 0, 520, 300), Wall(520, 0, 300, 200), Wall(780, 200, 20, 80)]
walls2 = [Wall(0, 520, 800, 80), Wall(0, 0, 40, 440), Wall(40, 0, 760, 80), Wall(200, 240, 60, 280), Wall(220, 80, 140, 40), Wall(100, 240, 100, 40), Wall(300, 240, 60, 230), Wall(300, 120, 30, 120), Wall(760, 80, 40, 320), Wall(720, 340, 40, 40), Wall(510, 280, 100, 40), Wall(720, 80, 40, 40), Wall(720, 480, 80, 40)]
walls3 = [Wall(0, 520, 800, 80), Wall(0, 0, 760, 80), Wall(760, 0, 40, 400), Wall(0, 80, 40, 320), Wall(520, 360, 240, 40), Wall(360, 200, 320, 40), Wall(320, 200, 40, 200), Wall(280, 280, 40, 120), Wall(240, 320, 40, 80), Wall(720, 300, 40, 60), Wall(720, 80, 40, 40), Wall(0, 480, 80, 40), Wall(40, 80, 40, 40), Wall(640, 140, 40, 60), Wall(440, 240, 40, 40), Wall(360, 240, 80, 200)]
walls4 = [Wall(0, 520, 800, 80), Wall(0, 0, 800, 180), Wall(0, 180, 40, 220), Wall(0, 480, 80, 40), Wall(40, 180, 40, 40), Wall(470, 180, 30, 40), Wall(720, 480, 40, 40), Wall(470, 320, 30, 100), Wall(500, 180, 30, 240), Wall(215, 320, 100, 40), Wall(760, 320, 40, 200)]
walls5 = [Wall(0, 520, 800, 80), Wall(0, 0, 800, 40), Wall(0, 480, 40, 40), Wall(200, 480, 120, 40), Wall(0, 40, 40, 360), Wall(40, 240, 280, 160), Wall(760, 40, 40, 400), Wall(280, 160, 40, 80), Wall(320, 360, 440, 40), Wall(580, 400, 180, 40), Wall(400, 200, 80, 40), Wall(600, 200, 80, 40)]
walls6 = [Wall(0, 520, 600, 80), Wall(600, 560, 200, 40), Wall(0, 0, 800, 80), Wall(0, 80, 40, 360), Wall(760, 80, 40, 340), Wall(680, 80, 80, 260), Wall(600, 80, 80, 340)]
walls7 = [Wall(0, 560, 480, 40), Wall(480, 520, 320, 80), Wall(0, 80, 20, 400), Wall(0, 0, 800, 80), Wall(780, 320, 20, 200), Wall(760, 480, 20, 40), Wall(600, 80, 40, 360), Wall(780, 80, 20, 120), Wall(170, 200, 200, 40)]
walls8 = [Wall(0, 520, 800, 80)]
walls = [walls0, walls1, walls2, walls3, walls4, walls5, walls6, walls7, walls8]

objects0 = [Block(400, 300), GravSwap("V", 400, 530), Treadmill("clock", 180, 460, 120), PlateDoor(red, "U", 300, 500, 40, 200, 40, 40, 760, 200), PlateDoor(blue, "D", 300, 455, 40, 160, 40, 40, 760, 160)]
objects1 = [Block(425, 320), PlateDoor(red, "D", 100, 515, 780, 280, 20, 80, 780, 200)]
objects2 = [Block(520, 440), GravSwap("V", 150, 490), GravSwap("V", 435, 490), GravSwap("V", 435, 110), GravSwap("V", 260, 150), PlateDoor(red, "U", 530, 80, 760, 400, 40, 80, 760, 320)]
objects3 = [Block(320, 120), Block(110, 440), GravSwap("H", 730, 220), GravSwap("V", 430, 110), GravSwap("H", 70, 370), PlateDoor(red, "U", 120, 80, 520, 400, 40, 120, 320, 400), PlateDoor(blue, "D", 370, 515, 520, 80, 40, 120, 520, 240)]
objects4 = [Block(225, 440), Block(560, 440), GravSwap("V", 265, 390), GravSwap("V", 190, 210), PlateDoor(red, "D", 100, 515, 760, 180, 40, 140, 760, 40), PlateDoor(blue, "D", 235, 315, 470, 420, 60, 100, 470, 320)]
objects5 = [Block(40, 160), GravSwap("V", 690, 490), GravSwap("V", 240, 450), GravSwap("V", 450, 490), Treadmill("counter", 320, 320, 440), Treadmill("clock", 40, 480, 160), Treadmill("counter", 40, 40, 720), PlateDoor(red, "D", 200, 235, 280, 400, 40, 80, 280, 320), PlateDoor(blue, "U", 420, 400, 280, 80, 40, 80, 280, 160), PlateDoor(green, "D", 410, 195, 580, 440, 40, 80, 580, 520), PlateDoor(yellow, "D", 610, 195, 760, 440, 40, 80, 760, 520)]
objects6 = [Block(520, 460), Treadmill("counter", 600, 520, 200)]
objects7 = [Block(200, 480)]
objects8 = []
objects = [objects0, objects1, objects2, objects3, objects4, objects5, objects6, objects7, objects8]

screen = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("LabGame")
drawLevel()
pygame.display.update()

#gamegame
running = True
timer = 0
while running:

    timer += 1
    if timer == 2000:
        timer = 0
    else:
        continue

    #quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            break
            
    keys = pygame.key.get_pressed()

    #player stuff
    player.movement()
    winCheck()

    #object stuff
    for x in objects[level]:
        x.update()


    reDraw()
    
