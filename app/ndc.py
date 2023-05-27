import pyxel

class Sprite:
    def __init__(self, x, y, text_x, text_y):
        self.x, self.y = x, y
        self.width, self.height = 8,8
        self.texture_pos_x, self.texture_pos_y = text_x, text_y 

    def update(self):
        pass # Déplacé dans la classe
        
            
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
        pass

    def draw(self):
        x, y = self.hero.get_coords()
        if self.salle == "haut": #Gère salle du haut
            pyxel.bltm(0, 0, 0, 128, 0, 128, 128)
            #self.hero.set_y(120)
            self.salle = "haut"
        if self.salle == "milieu": #Gère salle du bas
            self.salle = "milieu"
            pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
        self.collision(self.salle)
    
    def get_salle(self): ## Renvoie la salle actuelle
        return self.salle
        
    
    def collision(self, salle):## Gère les collisions avec les murs
        x, y = self.hero.get_coords()
        match salle:
            case "milieu":
                pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
                print(x, y)
                if 40 <= x <= 80 and y == 40:
                    self.hero.set_y(y - 1)
                if 40 <= x <= 80 and y == 80:
                    self.hero.set_y(y + 1)
                if 40 <= y <= 80 and x == 40:
                    self.hero.set_x(x - 1)
                if 40 <= y <= 80 and x == 80:
                    self.hero.set_x(x + 1)

                if (x < 2 and y > 40) and (x < 2 and y < 71): #porte de gauche
                    self.hero.set_x(120)
                if (x > 127 and y > 40) and (x > 127 and y < 71): #porte de droite
                    self.hero.set_x(50)
                if (y <= 1 and x > 40) and (y <= 1 and x < 71): #porte du haut
                    self.hero.set_y(127)
                    self.salle = "haut"
                if (y > 128 and x > 40) and (y > 128 and x < 71): #porte du bas
                    self.hero.set_y(2)


                if x < 0 or x >= 128: #colision mur droite
                    self.hero.set_x(1)
                if (x > 120 and y < 49) or (x > 120 and y > 70): #colision mur de gauche
                    self.hero.set_x(120)
                if (y < 0 and x < 49) or (y < 0 and x > 70): #colision mur du haut
                    self.hero.set_y(0)
                if (y > 120 and x < 49) or (y > 120 and x > 70): #colision mur du bas
                    self.hero.set_y(120)
                
            case "haut":
                print(x, y, 2)
                pyxel.bltm(0, 0, 0, 128, 0, 128, 128)
                
                if (y > 128 and x > 40) and (y > 128 and x < 71): #porte du bas
                    self.salle = "milieu"
                    self.hero.set_y(9)
                    print("porte bas")
                
                if 40 <= x <= 80 and y == 8:
                    self.salle = ""
                    pyxel.cls(0)
                    pyxel.text(64 - len("YOU WIN") / 2, 64, "YOU WIN", 7)


class TitleScreen:
    def __init__(self) -> None:
        pass

    def update(self):
        pass

    def draw(self):
        pyxel.text(24, 50, "Espace pour commencer", 7)
        pyxel.blt(57, 60, 0, 25, 32, 14, 7)

class App:
    def __init__(self):
        pyxel.init(128, 128) ## Taille fenêtre
        self.resources = pyxel.load("..\\assets\\2.pyxres")
        self.titlescreen = TitleScreen() ## Création de l'écran titre
        self.hero = Hero(0, 0, 24, 16) ## (64, 64) coordonnées de départ du héros, (24, 16) coordonnées de la texture du héros
        self.level = Level(self.hero) ## Création de la map
        pyxel.Music.set = pyxel.play(0, 1, loop=True)
        self.index = 0
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
            pyxel.text(0, 2, "  Trouve la            cle !", 7)
        
        
        


# Pyxel app Running
if __name__ == "__main__":
    App()
