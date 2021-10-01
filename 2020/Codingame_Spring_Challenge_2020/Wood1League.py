import sys
import math
from collections import deque

# Grab the pellets as fast as you can!
from random import randint

SUPERPELLETS_FINISHED: bool = False
TOGGLE_SUPERPELLET: bool = True

class Coordinate:
    def __init__(self, coordinate_x: int, coordinate_y: int):
        self.coordinateX: int = coordinate_x
        self.coordinateY: int = coordinate_y


class Pac:
    def __init__(self, pac_agent_id: int, mine_or_not: bool, pac_coordinate: Coordinate):
        self.pacID: int = pac_agent_id
        self.mineOrNot: bool = mine_or_not
        self.pacCoordinate: Coordinate = pac_coordinate


class Pellet:
    def __init__(self, pellet_coordinate: Coordinate, pellet_value: int):
        self.pelletCoordinate: Coordinate = pellet_coordinate
        self.pelletValue: int = pellet_value  # 1 or 10


class QueueNode:
    def __init__(self, node_coordinate: Coordinate, node_distance: int):
        self.nodeCoordinate: Coordinate = node_coordinate  # The cordinate of the cell
        self.nodeDistance: int = node_distance  # Cell's distance from the source


def isValid(coodinate_to_check: Coordinate, grid_matrix: list):
    return (coodinate_to_check.coordinateX >= 0) and \
           (coodinate_to_check.coordinateX < len(grid_matrix)) and \
           (coodinate_to_check.coordinateY >= 0) and \
           (coodinate_to_check.coordinateY < len(grid_matrix[0]))


def findShortestPathInMaze(grid_matrix: list, start_coord: Coordinate, end_coord: Coordinate):
    # check source and destination cell
    # of the matrix have value 1
    infinity: int = float('inf')
    if not isValid(start_coord, grid_matrix):
        return infinity
    if not isValid(end_coord, grid_matrix):
        return infinity
    if grid_matrix[start_coord.coordinateX][start_coord.coordinateY] != " ":
        return infinity
    if grid_matrix[end_coord.coordinateX][end_coord.coordinateY] != " ":
        return infinity

    visited = [[False for i in range(len(grid_matrix[0]))] for j in range(len(grid_matrix))]

    # Mark the source cell as visited
    visited[start_coord.coordinateX][start_coord.coordinateY] = True

    # Create a queue for BFS
    queueStore = deque()

    # Distance of source cell is 0
    node = QueueNode(start_coord, 0)
    queueStore.append(node)  # Enqueue source cell

    # Do a BFS starting from source cell
    while queueStore:
        sidePointsList = [Coordinate(-1, 0),
                          Coordinate(0, -1),
                          Coordinate(0, 1),
                          Coordinate(1, 0)]

        curr = queueStore.popleft()  # Dequeue the front cell

        # If we have reached the destination cell,
        # we are done
        pt = curr.nodeCoordinate
        if pt.coordinateX == end_coord.coordinateX and pt.coordinateY == end_coord.coordinateY:
            return curr.nodeDistance

            # Otherwise enqueue its adjacent cells
        for sidePoint in sidePointsList:
            pointCoordinate = Coordinate(pt.coordinateX + sidePoint.coordinateX, pt.coordinateY + sidePoint.coordinateY)

            # if adjacent cell is valid, has path
            # and not visited yet, enqueue it.
            if isValid(pointCoordinate, grid_matrix):
                if grid_matrix[pointCoordinate.coordinateX][pointCoordinate.coordinateY] == " ":
                    if not visited[pointCoordinate.coordinateX][pointCoordinate.coordinateY]:
                        visited[pointCoordinate.coordinateX][pointCoordinate.coordinateY] = True
                        Adjcell = QueueNode(pointCoordinate, curr.nodeDistance + 1)
                        queueStore.append(Adjcell)

                # Return infinity if destination cannot be reached
    return infinity


def findNearestPellet(grid_matrix, pellet_list, the_start_coordinate):
    nearestPellet: Pellet = pellet_list[0]
    nearestDistance: int = findShortestPathInMaze(grid_matrix, the_start_coordinate, nearestPellet.pelletCoordinate)
    for pellet in pellet_list[1:-1]:
        thisPelletsDistance = findShortestPathInMaze(grid_matrix, the_start_coordinate, pellet.pelletCoordinate)
        if (thisPelletsDistance < nearestDistance):
            nearestPellet = pellet
            nearestDistance = thisPelletsDistance

    return nearestPellet


def findNearestSuperPellet(grid_matrix, pellet_list, the_start_coordinate):
    supetPelletList: list[Pellet] = []
    for pellet in pellet_list:
        if (pellet.pelletValue == 10):
            supetPelletList.append(pellet)

    return findNearestPellet(grid_matrix, supetPelletList, the_start_coordinate)


def findNearestSuperPelletOrPellet(grid_matrix: list, pellet_list: list, the_start_coordinate: Coordinate):
    global SUPERPELLETS_FINISHED
    if not SUPERPELLETS_FINISHED and TOGGLE_SUPERPELLET:
        supetPelletList: list = []
        for pellet in pellet_list:
            if pellet.pelletValue > 1:
                supetPelletList.append(pellet)

        if len(supetPelletList) > 0:
            return findNearestPellet(grid_matrix, supetPelletList, the_start_coordinate)
        else:
            SUPERPELLETS_FINISHED = True

    radius: int = 1
    searchPelletList: list[Pellet] = []
    while len(searchPelletList) == 0:
        for nearbyPellet in pellet_list:
            if isNearEnough(the_start_coordinate, nearbyPellet.pelletCoordinate, radius):
                searchPelletList.append(nearbyPellet)
        radius = radius + 1

    return findNearestPellet(grid_matrix, searchPelletList, the_start_coordinate)


def isNearEnough(start_coordinate: Coordinate, end_coordinate: Coordinate, distance: int):
    return abs(start_coordinate.coordinateX - end_coordinate.coordinateX) + abs(
        start_coordinate.coordinateY - end_coordinate.coordinateY) < distance


def findMyPac(pacList: list):
    myPacs = []
    for pac in pacList:
        if pac.mineOrNot:
            myPacs.append(pac)
    return myPacs


def findNearestPacEnemy(pacList: list, myPacCoordinates: Coordinate):
    nearestEnemyPac: Pac = Pac(-1, False, Coordinate(-1, -1))
    distance: int = float('inf')
    for pac in pacList:
        if not pac.mineOrNot:
            newDistance = min(distance, abs(myPacCoordinates.coordinateX - pac.pacCoordinate.coordinateX) + abs(
                myPacCoordinates.coordinateY - pac.pacCoordinate.coordinateY))
            if newDistance != distance:
                nearestEnemyPac = pac
    return nearestEnemyPac


def checkEnemyPacPosition(pacList: list, myPacCoordinates: Coordinate):
    for pac in pacList:
        changeX: int = myPacCoordinates.coordinateX - pac.pacCoordinate.coordinateX
        changeY: int = myPacCoordinates.coordinateY - pac.pacCoordinate.coordinateY
        if (abs(changeX) + abs(changeY) == 1 or abs(changeX) + abs(changeY) == 2) and (abs(changeX) == 1 or abs(changeY) == 1):
            return Coordinate(changeX, changeY)
    return Coordinate(2, 2)


def findNearestPossiblePosInDirection(gridMatrix: list, myPacCoordinates: Coordinate,
                                      nearbyEnemyPacCoordinatesDifference: Coordinate):
    if nearbyEnemyPacCoordinatesDifference.coordinateX == 0:
        if isValid(Coordinate(myPacCoordinates.coordinateX,
                              myPacCoordinates.coordinateY + nearbyEnemyPacCoordinatesDifference.coordinateY),
                   gridMatrix) and gridMatrix[myPacCoordinates.coordinateX][
            myPacCoordinates.coordinateY + nearbyEnemyPacCoordinatesDifference.coordinateY] == " ":
            return Coordinate(myPacCoordinates.coordinateX,
                              myPacCoordinates.coordinateY + nearbyEnemyPacCoordinatesDifference.coordinateY)
        if isValid(Coordinate(myPacCoordinates.coordinateX + 1, myPacCoordinates.coordinateY), gridMatrix) and \
                gridMatrix[myPacCoordinates.coordinateX + 1][myPacCoordinates.coordinateY] == " ":
            return Coordinate(myPacCoordinates.coordinateX + 1, myPacCoordinates.coordinateY)
        if isValid(Coordinate(myPacCoordinates.coordinateX - 1, myPacCoordinates.coordinateY), gridMatrix) and \
                gridMatrix[myPacCoordinates.coordinateX - 1][myPacCoordinates.coordinateY] == " ":
            return Coordinate(myPacCoordinates.coordinateX - 1, myPacCoordinates.coordinateY)
    elif nearbyEnemyPacCoordinatesDifference.coordinateY == 0:
        if isValid(Coordinate(myPacCoordinates.coordinateX + nearbyEnemyPacCoordinatesDifference.coordinateX,
                              myPacCoordinates.coordinateY),
                   gridMatrix) and \
                gridMatrix[myPacCoordinates.coordinateX + nearbyEnemyPacCoordinatesDifference.coordinateX][
                    myPacCoordinates.coordinateY] == " ":
            return Coordinate(myPacCoordinates.coordinateX + nearbyEnemyPacCoordinatesDifference.coordinateX,
                              myPacCoordinates.coordinateY)
        if isValid(Coordinate(myPacCoordinates.coordinateX, myPacCoordinates.coordinateY + 1), gridMatrix) and \
                gridMatrix[myPacCoordinates.coordinateX][myPacCoordinates.coordinateY + 1] == " ":
            return Coordinate(myPacCoordinates.coordinateX, myPacCoordinates.coordinateY + 1)
        if isValid(Coordinate(myPacCoordinates.coordinateX, myPacCoordinates.coordinateY - 1), gridMatrix) and \
                gridMatrix[myPacCoordinates.coordinateX][myPacCoordinates.coordinateY - 1] == " ":
            return Coordinate(myPacCoordinates.coordinateX, myPacCoordinates.coordinateY - 1)

    return myPacCoordinates


def findIfPelletStillPresent(pelletList: list, pelletCoordinates: Coordinate):
    for pellet in pelletList:
        if pellet.pelletCoordinate.coordinateX == pelletCoordinates.coordinateX and pellet.pelletCoordinate.coordinateY == pelletCoordinates.coordinateY:
            return True
    return False


def findRandomPellet(pelletList: list):
    return pelletList[randint(0, len(pelletList) - 1)]


# width: size of the grid
# height: top left corner is (x=0, y=0)
width, height = [int(i) for i in input().split()]
grid = [["E" for x in range(width)] for y in range(height)]
for i in range(height):
    row = input()  # one line of the grid: space " " is floor, pound "#" is wall
    grid[i] = row

# game loop

while True:
    my_score, opponent_score = [int(i) for i in input().split()]
    visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
    pacList = []
    for i in range(visible_pac_count):
        # pac_id: pac number (unique within a team)
        # mine: true if this pac is yours
        # x: position in the grid
        # y: position in the grid
        # type_id: unused in wood leagues
        # speed_turns_left: unused in wood leagues
        # ability_cooldown: unused in wood leagues
        pac_id, mine, x, y, type_id, speed_turns_left, ability_cooldown = input().split()
        pac_id = int(pac_id)
        mine = mine != "0"
        x = int(x)
        y = int(y)
        pacList.append(Pac(pac_id, mine, Coordinate(x, y)))
        speed_turns_left = int(speed_turns_left)
        ability_cooldown = int(ability_cooldown)
    visible_pellet_count = int(input())  # all pellets in sight
    pelletList = []
    for i in range(visible_pellet_count):
        # value: amount of points this pellet is worth
        x, y, value = [int(j) for j in input().split()]
        pelletList.append(Pellet(Coordinate(x, y), value))

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    myPacs: list = findMyPac(pacList)

    outputString = ""
    for i in range(len(myPacs)):
        myPacCoordinates = myPacs[i].pacCoordinate
        nearbyEnemyPacCoordinatesDifference: Coordinate = checkEnemyPacPosition(pacList, myPacCoordinates)

        if nearbyEnemyPacCoordinatesDifference.coordinateX > 1:
            TOGGLE_SUPERPELLET = True
            nearestSuperPelletOrPellet: Pellet = findNearestSuperPelletOrPellet(grid, pelletList, myPacCoordinates)
            xCoord: int = nearestSuperPelletOrPellet.pelletCoordinate.coordinateX
            yCoord: int = nearestSuperPelletOrPellet.pelletCoordinate.coordinateY

            # MOVE <pacId> <x> <y>
            outputString = outputString + "MOVE " + str(myPacs[i].pacID) + " " + str(xCoord) + " " + str(yCoord)
            if i != len(myPacs) - 1:
                outputString = outputString + " | "
        else:
            TOGGLE_SUPERPELLET = False
            newCoordinates: Coordinate = findNearestPossiblePosInDirection(grid, myPacCoordinates,
                                                                           nearbyEnemyPacCoordinatesDifference)
            if newCoordinates.coordinateX == myPacCoordinates.coordinateX and \
                    newCoordinates.coordinateY == myPacCoordinates.coordinateY:
                newPelletDest: Pellet = findRandomPellet(pelletList)
                newCoordinates.coordinateX = newPelletDest.pelletCoordinate.coordinateX
                newCoordinates.coordinateY = newPelletDest.pelletCoordinate.coordinateY
            outputString = outputString + "MOVE " + str(myPacs[i].pacID) + " " + str(
                newCoordinates.coordinateX) + " " + str(newCoordinates.coordinateY)
            if i != len(myPacs) - 1:
                outputString = outputString + " | "

    print(outputString)
