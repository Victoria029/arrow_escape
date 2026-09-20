# models/data_model.py
from enum import Enum
from config import GRID_OFFSET_X, GRID_OFFSET_Y, CELL_SIZE


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Arrow:
    def __init__(self, row: int, col: int, direction: Direction):
        self.row = row
        self.col = col
        self.direction = direction
        self.is_visible = True
        self.is_colliding = False
        self.collide_timer = 0
        self.collide_offset = 15  # 新增：碰撞时的最大位移距离（像素）

        # 动画像素坐标
        self.base_px = GRID_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
        self.base_py = GRID_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
        self.px = self.base_px
        self.py = self.base_py