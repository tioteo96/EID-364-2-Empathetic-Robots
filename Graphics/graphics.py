import pygame
from random import randint

pygame.init()

BGs = [pygame.image.load('blueprint/B1_white.jpg'), pygame.image.load('blueprint/B2_white.jpg'),
       pygame.image.load('blueprint/1_white.jpg'), pygame.image.load('blueprint/2_white.jpg'),
       pygame.image.load('blueprint/3_white.jpg'), pygame.image.load('blueprint/4_white.jpg'),
       pygame.image.load('blueprint/5_white.jpg'), pygame.image.load('blueprint/6_white.jpg'),
       pygame.image.load('blueprint/7_white.jpg'), pygame.image.load('blueprint/8_white.jpg'),
       pygame.image.load('blueprint/9_white.jpg'), ]

clock = pygame.time.Clock()


class blueprint(object):
    def __init__(self, FLOOR):
        if FLOOR > 0:
            self.floor = FLOOR + 1
        elif FLOOR < 0:
            self.floor = FLOOR + 2

    def find_size(self, FLOOR):
        BP_SIZE = BGs[FLOOR].get_size()
        div_num = 2
        BP_SIZE = (BP_SIZE[0] // div_num, BP_SIZE[1] // div_num)

        return FLOOR, BP_SIZE


class User(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 1
        self.vel = 1
        self.isNew = False
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.path = [(x, y)]

    def track(self, KEYS, BP_SIZE):
        if KEYS[pygame.K_LEFT] and self.x > self.vel + self.radius:
            self.x -= self.vel
        if KEYS[pygame.K_RIGHT] and self.x < BP_SIZE[0] - self.radius:
            self.x += self.vel
        if KEYS[pygame.K_UP] and self.y > self.vel + self.radius:
            self.y -= self.vel
        if KEYS[pygame.K_DOWN] and self.y < BP_SIZE[1] - self.radius:
            self.y += self.vel

        self.path.append((self.x, self.y))

    def draw(self, WIN, BG, isLIVE):
        if isLIVE:
            pygame.draw.circle(WIN, self.color, self.path[-1], self.radius * 2)
        else:
            for trace in self.path:
                pygame.draw.circle(WIN, self.color, trace, self.radius)


def initialize(FLOOR, BP_SIZE):
    WIN = pygame.display.set_mode(BP_SIZE)
    BG = pygame.transform.scale(BGs[FLOOR], BP_SIZE)
    WIN.blit(BG, (0, 0))
    pygame.display.set_caption("first test")
    return WIN, BG


def redraw():
    win.blit(bg, (0, 0))
    for user in Users:
        user.draw(win, bg, isLive)
    pygame.display.update()


# initial set up
bp = blueprint(1)
floor, bp_size = bp.find_size(bp.floor)
win, bg = initialize(floor, bp_size)

# mainloop
Users = [User(200, 350)]
user_num = 0
isLive = False
run = True
while run:
    # setting fps
    clock.tick(60)
    # closing window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # adding user
    if keys[pygame.K_SPACE]:
        if len(Users) < 5:
            Users.append(User(200, 350))

    # selecting user
    if keys[pygame.K_0]:
        user_num = 0
    elif keys[pygame.K_1]:
        user_num = 1
    elif keys[pygame.K_2]:
        user_num = 2
    elif keys[pygame.K_3]:
        user_num = 3
    elif keys[pygame.K_4]:
        user_num = 4

    # selecting mode (live, history)
    if keys[pygame.K_l]:
        isLive = True
    elif keys[pygame.K_h]:
        isLive = False

    Users[user_num].track(keys, bp_size)

    redraw()

pygame.quit()
