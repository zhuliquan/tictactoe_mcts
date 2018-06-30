#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : Administrator
# date   : 2018/6/26
import numpy as np
import pandas as pd
from game import State
from game import get_opponent
from copy import deepcopy


class Node:
    def __init__(self, state: State, parent=None):
        self.state = deepcopy(state)
        self.untried_actions = state.get_available_actions()
        self.parent = parent
        self.children = {}
        self.Q = 0  # 节点最终收益价值
        self.N = 0  # 节点被访问的次数

    def weight_func(self, c_param=1.4):
        if self.N != 0:
            # tip： 这里使用了-self.Q 因为子节点的收益代表的是对手的收益
            w = -self.Q / self.N + c_param * np.sqrt(2 * np.log(self.parent.N) / self.N)
        else:
            w = 0.0
        return w

    @staticmethod
    def get_random_action(available_actions):
        action_number = len(available_actions)
        action_index = np.random.choice(range(action_number))
        return available_actions[action_index]

    def select(self, c_param=1.4):
        """
        根据当前的子节点情况选择最优的动作并返回子节点
        :param c_param: 探索参数用于探索的比例
        :return: 最优动作，最优动作下的子节点
        """
        weights = [child_node.weight_func(c_param) for child_node in self.children.values()]
        action = pd.Series(data=weights, index=self.children.keys()).idxmax()
        next_node = self.children[action]
        return action, next_node

    def expand(self):
        """
        扩展子节点并返回刚扩展的子节点
        :return: 刚扩展出来的子节点
        """
        # 从没有尝试的节点中选择
        action = self.untried_actions.pop()
        # 获得当前的节点对应的玩家
        current_player = self.state.player
        # 获得下一步的局面
        next_board = self.state.board.copy()
        next_board[action] = current_player
        # 获得下一步的玩家
        next_player = get_opponent(current_player)
        # 扩展出一个子节点
        state = State(next_board, next_player)
        child_node = Node(state, self)
        self.children[action] = child_node
        return child_node

    def update(self, winner):
        """
        经过模拟之后更新节点的价值和访问次数
        :param winner: 返回模拟的胜者
        :return:
        """
        self.N += 1
        opponent = get_opponent(self.state.player)

        if winner == self.state.player:
            self.Q += 1
        elif winner == opponent:
            self.Q -= 1

        if self.is_root_node():
            self.parent.update(winner)

    def rollout(self):
        """
        从当前节点进行蒙特卡洛模拟返回模拟结果
        :return: 模拟结果
        """
        current_state = deepcopy(self.state)
        while True:
            is_over, winner = current_state.get_state_result()
            if is_over:
                break
            available_actions = current_state.get_available_actions()
            action = Node.get_random_action(available_actions)
            current_state = current_state.get_next_state(action)
        return winner

    def is_full_expand(self):
        """
        检测节点是否是已经完全扩展了
        :return: 返回节点是否完全扩展
        """
        return len(self.untried_actions) == 0

    def is_root_node(self):
        """
        检测节点是否是根节点
        :return: 返回节点是否是根节点
        """
        return self.parent


class MCTS:
    def __init__(self):
        self.root = None

    def __str__(self):
        return "ai"

    def simulation(self, count=1000):
        """
        用于模拟蒙特卡罗搜索
        :param count: 模拟的次数
        :return:
        """
        for _ in range(count):
            leaf_node = self.simulation_policy()
            winner = leaf_node.rollout()
            leaf_node.update(winner)

    def simulation_policy(self):
        """
        模拟过程中找到当前的叶子节点
        :return: 叶子节点
        """
        current_node = self.root
        while True:
            is_over, _ = current_node.state.get_state_result()
            if is_over:
                break
            if current_node.is_full_expand():
                _, current_node = current_node.select()
            else:
                return current_node.expand()
        leaf_node = current_node
        return leaf_node

    def take_action(self, current_state):
        """
        蒙特卡罗模拟选择最优动作
        :param current_state: 当前的状态
        :return: 最优动作
        """
        self.root = Node(current_state, None)
        self.simulation()
        action, _ = self.root.select(0.0)
        return action
