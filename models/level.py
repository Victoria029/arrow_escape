# models/level.py
class Level:
    def __init__(self, level_id: int, arrows_data: list):
        self.level_id = level_id
        self.arrows_data = arrows_data