import time

from utils import utils, menus
from items import ItemType
from . import (
    states, 
)


def menu(pick, title, choices):
    blink = False
    while True:
        blink = not blink
        utils.clear_screen()
        options = f"{title}\n"
        for n, choice in enumerate(choices, start=1):
            options += f"{'X' if blink and pick == n else n}. {choice + ' <-' if pick == n else choice}\n"
        print(options)
        time.sleep(2/3)

def game(state, entities):
    frame_buffer = ""
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
            state.rounds, 
            entities.player.score, 1.0 / state.frame_time,
            time.time() - state.round_start)
        
        frame_buffer += f"{menus.instructions()}\n{header}\n{''.join(field)}\n{footer}"
        print(frame_buffer)
        frame_buffer = ""

def shop(s: states.ShopState, player, items):
    blink = False
    while True:
        blink = not blink
        utils.clear_screen()
        options = menus.shop_header(s.current_page, s.total_pages)
        
        if s.total_items == 0: options += f"\n - No Items -"
        
        start_index = s.current_page * s.items_per_page
        end_index = min(start_index + s.items_per_page, s.total_items)
        for n, item in enumerate(items[start_index:end_index], start=1):
            n = n+start_index
            if item.count < 0:
                options += menus.shop_dummy(n, blink, s.cursor_position, item)
                continue

            if s.bought == n:
                name = utils.obfuscated(str(item), '~')
                s.bought = 0
            elif player.balance < item.price:
                name = utils.obfuscated(str(item), '$')
            else: name = str(item)
            options += menus.shop_item(n, blink, s.cursor_position, item, name)
        options += f"\n - Wallet: {player.balance} -\n"
        print(options)
        time.sleep(2/3)

def inventory(s: states.InventoryState):
    blink = False
    while True:
        blink = not blink
        utils.clear_screen()
        options = " - Inventory -\n"
        
        for col in s.cols:
            options += utils.ellipse_justified(f"  {ItemType.typename(col)}  ", s.menu_col_width)
        options += "\n"
        for r in range(s.menu_height):
            for n, col in enumerate(s.cols):
                if r > len(s.rows[n]) - 1:
                    options += ' ' * s.menu_col_width
                else:
                    item = s.rows[n][r]
                    index = 'X' if blink and (s.row_cur == r and s.col_cur == n) else '•'
                    options += utils.ellipse_justified(f"{index} {item.count}x {item}", s.menu_col_width-1) + ' '
            options += "\n"
        
        if s.total_items() == 0:
            options = options.split('\n')[0] + "\n - Empty -"
        print(options)
        time.sleep(2/3)