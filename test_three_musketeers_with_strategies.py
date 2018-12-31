import pytest
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

boardt =  [ [R, R, R, R, M],
            [_, R, R, R, R],
            [R, _, _, R, R],
            [_, M, _, R, R],
            [_, _, M, _, R] ] # board to demonstrate various logical options

def test_computer_tactic():
    computer_tactic('E')
    assert type(tactic) == tuple
    assert tactic == ('E', '')
    computer_tactic('M')
    assert tactic == ('M', '')

def test_tactic_lookup():
    tactic = ('H', 'WfGHet')
    assert tactic_lookup() == ('down', 'left', 'right', 'up')
    tactic = ('H', 'Vn4SHy')
    assert tactic_lookup() == ('right', 'down', 'up', 'left')
    tactic = ('H', 'gHwrEP')
    assert tactic_lookup() == ('up', 'right', 'left', 'down')

def test_distance():
    assert distance((0,0), (0,2)) == 2.0
    assert distance((4,4), (0,2)) == 4.5
    assert distance((123,0), (456,1)) == 333.0
    
def test_area():
    assert area((0,0), (0,4), (4,4)) == 8.0
    assert area((0,0), (0,2), (0,1)) == 0.0
    assert area((2,1), (1,1), (4,2)) == 0.5
    assert area((123,0), (5,5), (-123,-5)) == 910.0
    
def test_player_locations():
    create_board()
    assert type(player_locations('M')) == list
    assert player_locations('M') == [(0, 4), (2, 2), (4, 0)]
    set_board(board1)
    assert player_locations('M') == [(0, 3), (1, 3), (2, 2)]
    set_board(boardw)
    assert player_locations('M') == [(0, 3), (1, 3), (2, 3)]
    assert player_locations('R') == [(1, 2), (2, 1), (3, 1), (4, 3), (4, 4)]

def test_can_move_piece_at():
    set_board(board1)
    assert type(can_move_piece_at((0,0))) == bool
    assert can_move_piece_at((0,0)) == False
    assert can_move_piece_at((1,2)) == True
    assert can_move_piece_at((1,3)) == True
    assert can_move_piece_at((0,0), legal=False) == True
    assert can_move_piece_at((1,2), legal=False) == True
    assert can_move_piece_at((1,3), legal=False) == False
    assert can_move_piece_at((1,2), direction=['left']) == True
    assert can_move_piece_at((1,2), direction=['down']) == False
    assert can_move_piece_at((1,2), direction=['left'], legal=False) == False
    assert can_move_piece_at((1,2), direction=['down'], legal=False) == True
    assert can_move_piece_at((1,3), direction=['left']) == True
    assert can_move_piece_at((1,3), direction=['up']) == False
    assert can_move_piece_at((1,3), direction=['left'], legal=False) == False
    assert can_move_piece_at((1,3), direction=['up'], legal=False) == True   

def test_possible_moves_from():
    create_board()
    assert type(possible_moves_from((0,0))) == list
    assert possible_moves_from((0,0)) == []
    assert possible_moves_from((2,2)) == ['left', 'up', 'down', 'right']
    assert possible_moves_from((0,0), legal=False) == ['down', 'right']
    assert possible_moves_from((2,2), legal=False) == []
    set_board(board1)
    assert possible_moves_from((0,0)) == []
    assert possible_moves_from((0,3)) == []
    assert possible_moves_from((1,3)) == ['left', 'down']  
    assert possible_moves_from((0,0), legal=False) == []
    assert possible_moves_from((0,3), legal=False) == ['left', 'down', 'right']
    assert possible_moves_from((1,3), legal=False) == ['left', 'down']

def test_all_possible_moves_for():
    set_board(boardw)
    assert type(all_possible_moves_for('M')) == list
    assert all_possible_moves_for('M') == [((1, 3), 'left')]
    assert all_possible_moves_for('R') == [((1, 2), 'left'), ((1, 2), 'up'), ((1, 2), 'down'),  ((2, 1), 'left'),
                                     ((2, 1), 'up'), ((2, 1), 'right'), ((3, 1), 'left'), ((3, 1), 'down'),
                                     ((3, 1), 'right'), ((4, 3), 'left'), ((4, 3), 'up'), ((4, 4), 'up')]
    assert all_possible_moves_for('M', legal=False) == [((0, 3), 'left'), ((0, 3), 'down'), ((0, 3), 'right'),
                                     ((1, 3), 'up'), ((1, 3), 'down'), ((1, 3), 'right'), ((2, 3), 'left'),
                                     ((2, 3), 'up'), ((2, 3), 'down'), ((2, 3), 'right')]
    assert all_possible_moves_for('R', legal=False) == [((1, 2), 'right'), ((2, 1), 'down'), ((3, 1), 'up'),
                                     ((4, 3), 'right'), ((4, 4), 'left')]

def test_choose_musketeer_move():
    set_board(board1)
    assert type(choose_musketeer_move(difficulty='E')) == tuple
    assert type(choose_musketeer_move(difficulty='M')) == tuple
    assert type(choose_musketeer_move(difficulty='H')) == tuple
    assert choose_musketeer_move(difficulty='H') == ((2,2), 'left')
    set_board(boardt)    
    assert choose_musketeer_move(difficulty='H') == ((0,4), 'left')
    
def test_choose_enemy_move():
    set_board(boardt)
    assert type(choose_enemy_move(difficulty='E')) == tuple
    assert type(choose_enemy_move(difficulty='M')) == tuple
    assert type(choose_enemy_move(difficulty='H')) == tuple