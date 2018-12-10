# Improving Computer AI

# Ideas from Birkbeck:
# The three Musketeers should try to stay as far away from one another as possible.  
# Cardinal Richelieu's men should try to all move in the same direction.

# DB Ideas:

# - Input to select difficulty (M/H)
# -- M: Computer maximises game length (E - follows M, M - avoid common rows/columns)
# -- H: Computer uses consistent tactics (E - direction, M - maximise distance)

# When computer = 'R':
# - Extend game by working out next possible 'M' moves and matching
# - Current moves are prioritised on the basis:
#    direction = ('left', 'right', 'up', 'down')
# -- Prioritise 'R' movement to the topleft, bottomleft etc.

# When computer = 'M':
# - Prioritise 'M' movement which will not put 'M' in same column / row
# - Calculate proxy for Euclidean distance (d-row*d-column) choose move which
#    maximises distance

# Changes will be required to game code following implementation..

#%% Code from base implementation - required to be included for pytest

def create_board():
    global board
    """Creates the initial Three Musketeers board and makes it globally
       available (That is, it doesn't have to be passed around as a
       parameter.) 'M' represents a Musketeer, 'R' represents one of
       Cardinal Richleau's men, and '-' denotes an empty space."""
    m = 'M'
    r = 'R'
    board = [ [r, r, r, r, m],
              [r, r, r, r, r],
              [r, r, m, r, r],
              [r, r, r, r, r],
              [m, r, r, r, r] ]

def set_board(new_board):
    """Replaces the global board with new_board."""
    global board
    board = new_board

def get_board():
    """Just returns the board. Possibly useful for unit tests."""
    return board

def string_to_location(s):
    """Given a two-character string (such as 'A5'), returns the designated
    location as a 2-tuple (such as (0, 4)).
    The function should raise ValueError exception if the input
    is outside of the correct range (between 'A' and 'E' for s[0] and
    between '1' and '5' for s[1]"""
    if ord(s[0]) < 65 or ord(s[0]) > 69:  # Takes first character of input and converts to unicode, throws exception if not within range A-E
        raise ValueError('Row is out of bounds.')
    if ord(s[1]) < 49 or ord(s[1]) > 53:  # Takes second character of input and converts to unicode, throws exception if not within range 1-5
        raise ValueError('Column is out of bounds.')
    return (ord(s[0])-65, ord(s[1])-49)  # If input within valid range, uses offset of unicode value to convert to range 0-4

def location_to_string(location):
    """Returns the string representation of a location.
    Similarly to the previous function, this function should raise
    ValueError exception if the input is outside of the correct range
    """
    if location[0] < 0 or location[0] > 4:  # Takes first character of input, throws exception if not within range 0-4
        raise ValueError('Row is out of bounds.')
    if location[1] < 0 or location[1] > 4:  # Takes second character of input, throws exception if not within range 0-4
        raise ValueError('Column is out of bounds.')
    return chr(location[0]+65) + chr(location[1]+49)  # If input within valid range, uses offset of unicode value to convert to range A-E and 1-5 respectively

def at(location):
    """Returns the contents of the board at the given location.
    You can assume that input will always be in correct range."""
    return board[location[0]][location[1]]  # Maps input location to board matrix based on hyperparameter location in (row, column) format

def all_locations():
    """Returns a list of all 25 locations on the board."""
    return [i for j in board for i in j]  # List comprehension to remove matrix organisational structure from global variable board
    
def adjacent_location(location, direction):
    """Return the location next to the given one, in the given direction.
    Does not check if the location returned is legal on a 5x5 board.
    You can assume that input will always be in correct range."""
    moves = {'left': (0,-1), 'right': (0,1), 'up': (-1,0), 'down': (1,0)}  # Dictionary is defined to map hyperparameter direction to mathematical operators to be combined through addition
    (row, column) = location  # Hyperparameter location split in to row and column element
    row += moves[direction][0]  # Relevant calculation performed on row and column as defined through dictionary (-/+ 1)
    column += moves[direction][1]
    return (row, column)  # Row and column recombined to form tuple

def is_legal_move_by_musketeer(location, direction):
    """Tests if the Musketeer at the location can move in the direction.
    You can assume that input will always be in correct range. Raises
    ValueError exception if at(location) is not 'M'"""
    if at(location) != 'M' or at(adjacent_location(location, direction)) != 'R':  # Logic checks character at hyperparameter location is musketeer and enemy present in hyperparameter direction
        raise ValueError('Move Not Valid.')  # If either logic statements is false, an exception is thrown
    else:
        return True  # Otherwise, the move is valid

def is_legal_move_by_enemy(location, direction):
    """Tests if the enemy at the location can move in the direction.
    You can assume that input will always be in correct range. Raises
    ValueError exception if at(location) is not 'R'"""
    if at(location) != 'R' or at(adjacent_location(location, direction)) != '-':  # Logic checks character at hyperparameter location is enemy and empty space present in hyperparameter direction
        raise ValueError('Move Not Valid.')  # If either logic statements is false, an exception is thrown
    else:
        return True  # Otherwise, the move is valid

def is_legal_location(location):
    """Tests if the location is legal on a 5x5 board.
    You can assume that input will always be a pair of integers."""
    if 0 <= location[0] <= 4 and 0 <= location[1] <= 4:  # Compares if each position in hyperparamter location within legal range 0-4
        return True  # Return True if logic met
    else:
        return False
    
def is_within_board(location, direction):
    """Tests if the move stays within the boundaries of the board.
    You can assume that input will always be in correct range."""
    # Uses function adjacent_location to find resulting position of move, then function is_legal_location to check if valid and determine output
    return is_legal_location(adjacent_location(location, direction))

def can_move_piece_at(location, direction=('left', 'right', 'up', 'down')):
    # Included direction as hyperparameter to avoid redundancy in function is_legal_move, by default contains all legal (perpendicular) move directions
    """Tests whether the player at the location has at least one move available.
    You can assume that input will always be in correct range."""
    if at(location) == 'M':  # Uses at funon to determine player at hyperparameter location, if musketeer:
        for dir in direction:  # Itererate through each element in hyperparameter direction
            if is_within_board(location, dir) == True and at(adjacent_location(location, dir)) == 'R':  # If location in direction contains enemy and is valid location       
                return True  # Return True and break
                break
        return False  # Return False if logic not met for all directions considered
    elif at(location) == 'R':  # Alternate scenario, if player at hyperparameter location is enemy:
        for dir in direction:
            if is_within_board(location, dir) == True and at(adjacent_location(location, dir)) == '-':  # If location in direction contains empty space and is valid location
                return True  # Return True and break
                break
        return False  # Return False if logic not met for all directions considered
    else:  # Else condition, if no valid moves are present for player at location, return False
        return False
    
def is_legal_move(location, direction):
    """Tests whether it is legal to move the piece at the location
    in the given direction.
    You can assume that input will always be in correct range."""
    # Uses function adjacent_location to find resulting position of move, then function can_move_piece_at to check if valid and determine output
    return can_move_piece_at(location, [direction])

def has_some_legal_move_somewhere(who):
    """Tests whether a legal move exists for player "who" (which must
    be either 'M' or 'R'). Does not provide any information on where
    the legal move is.
    You can assume that input will always be in correct range."""
    # Performs count on putputs from function all_possible_moves_for, if number of valid moves is greater than zero return True
    if len(all_possible_moves_for(who)) > 0:
        return True
    else:
        return False

def make_move(location, direction):
    """Moves the piece in location in the indicated direction.
    Doesn't check if the move is legal. You can assume that input will always
    be in correct range."""
    l1 = location  # Starting position for move
    l2 = adjacent_location(location, direction)  # Ending position for move, determined using function adjacent_location
    board[l1[0]][l1[1]], board[l2[0]][l2[1]] = '-', board[l1[0]][l1[1]]  # Contents of board are copied from starting to ending location, and replaced with empty space (-)

def choose_computer_move(who):
    """The computer chooses a move for a Musketeer (who = 'M') or an
    enemy (who = 'R') and returns it as the tuple (location, direction),
    where a location is a (row, column) tuple as usual.
    You can assume that input will always be in correct range."""
    from random import choice  # Import choice from library random, chooses random element from a non-empty sequence
    if has_some_legal_move_somewhere(who) == False:  # Logic checks if any moves are possible for hyperparameter who using function has_some_legal_move_somewhere
        raise ValueError('No moves possible.')  # If False, an exception is thrown
    else:    
        return choice(all_possible_moves_for(who))  # Returns random element of output of function all_possible_moves_for for hyperparameter who (computer)

def is_enemy_win():
    """Returns True if all 3 Musketeers are in the same row or column."""
    for i in range (0,5):  # i iteration represents that one row and one column will be inspected each loop
        row = 0  # Initialises variable, to contain all occurances of musketeers in each row and column inspected
        col = 0  # Variables are reset each i iternation, as no of occurances must be contained within a given row or column
        for j in range (0,5):  # j iteration represents elements within each row and column specified in i iteration
            if board[i][j] == 'M':  # In first logic, i remains constant in index position one, representing row i
                row += 1  # Iterating through j element positions, one is increased to count if musketeer is present
            if board[j][i] == 'M':  # In second logic, i remains constant in index position two, representing column i
                col += 1
        if row == 3 or col == 3:  # If either row or column i contain three musketeers, the enemy wins game
            return True  # Returns true and iteration breaks
            break
    return False  # If conditions not met, return False
    
#%% Additional functions
    
def computer_tactic(difficulty):
    """A games strategy will be chosen for 'R', this will vary from game to game
    to increase difficulty. The output is a tuple of possible moves which are
    prioritsed in order from left to right depending on availability."""
    select_tactic = ''
    if difficulty == 'H':
        from random import choice
        select_tactic = choice(['ugsRGv','Wq4d66','KhzYQv','Vn4SHy','WuvaNj','gHwrEP','WfGHet','W8vzXJ'])
    global tactic
    tactic = (difficulty, select_tactic)
    #return (difficulty, tactic_lookup[tactic[1]])

# Not required? Tactic variable is local within start()
def tactic_lookup(tactic):
    """In order not to have enemy tactic visable as global variable, a dictionary
    is defined to anonamise the tactic to the player."""
    tactic_lookup = {
            'ugsRGv': ('left', 'up', 'down', 'right'),
            'Wq4d66': ('left', 'down', 'up', 'right'),
            'KhzYQv': ('right', 'up', 'down', 'left'),
            'Vn4SHy': ('right', 'down', 'up', 'left'),
            'WuvaNj': ('up', 'left', 'right', 'down'),
            'gHwrEP': ('up', 'right', 'left', 'down'),
            'WfGHet': ('down', 'left', 'right', 'up'),
            'W8vzXJ': ('down', 'right', 'left', 'up') }
    return tactic_lookup[tactic[1]]

def set_tactic(difficulty, new_tactic):
    """Replaces the global tactic with new_tactic."""
    global tactic
    tactic = (difficulty, new_tactic)

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

        #or..
        #def adjacent_location(location, direction):
        #moves = {'left': (0,-1), 'right': (0,1), 'up': (-1,0), 'down': (1,0)}
        #return tuple(x+y for x, y in zip(location, moves[direction]))"""

def player_locations(player):
    """Returns all locations for the player in a list of tuples.
    Previously part of all_possible_moves_for(), but useful input for relative
    distance calculations."""
    return [(i, j) for i in range(0,5) for j in range(0,5) if board[i][j] == player]

def possible_moves_from(location):
    moves = []
    direction = ('left', 'up', 'down', 'right') #tactic[1]
    if at(location) == 'M':
        for dir in direction:
            if is_within_board(location, dir) == True and at(adjacent_location(location, dir)) == 'R':
                moves.append(dir)
    elif at(location) == 'R':
        for dir in direction:
            if is_within_board(location, dir) == True and at(adjacent_location(location, dir)) == '-':
                moves.append(dir)
    return moves

def possible_moves_from_for_list(locations):
    moves = []
    direction = ('left', 'up', 'down', 'right') #tactic[1]
    for loc in locations:
        if at(loc) == 'M':
            for dir in direction:
                if is_within_board(loc, dir) == True: # and at(adjacent_location(loc, dir)) == 'R':
                    moves.append((loc, dir))
        elif at(loc) == 'R':
            for dir in direction:
                if is_within_board(loc, dir) == True: # and at(adjacent_location(loc, dir)) == '-':
                    moves.append((loc, dir))
    return moves

def all_possible_moves_for(player):
    """Returns every possible move for the player ('M' or 'R') as a list
    (location, direction) tuples.
    You can assume that input will always be in correct range."""
    player_loc = player_locations(player)
    moves = []
    for loc in player_loc:
        for dir in possible_moves_from(loc):
            moves.append((loc, dir))
    return moves

def choose_musketeer_move():
    """Based on all possible moves for 'M', chooses move that maximises proxy
    for distance to other 'M' on board.
    Returns a tuple (location, direction), where location is a (row, column) tuple."""
    if tactic[0] == 'E':
        from random import choice
        return choice(all_possible_moves_for('M'))
    elif tactic[0] == 'M':
        return ((0,0), 'right')
    else:
        return ((0,0), 'right')

def choose_enemy_move():
    """Based on all possible moves for 'R', priotise moves that move in common
    direction, then moves that extend the game by creating possible moves for 'M'.
    Returns a tuple (location, direction), where location is a (row, column) tuple."""
    if tactic[0] == 'E':
        from random import choice
        return choice(all_possible_moves_for('R'))
    elif tactic[0] == 'M':
        m_moves = adjacent_location_for_list(possible_moves_from_for_list(player_locations('M')))
        e_moves = adjacent_location_for_list(all_possible_moves_for('R'))
        #return choice[m for m in m_moves for e in e_moves if m==e]  # Missing direction
        return ((0,0), 'right')
    else:
        return ((0,0), 'right')

#%% User communication update

#---------- Communicating with the user ----------
#----you do not need to modify code below unless you find a bug
#----a bug in it before you move to stage 3

def choose_difficulty():
    """Returns 'E' or 'H' if user has selected easy or hard difficulty."""
    difficulty = ""
    while difficulty != 'E' and difficulty != 'H':
        answer = input("Select computer difficulty level. Easy (E) or Hard (H)? ")
        answer = answer.strip()
        if answer != "":
            difficulty = answer.upper()[0]
    return difficulty

def move_musketeer(users_side):
    """Gets the Musketeer's move (from either the user or the computer)
       and makes it."""
    if users_side == 'M':
        (location, direction) = get_users_move()
        if at(location) == 'M':
            if is_legal_move(location, direction):
                make_move(location, direction)
                describe_move("Musketeer", location, direction)
        else:
            print("You can't move there!")
            return move_musketeer(users_side)
    else: # Computer plays Musketeer
        (location, direction) = choose_computer_move('M')         
        make_move(location, direction)
        describe_move("Musketeer", location, direction)
        
def move_enemy(users_side):
    """Gets the enemy's move (from either the user or the computer)
       and makes it."""
    if users_side == 'R':
        (location, direction) = get_users_move()
        if at(location) == 'R':
            if is_legal_move(location, direction):
                make_move(location, direction)
                describe_move("Enemy", location, direction)
        else:
            print("You can't move there!")
            return move_enemy(users_side)
    else: # Computer plays enemy
        (location, direction) = choose_computer_move('R')        
        make_move(location, direction)
        describe_move("Enemy", location, direction)
        return board

def start():
    """Plays the Three Musketeers Game."""
    users_side = choose_users_side()
    difficulty = choose_difficulty()
    board = create_board()
    print_instructions()
    print_board()
    while True:
        if has_some_legal_move_somewhere('M'):
            board = move_musketeer(users_side)
            print_board()
            if is_enemy_win():
                print("Cardinal Richleau's men win!")
                break
        else:
            print("The Musketeers win!")
            break
        if has_some_legal_move_somewhere('R'):
            board = move_enemy(users_side)
            print_board()
        else:
            print("The Musketeers win!")
            break