import unittest
import pygame
import sys
sys.path.append('src')
from ui.game_ui import GameUI
from game.tetris import Tetris

class TestGameUI(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.game = Tetris()
        self.ui = GameUI(self.screen, self.game)
        
    def tearDown(self):
        pygame.quit()
        
    def test_init(self):
        """测试UI初始化"""
        self.assertIsNotNone(self.ui.colors)
        self.assertIsNotNone(self.ui.font_large)
        self.assertIsNotNone(self.ui.font_medium)
        self.assertIsNotNone(self.ui.font_small)
        
    def test_dimensions(self):
        """测试游戏区域尺寸计算"""
        self.assertEqual(self.ui.game_width, self.ui.config.COLS * self.ui.config.CELL_SIZE)
        self.assertEqual(self.ui.game_height, self.ui.config.ROWS * self.ui.config.CELL_SIZE)
        
    def test_draw_functions(self):
        """测试所有绘制函数"""
        # 测试基本绘制
        self.ui.draw()
        
        # 测试暂停状态
        self.game.is_paused = True
        self.ui.draw()
        
        # 测试游戏结束状态
        self.game.is_paused = False
        self.game.game_over = True
        self.ui.draw()
        
if __name__ == '__main__':
    unittest.main() 