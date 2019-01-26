import time
import pygame
import sys
import math


"""
ls
git commit -am "message"
git push
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
displayWidth = 1200
displayHeight = 900
screenColor = lightBlue
gravity = 1
FPS = 120.0
level = 1

#classes
class Player(object):
    jumping = False
    falling = False
    jumpHeight = 0
    fallSpeed = 0
    startX = 0
    startY = 0
    canMoveR = True
    canMoveL = True
    canMoveU = True
    canMoveD = True
    pushingR = False
    pushingL = False
    spinning = 'N' #allows push to work easily
    
    def __init__(self, color, locX, locY, width, height):
        self.color = color
        self.width = width
        self.height = height
        self.locX = locX
        self.locY = locY
        self.blockers = (Wall, Block, PlateDoor, Treadmill)
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.locX, self.locY, self.width, self.height), 0)
        
    def movement(self):
        #block checks
        self.canMoveR = canMove('R', self)
        self.canMoveL = canMove('L', self)
        self.canMoveU = canMove('U', self)
        self.canMoveD = canMove('D', self)
        canJump = gravity == 1 and self.canMoveU or gravity == -1 and self.canMoveD
        canFall = gravity == 1 and self.canMoveD or gravity == -1 and self.canMoveU
        newJump = not keys[pygame.K_UP]
        self.pushingR = keys[pygame.K_RIGHT] and not self.canMoveR
        self.pushingL = keys[pygame.K_LEFT] and not self.canMoveL
        
        #walking
        if keys[pygame.K_RIGHT] and self.canMoveR:
                self.locX += 3
        if keys[pygame.K_LEFT] and self.canMoveL:
                self.locX -= 3

        #jumping
        if newJump and not self.jumping and not self.falling and canJump:
            self.jumping = True
            self.jumpHeight = 0
        if keys[pygame.K_UP] and self.jumping and self.jumpHeight < 140 and canJump:
            self.locY -= 7.5 * gravity
            self.jumpHeight += 7.5
        if self.jumpHeight >= 140:
            self.jumping = False
            self.falling = True

        #falling
        if (upReleased() or not self.jumping or not canJump) and canFall:
            self.locY += (0.06 + self.fallSpeed) * gravity
            self.fallSpeed += 0.25
            self.jumping = False
            self.falling = True
        if not canFall:
            self.falling = False
            self.fallSpeed = 0

        #pushing
        if self.pushingR:
            push('R', self, 2)
        if self.pushingL:
            push('L', self, 2)
        
        #offscreen
        if self.locX < 0:
            self.locX += 1

        fixPos(self)
            
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
    canMoveR = False
    canMoveL = False
    canMoveU = False
    canMoveD = False
    spinning = 'N'
    
    def __init__(self, locX, locY):
        self.locX = locX
        self.locY = locY
        self.startX = locX
        self.startY = locY
        self.blockers = (Player, Wall, Block, PlateDoor, Treadmill)
        
    def draw(self):
        pygame.draw.rect(screen, white, (self.locX, self.locY, self.width, self.height), 0)
        pygame.draw.rect(screen, lightGrey, (self.locX + 5, self.locY + 5, self.width - 10, self.height - 10), 0)
        pygame.draw.rect(screen, white, (self.locX + 20, self.locY + 20, self.width - 40, self.height - 40), 2)
        
    def update(self):
        #block checks
        self.canMoveR = canMove('R', self)
        self.canMoveL = canMove('L', self)
        self.canMoveU = canMove('U', self)
        self.canMoveD = canMove('D', self)
        canFall = gravity == 1 and self.canMoveD or gravity == -1 and self.canMoveU
        
        #falling
        if canFall:
            self.locY += (0.06 + self.fallSpeed) * gravity
            self.fallSpeed += 0.4
            self.falling = True
        else:
            self.fallSpeed = 0
            self.falling = False
        
        self.spinning = 'N'
        fixPos(self)
            
class PlateDoor(object):
    plateWidth = 60
    plateHeight = 5
    triggered = False
    trigStart = False
    canMoveR = False
    canMoveL = False
    canMoveU = False
    canMoveD = False
    pushingR = False
    pushingL = False
    pushingU = False
    pushingD = False
    
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
        self.blockers = (Block, PlateDoor, Player)
        
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

        self.pushingR = False
        self.pushingL = False
        self.pushingU = False
        self.pushingD = False

        self.canMoveR = canMove('R', self)
        self.canMoveL = canMove('L', self)
        self.canMoveU = canMove('U', self)
        self.canMoveD = canMove('D', self)

        if self.triggered:
            if self.locY > self.doorEndY:
                if self.canMoveU:
                    self.locY = self.doorEndY if self.locY - self.doorEndY < 12 else self.locY - 12
                else:
                    self.pushingU = True
            if self.locY < self.doorEndY:
                if self.canMoveD:
                    self.locY = self.doorEndY if self.doorEndY - self.locY < 12 else self.locY + 12
                else:
                    self.pushingD = True
            if self.locX > self.doorEndX:
                if self.canMoveL:
                    self.locX = self.doorEndX if self.locX - self.doorEndX < 12 else self.locX - 12
                else:
                    self.pushingL = True
            if self.locX < self.doorEndX:
                if self.canMoveR:
                    self.locX = self.doorEndX if self.doorEndX - self.locX< 12 else self.locX + 12
                else:
                    self.pushingR = True

            self.plateHeight = 2
            if self.pressDir == 'D':
                self.plateImageY = self.plateLocY + 3         
        else:
            if self.locY > self.doorStartY:
                if self.canMoveU:
                    self.locY = self.doorStartY if self.locY - self.doorStartY < 12 else self.locY - 12
                else:
                    self.pushingU = True
            if self.locY < self.doorStartY:
                if self.canMoveD:
                    self.locY = self.doorStartY if self.doorStartY - self.locY < 12 else self.locY + 12
                else:
                    self.pushingD = True
            if self.locX > self.doorStartX:
                if self.canMoveL:
                    self.locX = self.doorStartX if self.locX - self.doorStartX < 12 else self.locX - 12
                else:
                    self.pushingL = True
            if self.locX < self.doorStartX:
                if self.canMoveR:
                    self.locX = self.doorStartX if self.doorStartX - self.locX< 12 else self.locX + 12
                else:
                    self.pushingR = True

            self.plateImageY = self.plateLocY
            self.plateHeight = 5
        
        if self.pushingR:
            push('R', self, 8)
        if self.pushingL:
            push('L', self, 8)
        if self.pushingU:
            push('U', self, 8)
        if self.pushingD:
            push('D', self, 8)
        fixPos(self)

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
        if self.rotation == 'V':
            pygame.draw.line(screen, black, (self.locX, self.locY - 30), (self.locX, self.locY + 30), 8)
        elif self.rotation == 'H':
            pygame.draw.line(screen, black, (self.locX - 30, self.locY), (self.locX + 30, self.locY), 8)
        pygame.draw.circle(screen, black, (self.locX, self.locY), 20, 0)
        pygame.draw.circle(screen, gravSwapColor, (self.locX, self.locY), 15, 0)
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
            gravity *= -1
            screenColor = lightBlue if gravity == 1 else lightGreen
            gravSwapColor = lightGreen if gravity == 1 else lightBlue
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
    
    def __init__(self, rotation, locX, locY, width):
        self.rotation = rotation
        self.locX = locX
        self.locY = locY
        self.width = width
        self.numberLines = int((width - 40) / 20)
        
    def draw(self):
        pygame.draw.rect(screen, black, (self.locX + 20, self.locY, self.width - 40, self.height), 0)
        pygame.draw.circle(screen, black, (self.locX + 20, self.locY + 20), 20, 0)
        pygame.draw.circle(screen, black, (self.locX + self.width - 20, self.locY + 20), 20, 0)
        color = lightRed if self.rotation == 'R' else purple
        pygame.draw.rect(screen, color, (self.locX + 20, self.locY + 10, self.width - 40, self.height - 20), 0)
        pygame.draw.circle(screen, color, (self.locX + 20, self.locY + 20), 10, 0)
        pygame.draw.circle(screen, color, (self.locX + self.width - 20, self.locY + 20), 10, 0)
        
    def drawLines(self, color):
        if self.rotation == 'R':
            self.lineX1 = self.locX + self.spinState
            self.lineX2 = self.locX + self.width - self.spinState
            for x in range(self.numberLines):
                pygame.draw.line(screen, color, (self.lineX1, self.locY), (self.lineX1, self.locY + 9), 1)
                self.lineX1 += 20
                pygame.draw.line(screen, color, (self.lineX2, self.locY + 30), (self.lineX2, self.locY + 39), 1)
                self.lineX2 -= 20

            self.angle1 = math.pi + (self.spinState * -math.pi / 40)
            self.angle2 = self.angle1 - math.pi / 2
            pygame.draw.line(screen, color, (self.locX + self.width - 20 + (10 * math.cos(self.angle1)), self.locY + 20 - (10 * math.sin(self.angle1))), (self.locX + self.width - 20 + (19 * math.cos(self.angle1)), self.locY + 20 - (19 * math.sin(self.angle1))), 1)
            pygame.draw.line(screen, color, (self.locX + self.width - 20 + (10 * math.cos(self.angle2)), self.locY + 20 - (10 * math.sin(self.angle2))), (self.locX + self.width - 20 + (19 * math.cos(self.angle2)), self.locY + 20 - (19 * math.sin(self.angle2))), 1)
            pygame.draw.line(screen, color, (self.locX + 20 - (10 * math.cos(self.angle1)), self.locY + 20 + (10 * math.sin(self.angle1))), (self.locX + 20 - (20 * math.cos(self.angle1)), self.locY + 20 + (19 * math.sin(self.angle1))), 1)
            pygame.draw.line(screen, color, (self.locX + 20 - (10 * math.cos(self.angle2)), self.locY + 20 + (10 * math.sin(self.angle2))), (self.locX + 20 - (20 * math.cos(self.angle2)), self.locY + 20 + (19 * math.sin(self.angle2))), 1)
        elif self.rotation == 'L':
            self.lineX1 = self.locX + self.width - self.spinState
            self.lineX2 = self.locX + self.spinState
            for x in range(self.numberLines):
                pygame.draw.line(screen, color, (self.lineX1, self.locY), (self.lineX1, self.locY + 9), 1)
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
        if self.spinState == 40: 
            self.spinState = 20
        else:
            self.spinState += 1
        
    def treadBlockBlock(self, direction, test):
        if test is player:
            return False
        if direction == 'U':
            return self.locY + (self.height / 2) < test.locY <= self.locY + self.height and self.locX - test.width  + 20 < test.locX < self.locX + self.width - 20
        if direction == 'D':
            return self.locY - test.height <= test.locY < self.locY + (self.height / 2) - test.height and self.locX - test.width + 20 < test.locX < self.locX + self.width - 20
    #tries to spin player and blocks
    def update(self):
        objects[level].append(player)
        checkDir = 'D' if gravity == 1 else 'U'
        for x in objects[level]:
            if isinstance(x, (Block, Player)):
                if self.treadBlockBlock(checkDir, x):
                    x.spinning = self.rotation if gravity == 1 else opposite(self.rotation)
                canMove = x.canMoveR if gravity == 1 and self.rotation == 'R' or gravity == -1 and self.rotation == 'L' else x.canMoveL
                if oneBlock(checkDir, x, self):
                    if self.rotation == 'R' and canMove:
                        if gravity == 1 and x.locX > self.locX + self.width - 1.5:
                            x.locX = self.locX + self.width
                        elif gravity == -1 and x.locX + x.width < self.locX + 1.5:
                            x.locX = self.locX - x.width
                        else:
                            x.locX += 1.5 * gravity
                        fixPos(x)
                    elif self.rotation == 'L' and canMove:
                        if gravity == 1 and x.locX + x.width < self.locX + 1.5:
                            x.locX = self.locX - x.width
                        elif gravity == -1 and x.locX > self.locX + self.width - 1.5:
                            x.locX = self.locX + self.width
                        else:
                            x.locX -= 1.5 * gravity
                        fixPos(x)
        objects[level].remove(player)
        
#functions
def drawLevel():
    screen.fill(screenColor)
    for x in objects[level]:
        if isinstance(x, GravSwap):
            x.draw()
    for x in objects[level]:
        if not isinstance(x, GravSwap):
            x.draw()
    for x in walls[level]:
        pygame.draw.rect(screen, black, (x.locX, x.locY, x.width, x.height), 0)
    player.draw()
    

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
            dirtRects.append((x.locX, x.locY, x.width, x.height))
            x.drawLines(black)
            x.spinImage()
            x.drawLines(lightGrey)
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
                elif x.pressDir == 'D':
                    pygame.draw.rect(screen, screenColor, (x.plateLocX, x.plateLocY + 3, x.plateWidth, 2), 0)
                elif x.pressDir == 'U':
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
        if isinstance(x, GravSwap) and x.locX - 30 - y.width <= y.startX <= x.locX + 30 and x.locY - 30 - y.height <= y.startY <= x.locY + 30:
            x.draw()

def plateCover(y):
    for x in objects[level]:
        if isinstance(x, PlateDoor) and x.plateLocX - y.width <= y.startX <=  x.plateLocX + x.plateWidth and x.plateImageY - y.height <= y.startY <=  x.plateImageY + x.plateHeight:
            global redrawers
            redrawers.append(x)

def fixPos(obj):
    objects[level].append(player)
    blocks = [walls[level], objects[level]]
    for arr in blocks:
        for block in arr:
            if isinstance(block, obj.blockers) and not block is obj and block.locY - obj.height < obj.locY < block.locY + block.height and block.locX - obj.width < obj.locX < block.locX + block.width:
                if obj.startX > block.locX + block.width: 
                    obj.locX = block.locX + block.width
                elif obj.startX < block.locX - obj.width:
                    obj.locX = block.locX - obj.width
                if obj.startY >= block.locY + block.height: #Ys get the equal to prevent horizontal crunch jankiness (be careful with vertical)
                    obj.locY = block.locY + block.height
                elif obj.startY <= block.locY - obj.height:
                    obj.locY = block.locY - obj.height
    objects[level].remove(player)
                    
def oneBlock(direction, test, block):
    if direction == 'R':
        return test.locX + test.width == block.locX and block.locY - test.height < test.locY < block.locY + block.height
    if direction == 'L':
        return test.locX == block.locX + block.width and block.locY - test.height < test.locY < block.locY + block.height
    if direction == 'U':
        return block.locY + (block.height / 2) < test.locY <= block.locY + block.height and block.locX - test.width < test.locX < block.locX + block.width
    if direction == 'D':
        return block.locY - test.height <= test.locY < block.locY + (block.height / 2) - test.height and block.locX - test.width < test.locX < block.locX + block.width
        
def canMove(direction, test):
    objects[level].append(player)
    blockChecks = []
    arrs = [walls[level], objects[level]]
    for arr in arrs:
        for x in arr:
            if isinstance(x, test.blockers) and not x is test:
                blockChecks.append(oneBlock(direction, test, x))
    objects[level].remove(player)
    if (direction == 'L' and test.locX <= 0) or (direction == 'D' and test.locX < 0):
        blockChecks.append(True)  
    return not any(blockChecks)

def push(direction, test, pushSpeed):
    objects[level].append(player)
    for block in objects[level]:
        if isinstance(block, (Block, Player)) and not block is test and oneBlock(direction, test, block) and not block.falling and (block.spinning == 'N' or block.spinning == direction):
            push(direction, block, pushSpeed)
    if canMove(direction, test):
        if direction == 'R':
            test.locX += pushSpeed
        elif direction == 'L':
            test.locX -= pushSpeed
        elif direction == 'U':
            test.locY -= pushSpeed
        elif direction == 'D':
            test.locY += pushSpeed
        fixPos(test)       
    objects[level].remove(player) 

def winCheck():
    if player.locX > displayWidth + 2:
        global level
        global gravity
        global screenColor
        global gravSwapColor
        level += 1
        gravity = 1
        screenColor = lightBlue
        gravSwapColor = lightGreen

        spawnSpot()
        drawLevel()
        pygame.display.update()
        
def upReleased():
    keyPressed = pygame.key.get_pressed()
    return not keyPressed[pygame.K_UP]

def opposite(direction):
    if direction == 'R':
        return 'L'
    elif direction == 'L':
        return 'R'
    elif direction == 'U':
        return 'D'
    elif direction == 'D':
        return 'U'
    else:
        return direction

def spawnSpot():
    if level > 0:
        player.locX = -20
    switch = {
        1: 360,
        2: 760,
        3: 640,
        4: 620,
        5: 780,
        6: 700,
        7: 650
    }
    player.locY = switch.get(level, 80)
    
#set up
player = Player(playerColor, 200, 420, 20, 40)
spawnSpot()

walls0 = [Wall(0, 0, 1200, 40), Wall(0, 860, 1200, 40)]
walls1 = [Wall(0, 0, 1200, 320), Wall(0, 700, 1200, 200), Wall(0, 400, 300, 300), Wall(400, 320, 80, 300), Wall(1100, 480, 100, 220), Wall(680, 600, 120, 40), Wall(830, 600, 270, 100), Wall(480, 320, 335, 180), Wall(1060, 560, 40, 40)]
walls2 = [Wall(0, 0, 1200, 100), Wall(0, 800, 1200, 100), Wall(0, 100, 80, 620), Wall(400, 300, 80, 500), Wall(160, 300, 240, 80), Wall(600, 100, 80, 640), Wall(480, 100, 120, 40), Wall(680, 100, 40, 40), Wall(680, 660, 40, 80), Wall(1120, 760, 80, 40), Wall(1160, 100, 40, 540), Wall(1120, 100, 40, 420), Wall(870, 480, 100, 40)]
walls3 = [Wall(0, 0, 1200, 120), Wall(0, 720, 1200, 180), Wall(0, 680, 80, 40), Wall(0, 120, 40, 480), Wall(1160, 120, 40, 480), Wall(360, 520, 80, 80), Wall(600, 280, 400, 200), Wall(440, 440, 80, 160), Wall(520, 360, 80, 240), Wall(600, 480, 140, 160), Wall(40, 120, 40, 40), Wall(800, 560, 360, 40), Wall(960, 120, 40, 40), Wall(960, 240, 40, 40), Wall(1080, 200, 80, 40), Wall(1000, 320, 80, 40), Wall(1080, 440, 80, 40)]
walls4 = [Wall(0, 0, 1200, 200), Wall(0, 700, 1200, 200), Wall(0, 200, 80, 380), Wall(1120, 500, 80, 200), Wall(1120, 200, 80, 220), Wall(640, 200, 80, 200), Wall(0, 660, 120, 40), Wall(80, 200, 40, 40), Wall(600, 200, 40, 40), Wall(1080, 660, 40, 40), Wall(600, 320, 60, 260), Wall(300, 400, 80, 40)]
walls5 = [Wall(0, 0, 1200, 80), Wall(0, 820, 80, 80), Wall(80, 860, 320, 40), Wall(400, 820, 800, 80), Wall(0, 80, 80, 660), Wall(1120, 80, 80, 660), Wall(80, 660, 1040, 80), Wall(400, 200, 80, 460), Wall(760, 350, 80, 40)]
walls6 = [Wall(0, 0, 700, 120), Wall(780, 0, 420, 120), Wall(700, 0, 80, 80), Wall(0, 780, 780, 120), Wall(780, 820, 420, 80), Wall(900, 780, 300, 40), Wall(0, 120, 80, 540), Wall(0, 740, 120, 40), Wall(80, 120, 40, 40), Wall(820, 120, 120, 120), Wall(780, 120, 40, 40), Wall(780, 360, 80, 320), Wall(860, 360, 80, 200), Wall(940, 120, 260, 440), Wall(900, 560, 220, 40), Wall(1160, 560, 40, 70), Wall(1160, 750, 40, 30), Wall(360, 120, 40, 40)]
walls7 = [Wall(0, 0, 420, 170), Wall(420, 0, 120, 130), Wall(540, 0, 660, 170), Wall(0, 730, 1200, 170), Wall(0, 690, 160, 40), Wall(0, 170, 40, 440), Wall(40, 170, 40, 40), Wall(40, 330, 120, 80), Wall(1160, 490, 40, 280), Wall(1080, 170, 120, 240), Wall(1000, 170, 40, 40), Wall(1040, 170, 40, 320), Wall(880, 690, 280, 40), Wall(600, 430, 120, 40)]
walls8 = [Wall(0, 820, 1200, 80)]
walls = [walls0, walls1, walls2, walls3, walls4, walls5, walls6, walls7, walls8]

objects0 = [Block(400, 400), Block(400, 300), Treadmill('R', 700, 860, 80)]
objects1 = [Block(775, 520), PlateDoor(red, 'D', 320, 695, 1160, 320, 40, 160, 1160, 160)]
objects2 = [Block(720, 720), GravSwap('V', 350, 770), GravSwap('V', 540, 170), GravSwap('V', 780, 130), GravSwap('V', 920, 770), PlateDoor(red, 'U', 890, 100, 1160, 640, 40, 120, 1160, 420)]
objects3 = [Block(240, 640), Block(680, 200), GravSwap('V', 140, 690), GravSwap('V', 800, 150), GravSwap('H', 1110, 340), PlateDoor(red, 'U', 180, 120, 800, 600, 40, 120, 440, 600), PlateDoor(blue, 'D', 620, 715, 960, 160, 40, 80, 960, 80)]
objects4 = [Block(430, 620), Block(860, 620), GravSwap('V', 340, 670), GravSwap('V', 470, 230), PlateDoor(red, 'D', 310, 395, 600, 580, 60, 120, 600, 470), PlateDoor(blue, 'D', 160, 695, 1120, 420, 40, 80, 1120, 340)]
objects5 = [Block(80, 580), GravSwap('V', 440, 790), GravSwap('V', 660, 790), GravSwap('V', 980, 790), Treadmill('R', 80, 820, 160), Treadmill('L', 240, 820, 160), Treadmill('L', 80, 80, 1040), Treadmill('L', 480, 620, 640), PlateDoor(red, 'D', 320, 655, 480, 740, 40, 80, 480, 660), PlateDoor(blue, 'U', 630, 740, 400, 120, 80, 80, 400, 200), PlateDoor(green, 'D', 770, 345, 800, 740, 40, 80, 800, 660), PlateDoor(yellow, 'U', 770, 390, 1120, 740, 40, 80, 1120, 660)]
objects6 = [Block(700, 700), Block(860, 240), GravSwap('V', 430, 750), GravSwap('V', 170, 150), GravSwap('V', 1010, 630), Treadmill('R', 320, 520, 380), Treadmill('L', 780, 780, 120), Treadmill('L', 780, 320, 160), Treadmill('L', 860, 560, 40), Treadmill('R', 1120, 560, 40), PlateDoor(red, 'D', 930, 775, 1160, 630, 40, 120, 1160, 510), PlateDoor(blue, 'D', 1030, 775, 820, 240, 40, 80, 820, 160), PlateDoor(green, 'U', 420, 120, 700, 80, 80, 40, 700, 640)]
objects7 = [Block(80, 250), Block(760, 650), GravSwap('V', 660, 400), GravSwap('V', 660, 500), Treadmill('L', 840, 690, 40), Treadmill('R', 160, 690, 40), Treadmill('L', 520, 430, 80), Treadmill('R', 720, 430, 80), Treadmill('L', 420, 130, 120)]
objects8 = []
objects = [objects0, objects1, objects2, objects3, objects4, objects5, objects6, objects7, objects8]

screen = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("LabGame")
drawLevel()
pygame.display.update()

#gamegame
running = True
while running:
    startT = time.time()
    #quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            break
            
    keys = pygame.key.get_pressed()
    
    for x in objects[level]:
        if isinstance(x, (Block, PlateDoor)):
            x.startX = x.locX
            x.startY = x.locY
    player.startX = player.locX
    player.startY = player.locY

    player.movement()
    winCheck()

    for x in objects[level]:
        x.update()

    if time.time() - startT <= 1 / FPS:
        time.sleep(1 / FPS - time.time() + startT)
    else:
        print("lag")
    reDraw()
    
