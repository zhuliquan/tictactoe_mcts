#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : Administrator
# date   : 2018/6/29


class Human:
    def __init__(self):
        pass

    def __str__(self):
        return "human"

    def take_action(self, current_state):
        """
        人类玩家采取动作
        :param current_state: 当前的状态
        :return: 最优动作
        """
        while True:
            while True:
                command = input("以 i,j 形式输入你的落子，例如1,2:")
                try:
                    i, j = [int(index) for index in command.split(",")]
                    break
                except:
                    print("输入格式不对,请从新输入")
            action = i, j
            if action not in current_state.get_available_actions():
                print("输入的位置有问题,请从新输入")
            else:
                break
        return action
