import unittest
import sys
sys.path.append('src')
from game.tetris import Tetris

class TestCoreMechanics(unittest.TestCase):
    def setUp(self):
        self.game = Tetris()
        
    def test_piece_generation(self):
        """测试方块生成"""
        piece = self.game.generate_piece()
        self.assertIn('shape', piece)
        self.assertIn('color', piece)
        self.assertTrue(1 <= piece['color'] <= 7)
        
    def test_movement(self):
        """测试方块移动"""
        # 记录初始位置
        initial_pos = self.game.current_pos.copy()
        
        # 测试左移
        self.game.move_left()
        self.assertEqual(self.game.current_pos[1], initial_pos[1] - 1)
        
        # 测试右移
        self.game.move_right()
        self.assertEqual(self.game.current_pos[1], initial_pos[1])
        
        # 测试下移
        self.game.move_down()
        self.assertEqual(self.game.current_pos[0], initial_pos[0] + 1)
        
    def test_rotation(self):
        """测试方块旋转"""
        # 保存原始形状
        original_shape = [row[:] for row in self.game.current_piece['shape']]
        
        # 执行旋转
        self.game.rotate()
        
        # 验证形状已改变
        self.assertNotEqual(original_shape, self.game.current_piece['shape'])
        
    def test_collision(self):
        """测试碰撞检测"""
        # 测试边界碰撞
        self.game.current_pos = [0, -1]  # 左边界外
        self.assertFalse(self.game.is_valid_move(self.game.current_pos[0], self.game.current_pos[1]))
        
        # 测试底部碰撞
        self.game.current_pos = [self.game.config.ROWS, 0]  # 底部边界外
        self.assertFalse(self.game.is_valid_move(self.game.current_pos[0], self.game.current_pos[1]))
        
    def test_line_clear(self):
        """测试消除行"""
        # 创建一个完整行
        row = self.game.config.ROWS - 1
        for col in range(self.game.config.COLS):
            self.game.board[row][col] = 1
            
        # 执行消除检查
        initial_score = self.game.score
        self.game.check_lines()
        
        # 验证分数增加
        self.assertGreater(self.game.score, initial_score)
        
if __name__ == '__main__':
    unittest.main() 