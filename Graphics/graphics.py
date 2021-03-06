import pygame
import time
import glob
from datetime import datetime
import os
from random import randint


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


class Room(object):
    def __init__(self, x, y, x_len, y_len, roomname):
        self.x = x
        self.y = y
        self.x_len = x_len
        self.y_len = y_len
        self.rect = pygame.Rect(x, y, x_len, y_len)
        self.name = roomname
        self.occupied = False

    def draw(self, WIN):
        pygame.draw.rect(win, (0, 0, 255), self.rect, 1)


class Room_template(object):
    def __init__(self):
        self.x = 200
        self.y = 330
        self.x_len = 150
        self.y_len = 70
        self.rect = pygame.Rect(self.x, self.y, self.x_len, self.y_len)
        self.vel = 1
        self.visible = False
        self.ticker = 0

    def draw(self, WIN):
        if self.visible:
            pygame.draw.rect(win, (0, 255, 255), self.rect)

    def change_meas(self, KEYS):
        if KEYS[pygame.K_KP4]:
            if KEYS[pygame.K_KP0]:
                self.x_len -= self.vel
            else:
                self.x -= self.vel
        if KEYS[pygame.K_KP6]:
            if KEYS[pygame.K_KP0]:
                self.x_len += self.vel
            else:
                self.x += self.vel
        if KEYS[pygame.K_KP8]:
            if KEYS[pygame.K_KP0]:
                self.y_len -= self.vel
            else:
                self.y -= self.vel
        if KEYS[pygame.K_KP2]:
            if KEYS[pygame.K_KP0]:
                self.y_len += self.vel
            else:
                self.y += self.vel
        if self.ticker == 0:
            if KEYS[pygame.K_KP_MULTIPLY]:
                self.ticker = self.ticker + 1
                if self.visible:
                    self.visible = False
                else:
                    self.visible = True
            if KEYS[pygame.K_KP_ENTER]:
                print('x = {0} \ny = {1} \nx_len = {2} \ny_len = {3}\n\n'.format(self.x, self.y, self.x_len, self.y_len))
                self.ticker += 1
        else:
            self.ticker += 1
            if self.ticker >= 15:
                self.ticker = 0

        self.rect = pygame.Rect(self.x, self.y, self.x_len, self.y_len)


class User(object):
    def __init__(self, x, y, name):
        self.name = name
        self.x = x
        self.y = y
        self.radius = 1
        self.vel = 1
        self.isNew = False
        self.color = (randint(100, 255), randint(100, 255), randint(100, 255))
        self.path = [(x, y)]
        self.textfile = open('%s.txt' % name,"w")

    def in_room(self, room):
        x1, y1, w, h = room.rect
        x2, y2 = x1+w, y1+h
        x = self.x
        y = self.y
        if x1 < x < x2:
            if y1 < y < y2:
                return True
        return False

    def track(self, KEYS, BP_SIZE, rooms):
        for room in rooms:
            if not self.in_room(room):
                if room.occupied:
                    print(self.name + " left room: " + room.name)
                    print('{0}|left|{1}|{2}'.format(self.name,room.name,time.asctime()), file=self.textfile)
                room.occupied = False
            else:

                if not room.occupied:
                    print(self.name + " entered room: " + room.name)
                    print('{0}|entered|{1}|{2}'.format(self.name,room.name,time.asctime()), file=self.textfile)
                room.occupied = True

        changed = False
        if KEYS[pygame.K_LEFT] and self.x > self.vel + self.radius:
            self.x -= self.vel
            changed = True
        if KEYS[pygame.K_RIGHT] and self.x < BP_SIZE[0] - self.radius:
            self.x += self.vel
            changed = True
        if KEYS[pygame.K_UP] and self.y > self.vel + self.radius:
            self.y -= self.vel
            changed = True
        if KEYS[pygame.K_DOWN] and self.y < BP_SIZE[1] - self.radius:
            self.y += self.vel
            changed = True
        if changed:
            self.path.append((self.x, self.y))

    def draw(self, WIN, BG, isLIVE):
        if isLIVE:
            pygame.draw.circle(WIN, self.color, self.path[-1], self.radius * 4)
        else:
            for trace in self.path:
                count = self.path.count(trace)
                newColor = (self.color[0]//count, self.color[1]//count, self.color[2]//count)
                pygame.draw.circle(WIN, newColor, trace, self.radius * 2 * count)


def initialize(FLOOR, BP_SIZE):
    WIN = pygame.display.set_mode(BP_SIZE)
    BG = pygame.transform.scale(BGs[FLOOR], BP_SIZE)
    WIN.blit(BG, (0, 0))
    pygame.display.set_caption("first test")
    return WIN, BG


def redraw(Rooms):
    win.blit(bg, (0, 0))
    for user in Users:
        user.draw(win, bg, isLive)
    for room in Rooms:
        room.draw(win)
    room_temp.draw(win)
    pygame.display.update()


def loadRooms():
    Rooms = []
    with open('Room_info.txt') as f:
        line = f.readline()
        line_num = 1
        while line:
            room_vars = line.split(':')
            if len(room_vars) != 5:
                print("Error: Issue reading room config at line: " + str(line_num))
                pygame.quit()
                exit()
            Rooms.append(Room(int(room_vars[0]), int(room_vars[1]), int(room_vars[2]), int(room_vars[3]),
                              room_vars[4].rstrip("\n")))
            line = f.readline()
            line_num += 1
    return Rooms


def loadData():
    # Load data
    filepath = ".\Person*"
    txt = glob.glob(filepath)
    for textfile in txt:
        if os.stat(textfile).st_size == 0:
            break
        f = open(textfile, 'r')
        line = f.readline()
        while line and line.strip():
            token1 = line.split('|')
            token1[3] = token1[3].rstrip("\n")

            print(token1)

            nextline = f.readline()
            if len(nextline) != 0:
                token2 = nextline.split('|')
                token2[3] = token2[3].rstrip("\n")

                print(token2)

                next = True
            else:
                next = False
                break
            if next:
                if token1[1] != token2[1] and token1[2] == token2[2]:
                    time1 = datetime.strptime(token1[3], '%c')
                    time2 = datetime.strptime(token2[3], '%c')
                    duration = time2 - time1
                    duration_sec = duration.total_seconds()
                    print(duration_sec)
            line = f.readline()


# initial set up
pygame.init()
BGs = [pygame.image.load('blueprint/B1_white.jpg'), pygame.image.load('blueprint/B2_white.jpg'),
       pygame.image.load('blueprint/1_white.jpg'), pygame.image.load('blueprint/2_white.jpg'),
       pygame.image.load('blueprint/3_white.jpg'), pygame.image.load('blueprint/4_white.jpg'),
       pygame.image.load('blueprint/5_white.jpg'), pygame.image.load('blueprint/6_white.jpg'),
       pygame.image.load('blueprint/7_white.jpg'), pygame.image.load('blueprint/8_white.jpg'),
       pygame.image.load('blueprint/9_white.jpg'), ]
clock = pygame.time.Clock()
bp = blueprint(1)
floor, bp_size = bp.find_size(bp.floor)
win, bg = initialize(floor, bp_size)

Rooms = loadRooms()
loadData()


Users = [User(200, 350, "Person1")]
room_temp = Room_template()
user_num = 0
isLive = False
run = True
# mainloop
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
            Users.append(User(200, 350,"Person"+str(len(Users)+1)))

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
        print('Hello World')
    elif keys[pygame.K_h]:
        isLive = False
    room_temp.change_meas(keys)
    Users[user_num].track(keys, bp_size, Rooms)

    redraw(Rooms)

pygame.quit()
