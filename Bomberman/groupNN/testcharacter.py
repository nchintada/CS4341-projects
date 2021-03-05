# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from queue import PriorityQueue
import random
class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        #m1 = random.randint(-1, 1)
        #m2 = random.randint(0, 1)
        #self.move(m1, m2)
        loc = (self.x, self.y)
        goal = (7, 18)
        #print(wrld.empty_at(goal[0], goal[1]))
        came_from, cost_so_far = self.AStar(wrld, loc, goal)
        print(came_from)
        #print(cost_so_far)
        #next_position = list(came_from.keys())[list(came_from.values()).index(loc)]
        #next_move = self.calculateD(loc, next_position)
        #print(next_move)
        #print(came_from[goal])
        #for move in list(came_from.keys()):
        #    self.set_cell_color(move[0], move[1], Fore.RED + Back.GREEN)
        #print(self.getNeighbors(loc, wrld))
        #self.move(next_move[0], next_move[1])
        path = goal
        next = (0, 0)
        while path != loc:
            temp = path
            path = came_from[path]
            #print(path)
            if path == loc:
                next = temp
                break
        next_move = self.calculateD(loc, next)
        print(loc)
        print(next)
        print(next_move)
        self.move(next_move[0], next_move[1])



    def AStar(self, wrld, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in self.getNeighbors(current, wrld):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.calculateH(next, goal)
                    frontier.put(next, priority)
                    came_from[next] = current
        return came_from, cost_so_far


    def calculateH(self, loc1, loc2):
        (x1, y1) = loc1
        (x2, y2) = loc2
        return abs(x1 - x2) + abs(y1 - y2)

    def calculateD(self, loc1, loc2):
        (x1, y1) = loc1
        (x2, y2) = loc2
        return ((x2 - x1), (y2 - y1))

    def getNeighbors(self, loc, wrld):
        list_of_N = []
        for dx in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if (loc[0] + dx >= 0) and (loc[0] + dx < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    # Make sure the monster is moving
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if (loc[1] + dy >= 0) and (loc[1] + dy < wrld.height()):
                            # No need to check impossible moves
                            if wrld.exit_at(loc[0] + dx, loc[1] + dy):
                                list_of_N.append((loc[0] + dx, loc[1] + dy))
                                break
                            if wrld.empty_at(loc[0] + dx, loc[1] + dy):
                                list_of_N.append((loc[0] + dx, loc[1] + dy))
        return list_of_N
