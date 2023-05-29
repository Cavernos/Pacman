import pyxel


class Sprite:
    def __init__(self, x, y, text_x, text_y):
        self.x, self.y = x, y
        self.width, self.height = 8, 8
        self.texture_pos_x, self.texture_pos_y = text_x, text_y

    def update(self):
        pass  # Déplacé dans la classe

    def update_sprite(self, x, y):
        if (x % 10 <= 5 or y % 10 >= 5) and (self.texture_pos_x == 24 and self.texture_pos_y == 16):
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
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            self.x = self.x + 1
            self.update_sprite(self.x, self.y)
        elif pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            self.y = self.y + 1
            self.update_sprite(self.x, self.y)
        elif pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_UP):
            self.y = self.y - 1
            self.update_sprite(self.x, self.y)
        elif pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_LEFT):
            self.x = self.x - 1
            self.update_sprite(self.x, self.y)


class Level:  ## Gère la map
    def __init__(self, hero: Hero) -> None:
        self.hero = hero
        # 1 Salle du Haut
        # 0 Salle du Milieu
        # -1 Salle du Bas
        # -10 Salle de Gauche
        # 10 Salle de droite
        self.salle = 0
        self.middle_room = Room(0, hero)
        self.nord_room = Room(1, hero)
        self.south_room = Room(-1, hero)
        self.left_room = Room(-10, hero)
        self.right_room = Room(10, hero)
        self.rooms = [self.nord_room, self.middle_room, self.south_room, self.left_room, self.right_room]

    def update(self):
        match self.salle:
            case 0:
                self.rooms[1].update()
            case 1:
                self.rooms[0].update()
            case -1:
                self.rooms[2].update()
            case 10:
                self.rooms[4].update()
            case -10:
                self.rooms[3].update()

    def draw(self):
        match self.salle:
            case 0:
                self.rooms[1].draw()
                self.salle = self.rooms[1].getId()
                self.rooms[1].setId(0)
            case 1:
                self.rooms[0].draw()
                self.salle = self.rooms[0].getId()
                self.rooms[0].setId(1)
            case -1:
                self.rooms[2].draw()
                self.salle = self.rooms[2].getId()
                self.rooms[2].setId(-1)
            case 10:
                self.rooms[4].draw()
                self.salle = self.rooms[4].getId()
                self.rooms[4].setId(10)
            case -10:
                self.rooms[3].draw()
                self.salle = self.rooms[3].getId()
                self.rooms[3].setId(-10)

        # self.collision(self.salle)

    def set_room(self, room_id):
        self.salle = room_id

    # def collision(self, salle):  # Gère les collisions avec les murs
    #     x, y = self.hero.get_coords()
    #     match salle:
    #         case "milieu":
    #             pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
    #             if 40 <= x <= 80 and y == 40:
    #                 self.hero.set_y(y - 1)
    #             if 40 <= x <= 80 and y == 80:
    #                 self.hero.set_y(y + 1)
    #             if 40 <= y <= 80 and x == 40:
    #                 self.hero.set_x(x - 1)
    #             if 40 <= y <= 80 and x == 80:
    #                 self.hero.set_x(x + 1)
    #
    #             if (x < 2 and y > 40) and (x < 2 and y < 71):  # porte de gauche
    #                 self.hero.set_x(120)
    #             if (x > 127 and y > 40) and (x > 127 and y < 71):  # porte de droite
    #                 self.hero.set_x(50)
    #             if (y <= 1 and x > 40) and (y <= 1 and x < 71):  # porte du haut
    #                 self.hero.set_y(127)
    #                 self.salle = "haut"
    #             if (y > 128 and x > 40) and (y > 128 and x < 71):  # porte du bas
    #                 self.hero.set_y(2)
    #
    #             if x < 0 or x >= 128:  # colision mur droite
    #                 self.hero.set_x(1)
    #             if (x > 120 and y < 49) or (x > 120 and y > 70):  # colision mur de gauche
    #                 self.hero.set_x(120)
    #             if (y < 0 and x < 49) or (y < 0 and x > 70):  # colision mur du haut
    #                 self.hero.set_y(0)
    #             if (y > 120 and x < 49) or (y > 120 and x > 70):  # colision mur du bas
    #                 self.hero.set_y(120)
    #
    #         case "haut":
    #             print(x, y, 2)
    #             pyxel.bltm(0, 0, 0, 128, 0, 128, 128)
    #
    #             if (y > 128 and x > 40) and (y > 128 and x < 71):  # porte du bas
    #                 self.salle = "milieu"
    #                 self.hero.set_y(9)
    #                 print("porte bas")
    #
    #             if 40 <= x <= 80 and y == 8:
    #                 self.salle = ""
    #                 pyxel.cls(0)
    #                 pyxel.text(64 - len("YOU WIN") / 2, 64, "YOU WIN", 7)


# Création d'une
# index de la pièce: int
# personnage principal
class Room:
    def __init__(self, index, hero: Hero):
        self.index = index
        self.hero = hero

        # Definitions des portes et des index
        # index_room_to_go, x, y, w, h, hero_x, hero_y
        door_index = index + 1 if index < 1 else index
        self.door_north = Door(door_index, 48, 1, 24, 2, 67, 120)
        door_index = index - 1 if index > -1 else index
        self.door_south = Door(door_index, 48, 120, 24, 2, 67, 6)
        door_index = index - 10 if index > -10 else index
        self.door_left = Door(door_index, 0, 40, 2, 32, 120, 67)
        door_index = index + 10 if index < 10 else index
        self.door_right = Door(door_index, 120, 40, 2, 32, 6, 67)
        self.objects = []

    # Gestion des Objet et des collision
    # Gestion des portes avec le changements de salle
    def update(self):
        hero_x, hero_y = self.hero.get_coords()
        if hero_x >= 120:
            self.hero.set_x(hero_x - 1)
        if hero_y >= 120:
            self.hero.set_y(hero_y - 1)
        if hero_y <= 0:
            self.hero.set_y(hero_y + 1)
        if hero_x <= 0:
            self.hero.set_x(hero_x + 1)
        self.objects = self.create_object_list()

        for door in self.objects[0]:
            door_x, door_y = door.get_coords()
            door_w, door_h = door.get_dims()
            if (door_x <= hero_x <= door_x + door_w) and (door_y <= hero_y <= door_y + door_h):
                self.hero.set_y(door.get_hero_y() - 3)
                self.hero.set_x(door.get_hero_x() - 3)
                self.setId(door.get_id())
                break
            for piece in self.objects[1]:
                if piece.get_id() == self.getId():
                    object_x, object_y = piece.get_coords()
                    object_w, object_h = piece.get_dims()
                    if (object_x <= hero_x <= object_x + object_w) and hero_y == object_y:
                        self.hero.set_y(hero_y - 1)
                        break
                    if (object_y <= hero_y <= object_y + object_h) and hero_x == object_x:
                        self.hero.set_x(hero_x - 1)
                        break
                    if (object_x <= hero_x <= object_x + object_w) and hero_y == object_y + object_h:
                        self.hero.set_y(hero_y + 1)
                        break
                    if (object_y <= hero_y <= object_y + object_h) and hero_x == object_x + object_w:
                        self.hero.set_x(hero_x + 1)
                        break

    def create_object_list(self):
        match self.index:
            case 0:
                return [
                    (self.door_north, self.door_south, self.door_left, self.door_right),
                    (Well(0, 40, 40, 40, 40),)]
            case 1:
                return [(self.door_south,), (Chest(1, 48, 0, 24, 8),)]
            case -1:
                return [(self.door_north, self.door_south), ()]
            case -10:
                return [(self.door_right,), ()]
            case 10:
                return [(self.door_left,), ()]

    # Création de la salle en fonction de l'index
    def draw(self):
        match self.index:
            case 0:
                pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
            case 1:
                pyxel.bltm(0, 0, 0, 128, 0, 128, 128)
            case -1:
                pyxel.bltm(0, 0, 0, 512, 0, 128, 128)
            case 10:
                pyxel.bltm(0, 0, 0, 384, 0, 128, 128)
            case -10:
                pyxel.bltm(0, 0, 0, 256, 0, 128, 128)

    def getId(self):
        return self.index

    def setId(self, index):
        self.index = index


# Création d'un objet
class Object:
    def __init__(self, index, x, y, width, height):
        self.index = index
        self.x = x
        self.y = y
        self.w = width
        self.h = height

    def get_coords(self):
        return self.x, self.y

    def get_dims(self):
        return self.w, self.h

    def get_id(self):
        return self.index


# Création d'une porte
# index de la pièce dans laquelle on souhaite se rendre
# x coordonnées en x
# y coordonnées en y
# w largeur de l'objet
# h hauteur de l'objet
# hero_y coordonnée de tp du perso principale
class Door(Object):
    def __init__(self, room_index, x, y, width, height, hero_x, hero_y):
        super().__init__(room_index, x, y, width, height)
        self.hero_y = hero_y
        self.hero_x = hero_x

    def get_hero_y(self):
        return self.hero_y

    def get_hero_x(self):
        return self.hero_x


# Création d'un puit
class Well(Object):
    def __init__(self, index, x, y, w, h):
        super().__init__(index, x, y, w, h)


class Chest(Object):
    def __init__(self, index, x, y, w, h):
        super().__init__(index, x, y, w, h)


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
        pyxel.init(128, 128)  # Taille fenêtre
        pyxel.load("..\\assets\\2.pyxres")

        # Création de l'écran titre
        self.titlescreen = TitleScreen()

        # (64, 64) coordonnées de départ du héros, (24, 16) coordonnées de la texture du héros
        self.hero = Hero(0, 0, 24, 16)
        # Création de la map
        self.level = Level(self.hero)

        # Musique
        pyxel.play(0, 1, loop=True)
        self.index = 0
        pyxel.run(self.update, self.draw)  # Boucle principale

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):  # Quitte le jeu si la touche Echap est pressée
            pyxel.quit()
        self.level.update()
        self.hero.update()

    def draw(self):
        if self.index == 0:
            self.titlescreen.draw()  # Dessine l'écran titre
        if pyxel.btn(pyxel.KEY_SPACE) or self.index == 1:
            self.index = 1
            pyxel.cls(0)  # Nettoie l'écran
            self.level.draw()  # Dessine la map
            self.hero.draw()  # Dessine le héros
            pyxel.text(0, 2, "  Trouve la            cle !", 7)


# Pyxel app Running
if __name__ == "__main__":
    App()
