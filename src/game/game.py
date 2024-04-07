import time

from typing import List

from items import items
from entities import *
from . import (
    actions,
    states,
    renderer, 
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
            balance=30,
            render='p',
            attack_render='~',
            attack_damage=20,
            attack_range=2,
            attack_speed=1.0)
        
        self.shop = [
            items.Dummy(name="Health"),
            items.RejuvenationBead( price=5,    strength=50,                    count=2), 
            items.MedKit(           price=10,   strength=100,                   count=4), 
            items.CrimsonFlask(     price=20,   strength=250,                   count=6),
            items.HiElixir(         price=40,   strength=400,                   count=44),
            items.Dummy(),
            items.Dummy(),

            items.Dummy(name="Attack"),
            items.SplashStrength(   price=20,   strength=3,     duration=1,     count=10),
            items.Dirk(             price=40,   strength=2,     duration=5,     count=5),
            items.LongSword(        price=100,  strength=10,                    count=2),
            items.Dummy(),
            items.Dummy(),
            items.Dummy(),

            items.Dummy(name="Haste"),
            items.Quicksilver(      price=10,   strength=1,                     count=1),
            items.SwiftDagger(      price=40,   strength=2,                     count=2),
            items.HasteHelm(        price=100,  strength=10,                    count=2),
            items.Dummy(name="Reach"),
            items.Exaltion(         price=10,   strength=1,     duration=2,     count=1),
            items.Aura(             price=40,   strength=2,     duration=4,     count=2),

            items.Dummy(name="Weapons (unimplemented)"),
            items.Excalibur(        price=100,  damage=1),
            items.Murasame(         price=180,  damage=2),
        ]
    
    def game_loop(self) -> int:
        state = self.state
        entities = self.entities
        
        utils.clear_screen()

        data = (state, entities.player, self.shop)
        if state.round_ended:
            if state.ingame:
                state.rounds += 1
                state.total_rounds += 1
                state.round_end = time.time()
            state.ingame = False
        
        if state.slaughtered or state.escaped:
            entities.player.update(state)
        elif state.died:
            state.rounds = 0
            state.deaths += 1
            state.difficulty = 1
            entities.player.reset()
        state.max_rounds = max(state.max_rounds, state.rounds)
            
        if state.ingame:
            actions.main_menu(*data, "MENU")
        elif state.slaughtered or state.escaped:
            actions.main_menu(*data, menus.win_screen(state, entities.player, state.round_time), won=True)
        elif state.died:
            actions.main_menu(*data, menus.lost_message(state, entities.player))
        else:
            actions.main_menu(*data, menus.menu_welcome())
        
        if state.playing:
            state.playspace = 12 * state.difficulty

            if not state.ingame:
                state.round_start = time.time()
                state.round_end = None
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
            
            state.frame_time = 1.0 / state.tickrate
            state.died = False
            state.slaughtered = False
            state.escaped = False
            state.ingame = True

            print(menus.start_header(state, entities))
        
        while state.playing:
            self.t_start = time.time()
            
            actions.user_input(state, entities)

            renderer.game(state, entities)
            
            update_handler.update(state, entities)

            self.tick()
            

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
    
    def tick(self):
        self.state.delta_time = time.time() - self.t_start
        time.sleep(max(0, 1.0 / self.state.tickrate - self.state.delta_time))
        self.state.frame_time = time.time() - self.t_start