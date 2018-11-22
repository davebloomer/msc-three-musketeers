import pytest
from three_musketeers import *

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
            [M, _, _, R, _] ] # board with no valid move

boardw =  [ [_, _, _, M, _],
            [_, _, R, M, _],
            [_, R, _, M, _],
            [_, R, _, _, _],
            [_, _, _, R, _] ] # board that meets winning condition

def test_create_board():
    create_board()
    assert at((0,0)) == R
    assert at((0,4)) == M
    assert at((4,4)) == R
    assert at((4,0)) == M

def test_set_board():
    set_board(board1)
    assert at((0,0)) == _
    assert at((1,2)) == R
    assert at((1,3)) == M
    set_board(boardx)
    assert at((0,0)) == M
    assert at((2,3)) == R
    assert at((2,4)) == _
    set_board(boardw)
    assert at((1,2)) == R
    assert at((1,3)) == M
    assert at((1,4)) == _
    
def test_get_board():
    set_board(board1)
    assert board1 == get_board()
    set_board(boardx)
    assert boardx == get_board()
    set_board(boardw)
    assert boardw == get_board()

def test_string_to_location():
    assert type(string_to_location('A1')) == tuple
    with pytest.raises(ValueError):
        string_to_location('X3')
        string_to_location('B7')
    assert string_to_location('A1') == (0,0)
    assert string_to_location('D4') == (3,3)
    assert string_to_location('E2') == (4,1)

def test_location_to_string():
    assert type(location_to_string((0,0))) == str
    with pytest.raises(ValueError):
        location_to_string((0,5))
        location_to_string((-1,2))
    assert location_to_string((0,0)) == 'A1'
    assert location_to_string((3,3)) == 'D4'
    assert location_to_string((4,1)) == 'E2'
        
def test_at():
    assert type(location_to_string((0,0))) == str

def test_all_locations():
    assert type(all_locations()) == str
    
def test_adjacent_location():
    assert type(adjacent_location((0,0),'left')) == tuple
    
def test_is_legal_move_by_musketeer():
    assert type(is_legal_move_by_musketeer((0,0),'left')) == bool
    
def test_is_legal_move_by_enemy():
    assert type(is_legal_move_by_enemy((0,0),'left')) == bool

def test_is_legal_move():
    assert type(is_legal_move((0,0),'left')) == bool

def test_can_move_piece_at():
    assert type(can_move_piece_at((0,0))) == bool

def test_has_some_legal_move_somewhere():
    set_board(board1)
    assert has_some_legal_move_somewhere('M') == True
    assert has_some_legal_move_somewhere('R') == True
    # Eventually put at least three additional tests here
    # with at least one additional board

def test_possible_moves_from():
    assert type(possible_moves_from((0,0))) == list

def test_is_legal_location():
    assert type(is_legal_location((0,0))) == bool

def test_is_within_board():
    assert type(is_within_board((0,0),'left')) == bool

def test_all_possible_moves_for():
    assert type(all_possible_moves_for('M')) == list
    assert type(all_possible_moves_for('M')[0]) == tuple
    
def test_make_move():
    pass

def test_choose_computer_move():
    assert type(choose_computer_move('M')) == tuple
    # Should work for both 'M' and 'R'

def test_is_enemy_win():
    assert type(is_enemy_win()) == bool