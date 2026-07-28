import pygame, random
from pygame.locals import *



STARTING_FPS = 10
FPS_INCREMENT_FREQUENCY = 180



DIRECTION_UP    = 1
DIRECTON_DOWN   = 2
DIRECTION_LEFT  = 3
DIRECTION_RIGHT = 4


WORLD_SIZE_X = 50
WORLD_SIZE_Y = 50



SNAKE_START_LENGTH = 4
SNAKE_COLOR = ((random.randint(0, 255), random.randint(0, 255), random.randint(0,255)))
FOOD_COLOR = ((random.randint(0, 255), random.randint(0, 255), random.randint(0,255)))
BARRIER_COLOR = (0, 0, 0)


class Snake:


    def __init__(self, x, y, startLength):
        self.startLength = startLength
        self.startX = x
        self.startY = y
        self.reset()

    def reset(self):
        self.pieces = []
        self.direction = 1

        for n in range(0, self.startLength):
            self.pieces.append((self.startX, self.startY + n))

    def changeDirection(self, direction):

        if self.direction == 1 and direction == 2: return
        if self.direction == 2 and direction == 1: return
        if self.direction == 3 and direction == 4: return
        if self.direction == 4 and direction == 3: return

        self.direction = direction

    def getHead(self):
        return self.pieces[0]

    def getTail(self):
        return self.pieces[len(self.pieces) - 1]

    def update(self):
        (headX, headY) = self.getHead()
        head = ()

        if self.direction == 1: head = (headX, headY - 1)
        elif self.direction == 2: head = (headX, headY + 1)
        elif self.direction == 3: head = (headX - 1, headY)
        elif self.direction == 4: head = (headX + 1, headY)

        self.pieces.insert(0, head)
        self.pieces.pop()

    def grow(self):
        (tx, ty) = self.getTail()
        piece = ()

        if self.direction == 1: piece = (tx, ty + 1)
        elif self.direction == 2: piece = (tx, ty - 1)
        elif self.direction == 3: piece = (tx + 1, ty)
        elif self.direction == 4: piece = (tx - 1, ty)

        self.pieces.append(piece)

    def collidesWithSelf(self):
        return len([p for p in self.pieces if p == self.getHead()]) > 1



class SnakeGame:

    def __init__(self, window, screen, clock, font):
        self.window = window
        self.screen = screen
        self.clock = clock
        self.font = font

        self.fps = STARTING_FPS
        self.ticks = 0
        self.playing = True
        self.score = 0

        self.nextDirection = DIRECTION_UP
        self.sizeX = WORLD_SIZE_X
        self.sizeY = WORLD_SIZE_Y
        self.food = []
        self.snake = Snake(WORLD_SIZE_X / 2, WORLD_SIZE_Y / 2, SNAKE_START_LENGTH)
        self.barrier = []

        self.addFood()
        self.addBarrier()

    def getFoodPos(self):
        return self.food[0]


    def addFood(self):
        fx = None
        fy = None

        while fx is None or fy is None or (fx, fy) in self.food:
            fx = random.randint(1, self.sizeX)
            fy = random.randint(1, self.sizeY)
        
        self.food.append((fx, fy))

    def addBarrier(self):
        fx = None
        fy = None

        while fx is None or fy is None or (fx, fy) in self.barrier:
            fx = random.randint(1, self.sizeX)
            fy = random.randint(1, self.sizeY)

        self.barrier.append((fx,fy))

    def input(self, events):
        for e in events:
            if e.type == QUIT:
                return False

            elif e.type == KEYDOWN:
                if   e.key == K_UP: self.nextDirection = 1
                elif e.key == K_DOWN: self.nextDirection = 2
                elif e.key == K_LEFT: self.nextDirection = 3
                elif e.key == K_RIGHT: self.nextDirection = 4
                elif e.key == K_ESCAPE: return False
                elif e.key == K_SPACE and not self.playing: 
                    self.reset()
                
        return True

    def update(self):
        self.snake.changeDirection(self.nextDirection)
        self.snake.update()

        # for barrier in self.barrier:
        #     if self.food.getFoodPos() == barrier:
        #         self.food.remove(food)
        #         self.addFood()

        for food in self.food: 
            if self.snake.getHead() == food:
                self.food.remove(food)
                self.addFood()
                self.snake.grow()
                self.score += len(self.snake.pieces) * 50
                if self.score%100 == 0:
                    self.addBarrier()
                

        for barrier in self.barrier:
            if self.snake.getHead() == barrier:
                self.playing = False

        # (bx, by) = self.food.getFoodPos()
        (hx, hy) = self.snake.getHead()
        if self.snake.collidesWithSelf() or hx < 1 or hy < 1 or hx > self.sizeX or hy > self.sizeY:
            self.playing = False

    def reset(self):
        self.playing = True
        self.nextDirection = DIRECTION_UP
        self.fps = STARTING_FPS
        self.score = 0
        self.snake.reset()
        self.barrier = [] 
        self.addBarrier()


    def draw(self):
        # self.screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0,255)))
        self.screen.fill((150, 150, 150))

        (width, height) = self.window.get_size()
        blockWidth = int(width / self.sizeX)
        blockHeight = int(height / self.sizeY)

        for (px, py) in self.snake.pieces: 
            pygame.draw.rect(self.screen, SNAKE_COLOR, (blockWidth * (px-1), blockHeight * (py-1), blockWidth, blockHeight))

        for (fx, fy) in self.food:
            pygame.draw.rect(self.screen, FOOD_COLOR, (blockWidth * (fx-1), blockHeight * (fy-1), blockWidth, blockHeight))

        for (fx, fy) in self.barrier:
            pygame.draw.rect(self.screen, BARRIER_COLOR, (blockWidth * (fx-1), blockHeight * (fy-1), blockWidth, blockHeight))

        pygame.display.flip()


    def drawDeath(self):
        self.screen.fill((255, 0, 0))
        self.screen.blit(self.font.render("Game over! Press Space to start a new game", 1, (255, 255, 255)), (137, 150))
        self.screen.blit(self.font.render("Your score is: %d" % self.score, 1, (255, 255, 255)), (275, 180))
        pygame.display.flip()

    def drawStart(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.font.render("Welcome to snake, collect the food and avoid", 1, (255, 255, 255)), (137, 150))
        self.screen.blit(self.font.render("the black barriers!", 1, (255, 255, 255)), (275, 180))

    def run(self, events):
        if not self.input(events): return False


        # if self.start:
        if self.playing: 
            self.update()
            self.draw()
        else: self.drawDeath()

        self.clock.tick(self.fps)

        self.ticks += 1
        if self.ticks % FPS_INCREMENT_FREQUENCY == 0: self.fps += 1

        return True