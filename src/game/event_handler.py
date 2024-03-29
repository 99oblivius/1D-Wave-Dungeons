from getkey import getkey, keys

from entities import *
from . import (
    event_actions, 
    renderer
)


def user_input(state, entities):
    key = getkey()
    if key == keys.ESCAPE:
        state.playing = False
    
    if key in ('w', keys.SPACE, keys.UP):
        event_actions.attacking(entities.player, entities.enemies, entities.effects)
    
    if key == keys.LEFT or key == 'a':
        entities.player.left()
    
    elif key == keys.RIGHT or key == 'd':
        entities.player.right()

def main_menu(state, title: str="", won: bool=False):
    default_choices = [
        "Enter Dungeon", 
        "Shop", 
        "Guide",
        "Exit"]
    won_choices = [
        "Enter Dungeon", 
        "Go to Next Dungeon",
        "Shop", 
        "Guide",
        "Exit"]
    choice = renderer.menu_select(title, won_choices if won else default_choices)
    if not won and choice > 1: choice += 1
    match choice:
        case 1:  # Enter Dungeon
            state.playing = True
        case 2:  # Go to next dungeon
            state.difficulty += 1
            state.playing = True
        case 3:  # Shop
            pass
        case 4:  # Guide
            pass
        case 5:  # Exit
            state.playing = False
            state.run = False