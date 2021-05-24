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
import sys
import pygame
import time
import random
import json
import requests
import socket

from CircletraceSolver import Solver

blue = 0, 0, 255
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
cyan = 0, 180, 105
maroon = 119, 27, 7

obst = []
path = []
destiny = []
gr = 10  # Grace Radius variables
#size = width, height = 900, 600
size = width, height = 900, 760


def sp():
    return (random.randint(80, 100))


def pos(m):
    return (random.randint(1, m-1))


def init_obstacles():  # Later run in for loop
    for q in obst:
        pygame.draw.circle(screen, green, q[0:2], q[2]+gr, 0)
        pygame.draw.circle(screen, maroon, q[0:2], q[2], 0)
        q[2] = q[2] + 10


def dist_between(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5


def OptimisePathDistance(ipos, destiny):
    finaldestiny = [ipos]
    while(len(destiny) > 0):
        pygame.display.update()
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
        pygame.display.update()
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
        pygame.display.update()
        if(f(o[0], o[1], s[0], s[1], e[0], e[1]) == False):
            # print(o, "NOT OBSTACLE")
            k = 2
        else:
            distance = ((e[1]-s[1])*o[0] - (e[0]-s[0])*o[1] +
                        e[0]*s[1] - e[1]*s[0])/dist_between(s, e)
            if(abs(distance) < o[2]):
                # print(o, "As OBSTACLE")
                trouble.append(o)
    return trouble


def lastpt(path, obstacles, start):
    for i in path[::-1]:
        pygame.display.update()
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
        pygame.display.update()
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
            pygame.display.update()
            dangle = floor(acos((i[2] - gr)/i[2])*180/pi)
            temp = sol.Solver(i, path[-1], end, dangle)
            path = path + temp
    path.append(end)
    path = refine(path, obstacles)
    if len(obstacles) == 0:
        path.append(end)
    return path


def reset():
    global obst, path, destiny, screen
    # obst1 = [325, 300, 50]
    # obst2 = [435, 300, 25]
    # obst3 = [575, 250, 50]
    # obst4 = [600, 400, 45]
    # obst = [obst1, obst2, obst3, obst4]
    IPaddress = socket.gethostbyname(socket.gethostname())
    if IPaddress == "127.0.0.1":
        print("No internet, your localhost is " + IPaddress)
        print("########* CONNECT TO INTERNET *#########")
    while True:
        if not socket.gethostbyname(socket.gethostname()) == "127.0.0.1":
            break
    ###
    print("GETTING DATA FROM THE JSON FILE ON GITHUB")
    url = "https://raw.githubusercontent.com/Rakshak-Controls-Subsystem-IIT-Bombay/Communication-with-Server/master/toXYconverted.json"
    request = requests.get(url)
    request_text = request.text

    data = json.loads(request_text)
    # print(data)

    Stat_Obs = data['stationaryObstacles']

    obst = []
    for Obs in Stat_Obs:
        temp = [None, None, None, None]
        temp[0] = int(Obs['x'])/1.5
        temp[1] = int(Obs['y'])/1.5
        temp[2] = int(Obs['radius'])/4
        temp[3] = int(Obs['height'])
        obst.append(temp)

    ###
    way = data['waypoints']

    destiny = []
    for W in way:
        temp = [None, None]
        temp[0] = int(W['x'])/1.6
        temp[1] = int(W['y'])/1.6
        #temp[2] = int(W['altitude'])
        destiny.append(temp)

    ###
    path = []

    screen = pygame.display.set_mode(size)
    screen.fill((240, 240, 0))
    init_obstacles()
    pygame.display.update()


def obstacleWaypoints_Path(Point1, m):
    obsWaypoint = []
    while(not len(obsWaypoint) == m):
        x = pos(width)
        y = pos(height)
        obsWaypoint.append([x, y])
        for i in obst:
            if not dist_between([x, y], [i[0], i[1]]) > i[2]:
                obsWaypoint.pop(-1)
                break

    Obst_start = obsWaypoint[0]
    for i in obsWaypoint:
        if i[0]**2+i[1]**2 < Obst_start[0]**2+Obst_start[1]**2:
            Obst_start = i
        pygame.draw.circle(screen, blue, i, 6, 0)
    pygame.display.update()

    if not Point1 == "null":
        Obst_start = Point1
        obsWaypoint.insert(0, Point1)
    obsWaypoint = OptimisePathDistance(Obst_start, obsWaypoint[0:n])
    obsWaypoint.pop(0)

    obsPath = [obsWaypoint[0], [0, 0]]
    for i in range(0, len(obsWaypoint)-1):
        path = findpath(obsWaypoint[i], obsWaypoint[i+1])
        obsPath.pop(-1)
        if path[0] == obsPath[-1]:
            path.pop(0)
        for j in path:
            obsPath.append([j[0], j[1]])

    if obsPath[-1] == obsPath[-2]:
        obsPath.pop(-1)
    print("obsPath", obsPath)
    return obsPath


#n = int(input("Enter the number of waypoints to visit:"))
reset()
n = len(destiny)

goalset = 0
while True:
    # MODIFICATIONS STARTS FROM HERE
    obsPath = obstacleWaypoints_Path("null", 3)

    for position in destiny:
        pygame.draw.circle(screen, red, position, 6, 0)
        pygame.display.update()

    # while goalset < n:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             position = event.pos
    #             print(position)
    #             destiny.append(position)
    #             if goalset == 0:
    #                 start = position
    #             pygame.draw.circle(screen, red, position, 6, 0)
    #             pygame.display.update()
    #             goalset += 1

    T = time.time()
    # change speed to experiment
    v0 = 50
    p = n
    NextPoint = []

    DynObst_radius = 6
    DynObst = obsPath[0]
    DynObst_temp = [DynObst[0], DynObst[1], DynObst_radius]
    DynObst_speed = 50
    obst.append(DynObst_temp)

    while True:
        time.sleep(0.0)

        k = time.time()
        delT = k-T
        T = k

        # DYNAMIC OBSTACLE POSITION UPDATE
        if DynObst == obsPath[0] or dist_between(DynObst, obsPath[0]) < 5.0:
            DynObst = obsPath[0]
            obsPath.pop(0)
            if len(obsPath) == 0:
                obsPath = obstacleWaypoints_Path(DynObst, 3)
                obsPath.pop(0)
        else:
            dis = dist_between(DynObst, obsPath[0])
            obsDirection = [(obsPath[0][0]-DynObst[0])/dis,
                            (obsPath[0][1]-DynObst[1])/dis]
            DynObst[0] = DynObst[0] + DynObst_speed*delT*obsDirection[0]
            DynObst[1] = DynObst[1] + DynObst_speed*delT*obsDirection[1]

        obst[len(obst)-1] = [int(DynObst[0]), int(DynObst[1]), DynObst_radius]
        pygame.draw.circle(
            screen, blue, [int(DynObst[0]), int(DynObst[1])], 2, 0)
        pygame.display.update()
        pygame.display.update()
        print("DynObst", DynObst)
        # UAV POSITION UPDATE
        destiny = OptimisePathDistance(destiny[0], destiny[1:p])

        for i in range(0, len(destiny)-1):
            path = findpath(destiny[i], destiny[i+1])
            if i == 0:
                NextPoint = [path[1][0], path[1][1]]
                print("path", path)

            for i in range(len(path)-1):
                pygame.draw.line(screen, cyan, path[i], path[i+1])
                pygame.display.update()
                pygame.display.update()

        FirstPoint = [destiny[0][0], destiny[0][1]]
        dis = dist_between(FirstPoint, NextPoint)
        m = [NextPoint[0]-FirstPoint[0], NextPoint[1]-FirstPoint[1]]

        s = v0*delT
        dList = [s*m[0]/dis, s*m[1]/dis]

        print('x', dList, FirstPoint, NextPoint)

        destiny[0] = [FirstPoint[0] + dList[0], FirstPoint[1] + dList[1]]
        print("UAVPos", destiny[0])

        if dist_between(destiny[0], destiny[1]) < 5.0:
            destiny[0] = destiny[1]
            destiny.pop(1)
            p -= 1

        IntegerPostion = [int(i) for i in destiny[0]]
        print("UAVIntPos", IntegerPostion)
        pygame.draw.circle(screen, red, IntegerPostion, 2, 0)
        pygame.display.update()
        pygame.display.update()
        # for _ in range(20):
        #     pygame.display.update()

        if p < 2:
            break

    goalset = 0
    destiny = []
    print("Destination Arrived")

    # FOR RESETTING THE WHOLE GAME
    flag = True
    while(flag):
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                flag = False
    reset()
