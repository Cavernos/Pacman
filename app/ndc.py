

import pyxel

counter = 0


class Sprite:
    def __init__(self, x, y, text_x, text_y, health=3, armor=3):
        self.x, self.y = x, y
        self.width, self.height = 8, 8
        self.health = health
        self.armor = armor
        self.weapon = None
        self.texture_pos_x, self.texture_pos_y = text_x, text_y

    def update_sprite(self, x, y):
        if (x % 10 <= 5 or y % 10 >= 5) and (self.texture_pos_x == 24 and self.texture_pos_y == 16):
            self.texture_pos_x, self.texture_pos_y = 32, 16
        else:
            self.texture_pos_x, self.texture_pos_y = 24, 16

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.texture_pos_x, self.texture_pos_y, self.width, self.height, 2)

    def death(self):
        if self.health <= 0:
            return True
        return False

    def has_weapon(self):
        if isinstance(self.weapon, Weapon):
            self.weapon.set_hero(self)
            return True
        return False

    def get_coords(self):
        return self.x, self.y

    def get_health(self):
        return self.health

    def get_weapon(self):
        return self.weapon

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y


class Hero(Sprite):
    def __init__(self, x, y, text_x, text_y, key=None):
        super().__init__(x, y, text_x, text_y)
        self.key = key

    def update(self):
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            self.x = self.x + 1
            self.update_sprite(self.x, self.y)
        if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            self.y = self.y + 1
            self.update_sprite(self.x, self.y)
        if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_UP):
            self.y = self.y - 1
            self.update_sprite(self.x, self.y)
        if pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_LEFT):
            self.x = self.x - 1
            self.update_sprite(self.x, self.y)

        if self.has_weapon():
            self.weapon.update()

    def draw(self):
        super().draw()
        for i in range(self.health):
            pyxel.blt(2 + 10 * i, 115, 0, 104, 8, 8, 8, 2)
        for i in range(self.armor):
            pyxel.blt(85 + 10 * i, 115, 0, 32, 24, 8, 8, 2)
        if self.key is not None:
            self.key.draw()
        if self.weapon is not None:
            self.weapon.draw()
            match self.weapon.get_id():
                case 0:
                    pyxel.blt(115, 105, 0, 64, 8, 8, 8, 2)
                case 1:
                    pyxel.blt(105, 105, 0, 24, 24, 8, 8, 2)

    def set_health(self, health):
        self.health = health

    def set_weapon(self, weapon_index):
        self.weapon = weapon_index

    def set_armor(self, armor):
        self.armor = armor

    def set_key(self, key):
        self.key = key

    def has_key(self):
        if isinstance(self.key, Key):
            return True
        return False

    def damage(self, damage):
        if self.get_armor() >= 0:
            self.set_armor(self.get_armor() - damage)
        else:
            self.set_health(self.get_health() - damage)

    def get_armor(self):
        return self.armor


class Level:  # Gère la map
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

    def set_room(self, room_id):
        self.salle = room_id


# Création d'une
# index de la pièce: int
# personnage principal
class Room:
    def __init__(self, index, hero: Hero):
        self.use = 0
        self.index = index
        self.hero = hero
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

        for piece in self.objects[2]:
            if piece.get_id() == self.getId():
                object_x, object_y = piece.get_coords()
                object_w, object_h = piece.get_dims()
                if (object_x <= hero_x <= object_x + object_w) \
                        and (object_y <= hero_y <= object_y + object_h) \
                        and self.use == 0:
                    self.use = 1
                    match piece.update():
                        case "health":
                            if self.hero.get_health() <= 3:
                                self.hero.set_health(self.hero.get_health() + 1)
                            break
                        case "armor":
                            if self.hero.get_armor() <= 3:
                                self.hero.set_armor(self.hero.get_armor() + 1)
                            break
                        case _:
                            if isinstance(piece.update(), Weapon):
                                self.hero.set_weapon(piece.update())
                                break
                            if isinstance(piece.update(), Key):
                                self.hero.set_key(piece.update())
                                break
        if self.hero.death() or self.hero.has_key():
            self.use = 0

    def create_object_list(self) -> list[tuple]:
        # Definitions des objets en fontion de l'id de chaque salle
        # Liste de la forme [(Doors), (Simple Object), (Specific Object), (Enemies))]
        match self.index:
            case 0:
                return [
                    (
                        # Door North
                        Door(1, 48, 1, 24, 2, 67, 120),
                        # Door South
                        Door(-1, 48, 120, 24, 2, 67, 6),
                        # Door West
                        Door(-10, 0, 40, 2, 32, 120, 67),
                        # Door Est
                        Door(10, 120, 40, 2, 32, 6, 67)),
                    (Well(0, 40, 40, 40, 40),), ()]
            case 1:
                return [(Door(0, 48, 120, 24, 2, 67, 6),), (), (Chest(1, 48, 0, 24, 8),)]
            case -1:
                return [(Door(0, 48, 1, 24, 2, 67, 120), Door(-1, 48, 120, 24, 2, 67, 6)), (), ()]
            case -10:
                return [(Door(0, 120, 40, 2, 32, 6, 67),), (), ()]
            case 10:
                return [(Door(0, 0, 40, 2, 32, 120, 67),), (), ()]

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
        for piece in self.objects[2]:
            piece.draw(0)

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
        self.loot = [Weapon(0, 2), "health", "armor", Weapon(1, 1), Key(0, 115, 115, 8, 8)]

    def update(self):
        loot_index = pyxel.rndi(0, len(self.loot) - 1)
        return self.loot[loot_index]

    def draw(self, index):
        if index == 0:
            pyxel.blt(self.x, self.y, 0, 112, 8, 16, 8, 2)
        elif index == 1:
            pyxel.blt(self.x, self.y, 0, 112, 8, 16, 8, 2)


class Weapon:
    def __init__(self, index, damage, hero: Hero = None):
        self.index = index
        self.damage = damage
        self.hero = hero

    def update(self):
        pass

    def draw(self):
        hero_x, hero_y = self.hero.get_coords()
        global counter
        match self.index:
            case 0:
                if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and counter <= 0:
                    pyxel.line(hero_x + 8, hero_y + 4, hero_x + 10, hero_y + 4, 0)
                    if self.hero is not None:
                        self.hero.damage(self.damage)
                    counter = 20
                counter -= 1
            case 1:
                if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and counter <= 0:
                    if self.hero is not None:
                        self.hero.damage(self.damage)
                    counter = 10
                counter -= 1

    def set_hero(self, hero):
        self.hero = hero

    def get_id(self):
        return self.index


class Key(Object):
    def __init__(self, index, x, y, w, h):
        super().__init__(index, x, y, w, h)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 88, 40, self.w, self.h, 2)


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
            pyxel.cls(0)  # Passe l'écran au noir
            if not self.hero.death():
                self.level.draw()  # Dessine la map
                self.hero.draw()  # Dessine le héros
                pyxel.text(0, 2, "  Trouve la            cle !", 7)
                # Mécanique de win
                # if self.hero.has_key():
                #     pyxel.cls(0)
                #     pyxel.text(47, 60, "You Win", 7)
                #     if pyxel.btn(pyxel.KEY_M):
                #         self.level.draw()
                #         self.hero.draw()
                #         self.hero.set_key(None)
                #         self.level.set_room(0)
                #         self.hero.set_health(3)
                #         self.hero.set_x(0)
                #         self.hero.set_y(0)
            else:
                pyxel.text(47, 60, "You Lose", 7)
                pyxel.text(24, 68, "Press m to restart", 7)
                if pyxel.btn(pyxel.KEY_M):
                    self.level.set_room(0)
                    self.hero.set_health(3)
                    self.hero.set_x(0)
                    self.hero.set_y(0)
                    self.hero.set_weapon(None)


# Pyxel app Running
if __name__ == "__main__":
    App()
