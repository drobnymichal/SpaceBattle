import pygame
from random import randint

DOWN = 1
UP = -1
LEFT = -1
RIGHT = 1

PLAYER = "PLAYER"
BOSS = "UFO"

SCREENSIZE = [720, 720]

class Laser:
    def __init__(self, x_axis, y_axis, speed, direction, path) -> None:
        self.size = (30, 30)
        self.image = pygame.transform.scale(pygame.image.load(path), self.size)
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_axis, self.y_axis)
        self.direction = direction
        self.speed = speed
        
    def updatePos(self) -> bool:
        if not 0 <= self.y_axis <= SCREENSIZE[1]:
            return False
        self.y_axis += int(self.speed) * self.direction
        self.rect.center = (self.x_axis, self.y_axis)
        return True


class Player:
    def __init__(self) -> None:
        self.size = (100, 100)
        self.image = pygame.transform.scale(pygame.image.load("images/spaceship.png"), self.size)
        self.x_axis = SCREENSIZE[0] // 2
        self.y_axis = SCREENSIZE[1] - 50

        self.rect = self.image.get_rect()
        self.rect.center = (self.x_axis, self.y_axis)
        self.lasers = []
        self.healths = 100

    def updatePos(self):
        self.rect.center = (self.x_axis, self.y_axis)

    def changeBossPos(self, direction):
        if (direction == LEFT and self.size[0] // 2 > self.x_axis) or (direction == RIGHT and self.x_axis > SCREENSIZE[0] - self.size[0] // 2):
            return

        self.x_axis += (direction) * 3
        self.updatePos()
    
    def createLaser(self):
        self.lasers.append(Laser(self.x_axis, self.y_axis, 2, UP, "images/bullet.png"))

    def updateLasers(self):
        new = []
        for laser in self.lasers:
            if laser.updatePos():
                new.append(laser)
        self.lasers = new

    def checkColisions(self, lasers):
        new = []
        for laser in lasers:
            if laser.rect.colliderect(self.rect):
                self.healths -= 20
                print(self.healths)
            else:
                new.append(laser)
        return new



class Boss:
    def __init__(self) -> None:
        self.size = (100, 75)
        self.image = pygame.transform.scale(pygame.image.load("images/ufo.png"), self.size)
        self.x_axis = SCREENSIZE[0] // 2
        self.y_axis = 50

        self.rect = self.image.get_rect()
        self.rect.center = (self.x_axis, self.y_axis)
        self.move = 1
        self.lasers = []
        self.healths = 100

    def updatePos(self):
        self.rect.center = (self.x_axis, self.y_axis)

    def changeBossPos(self):
        if not 0 + self.size[0] // 2 < self.x_axis < SCREENSIZE[0] - self.size[0] // 2:
            self.move *= (-1)
        self.x_axis += self.move
        self.updatePos()
    
    def createLaser(self):
        self.lasers.append(Laser(self.x_axis, self.y_axis, randint(1, 3), DOWN, "images/laser.png"))

    def updateLasers(self):
        new = []
        for laser in self.lasers:
            if laser.updatePos():
                new.append(laser)
        self.lasers = new

    def checkColisions(self, lasers):
        new = []
        for laser in lasers:
            if laser.rect.colliderect(self.rect):
                self.healths -= 20
                print(self.healths)
            else:
                new.append(laser)
        return new
            



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (30,144,255)
GREY = (169,169,169)


class GameScreen:

    def mainLoop(self, screen, clock):

        player = Player()
        boss = Boss()
        playerBlaster = 0
        endScreen = False

        end = False

        while not end:
            
            if playerBlaster < 60:
                playerBlaster += 1

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.changeBossPos(LEFT)
            elif keys[pygame.K_RIGHT]:
                player.changeBossPos(RIGHT)
                

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and playerBlaster == 60:
                        player.createLaser()
                        playerBlaster = 0
            
            if endScreen:
                font = pygame.font.SysFont('arial', 80)
                text = font.render("THE END", True, WHITE)
                screen.blit(text, (SCREENSIZE[0] // 2 - 140, SCREENSIZE[1] // 2))
                clock.tick(60)
                pygame.display.flip()
                continue


            screen.fill(BLACK)
            boss.changeBossPos()
            boss.updateLasers()

            if randint(1, 60) == 1:
                boss.createLaser()

            player.updateLasers()
            
            boss.lasers = player.checkColisions(boss.lasers)

            player.lasers = boss.checkColisions(player.lasers)

            if player.healths <= 0:
                return BOSS

            if boss.healths <= 0:
                return PLAYER

            for laser in player.lasers:
                screen.blit(laser.image, laser.rect)

            for laser in boss.lasers:
                screen.blit(laser.image, laser.rect)
            
            pygame.draw.rect(screen, RED, [10, 100, 10, 100 - boss.healths])
            pygame.draw.rect(screen, GREEN, [10, 100 + 100 - boss.healths, 10, boss.healths])

            pygame.draw.rect(screen, RED, [SCREENSIZE[0] - 20, SCREENSIZE[1] - 200, 10, 100 - player.healths])
            pygame.draw.rect(screen, GREEN, [SCREENSIZE[0] - 20, SCREENSIZE[1] - 200 + 100 - player.healths, 10, player.healths])

            screen.blit(player.image, player.rect)
            screen.blit(boss.image, boss.rect)
            clock.tick(60)
            pygame.display.flip()
        return False


class EndScreen:
    def mainLoop(self, screen, clock, winner) -> bool:
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return True

            font = pygame.font.SysFont('arial', 50)
            text = font.render("THE WINNER IS " + winner, True, WHITE)
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            clock.tick(60)

            text = font.render("PRESS R FOR NEW GAME", True, WHITE)
            ff = screen.get_rect().center
            screen.blit(text, text.get_rect(center = (ff[0], ff[1] + 100)))
            clock.tick(60)
            pygame.display.flip()
        
        
            


def mainLoop():
    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption("SPACE BATTLE")
    clock = pygame.time.Clock()

    run = True
    while run:
        winner = GameScreen().mainLoop(screen, clock)
        
        if winner is None:
            pygame.quit
            return None

        run = EndScreen().mainLoop(screen, clock, winner)
    
    pygame.quit
    





mainLoop()
