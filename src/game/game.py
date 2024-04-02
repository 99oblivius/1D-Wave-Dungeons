import time

from typing import List

from items import *
from entities import *
from . import (
    states,
    renderer, 
    event_handler, 
    update_handler
)

from getkey import getkey

from utils import utils, menus


class Entities:
    def __init__(self):
        self.player = None
        self.enemies: List[Enemy] = []
        self.effects: List[Effect] = []


class Game:
    state = states.GameState()
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
        
        self.shop = [
            Dummy(name="Health Potions"),
            HealthPotion(price=5, strength=50, count=2), 
            HealthPotion(price=10, strength=100, count=4), 
            HealthPotion(price=20, strength=250, count=6),
            HealthPotion(price=40, strength=400, count=44),
            Dummy(),
            Dummy(),

            Dummy(name="Strength Potions"),
            StrengthPotion(price=20, strength=1, count=10),
            StrengthPotion(price=40, strength=2, count=5),
            StrengthPotion(price=100, strength=10, count=2),
            Dummy(name="Range Boost"),
            RangeBoost(price=10, strength=1, count=1),
            RangeBoost(price=40, strength=2, count=2),

            Dummy(name="Speed Boost"),
            SpeedPotion(price=10, strength=1, count=1),
            SpeedPotion(price=40, strength=2, count=2),
            SpeedPotion(price=100, strength=10, count=2),
            Dummy(),
            Dummy(),
            Dummy(),

            Dummy(name="Weapons"),
            Excalibur(price=100, damage=1)
        ]
    
    def game_loop(self) -> int:
        state = self.state
        entities = self.entities
        
        utils.clear_screen()

        data = (state, entities.player, self.shop)
        if state.round_ended:
            state.ingame = False
            state.total_rounds += 1
            if not state.round_end:
                state.round_end = time.time()
                
            if state.slaughtered or state.escaped:
                event_handler.main_menu(*data, menus.win_screen(state, entities.player, state.round_time), won=True)
            elif state.died:
                event_handler.main_menu(*data, menus.lost_message(state, entities.player))
        else:
            if state.ingame:
                event_handler.main_menu(*data, "MENU")
            else:
                event_handler.main_menu(*data, menus.menu_welcome())
        
        if state.playing:
            state.max_rounds = max(state.max_rounds, state.rounds)
            if not state.ingame:
                state.round_start = time.time()
                state.round_end = None
            if state.died:
                entities.player.reset()
                state.rounds = 0
                state.total_rounds += 1
                state.deaths += 1
                state.difficulty = 1
            elif state.slaughtered or state.escaped:
                entities.player.update(state)
            else:
                state.rounds = 0
            
            state.ingame = True
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
        print(menus.ending_thanks(self.state, self.entities.player))
        getkey()

    def pause(self):
        if self.process is not None:
            if self.process.is_alive():
                return self.process.suspend()
            self.process.resume()

    def close(self):
        self.state.playing = False
        self.state.run = False