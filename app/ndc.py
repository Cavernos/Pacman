import pyxel

class Sprite:
    def __init__(self, resources):
        self.resources = resources
    def draw(self):
        pyxel.blt(0, 0)

class Hero(Sprite):
    def __init__(self):
        super().__init__()

class IA(Sprite):
    def __init__(self):
        super().__init__()

class Level:
    def __init__(self) -> None:
        pass

class Tree(Level):
    def __init__(self) -> None:
        super().__init__()

class App:
    def __init__(self):
        pyxel.init(128, 128)
        self.resources = pyxel.load("assets/2.pyxres", 0)
        self.hero = Hero()

    def update(self):
        pass
    def draw(self):
        pyxel.cls(0)
        self.hero.draw()
        
        


# Pyxel app Running
if __name__ == "__main__":
    App()
