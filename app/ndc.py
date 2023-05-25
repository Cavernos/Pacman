import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120)
        self.x = 0
        pyxel.run(self.update, self.draw)

class sprite:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        
    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.img, 0, 16, 16, 0)