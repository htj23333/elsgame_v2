# Title
核心机制测试

# Description
验证游戏核心机制的正确性

# Test Cases
1. 方块控制测试
   - 验证左右移动
   - 验证旋转
   - 验证加速下落
   
2. 碰撞检测测试
   - 验证边界碰撞
   - 验证方块间碰撞
   
3. 消除机制测试
   - 验证单行消除
   - 验证多行同时消除
   
4. 计分系统测试
   - 验证基础得分
   - 验证连消加分

# Dependencies
- [ ] {003} 核心机制实现

# Status History
- 2024-01-15: Created
- 2024-01-15: [ ] 等待核心机制实现完成后进行测试
- 2024-01-15: [-] 开始核心机制测试
- 2024-01-15: [x] 核心机制测试用例编写完成

# Test Results
1. 方块控制测试
   - [x] test_piece_generation: 通过
   - [x] test_movement: 通过
   - [x] test_rotation: 通过

2. 碰撞检测测试
   - [x] test_collision: 通过

3. 消除机制测试
   - [x] test_line_clear: 通过 