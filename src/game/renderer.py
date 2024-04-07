import time

from utils import utils, menus
from items import items, ItemType
import entities
from . import (
    states, 
)


def menu(pick, title, choices):
    blink = False
    while True:
        blink = not blink
        utils.clear_screen()
        lines = f"{title}\n"
        for n, choice in enumerate(choices, start=1):
            lines += f"{'X' if blink and pick == n else n}. {choice + ' <-' if pick == n else choice}\n"
        print(lines)
        time.sleep(2/3)

def game(state, entities):
    lines = ""
    field = ['_'] * state.playspace
    for i in entities.effects + entities.enemies + [entities.player]:
        if i.pos is not None and 0 <= i.pos < state.playspace:
            field[i.pos] = i.render
        utils.clear_screen()
        header = menus.header_func(
            entities.player.health, 
            entities.player.attack_damage,
            sum(enemy.health for enemy in entities.enemies))
        
        footer = menus.footer_func(
            state.rounds+1, 
            entities.player.score, 1.0 / state.frame_time,
            time.time() - state.round_start)
        
        lines += f"{menus.instructions()}\n{header}\n{''.join(field)}\n{footer}"
        print(lines)
        lines = ""

def shop(s: states.ShopState, player: entities.Player, shop_items: list[items.Item]):
    blink = False
    while True:
        blink = not blink
        utils.clear_screen()
        lines = menus.shop_header(s.current_page, s.total_pages)
        
        if s.total_items == 0: lines += f"\n - No Items -"
        
        start_index = s.current_page * s.items_per_page
        end_index = min(start_index + s.items_per_page, s.total_items)
        for n, item in enumerate(shop_items[start_index:end_index], start=1):
            n = n+start_index
            if item.count < 0:
                lines += menus.shop_dummy(n, blink, s.cursor_position, item)
                continue

            if s.bought == n:
                name = utils.obfuscated(str(item), '~')
                s.bought = 0
            elif player.balance < item.price:
                name = utils.obfuscated(str(item), '$')
            else: name = str(item)
            lines += menus.shop_item(n, blink, s.cursor_position, item, name)
        lines += f"\n - Wallet: {player.balance} -\n"
        lines += f"\nDescription: {shop_items[s.cursor_position-1].description}"
        print(lines)
        time.sleep(2/3)

def inventory(s: states.InventoryState, player: entities.Player):
    blink = False
    while True:
        blink = not blink
        utils.clear_screen()
        lines = " - Inventory -\n"
        
        for col in s.cols:
            lines += utils.ellipse_justified(f"  {ItemType.typename(col)}  ", s.menu_col_width)
        lines += "\n"
        for r in range(s.menu_height):
            for n, col in enumerate(s.cols):
                if r > len(s.rows[n]) - 1:
                    lines += ' ' * s.menu_col_width
                else:
                    item = s.rows[n][r]
                    index = 'X' if blink and (s.row_cur == r and s.col_cur == n) else '•'
                    lines += utils.ellipse_justified(f"{index} {item.count}x {item}", s.menu_col_width-1) + ' '
            lines += "\n"
        
        if s.total_items() == 0:
            lines = lines.split('\n')[0] + "\n - Empty -"
        lines += f"""\n
Stats:
 - Health:{player.health:g} Balance:{player.balance:g} -
 - dmg:{player.attack_damage:.0f} atkspeed:{player.attack_speed:.1f} range:{player.attack_range:.0f} -
"""
        if s.total_items() > 0:
            lines += f"\nDescription: {s.rows[s.col_cur][s.row_cur].description}"
        print(lines)
        time.sleep(2/3)
