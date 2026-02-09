#Shared methods for Rush Hour puzzle to parse the board, get moves, apply moves
#A state is a tuple of 6 tuples of 6 chars (the 6x6 grid).

# Exit 
EXIT_ROW = 2
EXIT_COL = 6

#Read a board file and return the 6x6 interior as a tuple of tuples
def parse_board_file(filepath):
    with open(filepath) as f:
        lines = [line.rstrip() for line in f.readlines()]
    rows = []
    for i in range(1, 7):
        line = lines[i]
        row = line[1:7]
        rows.append(tuple(row))
    return tuple(rows)

#Scan the grid and return a list of vehicles (id, row, col, length, H/V).
def get_vehicles(state):
    seen = set()
    vehicles = []
    for r in range(6):
        for c in range(6):
            ch = state[r][c]
            if ch not in (' ', '*') and ch not in seen:
                seen.add(ch)
                # figure out if horizontal or vertical and length
                if c + 1 < 6 and state[r][c + 1] == ch:
                    # horizontal
                    length = 1
                    while c + length < 6 and state[r][c + length] == ch:
                        length += 1
                    vehicles.append((ch, r, c, length, 'H'))
                else:
                    # vertical
                    length = 1
                    while r + length < 6 and state[r + length][c] == ch:
                        length += 1
                    vehicles.append((ch, r, c, length, 'V'))
    return vehicles

#when red car X is not on the board anymore
def is_goal(state):
    for r in range(6):
        for c in range(6):
            if state[r][c] == 'X':
                return False
    return True


#Convert lists to tuples
def list_to_state(grid):
    return tuple(tuple(row) for row in grid)

#Apply a single move and return the new state
def apply_move(state, move):
    vid, direction = move[0], move[1]
    vehicles = get_vehicles(state)
    # find this vehicle
    for v in vehicles:
        if v[0] == vid:
            break
    else:
        return None  # vehicle not found

    vrow, vcol, length, orient = v[1], v[2], v[3], v[4]
    grid = [list(row) for row in state]

    if direction == 'L':
        if orient != 'H':
            return None
        new_col = vcol - 1
        if new_col < 0:
            return None
        dest = grid[vrow][new_col]
        if dest != ' ' and dest != '*':
            return None
        if dest == '*' and vid != 'X':
            return None
        for i in range(length):
            grid[vrow][vcol + i] = ' '
        if dest != '*':
            for i in range(length):
                grid[vrow][new_col + i] = vid
        return list_to_state(grid)

    if direction == 'R':
        if orient != 'H':
            return None

        front = vcol + length - 1
        nextc = front + 1

        # escape: X moves off the board to the right
        if vid == 'X' and vrow == EXIT_ROW and nextc == EXIT_COL:
            for i in range(length):
                grid[vrow][vcol + i] = ' '
            return list_to_state(grid)

        # normal right move
        if nextc >= 6:
            return None
        if grid[vrow][nextc] != ' ':
            return None

        # move right by 1
        grid[vrow][vcol] = ' '
        grid[vrow][nextc] = vid
        return list_to_state(grid)


    if direction == 'U':
        if orient != 'V':
            return None
        new_row = vrow - 1
        if new_row < 0:
            return None
        dest = grid[new_row][vcol]
        if dest != ' ' and dest != '*':
            return None
        if dest == '*' and vid != 'X':
            return None
        for i in range(length):
            grid[vrow + i][vcol] = ' '
        if dest != '*':
            for i in range(length):
                grid[new_row + i][vcol] = vid
        return list_to_state(grid)

    if direction == 'D':
        if orient != 'V':
            return None
        new_row = vrow + length
        if new_row >= 6:
            return None
        dest = grid[new_row][vcol]
        if dest != ' ' and dest != '*':
            return None
        if dest == '*' and vid != 'X':
            return None
        for i in range(length):
            grid[vrow + i][vcol] = ' '
        if dest != '*':
            for i in range(length):
                grid[vrow + 1 + i][vcol] = vid
        return list_to_state(grid)

    return None

#Return list of all allowed moves from this state.
def get_all_moves(state):
    vehicles = get_vehicles(state)
    moves = []
    for v in vehicles:
        vid, r, c, length, orient = v[0], v[1], v[2], v[3], v[4]
        if orient == 'H':
            # can move left or no
            if c > 0 and state[r][c - 1] in (' ', '*'):
                if state[r][c - 1] != '*' or vid == 'X':
                    moves.append(vid + 'L')
            
            # can move right or no
            front = c + length - 1
            nextc = front + 1

            if vid == 'X' and r == EXIT_ROW and nextc == EXIT_COL:
                moves.append('XR')
            elif nextc < 6 and state[r][nextc] == ' ':
                moves.append(vid + 'R')

        else:
            # vertical
            if r > 0 and state[r - 1][c] in (' ', '*'):
                if state[r - 1][c] != '*' or vid == 'X':
                    moves.append(vid + 'U')
            if r + length < 6 and state[r + length][c] in (' ', '*'):
                if state[r + length][c] != '*' or vid == 'X':
                    moves.append(vid + 'D')
    return moves

#Return list of (move, new_state) for each allowed move
def get_successors(state):
    result = []
    for move in get_all_moves(state):
        new_state = apply_move(state, move)
        if new_state is not None:
            result.append((move, new_state))
    return result


def h1_distance(state):
    # find rightmost column of X
    right = None
    for r in range(6):
        for c in range(6):
            if state[r][c] == 'X' and (right is None or c > right):
                right = c

    if right is None:
        return 0

    # distance from X's right edge to exit
    return (EXIT_COL - 1) - right 


def h2_distance(state):
    # find rightmost column of X
    right = None
    for r in range(6):
        for c in range(6):
            if state[r][c] == 'X' and (right is None or c > right):
                right = c

    if right is None:
        return 0

    # count blocking vehicles
    blocking_vehicles = set()
    for col in range(right + 1, 6):
        ch = state[EXIT_ROW][col]
        if ch != ' ':
            blocking_vehicles.add(ch)

    return ((EXIT_COL - 1) - right) + len(blocking_vehicles)

