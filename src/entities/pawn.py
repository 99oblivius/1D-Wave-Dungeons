from typing import Optional

from items import Item, ItemType

class Pawn:
    last_attack = -1.0

    def __init__(self,
            pos: float = 0.0,
            left_facing: bool = False,
            health: float = 0.0,
            speed: float = 0.0,
            render: str = 'O',
            attack_damage: float = 0.0,
            attack_render: str = ' ',
            attack_range: int = 0,
            attack_speed: float = 1.0):
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
        self._pos -= self.speed

    def right(self):
        self._pos += self.speed

    def damage(self, target) -> bool:
        if not isinstance(target, Pawn):
            return False
        target.health = max(0.0, target.health - self.attack_damage)
        return True


class Player(Pawn):
    def __init__(self,
        pos: int = 0,
        health=100.0,
        speed=1.0,
        render='p',
        attack_render='~',
        attack_damage=20,
        attack_range=2,
        attack_speed=1.0
    ):
        super().__init__(
            pos=pos,
            health=health,
            speed=speed,
            render=render,
            attack_render=attack_render,
            attack_damage=attack_damage,
            attack_range=attack_range,
            attack_speed=attack_speed)
        
        self.defaults = {
            'health': health,
            'attack_damage': attack_damage,
            'attack_range': attack_range,
            'attack_speed': attack_speed,
        }
        self.score = 0
        self.balance = 9999
        self.inventory = {item_type: [] for item_type in ItemType}
    
    def buy_item(self, item: Item) -> bool:
        if self.balance >= item.price:
            item.count -= 1
            item = item.take()
            self.balance -= item.price

            location = self.inventory[item.item_type]
            for it in location:
                if it == item:
                    location[location.index(item)].count += 1
                    break
            else:
                location.append(item)
                self.inventory[item.item_type] = sorted(
                    self.inventory[item.item_type],
                    key=lambda x: (-x.count, -x.strength)
                )
                print(self.inventory[item.item_type])
            if item.item_type == ItemType.EFFECT:
                self.use_item(item, self)
            return True
        return False

    def use_item(self, item: Item, target: Pawn):
        if item.count > 0:
            item.use(target)
        if item.count == 0:
            self.inventory[item.item_type].remove(item)
    
    def reset(self):
        self.pos = 0
        self.score = 0
        self.left_facing = False
        self.render = 'p'
        self.items = []

        self.health = self.defaults['health']
        self.attack_damage = self.defaults['attack_damage']
        self.attack_range = self.defaults['attack_range']
        self.attack_speed = self.defaults['attack_speed']

    
    def update(self, state):
        self.pos = 0
        self.left_facing = False
        self.render = 'p'
        self.health += state.rounds * 2.5  # make items scale it
        self.attack_damage += self.score**1.125

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

    def __init__(self,
            pos: Optional[int] = None,
            health=100.0,
            speed=0.5,
            render='E',
            attack_render='-',
            points=1,
            *args,
            **kwargs):
        super().__init__(
            health=health,
            speed=speed,
            render=render,
            attack_render=attack_render,
            *args,
            **kwargs)
        self.points = points
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