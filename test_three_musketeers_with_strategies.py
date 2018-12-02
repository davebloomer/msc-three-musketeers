import pytest
from three_musketeers import *
from three_musketeers_with_strategies import *

left = 'left'
right = 'right'
up = 'up'
down = 'down'
M = 'M'
R = 'R'
_ = '-'

board1 =  [ [_, _, _, M, _],
            [_, _, R, M, _],
            [_, R, M, R, _],
            [_, R, _, _, _],
            [_, _, _, R, _] ]

boardx =  [ [M, _, _, _, M],
            [_, _, R, _, _],
            [_, R, _, R, _],
            [_, R, _, _, _],
            [M, _, _, R, _] ] # board with no valid move for musketeer

boardw =  [ [_, _, _, M, _],
            [_, _, R, M, _],
            [_, R, _, M, _],
            [_, R, _, _, _],
            [_, _, _, R, R] ] # board that meets enemy winning condition

def test_adjacent_location_for_list():
    assert type(adjacent_location_for_list([((0, 0), 'right')])) == list
    assert adjacent_location_for_list([((0, 0), 'right')]) == [(0, 1)]
    assert adjacent_location_for_list([((0, 0), 'right'), ((4, 4), 'up')]) == [(0, 1), (3, 4)]
    set_board(board1)
    assert adjacent_location_for_list(all_possible_moves_for('M')) == [(1, 2), (2, 3), (2, 1), (2, 3), (1, 2)]
    set_board(boardw)
    assert adjacent_location_for_list(all_possible_moves_for('M')) == [(1, 2)]

def test_player_locations():
    create_board()
    assert type(player_locations('M')) == list
    assert player_locations('M') == [(0, 4), (2, 2), (4, 0)]
    set_board(board1)
    assert player_locations('M') == [(0, 3), (1, 3), (2, 2)]
    set_board(boardw)
    assert player_locations('M') == [(0, 3), (1, 3), (2, 3)]
    assert player_locations('R') == [(1, 2), (2, 1), (3, 1), (4, 3), (4, 4)]

def test_all_possible_moves_for():
    set_board(boardw)
    direction = ('left', 'down', 'up', 'right')
    assert type(all_possible_moves_for('M')) == list
    assert all_possible_moves_for('M') == [((1, 3), 'left')]
    assert all_possible_moves_for('R') == [((1, 2), 'left'), ((1, 2), 'down'), ((1, 2), 'up'),  ((2, 1), 'left'),
                                     ((2, 1), 'up'), ((2, 1), 'right'), ((3, 1), 'left'), ((3, 1), 'down'),
                                     ((3, 1), 'right'), ((4, 3), 'left'), ((4, 3), 'up'), ((4, 4), 'up')]
    
def test_choose_musketeer_move():
    set_board(board1)
    direction = ('left', 'down', 'up', 'right')  
    assert type(choose_musketeer_move()) == tuple

def test_chooseenemy_move():
    set_board(board1)
    direction = ('left', 'down', 'up', 'right')  
    assert type(choose_enemy_move()) == tuple