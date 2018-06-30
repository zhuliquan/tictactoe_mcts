# 项目说明

> 这是一个使用python实现的蒙特卡罗树搜索玩TicTacToe游戏，
这里主要参考了一篇[MCTS的博文](https://int8.io/monte-carlo-tree-search-beginners-guide/)

## 文件说明

项目中有四个文件
- game.py 
- human.py 
- mcts.py 
- run_tictactoe.py
---
>比较重要的是game.py 和 mcts.py 文件。在game.py 中主要包含状态类State 和 游戏类Game
在mcts.py 中主要包含搜索树的节点类Node 和 搜索树类MCTS

## 运行程序
如果你想ai玩这个游戏你可以运行run_tictactoe.py这个文件。
```
python run_tictactoe.py
```

## 运行条件
- python 3.6.5
- numpy 1.13.3
- pandas 0.22.0
