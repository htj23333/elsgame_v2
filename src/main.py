import pygame
import sys
from game.tetris import Tetris
from ui.game_ui import GameUI
from utils.config import Config
from utils.sound_manager import SoundManager

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.config = Config()
        self.screen = pygame.display.set_mode((
            self.config.WINDOW_WIDTH,
            self.config.WINDOW_HEIGHT
        ))
        pygame.display.set_caption("俄罗斯方块")
        
        self.sound_manager = SoundManager()
        self.game = Tetris()
        self.ui = GameUI(self.screen, self.game)
        self.clock = pygame.time.Clock()
        
        # 添加下落计时器
        self.last_fall_time = pygame.time.get_ticks()
        self.fall_delay = 1000  # 初始下落延迟(毫秒)
        
        # 添加按键延迟控制
        self.key_delay = 100  # 按键延迟(毫秒)
        self.last_move_time = 0  # 上次移动时间
        self.last_rotate_time = 0  # 上次旋转时间
        self.rotate_delay = 200  # 旋转延迟(毫秒)
        
    def handle_events(self):
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.game.restart()
                    self.last_fall_time = current_time
                    self.fall_delay = 1000
                elif event.key == pygame.K_SPACE:
                    self.game.toggle_pause()
                    
        # 获取当前按下的所有键
        keys = pygame.key.get_pressed()
        if not self.game.is_paused and not self.game.game_over:
            # 左右移动添加延迟
            if current_time - self.last_move_time > self.key_delay:
                if keys[pygame.K_LEFT]:
                    self.game.move_left()
                    self.last_move_time = current_time
                elif keys[pygame.K_RIGHT]:
                    self.game.move_right()
                    self.last_move_time = current_time
                    
            # 下移动不需要太多延迟
            if keys[pygame.K_DOWN]:
                self.game.move_down()
                
            # 旋转添加更长的延迟
            if keys[pygame.K_UP] and current_time - self.last_rotate_time > self.rotate_delay:
                self.game.rotate()
                self.last_rotate_time = current_time
                    
        return True
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            
            if not self.game.is_paused and not self.game.game_over:
                # 控制自动下落速度
                current_time = pygame.time.get_ticks()
                if current_time - self.last_fall_time > self.fall_delay:
                    self.game.move_down()
                    self.last_fall_time = current_time
                    # 根据等级调整下落速度，但限制最快速度
                    self.fall_delay = max(300, 1000 - (self.game.level - 1) * 50)  # 降低速度增长率
            
            self.ui.draw()
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = TetrisGame()
    game.run() 