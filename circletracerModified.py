# Algorithm
# Accept all points and obstacles
# Start with first point..
# Check if path from first point to second lies through any circle(obstacle)
# if not go straight
# else
#   Make a list of obstacles..
#   go to intersection of first obst and line
#   grace circle until second intersection point
#   go straight again until next circle and line intersection (repeat from 6)
# (You must get till end by this and repeat this for all start-end pairs)

from math import acos, floor, pi

import pygame
from pygame import *
import time

from CircletraceSolver import Solver

blue = 0, 0, 255
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
cyan = 0, 180, 105
maroon = 119, 27, 7

obst1 = [325, 300, 50]
obst2 = [435, 300, 25]
obst3 = [575, 250, 50]
obst4 = [600, 400, 45]
obst = [obst1, obst2, obst3, obst4]
path = []
gr = 10  # Grace Radius variables
size = width, height = 900, 600


def sp():
    return (random.randint(1, 4))


def pos(m):
    return (random.randint(1, m-1))


def ballPositon(n):
    obs = [None]*n
    speed = [None]*n

    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Moving obstracle")

    # print(ball)

    # assigning random values for obs and speed
    for i in range(n):
        #obs[i] = pygame.transform.scale(ball, (ball.get_width(), ball.get_height())).get_rect()
        obs[i] = ball.get_rect()
        obs[i].center = pos(width), pos(height)
        speed[i] = [sp(), sp()]


def init_obstacles():  # Later run in for loop
    for q in obst:
        pygame.draw.circle(screen, green, q[0:2], q[2]+gr, 0)
        pygame.draw.circle(screen, maroon, q[0:2], q[2], 0)
        q[2] = q[2] + 10


def reset():
    screen.fill((240, 240, 0))
    init_obstacles()
    pygame.display.update()
    print("resetting")


def dist_between(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5


def OptimisePathDistance(ipos, destiny):
    finaldestiny = [ipos]
    while(len(destiny) > 0):
        dist_row = []
        for i in destiny:
            dist_row.append(dist_between(i, finaldestiny[-1]))
        mini = sorted(dist_row)
        nearwaypt = destiny[dist_row.index(mini[0])]
        finaldestiny.append(nearwaypt)
        # now remove nearwaypt from destiny
        destiny.remove(nearwaypt)
    return finaldestiny


def sortedobstacles(obstacles, start):
    distances = []
    for o in obstacles:
        d = dist_between(o, start)
        distances.append(d)
    distances1 = sorted(distances)
    sl = []
    for i in range(0, len(obstacles)):
        sl.append(obstacles[distances.index(distances1[i])])
    return sl


def f(p, q, x1, y1, x2, y2):  # Tells whether this is a obstacle or not
    t = ((y1-q)*(y2-y1)+(x2-x1)*(x1-p))*((y2-q)*(y2-y1)+(x2-x1)*(x2-p))
    if t < 0:
        return True
    else:
        return False


def inmypath(obst, s, e):
    trouble = []
    for o in obst:
        if(f(o[0], o[1], s[0], s[1], e[0], e[1]) == False):
            #print(o, "NOT OBSTACLE")
            k = 2
        else:
            distance = ((e[1]-s[1])*o[0] - (e[0]-s[0])*o[1] +
                        e[0]*s[1] - e[1]*s[0])/dist_between(s, e)
            if(abs(distance) < o[2]):
                #print(o, "As OBSTACLE")
                trouble.append(o)
    return trouble


def lastpt(path, obstacles, start):
    for i in path[::-1]:
        thisisgood = True
        obst = inmypath(obstacles, start, i)
        for j in obstacles:
            if j in obst:
                thisisgood = False
                break
        if thisisgood:
            return i


def refine(path, obstacles):
    refinedpath = [path[0]]
    startpt = path[0]
    startptidx = 0
    while(startpt is not path[-1]):
        lastpoint = lastpt(path[startptidx:], obstacles, refinedpath[-1])
        refinedpath.append(lastpoint)
        startpt = lastpoint
        startptidx = path.index(startpt)
    return refinedpath


def findpath(start, end):
    global obst, gr
    sol = Solver()
    obstacles = inmypath(obst, start, end)
    path = [start]
    if len(obstacles) > 0:
        obstacles = sortedobstacles(obstacles, start)
        for i in obstacles:
            dangle = floor(acos((i[2] - gr)/i[2])*180/pi)
            temp = sol.Solver(i, path[-1], end, dangle)
            path = path + temp
    path.append(end)
    path = refine(path, obstacles)
    if len(obstacles) == 0:
        path.append(end)
    return path


n = int(input("Enter the number of waypoints to visit:"))
screen = pygame.display.set_mode(size)
screen.fill((240, 240, 0))
init_obstacles()
pygame.display.update()

goalset = 0
destiny = []


while True:
    while goalset < n:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                print(position)
                destiny.append(position)

                if goalset == 0:
                    start = position

                pygame.draw.circle(screen, red, position, 6, 0)
                pygame.display.update()
                goalset += 1

            if event.type == pygame.QUIT:
                pygame.quit()

    T = time.time()
    v0 = 100
    p = n
    NextPoint = []
    while True:
        time.sleep(0.0)
        k = time.time()

        delT = k-T
        T = k

        destiny = OptimisePathDistance(destiny[0], destiny[1:p])

        for i in range(0, len(destiny)-1):
            path = findpath(destiny[i], destiny[i+1])
            if i == 0:
                NextPoint = [path[1][0], path[1][1]]
                print("path", path)

            for i in range(len(path)-1):
                pygame.draw.line(screen, cyan, path[i], path[i+1])
                pygame.display.update()

        FirstPoint = [destiny[0][0], destiny[0][1]]
        dis = dist_between(FirstPoint, NextPoint)
        m = [NextPoint[0]-FirstPoint[0], NextPoint[1]-FirstPoint[1]]

        s = v0*delT
        dList = [s*m[0]/dis, s*m[1]/dis]

        print('x', dList, FirstPoint, NextPoint)

        destiny[0] = [FirstPoint[0] + dList[0], FirstPoint[1] + dList[1]]
        print(destiny[0])

        if dist_between(destiny[0], destiny[1]) < 2.0:
            destiny[0] = destiny[1]
            destiny.pop(1)
            p -= 1

        NewStartPos = [int(i) for i in destiny[0]]
        print(NewStartPos)
        pygame.draw.circle(screen, red, NewStartPos, 2, 0)
        # pygame.display.flip()
        pygame.display.update()

        if p < 2:
            break

    goalset = 0
    destiny = []
    print("Destination Arrived")
