import random

class GameMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.tiles = []
        self.traps = []
        self.medkits = []

    def generate(self):

        self.tiles = [
            ["." for _ in range(self.width)]
            for _ in range(self.height)
        ]

        # стены
        for x in range(self.width):
            self.tiles[0][x] = "#"
            self.tiles[self.height - 1][x] = "#"

        for y in range(self.height):
            self.tiles[y][0] = "#"
            self.tiles[y][self.width - 1] = "#"

        # случайные стены
        for _ in range(40):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            self.tiles[y][x] = "#"

        # ловушки
        for _ in range(10):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)

            if self.tiles[y][x] == ".":
                self.tiles[y][x] = "^"

        # аптечки
        for _ in range(5):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)

            if self.tiles[y][x] == ".":
                self.tiles[y][x] = "+"