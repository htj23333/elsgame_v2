import unittest
import sys
import os

# 添加源代码目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# 导入测试模块
from test_game_ui import TestGameUI
from test_core_mechanics import TestCoreMechanics
from test_basic_functions import TestBasicFunctions

def run_tests():
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGameUI))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCoreMechanics))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBasicFunctions))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 返回测试结果
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1) 