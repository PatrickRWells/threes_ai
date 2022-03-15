from cmath import sin
import numpy as np
import random
from copy import copy
import math

class Grid:
    _size = 4
    def __init__(self, size = 4, *args, **kwargs):
        self._size = size
        self._grid = np.zeros(size*size, dtype = int)
    
    def __str__(self):
        base = "{}, {}, {}, {}\n"
        retval = ""
        for i in range(self._size):
            retval += base.format(*self._grid[i*self._size: ((i+1)*self._size)])

        return retval

    @classmethod
    def get_index(self, x, y):
        if x >= self._size or y >= self._size:
            return
        return x*self._size + y
    
    @classmethod
    def get_xy(self, i):
        return i%4,  math.floor(i/4)
    
    @property
    def grid(self):
        return self._grid


    def get_score(self):
        score = 0
        for val in self._grid:
            if val < 3:
                continue
            exp = math.log2((val / 3)) + 1
            score += math.pow(3, exp)
        return score
        
    @property
    def has_empty(self, *args, **kwargs):
        if 0 in self._grid:
            return True
        else:
            return False

    def insert(self, x: int, y: int, val: int):
        i = self.get_index(x,y)
        if self._grid[i] != 0:
            return False
        self._grid[i] = val
        return True

    def check_collision(self, a, b):
        if a + b == 3:
            return 3
        elif a == b and a > 2: 
            return a*2

        return False
    
    @property
    def max(self):
        return np.max(self._grid)

    def swipe_left(self, *args, **kwargs):
        new_grid = copy(self._grid)
        for i in range(self._size):
            bounds = (i*self._size, (i+1)*self._size)
            row = self._grid[bounds[0]: bounds[1]]
            for index, val in enumerate(row):
                sindex = self.get_index(i, index)
                if index == 0:
                    continue
                elif new_grid[sindex - 1] == 0:
                    new_grid[sindex - 1] = val
                    new_grid[sindex] = 0

                else:
                    c = self.check_collision(new_grid[sindex], new_grid[sindex -1])
                    if c:
                        new_grid[sindex - 1] = c
                        new_grid[sindex] = 0
        if np.array_equal(self._grid, new_grid):
            return False            
        self._grid = new_grid
        return True

    def swipe_right(self, *args, **kwargs):
        new_grid = copy(self._grid)
        for i in range(self._size):
            bounds = (i*self._size, (i+1)*self._size)
            row = self._grid[bounds[0]: bounds[1]]
            for index, val in enumerate(reversed(row)):
                real_index = self._size - index - 1
                sindex = self.get_index(i, real_index)
                if real_index == 3:
                    continue
                elif new_grid[sindex + 1] == 0:
                    new_grid[sindex + 1] = val
                    new_grid[sindex] = 0
                else:
                    c = self.check_collision(new_grid[sindex], new_grid[sindex + 1])
                    if c:
                        new_grid[sindex + 1] = c
                        new_grid[sindex] = 0
        if np.array_equal(self._grid, new_grid):
            return False            
        self._grid = new_grid
        return True

    def swipe_up(self, *args, **kwargs):
        new_grid = copy(self._grid)
        for i in range(self._size):
            col = [self._grid[i + 4*ix] for ix in range(4)]
            for index, val in enumerate(col):
                sindex = self.get_index(index, i)
                if index == 0:
                    continue
                elif new_grid[sindex - 4] == 0:
                    new_grid[sindex - 4] = val
                    new_grid[sindex] = 0
                else:
                    c = self.check_collision(new_grid[sindex], new_grid[sindex -4])
                    if c:
                        new_grid[sindex -4] = c
                        new_grid[sindex] = 0            
        if np.array_equal(self._grid, new_grid):
            return False            
        self._grid = new_grid
        return True
    
    def swipe_down(self, *args, **kwargs):
        new_grid = copy(self._grid)
        for i in range(self._size):
            col = [self._grid[i + 4*ix] for ix in range(4)]
            for index, val in enumerate(reversed(col)):
                real_index = self._size - index - 1
                sindex = self.get_index(real_index, i)
                if index == 0:
                    continue
                elif new_grid[sindex + 4] == 0:
                    new_grid[sindex + 4] = val
                    new_grid[sindex] = 0
                else:
                    c = self.check_collision(new_grid[sindex], new_grid[sindex + 4])
                    if c:
                        new_grid[sindex + 4] = c
                        new_grid[sindex] = 0            
        if np.array_equal(self._grid, new_grid):
            return False            
        self._grid = new_grid
        return True


class Game:
    
    def __init__(self, size, *args, **kwargs):
        self._grid = Grid(size)
        self._init()
    
    def __str__(self):
        g = str(self._grid)
        g += "Next: {}\n".format(self._next)
        g += "Score: {}".format(int(self.score))
        return g


    def _init(self, starting = 9, *args, **kwargs):
        self.get_basic_list()
        self._max = 3
        for i in range(starting):
            next = self.get_next_basic()
            self.add_tile(next)
        self._next = self.get_next()
        self.score = self._grid.get_score()

    
    @property
    def next(self):
        return self._next

    def add_tile(self, val):
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            while not self._grid.insert(x,y, val):
                x = random.randint(0, 3)
                y = random.randint(0, 3)
    
    
    def get_next_basic(self, *args, **kwargs):
        val = self._basic_list.pop(0)
        if len(self._basic_list) == 0:
            self.get_basic_list()
        return val

    def get_basic_list(self, *args, **kwargs):
        arr = [1,1,1,1,2,2,2,2,3,3,3,3]
        random.shuffle(arr)
        self._basic_list = arr
    
    def get_bonus_list(self, max, *args, **kwargs):
        if max < 48:
            self._bonus_list = []
        else:
            self._bonus_list = []
            i = 6
            while i <= max/8:
                self._bonus_list.append(i)
                i *= 2
    def update(self):
        self._add_new()
        self.score = self._grid.get_score()
        print(self)

    def swipeLeft(self, *args, **kwargs):
        if self._grid.swipe_left():
            self.update()

    def swipeRight(self, *args, **kwargs):
        if self._grid.swipe_right():
            self.update()
    
    def swipeUp(self, *args, **kwargs):
        if self._grid.swipe_up():
            self.update()

    def swipeDown(self, *args, **kwargs):
        if self._grid.swipe_down():
            self.update()
    
    def get_next(self, *args, **kwargs):
        if self._grid.max != self._max:
            self._max = self._grid.max
            self.get_bonus_list(self._max)
        if self._max >= 48 and np.random.randint(0, 22) == 21:
            return random.choice(self._bonus_list)
        else:
            return self.get_next_basic()
    
    
    def _add_new(self, *args, **kwargs):
        if not self._grid.has_empty:
            print("Game over!")
            print("Final Score: {}".format(self.score))
            exit()
        else:
            self.add_tile(self._next)
            self._next = self.get_next()
        
    def play(self):
        print(self)
        allowed = ['U','D', 'L','R','Q']        
        while True:
            c = input("Input a command: ")
            d = c.upper()
            if d not in allowed:
                print("Invalid command")
                continue
            if d == 'Q':
                exit()
            elif d == 'U':
                self.swipeUp()
            elif d == 'D':
                self.swipeDown()
            elif d == 'L':
                self.swipeLeft()
            elif d == 'R':
                self.swipeRight()
            print(self)

if __name__ == "__main__":
    g = Game(4)
    g.play()