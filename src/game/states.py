from datetime import datetime

from typing import List

from items import items
from entities import Player


class GameState:
    def __init__(self, 
        process=None, 
        playing=False
    ):
        self.game_start_time = None
        self.process = process
        self.run = True

        self.menu_cursor = 1
        self.ingame = False

        self.playing = playing
        self.died = False
        self.slaughtered = False
        self.escaped = False

        self.difficulty = 1
        self.playspace = 12
        self.rounds = 0

        self.round_start = None
        self.round_end = None
        self.total_rounds = 0
        self.max_rounds = 0
        self.deaths = 0

        self.tickrate = 6
        self.delta_time = 1.0 / self.tickrate
        self.frame_time = 0.0
    
    def __str__(self):
        return f"""GameState(
game_start_time={datetime.fromtimestamp(self.game_start_time)}, 
process={self.process}, 
run={self.run}, 
playing={self.playing}, 
died={self.died}, 
slaughtered={self.slaughtered}, 
escaped={self.escaped}, 
difficulty={self.difficulty}, 
playspace={self.playspace}, 
rounds={self.rounds}, 
round_start={datetime.fromtimestamp(self.round_start) if self.round_start is not None else None}, 
round_end={datetime.fromtimestamp(self.round_end) if self.round_end is not None else None}, 
total_rounds={self.total_rounds}, 
max_rounds={self.max_rounds}, 
deaths={self.deaths}, 
tickrate={self.tickrate}, 
delta_time={self.delta_time}, 
frame_time={self.frame_time})"""
    
    @property
    def round_ended(self) -> bool:
        return any((self.slaughtered, self.escaped, self.died))
    
    @property
    def round_time(self):
        if self.round_end is None or self.round_start is None:
            return 0
        return int(self.round_end - self.round_start)
    
    @property
    def wins(self):
        return self.total_rounds - self.deaths


class ShopState:
    def __init__(self, items: list[items.Item], items_per_page: int):
        self.items_per_page = items_per_page

        self.total_items = len(items)
        self.total_pages = (self.total_items - 1) // items_per_page + 1
        self.current_page = 0
        self.cursor_position = 1
        self.bought = 0
    
    def update(self, items: list[items.Item]):
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
        items = player.inventory.items()
        self.cols = [t for t, ls in items if len(ls) > 0]
        self.rows = [ls for _, ls in items if len(ls) > 0]