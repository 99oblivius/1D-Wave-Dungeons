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
    def __init__(self, name="Range Boost", price: int=10, strength: int=1, item_type: ItemType=ItemType.EFFECT, duration: int=0, *args, **kwargs):
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
        return f"{self.name} - {self.strength}"

class Exaltion(Reach):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Exaltion",*args, **kwargs)

class Aura(Reach):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Aura", *args, **kwargs)




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
        return f"{self.name} - {self.strength}"

class RejuvenationBead(Health):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Rejuvenation Bead", *args, **kwargs)

class MedKit(Health):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Med-Kit", *args, **kwargs)

class CrimsonFlask(Health):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Crimson Flask", *args, **kwargs)

class HiElixir(Health):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Hi-Elixir", *args, **kwargs)




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
        return f"{self.name} - {self.strength}"

class SplashStrength(Strength):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Splash", item_type=ItemType.EFFECT, *args, **kwargs)

class Dirk(Strength):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Dirk", *args, **kwargs)

class LongSword(Strength):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Long Sword", *args, **kwargs)




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
        return f"{self.name} - {self.strength}"

class Quicksilver(AttackSpeed):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Quicksilver", *args, **kwargs)    

class SwiftDagger(AttackSpeed):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Swiftness Dagger", *args, **kwargs)    

class HasteHelm(AttackSpeed):
    def __init__(self, *args, **kwargs):
        super().__init__(name="Haste Helm", *args, **kwargs)




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

