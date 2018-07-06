#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : Administrator
# date   : 2018/6/28
from game import Game
from mcts import MCTS
from human import Human


if __name__ == '__main__':
    game = Game()
    human = Human()
    ai = MCTS()
    players = {0: ai, 1: human}

    turn = 0
    while True:
        current_state = game.state
        action = players[turn].take_action(current_state)
        game.step(action)
        game.render()
        print("###{0}在{1}落子###".format(players[turn], action))

        # 判断结果
        is_over, winner = game.game_result()
        if is_over:
            if winner:
                print("winner {0}".format(players[turn]))
            else:
                print("平局")
            break

        # 更新执棋方
        turn = (turn + 1) % 2


