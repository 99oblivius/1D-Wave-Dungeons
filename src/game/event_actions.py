import time
from typing import List
from multiprocessing import Process

from getkey import getkey, keys

from entities import *
from utils import utils
from items import Item


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

def menu_select(title, choices: List[str]=["1.", "2.", "3."]):
    pick = 1
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
    time.sleep(1/2)
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
        else:
            continue
        choosing.terminate()
        choosing = Process(target=choices_func)
        choosing.start()
    if choosing.is_alive():
        choosing.terminate()
    utils.clear_screen()
    return pick


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


def shop_select(items, player, items_per_page=4):
    s = ShopState(items, items_per_page)

    def render_menu(s: ShopState):
        blink = False
        while True:
            blink = not blink
            utils.clear_screen()
            options = f" - {s.current_page + 1} of {s.total_pages} -"
            options += f"Player pick: {s.cursor_position}\n"
            options += f" - Move: W,A,S,D,↑,←,↓,→  Buy: ENTER  Exit: ESCAPE -\n"
            options += f"Player Balance: {player.balance}\n"
            
            start_index = s.current_page * items_per_page
            end_index = min(start_index + items_per_page, s.total_items)
            if s.total_items == 0:
                options += f"\n - No Items -"
            for n, item in enumerate(items[start_index:end_index], start=1):
                n = n+start_index
                if s.bought == n:
                    name = utils.obfuscated(item.name, '~')
                    s.bought = 0
                elif player.balance < item.price: name = utils.obfuscated(item.name, 'X')
                else: name = item.name

                index = 'X'*len(str(n)) if blink and s.cursor_position == n else n
                options += f"{index}. {name + ' <-' if s.cursor_position == n else name + '   '} Cost:{item.price} x{item.count:02}\n"
            print(options)
            time.sleep(2/3)
    choosing = Process(target=render_menu, args=(s,))
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

        elif key == keys.ENTER and s.total_items > 0:
            selected_index = s.cursor_position - 1
            if selected_index < s.total_items:
                print("Item: ", s.cursor_position)
                print("Item: ", items[selected_index].name)
                if player.buy_item(items[selected_index]):
                    s.bought = s.cursor_position
                if items[s.cursor_position-1].count < 1:
                    items.pop(selected_index)
        
        choosing.terminate()
        s.update(items)
        choosing = Process(target=render_menu, args=(s,))
        choosing.start()
    if choosing.is_alive():
        choosing.terminate()
    utils.clear_screen()
