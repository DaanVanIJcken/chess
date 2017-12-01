#!/usr/bin/env python

import random


def pos_neg(integer):
    # returns 0 when giving 0, -1 for every value < 0 and 1 for every value > 0
    return [[1, -1][integer < 0], 0][integer == 0]


def simulate_board(start: tuple, end: tuple, board: list):
    fake_board = eval(str(board))
    fake_board[end[0]][end[1]] = fake_board[start[0]][start[1]]
    fake_board[start[0]][start[1]] = ' '
    return fake_board


def check_check(board: list, colour: str, fast_check: bool = False) -> str:
    # watch out w/ globals (function calls itself)
    pieces_opponent = [(col, row) for row in range(len(board[0])) for col in range(len(board))
                       if board[col][row][0] == ('w' if colour[0] == 'b' else 'b')]
    pieces_friendly = [(col, row) for row in range(len(board[0])) for col in range(len(board))
                       if board[col][row][0] == ('b' if colour[0] == 'b' else 'w') and 'king' not in board[col][row]]
    try:
        coord_king = [(col, row) for row in range(len(board[0])) for col in range(len(board))
                      if board[col][row] == ('b' if colour[0] == 'b' else 'w') + '_king'][0]
    except IndexError:
        return ''

    for coord in pieces_opponent:
        if coord_king in possible_moves(coord, board, True):  # a piece can attack the king  |  keep the True here
            if fast_check:
                return 'check'
            if len(possible_moves(coord_king, board)) == 0:  # the king cant move, but there are 2 ways out:
                for coord2 in pieces_friendly:
                    if coord in possible_moves(coord2, board):  # a piece can kill the attacker
                        return 'check'
                    for coord3 in possible_moves(coord2, board):  # a piece can block the line
                        sim_board = simulate_board((coord2[0], coord2[1]), (coord3[0], coord3[1]), board)
                        if check_check(sim_board, colour, True) == '':  # keep the True here
                            return 'check'
                return 'checkmate'
            return 'check'
    return ''


def possible_moves(current_pos: tuple, board: list, fast_king: bool = False) -> list:
    """"if fast_king is True, the function will not check for the next king to
see if he can move and will auto-assume he is a piece that can be lost wo/ consequence"""
    # watch out w/ globals (function calls itself)
    try:
        if board[current_pos[0]][current_pos[1]] == ' ':
            return []
    except IndexError:
        current_pos = list(current_pos)
        current_pos[0], current_pos[1] = list(range(8))[current_pos[0] % 8], list(range(8))[current_pos[1] % 8]
    pos_x, pos_y = current_pos[0], current_pos[1]
    piece, to_return = board[pos_x][pos_y], []

    if 'pawn' in piece:
        if 'w_' in piece:
            returnable = [(-1, 0), (-2, 0)] if pos_x == 6 and board[5][pos_y] == ' ' else [(-1, 0)]
            if board[pos_x - 1][pos_y - 1][0] == 'b' and pos_x > 0 and pos_y > 0:
                to_return.append((pos_x - 1, pos_y - 1))
            if pos_y < 7 and pos_x > 0 and board[pos_x - 1][pos_y + 1][0] == 'b':
                to_return.append((pos_x - 1, pos_y + 1))
        else:
            returnable = [(1, 0), (2, 0)] if pos_x == 1 and board[2][pos_y] == ' ' else [(1, 0)]
            if 7 > pos_y > 0 and board[pos_x + 1][pos_y - 1][0] == 'w':
                to_return.append((pos_x + 1, pos_y - 1))
            if pos_y < 7 > pos_x and board[pos_x + 1][pos_y + 1][0] == 'w':
                to_return.append((pos_x + 1, pos_y + 1))
    elif 'knight' in piece:
        returnable = [(-2, -1), (-1, -2), (+1, -2), (+2, -1), (-2, +1), (+2, +1), (-1, +2), (+1, +2)]
    elif 'rook' in piece:
        returnable = [(i1, i2) for i1 in range(-7, 8) for i2 in range(-7, 8) if (i1 == 0 or i2 == 0)]
    elif 'bishop' in piece:
        returnable = [(i1, i2) for i1 in range(-7, 8) for i2 in range(-7, 8) if i1 * i1 == i2 * i2]
    elif 'queen' in piece:
        returnable = [(i1, i2) for i1 in range(-7, 8) for i2 in range(-7, 8)
                      if (i1 * i1 == i2 * i2 or (i1 == 0 or i2 == 0))]
    else:  # if 'king' in piece:
        returnable = [(i1, i2) for i1 in range(-1, 2) for i2 in range(-1, 2)]

    for (coord1, coord2) in returnable:  # valid move check
        if ((((pos_x + coord1 < 0) or (pos_y + coord2 < 0) or
                  (pos_x + coord1 > 7) or (pos_y + coord2 > 7)) or
                 (coord1 == coord2 == 0)) or (
                # checks if the total of both is < 0 or > 8 or both are equal to 0

                not (board[pos_x + pos_neg(coord1)][pos_y + pos_neg(
                    coord2)][0] in [' ', ('b' if 'w_' in piece else 'w')]) and
                         'knight' not in piece) or (
                # looks if the first spot in this row is empty (if it's not a knight)

                not (board[pos_x + coord1][pos_y + coord2][0] in [' ', ('b' if 'w_' in piece else 'w')])) or (
                # checks if spot you're moving to is empty

                ('pawn' in piece and coord2 == 0
                 and board[pos_x + coord1][pos_y + coord2][0] in ('b' if 'w_' in piece else 'w')))):
            # checks that it cant hit forward for a pawn
            continue

        if piece[2:] not in ['knight', 'king', 'pawn']:
            # extra check for non-kings, knights, pawns (extension of the 2nd check) ->
            # checks if the spots till the desired pos are all empty...
            if 'w_' in piece and not fast_king:
                '''if you want to you can test the list comprehension that's up w/ these loops,
                this whole thing seems to work some way or another'''
                print('-=-=-\n', pos_x + coord1, pos_y + coord2)
                for a in range(
                                min(pos_x + coord1, pos_x) + (0 if coord1 == 0 else 1),
                                max(pos_x + coord1, pos_x) + (1 if coord1 == 0 else 0)):
                    for b in range(
                                    min(pos_y + coord2, pos_y) + (0 if coord2 == 0 else 1),
                                    max(pos_y + coord2, pos_y) + (1 if coord2 == 0 else 0)):
                        print(a, b, '  -  ', board[a][b])
                print('\n')

            if any([True
                    for a in range(
                    # minimum of pos_x/new pos_x, add 1 if they're not the same else loop will fail
                            min(pos_x + coord1, pos_x) + (0 if coord1 == 0 else 1),
                    # maximum of pos_x/new pos_x, add 1 if they're the same else loop won't run
                            max(pos_x + coord1, pos_x) + (1 if coord1 == 0 else 0))
                    for b in range(
                    # minimum of pos_y/new pos_y, add 1 if they're not the same else loop will fail
                            min(pos_y + coord2, pos_y) + (0 if coord2 == 0 else 1),
                    # minimum of pos_y/new pos_y, add 1 if they're the same else loop won't run
                            max(pos_y + coord2, pos_y) + (1 if coord2 == 0 else 0))
                    if
                    (board[a][b][0] != ' '
                     # if the spot is filled with one of your own pieces
                     and (not ('bishop' in piece) or ((pos_x + a) * (pos_x + a) == (pos_y + b) * (pos_y + b)))
                     # and it's a valid coord for a bishop
                     and (not ('rook' in piece) or (pos_x == a or pos_y == b))
                     # and it's a valid coord for a rook
                     and ((not ('queen' in piece) or (
                                        ((pos_x + a) * (pos_x + a) == (pos_y + b) * (
                                                    pos_y + b)) or pos_x == a or pos_y == b)))
                     # and it's a valid coord for a queen
                     )]):
                continue  # the way to the spot is filled w/ one of your own pieces: invalid move

        if fast_king is False:
            # extra check to make sure the king is safe, only execute when fast_king is False
            '''side-note: keep fast_check to True or an infinite loop can be
                made in which each king keeps checking if he can go to a spot'''
            fake_board = simulate_board((pos_x, pos_y), (pos_x + coord1, pos_y + coord2), board)
            if check_check(fake_board, ('w' if 'w_' in piece else 'b'), True) == 'check':
                continue  # king would be under attack by opponents piece: invalid move

        to_return.append((pos_x + coord1, pos_y + coord2))
    return to_return


def get_piece(board: list, team: str, piece_: str) -> tuple:
    for i, line in enumerate(board):
        for j, piece in enumerate(line):
            if piece != ' ':
                if piece[:2] == 'w_' if team == 'w_' else piece[:2] == 'b':
                    if piece[2:] == piece_:
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


'''211277-20171201-db4c0360'''


def team_to_opponent(team: str) -> str:
    return 'b_' if team == 'w_' else 'w_'


def move_piece(board: list, team, piece_pos: tuple) -> dict:
    opponent = team_to_opponent(team)
    for move in possible_moves(piece_pos, board):
        fake_board = eval(str(board))
        fake_board[move["from"][0]][move["from"][1]] = ' '
        fake_board[move["to"][0]][move["to"][1]] = \
            board[piece_pos[0]][piece_pos[1]]
        if not check_pos(fake_board, move["to"], opponent):
            return {"from": piece_pos, "to": move}
    return {}


def worse(self: str, other: str):
    values = {'pawn': 1, "knight": 2, "bishop": 3, "rook": 4, "queen": 5,
              "king": 6}
    if values[self] < values[other]:
        return True
    else:
        return False


def calculate_path(from_: tuple, to: tuple) -> list[tuple]:
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
                    for movement in range(abs(to[0] - from_[0]))]
        if to[0] > from_[0] and to[1] < from_[1]:
            return [(from_[0] + movement, from_[1] - movement)
                    for movement in range(abs(to[0] - from_[0]))]
        if to[0] < from_[0] and to[1] > from_[1]:
            return [(from_[0] - movement, from_[1] + movement)
                    for movement in range(abs(to[0] - from_[0]))]
        else:  # to[0] < from_[0] and to[1] < from_[1]:
            return [(from_[0] - movement, from_[1] - movement)
                    for movement in range(abs(to[0] - from_[0]))]
    else:
        return []


def kill_piece(board: list, team: str, piece: str) -> dict:
    # todo write a function to kill the enemies piece (king or queen)
    pass


def protect_piece(board: list, team: str, piece: str) -> dict:
    team = 'b_' if team == 'black' else 'w_'
    opponent = team_to_opponent(team)
    piece_pos_team = get_piece(board, team, piece)

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
                        defenders.append((coord1, coord2))
                    # clean up
                    del coord1, coord2

                if len(defenders) > 0:
                    if check_pos(board, attack, opponent):
                        # the attacker is defended by another piece
                        move = move_piece(board, team, piece_pos_team)
                        if move:
                            # try to move the king if you can
                            return move
                        else:
                            del move
                            defenders = [{'name': board[defender[0]][defender[0]][2:],
                                          'coords': defender}
                                         for defender in defenders]
                            # find the least important piece
                            worst = defenders[0]
                            for defender in defenders:
                                if worse(defender['name'], worst["name"]):
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
                paths = [{calculate_path(attacker["from"], piece_pos_team)}
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
    kill_king = kill_piece(board, team, 'king')
    if kill_king:
        return kill_king
    del kill_king

    protect_king = protect_piece(board, team, 'king')
    if protect_king:
        return protect_king
    del protect_king

    kill_queen = kill_piece(board, team, 'queen')
    if kill_queen:
        return kill_queen
    del kill_queen

    protect_queen = protect_piece(board, team, 'queen')
    if protect_queen:
        return protect_queen
    del protect_queen
