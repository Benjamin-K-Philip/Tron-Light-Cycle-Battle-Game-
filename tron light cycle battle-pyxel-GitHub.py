import math
import random
from dataclasses import dataclass

import pyxel


WIDTH = 240
HEIGHT = 180
CELL = 4
GRID_W = WIDTH // CELL
GRID_H = HEIGHT // CELL
FPS = 30


BLACK = 0
NAVY = 1
PURPLE = 2
GREEN = 3
BROWN = 4
DARK_BLUE = 5
LIGHT_BLUE = 6
WHITE = 7
RED = 8
ORANGE = 9
YELLOW = 10
LIME = 11
CYAN = 12
GRAY = 13
PINK = 14
PEACH = 15


DIRS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}
OPPOSITE = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}


@dataclass
class Bike:
    name: str
    x: int
    y: int
    direction: str
    color: int
    trail_color: int
    glow_color: int
    keys: dict
    alive: bool = True
    human: bool = True
    score: int = 0
    pending_dir: str | None = None

    def head(self):
        return self.x, self.y


class TronGame:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="TRON Light Cycle Battle", fps=FPS)
        pyxel.mouse(False)

        self.state = "menu"
        self.mode = "cpu"
        self.winner_text = ""
        self.round_over_timer = 0

        self.grid = [[None for _ in range(GRID_H)] for _ in range(GRID_W)]
        self.bikes = []
        self.sparkles = []

        self.menu_index = 0
        self.menu_items = [
            "1 Player vs System",
            "2 Player Duel",
            "How to Play",
        ]
        self.how_to = False

        pyxel.run(self.update, self.draw)

    def reset_round(self, full_reset=False):
        self.grid = [[None for _ in range(GRID_H)] for _ in range(GRID_W)]

        left = Bike(
            name="Player 1",
            x=8,
            y=GRID_H // 2,
            direction="RIGHT",
            color=CYAN,
            trail_color=LIGHT_BLUE,
            glow_color=WHITE,
            keys={
                "UP": pyxel.KEY_W,
                "DOWN": pyxel.KEY_S,
                "LEFT": pyxel.KEY_A,
                "RIGHT": pyxel.KEY_D,
            },
            human=True,
        )

        right = Bike(
            name="System" if self.mode == "cpu" else "Player 2",
            x=GRID_W - 9,
            y=GRID_H // 2,
            direction="LEFT",
            color=ORANGE,
            trail_color=YELLOW,
            glow_color=PEACH,
            keys={
                "UP": pyxel.KEY_UP,
                "DOWN": pyxel.KEY_DOWN,
                "LEFT": pyxel.KEY_LEFT,
                "RIGHT": pyxel.KEY_RIGHT,
            },
            human=self.mode == "pvp",
        )

        if full_reset or len(self.bikes) < 2:
            left.score = 0
            right.score = 0
        else:
            left.score = self.bikes[0].score
            right.score = self.bikes[1].score

        self.bikes = [left, right]

        for bike in self.bikes:
            self.mark_trail(bike.x, bike.y, bike.trail_color)

        self.sparkles = []
        self.round_over_timer = 0
        self.winner_text = ""
        self.state = "play"

    def mark_trail(self, gx, gy, color):
        if 0 <= gx < GRID_W and 0 <= gy < GRID_H:
            self.grid[gx][gy] = color

    def update(self):
        if self.state == "menu":
            self.update_menu()
        elif self.state == "play":
            self.update_play()
        elif self.state == "round_over":
            self.update_round_over()

    def update_menu(self):
        if self.how_to:
            if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.KEY_RETURN):
                self.how_to = False
            return

        if pyxel.btnp(pyxel.KEY_UP):
            self.menu_index = (self.menu_index - 1) % len(self.menu_items)

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.menu_index = (self.menu_index + 1) % len(self.menu_items)

        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.menu_index == 0:
                self.mode = "cpu"
                self.reset_round(full_reset=True)
            elif self.menu_index == 1:
                self.mode = "pvp"
                self.reset_round(full_reset=True)
            else:
                self.how_to = True

    def update_play(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.state = "menu"
            self.how_to = False
            return

        for bike in self.bikes:
            if bike.alive and bike.human:
                self.read_input(bike)

        cpu = self.bikes[1]
        if self.mode == "cpu" and cpu.alive:
            cpu.direction = self.cpu_choose_direction(cpu, self.bikes[0])

        next_positions = []
        for bike in self.bikes:
            if not bike.alive:
                next_positions.append((bike.x, bike.y))
                continue

            if bike.pending_dir and bike.pending_dir != OPPOSITE[bike.direction]:
                bike.direction = bike.pending_dir
            bike.pending_dir = None

            dx, dy = DIRS[bike.direction]
            next_positions.append((bike.x + dx, bike.y + dy))

        collisions = [False, False]
        for i, (nx, ny) in enumerate(next_positions):
            bike = self.bikes[i]
            if not bike.alive:
                continue

            if nx < 0 or nx >= GRID_W or ny < 0 or ny >= GRID_H:
                collisions[i] = True
                continue

            if self.grid[nx][ny] is not None:
                collisions[i] = True

        if next_positions[0] == next_positions[1]:
            collisions[0] = collisions[1] = True

        for i, bike in enumerate(self.bikes):
            if collisions[i]:
                bike.alive = False
                self.spawn_crash(*bike.head(), bike.color)

        if not any(b.alive for b in self.bikes):
            self.finish_round("Draw")
            return

        if not self.bikes[0].alive:
            self.bikes[1].score += 1
            self.finish_round(f"{self.bikes[1].name} wins")
            return

        if not self.bikes[1].alive:
            self.bikes[0].score += 1
            self.finish_round(f"{self.bikes[0].name} wins")
            return

        for i, bike in enumerate(self.bikes):
            bike.x, bike.y = next_positions[i]
            self.mark_trail(bike.x, bike.y, bike.trail_color)

        self.update_sparkles()

    def update_round_over(self):
        self.update_sparkles()
        self.round_over_timer -= 1

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.reset_round(full_reset=False)
        elif pyxel.btnp(pyxel.KEY_M):
            self.state = "menu"
            self.how_to = False
        elif self.round_over_timer <= 0:
            self.reset_round(full_reset=False)

    def finish_round(self, text):
        self.winner_text = text
        self.state = "round_over"
        self.round_over_timer = FPS * 3

    def read_input(self, bike):
        for direction, key in bike.keys.items():
            if pyxel.btnp(key) and direction != OPPOSITE[bike.direction]:
                bike.pending_dir = direction

    def cpu_choose_direction(self, cpu, enemy):
        options = [cpu.direction, self.turn_left(cpu.direction), self.turn_right(cpu.direction)]
        safe_moves = []

        for d in options:
            if d == OPPOSITE[cpu.direction]:
                continue
            nx, ny = self.peek(cpu.x, cpu.y, d)
            if self.is_safe(nx, ny):
                score = self.evaluate_move(nx, ny, d, enemy)
                safe_moves.append((score, d))

        if safe_moves:
            safe_moves.sort(reverse=True)
            return safe_moves[0][1]

        for d in DIRS:
            nx, ny = self.peek(cpu.x, cpu.y, d)
            if self.is_safe(nx, ny):
                return d

        return cpu.direction

    def evaluate_move(self, nx, ny, direction, enemy):
        area = self.flood_count(nx, ny, limit=140)
        ex, ey = enemy.head()
        dist = abs(nx - ex) + abs(ny - ey)
        attack_bias = 12 - min(dist, 12)
        wall_bias = self.wall_distance(nx, ny)
        straight_bonus = 3 if direction == self.bikes[1].direction else 0
        lane_bias = 0

        if abs(ny - ey) <= 2 or abs(nx - ex) <= 2:
            lane_bias = 4

        return area + attack_bias + wall_bias + straight_bonus + lane_bias + random.random()

    def flood_count(self, sx, sy, limit=140):
        seen = {(sx, sy)}
        stack = [(sx, sy)]
        count = 0

        while stack and count < limit:
            x, y = stack.pop()
            count += 1
            for dx, dy in DIRS.values():
                nx, ny = x + dx, y + dy
                if (nx, ny) in seen:
                    continue
                if self.is_safe(nx, ny):
                    seen.add((nx, ny))
                    stack.append((nx, ny))

        return count

    def wall_distance(self, x, y):
        return min(x, y, GRID_W - 1 - x, GRID_H - 1 - y)

    def is_safe(self, x, y):
        return 0 <= x < GRID_W and 0 <= y < GRID_H and self.grid[x][y] is None

    def peek(self, x, y, direction):
        dx, dy = DIRS[direction]
        return x + dx, y + dy

    def turn_left(self, d):
        return {"UP": "LEFT", "LEFT": "DOWN", "DOWN": "RIGHT", "RIGHT": "UP"}[d]

    def turn_right(self, d):
        return {"UP": "RIGHT", "RIGHT": "DOWN", "DOWN": "LEFT", "LEFT": "UP"}[d]

    def spawn_crash(self, gx, gy, color):
        px = gx * CELL + CELL // 2
        py = gy * CELL + CELL // 2
        for _ in range(24):
            ang = random.random() * math.tau
            speed = random.uniform(0.4, 2.0)
            self.sparkles.append([px, py, math.cos(ang) * speed, math.sin(ang) * speed, 20, color])

    def update_sparkles(self):
        fresh = []
        for s in self.sparkles:
            s[0] += s[2]
            s[1] += s[3]
            s[4] -= 1
            if s[4] > 0:
                fresh.append(s)
        self.sparkles = fresh

    def draw(self):
        pyxel.cls(BLACK)
        if self.state == "menu":
            self.draw_menu()
        else:
            self.draw_arena()
            self.draw_hud()
            if self.state == "round_over":
                self.draw_round_over()

    def draw_menu(self):
        self.draw_grid_background()

        pyxel.text(72, 22, "TRON", WHITE)
        pyxel.text(58, 34, "LIGHT CYCLE BATTLE", CYAN)

        for i, item in enumerate(self.menu_items):
            y = 74 + i * 18
            selected = i == self.menu_index
            color = YELLOW if selected else LIGHT_BLUE
            marker = ">" if selected else " "
            pyxel.rectb(54, y - 4, 130, 14, color)
            pyxel.text(62, y, f"{marker} {item}", color)

        pyxel.text(34, 144, "ENTER: Select  UP/DOWN: Menu", GRAY)
        pyxel.text(24, 154, "A neon arena inspired from the 1982 TRON movie.", ORANGE)

        if self.how_to:
            pyxel.rect(20, 40, 200, 100, NAVY)
            pyxel.rectb(20, 40, 200, 100, CYAN)
            lines = [
                "Avoid walls and all trails.",
                "Player 1: W A S D",
                "Player 2: Arrow Keys",
                "Esc: Back to menu during match",
                "M: Menu after round ends",
                "The system favors aggressive lanes",
                "and clean, cinematic turns.",
                "Press Enter or Esc to close.",
            ]
            for i, line in enumerate(lines):
                pyxel.text(30, 52 + i * 10, line, WHITE if i < 2 else LIGHT_BLUE)

    def draw_grid_background(self):
        for x in range(0, WIDTH, CELL * 2):
            pyxel.line(x, 0, x, HEIGHT, NAVY)
        for y in range(0, HEIGHT, CELL * 2):
            pyxel.line(0, y, WIDTH, y, NAVY)
        pyxel.rectb(4, 4, WIDTH - 8, HEIGHT - 8, DARK_BLUE)

    def draw_arena(self):
        self.draw_grid_background()

        for x in range(GRID_W):
            for y in range(GRID_H):
                color = self.grid[x][y]
                if color is not None:
                    px = x * CELL
                    py = y * CELL
                    pyxel.rect(px, py, CELL, CELL, color)
                    if pyxel.frame_count % 12 < 6:
                        pyxel.pset(px + 1, py + 1, WHITE)

        for bike in self.bikes:
            if bike.alive:
                px = bike.x * CELL
                py = bike.y * CELL
                pyxel.rect(px - 1, py - 1, CELL + 2, CELL + 2, bike.glow_color)
                pyxel.rect(px, py, CELL, CELL, bike.color)

        for x, y, _, _, life, color in self.sparkles:
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                pyxel.pset(int(x), int(y), color if life % 2 else WHITE)

    def draw_hud(self):
        pyxel.rect(0, 0, WIDTH, 12, BLACK)

        if len(self.bikes) >= 2:
            pyxel.text(6, 3, f"P1 {self.bikes[0].score}", CYAN)
            label = "SYS" if self.mode == "cpu" else "P2"
            pyxel.text(WIDTH - 44, 3, f"{label} {self.bikes[1].score}", ORANGE)

        mode_text = "1P VS SYSTEM" if self.mode == "cpu" else "2 PLAYER"
        pyxel.text(92, 3, mode_text, WHITE)

    def draw_round_over(self):
        pyxel.rect(40, 68, 160, 42, BLACK)
        pyxel.rectb(40, 68, 160, 42, WHITE)
        pyxel.text(92, 80, self.winner_text, YELLOW)
        pyxel.text(62, 92, "ENTER: next round  M: menu", LIGHT_BLUE)


TronGame()