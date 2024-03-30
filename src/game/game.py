import time

from typing import List

from entities import *
from . import (
    renderer, 
    event_actions,
    event_handler, 
    update_handler
)

from utils import utils, menus

class State:
    def __init__(self, 
        process=None, 
        playing=False
    ):
        self.game_start_time = None
        self.process = process
        self.playing = playing
        self.run = True
        self.died = False
        self.slaughtered = False
        self.escaped = False

        self.difficulty = 1
        self.playspace = 12
        self.rounds = 0

        self.tickrate = 6
        self.delta_time = 1.0 / self.tickrate
        self.frame_time = 0.0


class Entities:
    def __init__(self):
        self.player = None
        self.enemies: List[Enemy] = []
        self.effects: List[Effect] = []


class Game:
    state = State()
    entities = Entities()
    def __init__(self):
        self.entities.player = Player(
            health=100,
            speed=1.0,
            render='p',
            attack_render='~',
            attack_damage=20,
            attack_range=2,
            attack_speed=1.0)
    
    def game_loop(self) -> int:
        state = self.state
        entities = self.entities
        
        utils.clear_screen()
        if state.slaughtered or state.escaped:
            event_handler.main_menu(state, entities.player, menus.win_screen(state, entities.player), won=True)
        elif state.died:
            event_handler.main_menu(state, entities.player, menus.lost_message(state, entities.player))
        else:
            event_handler.main_menu(state, entities.player, menus.menu_welcome())
        
        if state.playing:
            if state.died:
                entities.player.reset()
                state.rounds = 0
                state.difficulty = 1
            elif state.slaughtered or state.escaped:
                entities.player.update(state)
            else:
                state.rounds = 0
            
            state.frame_time = 1.0 / state.tickrate
            state.rounds += 1
            state.playspace = 12 * state.difficulty
            state.died = False
            state.slaughtered = False
            state.escaped = False

            entities.enemies = [Enemy(
                pos=int(state.playspace * 0.8 - 3 * n),
                speed=1 / 5,
                health=100.0 + (state.difficulty - 1) * 4**(state.difficulty / 3),
                attack_damage=utils.clamp((state.difficulty - 1)**0.5 / 2.5 + 1, 20, 100.0),
                attack_range=1,
                attack_speed=0.5,
                points=state.rounds+1)
            for n, _ in enumerate(range(int(state.difficulty * state.difficulty / 3 + 1)))]
            entities.effects = []
            print(menus.start_header(state, entities))

        while state.playing:
            last_time = time.time()
            
            event_handler.user_input(state, entities)

            renderer.render(state, entities)
            
            update_handler.update(state, entities)
            
            start_time = time.time()
            state.delta_time = start_time - last_time

            time.sleep(max(0, 1.0 / state.tickrate - self.state.delta_time))
            state.frame_time = time.time() - last_time

    def start(self):
        self.state.game_start_time = time.time()
        while self.state.run:
            self.game_loop()
        input(menus.ending_thanks(self.state, self.entities.player))

    def pause(self):
        if self.process is not None:
            if self.process.is_alive():
                return self.process.suspend()
            self.process.resume()

    def close(self):
        self.state.playing = False
        self.state.run = False