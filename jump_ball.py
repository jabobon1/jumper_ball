import pygame
import random
import os
import sys
import pygame.key

pygame.font.init()  # init font

WIN_WIDTH = 500
WIN_HEIGHT = 800

BALL_IMG = pygame.image.load(os.path.join('imgs', 'ball.png'))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))

STAT_FONT = pygame.font.SysFont('comicsans', 50)


class Ball:
    IMG = BALL_IMG

    def __init__(self, x, y):
        self.img = self.IMG

        self.x = x
        self.y = y
        self.tick_count = 0
        self.vel = 0
        # Force of jump
        self.force = -10
        # Speed for X direction
        self.speed = 7

    def jump(self, floor=668):
        # Allow jump only when ball near to the ground
        if self.y > floor - 10:
            self.vel = self.force
            # Back force to normal consist
            self.force = -10
            self.tick_count = 0

    def force_jump(self, key):
        # Increasing the power of jump while 'space' is pressed
        if key[pygame.K_SPACE]:
            self.force -= 2

    def move(self, floor):
        self.floor = floor

        self.tick_count += 1

        # Free fall rate
        self.free_speed = round(self.vel + 10 * (self.tick_count / 10), 2)

        # print('floor {}, d {}, free_speed {}'.format(floor, self.free_speed, self.free_speed))

        # check if ball in the air
        if self.y + self.free_speed < self.floor:
            self.y += self.free_speed


        # Stop ball in the ground
        elif self.y + self.free_speed >= self.floor and abs(self.free_speed) < 2:
            self.y = self.floor
            self.vel = 0
            self.tick_count = 0


        # rebound ball
        elif self.y + self.free_speed > self.floor:
            self.y = self.floor
            self.tick_count = 2
            self.vel = (self.free_speed * (-1)) * 0.7

    def walk(self, key):
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            if self.x > 2:
                self.x -= self.speed
            elif self.x <= 2:
                self.x += round(self.speed / 4)
        elif key[pygame.K_RIGHT] or key[pygame.K_d]:
            if self.x < WIN_WIDTH - self.IMG.get_width():
                self.x += self.speed
            elif self.x >= WIN_WIDTH - self.IMG.get_width() - 1:
                self.x -= round(self.speed / 4)

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


def draw_window(win, ball, score, pipes, free_speed):
    win.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(win)
    text = STAT_FONT.render('Height: ' + str(score), 1, (255, 255, 255))
    speed = STAT_FONT.render('Speed: ' + str(free_speed), 1, (255, 255, 255))

    win.blit(speed, (5, 10))

    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    win.blit(BASE_IMG, (0, 730))

    ball.draw(win)
    pygame.display.update()


class Pipe:

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(450, 700)
        self.bottom = self.height

    def draw(self, win):
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, ball):
        ball_mask = ball.get_mask()
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        bottom_offset = (self.x - ball.x, self.bottom - round(ball.y))

        b_point = ball_mask.overlap(bottom_mask, bottom_offset)
        if b_point:
            # print('bottom {}, ball.y {}'.format(self.bottom - BALL_IMG.get_height(), round(ball.y)))
            return self.bottom - BALL_IMG.get_height() + 1
        return False


def main():
    ball = Ball(120, 668)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    pipes = [Pipe(350), Pipe(100)]
    floor = 668
    run = True
    while run:
        clock.tick(35)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:

                if event.key == pygame.K_SPACE:
                    ball.jump(floor)
        floor = 668
        # Change value of Y ground if ball above any of pipes
        for pipe in pipes:
            x_check = ball.x + (ball.IMG.get_width() / 2) in range(pipe.x, pipe.x + PIPE_IMG.get_width() + 1)
            y_check = round(ball.y) - 1 <= pipe.bottom - BALL_IMG.get_height()
            if x_check and y_check:
                floor = pipe.bottom - BALL_IMG.get_height() + 1


        keys = pygame.key.get_pressed()
        ball.walk(keys)
        ball.force_jump(keys)
        ball.move(floor)
        score = round(abs(ball.y - 668))
        free_speed = round(abs(ball.free_speed))
        draw_window(win, ball, score=score, pipes=pipes, free_speed=free_speed)

    pygame.quit()
    sys.exit()


main()
