#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : Administrator
# date   : 2018/6/28
from game import Game
from mcts import MCTS
from human import Human
from game import player_o
from game import player_x


if __name__ == '__main__':
    human = Human()
    ai = MCTS()
    players = {0: ai, 1: human}
    players_id = {ai: player_o, human: player_x}
    winner2result = {player_o: ai, player_x: human}

    turn = 0
    Game.start_player = players_id[players[turn]]  # tip: 这一步一定要在game初始化之前
    game = Game()
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
                print("winner {0}".format(winner2result[winner]))
            else:
                print("平局")
            break

        # 更新执棋方
        turn = (turn + 1) % 2

