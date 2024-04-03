from getkey import getkey, keys

from entities import *
from . import (
    event_handler, 
)


def user_input(state, entities):
    key = getkey()
    if key == keys.ESCAPE:
        state.playing = False
    
    if key in ('w', keys.SPACE, keys.UP):
        event_handler.attacking(entities.player, entities.enemies, entities.effects)
    
    if key == keys.LEFT or key == 'a':
        entities.player.left()
    
    elif key == keys.RIGHT or key == 'd':
        entities.player.right()

def main_menu(state, player, shop, title: str="", won: bool=False):
    choices = [
        "Enter Dungeon", 
        "Inventory",
        "Shop", 
        "Stats",
        "Guide",
        "Exit"]
    if won: choices.insert(1, "Go to Next Dungeon")
    choice = event_handler.menu(state.menu_cursor, title, choices)
    state.menu_cursor = choice
    if not won and choice > 1: choice += 1

    match choice:
        case 1:  # Enter Dungeon
            state.playing = True
        case 2:  # Go to next dungeon
            state.menu_cursor = 1
            state.difficulty += 1
            state.playing = True
        case 3:  # Stats
            event_handler.inventory_menu(state, player)
        case 4:  # Shop
            event_handler.shop_menu(player, shop)
        case 5:  # Stats
            event_handler.stats(state)
        case 6:  # Guide
            event_handler.guide(state, player)
        case 7:  # Exit
            state.playing = False
            state.run = False
