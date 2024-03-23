import time

from multiprocessing import Process
from typing import List, Optional

from getkey import getkey, keys


instructions = " - Move: A,D,←,→  Attack: W,↑,SPACE -"
header_func = lambda health, attack_damage, boss_health: f" - HP:{health:02.0f} - DMG:{attack_damage:02.0f} - BOSS:{boss_health:.0f} -"
footer_func = lambda rounds, score, framerate, elapsed: f" - r:{int(rounds)} s:{score} fps:{framerate:.0f} - t:{elapsed:.0f} -"

def clear_screen():
  print(end="\033c", flush=True)

def clamp(x, a, b):
  assert (a <= b)
  return max(a, min(b, x))

def plural(value) -> str:
  return 's' if value != 1 else ''


class Pawn:
  last_attack = -1.0

  def __init__(self,
               pos: Optional[float] = None,
               left_facing: bool = False,
               health: float = 0.0,
               speed: float = 0.0,
               render: str = 'O',
               attack_damage: float = 1.0,
               attack_render: str = ' ',
               attack_range: int = 0,
               attack_speed: float = 2.0):
    self._pos = pos
    self.left_facing = left_facing
    self.health = health
    self.speed = speed
    self.render = render
    self.attack_damage = attack_damage
    self.attack_render = attack_render
    self.attack_range = attack_range
    self.attack_speed = attack_speed

  def __str__(self):
    attributes = ", ".join(f"{key}={value}"
                           for key, value in vars(self).items())
    return f"{self.__class__.__name__}({{{attributes}}})"

  def __repr__(self):
    attributes = ", ".join(f"{key}={value}"
                           for key, value in vars(self).items())
    return f"{self.__class__.__name__}({{{attributes}}})"

  @property
  def pos(self) -> int:
    if self._pos - int(self._pos) < 0.5:
      return int(self._pos)
    else:
      return int(self._pos) + 1

  @pos.setter
  def pos(self, value):
    self._pos = float(value)

  def left(self):
    self.pos -= self.speed

  def right(self):
    self.pos += self.speed

  def damage(self, target) -> bool:
    if not isinstance(target, Pawn):
      return False
    target.health -= self.attack_damage
    return True


class Player(Pawn):
  score = 0
  
  def __init__(self,
               pos: Optional[int] = None,
               health=100.0,
               render='p',
               attack_render='~',
               speed=1.0,
               *args,
               **kwargs):
    super().__init__(health=health,
                     render=render,
                     attack_render=attack_render,
                     speed=speed,
                     *args,
                     **kwargs)
    if pos is not None:
      self._pos = pos

  def left(self):
    if self.left_facing:
      self._pos -= self.speed
    else:
      self.left_facing = True
      self.render = 'q'

  def right(self):
    if self.left_facing:
      self.left_facing = False
      self.render = 'p'
    else:
      self._pos += self.speed


class Enemy(Pawn):
  points = 1

  def __init__(self,
               pos: Optional[int] = None,
               health=100.0,
               speed=0.5,
               render='E',
               attack_render='-',
               *args,
               **kwargs):
    super().__init__(health=health,
                     speed=speed,
                     render=render,
                     attack_render=attack_render,
                     *args,
                     **kwargs)
    if pos is not None:
      self._pos = pos
    self.left_facing = True

  def left(self):
    if self.left_facing:
      self._pos -= self.speed
    else:
      self.left_facing = True

  def right(self):
    if self.left_facing:
      self.left_facing = False
    else:
      self._pos += self.speed


class Effect:
  def __init__(self, pos: int, render: str = '~', lifetime: float = 1.0):
    self.pos = pos
    self.render = render
    self.lifetime = lifetime


class Game:
  process = None
  tickrate = 60
  delta_time = 1.0 / tickrate
  frame_buffer = ""
  rounds = 0
  player = Player(pos=0,
                  health=100.0,
                  attack_damage=20,
                  attack_speed=2.0,
                  attack_range=4)

  def __init__(self, difficulty: int = 1):
    self.running = False

    self.game_start_time = time.time()
    self.difficulty = difficulty
    self.playspace = 10 * difficulty

    self.player.pos = 0
    self.player.left_facing = False
    self.player.render = 'p'
    self.player.health += self.rounds * 2.5
    self.player.attack_damage += self.player.score**1.125

    self.enemies: List[Enemy] = [
        Enemy(pos=int(self.playspace * 0.8 - (3 * n)),
              speed=1 / 3,
              health=100.0 + (difficulty - 1) * 4**(difficulty / 3),
              attack_damage=clamp((difficulty - 1)**0.5 / 2.5 + 1, 20, 100.0),
              attack_range=1,
              attack_speed=1.0)
        for n, _ in enumerate(range(int(difficulty * difficulty / 3 + 1)))
    ]
    self.effects: List[Effect] = []

    header = header_func(self.player.health, self.player.attack_damage,
                         sum(enemy.health for enemy in self.enemies))
    print(f"""{instructions}\n{header}\n - Difficulty {difficulty} chosen!""")

  def game_loop(self):
    self.frame_time = 1.0 / self.tickrate
    self.rounds += 1
    while self.running:
      last_time = time.time()

      self.user_input()

      self.render()
      self.update_logic()
      start_time = time.time()
      self.delta_time = start_time - last_time

      time.sleep(max(0, 1.0 / self.tickrate - self.delta_time))
      self.frame_time = time.time() - last_time

  def update_logic(self):
    # Effect update
    kill = []
    for effect in self.effects:
      effect.lifetime -= self.delta_time
      if effect.lifetime <= 0:
        kill.append(effect)
    for effect in kill:
      self.effects.remove(effect)

    # Enemy update
    kill = []
    for n, enemy in enumerate(self.enemies):
      old_positions = self.enemies[n + 1:]
      if enemy.pos > self.player.pos + enemy.attack_range:
        blocked = any(
            (True for e in old_positions if -1 < enemy.pos - e.pos < 2))
        if not blocked:
          enemy.left()

      elif enemy.pos < self.player.pos - enemy.attack_range:
        blocked = any(
            (True for e in old_positions if -1 < e.pos - enemy.pos < 2))
        if not blocked:
          enemy.right()
      else:
        self.attacking(enemy, [self.player])

      if enemy.health <= 0:
        self.player.score += enemy.points
        kill.append(enemy)
    for enemy in kill:
      self.enemies.remove(enemy)

    # Player update
    died = self.player.health <= 0.0
    slaughtered = all(enemy.health <= 0 for enemy in self.enemies)
    escaped = self.player.pos > self.playspace - 1
    if any((died, slaughtered, escaped)):
      clear_screen()

      if slaughtered or escaped:
        print(f""" - YOU WIN! -
Score: {self.player.score}
 - It took you {int(time.time() - self.game_start_time)} seconds! -
Maybe you can play again and do better? Y/n:\n""")
      else:
        print(""" - You LOST... -
Play again and win? Y/n:\n""")

      time.sleep(2 / 3)
      choice = None
      while choice not in ('y', 'n', '\n', keys.SPACE):
        choice = getkey()
      clear_screen()
      if choice in ('y', keys.SPACE, '\n'):
        if died:
          self.player.health = 100.0
          self.player.attack_damage = 20
          self.player.score = 0
          self.rounds = 0
        else:
          print("Should the difficulty increase? y/N:")
          choice = None
          while choice not in ('y', 'n', '\n', keys.SPACE):
            choice = getkey()
          clear_screen()
          if choice == 'y':
            self.difficulty += 1
        self.__init__(difficulty=self.difficulty)
        self.close()
        self.start()
        for enemy in self.enemies:
          enemy.points += 1
      else:
        self.running = False
        print(f""" - Thank you for playing The Trans Academy Week 4 PvP Game! -
      Made by yours truly - Livia
You scored {self.player.score} point{plural(self.player.score)} in {self.rounds} round{plural(self.rounds)}!
 - Come again soon <3 -""")
    return

  def user_input(self):
    key = getkey()
    if key == keys.ESCAPE:
      self.running = False
    if key in ('w', keys.SPACE, keys.UP):
      self.attacking(self.player, self.enemies)
    if key == keys.LEFT or key == 'a':
      self.player.left()
    elif key == keys.RIGHT or key == 'd':
      self.player.right()

  def attacking(self, attacker: Pawn, targets: List[Enemy]):
    if attacker.last_attack + 1 / attacker.attack_speed > time.time():
      return

    # Place effects
    self.effects.extend([])
    for n in range(attacker.attack_range):
      effect_pos = (-1)**int(attacker.left_facing) * (n + 1) + attacker.pos
      self.effects.append(
          Effect(pos=effect_pos, render=attacker.attack_render, lifetime=0.15))

      for target in targets:
        if target.pos == effect_pos:
          attacker.damage(target)
    attacker.last_attack = time.time()

  def render(self):
    field = ['_'] * self.playspace
    for i in self.enemies + self.effects + [self.player]:
      if i.pos is not None and 0 <= i.pos < self.playspace:
        field[i.pos] = i.render
    clear_screen()
    header = header_func(self.player.health, self.player.attack_damage,
                         sum(enemy.health for enemy in self.enemies))
    footer = footer_func(self.rounds, self.player.score, 1.0 / self.frame_time,
                         time.time() - self.game_start_time)
    self.frame_buffer += f"{instructions}\n{header}\n{''.join(field)}\n{footer}"
    print(self.frame_buffer)
    self.frame_buffer = ""

  def start(self):
    self.running = True
    self.game_loop()

  def pause(self):
    if self.process.is_alive():
      return self.process.suspend()
    self.process.resume()

  def close(self):
    self.running = False


if __name__ == '__main__':
  difficulties = range(1, 5)
  difficulty = -1
  pick = 1
  
  def choose_difficulty():
    blink = False
    while True:
      blink = not blink
      clear_screen()
      choices = ""
      for n in difficulties:
        choices += f"{'X' if blink and pick == n else n}. {'<-' if pick == n else ''}\n"
      print(f""" -- Welcome to The Trans Academy Week 4 PvP Game! --
  Select your difficulty:
  {choices}""")
      time.sleep(2 / 3)
  
  choosing = Process(target=choose_difficulty)
  choosing.start()
  while True:
    key = getkey()
    if key in (keys.DOWN, keys.PAGE_DOWN, 's', 'j'):
      pick = pick % len(difficulties) + 1
    elif key in (keys.UP, keys.PAGE_UP, 'w', 'k'):
      pick = (pick - 2) % len(difficulties) + 1
    elif key == keys.HOME:
      pick = difficulties[0]
    elif key == keys.END:
      pick = difficulties[-1]
    elif key == keys.SPACE or key == keys.ENTER:
      break
    else:
      continue
    choosing.terminate()
    choosing = Process(target=choose_difficulty)
    choosing.start()
  if choosing.is_alive():
    choosing.terminate()
  clear_screen()
  
  game = Game(difficulty=pick)
  game.start()
