#!/usr/bin/env python

import random


def pos_neg(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def possible_moves(CurrentPos: tuple, board: list) -> list:
    try:
        if board[CurrentPos[0]][CurrentPos[1]] == ' ':
            return []
    except NameError:
        return []
    except IndexError:
        return []
    piece, to_return = board[CurrentPos[0]][CurrentPos[1]], []

    if 'pawn' in piece:
        if 'w_' in piece:
            if CurrentPos[0] == 6:
                returnable = [(-1, 0), (-2, 0)]
            else:
                returnable = [(-1, 0)]
            try:
                if board[CurrentPos[0] - 1][CurrentPos[1] - 1][0] == 'b':
                    to_return.append((CurrentPos[0] - 1, CurrentPos[1] - 1))
            except IndexError:
                pass
            try:
                if board[CurrentPos[0] - 1][CurrentPos[1] + 1][0] == 'b':
                    to_return.append((CurrentPos[0] - 1, CurrentPos[1] + 1))
            except IndexError:
                pass
        else:
            if CurrentPos[0] == 1:
                returnable = [(1, 0), (2, 0)]
            else:
                returnable = [(1, 0)]
            try:
                if board[CurrentPos[0] + 1][CurrentPos[1] - 1][0] == 'w':
                    to_return.append((CurrentPos[0] + 1, CurrentPos[1] - 1))
            except IndexError:
                pass
            try:
                if board[CurrentPos[0] + 1][CurrentPos[1] + 1][0] == 'w':
                    to_return.append((CurrentPos[0] + 1, CurrentPos[1] + 1))
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
        condition1 = (not (board[CurrentPos[0]
                                 + pos_neg(coord1)][CurrentPos[1]
                                                    + pos_neg(coord2)][0] in
                           [' ', ('b' if 'w_' in piece else 'w')]) and
                      no_knight)
        # checks if spot is empty
        condition2 = (not (board[CurrentPos[0]
                                 + coord1][CurrentPos[1]
                                           + coord2][0] in
                           [' ', 'b' if 'w_' in piece else 'w']))
        # checks if the total of both is < 0, or checks that it cant hit forward for a pawn
        condition3_1 = (CurrentPos[0] + coord1 < 0) or (CurrentPos[1] + coord2 < 0)
        pawn = 'pawn' in piece
        condition3_2 = not (
            pawn and coord2 == 0 and board[CurrentPos[0] + coord1]
            [CurrentPos[1] + coord2][0] in ('b' if 'w_' in piece else 'w'))
        condition3 = condition3_1 and condition3_2
        try:
            if condition1 or condition2 or condition3:
                continue

            if 'knight' not in piece:
                # checks if the spots till the desired pos are all empty... (extension of the first check)
                if any([True
                        for a in range(min(CurrentPos[0] + coord1,
                                           CurrentPos[0])
                                               + (0 if coord1 == 0 else 1),
                                       max(CurrentPos[0] + coord1,
                                           CurrentPos[0])
                                               + (1 if coord1 == 0 else 0))
                        for b in range(min(CurrentPos[1] + coord2,
                                           CurrentPos[1])
                                               + (0 if coord2 == 0 else 1),
                                       max(CurrentPos[1] + coord2,
                                           CurrentPos[1]) + (
                                               1 if coord2 == 0 else 0))
                        if not (Board[a][b] in [' ', ('b' if 'w_' in piece
                                                      else 'w')]) and (
                        not ('bishop' in piece) or (CurrentPos[0] + a) *
                                (CurrentPos[0] + a) == (CurrentPos[1] + b) * (
                        CurrentPos[1] + b))]):
                    ##                    print("Oh hi there, didn't see you!")
                    continue

            to_return.append((CurrentPos[0] + coord1, CurrentPos[1] + coord2))

            to_return.append((CurrentPos[0] + coord1, CurrentPos[1] + coord2))
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
    team = 'b_' if team == 'white' else 'w_'
    opponent = team_to_opponent(team)
    king_pos_team = get_king(board, team)
    king_pos_opponent = get_king(board, opponent)

    # kill the enemy king
    if check_pos(board, king_pos_opponent, team, king=True):
        return check_pos(board, king_pos_opponent, team, king=True)[0]

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

                if check_pos(board, attack, opponent):
                    # the attacker is defended by another piece
                    if move_king(board, team, king_pos_team):
                        # try to move the king if you can
                        return move_king(board, team, king_pos_team)
                    else:
                        # todo calculate which piece is best to lose
                        pass
                else:
                    return random.choice(defenders)
            else:
                return move_king(board, team, king_pos_team)
        else:
            if move_king(board, team, king_pos_team):
                # try to move the king if you can
                return move_king(board, team, king_pos_team)
            