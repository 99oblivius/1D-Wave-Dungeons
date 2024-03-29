import time

from game import Game

from multiprocessing import Process

from getkey import getkey, keys
from utils.utils import clear_screen


if __name__ == '__main__':
    game = Game()
    game.start()
