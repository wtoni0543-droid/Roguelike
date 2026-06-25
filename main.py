from rich import print
import os
import random

from player import Player
from monster import Monster
from map import GameMap

WIDTH = 40
HEIGHT = 20

# =========================================
# ОЧИСТКА
# =========================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# =========================================
# МЕНЮ
# =========================================
from rich import print

def menu():

    while True:

        clear()

        print("[bold green]██╗██████╗  ██████╗  ██████╗ [/bold green]")
        print("[bold green]██║██╔══██╗██╔═══██╗██╔════╝ [/bold green]")
        print("[bold green]██║██████╔╝██║   ██║██║  ███╗[/bold green]")
        print("[bold green]██║██╔══██╗██║   ██║██║   ██║[/bold green]")
        print("[bold green]██║██║  ██║╚██████╔╝╚██████╔╝[/bold green]")
        print("[bold green]╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ [/bold green]")

        print()
        print("[1] Играть")
        print("[2] Выход")

        c = input("\n> ").strip()

        if c == "1":
            return

        elif c == "2":
            exit()
# =========================================
# HUD
# =========================================

def draw_hud(player, monsters, level):

    print()

    left = [
        "╔════════════════════════════╗",
        f"║ ЭТАЖ: {level}".ljust(29) + "║",
        f"║ HP: {player.hp}/{player.max_hp}".ljust(29) + "║",
        f"║ УРОН: {player.damage}".ljust(29) + "║",
        f"║ ЗОЛОТО: {player.gold}".ljust(29) + "║",
        f"║ ВРАГОВ: {len(monsters)}".ljust(29) + "║",
        "╚════════════════════════════╝"
    ]

    right = [
        "ПОДСКАЗКИ:",
        "P - Игрок",
        "G - Гоблин",
        "T - Танк",
        "S - Стрелок",
        "B - Босс",
        "^ - Ловушка",
        "+ - Аптечка",
        "C - Сундук",
        "$ - Торговец",
        "> - Лестница"
    ]

    max_lines = max(len(left), len(right))

    for i in range(max_lines):

        l = left[i] if i < len(left) else " " * 30
        r = right[i] if i < len(right) else ""

        print(f"{l}    {r}")

# =========================================
# ЛУТ
# =========================================

def drop_loot(monster, game_map, log):

    gold = random.randint(10, 30)

    return gold

# =========================================
# ВРАГИ
# =========================================

def spawn(level):

    monsters = []

    if level == 5:

        boss = Monster(20, 10, "boss")

        boss.hp = 400
        boss.damage = 8

        monsters.append(boss)

        return monsters

    monsters.append(Monster(10, 5, "goblin"))
    monsters.append(Monster(15, 8, "tank"))
    monsters.append(Monster(25, 6, "shooter"))

    return monsters

# =========================================
# СУНДУКИ
# =========================================

def spawn_chests(game_map):

    for _ in range(3):

        x = random.randint(3, WIDTH - 4)
        y = random.randint(3, HEIGHT - 4)

        game_map.tiles[y][x] = "C"

# =========================================
# ЛОВУШКИ
# =========================================

def spawn_traps(game_map):

    for _ in range(7):

        x = random.randint(3, WIDTH - 4)
        y = random.randint(3, HEIGHT - 4)

        game_map.tiles[y][x] = "^"

# =========================================
# ТОРГОВЕЦ
# =========================================

def spawn_merchant(game_map, level):

    if level in [2, 4]:

        game_map.tiles[10][20] = "$"

# =========================================
# МАГАЗИН
# =========================================

def shop(player, log, level):

    clear()

    print("[bold yellow]ТОРГОВЕЦ[/bold yellow]\n")

    print(f"ЗОЛОТО: {player.gold}\n")

    print("[1] +20 HP (30 золота)")
    print("[2] +10 УРОНА (40 золота)")

    if level == 4:
        print("[3] МЕЧ БОГА +50 (100 золота)")

    print("[0] Выход")

    c = input("\n> ")

    if c == "1":

        if player.gold >= 30:

            player.gold -= 30
            player.max_hp += 20
            player.hp += 20

            log.append("❤️ HP увеличено")

    elif c == "2":

        if player.gold >= 40:

            player.gold -= 40
            player.damage += 10
            log.append("⚔️ Урон увеличен")

    elif c == "3" and level == 4:

        if player.gold >= 100:

            player.gold -= 100
            player.damage += 50

            log.append("🔥 Куплен Меч Бога")

# =========================================
# ИГРА
# =========================================

def game():

    level = 1

    game_map = GameMap(WIDTH, HEIGHT)
    game_map.generate()

    spawn_chests(game_map)
    spawn_traps(game_map)
    spawn_merchant(game_map, level)

    player = Player(2, 2)

    player.gold = 0

    monsters = spawn(level)

    log = []

    stairs_spawned = False

    while True:

        clear()

        # лестница
        if len(monsters) == 0 and not stairs_spawned:

            game_map.tiles[HEIGHT - 2][WIDTH - 2] = ">"

            stairs_spawned = True

            log.append("⬇️ Появилась лестница")

        # =========================================
        # КАРТА
        # =========================================

        for y in range(HEIGHT):

            for x in range(WIDTH):

                char = game_map.tiles[y][x]

                # враги
                for m in monsters:

                    if m.x == x and m.y == y:

                        if m.type == "tank":
                            char = "T"

                        elif m.type == "shooter":
                            char = "S"

                        elif m.type == "boss":
                            char = "B"

                        else:
                            char = "G"

                # игрок
                if player.x == x and player.y == y:
                    char = "P"

                # цвета
                if char == "#":
                    print("[grey37]#[/grey37]", end="")

                elif char == "P":
                    print("[bold green]P[/bold green]", end="")

                elif char == "G":
                    print("[green]G[/green]", end="")

                elif char == "T":
                    print("[bold red]T[/bold red]", end="")

                elif char == "S":
                    print("[bold magenta]S[/bold magenta]", end="")

                elif char == "B":
                    print("[bold red]B[/bold red]", end="")

                elif char == "^":
                    print("[yellow]^[/yellow]", end="")

                elif char == "+":
                    print("[cyan]+[/cyan]", end="")

                elif char == "C":
                    print("[bold yellow]C[/bold yellow]", end="")

                elif char == "$":
                    print("[bold yellow]$[/bold yellow]", end="")

                elif char == ">":
                    print("[white]>[/white]", end="")

                else:
                    print(".", end="")

            print()

        draw_hud(player, monsters, level)

        # =========================================
        # ЛОГИ
        # =========================================

        print("\n[bold cyan]ЛОГИ:[/bold cyan]")

        for text in log[-10:]:
            print(text)

        # =========================================
        # ВВОД
        # =========================================

        cmd = input("\n> ").lower()

        if cmd == "q":
            break

        dx = 0
        dy = 0

        if cmd == "w":
            dy = -1

        elif cmd == "s":
            dy = 1

        elif cmd == "a":
            dx = -1

        elif cmd == "d":
            dx = 1

        nx = player.x + dx
        ny = player.y + dy

        attacked = False

        # =========================================
        # АТАКА
        # =========================================

        for m in monsters[:]:

            if m.x == nx and m.y == ny:

                m.hp -= player.damage

                log.append(f"⚔️ Удар по {m.type}")

                # контратака
                if m.hp > 0:

                    player.hp -= m.damage

                    log.append(f"💥 Враг ударил на {m.damage}")

                # смерть
                if m.hp <= 0:
                    monsters.remove(m)

                    gold = drop_loot(m, game_map, log)

                    player.gold += gold

                    log.append(f"💰 +{gold} золота")

                    # босс
                    if m.type == "boss":

                        clear()

                        print("[bold yellow]")
                        print("🏆 ТЫ ПРОШЁЛ ИГРУ")
                        print("[/bold yellow]")

                        input("\nEnter...")
                        return

                attacked = True
                break

        # =========================================
        # ДВИЖЕНИЕ
        # =========================================

        if not attacked:

            if game_map.tiles[ny][nx] != "#":

                player.x = nx
                player.y = ny

        # =========================================
        # КЛЕТКА
        # =========================================

        tile = game_map.tiles[player.y][player.x]

        # хил
        if tile == "+":

            player.hp = min(player.max_hp, player.hp + 30)

            game_map.tiles[player.y][player.x] = "."

            log.append("💊 HP +30")

        # ловушка
        if tile == "^":

            dmg = random.randint(10, 20)

            player.hp -= dmg

            game_map.tiles[player.y][player.x] = "."

            log.append(f"☠️ Ловушка: {dmg} урона")

        # сундук
        if tile == "C":

            game_map.tiles[player.y][player.x] = "."

            gold = random.randint(20, 50)

            player.gold += gold

            log.append(f"💰 Сундук: +{gold} золота")

        # торговец
        if tile == "$":

            shop(player, log, level)

        # лестница
        if tile == ">":

            level += 1

            game_map = GameMap(WIDTH, HEIGHT)
            game_map.generate()

            spawn_chests(game_map)
            spawn_traps(game_map)
            spawn_merchant(game_map, level)

            monsters = spawn(level)

            player.x = 2
            player.y = 2

            stairs_spawned = False

            log.clear()

            log.append(f"⬇️ Этаж {level}")

        # =========================================
        # AI
        # =========================================

        for m in monsters[:]:

            dist = abs(m.x - player.x) + abs(m.y - player.y)

            # стрелок
            if m.type == "shooter":

                if dist <= 3:

                    player.hp -= m.damage

                    log.append(f"🔫 Стрелок: {m.damage} урона")

                    continue

            # ближний бой
            if dist == 1:

                player.hp -= m.damage

                log.append(f"💥 Враг ударил: {m.damage}")

                continue

            # случайное движение
            dx, dy = random.choice([
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
                (0, 0)  # иногда стоит на месте
            ])

            new_x = m.x + dx
            new_y = m.y + dy

            # не ходим сквозь стены
            if game_map.tiles[new_y][new_x] != "#":
                m.x = new_x
                m.y = new_y

        # =========================================
        # СМЕРТЬ
        # =========================================

        if player.hp <= 0:

            clear()

            print("[bold red]ТЫ ПОГИБ[/bold red]")

            input("\nEnter...")
            break

# =========================================
# START
# =========================================

if __name__ == "__main__":

    menu()
    game()