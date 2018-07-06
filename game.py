#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : Administrator
# date   : 2018/6/26
import numpy as np
player_o = 1
player_x = -1


def get_opponent(player):
    """
    返回对手
    :param player: 玩家
    :return: 返回输入玩家的对手
    """
    opponent = player_o if player == player_x else player_x
    return opponent


class State:

    def __init__(self, board, player):
        self.board = board.copy()
        self.player = player

    def __eq__(self, other):
        if (self.board == other.board).all() and self.player == other.player:
            return True
        else:
            return False

    def get_available_actions(self):
        """
        感觉状态的局面返回可以落子的位置，这些位置称之为动作
        :return: 可行的动作
        """
        space = np.where(self.board == 0)
        coordinate = zip(space[0], space[1])
        available_actions = [(i, j) for i, j in coordinate]
        return available_actions

    def get_state_result(self):
        """
        返回状态对应局面的结果
        如果游戏是已经结束了 is_over = True 如果没有 is_over = False, winner = None
        如果游戏已经结束可以分为三种结果: x 的胜利, o 的胜利, 平局
        winner 可以取[x,o,None]这三种情况
        :return: 返回一个元组(is_over, winner)
        """
        board = self.board
        sum_row = np.sum(board, 0)
        sum_col = np.sum(board, 1)
        diag_sum_tl = board.trace()
        diag_sum_tr = np.fliplr(board).trace()

        n = self.board.shape[0]
        if (sum_row == n).any() or (sum_col == n).any() or diag_sum_tl == n or diag_sum_tr == n:
            is_over, winner = True, player_o
        elif (sum_row == -n).any() or (sum_col == -n).any() or diag_sum_tl == -n or diag_sum_tr == -n:
            is_over, winner = True, player_x
        elif (board != 0).all():
            is_over, winner = True, None
        else:
            is_over, winner = False, None

        return is_over, winner

    def get_next_state(self, action):
        """
        根据动作返回一个新的状态
        :param action: 动作
        :return: 新的状态
        """
        next_board = self.board.copy()
        next_board[action] = self.player
        next_player = get_opponent(self.player)
        next_state = State(next_board, next_player)
        return next_state


class Game:
    start_player = player_o
    game_size = 3

    def __init__(self, state=None):
        if state:
            if state.board.shape[0] != Game.game_size:
                raise Exception("用于初始化的棋盘尺寸不对")

            board = state.board
            player = state.player
        else:
            board = np.zeros((Game.game_size, Game.game_size), dtype=np.int32)
            player = Game.start_player
        self.state = State(board, player)

    def reset(self, state=None):
        """
        初始化游戏局面
        可以默认初始化，也可以使用外界的状态进行初始化
        :param state: None 表示默认初始化，其他情况是利用外界状态初始化
        """
        if state:
            if state.board.shape[0] != Game.game_size:
                raise Exception("用于初始化的棋盘尺寸不对")
            board = state.board
            player = state.player
            self.state = State(board, player)
        else:
            self.state.board = np.zeros((Game.game_size, Game.game_size), dtype=np.int32)
            self.state.player = Game.start_player
        return self.state

    def step(self, action):
        """
        在局面上采取动作，采取动作会修改游戏的当前状态
        :param action: 在局面可以落子的位置
        :return: 新的状态
        """
        if action:
            self.state = self.state.get_next_state(action)
        return self.state

    def game_result(self):
        """
        采取动作后返回游戏的结果
        :return: tuple (is_over, winner)
        """
        return self.state.get_state_result()

    def render(self, board=None):
        """
        渲染当前的局面和使用外界的局面去渲染
        :param board: None 表示使用自己的局面进行渲染，其他情况是使用外界的局面进行渲染
        :return:
        """
        if board:
            if board.shape[0] != Game.game_size:
                raise Exception("用于初始化的棋盘尺寸不对")
        else:
            board = self.state.board

        for i in range(Game.game_size):
            for j in range(Game.game_size):
                if board[i, j] == player_x:
                    print(" x ", end="")
                elif board[i, j] == player_o:
                    print(" o ", end="")
                else:
                    print(" . ", end="")
            print()

