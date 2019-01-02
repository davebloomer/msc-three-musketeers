# Extended Program with Strategies
# 13161521 - David Bloomer - MSc Data Science (PT)

#%% Updated and additional functions
    
def computer_tactic(difficulty):
    """Stores the computer difficulty and a creates series of directions.
    The directions can be used to determine strategy and vary from
    game to game to limit predictability. As tactic is a global variable,
    directions are represented as an encrypted string, which can be called
    using tactic_lookup()."""
    global tactic
    select_tactic = choice(['ugsRGv','Wq4d66','KhzYQv','Vn4SHy','WuvaNj','gHwrEP','WfGHet','W8vzXJ'])  # String chosen at random corresponding to a series of directions
    tactic = (difficulty, select_tactic)  # Sets global variable tactic to contain difficulty and series of directions where relevant

def tactic_lookup():
    """To avoid having computer tactic visable as global variable, a
    dictionary is defined to anonamise the tactic to the player. Output is a
    tuple of directions, which are prioritised from left to right."""
    tactic_dict = {  # Look-up table corresponding to strings in computer_tactic()
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
    """Replaces the tactic with new_tactic. May be useful for testing."""
    global tactic
    tactic = (difficulty, new_tactic)
    
def distance(loc1, loc2):
    """Returns the distance between two locations on board.
    Independant of possible range of board locations."""
    (row1, col1) = loc1
    (row2, col2) = loc2
    return round(((row2-row1)**2 + (col2-col1)**2)**0.5, 1)

def area(loc1, loc2, loc3):
    """Returns the area between three locations on board.
    Independant of possible range of board locations."""
    (row1, col1) = loc1
    (row2, col2) = loc2
    (row3, col3) = loc3
    return round(abs((row1*(col2-col3)+row2*(col3-col1)+row3*(col1-col2))/2),2)

def can_move_piece_at(location, direction=['left', 'up', 'down', 'right'], legal=True):
    # Included direction as hyperparameter to avoid redundancy in is_legal_move(), by default contains all legal (perpendicular) move directions
    # Directions must be stored as list rather than tuple, otherwise when single direction is given, tuple will iterate through letters
    """Tests whether the player at the location has at least one move available.
    You can assume that input will always be in correct range."""
    """Additional hyperparameter defines whether legal or illegal moves are
    returned, by default this is True. This functionality is used in computer
    tactics to predict possible moves taken by the next player. For example,
    the enemy may wish to move to a location where a legal move is currently
    not available to extend game."""    
    if at(location) == 'M':  # Uses at() to determine player at hyperparameter location, if musketeer:
        for dir in direction:  # Itererate through each element in hyperparameter direction
            if is_within_board(location, dir) == True and is_legal_move_by_musketeer(location, dir) == legal:  # If location in direction is valid and legal move
                return True  # Return True and break
                break
        return False  # Return False if logic not met for all directions considered
    elif at(location) == 'R':  # Alternate scenario, if player at hyperparameter location is enemy:
        for dir in direction:
            if is_within_board(location, dir) == True and is_legal_move_by_enemy(location, dir) == legal:  # If location in direction is valid and legal move
                return True  # Return True and break
            
                break
        return False  # Return False if logic not met for all directions considered
    else:  # Else condition, if no valid moves are present for player at location, return False
        return False

def possible_moves_from(location, legal=True):
    """Returns a list of directions ('left', etc.) in which it is legal
       for the player at location to move. If there is no player at
       location, returns the empty list, [].
       You can assume that input will always be in correct range."""
    """Additional hyperparameter defines whether legal or illegal moves are
    returned, by default this is True. Passes legal to can_move_piece_at()"""  
    moves = []  # Initialises empty list, to contain all valid move directions
    direction=['left', 'up', 'down', 'right']  # Local variable defined containing all legal (perpendicular) move directions
    for dir in direction:  # Itererate through each element in variable direction
        if can_move_piece_at(location, [dir], legal) == True:  # If is a valid move for player at location, can_move_piece_at() will return True 
                moves.append(dir)  # Append list with valid move direction
    return moves
    
def player_locations(player):
    """Returns all locations for the player in a list of tuples.
    Previously part of all_possible_moves_for(), but useful input for other
    functions."""
    # List comprehension to find player location(s) from global variable board
    return [(i, j) for i in range(0,5) for j in range(0,5) if board[i][j] == player]

def all_possible_moves_for(player, legal=True):
    """Returns every possible move for the player ('M' or 'R') as a list
    (location, direction) tuples.
    You can assume that input will always be in correct range."""
    """Additional hyperparameter defines whether legal or illegal moves are
    returned, by default this is True. Passes legal to possible_moves_from()"""
    player_loc = player_locations(player)  # Player locations determined from player_locations()
    moves = []  # Initialises empty list, to contain all valid moves for each location in list
    for loc in player_loc:  # For each player location
        for dir in possible_moves_from(loc, legal):  # Determine valid move directions from possible_moves_from()
            moves.append((loc, dir))  # Append list with combination of player location and direction
    return moves

def choose_computer_move(who):
    """The computer chooses a move for a Musketeer (who = 'M') or an
    enemy (who = 'R') and returns it as the tuple (location, direction),
    where a location is a (row, column) tuple as usual.
    You can assume that input will always be in correct range."""
    if has_some_legal_move_somewhere(who) == False:  # Logic checks if any moves are possible for hyperparameter who using has_some_legal_move_somewhere()
        raise ValueError('No moves possible.')  # If False, an exception is thrown
    elif who == 'M':  # Musketeer and enemy move are defined as seperate functions due to complexity
        return choose_musketeer_move(difficulty=tactic[0])  # Calls choose_musketeer_move() along with difficulty level from tactic global variable
    else:  # who == 'R'
        return choose_enemy_move(difficulty=tactic[0])  # Calls choose_enemy_move() along with difficulty level from tactic global variable
    
def choose_musketeer_move(difficulty):
    """Extension of choose_computer_move('M'). Hyperparameter difficulty defined
    determines tactic used by computer. These are:
    'E' = random choice of all legal moves possible
    'M' = where possible, a random choice of all legal moves that do not place
        musketeer in common row or column
    'H' = for all legal moves possible, subsequent area is calculated between
        musketeer locations, the move creating the largest area is chosen
    Returns a tuple (location, direction), where location is a (row, column) tuple."""
    if difficulty == 'E':  # If computer diffuculty is 'E':
        return choice(all_possible_moves_for('M'))  # Returns random element of output from all_possible_moves_for() for musketeers
    else:
        moves = []  # Initialises empty list, to contain all moves that meet critera for tactic
        m_locations = player_locations('M')  # Location of musketeers
        m_moves = all_possible_moves_for('M')  # Possible moves for musketeers
        for i in range (0, 3):  # i iteration represents each of the three musketeers, moves for each will be considered in turn
            m_loc1 = m_locations[i-1]  # The locations of the other musketeers are stored in local variables
            m_loc2 = m_locations[i-2]
            m_loc_row = (m_loc1[0], m_loc2[0])  # Locations are re-arranged in to tuples containing rows and cols
            m_loc_col = (m_loc1[1], m_loc2[1])
            for j in range (0, len(m_moves)):  # j iternation represents each possible move
                if m_locations[i] == m_moves[j][0]:  # If possible move is for ith musketeer being considered
                    m_next = adjacent_location(m_moves[j][0], m_moves[j][1])  # Calculate resultant location of musketeer following move
                    if difficulty == 'M':  # If computer diffuculty is 'M':
                        # Append moves which do not result in moving in to same row or column as other musketeers
                        if m_next[0] not in m_loc_row and m_next[1] not in m_loc_col:
                            moves.append(m_moves[j])
                    else:  # If computer diffuculty is 'H':
                        # Append area and move for each possible move
                        moves.append((area(m_next,m_loc1,m_loc2), m_moves[j]))
        if difficulty == 'M':  # Once possible moves for specified difficulty are calculated, if computer diffuculty is 'M':
            if len(moves) == 0:  # It may be that no move meets criteria
                return choice(m_moves)  # In this case, return random element from all possible legal moves for musketeers
            return choice(moves)  # Returns random element of variable moves
        else:  # If computer diffuculty is 'H':
            moves = sorted(moves, reverse=True)  # Variables moves is reverse sorted, in order of largest to smallest area
            return moves[0][1] # Returns move corresponding to first element of variable moves (ie. the largest area)

def choose_enemy_move(difficulty):
    """Extension of choose_computer_move('R'). Hyperparameter difficulty defined
    determines tactic used by computer. These are:
    'E' = random choice of all legal moves possible
    'M' = random choice of all legal moves that place enemy in position
        perpendicular to musketeer, with preference given to moves that draw
        musketeer in direction specified by computer tactic
    'H' = if option exists for musketeer to move in opposite direction from
        specified tactic, it is removed, otherwise difficulty 'M' move played
    Returns a tuple (location, direction), where location is a (row, column) tuple."""
    if difficulty == 'E':  # If computer diffuculty is 'E':
        return choice(all_possible_moves_for('R'))  # Returns random element of output from all_possible_moves_for() for enemy
    else:
        if difficulty == 'H':  # If computer diffuculty is 'H':
            m_moves = all_possible_moves_for('M', legal=True)  # Possible moves for musketeers that are currently available
            moves = []  # Initialises empty list, to contain all moves that meet critera for tactic
            for i in range (0, len(m_moves)):  # i iternation represents each possible musketeer move
                if can_move_piece_at(adjacent_location(m_moves[i][0], m_moves[i][1]), [tactic_lookup()[-1]]) == True:  # If enemy can move away from musketeer to block movement in opposite of tactic direction
                    moves.append((adjacent_location(m_moves[i][0], m_moves[i][1]), tactic_lookup()[-1]))  # Append enemy move to list
            if len(moves) > 0:  # If such a move exists, return random element from moves
                return choice(moves)
        # If difficulty = 'M', or no valid blocking move is available for difficulty 'H':
        e_moves = all_possible_moves_for('R')  # Possible moves for enemy
        m_moves = all_possible_moves_for('M', legal=False)  # Possible moves for musketeers that are not currently available (ie. potential next moves)
        moves = []  # Initialises empty list, to contain all moves that meet critera for tactic
        for i in range (0, len(e_moves)):  # i iternation represents each possible enemy move
            e_next = adjacent_location(e_moves[i][0], e_moves[i][1])  # Calculate resultant location of enemy following move
            for j in range (0, len(m_moves)):  # j iternation represents each possible illegal musketeer move
                m_next = adjacent_location(m_moves[j][0], m_moves[j][1])  # Calculate resultant location of musketeer following move
                if e_next == m_next:  # Where combination of moves matches, the enemy move would allow musketeer to make jth move if selected
                        moves.append((m_moves[j], e_moves[i]))  # Append corresponding musketeer and enemy moves
        if len(moves) == 0:  # It may be that no move meets criteria (ie. the final move of the game)
            return choice(e_moves) # In this case, return random element from all possible legal moves for enemy
        else:
            moves_in_dir = []  # Initialises empty list, to contain subset of moves that meet critera for tactic
            for dir in tactic_lookup():  # Iteration to check each preferential move direction for tactic in turn
                for m in moves:  # Iteration to consider each move in variable moves 
                    if m[0][1] == dir:  # Where musketeer move direction matches tactic direction
                        moves_in_dir.append(m[1])  # Append enemy move to list
                if len(moves_in_dir) > 0:  # If any moves matches tactic direction considered
                    return choice(moves_in_dir)  # Return random element from variable moves_in_dir
        
#%% Updated and additional user communication

def choose_difficulty():  # Modified version of choose_users_side() from base implimentation
    """Returns 'E', 'M' or 'H' based on user selected start difficulty."""
    difficulty = ""
    while difficulty != 'E' and difficulty != 'M' and difficulty != 'H':
        answer = input("Select computer difficulty level. Easy (E), Medium (M) or Hard (H)? ")
        answer = answer.strip()
        if answer != "":
            difficulty = answer.upper()[0]
    return computer_tactic(difficulty)  # User input calls computer_tactic() to create tactic global variable

def start():  # Modified version of start() from base implimentation
    """Plays the Three Musketeers Game."""
    users_side = choose_users_side()
    tactic = choose_difficulty()  # User now prompted to select game difficulty
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

#%% Tactics Evaluation - independant from start() functionality
"""The following code is not part of the game. It allows n simulations of the
game to be played using the computer controlling both sides. The difficulty is
specified for the musketeers and enemy using mdiff and ediff respectively. This
function is useful for evaluating tactics, a summary of findings is given in the
GitHub readme."""

def play_sim(n, mdiff='M', ediff='M'):
    computer_tactic(ediff)  # computer_tactic() function is called to generate directions used for enemy at 'H' difficulty
    m_win = 0  # counter for number of musketeer wins
    e_win = 0  # counter for number of enemy wins
    m_log = []  # log stores number of moves performed in game where musketeer wins
    e_log = []  # log stores number of moves performed in game where enemy wins
    for i in range (0, n):  # iteration to complete n games
        # the following is a modified version of start()
        board = create_board()
        moves = 0  # counter for number of moves in the nth game
        while True:
            if has_some_legal_move_somewhere('M'):
                board = auto_move_musketeer(mdiff)
                moves += 1
                if is_enemy_win():  # the following is performed in enemy winning condition:
                    e_win += 1  # add 1 to number of enemy wins
                    e_log.append(moves)  # record number of moves required
                    break  # breaks nth iteration, next game will be simulated
            else:  # comparable operations are performed in musketeer winning conditions.
                m_win += 1
                m_log.append(moves)
                break
            if has_some_legal_move_somewhere('R'):
                board = auto_move_enemy(ediff)
                moves += 1
            else:
                m_win += 1
                m_log.append(moves)
                break
    # summary statistics for simulated games (games played, win number (win percent), average moves)
    print ('Played ' + str(n) + ' games:')
    print ('Wins - M: ' + str(m_win) + ' (' + str(round((m_win/n)*100,1)) + '%) R: ' + str(e_win) + ' (' + str(round((e_win/n)*100,1)) + '%)')
    if m_win > 0:  # for average moves statistic, if number of wins equals zero, stops divide by zero error
        print ('Avg Move No. - M: ' + str(round(sum(m_log)/len(m_log),1)))
    if e_win > 0:
        print ('Avg Move No. - R: ' + str(round(sum(e_log)/len(e_log),1)))

def auto_move_musketeer(mdiff):  # modified version of move_musketeer() to allow computer to play both sides and pass difficulty
        (location, direction) = choose_musketeer_move(difficulty=mdiff)
        make_move(location, direction)
        
def auto_move_enemy(ediff):  # modified version of move_enemy() to allow computer to play both sides and pass difficulty
        (location, direction) = choose_enemy_move(difficulty=ediff)
        make_move(location, direction)

#%%##################################################################
#### CODE BELOW THIS POINT IS UNCHANGED FROM BASE IMPLEMENTATION ####
#####################################################################

from random import choice  # Import choice from library random, chooses random element from a non-empty sequence

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
    if at(location) != 'M':  # Logic checks character at hyperparameter location is musketeer 
        raise ValueError('Location Not Valid.')   # If logic statement is false, an exception is thrown
    elif at(adjacent_location(location, direction)) == 'R':  # Logic checks enemy present in specified adjacent location
        return True
    else:
        return False
    
def is_legal_move_by_enemy(location, direction):
    """Tests if the enemy at the location can move in the direction.
    You can assume that input will always be in correct range. Raises
    ValueError exception if at(location) is not 'R'"""
    if at(location) != 'R':  # Logic checks character at hyperparameter location is enemy 
        raise ValueError('Location Not Valid.')  # If logic statement is false, an exception is thrown
    elif at(adjacent_location(location, direction)) == '-':  # Logic checks if empty space is present in specified adjacent location
        return True
    else:
        return False

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
    # Uses adjacent_location() to find resulting position of move, then is_legal_location() to check if valid and determine output
    return is_legal_location(adjacent_location(location, direction))
    
def is_legal_move(location, direction):
    """Tests whether it is legal to move the piece at the location
    in the given direction.
    You can assume that input will always be in correct range."""
    # Uses adjacent_location() to find resulting position of move, then can_move_piece_at() to check if valid and determine output
    return can_move_piece_at(location, [direction])

def has_some_legal_move_somewhere(who):
    """Tests whether a legal move exists for player "who" (which must
    be either 'M' or 'R'). Does not provide any information on where
    the legal move is.
    You can assume that input will always be in correct range."""
    # Performs count on putputs from all_possible_moves_for(), if number of valid moves is greater than zero return True
    if len(all_possible_moves_for(who)) > 0:
        return True
    else:
        return False

def make_move(location, direction):
    """Moves the piece in location in the indicated direction.
    Doesn't check if the move is legal. You can assume that input will always
    be in correct range."""
    l1 = location  # Starting position for move
    l2 = adjacent_location(location, direction)  # Ending position for move, determined using adjacent_location()
    board[l1[0]][l1[1]], board[l2[0]][l2[1]] = '-', board[l1[0]][l1[1]]  # Contents of board are copied from starting to ending location, and replaced with empty space (-)

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

#%%--------- Communicating with the user ----------
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

def describe_move(who, location, direction):
    """Prints a sentence describing the given move."""
    new_location = adjacent_location(location, direction)
    print(who, 'moves', direction, 'from',\
          location_to_string(location), 'to',\
          location_to_string(new_location) + ".\n")