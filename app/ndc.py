import pyxel

class Sprite:
    def __init__(self):
        pass

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

    def update(self):
        pass
    def draw(self):
        pass
        
        


# Pyxel app Running
if __name__ == "__main__":
    App()
