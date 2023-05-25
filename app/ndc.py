import pyxel

class Sprite:
    def __init__(self, x, y, text_x, text_y):
        self.x, self.y = x, y
        self.width, self.height = 8,8
        self.texture_pos_x, self.texture_pos_y = text_x, text_y 

    def update(self):

        if (self.x < 0 and self.y > 40) and (self.x < 0 and self.y < 71): #apparait de l'autre coté de l'écran si dans la porte
            # self.x = 127
            pass
        if (self.x > 128 and self.y > 40) and (self.x > 128 and self.y < 71):
            self.x = 0
        
        if (self.y < 0 and self.x > 40) and (self.y < 0 and self.x < 71): #porte du haut
            self.y = 127
        if (self.y > 128 and self.x > 40) and (self.y > 128 and self.x < 71): #porte du bas
            self.y = 0
            pass
        if self.x <= 0 or self.x >= 128:
            self.x = 0
        if (self.x > 120 and self.y < 49) or (self.x > 120 and self.y > 70): #colision mur de droite
            self.x = 120

        if (self.y < 0 and self.x < 49) or (self.y < 0 and self.x > 70): #colision mur du haut
            self.y = 0
        if (self.y > 120 and self.x < 49) or (self.y > 120 and self.x > 70): #colision mur du bas
            self.y = 120
        

        
            
    def update_sprit(self, x, y):
        if (x%10 <= 5 or y%10 >= 5) and (self.texture_pos_x == 24 and self.texture_pos_y == 16):
            self.texture_pos_x, self.texture_pos_y = 32, 16
           
        else:
            self.texture_pos_x, self.texture_pos_y = 24, 16

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.texture_pos_x, self.texture_pos_y, self.width, self.height)

    def get_coords(self):
        return self.x, self.y
    
    def set_x(self, x):
        self.x = x
    def set_y(self, y):   
        self.y = y

class Hero(Sprite):
    def __init__(self, x, y, text_x, text_y):
        super().__init__(x, y, text_x, text_y)
    
    def update(self):
        super().update()
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            self.x = self.x + 1
            self.update_sprit(self.x, self.y)
        elif pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            self.y = self.y + 1
            self.update_sprit(self.x, self.y)
        elif pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_UP):
            self.y = self.y - 1
            self.update_sprit(self.x, self.y)
        elif pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_LEFT):
            self.x = self.x - 1
            self.update_sprit(self.x, self.y)

        
        

class Level: ## Gère la map
    def __init__(self, hero: Hero) -> None:
        self.hero = hero
        self.salle = "milieu"
    def update(self):
        self.collision(self.salle)

    def draw(self):
        x, y = self.hero.get_coords()
        if 40 <= x <= 80 and y == 0 and self.salle == "milieu" or self.salle == "haut":
            pyxel.bltm(0, 0, 0, 128, 0, 128, 128)
            self.salle = "haut"
        if (40 <= x <= 80 and y == 128) and (self.salle == "haut") or self.salle == "milieu":
            self.salle = "milieu"
            pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
        
    
    def collision(self, salle):## Gère les collisions avec les murs
        x, y = self.hero.get_coords() 
        match salle:
            case "milieu":
                if 40 <= x <= 80 and y == 40:
                    self.hero.set_y(y - 1)
                if 40 <= x <= 80 and y == 80:
                    self.hero.set_y(y + 1)
                if 40 <= y <= 80 and x == 40:
                    self.hero.set_x(x - 1)
                if 40 <= y <= 80 and x == 80:
                    self.hero.set_x(x + 1)
            case "haut":
                 if 40 <= x <= 80 and y == 8:
                    pyxel.text(64, 64, "YOU WIN", 7)
            
        


class TitleScreen:
    def __init__(self) -> None:
        pass

    def update(self):
        pass

    def draw(self):
        pyxel.blt(57, 60, 0, 25, 32, 14, 7)

class App:
    def __init__(self):
        pyxel.init(128, 128) ## Taille fenêtre
        self.resources = pyxel.load("..\\assets\\2.pyxres")
        self.titlescreen = TitleScreen() ## Création de l'écran titre
        self.hero = Hero(0, 0, 24, 16) ## (64, 64) coordonnées de départ du héros, (24, 16) coordonnées de la texture du héros
        self.level = Level(self.hero) ## Création de la map
        self.index = 0
        pyxel.Music.set = pyxel.play(0, 1, loop=True)

        pyxel.run(self.update, self.draw) ## Boucle principale

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE): ## Quitte le jeu si la touche Echap est pressée
            pyxel.quit()
        self.level.update()
        self.hero.update()
            
            
    def draw(self):
        if self.index == 0:
            self.titlescreen.draw() ## Dessine l'écran titre
        if pyxel.btn(pyxel.KEY_SPACE) or self.index == 1: 
            self.index = 1
            pyxel.cls(0) ## Nettoie l'écran
            self.level.draw() ## Dessine la map
            self.hero.draw() ## Dessine le héros
        
        
        


# Pyxel app Running
if __name__ == "__main__":
    App()
