import random


def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class Monster:

    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

        # характеристики
        if type == "goblin":
            self.hp = 30
            self.damage = 5

        elif type == "tank":
            self.hp = 80
            self.damage = 8

        elif type == "shooter":
            self.hp = 40
            self.damage = 10

        elif type == "roamer":
            self.hp = 35
            self.damage = 6

        elif type == "boss":
            self.hp = 200
            self.damage = 15

        else:
            self.hp = 30
            self.damage = 5

    # движение к игроку
    def move_towards(self, player, game_map):
        dx = 0
        dy = 0

        if player.x > self.x:
            dx = 1
        elif player.x < self.x:
            dx = -1

        if player.y > self.y:
            dy = 1
        elif player.y < self.y:
            dy = -1

        nx = self.x + dx
        ny = self.y + dy

        if game_map.tiles[ny][nx] != "#":
            self.x = nx
            self.y = ny

    # ИИ
    def update_ai(self, player, game_map, messages):

        dist = distance(self.x, self.y, player.x, player.y)

        AGRO_RANGE = 5  # радиус агра

        # если рядом — стоит (атака в main.py)
        if dist == 1:
            return

        # если далеко — просто гуляет
        if dist > AGRO_RANGE:
            dx, dy = random.choice([
                (1, 0), (-1, 0), (0, 1), (0, -1)
            ])

            nx = self.x + dx
            ny = self.y + dy

            if game_map.tiles[ny][nx] != "#":
                self.x = nx
                self.y = ny

            return

        # если в радиусе — идёт к игроку
        self.move_towards(player, game_map)