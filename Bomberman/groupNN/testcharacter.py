# This is necessary to find the main code
import sys

from Bomberman.bomberman.sensed_world import SensedWorld

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from queue import PriorityQueue
import numpy as np

import random
import math
from enum import Enum

class TestCharacter(CharacterEntity):

    depth = 4

    def do(self, wrld):
        # Your code here
        #m1 = random.randint(-1, 1)
        #m2 = random.randint(0, 1)
        #self.move(m1, m2)
        loc = (self.x, self.y)
        #print(wrld.empty_at(goal[0], goal[1]))
        wrldState = self.evaluateState(wrld)
        characterState = wrldState[0]
        # do expectimax
        if characterState == state.UNSAFE:
            #use wrldState[1] to get monster list
            #stupid monster name
            if wrldState[1][0] == 'stupid':
                v, action = self.maxvalue(wrld, loc, 0)
                print(action)
                next_move = self.calculateD(loc, action)
                print(next_move)
                self.move(next_move[0], next_move[1])

        if characterState == state.SAFE:
            came_from, cost_so_far = self.AStar(wrld, loc, wrld.exitcell, [obstacles.EXIT])
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
            path = wrld.exitcell
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

    # Also passes up our action
    def maxvalue(self, wrld, curr, d):
        if self.evaluateState(wrld)[0] == state.SAFE or d == self.depth:
            print("maxvalue")
            return self.utility(wrld), curr
        if self.evaluateState(wrld)[0] == state.DEAD:
            return -10000, curr
        v = -math.inf
        action = (0, 0)
        for a in self.getNeighbors(curr, wrld, [obstacles.EXIT]):
            # v = max(v, self.expvalue(wrld, a))
            newWrld = SensedWorld.from_world(wrld)
            character = next(iter(newWrld.characters.values()))[0]
            new_move = self.calculateD((character.x, character.y), (a[0], a[1]))
            print(new_move[0], new_move[1])
            character.move(new_move[0], new_move[1])
            newerWrld = newWrld.next()[0]
            val = self.expvalue(newerWrld, a, d + 1)
            if val > v:
                v = val
                action = a
        return v, action

    # Probably will need to call expvalue on multiple monsters but that will be handled in maxvalue
    def expvalue(self, wrld, act, d):
        if self.evaluateState(wrld)[0] == state.SAFE or d == self.depth:
            print("expvalue" )
            return self.utility(wrld)
        v = 0
        mcurr = self.getMonster(wrld, 'stupid')
        possible_moves = self.getNeighbors((mcurr.x, mcurr.y), wrld, [obstacles.PLAYER])
        for a in possible_moves:
            p = 1.0/len(possible_moves)
            # p←Probability(a)
            # v←v+p·Max-value(Result(state,a))
            # print("What are we getting? " + )
            newWrld = SensedWorld.from_world(wrld)
            monster = self.getMonster(newWrld, 'stupid')
            new_move = self.calculateD((monster.x, monster.y), (a[0], a[1]))
            monster.move(new_move[0], new_move[1])
            print("Monster position before" + str(monster.x) + ' ' + str(monster.y))
            newerWrld = newWrld.next()[0]
            monster = self.getMonster(newerWrld, 'stupid')
            print("Monster position after" + str(monster.x) + ' ' + str(monster.y))
            print("expvalue for loop")
            value = self.maxvalue(newerWrld, act, d+1)[0]
            v = v + p*value
        return v

    def getMonster(self, wrld, name):
        for monster in list(wrld.monsters.values()):
            if monster[0].name == name:
                return monster[0]


    def utility(self, wrld):
        return self.monster_utility(wrld) - self.exit_utility(wrld)

    def exit_utility(self, wrld):
        try:
            chara = next(iter(wrld.characters.values()))
            character = chara[0]
        except (IndexError, StopIteration):
            return 0
        loc = (character.x, character.y)
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

    def monster_utility(self, wrld):
        try:
            chara = next(iter(wrld.characters.values()))
            character = chara[0]
        except (IndexError, StopIteration):
            return 0
        m = next(iter(wrld.monsters.values()))[0]
        loc = (character.x, character.y)
        mloc = (m.x, m.y)
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
        #(x1, y1) = loc1
        #(x2, y2) = loc2
        #return abs(x1 - x2) + abs(y1 - y2)
        return math.sqrt(((loc1[0] - loc2[0]) ** 2) + ((loc1[1] - loc2[1]) ** 2))

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
    def evaluateState(self, wrld):
        #print(wrld.monsters)
        try:
            chara = next(iter(wrld.characters.values()))
            character = chara[0]
        except (IndexError, StopIteration):
            return state.DEAD, []
        try:
            monsters = list(wrld.monsters.values())
        except (StopIteration):
            pass

        loc = (character.x, character.y)
        counters = {}
        #print(monsters)
        for monster in monsters:
            m = monster[0]
            #print(monster)
            monsterType = m.name
            mloc = (m.x, m.y)
            monster_came_from, monster_cost_so_far = self.AStar(wrld, loc, mloc, [obstacles.MONSTER, obstacles.PLAYER])
            #print(monster_came_from)
            #print(monster_cost_so_far)
            counter = 0
            path = mloc
            while path != loc:
                path = monster_came_from[path]
                # print(path)
                if path == loc:
                    break
                counter += 1
            counters[monsterType] = counter
        counts = [(k, v) for k, v in counters.items() if v <= 40]
        flag = False
        monsterTypes = []
        for count in counts:
            if count[1] <= 4:
                flag = True
                monsterTypes.append(count[0])
        if flag:
            #print(counts)
            return state.UNSAFE, monsterTypes
        return state.SAFE, []


class state(Enum):
    SAFE = 1
    UNSAFE = 2
    DEAD = 3

class obstacles(Enum):
    EXIT = 1
    MONSTER = 2
    WALL = 3
    BOMB = 4
    EXPLOSION = 5
    PLAYER = 6