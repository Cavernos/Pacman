import pyxel

class Sprite:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.width, self.height = 8,8

    def update(self):
        if pyxel.btnp(pyxel.KEY_D):
            self.x = self.x + 1

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 24, 16, self.width, self.height)

class Hero(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)

class IA(Sprite):
    def __init__(self):
        super().__init__()

class Level:
    def __init__(self) -> None:
        pass

    def update(self):

    def draw(self):
        

class Tree(Level):
    def __init__(self) -> None:
        super().__init__()

class App:
    def __init__(self):
        pyxel.init(128, 128)
        self.resources = pyxel.load("..\\assets\\2.pyxres")
        self.hero = Hero(0, 0)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        self.hero.update()
    def draw(self):
        pyxel.cls(0)
        self.hero.draw()
        
        


# Pyxel app Running
if __name__ == "__main__":
    App()
