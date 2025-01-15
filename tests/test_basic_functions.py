import unittest
import sys
sys.path.append('src')
from game.tetris import Tetris
from utils.sound_manager import SoundManager

class TestBasicFunctions(unittest.TestCase):
    def setUp(self):
        self.game = Tetris()
        self.sound_manager = SoundManager()
        
    def test_pause_resume(self):
        """测试暂停/继续功能"""
        # 初始状态
        self.assertFalse(self.game.is_paused)
        
        # 暂停
        self.game.toggle_pause()
        self.assertTrue(self.game.is_paused)
        
        # 继续
        self.game.toggle_pause()
        self.assertFalse(self.game.is_paused)
        
    def test_restart(self):
        """测试重新开始功能"""
        # 修改游戏状态
        self.game.score = 1000
        self.game.level = 5
        self.game.is_paused = True
        
        # 重新开始
        self.game.restart()
        
        # 验证状态重置
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.level, 1)
        self.assertFalse(self.game.is_paused)
        
    def test_sound_system(self):
        """测试音效系统"""
        # 测试音效加载
        self.assertIsNotNone(self.sound_manager.sounds)
        
        # 测试音效开关
        self.assertTrue(self.sound_manager.sound_enabled)
        self.sound_manager.toggle_sound()
        self.assertFalse(self.sound_manager.sound_enabled)
        
        # 测试各种音效播放
        self.sound_manager.play_move()
        self.sound_manager.play_rotate()
        self.sound_manager.play_clear()
        self.sound_manager.play_drop()
        self.sound_manager.play_pause()
        self.sound_manager.play_start()
        self.sound_manager.play_gameover()
        
if __name__ == '__main__':
    unittest.main() 