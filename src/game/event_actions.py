import time
from typing import List
from multiprocessing import Process

from getkey import getkey, keys

from entities import *
from utils import utils


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