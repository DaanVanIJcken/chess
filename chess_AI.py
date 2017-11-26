#!/usr/bin/env python

import random


def pos_neg(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def possible_moves(current_pos: tuple, board: list) -> list:
    try:
        if board[current_pos[0]][current_pos[1]] == ' ':
            return []
    except IndexError:
        return []
    piece, to_return = board[current_pos[0]][current_pos[1]], []

    if 'pawn' in piece:
        if 'w_' in piece:
            if current_pos[0] == 6:
                returnable = [(-1, 0), (-2, 0)]
            else:
                returnable = [(-1, 0)]
            try:
                if board[current_pos[0] - 1][current_pos[1] - 1][0] == 'b':
                    to_return.append((current_pos[0] - 1, current_pos[1] - 1))
            except IndexError:
                pass
            try:
                if board[current_pos[0] - 1][current_pos[1] + 1][0] == 'b':
                    to_return.append((current_pos[0] - 1, current_pos[1] + 1))
            except IndexError:
                pass
        else:
            if current_pos[0] == 1:
                returnable = [(1, 0), (2, 0)]
            else:
                returnable = [(1, 0)]
            try:
                if board[current_pos[0] + 1][current_pos[1] - 1][0] == 'w':
                    to_return.append((current_pos[0] + 1, current_pos[1] - 1))
            except IndexError:
                pass
            try:
                if board[current_pos[0] + 1][current_pos[1] + 1][0] == 'w':
                    to_return.append((current_pos[0] + 1, current_pos[1] + 1))
            except IndexError:
                pass
    if 'knight' in piece:
        returnable = [(-2, -1), (-1, -2), (+1, -2), (+2, -1), (-2, +1),
                      (+2, +1), (-1, +2), (+1, +2)]
    if 'rook' in piece:
        returnable = [(i1, i2) for i1 in range(-7, 8) for i2 in range(-7, 8) if
                      (i1 == 0 or i2 == 0) and not (i1 == i2 == 0)]
    if 'bishop' in piece:
        returnable = [(i1, i2) for i1 in range(-7, 8) for i2 in range(-7, 8) if
                      i1 * i1 == i2 * i2 and not (i1 == i2 == 0)]
    if 'queen' in piece:
        returnable = [(i1, i2) for i1 in range(-7, 8) for i2 in range(-7, 8) if
                      (i1 * i1 == i2 * i2 or (i1 == 0 or i2 == 0)) and not (
                          i1 == i2 == 0)]
    if 'king' in piece:
        returnable = [(i1, i2) for i1 in range(-1, 2) for i2 in range(-1, 2) if
                      not (i1 == i2 == 0)]

    for (coord1, coord2) in returnable:
        # looks if the first spot in this row is empty
        no_knight = 'knight' not in piece
        condition1 = (not (board[current_pos[0]
                                 + pos_neg(coord1)][current_pos[1]
                                                    + pos_neg(coord2)][0] in
                           [' ', ('b' if 'w_' in piece else 'w')]) and
                      no_knight)
        # checks if spot is empty
        condition2 = (not (board[current_pos[0]
                                 + coord1][current_pos[1]
                                           + coord2][0] in
                           [' ', 'b' if 'w_' in piece else 'w']))
        # checks if the total of both is < 0, or checks that it cant hit forward for a pawn
        condition3_1 = (current_pos[0] + coord1 < 0) or (current_pos[1] + coord2 < 0)
        condition3_2 = ('pawn' in piece and coord2 == 0 and board[current_pos[0] + coord1]
            [current_pos[1] + coord2][0] in ('b' if 'w_' in piece else 'w'))
        condition3 = condition3_1 or condition3_2
        try:
            if condition1 or condition2 or condition3:
                continue

            if 'knight' not in piece:
                # checks if the spots till the desired pos are all empty... (extension of the first check)
                if any([True
                        for a in range(min(current_pos[0] + coord1,
                                           current_pos[0])
                                               + (0 if coord1 == 0 else 1),
                                       max(current_pos[0] + coord1,
                                           current_pos[0])
                                               + (1 if coord1 == 0 else 0))
                        for b in range(min(current_pos[1] + coord2,
                                           current_pos[1])
                                               + (0 if coord2 == 0 else 1),
                                       max(current_pos[1] + coord2,
                                           current_pos[1]) + (
                                               1 if coord2 == 0 else 0))
                        if not(board[a][b] in [' ', ('b' if 'w_' in piece
                                                     else 'w')]) and
                                (not('bishop' in piece) or (current_pos[0]+a)
                                    * (current_pos[0]+a) == (current_pos[1]+b)  # ==
                                    * (current_pos[1]+b))]):
                    continue

            to_return.append((current_pos[0] + coord1, current_pos[1] + coord2))

            to_return.append((current_pos[0] + coord1, current_pos[1] + coord2))
        except IndexError:
            pass
    return to_return


def get_king(board, team: str):
    for i, line in enumerate(board):
        for j, piece in enumerate(line):
            if piece == 'w_king' if team == 'w_' else piece == 'b_king':
                king_pos = (i, j)
                return king_pos


def check_pos(board, pos, team, king=False) -> list:  # can team kill what is on pos
    routes = []
    for i, line in enumerate(board):
        for j, piece in enumerate(line):
            if piece[:2] == team:
                if pos in possible_moves((i, j), board):
                    if king:
                        return [{"from": (i, j), "to": pos}]
                    else:
                        routes.append({"from": (i, j), "to": pos})
    return routes


def team_to_opponent(team):
    return 'b_' if team == 'w_' else 'w_'


def move_king(board: list, team, king_pos: tuple) -> dict:
    opponent = team_to_opponent(team)
    for move in possible_moves(king_pos, board):
        if not check_pos(board, move, opponent):
            return {"from": king_pos, "to": move}
    return {}


def think(board, team):
    team = 'b_' if team == 'black' else 'w_'
    opponent = team_to_opponent(team)
    king_pos_team = get_king(board, team)
    king_pos_opponent = get_king(board, opponent)

    # kill the enemy king
    if check_pos(board, king_pos_opponent, team, king=True):
        return check_pos(board, king_pos_opponent, team, king=True)[0]
    del king_pos_opponent

    # defend my own king
    if check_pos(board, king_pos_team, opponent):
        # can my king be killed next turn
        if len(check_pos(board, king_pos_team, opponent)) == 1:
            # my king can only be killed one way.
            attack = check_pos(board, king_pos_team, opponent)[0]["from"]
            # from what position can my king be killed
            if check_pos(board, attack, team):
                # I can kill whatever is check'ing my king

                # find which pieces can kill the attacker
                # without opening the king to a new attack
                defenders = []
                for attacker in check_pos(board, attack, opponent):
                    coord1 = attacker['from'][0]
                    coord2 = attacker['from'][1]
                    fake_board = eval(str(board))
                    fake_board[coord1][coord2] = ' '
                    fake_board[attack[0]][attack[1]] = ' '
                    if check_pos(board, king_pos_team, opponent):
                        defenders.append((coord1, coord2))
                del coord1, coord2, fake_board
                if len(defenders) < 0:
                    if check_pos(board, attack, opponent):
                        # the attacker is defended by another piece
                        if move_king(board, team, king_pos_team):
                            # try to move the king if you can
                            return move_king(board, team, king_pos_team)
                        else:
                            # todo find what piece is best to lose
                            pass
                    else:
                        return random.choice(defenders)
                else:
                    # todo try to block the enemy
            else:
                return move_king(board, team, king_pos_team)
        else:
            if move_king(board, team, king_pos_team):
                # try to move the king if you can
                return move_king(board, team, king_pos_team)
            
