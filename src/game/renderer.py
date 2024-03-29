import time

from utils import utils, menus


def render(state, entities):
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
            time.time() - state.game_start_time)
        
        frame_buffer += f"{menus.instructions()}\n{header}\n{''.join(field)}\n{footer}"
        print(frame_buffer)
        frame_buffer = ""

