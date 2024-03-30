from getkey import getkey, keys

from entities import *
from items import *
from . import (
    event_actions, 
    event_actions,
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

def main_menu(state, player, title: str="", won: bool=False):
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
    choice = event_actions.menu_select(title, won_choices if won else default_choices)
    if not won and choice > 1: choice += 1
    match choice:
        case 1:  # Enter Dungeon
            state.playing = True
        case 2:  # Go to next dungeon
            state.difficulty += 1
            state.playing = True
        case 3:  # Shop
            show_shop_menu(player)
        case 4:  # Guide
            pass
        case 5:  # Exit
            state.playing = False
            state.run = False

def show_shop_menu(player):
    items_for_sale = [
        HealthPotion(10, 50, count=2), 
        HealthPotion(20, 150, count=4), 
        HealthPotion(30, 250, count=6),
    ]

    selected_item_index = event_actions.shop_select(items_for_sale, player)
    if selected_item_index is not None:
        selected_item = items_for_sale[selected_item_index]
        if player.balance >= selected_item.price:
            player.buy_item(selected_item)
            print(f"Bought {selected_item.name} for {selected_item.price}.")
        else:
            print("Not enough balance.")
