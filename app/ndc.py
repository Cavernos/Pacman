import pyxel

class Sprite:
    def __init__(self, resources, x, y):
        self.resources = resources
        self.x, self.y = x, y
        self.width, self.height = 8,8

    def update(self):
        pass
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 24, 16, self.width, self.height)

class Hero(Sprite):
    def __init__(self, resources, x, y):
        super().__init__(resources, x, y)

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
        self.resources = pyxel.load("..\\assets\\2.pyxres")
        self.hero = Hero(self.resources, 0, 0)
        pyxel.run(self.update, self.draw)

    def update(self):
        pass
    def draw(self):
        pyxel.cls(0)
        self.hero.draw()
        
        


# Pyxel app Running
if __name__ == "__main__":
    App()
