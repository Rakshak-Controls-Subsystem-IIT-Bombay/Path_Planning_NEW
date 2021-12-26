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
# Height is added to the waypoints - Anjali Muthyala


from math import acos, floor, pi

import time
from vpython import *

from CircletraceSolver import Solver

blue = vec(0, 0, 1)
white = vec(1, 1, 1)
black = vec(0, 0, 0)
red = vec(1, 0, 0)
green = vec(0, 1, 0)
cyan = vec(0, 0.706, 0.412)
maroon = vec(0.47, 0.106, 0.027)

obst1 = [325, 300, 50]
obst2 = [435, 300, 25]
obst3 = [575, 250, 50]
obst4 = [600, 400, 45]
obst = [obst1, obst2, obst3, obst4]
path = []
gr = 10  # Grace Radius variables
size = width, height = 900, 600



def init_obstacles():  # Later run in for loop
    for q in obst:
        cylinder(color=green, pos=vector(q[0], q[1], 0), axis=vector(0, 0, 200), radius=q[2]+gr, opacity=0.8)
        cylinder(color=maroon, pos=vector(q[0], q[1], 0), axis=vector(0, 0, 200), radius=q[2])
        q[2] = q[2] + 10


def reset():
    init_obstacles()
    print("resetting")


def dist_between(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5


def dist3d_between(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)**0.5


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
    if len(path) > 2:
        path = optimalheight(path)
    return path


def optimalheight(path):
    abs_dis = []
    temp = 0
    for i in range(len(path)-1):
        temp += dist_between(path[i], path[i+1])
        abs_dis.append(temp)

    h = []
    for j in range(len(path)-2):
        temp = path[0][-1] + (path[-1][-1] - path[0][-1])*abs_dis[j]/abs_dis[-1]
        h.append(temp)

    new_path = addheight(path, h)
    return new_path


def addheight(path, h):
    new_path = [0]*len(path)
    new_path[0] = path[0]
    for i in range(1, len(h)+1):
        temp = list(path[i])
        temp.append(h[i-1])
        new_path[i] = tuple(temp)
    new_path[-1] = path[-1]
    return new_path


goalset = 0
destiny = []
n = int(input("Enter the number of waypoints to visit:"))
screen = canvas(width=1000, height=600)
screen.camera.pos = vector(450, 900, 400)
# screen.center = vector(450, 300, 0)
screen.camera.axis = vector(0, -600, -400)
screen.up = vector(1, -400, 600)

box(pos=vector(450, 300, 0), size=vector(900, 600, 0.1), color=color.white)
init_obstacles()

# Example waypoints for input
# (226, 288, 10)
# (390, 341, 70)
# (641, 223, 100)
# (687, 469, 50)

while True:
    while goalset < n:
        print("Enter the coordinates of the waypoints:")
        arr = input()
        position = tuple(map(float, arr.split(" ")))
        pos_vec = vector(position[0], position[1], position[2])
        # print(position)
        destiny.append(position)

        if goalset == 0:
            start = position

        sphere(color=red, pos=vector(pos_vec), radius=6)
        goalset += 1


    T = time.time()
    v0 = 20
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
                NextPoint = [path[1][0], path[1][1], path[1][2]]
                # print("path", path)

            # for i in range(len(path)-1):
            #     curve(vector(path[i][0], path[i][1], path[i][2]),
            #           vector(path[i + 1][0], path[i + 1][1], path[i + 1][2]), color=cyan, radius=1)

        FirstPoint = [destiny[0][0], destiny[0][1], destiny[0][2]]
        dis = dist3d_between(FirstPoint, NextPoint)
        m = [NextPoint[0]-FirstPoint[0], NextPoint[1]-FirstPoint[1], NextPoint[2]-FirstPoint[2]]

        s = v0*delT
        dList = [s*m[0]/dis, s*m[1]/dis, s*m[2]/dis]

        # print('x', dList, FirstPoint, NextPoint)

        destiny[0] = [FirstPoint[0] + dList[0], FirstPoint[1] + dList[1], FirstPoint[2] + dList[2]]
        print(destiny[0])

        if dist3d_between(destiny[0], destiny[1]) < 5.0:
            destiny[0] = destiny[1]
            destiny.pop(1)
            p -= 1

        NewStartPos = vec(destiny[0][0], destiny[0][1], destiny[0][2])
        # print(NewStartPos)
        sphere(color=red, pos=vector(NewStartPos), radius=2)

        if p < 2:
            break

    goalset = 0
    destiny = []
    print("Destination Arrived")
