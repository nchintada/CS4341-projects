# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from queue import PriorityQueue

import random
import math
from enum import Enum

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        #m1 = random.randint(-1, 1)
        #m2 = random.randint(0, 1)
        #self.move(m1, m2)
        loc = (self.x, self.y)
        m = next(iter(wrld.monsters.values()))
        monster = (m[0].x, m[0].y)
        exitBlock = (7, 18)
        #print(wrld.empty_at(goal[0], goal[1]))
        characterState = self.evaluateState(wrld, loc, monster)
        # do expectimax
        if characterState == state.UNSAFE:
            next_loc = self.maxvalue(wrld, loc, [monster], 0)[1]
            next_move = self.calculateD(loc, next_loc)
            self.move(next_move[0], next_move[1])

        if characterState == state.SAFE:
            came_from, cost_so_far = self.AStar(wrld, loc, exitBlock, [obstacles.EXIT])
            #print(came_from)
            #print(cost_so_far)
            #next_position = list(came_from.keys())[list(came_from.values()).index(loc)]
            #next_move = self.calculateD(loc, next_position)
            #print(next_move)
            #print(came_from[goal])
            #for move in list(came_from.keys()):
            #    self.set_cell_color(move[0], move[1], Fore.RED + Back.GREEN)
            #print(self.getNeighbors(loc, wrld))
            #self.move(next_move[0], next_move[1])
            path = exitBlock
            next_m = (0, 0)
            while path != loc:
                temp = path
                path = came_from[path]
                #print(path)
                if path == loc:
                    next_m = temp
                    break
            next_move = self.calculateD(loc, next_m)
            #print(loc)
            #print(next)
            #print(next_move)
            self.move(next_move[0], next_move[1])

    # Probably will need to call expvalue on multiple monsters but that will be handled in maxvalue
    def expvalue(self, wrld, act, mcurr, d):
        if self.evaluateState(wrld, act, mcurr) == state.SAFE or d == 4:
            return self.monster_utility(wrld, act, mcurr)
        v = 0
        possible_moves = self.getNeighbors((mcurr[0], mcurr[1]), wrld, [obstacles.PLAYER])
        for a in possible_moves:
            p = 1.0/len(possible_moves)
            # p←Probability(a)
            # v←v+p·Max-value(Result(state,a))
            # print("What are we getting? " + )
            value = self.maxvalue(wrld, act, [a], d+1)[0]
            v = v + p*value
        return v


    # Also passes up our action
    def maxvalue(self, wrld, curr, monsters, d):
        if self.evaluateState(wrld, curr, monsters[0]) == state.SAFE or d == 4:
            return self.utility(wrld, curr, monsters[0]), curr
        v = -math.inf
        action = (0, 0)
        for a in self.getNeighbors(curr, wrld, [obstacles.EXIT]):
            # v = max(v, self.expvalue(wrld, a))
            print("Monster: " + str(monsters[0]))
            val = self.expvalue(wrld, a, (monsters[0][0], monsters[0][1]), d+1)
            if val > v:
                v = val
                action = a
        return v, action

    def utility(self, wrld, loc, mloc):
        return self.monster_utility(wrld, loc, mloc) - self.exit_utility(wrld, loc)

    def exit_utility(self, wrld, loc):
        e = wrld.exitcell
        exit_came_from, exit_cost_so_far = self.AStar(wrld, loc, (e[0], e[1]), [obstacles.EXIT])
        counter = 0
        path = (e[0], e[1])
        while path != loc:
            path = exit_came_from[path]
            # print(path)
            if path == loc:
                break
            counter += 1
        return counter

    def monster_utility(self, wrld, loc, mloc):
        monster_came_from, monster_cost_so_far = self.AStar(wrld, loc, mloc, [obstacles.MONSTER, obstacles.PLAYER])
        counter = 0
        path = mloc
        while path != loc:
            path = monster_came_from[path]
            # print(path)
            if path == loc:
                break
            counter += 1
        return counter

    def AStar(self, wrld, start, goal, list_of_e):
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

            for next in self.getNeighbors(current, wrld, list_of_e):
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

    def getNeighbors(self, loc, wrld, list_of_e):
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
                            if obstacles.EXIT in list_of_e:
                                if wrld.exit_at(loc[0] + dx, loc[1] + dy):
                                    list_of_N.append((loc[0] + dx, loc[1] + dy))
                                    break
                            if obstacles.MONSTER in list_of_e:
                                if wrld.monsters_at(loc[0] + dx, loc[1] + dy):
                                    list_of_N.append((loc[0] + dx, loc[1] + dy))
                                    break
                            if obstacles.PLAYER in list_of_e:
                                if wrld.characters_at(loc[0] + dx, loc[1] + dy):
                                    list_of_N.append((loc[0] + dx, loc[1] + dy))
                                    break
                            if wrld.empty_at(loc[0] + dx, loc[1] + dy):
                                list_of_N.append((loc[0] + dx, loc[1] + dy))
        return list_of_N


    #Will return either safe or not safe
    def evaluateState(self, wrld, loc, mloc):
        #print(wrld.monsters)
        m = next(iter(wrld.monsters.values()))[0]
        monster_came_from, monster_cost_so_far = self.AStar(wrld, loc, mloc, [obstacles.MONSTER, obstacles.PLAYER])
        print(monster_came_from)
        #print(monster_cost_so_far)
        counter = 0
        path = mloc
        while path != loc:
            path = monster_came_from[path]
            # print(path)
            if path == loc:
                break
            counter += 1
        if counter <= 4:
            return state.UNSAFE
        return state.SAFE


class state(Enum):
    SAFE = 1
    UNSAFE = 2

class obstacles(Enum):
    EXIT = 1
    MONSTER = 2
    WALL = 3
    BOMB = 4
    EXPLOSION = 5
    PLAYER = 6