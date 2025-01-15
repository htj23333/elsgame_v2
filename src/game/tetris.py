from utils.config import Config
from utils.sound_manager import SoundManager
import random

class Tetris:
    # 七种俄罗斯方块的形状定义
    SHAPES = [
        [[1, 1, 1, 1]],  # I
        [[1, 1], [1, 1]],  # O
        [[0, 1, 0], [1, 1, 1]],  # T
        [[0, 0, 1], [1, 1, 1]],  # L
        [[1, 0, 0], [1, 1, 1]],  # J
        [[0, 1, 1], [1, 1, 0]],  # S
        [[1, 1, 0], [0, 1, 1]]   # Z  
    ]

    def __init__(self):
        self.config = Config()
        self.sound_manager = SoundManager()
        self.reset()
        
    def reset(self):
        self.board = [[0] * self.config.COLS for _ in range(self.config.ROWS)]
        self.current_piece = None
        self.current_pos = [0, 0]
        self.next_piece = self.generate_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.is_paused = False
        self.game_over = False
        self.spawn_piece()
        
    def generate_piece(self):
        """生成一个新的随机方块"""
        return {
            'shape': random.choice(self.SHAPES),
            'color': random.randint(1, 7)  # 1-7对应不同颜色
        }
        
    def spawn_piece(self):
        """在顶部生成新方块"""
        self.current_piece = self.next_piece
        self.next_piece = self.generate_piece()
        # 设置初始位置(居中)
        self.current_pos = [0, self.config.COLS // 2 - len(self.current_piece['shape'][0]) // 2]
        
        # 检查是否可以放置新方块
        if not self.is_valid_move(self.current_pos[0], self.current_pos[1]):
            self.game_over = True
            self.sound_manager.play_sound('gameover')
        
    def is_valid_move(self, row, col):
        """检查移动是否有效"""
        shape = self.current_piece['shape']
        for r in range(len(shape)):
            for c in range(len(shape[0])):
                if shape[r][c]:
                    new_row = row + r
                    new_col = col + c
                    if (new_row >= self.config.ROWS or 
                        new_col < 0 or 
                        new_col >= self.config.COLS or 
                        (new_row >= 0 and self.board[new_row][new_col])):
                        return False
        return True
        
    def move_left(self):
        """向左移动当前方块"""
        if self.is_paused or self.game_over:
            return
        if self.is_valid_move(self.current_pos[0], self.current_pos[1] - 1):
            self.current_pos[1] -= 1
            self.sound_manager.play_sound('move')
        
    def move_right(self):
        """向右移动当前方块"""
        if self.is_paused or self.game_over:
            return
        if self.is_valid_move(self.current_pos[0], self.current_pos[1] + 1):
            self.current_pos[1] += 1
            self.sound_manager.play_sound('move')
        
    def move_down(self):
        """向下移动当前方块"""
        if self.is_paused or self.game_over:
            return
        if self.is_valid_move(self.current_pos[0] + 1, self.current_pos[1]):
            self.current_pos[0] += 1
            self.sound_manager.play_sound('move')
            return True
        self.lock_piece()
        return False
        
    def rotate(self):
        """旋转当前方块"""
        if self.is_paused or self.game_over:
            return
            
        # 创建旋转后的形状
        current = self.current_piece['shape']
        rotated = [[current[j][i] for j in range(len(current)-1, -1, -1)]
                  for i in range(len(current[0]))]
                  
        # 保存原始形状
        original = self.current_piece['shape']
        self.current_piece['shape'] = rotated
        
        # 检查旋转是否有效
        if not self.is_valid_move(self.current_pos[0], self.current_pos[1]):
            self.current_piece['shape'] = original
            return
            
        self.sound_manager.play_sound('rotate')
        
    def lock_piece(self):
        """将当前方块锁定到游戏板上"""
        shape = self.current_piece['shape']
        for r in range(len(shape)):
            for c in range(len(shape[0])):
                if shape[r][c]:
                    self.board[self.current_pos[0] + r][self.current_pos[1] + c] = self.current_piece['color']
                    
        self.sound_manager.play_sound('drop')
        self.check_lines()
        self.spawn_piece()
        
    def check_lines(self):
        """检查并消除完整的行"""
        lines_cleared = 0
        r = self.config.ROWS - 1
        while r >= 0:
            if all(self.board[r]):
                lines_cleared += 1
                # 移除该行并在顶部添加新行
                self.board.pop(r)
                self.board.insert(0, [0] * self.config.COLS)
            else:
                r -= 1
                
        if lines_cleared > 0:
            self.sound_manager.play_sound('clear')
            self.update_score(lines_cleared)
            
    def update_score(self, lines_cleared):
        """更新分数和等级"""
        # 基础分数
        points = {
            1: self.config.SCORE_SINGLE,
            2: self.config.SCORE_DOUBLE,
            3: self.config.SCORE_TRIPLE,
            4: self.config.SCORE_TETRIS
        }
        # 计算基础分数
        base_score = points.get(lines_cleared, 0)
        # 添加等级加成
        level_bonus = self.level * 0.1 + 1  # 每级增加10%分数
        self.score += int(base_score * level_bonus)
        
        # 更新消除的行数和等级
        self.lines_cleared += lines_cleared
        old_level = self.level
        self.level = (self.lines_cleared // self.config.LEVEL_LINES) + 1
        
        # 如果升级了，播放音效
        if self.level > old_level:
            self.sound_manager.play_sound('clear')
        
    def update(self):
        """更新游戏状态"""
        if self.is_paused or self.game_over:
            return
            
        # 移除自动下落逻辑，由主循环控制
        pass
        
    def toggle_pause(self):
        """暂停/继续游戏"""
        if not self.game_over:  # 只有在游戏未结束时才能暂停
            self.is_paused = not self.is_paused
            self.sound_manager.play_sound('pause')
        
    def restart(self):
        """重新开始游戏"""
        self.sound_manager.play_sound('start')
        # 完全重置游戏状态
        self.board = [[0] * self.config.COLS for _ in range(self.config.ROWS)]
        self.current_piece = None
        self.current_pos = [0, 0]
        self.next_piece = self.generate_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.is_paused = False
        self.game_over = False
        self.spawn_piece() 