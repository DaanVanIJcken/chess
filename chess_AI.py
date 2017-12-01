#!/usr/bin/env python

import random


def pos_neg(x: float): # or int
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def possible_moves(current_pos: tuple, board: list) -> list:
    if board[current_pos[0]][current_pos[1]] == ' ':
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


def get_piece(board: list, team: str, piece: str) -> tuple:
    for i, line in enumerate(board):
        for j, piece in enumerate(line):
            if piece != ' ':
                if piece[:2] == 'w_' if team == 'w_' else piece[:2] == 'b':
                    if piece[2:] == piece:
                        piece_pos = (i, j)
                        return piece_pos
    else: 
        return ()


def check_pos(board: list, pos: tuple, team: str, king: bool = False) -> list:
    # can team kill what is on pos
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


def team_to_opponent(team: str) -> str:
    return 'b_' if team == 'w_' else 'w_'


def move_piece(board: list, team, piece_pos: tuple) -> dict:
    opponent = team_to_opponent(team)
    for move in possible_moves(piece_pos, board):
        fake_board = eval(str(board))
        fake_board[move["from"][0]][move["from"][1]] = ' '
        fake_board[move["to"][0]][move["to"][1]] = \
            board[piece_pos[0]][piece_pos[1]]
        if not check_pos(fake_board, move[ "to"], opponent):
            return {"from": piece_pos, "to": move}
    return {}


def worse(self: str, other: str):
    values = {'pawn': 1, "knight": 2, "bishop": 3,"rook": 4, "queen":5,
              "king": 6}
    if values[self] < values[other]:
        return True
    else:
        return False


def calculate_path(board: list, from_: tuple, to: tuple) -> list[tuple]:
    piece = board[from_[0]][from_[1]]
    if from_[0] == to[0]:  # horizontal movement
        if from_[1] < to[1]:
            return [(from_[0] + movement, from_[1])
                    for movement in range(to[0] - from_[0])]
        else:
            return [(from_[0] + movement, from_[1])
                    for movement in range(0, to[0] - from_[0], -1)]
    elif from_[1] == to[1]:  # vertical movement
        if to[1] > from_[1]:
            return [(from_[0], from_[1] + movement)
                     for movement in range(to[1] - from_[1])]
        else:
            return [(from_[0], from_[1] + movement)
                     for movement in range(0, to[1] - from_[1], -1)]
    elif abs(to[0] - from_[0]) == abs(to[1] - from_[1]):  # diagonal movement
        if to[0] > from_[0] and to[1] > from_[1]:
            return [(from_[0] + movement, from_[1] + movement)
                    for movement in range(abs(to[0]-from_[0]))]
        if to[0] > from_[0] and to[1] < from_[1]:
            return [(from_[0] + movement, from_[1] - movement)
                    for movement in range(abs(to[0]-from_[0]))]
        if to[0] < from_[0] and to[1] > from_[1]:
            return [(from_[0] - movement, from_[1] + movement)
                    for movement in range(abs(to[0]-from_[0]))]
        else:  # to[0] < from_[0] and to[1] < from_[1]:
            return [(from_[0] - movement, from_[1] - movement)
                    for movement in range(abs(to[0]-from_[0]))]
    else:
        return []


def protect_piece(board: list, team: str, piece: str) -> dict:
    team = 'b_' if team == 'black' else 'w_'
    opponent = team_to_opponent(team)
    piece_pos_team = get_piece(board, team, piece)
    piece_pos_opponent = get_piece(board, opponent, piece)

    # kill the enemy piece
    if check_pos(board, piece_pos_opponent, team, king=True):
        return check_pos(board, piece_pos_opponent, team, king=True)[0]

    # defend my own piece
    if check_pos(board, piece_pos_team, opponent):
        # can my piece be killed next turn
        if len(check_pos(board, piece_pos_team, opponent)) == 1:
            # my king can only be killed one way.
            attack = check_pos(board, piece_pos_team, opponent)[0]["from"]
            # from what position can my piece be killed
            if check_pos(board, attack, team):
                # I can kill whatever is check'ing my king

                # find which pieces can kill the attacker
                # without opening the piece to a new attack
                defenders = []
                for defender in check_pos(board, attack, team):
                    coord1 = defender['from'][0]
                    coord2 = defender['from'][1]
                    if piece != 'king':
                        # possible moves does not check if this move is clever
                        # so I have to check it for myself
                        fake_board = eval(str(board))
                        fake_board[coord1][coord2] = ' '
                        fake_board[attack[0]][attack[1]] = ' '
                        if check_pos(board, piece_pos_team, opponent):
                            defenders.append((coord1, coord2))
                        del fake_board
                    else:
                        # this is the king. possible moves already stops me
                        # from making stupid moves that cause
                        # the king to be killable
                        defenders.append((coord1, coord2))# clean up
                    del coord1, coord2

                if len(defenders) > 0:
                    if check_pos(board, attack, opponent):
                        # the attacker is defended by another piece
                        if  move_piece(board, team, piece_pos_team):
                            # try to move the king if you can
                            return move_piece(board, team, piece_pos_team)
                        else:
                            defenders = [{'name': board[defender[0]][defender[0]][2:],
                                          'coords': defender}
                                         for defender in defenders]
                            # find the least important piece

                            for defender in defenders:
                                try:
                                    if worse(defender['name'], worst["name"]):
                                        worst = defender
                                except NameError:
                                    worst = defender
                            return {"from": worst['coords'], "to": attack}
                    else:
                        # it doesn't matter what piece is used to kill the attacker
                        return random.choice(defenders)
        else:
            piece_movement = move_piece(board, team, piece_pos_team)
            if piece_movement:
                # move the piece if you can
                return piece_movement
            else:
                del piece_movement  # clean up
                attackers = check_pos(board, piece_pos_team, opponent)
                attackers_names = [board[attacker[0]][attacker[0]][2:]
                                   for attacker in attackers]
                if 'knight' in attackers_names:
                    return {}  # the knight will kill me anyway
                paths = [set([calculate_path(board, attacker["from"], piece_pos_team)])
                         for attacker in attackers]
                # calculate all paths used by all attackers
                commons = paths[0]

                for path in paths:
                    commons = commons & path
                    # calculate which square
                    # is used by all attackers
                if len(commons) == 0:
                    return {}  # it is impossible to block all
                    # because they use different routes
                else:
                    defenders = []
                    for point in commons:
                        for defender in check_pos(board, point, team):
                            if check_pos(board, piece_pos_team, opponent):
                                defenders.append({"from": defender["from"],
                                                  "to": point})
                    if len(defenders) > 0:
                        return random.choice(defenders)
                    else:
                        del defenders
                        
                        
def think(board: list, team: str) -> dict:
    king = protect_piece(board, team, 'king')
    if king:
        return king
    del king
    queen = protect_piece(board, team, 'queen')
    if queen:
        return queen
    del queen
