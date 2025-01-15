class Config:
    def __init__(self):
        # 窗口设置
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        
        # 游戏区域设置
        self.CELL_SIZE = 30
        self.ROWS = 20
        self.COLS = 10
        
        # 游戏设置
        self.INITIAL_FALL_SPEED = 1.0
        self.SPEED_INCREASE = 0.1
        self.LEVEL_LINES = 10
        
        # 分数设置
        self.SCORE_SINGLE = 100
        self.SCORE_DOUBLE = 300
        self.SCORE_TRIPLE = 500
        self.SCORE_TETRIS = 800 