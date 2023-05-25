import pyxel

class Sprite:
    def __init__(self, x, y, text_x, text_y):
        self.x, self.y = x, y
        self.width, self.height = 8,8
        self.texture_pos_x, self.texture_pos_y = text_x, text_y 

    def update(self):
        if self.y <= 0 or self.y >= 128:
            self.y = 0
        if self.x <= 0 or self.x >= 128:
            self.x = 0
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            self.x = self.x + 1
        elif pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            self.y = self.y + 1
        elif pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_UP):
            self.y = self.y - 1
        elif pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_LEFT):
            self.x = self.x - 1
            

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.texture_pos_x, self.texture_pos_y, self.width, self.height)

class Hero(Sprite):
    def __init__(self, x, y, text_x, text_y):
        super().__init__(x, y, text_x, text_y)

class IA(Sprite):
    def __init__(self):
        super().__init__()

class Level:
    def __init__(self) -> None:
        pass

    def update(self):
        pass
    def draw(self):
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128)

class Tree(Level):
    def __init__(self) -> None:
        super().__init__()

class App:
    def __init__(self):
        pyxel.init(128, 128)
        self.resources = pyxel.load("..\\assets\\2.pyxres")
        self.hero = Hero(0, 0)
        self.level = Level()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        self.hero.update()
    def draw(self):
        pyxel.cls(0)
        self.level.draw()
        self.hero.draw()
        
        
        


# Pyxel app Running
if __name__ == "__main__":
    App()
