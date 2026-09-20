# levels/level_data.py
import random
from models.data_model import Direction


def generate_level(num_arrows):
    """
    逆向生成关卡（保证100%有解，绝不出现死锁）
    :param num_arrows: 期望生成的箭头数量
    :return: [(row, col, Direction), ...]
    """
    # 初始化 5x5 的空网格
    grid = [[None for _ in range(5)] for _ in range(5)]
    positions = [(r, c) for r in range(5) for c in range(5)]

    # 打乱位置列表
    random.shuffle(positions)

    arrows = []
    directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

    for r, c in positions:
        if len(arrows) >= num_arrows:
            break

        # 打乱方向列表，尝试找到一个路径畅通的方向
        random.shuffle(directions)
        for d in directions:
            # 检查 (r,c) 沿方向 d 的路径上是否有其他箭头
            clear = True
            if d == Direction.UP:
                for i in range(r - 1, -1, -1):
                    if grid[i][c] is not None:
                        clear = False
                        break
            elif d == Direction.DOWN:
                for i in range(r + 1, 5):
                    if grid[i][c] is not None:
                        clear = False
                        break
            elif d == Direction.LEFT:
                for i in range(c - 1, -1, -1):
                    if grid[r][i] is not None:
                        clear = False
                        break
            elif d == Direction.RIGHT:
                for i in range(c + 1, 5):
                    if grid[r][i] is not None:
                        clear = False
                        break

            # 如果路径畅通（这个箭头能直接飞出），就放置它，并停止尝试其他方向
            if clear:
                grid[r][c] = d
                arrows.append((r, c, d))
                break

    # 最后打乱一次顺序，让玩家不容易看出生成顺序，增加解谜难度
    random.shuffle(arrows)
    return arrows


# 每次重新启动程序时，都会重新随机生成 5 个关卡
# 难度递增：8 -> 12 -> 14 -> 16 -> 18 个箭头
LEVELS = [
    {"id": 1, "name": "第 1 关", "arrows": generate_level(8)},
    {"id": 2, "name": "第 2 关", "arrows": generate_level(12)},
    {"id": 3, "name": "第 3 关", "arrows": generate_level(14)},
    {"id": 4, "name": "第 4 关", "arrows": generate_level(16)},
    {"id": 5, "name": "第 5 关", "arrows": generate_level(18)}
]