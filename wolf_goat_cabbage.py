from collections import deque

def is_valid(state):
    m, w, g, c = state
    # check left bank without man
    if m != 'L':
        if w == 'L' and g == 'L':
            return False
        if g == 'L' and c == 'L':
            return False
    # check right bank without man
    if m != 'R':
        if w == 'R' and g == 'R':
            return False
        if g == 'R' and c == 'R':
            return False
    return True

def find_shortest_path():
    start = ('L', 'L', 'L', 'L')
    end = ('R', 'R', 'R', 'R')

    visited = set()
    queue = deque()
    queue.append((start, [start]))
    visited.add(start)

    while queue:
        current_state, path = queue.popleft()
        if current_state == end:
            return path
        current_man = current_state[0]
        other_side = 'R' if current_man == 'L' else 'L'
        # generate move alone
        new_state = list(current_state)
        new_state[0] = other_side
        new_state_tuple = tuple(new_state)
        if new_state_tuple not in visited and is_valid(new_state_tuple):
            visited.add(new_state_tuple)
            queue.append((new_state_tuple, path + [new_state_tuple]))
        # generate moves with each item
        for i in range(1, 4):
            if current_state[i] == current_man:
                new_state = list(current_state)
                new_state[0] = other_side
                new_state[i] = other_side
                new_state_tuple = tuple(new_state)
                if new_state_tuple not in visited and is_valid(new_state_tuple):
                    visited.add(new_state_tuple)
                    queue.append((new_state_tuple, path + [new_state_tuple]))
    return None

def print_moves(path):
    item_names = {1: 'wolf', 2: 'goat', 3: 'cabbage'}
    for i in range(1, len(path)):
        prev = path[i-1]
        curr = path[i]
        moved = []
        for j in range(4):
            if prev[j] != curr[j]:
                moved.append(j)
        if len(moved) == 1:
            print(f"Man crosses alone from {prev[0]} to {curr[0]}")
        else:
            item_index = moved[1]
            item = item_names[item_index]
            print(f"Man takes {item} from {prev[0]} to {curr[0]}")

path = find_shortest_path()
if path:
    print("Shortest sequence of moves:")
    print_moves(path)
else:
    print("No solution found.")