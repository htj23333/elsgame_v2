import pygame
from utils.config import Config

class GameUI:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.config = Config()
        self.init_colors()
        self.init_fonts()
        self.calculate_dimensions()
        
    def init_colors(self):
        self.colors = {
            # 深色主题背景色
            'background': (25, 25, 35),  # 深蓝灰色背景
            'grid': (45, 45, 55),        # 稍亮的网格线
            'text': (220, 220, 230),     # 柔和的白色文字
            
            # 方块颜色 - 使用现代柔和的色调
            'piece_colors': [
                None,  # 0 = empty
                (0, 184, 212),    # I - 青色
                (0, 200, 83),     # O - 绿色
                (255, 193, 7),    # T - 琥珀色
                (244, 67, 54),    # L - 红色
                (33, 150, 243),   # J - 蓝色
                (255, 152, 0),    # S - 橙色
                (156, 39, 176)    # Z - 紫色
            ]
        }
        
        # 添加高亮色用于方块边缘
        self.highlight_colors = []
        self.shadow_colors = []
        
        # 为每个方块颜色生成高亮和阴影色
        for color in self.colors['piece_colors']:
            if color is not None:
                # 高亮色 - 增加亮度
                highlight = tuple(min(c + 40, 255) for c in color)
                self.highlight_colors.append(highlight)
                
                # 阴影色 - 降低亮度
                shadow = tuple(max(c - 40, 0) for c in color)
                self.shadow_colors.append(shadow)
            else:
                self.highlight_colors.append(None)
                self.shadow_colors.append(None)
        
    def init_fonts(self):
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
    def calculate_dimensions(self):
        """计算游戏区域的尺寸和位置"""
        # 游戏区域
        self.game_width = self.config.COLS * self.config.CELL_SIZE
        self.game_height = self.config.ROWS * self.config.CELL_SIZE
        self.game_x = (self.config.WINDOW_WIDTH - self.game_width) // 2
        self.game_y = (self.config.WINDOW_HEIGHT - self.game_height) // 2
        
        # 预览区域
        self.preview_size = self.config.CELL_SIZE * 4
        self.preview_x = self.game_x + self.game_width + 50
        self.preview_y = self.game_y
        
    def draw(self):
        self.screen.fill(self.colors['background'])
        self.draw_grid()
        self.draw_board()
        self.draw_current_piece()
        self.draw_next_piece()
        self.draw_score()
        
        if self.game.is_paused:
            self.draw_pause_screen()
        elif self.game.game_over:
            self.draw_game_over_screen()
            
    def draw_grid(self):
        """绘制游戏网格"""
        # 绘制边框
        pygame.draw.rect(self.screen, self.colors['grid'],
                        (self.game_x - 2, self.game_y - 2,
                         self.game_width + 4, self.game_height + 4), 2)
        
        # 绘制网格线
        for x in range(self.config.COLS + 1):
            pygame.draw.line(self.screen, self.colors['grid'],
                           (self.game_x + x * self.config.CELL_SIZE, self.game_y),
                           (self.game_x + x * self.config.CELL_SIZE, self.game_y + self.game_height))
                           
        for y in range(self.config.ROWS + 1):
            pygame.draw.line(self.screen, self.colors['grid'],
                           (self.game_x, self.game_y + y * self.config.CELL_SIZE),
                           (self.game_x + self.game_width, self.game_y + y * self.config.CELL_SIZE))
                           
    def draw_board(self):
        """绘制游戏板上的已固定方块"""
        for row in range(self.config.ROWS):
            for col in range(self.config.COLS):
                if self.game.board[row][col]:
                    self.draw_cell(row, col, self.game.board[row][col])
                    
    def draw_current_piece(self):
        """绘制当前方块"""
        if not self.game.current_piece:
            return
            
        shape = self.game.current_piece['shape']
        color = self.game.current_piece['color']
        
        for row in range(len(shape)):
            for col in range(len(shape[0])):
                if shape[row][col]:
                    self.draw_cell(
                        self.game.current_pos[0] + row,
                        self.game.current_pos[1] + col,
                        color
                    )
                    
    def draw_cell(self, row, col, color_index):
        """绘制单个方块"""
        if color_index <= 0 or color_index >= len(self.colors['piece_colors']):
            return
            
        color = self.colors['piece_colors'][color_index]
        highlight = self.highlight_colors[color_index]
        shadow = self.shadow_colors[color_index]
        
        x = self.game_x + col * self.config.CELL_SIZE
        y = self.game_y + row * self.config.CELL_SIZE
        size = self.config.CELL_SIZE
        
        # 绘制主体
        pygame.draw.rect(self.screen, color,
                        (x, y, size, size))
        
        # 绘制高亮边缘（左上）
        pygame.draw.line(self.screen, highlight, (x, y), (x + size - 1, y), 2)
        pygame.draw.line(self.screen, highlight, (x, y), (x, y + size - 1), 2)
        
        # 绘制阴影边缘（右下）
        pygame.draw.line(self.screen, shadow, (x + size - 1, y), (x + size - 1, y + size - 1), 2)
        pygame.draw.line(self.screen, shadow, (x, y + size - 1), (x + size - 1, y + size - 1), 2)
        
    def draw_next_piece(self):
        """绘制下一个方块预览"""
        if not self.game.next_piece:
            return
            
        # 绘制预览区边框
        pygame.draw.rect(self.screen, self.colors['grid'],
                        (self.preview_x - 2, self.preview_y - 2,
                         self.preview_size + 4, self.preview_size + 4), 2)
                         
        # 绘制"NEXT"文字
        text = self.font_medium.render("NEXT", True, self.colors['text'])
        self.screen.blit(text, (self.preview_x, self.preview_y - 40))
        
        shape = self.game.next_piece['shape']
        color = self.game.next_piece['color']
        
        # 计算居中位置
        cell_size = self.preview_size // 4
        offset_x = (self.preview_size - len(shape[0]) * cell_size) // 2
        offset_y = (self.preview_size - len(shape) * cell_size) // 2
        
        for row in range(len(shape)):
            for col in range(len(shape[0])):
                if shape[row][col]:
                    x = self.preview_x + offset_x + col * cell_size
                    y = self.preview_y + offset_y + row * cell_size
                    pygame.draw.rect(self.screen, self.colors['piece_colors'][color],
                                   (x, y, cell_size, cell_size))
                    pygame.draw.rect(self.screen, (self.colors['piece_colors'][color][0]//2,
                                                 self.colors['piece_colors'][color][1]//2,
                                                 self.colors['piece_colors'][color][2]//2),
                                   (x, y, cell_size, cell_size), 1)
                                   
    def draw_score(self):
        """绘制分数"""
        score_x = self.preview_x
        score_y = self.preview_y + self.preview_size + 40
        
        text = self.font_medium.render("SCORE", True, self.colors['text'])
        self.screen.blit(text, (score_x, score_y))
        
        score = self.font_large.render(str(self.game.score), True, self.colors['text'])
        self.screen.blit(score, (score_x, score_y + 40))
        
    def draw_pause_screen(self):
        """绘制暂停界面"""
        self.draw_overlay()
        text = self.font_large.render("PAUSED", True, self.colors['text'])
        text_rect = text.get_rect(center=(self.config.WINDOW_WIDTH // 2,
                                        self.config.WINDOW_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
    def draw_game_over_screen(self):
        """绘制游戏结束界面"""
        self.draw_overlay()
        text1 = self.font_large.render("GAME OVER", True, self.colors['text'])
        text2 = self.font_medium.render("Press R to Restart", True, self.colors['text'])
        
        text1_rect = text1.get_rect(center=(self.config.WINDOW_WIDTH // 2,
                                          self.config.WINDOW_HEIGHT // 2 - 30))
        text2_rect = text2.get_rect(center=(self.config.WINDOW_WIDTH // 2,
                                          self.config.WINDOW_HEIGHT // 2 + 30))
                                          
        self.screen.blit(text1, text1_rect)
        self.screen.blit(text2, text2_rect)
        
    def draw_overlay(self):
        """绘制半透明遮罩"""
        overlay = pygame.Surface((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0)) 