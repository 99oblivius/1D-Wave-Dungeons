from typing import List

from items import Item
from entities import Player


class GameState:
    def __init__(self, 
        process=None, 
        playing=False
    ):
        self.game_start_time = None
        self.process = process
        self.playing = playing
        self.run = True
        self.died = False
        self.slaughtered = False
        self.escaped = False
        self.menu_cursor = 1

        self.difficulty = 1
        self.playspace = 12
        self.rounds = 0

        self.tickrate = 6
        self.delta_time = 1.0 / self.tickrate
        self.frame_time = 0.0


class ShopState:
    def __init__(self, items: List[Item], items_per_page: int):
        self.items_per_page = items_per_page

        self.total_items = len(items)
        self.total_pages = (self.total_items - 1) // items_per_page + 1
        self.current_page = 0
        self.cursor_position = 1
        self.bought = 0
    
    def update(self, items: List[Item]):
        self.total_items = len(items)
        self.total_pages = (self.total_items - 1) // self.items_per_page + 1
        if self.total_items < self.cursor_position:
            self.cursor_position = self.total_items


class InventoryState:
    def __init__(self, player: Player, menu_height: int, menu_col_width: int):
        self.menu_height = menu_height
        self.menu_col_width = menu_col_width
        self.row_cur = 0
        self.col_cur = 0

        self.col_disp = [0] * len(player.inventory)

        items = player.inventory.items()
        self.cols = [t for t, ls in items if len(ls) > 0]
        self.rows = [ls for _, ls in items if len(ls) > 0]
    
    def total_items(self):
        sum = 0
        for n in range(len(self.cols)):
            sum += len(self.rows[n])
        return sum
    
    def update(self, player: Player):
        pass