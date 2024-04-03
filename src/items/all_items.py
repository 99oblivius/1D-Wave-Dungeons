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
        item_type: ItemType=ItemType.MISCEL
    ):
        self.name = name
        self.price = price
        self.strength = strength
        self.count = count
        self.item_type: ItemType = item_type
    
    def __str__(self):
        return f"{self.name}"
    
    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return all((
            self.item_type == other.item_type, 
            self.name == other.name, 
            self.strength == other.strength))
    
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



class StrengthPotion(Item):
    def __init__(self, price: int=10, strength: int=10, *args, **kwargs):
        super().__init__(
            name="Strength Pot", 
            price=price, 
            strength=strength, 
            item_type=ItemType.ACTIVE, 
            *args, **kwargs)
    
    def use(self, player: 'Player'):
        self.count -= 1
        player.attack_damage *= 1 + self.strength / 10
    
    def __str__(self):
        return f"{self.name} - {self.strength}"

class SpeedPotion(Item):
    def __init__(self, price: int=10, strength: int=1, *args, **kwargs):
        super().__init__(
            name="Speed Pot", 
            price=price, 
            strength=strength, 
            item_type=ItemType.ACTIVE, 
            *args, **kwargs)
    
    def use(self, player: 'Player'):
        self.count -= 1
        player.attack_speed += self.strength / 3
    
    def __str__(self):
        return f"{self.name} - {self.strength}"



class RangeBoost(Item):
    def __init__(self, price: int=10, strength: int=1, *args, **kwargs):
        super().__init__(
            name="Range Boost", 
            price=price, 
            strength=strength, 
            item_type=ItemType.EFFECT, 
            *args, **kwargs)
    
    def use(self, player: 'Player'):
        self.count -= 1
        player.attack_range += self.strength
    
    def __str__(self):
        return f"{self.name} - {self.strength}"


class HealthPotion(Item):
    def __init__(self, price: int=5, strength: int=50, *args, **kwargs):
        super().__init__(
            name="Instant Health", 
            price=price, 
            strength=strength, 
            item_type=ItemType.EFFECT, 
            *args, **kwargs)
    
    def use(self, player: 'Player'):
        self.count -= 1
        player.health += self.strength
    
    def __str__(self):
        return f"{self.name} - {self.strength}"



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