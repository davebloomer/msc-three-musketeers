# Improving Computer AI

# Ideas from Birkbeck:
# The three Musketeers should try to stay as far away from one another as possible.  
# Cardinal Richelieu's men should try to all move in the same direction.

# DB Ideas:
# -- Input to select difficulty (easy/medium/hard)
# On basis of some/all ideas below
# 
# For 'R':
# -- Current moves are prioritised on the basis:
#  direction = ('left', 'right', 'up', 'down')
# Could vary to prioritise 'R' movement to the topleft, bottomleft etc.
# -- Extend game by working out next possible 'M' moves and matching
#
# For 'M'
# -- Give lower priority to moves which will put 'M' in same column / row
# -- or Calculate proxy for Euclidean distance (drow*dcolumn) choose move which
#  maximises distance

# Changes will be required to game code following implementation..

def adjacent_location_for_list(moves):
    """Calculates location next to given one, in the given direction, for use
    on a list. Functionality similar to adjacent_location(), to be used with
    output from all_possible_moves_for(). 
    Does not check if the location returned is legal on a 5x5 board.
    You can assume that input will always be in correct range."""    
    move_dest = []
    for i in moves:
        (location, direction) = i
        move_dest.append(adjacent_location(location, direction))
    return move_dest

def player_locations(player):
    """Returns all locations for the player in a list of tuples.
    Previously part of all_possible_moves_for(), but useful input for relative
    distance calculations."""
    player_loc = []
    for i in range (0,5):
        for j in range (0,5):
            if board[i][j] == player:
                player_loc.append((i,j))
    return player_loc

def create_enemy_tactic():
    """A games strategy will be chosen for 'R', this will vary from game to game
    to increase difficulty. The output is a tuple of possible moves which are
    prioritsed in order from left to right depending on availability."""
    from random import choice
    possible_tactics = [('left', 'up', 'down', 'right'),
    ('left', 'down', 'up', 'right'),
    ('right', 'up', 'down', 'left'),
    ('right', 'down', 'up', 'left'),
    ('up', 'left', 'right', 'down'),
    ('up', 'right', 'left', 'down'),
    ('down', 'left', 'left', 'up'),
    ('down', 'left', 'left', 'up')]
    global direction
    direction = choice(possible_tactics)

def all_possible_moves_for(player):
    """Returns every possible move for the player ('M' or 'R') as a list
    (location, direction) tuples.
    You can assume that input will always be in correct range."""
    player_loc = player_locations(player)
    moves = []
    for loc in player_loc:
        if player == 'M':
            for dir in direction:  # direction defined in create_enemy_tactic()
                if is_within_board(loc, dir) == True and at(adjacent_location(loc, dir)) == 'R':
                    moves.append((loc, dir))
        elif player == 'R':
            for dir in direction:
                if is_within_board(loc, dir) == True and at(adjacent_location(loc, dir)) == '-':
                     moves.append((loc, dir))
    return moves

def choose_musketeer_move():
    """Based on all possible moves for 'M', chooses move that maximises proxy
    for distance to other 'M' on board.
    Returns a tuple (location, direction), where location is a (row, column) tuple."""
    return ((0,0))

def choose_enemy_move():
    """Based on all possible moves for 'R', priotise moves that move in common
    direction, then moves that extend the game by creating possible moves for 'M'.
    Returns a tuple (location, direction), where location is a (row, column) tuple."""
    m_moves = possible_moves_from(player_locations('M'))
    e_moves = all_possible_moves_for('R')
    return ((0,0))