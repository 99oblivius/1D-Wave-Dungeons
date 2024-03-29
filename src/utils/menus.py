import time

from utils import utils


def menu_welcome() -> str:
    return " - Welcome to 1D-Wave-Dungeons - "

def instructions() -> str:
    return " - Move: A,D,←,→  Attack: W,↑,SPACE -"

def header_func(health, attack_damage, boss_health) -> str:
    return f" - HP:{health:02.0f} - DMG:{attack_damage:02.0f} - BOSS:{boss_health:.0f} -"

def footer_func(rounds, score, framerate, elapsed) -> str:
    return f" - r:{int(rounds)} s:{score} fps:{framerate:.0f} - t:{elapsed:.0f} -"

def lost_message(state, player) -> str:
    return f""" - You LOST... -
  Round{utils.plural(state.rounds)}: {state.rounds}
  Score: {player.score}
"""

def win_screen(state, player) -> str:
    return f""" - YOU WIN! -
- It took you {int(time.time() - state.game_start_time)} seconds! -
  Round{utils.plural(state.rounds)}: {state.rounds}
  Score: {player.score}
"""

def ending_thanks(state, player) -> str:
    return f""" - Thank you for playing 1D-Wave-Dungeons! -
You scored {player.score} point{utils.plural(player.score)}
 in {state.rounds} round{utils.plural(state.rounds)}!
 - Come again soon -
 - Made by yours truly <3 Livia
Press any key to exit..."""

def start_header(state, entities) -> str:
    header = header_func(entities.player.health, entities.player.attack_damage, sum(enemy.health for enemy in entities.enemies))
    return f"""{instructions()}\n{header}\n - Difficulty {state.difficulty} chosen!"""