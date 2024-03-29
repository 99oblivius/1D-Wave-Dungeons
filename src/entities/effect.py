class Effect:
    def __init__(self, pos: int, render: str = '~', lifetime: float = 1.0):
            self.pos = pos
            self.render = render
            self.lifetime = lifetime