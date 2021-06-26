from copy import deepcopy
import curses
from random import randint
from random import choice
from time import sleep


class Snake:
    def __init__(self):
        self.valid_inputs = {curses.KEY_UP: (
            0, -1), curses.KEY_DOWN: (0, 1), curses.KEY_RIGHT: (1, 1), curses.KEY_LEFT: (1, -1)}
        self.board = [['  ']*10 for _ in range(10)]
        self.board[randint(0, 9)][randint(0, 9)] = '🍎'
        self.body_coords = [[0, i] for i in range(4)]
        self.direction = [0, 1]

    def is_alive(self):
        head = self.body_coords[-1]
        tail = self.body_coords[:-1]
        return head not in tail

    def set_direction(self, key):
        idx = self.valid_inputs[key]
        if(idx[0] == self.direction[0] and idx[1] == -self.direction[1]):
            return
        self.direction[0] = idx[0]
        self.direction[1] = idx[1]

    def clear_board(self):
        for i in range(len(self.board)):
            for x in range(len(self.board[i])):
                if(self.board[i][x] != '🍎'):
                    self.board[i][x] = '  '
        for j in self.body_coords:
            if(self.body_coords.index(j) == 0):
                self.board[j[0]][j[1]] = '█ '
                continue
            self.board[j[0]][j[1]] = 'O '

    def move(self):
        new_head = deepcopy(self.body_coords)[0]
        new_head[self.direction[0]] += self.direction[1]
        self.body_coords.insert(0, new_head)
        if(not self.is_alive()):
            exit()
        self.body_coords.pop()
        if(self.body_coords[0][self.direction[0]] < 0):
            self.body_coords[0][self.direction[0]] = 9
        elif(self.body_coords[0][self.direction[0]] > 9):
            self.body_coords[0][self.direction[0]] = 0
        self.clear_board()
        if(not any('🍎' in x for x in self.board)):
            new_tail = deepcopy(self.body_coords)[-1]
            new_tail[self.direction[0]] -= self.direction[1]
            self.body_coords.append(new_tail)
            apple_coord_1 = choice(
                [i for i in range(0, 9) if i not in [x[0] for x in self.body_coords]])
            apple_coord_2 = choice(
                [i for i in range(0, 9) if i not in [x[1] for x in self.body_coords]])
            self.board[apple_coord_1][apple_coord_2] = '🍎'

    def redraw(self, stdscr):
        for i in range(len(self.board)):
            stdscr.addstr(i, 0, ' '.join(self.board[i]))
            stdscr.refresh()


def main(stdscr):
    stdscr.timeout(0)
    snake = Snake()
    while True:
        key = stdscr.getch()
        if(key in snake.valid_inputs):
            snake.set_direction(key)
        snake.move()
        snake.redraw(stdscr)
        sleep(0.3)


if __name__ == '__main__':
    curses.wrapper(main)