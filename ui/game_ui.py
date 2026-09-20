# ui/game_ui.py
import pygame
from config import *
from core.game_engine import GameEngine
from models.data_model import Direction
from levels.level_data import LEVELS


class GameUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.font_sm = pygame.font.SysFont("simhei", 18)
        self.font_md = pygame.font.SysFont("simhei", 24)
        self.font_lg = pygame.font.SysFont("simhei", 48)
        self.font_title = pygame.font.SysFont("simhei", 60)
        self.font_win = pygame.font.SysFont("simhei", 52)
        self.font_lose = pygame.font.SysFont("simhei", 56)
        self.font_clear = pygame.font.SysFont("simhei", 48)

        self.running = True
        self.engine = GameEngine()

        # 主菜单按钮
        self.start_btn_rect = pygame.Rect(WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 + 20, 240, 50)
        self.select_btn_rect = pygame.Rect(WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 + 90, 240, 50)
        # 新增：退出游戏按钮（放在选择关卡下方）
        self.exit_btn_rect = pygame.Rect(WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 + 160, 240, 50)

        # 游戏内底部按钮
        self.reset_btn_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT - 60, 130, 40)
        self.game_menu_btn_rect = pygame.Rect(WINDOW_WIDTH // 2 + 20, WINDOW_HEIGHT - 60, 130, 40)

        # 撤销、提示按钮
        self.undo_btn_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT - 120, 130, 40)
        self.hint_btn_rect = pygame.Rect(WINDOW_WIDTH // 2 + 20, WINDOW_HEIGHT - 120, 130, 40)

        # 选关界面按钮
        self.back_btn_rect = pygame.Rect(WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT - 80, 160, 40)
        self.level_rects = []

        # 结算界面按钮（胜利）
        btn_width = 130
        btn_height = 45
        btn_y = 520
        gap = 20
        total_w = btn_width * 3 + gap * 2
        start_x = (WINDOW_WIDTH - total_w) // 2
        self.win_menu_btn = pygame.Rect(start_x, btn_y, btn_width, btn_height)
        self.win_replay_btn = pygame.Rect(start_x + btn_width + gap, btn_y, btn_width, btn_height)
        self.win_next_btn = pygame.Rect(start_x + (btn_width + gap) * 2, btn_y, btn_width, btn_height)

        # 结算界面按钮（失败）
        self.lose_menu_btn = pygame.Rect(WINDOW_WIDTH // 2 - btn_width - 15, btn_y + 30, btn_width, btn_height)
        self.lose_retry_btn = pygame.Rect(WINDOW_WIDTH // 2 + 15, btn_y + 30, btn_width, btn_height)

        # 全部通关界面按钮
        self.all_clear_menu_btn = pygame.Rect(WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 + 50, 240, 50)

    def draw_text(self, text, x, y, color=COLOR_TEXT, font=None):
        font = font or self.font_md
        self.screen.blit(font.render(text, True, color), (x, y))

    def draw_start_screen(self):
        self.screen.fill(COLOR_BG)
        title = self.font_title.render("一箭又一箭", True, COLOR_TEXT)
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 150))
        sub = self.font_sm.render("看准方向与遮挡，按顺序把箭头送出棋盘", True, (100, 100, 100))
        self.screen.blit(sub, (WINDOW_WIDTH // 2 - sub.get_width() // 2, 230))

        arr_font = pygame.font.SysFont("simhei", 60)
        self.draw_text("↑", WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT // 2 - 30, COLOR_ARROW, arr_font)
        self.draw_text("→", WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2 - 30, COLOR_ARROW, arr_font)
        self.draw_text("↓", WINDOW_WIDTH // 2 + 60, WINDOW_HEIGHT // 2 - 30, COLOR_ARROW, arr_font)
        self.draw_text("←", WINDOW_WIDTH // 2 + 180, WINDOW_HEIGHT // 2 - 30, COLOR_ARROW, arr_font)

        # 开始游戏按钮
        pygame.draw.rect(self.screen, COLOR_BTN, self.start_btn_rect, border_radius=25)
        start_text = self.font_md.render("开始游戏", True, COLOR_BTN_TEXT)
        self.screen.blit(start_text, (self.start_btn_rect.centerx - start_text.get_width() // 2,
                                      self.start_btn_rect.centery - start_text.get_height() // 2))

        # 选择关卡按钮
        pygame.draw.rect(self.screen, COLOR_BTN, self.select_btn_rect, border_radius=25)
        select_text = self.font_md.render("选择关卡", True, COLOR_BTN_TEXT)
        self.screen.blit(select_text, (self.select_btn_rect.centerx - select_text.get_width() // 2,
                                       self.select_btn_rect.centery - select_text.get_height() // 2))

        # 新增：退出游戏按钮
        pygame.draw.rect(self.screen, COLOR_BTN, self.exit_btn_rect, border_radius=25)
        exit_text = self.font_md.render("退出游戏", True, COLOR_BTN_TEXT)
        self.screen.blit(exit_text, (self.exit_btn_rect.centerx - exit_text.get_width() // 2,
                                     self.exit_btn_rect.centery - exit_text.get_height() // 2))

        tip1 = self.font_sm.render("每关 3 次失误机会，用尽即失败", True, (100, 100, 100))
        tip2 = self.font_sm.render("游戏中按 Esc 或点「主菜单」可返回这里", True, (100, 100, 100))
        self.screen.blit(tip1, (WINDOW_WIDTH // 2 - tip1.get_width() // 2, WINDOW_HEIGHT - 120))
        self.screen.blit(tip2, (WINDOW_WIDTH // 2 - tip2.get_width() // 2, WINDOW_HEIGHT - 90))

    def draw_select_level_screen(self):
        self.screen.fill(COLOR_BG)
        title = self.font_lg.render("选择关卡", True, COLOR_TEXT)
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 80))

        self.level_rects = []
        for i, level in enumerate(LEVELS):
            rect = pygame.Rect(WINDOW_WIDTH // 2 - 200, 180 + i * 70, 400, 50)
            self.level_rects.append(rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, border_radius=10)
            pygame.draw.rect(self.screen, (200, 200, 200), rect, 2, border_radius=10)

            text_id = self.font_md.render(str(i + 1), True, COLOR_BTN)
            text_name = self.font_md.render(level["name"], True, COLOR_TEXT)
            text_count = self.font_sm.render(f"{len(level['arrows'])} 个箭头", True, (150, 150, 150))

            self.screen.blit(text_id, (rect.x + 30, rect.y + 12))
            self.screen.blit(text_name, (rect.x + 70, rect.y + 12))
            self.screen.blit(text_count, (rect.right - 100, rect.y + 15))

        pygame.draw.rect(self.screen, (255, 255, 255), self.back_btn_rect, border_radius=20)
        pygame.draw.rect(self.screen, (200, 200, 200), self.back_btn_rect, 2, border_radius=20)
        back_text = self.font_md.render("返回", True, COLOR_TEXT)
        self.screen.blit(back_text, (self.back_btn_rect.centerx - back_text.get_width() // 2,
                                     self.back_btn_rect.centery - back_text.get_height() // 2))

    def draw_arrow(self, arrow, hint_coord=None):
        color = COLOR_ARROW
        if getattr(arrow, 'is_colliding', False):
            color = COLOR_COLLISION

        cx = arrow.px
        cy = arrow.py

        if hint_coord and (arrow.row, arrow.col) == hint_coord:
            pygame.draw.circle(self.screen, (255, 255, 0), (arrow.base_px, arrow.base_py), CELL_SIZE // 2 - 4, 3)

        L, w, head_w, head_h = 22, 8, 22, 12

        if arrow.direction == Direction.UP:
            pygame.draw.rect(self.screen, color, (cx - w // 2, cy - L, w, L))
            pygame.draw.polygon(self.screen, color,
                                [(cx - head_w // 2, cy - L), (cx + head_w // 2, cy - L), (cx, cy - L - head_h)])
        elif arrow.direction == Direction.DOWN:
            pygame.draw.rect(self.screen, color, (cx - w // 2, cy, w, L))
            pygame.draw.polygon(self.screen, color,
                                [(cx - head_w // 2, cy + L), (cx + head_w // 2, cy + L), (cx, cy + L + head_h)])
        elif arrow.direction == Direction.LEFT:
            pygame.draw.rect(self.screen, color, (cx - L, cy - w // 2, L, w))
            pygame.draw.polygon(self.screen, color,
                                [(cx - L, cy - head_w // 2), (cx - L, cy + head_w // 2), (cx - L - head_h, cy)])
        elif arrow.direction == Direction.RIGHT:
            pygame.draw.rect(self.screen, color, (cx, cy - w // 2, L, w))
            pygame.draw.polygon(self.screen, color,
                                [(cx + L, cy - head_w // 2), (cx + L, cy + head_w // 2), (cx + L + head_h, cy)])

    def draw_game_screen(self):
        self.screen.fill(COLOR_BG)

        if self.engine.message_timer > 0 and self.engine.message:
            msg_rect = pygame.Rect(GRID_OFFSET_X, 95, GRID_WIDTH, 35)
            pygame.draw.rect(self.screen, (255, 230, 230), msg_rect, border_radius=8)
            msg_text = self.font_sm.render(self.engine.message, True, (200, 0, 0))
            self.screen.blit(msg_text, (msg_rect.centerx - msg_text.get_width() // 2,
                                        msg_rect.centery - msg_text.get_height() // 2))

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                pygame.draw.rect(self.screen, COLOR_GRID,
                                 pygame.Rect(GRID_OFFSET_X + c * CELL_SIZE, GRID_OFFSET_Y + r * CELL_SIZE, CELL_SIZE,
                                             CELL_SIZE), 1)
                arrow = self.engine.grid[r][c]
                if arrow and arrow.is_visible:
                    self.draw_arrow(arrow, self.engine.hint_coord)

        for arrow in self.engine.flying_arrows:
            self.draw_arrow(arrow)

        level_name = LEVELS[self.engine.current_level_index]["name"]
        self.draw_text(f"关卡: {self.engine.current_level_index + 1} ({level_name})", 30, 30)
        self.draw_text(f"失误: {self.engine.mistakes} / {MAX_MISTAKES}", 350, 30)
        remain = sum(1 for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.engine.grid[r][c] is not None)
        self.draw_text(f"剩余箭头: {remain}", 550, 30)

        pygame.draw.rect(self.screen, COLOR_BTN_WHITE, self.undo_btn_rect, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_BTN_WHITE_BORDER, self.undo_btn_rect, 2, border_radius=8)
        self.draw_text("撤销", self.undo_btn_rect.x + 45, self.undo_btn_rect.y + 8, COLOR_BTN_WHITE_TEXT, self.font_sm)

        pygame.draw.rect(self.screen, COLOR_BTN_WHITE, self.hint_btn_rect, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_BTN_WHITE_BORDER, self.hint_btn_rect, 2, border_radius=8)
        self.draw_text("提示", self.hint_btn_rect.x + 45, self.hint_btn_rect.y + 8, COLOR_BTN_WHITE_TEXT, self.font_sm)

        pygame.draw.rect(self.screen, COLOR_BTN, self.reset_btn_rect, border_radius=8)
        self.draw_text("重新开始", self.reset_btn_rect.x + 25, self.reset_btn_rect.y + 8, COLOR_BTN_TEXT, self.font_sm)

        pygame.draw.rect(self.screen, COLOR_BTN_WHITE, self.game_menu_btn_rect, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_BTN_WHITE_BORDER, self.game_menu_btn_rect, 2, border_radius=8)
        self.draw_text("主菜单", self.game_menu_btn_rect.x + 35, self.game_menu_btn_rect.y + 8, COLOR_BTN_WHITE_TEXT,
                       self.font_sm)

    def draw_win_overlay(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        card_width = 500
        card_height = 400
        card_x = (WINDOW_WIDTH - card_width) // 2
        card_y = 120
        card_rect = pygame.Rect(card_x, card_y, card_width, card_height)

        pygame.draw.rect(self.screen, (255, 255, 255), card_rect, border_radius=20)
        pygame.draw.rect(self.screen, (220, 220, 220), card_rect, 2, border_radius=20)

        title_text = self.font_win.render("恭喜过关！", True, (0, 180, 80))
        self.screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, card_y + 50))

        stats_text = f"用时 {self.engine.elapsed_time:.1f} 秒  ·  失误 {self.engine.mistakes} 次  ·  提示 {self.engine.hint_count} 次"
        stats_surface = self.font_md.render(stats_text, True, (120, 120, 120))
        self.screen.blit(stats_surface, (WINDOW_WIDTH // 2 - stats_surface.get_width() // 2, card_y + 150))

        clear_text = f"本关 {self.engine.initial_arrow_count} 个箭头已全部清除"
        clear_surface = self.font_sm.render(clear_text, True, (150, 150, 150))
        self.screen.blit(clear_surface, (WINDOW_WIDTH // 2 - clear_surface.get_width() // 2, card_y + 200))

        pygame.draw.rect(self.screen, COLOR_BTN_WHITE, self.win_menu_btn, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_BTN_WHITE_BORDER, self.win_menu_btn, 2, border_radius=10)
        menu_text = self.font_md.render("主菜单", True, COLOR_BTN_WHITE_TEXT)
        self.screen.blit(menu_text, (self.win_menu_btn.centerx - menu_text.get_width() // 2,
                                     self.win_menu_btn.centery - menu_text.get_height() // 2))

        pygame.draw.rect(self.screen, COLOR_BTN_WHITE, self.win_replay_btn, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_BTN_WHITE_BORDER, self.win_replay_btn, 2, border_radius=10)
        replay_text = self.font_md.render("重玩本关", True, COLOR_BTN_WHITE_TEXT)
        self.screen.blit(replay_text, (self.win_replay_btn.centerx - replay_text.get_width() // 2,
                                       self.win_replay_btn.centery - replay_text.get_height() // 2))

        if self.engine.current_level_index + 1 >= len(LEVELS):
            next_btn_text = "完成挑战"
        else:
            next_btn_text = "下一关"

        pygame.draw.rect(self.screen, COLOR_BTN, self.win_next_btn, border_radius=10)
        next_text = self.font_md.render(next_btn_text, True, COLOR_BTN_TEXT)
        self.screen.blit(next_text, (self.win_next_btn.centerx - next_text.get_width() // 2,
                                     self.win_next_btn.centery - next_text.get_height() // 2))

    def draw_lose_overlay(self):
        self.screen.fill((245, 245, 245))

        title_text = self.font_lose.render("失败", True, (230, 50, 50))
        self.screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 200))

        subtitle_text = self.font_md.render("失误次数用尽了", True, (100, 100, 100))
        self.screen.blit(subtitle_text, (WINDOW_WIDTH // 2 - subtitle_text.get_width() // 2, 290))

        remain = sum(1 for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.engine.grid[r][c] is not None)
        cleared = self.engine.initial_arrow_count - remain
        stats_text = f"已清除 {cleared} 个，还剩 {remain} 个  ·  用时 {self.engine.elapsed_time:.1f} 秒"
        stats_surface = self.font_sm.render(stats_text, True, (150, 150, 150))
        self.screen.blit(stats_surface, (WINDOW_WIDTH // 2 - stats_surface.get_width() // 2, 350))

        pygame.draw.rect(self.screen, COLOR_BTN_WHITE, self.lose_menu_btn, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_BTN_WHITE_BORDER, self.lose_menu_btn, 2, border_radius=10)
        menu_text = self.font_md.render("主菜单", True, COLOR_BTN_WHITE_TEXT)
        self.screen.blit(menu_text, (self.lose_menu_btn.centerx - menu_text.get_width() // 2,
                                     self.lose_menu_btn.centery - menu_text.get_height() // 2))

        pygame.draw.rect(self.screen, COLOR_BTN, self.lose_retry_btn, border_radius=10)
        retry_text = self.font_md.render("重试本关", True, COLOR_BTN_TEXT)
        self.screen.blit(retry_text, (self.lose_retry_btn.centerx - retry_text.get_width() // 2,
                                      self.lose_retry_btn.centery - retry_text.get_height() // 2))

    def draw_all_clear_screen(self):
        self.screen.fill((250, 250, 250))

        title_text = self.font_clear.render("恭喜通过所有关卡！", True, (255, 165, 0))
        self.screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 200))

        sub_text = self.font_md.render("你已经完成了全部挑战，太强了！", True, (100, 100, 100))
        self.screen.blit(sub_text, (WINDOW_WIDTH // 2 - sub_text.get_width() // 2, 300))

        pygame.draw.rect(self.screen, COLOR_BTN, self.all_clear_menu_btn, border_radius=25)
        btn_text = self.font_md.render("返回主菜单", True, COLOR_BTN_TEXT)
        self.screen.blit(btn_text, (self.all_clear_menu_btn.centerx - btn_text.get_width() // 2,
                                    self.all_clear_menu_btn.centery - btn_text.get_height() // 2))

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            if self.engine.state == "START":
                self.draw_start_screen()
            elif self.engine.state == "SELECT_LEVEL":
                self.draw_select_level_screen()
            elif self.engine.state == "ALL_CLEAR":
                self.draw_all_clear_screen()
            else:
                self.draw_game_screen()
                self.engine.update()
                if self.engine.state == "WIN":
                    self.draw_win_overlay()
                elif self.engine.state == "LOSE":
                    self.draw_lose_overlay()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos

                    if self.engine.state == "START":
                        if self.start_btn_rect.collidepoint(mx, my):
                            self.engine.load_level(0)
                        elif self.select_btn_rect.collidepoint(mx, my):
                            self.engine.state = "SELECT_LEVEL"
                        # 新增：点击退出游戏按钮，结束程序
                        elif self.exit_btn_rect.collidepoint(mx, my):
                            self.running = False

                    elif self.engine.state == "SELECT_LEVEL":
                        if self.back_btn_rect.collidepoint(mx, my):
                            self.engine.state = "START"
                        else:
                            for i, rect in enumerate(self.level_rects):
                                if rect.collidepoint(mx, my):
                                    self.engine.load_level(i)
                                    break

                    elif self.engine.state == "PLAYING":
                        if self.undo_btn_rect.collidepoint(mx, my):
                            self.engine.undo()
                        elif self.hint_btn_rect.collidepoint(mx, my):
                            self.engine.get_hint()
                        elif self.reset_btn_rect.collidepoint(mx, my):
                            self.engine.reset_current_level()
                        elif self.game_menu_btn_rect.collidepoint(mx, my):
                            self.engine.state = "START"
                        else:
                            self.engine.handle_click(mx, my)

                    elif self.engine.state == "WIN":
                        if self.win_menu_btn.collidepoint(mx, my):
                            self.engine.state = "START"
                        elif self.win_replay_btn.collidepoint(mx, my):
                            self.engine.reset_current_level()
                        elif self.win_next_btn.collidepoint(mx, my):
                            next_level = self.engine.current_level_index + 1
                            if next_level >= len(LEVELS):
                                self.engine.state = "ALL_CLEAR"
                            else:
                                self.engine.load_level(next_level)

                    elif self.engine.state == "LOSE":
                        if self.lose_menu_btn.collidepoint(mx, my):
                            self.engine.state = "START"
                        elif self.lose_retry_btn.collidepoint(mx, my):
                            self.engine.reset_current_level()

                    elif self.engine.state == "ALL_CLEAR":
                        if self.all_clear_menu_btn.collidepoint(mx, my):
                            self.engine.state = "START"

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.engine.state = "START"

        pygame.quit()

    def start(self):
        self.run()