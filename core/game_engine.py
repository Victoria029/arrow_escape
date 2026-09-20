# core/game_engine.py
import copy
import math
import pygame
from config import GRID_SIZE, CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, MAX_MISTAKES, WINDOW_WIDTH, WINDOW_HEIGHT
from models.data_model import Arrow, Direction
from levels.level_data import LEVELS
from utils.logger import get_logger

logger = get_logger(__name__)


class GameEngine:
    def __init__(self):
        self.current_level_index = 0
        self.mistakes = 0
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.state = "START"
        self.history = []
        self.hint_coord = None
        self.hint_timer = 0

        self.hint_count = 0
        self.initial_arrow_count = 0
        self.start_time = 0
        self.elapsed_time = 0.0

        self.flying_arrows = []
        self.message = ""
        self.message_timer = 0

    def load_level(self, index: int):
        if index >= len(LEVELS):
            return

        self.current_level_index = index
        self.mistakes = 0
        self.state = "PLAYING"
        self.history = []
        self.hint_coord = None
        self.hint_timer = 0
        self.flying_arrows = []

        self.hint_count = 0
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0.0
        self.message = ""
        self.message_timer = 0

        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        level_data = LEVELS[index]
        self.initial_arrow_count = len(level_data["arrows"])

        for row, col, direction in level_data["arrows"]:
            self.grid[row][col] = Arrow(row, col, direction)

        logger.info(f"加载关卡 {index + 1} - {level_data['name']}")

    def reset_current_level(self):
        self.load_level(self.current_level_index)

    def undo(self):
        if self.history:
            self.grid = self.history.pop()
            self.mistakes = max(0, self.mistakes - 1)
            self.state = "PLAYING"
            self.hint_coord = None
            self.flying_arrows = []  # 修复：撤销时清空飞行动画
            logger.info("执行撤销操作")
        else:
            logger.info("没有可以撤销的操作")

    def get_hint(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                arrow = self.grid[r][c]
                if arrow and arrow.is_visible:
                    if self.get_blocking_arrow(arrow) is None:
                        self.hint_coord = (r, c)
                        self.hint_timer = 60
                        self.hint_count += 1
                        logger.info(f"提示坐标: {r}, {c}")
                        return

    def get_arrow_at(self, row: int, col: int) -> Arrow | None:
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            return self.grid[row][col]
        return None

    def get_blocking_arrow(self, arrow: Arrow) -> Arrow | None:
        r, c = arrow.row, arrow.col
        if arrow.direction == Direction.UP:
            for i in range(r - 1, -1, -1):
                if self.grid[i][c] is not None: return self.grid[i][c]
        elif arrow.direction == Direction.DOWN:
            for i in range(r + 1, GRID_SIZE):
                if self.grid[i][c] is not None: return self.grid[i][c]
        elif arrow.direction == Direction.LEFT:
            for i in range(c - 1, -1, -1):
                if self.grid[r][i] is not None: return self.grid[r][i]
        elif arrow.direction == Direction.RIGHT:
            for i in range(c + 1, GRID_SIZE):
                if self.grid[r][i] is not None: return self.grid[r][i]
        return None

    def handle_click(self, mouse_x: int, mouse_y: int):
        if self.state != "PLAYING":
            return

        col = (mouse_x - GRID_OFFSET_X) // CELL_SIZE
        row = (mouse_y - GRID_OFFSET_Y) // CELL_SIZE

        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            return

        arrow = self.get_arrow_at(row, col)
        if arrow is None or not arrow.is_visible:
            return

            # 修复：如果正在播放碰撞弹回动画，禁止点击，避免连点刷失误
        if arrow.is_colliding:
            return

        self.history.append(copy.deepcopy(self.grid))
        if len(self.history) > 20:
            self.history.pop(0)

        self.hint_coord = None

        blocking_arrow = self.get_blocking_arrow(arrow)

        if blocking_arrow is None:
            logger.info(f"箭头 ({row}, {col}) 路径畅通，成功飞出")
            self.grid[row][col] = None
            self.flying_arrows.append(arrow)
        else:
            logger.info(f"箭头 ({row}, {col}) 被阻挡，碰撞！")
            self.mistakes += 1
            arrow.is_colliding = True
            arrow.collide_timer = 30

            distance = abs(arrow.row - blocking_arrow.row) + abs(arrow.col - blocking_arrow.col)
            arrow.collide_offset = max(15, distance * CELL_SIZE - 50)

            self.message = "前方有箭头挡路，换一个试试"
            self.message_timer = 90

    def check_win(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] is not None:
                    return
        # 修复：必须等所有飞行动画播放完毕（即飞出屏幕）才能算作过关
        if not self.flying_arrows:
            self.state = "WIN"
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0
            logger.info(f"关卡 {self.current_level_index + 1} 通关！用时 {self.elapsed_time:.1f} 秒")

    def check_lose(self):
        if self.mistakes >= MAX_MISTAKES:
            self.state = "LOSE"
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0
            logger.info("失误次数耗尽，游戏失败！")

    def update(self):
        for arrow in self.flying_arrows[:]:
            if arrow.direction == Direction.UP:
                arrow.py -= 20
            elif arrow.direction == Direction.DOWN:
                arrow.py += 20
            elif arrow.direction == Direction.LEFT:
                arrow.px -= 20
            elif arrow.direction == Direction.RIGHT:
                arrow.px += 20

            if (arrow.px < -100 or arrow.px > WINDOW_WIDTH + 100 or
                    arrow.py < -100 or arrow.py > WINDOW_HEIGHT + 100):
                self.flying_arrows.remove(arrow)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                arrow = self.grid[r][c]
                if arrow and arrow.is_colliding:
                    arrow.collide_timer -= 1
                    progress = (30 - arrow.collide_timer) / 30
                    offset = math.sin(progress * math.pi) * arrow.collide_offset

                    if arrow.direction == Direction.UP:
                        arrow.px, arrow.py = arrow.base_px, arrow.base_py - offset
                    elif arrow.direction == Direction.DOWN:
                        arrow.px, arrow.py = arrow.base_px, arrow.base_py + offset
                    elif arrow.direction == Direction.LEFT:
                        arrow.px, arrow.py = arrow.base_px - offset, arrow.base_py
                    elif arrow.direction == Direction.RIGHT:
                        arrow.px, arrow.py = arrow.base_px + offset, arrow.base_py

                    if arrow.collide_timer <= 0:
                        arrow.is_colliding = False
                        arrow.px, arrow.py = arrow.base_px, arrow.base_py

        if self.state == "PLAYING":
            self.check_win()
            self.check_lose()

        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer <= 0:
                self.message = ""

        if self.hint_timer > 0:
            self.hint_timer -= 1
            if self.hint_timer <= 0:
                self.hint_coord = None