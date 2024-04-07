from copy import deepcopy

from .item_type import ItemType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities import Player


class Weapon:
    def __init__(self, damage: float=1.0):
        self.damage = damage

    def equip(self):
        pass

    def unequip(self):
        pass


class Item:
    def __init__(self, 
        name: str="", 
        price: int=1, 
        strength: int=1, 
        count: int=1, 
        item_type: ItemType=ItemType.MISCEL,
        duration: int=0
    ):
        self.name = name
        self.price = price
        self.strength = strength
        self.count = count
        self.item_type: ItemType = item_type
        self.duration: int = duration
    
    def __str__(self):
        return f"{self.name}"
    
    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return all((
            self.item_type == other.item_type, 
            self.name == other.name, 
            self.strength == other.strength))

    @property
    def description(self):
        return f"""{self.name}"""
    
    def use(self, player: 'Player'):
        pass

    def take(self, amount: int=1):
        item = deepcopy(self)
        item.count = amount
        return item


class Dummy(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(
            price=0, 
            count=-1, 
            item_type=ItemType.DUMMY,
            *args, **kwargs)




class Reach(Item):
    def __init__(self, name="Range Boost", price: int=10, strength: int=1, item_type: ItemType=ItemType.ACTIVE, duration: int=0, *args, **kwargs):
        super().__init__(
            name=name, 
            price=price, 
            strength=strength, 
            item_type=item_type, 
            duration=duration,
            *args, **kwargs)
    
    def use(self, player: 'Player'):
        self.count -= 1
        player.attack_range += self.strength
    
    def __str__(self):
        return f"{self.name}"

class Exaltion(Reach):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Exaltion",*args, **kwargs)
    @property
    def description(self):
        return f"""{self.name} price:{self.price}
Your reach will grow by {self.strength}, and Exaltion will last {self.duration} rounds."""

class Aura(Reach):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Aura", *args, **kwargs)
    @property
    def description(self):
        return f"""{self.name} price:{self.price}
Gain {self.strength} reach for {self.duration} rounds. 
Aura won't disapoint."""




class Health(Item):
    def __init__(self, name="Instant Health", price: int=5, strength: int=50, item_type: ItemType=ItemType.EFFECT, duration: int=0, *args, **kwargs):
        super().__init__(
            name=name, 
            price=price, 
            strength=strength, 
            item_type=item_type, 
            duration=duration,
            *args, **kwargs)
    
    def use(self, player: 'Player'):
        self.count -= 1
        player.health += self.strength
    
    def __str__(self):
        return f"{self.name}"

class RejuvenationBead(Health):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Rejuvenation Bead", *args, **kwargs)
    @property
    def description(self):
        return f"""{self.name} price:{self.price}
Heal instantly and regenerate {self.strength}hp each round from now on."""

class MedKit(Health):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Med-Kit", *args, **kwargs)
    @property
    def description(self):
        return f"""{self.name} price:{self.price}
Heal a whole {self.strength}hp. It's a medkit. What else do you expect."""

class CrimsonFlask(Health):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Crimson Flask", *args, **kwargs)
    @property
    def description(self):
        return f"""{self.name} price:{self.price}
Chug for {self.strength}hp recovery."""

class HiElixir(Health):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Hi-Elixir", *args, **kwargs)
    @property
    def description(self):
        return f"""{self.name} price:{self.price}
It's magical or something. Instantly heal {self.strength}hp."""




class Strength(Item):
    def __init__(self, name: str="Strength Pot", price: int=10, strength: int=10, item_type: ItemType=ItemType.ACTIVE, duration: int=0, *args, **kwargs):
        super().__init__(
            name=name, 
            price=price, 
            strength=strength, 
            item_type=item_type, 
            duration=duration,
            *args, **kwargs)
    
    def use(self, player: 'Player'):
        self.count -= 1
        player.attack_damage *= 1 + self.strength / 10
    
    def __str__(self):
        return f"{self.name}"

class SplashStrength(Strength):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Splash", item_type=ItemType.EFFECT, *args, **kwargs)
    @property
    def description(self):
        return f"""{self.name} price:{self.price}
Gain {self.strength} for the next round."""

class Dirk(Strength):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Dirk", *args, **kwargs)
    @property
    def description(self):
        return f"""{self.name} price:{self.price}
For the long duration of {self.duration} rounds, gain {self.strength} damage."""

class LongSword(Strength):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Long Sword", *args, **kwargs)
    @property
    def description(self):
        return f"""{self.name} price:{self.price}
A sweet {self.strength} damage boost."""




class AttackSpeed(Item):
    def __init__(self, name="Haste Pot", price: int=10, strength: int=1, item_type: ItemType=ItemType.ACTIVE, duration: int=0, *args, **kwargs):
        super().__init__(
            name=name, 
            price=price, 
            strength=strength, 
            item_type=item_type, 
            duration=duration,
            *args, **kwargs)
    
    def use(self, player: 'Player'):
        self.count -= 1
        player.attack_speed += self.strength / 3
    
    def __str__(self):
        return f"{self.name}"

class Quicksilver(AttackSpeed):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Quicksilver", *args, **kwargs)
    @property
    def description(self):
        return f"""{self.name} price:{self.price}
Magic can give you that {self.strength} attack speed increase."""

class SwiftDagger(AttackSpeed):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Swiftness Dagger", *args, **kwargs)    
    @property
    def description(self):
        return f"""{self.name} price:{self.price}
Weight does make a difference. Gain {self.strength} attac speed."""

class HasteHelm(AttackSpeed):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Haste Helm", *args, **kwargs)
    @property
    def description(self):
        return f"""{self.name} price:{self.price}
This armor's special okay? {self.strength} attack speed special!"""




class Excalibur(Item, Weapon):
    def __init__(self, price: int=100, damage: float=1.0, *args, **kwargs):
        super().__init__(
            name="Excalibur Sword", 
            price=price, 
            item_type=ItemType.WEAPON, 
            *args, **kwargs)
        self.damage = damage
    
    def __str__(self):
        return f"{self.name} - {self.damage}"
    @property
    def description(self):
        return f"""{self.name} price:{self.price}
Chonky sword :3 Deals additional {self.damage} damage."""


class Murasame(Item, Weapon):
    def __init__(self, price: int=100, damage: float=2.0, *args, **kwargs):
        super().__init__(
            name="Murasame Katana", 
            price=price, 
            item_type=ItemType.WEAPON, 
            *args, **kwargs)
        self.damage = damage
    
    def __str__(self):
        return f"{self.name} - {self.damage}"
    @property
    def description(self):
        return f"""{self.name} price:{self.price}
This is a pretty one. Take care of it. {self.damage} extra damage."""

