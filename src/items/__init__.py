class Item:
    def __init__(self, name, price, count: int=1):
        self.name = name
        self.price = price
        self.count = count

    def use(self, player):
        pass

    def single(self):
        return Item(self.name, self.price, count=1)


class HealthPotion(Item):
    def __init__(self, price: int=5, strength: int=50, *args, **kwargs):
        super().__init__(name="Health Potion", price=price, *args, **kwargs)
        self.strength = strength

    def use(self, player):
        self.count -= 1
        player.health += self.strength


class StrengthPotion(Item):
    def __init__(self, price: int=10, strength: int=10):
        super().__init__(name="Strength Potion", price=price)
        self.strength = strength
    
    def use(self, player):
        self.count -= 1
        player.attack_damage *= 1 + self.strength / 10