import time
from typing import List
from multiprocessing import Process

from getkey import getkey, keys

from entities import *
from utils import utils
from items import Item, Dummy, ItemType
from . import (
    states, 
    renderer
)


def attacking(attacker: Pawn, targets: List[Enemy], effects):
    if attacker.last_attack + 1 / attacker.attack_speed > time.time():
        return

    # Place effects
    effects.extend([])
    for n in range(attacker.attack_range + 1):
        effect_pos = (-1)**int(attacker.left_facing) * n + attacker.pos
        if n > 0:
            effects.append(
                Effect(
                    pos=effect_pos, 
                    render=attacker.attack_render, 
                    lifetime=0.15
            ))

        for target in targets:
            if target.pos == effect_pos:
                attacker.damage(target)
    attacker.last_attack = time.time()

def menu_select(pick, title, choices: List[str]=["1.", "2.", "3."]):
    def choices_func():
        blink = False
        while True:
            blink = not blink
            utils.clear_screen()
            options = f"{title}\n"
            for n, choice in enumerate(choices, start=1):
                options += f"{'X' if blink and pick == n else n}. {choice + ' <-' if pick == n else choice}\n"
            print(options)
            time.sleep(2/3)
    
    choosing = Process(target=choices_func)
    choosing.start()
    time.sleep(1/3)
    while True:
        key = getkey()
        if key in (keys.DOWN, keys.PAGE_DOWN, 's', 'j'):
            pick = pick % len(choices) + 1
        elif key in (keys.UP, keys.PAGE_UP, 'w', 'k'):
            pick = (pick - 2) % len(choices) + 1
        elif key == keys.HOME:
            pick = 1
        elif key == keys.END:
            pick = len(choices)
        elif key == keys.SPACE or key == keys.ENTER:
            break
        elif key == keys.ESCAPE:
            if pick == len(choices):
                break
            pick = len(choices)
        else:
            continue
        choosing.terminate()

        choosing = Process(target=choices_func)
        choosing.start()
    if choosing.is_alive():
        choosing.terminate()
    utils.clear_screen()
    return pick


def shop_select(player: Player, items: List[Item], items_per_page=7):
    s = states.ShopState(items, items_per_page)

    choosing = Process(target=renderer.shop, args=(s, player, items))
    choosing.start()
    while True:
        key = getkey()
        if key == keys.ESCAPE:
            break
        elif key in (keys.DOWN, keys.PAGE_DOWN, 's'):
            s.cursor_position += 1
            if s.cursor_position % items_per_page == 1:
                s.current_page += 1
            if s.cursor_position > s.total_items:
                s.cursor_position = 1
                s.current_page = 0
                if s.current_page > s.total_pages - 1:
                    s.current_page = 0
        
        elif key in (keys.UP, keys.PAGE_UP, 'w'):
            s.cursor_position -= 1
            if s.cursor_position % items_per_page == 0:
                s.current_page -= 1
            if s.current_page < 0:
                s.current_page = s.total_pages - 1
                s.cursor_position = s.total_items
        
        elif key in (keys.LEFT, 'a'):
            if s.current_page > 0:
                s.current_page -= 1
                s.cursor_position = (s.cursor_position - items_per_page) % s.total_items
            else:
                s.current_page = s.total_pages - 1
                if s.cursor_position > len(items[items_per_page*s.current_page:]):
                    s.cursor_position = s.total_items
                else:
                    s.cursor_position = s.cursor_position + (s.total_pages-1) * items_per_page
        
        elif key in (keys.RIGHT, 'd'):
            if s.current_page < s.total_pages - 1:
                s.current_page += 1
                s.cursor_position = min(s.total_items, s.cursor_position + items_per_page)
            else:
                s.current_page = 0
                s.cursor_position = (s.cursor_position - 1) % items_per_page + 1
        
        elif (key == keys.ENTER or key == keys.SPACE) and s.total_items > 0:
            selected_index = s.cursor_position - 1
            item = items[selected_index]
            if item.item_type != ItemType.DUMMY and player.buy_item(item):
                s.bought = s.cursor_position
                if item.count == 0:
                    items[selected_index] = Dummy(name=" Sold Out")
        choosing.terminate()
        s.update(items)
        choosing = Process(target=renderer.shop, args=(s, player, items))
        choosing.start()
    if choosing.is_alive():
        choosing.terminate()
    utils.clear_screen()


def inventory_menu(state, player, menu_height=5, menu_col_width=30):
    s = states.InventoryState(player, menu_height, menu_col_width)
    
    choosing = Process(target=renderer.inventory, args=(s,))
    choosing.start()
    while True:
        key = getkey()
        if key == keys.ESCAPE:
            break
        elif not s.rows:
            continue
        elif key in (keys.DOWN, keys.PAGE_DOWN, 's'):
            s.row_cur += 1
            if s.row_cur > len(s.rows[s.col_cur]) - 1:
                s.row_cur = 0
        
        elif key in (keys.UP, keys.PAGE_UP, 'w'):
            s.row_cur -= 1
            if s.row_cur < 0:
                s.row_cur = len(s.rows[s.col_cur]) - 1
        
        elif key in (keys.LEFT, 'a') and s.col_cur > 0:
            s.col_cur -= 1
            col_length = len(s.rows[s.col_cur]) - 1
            if s.row_cur > col_length:
                s.row_cur = col_length

        elif key in (keys.RIGHT, 'd') and s.col_cur < len(s.cols) - 1:
            s.col_cur += 1
            col_length = len(s.rows[s.col_cur]) - 1
            if s.row_cur > col_length:
                s.row_cur = col_length
        
        elif (key == keys.ENTER or key == keys.SPACE):
            if len(s.cols) > 0 and len(player.inventory[s.cols[s.col_cur]]) > 0:
                col = player.inventory[s.cols[s.col_cur]]
                player.use_item(col[s.row_cur], player)
                if s.row_cur >= len(col):
                    s.row_cur -= 1
                if s.col_cur >= len(s.cols):
                    s.col_cur -= 1

        choosing.terminate()
        s.update(player)
        choosing = Process(target=renderer.inventory, args=(s,))
        choosing.start()
    if choosing.is_alive():
        choosing.terminate()
    utils.clear_screen()