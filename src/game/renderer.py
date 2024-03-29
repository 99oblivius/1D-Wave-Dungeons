import time

from typing import List
from multiprocessing import Process

from getkey import getkey, keys

from utils import utils, menus


def render(state, entities):
    frame_buffer = ""
    field = ['_'] * state.playspace
    for i in entities.enemies + entities.effects + [entities.player]:
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
            time.time() - state.game_start_time)
        
        frame_buffer += f"{menus.instructions()}\n{header}\n{''.join(field)}\n{footer}"
        print(frame_buffer)
        frame_buffer = ""

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
