# Improving Computer AI

# FAQ
# https://moodle.bbk.ac.uk/mod/forum/discuss.php?d=104920

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

# Adv thoughts...
# - It is not R direction that is important, but forcing M to move in that direction
#   Although one might be proxy for other..
# - Could come up with implementation to play n games, compare AI and rank

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
        select_tactic = choice(['ugsRGv','Wq4d66','KhzYQv','Vn4SHy','WuvaNj','gHwrEP','WfGHet','W8vzXJ'])
    tactic = (difficulty, select_tactic)

# Not required? Tactic variable is local within start()
def tactic_lookup():
    """In order not to have enemy tactic visable as global variable, a dictionary
    is defined to anonamise the tactic to the player."""
    tactic_dict = {
            'ugsRGv': ('left', 'up', 'down', 'right'),
            'Wq4d66': ('left', 'down', 'up', 'right'),
            'KhzYQv': ('right', 'up', 'down', 'left'),
            'Vn4SHy': ('right', 'down', 'up', 'left'),
            'WuvaNj': ('up', 'left', 'right', 'down'),
            'gHwrEP': ('up', 'right', 'left', 'down'),
            'WfGHet': ('down', 'left', 'right', 'up'),
            'W8vzXJ': ('down', 'right', 'left', 'up') }
    return tactic_dict[tactic[1]]

def set_tactic(difficulty, new_tactic):
    """Replaces the tactic with new_tactic. Useful for testing."""
    tactic = (difficulty, new_tactic)
    
def distance(location1, location2):
    """Returnsthe distance between two locations on board.
    Independant of possible range of board locaitons."""
    (row1, col1) = location1
    (row2, col2) = location2
    return round(((row2-row1)**2 + (col2-col1)**2)**0.5, 1)

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

def possible_moves_from(location, legal=True):
    moves = []
    direction = ('left', 'up', 'down', 'right') #tactic[1]?  # might not be correct way to do it
    if at(location) == 'M':
        for dir in direction:
            if legal == True:
                if is_within_board(location, dir) == True and at(adjacent_location(location, dir)) == 'R':
                    moves.append(dir)
            else:
                if is_within_board(location, dir) == True and at(adjacent_location(location, dir)) == '-':
                    moves.append(dir)
    elif at(location) == 'R':
        for dir in direction:
            if legal == True:
                if is_within_board(location, dir) == True and at(adjacent_location(location, dir)) == '-':
                    moves.append(dir)
            else:
                if is_within_board(location, dir) == True and at(adjacent_location(location, dir)) != '-':
                    moves.append(dir)
    return moves

def all_possible_moves_for(player, legal=True):
    player_loc = player_locations(player)
    moves = []
    for loc in player_loc:
        for dir in possible_moves_from(loc, legal):
            moves.append((loc, dir))
    return moves

# iterator function to avoid redundancy?
def choose_musketeer_move():
    """Based on all possible moves for 'M', chooses move that maximises proxy
    for distance to other 'M' on board.
    Returns a tuple (location, direction), where location is a (row, column) tuple."""
    if tactic[0] == 'E':
        from random import choice
        return choice(all_possible_moves_for('M'))
    elif tactic[0] == 'M':
        moves = []
        m_locations = player_locations('M')
        m_moves = all_possible_moves_for('M')
        for i in range (0, 3):
            for j in range (0, len(m_moves)):
                if m_locations[i] != m_moves[j][0]:
                    m_loc, m_dir = m_moves[j][0], m_moves[j][1]
                    m_next = adjacent_location(m_loc, m_dir)                 
                    moves.append((distance(m_next,m_locations[i]),m_moves[j]))  # pair-wise results, triangulation would be better
        moves = sorted(moves, reverse=True)
        return moves[0][1]
    else:  # +avoid row/column
        moves = []
        m_locations = player_locations('M')
        m_moves = all_possible_moves_for('M')
        for i in range (0, 3):
            for j in range (0, len(m_moves)):
                if m_locations[i] != m_moves[j][0]:
                    m_loc, m_dir = m_moves[j][0], m_moves[j][1]
                    m_next = adjacent_location(m_loc, m_dir)                
                    if m_next[0] != m_locations[i][0] and m_next[1] != m_locations[i][1]:
                        moves.append((distance(m_next,m_locations[i]),m_moves[j]))
        moves = sorted(moves, reverse=True)
        return moves[0][1]

def choose_enemy_move():
    """Based on all possible moves for 'R', priotise moves that move in common
    direction, then moves that extend the game by creating possible moves for 'M'.
    Returns a tuple (location, direction), where location is a (row, column) tuple."""
    if tactic[0] == 'E':
        return choice(all_possible_moves_for('R'))
    elif tactic[0] == 'M':
        m_moves = all_possible_moves_for('M', legal=False)
        e_moves = all_possible_moves_for('R')
        moves = []
        for i in range (0, len(e_moves)):
            e_loc, e_dir = e_moves[i][0], e_moves[i][1]
            e_move = adjacent_location(e_loc, e_dir)
            for j in range (0, len(m_moves)):
                m_loc, m_dir = m_moves[j][0], m_moves[j][1]
                m_move = adjacent_location(m_loc, m_dir)
                if e_move == m_move:
                    moves.append(e_moves[i])
        return choice(moves)
    else:
        m_moves = all_possible_moves_for('M', legal=False)  # repetition!!
        e_moves = all_possible_moves_for('R')
        moves = []
        for i in range (0, len(e_moves)):
            e_loc, e_dir = e_moves[i][0], e_moves[i][1]
            e_move = adjacent_location(e_loc, e_dir)
            for j in range (0, len(m_moves)):
                m_loc, m_dir = m_moves[j][0], m_moves[j][1]
                m_move = adjacent_location(m_loc, m_dir)
                if e_move == m_move:
                    moves.append(e_moves[i])
        move = []
        for dir in tactic[1]:
            for m in moves:
                if m[1] == dir:
                    move.append(m)
            if len(move) > 0:
                break
                return choice(moves)
        return choice(moves)

#%%---------- Communicating with the user ----------
#----you do not need to modify code below unless you find a bug
#----a bug in it before you move to stage 3

def print_board():
    print("    1  2  3  4  5")
    print("  ---------------")
    ch = "A"
    for i in range(0, 5):
        print(ch, "|", end = " ")
        for j in range(0, 5):
            print(board[i][j] + " ", end = " ")
        print()
        ch = chr(ord(ch) + 1)
    print()

def print_instructions():
    print()
    print("""To make a move, enter the location of the piece you want to move,
and the direction you want it to move. Locations are indicated as a
letter (A, B, C, D, or E) followed by an integer (1, 2, 3, 4, or 5).
Directions are indicated as left, right, up, or down (or simply L, R,
U, or D). For example, to move the Musketeer from the top right-hand
corner to the row below, enter 'A5 left' (without quotes).
For convenience in typing, you may use lowercase letters.""")
    print()

def choose_users_side():
    """Returns 'M' if user is playing Musketeers, 'R' otherwise."""
    user = ""
    while user != 'M' and user != 'R':
        answer = input("Would you like to play Musketeer (M) or enemy (R)? ")
        answer = answer.strip()
        if answer != "":
            user = answer.upper()[0]
    return user

def describe_move(who, location, direction):
    """Prints a sentence describing the given move."""
    new_location = adjacent_location(location, direction)
    print(who, 'moves', direction, 'from',\
          location_to_string(location), 'to',\
          location_to_string(new_location) + ".\n")

#%% User communication updates

def get_users_move():
    """Gets a legal move from the user, and returns it as a
       (location, direction) tuple."""    
    directions = {'L':'left', 'R':'right', 'U':'up', 'D':'down'}
    move = input("Your move? ").upper().replace(' ', '')
    if (len(move) >= 3
            and move[0] in 'ABCDE'
            and move[1] in '12345'
            and move[2] in 'LRUD'):
        location = string_to_location(move[0:2])
        direction = directions[move[2]]
        if is_legal_move(location, direction):
            return (location, direction)
    print("Illegal move--'" + move + "'")
    return get_users_move()

def choose_difficulty():
    """Returns 'E', 'M' or 'H' based on user selectedstart difficulty."""
    difficulty = ""
    while difficulty != 'E' and difficulty != 'M' and difficulty != 'H':
        answer = input("Select computer difficulty level. Easy (E), Medium (M) or Hard (H)? ")
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
    from random import choice
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