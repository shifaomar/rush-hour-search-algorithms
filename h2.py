#h2 Best-first search solver using h2, 
#estimates teh remaining cost as the no. of moves the red car needs to reach the exit 
#plus the no. of blocking vehicles. 

import sys
import heapq


from rushhour import (
    parse_board_file,
    is_goal,
    get_successors,
    h2_distance,
)


def h2(initial_state, heuristic, max_nodes=None):
    heap = []
    h0 = heuristic(initial_state)
    heapq.heappush(heap, (h0, 0, initial_state, []))

    closed = set()   # states already expanded
    nodes_visited = 0

    while heap:
        if max_nodes is not None and nodes_visited >= max_nodes:
            return None, nodes_visited

        f, g, state, path = heapq.heappop(heap)

        # Skip duplicate heap entries
        if state in closed:
            continue

        # Now expanding this state
        closed.add(state)
        nodes_visited += 1

        if is_goal(state):
            return path, nodes_visited

        for move, new_state in get_successors(state):
            if new_state in closed:
                continue
            new_g = g + 1
            new_f = new_g + heuristic(new_state)
            heapq.heappush(heap, (new_f, new_g, new_state, path + [move]))

    return None, nodes_visited



def main():
    if len(sys.argv) != 2:
        print("missing input file", file=sys.stderr)
        sys.exit(1)

    board_path = sys.argv[1]
    state = parse_board_file(board_path)
    solution, nodes_visited = h2(state, h2_distance)

    if solution is None:
        print("No solution found :(", file=sys.stderr)
        sys.exit(1)
    #remove later, for report
    print("Nodes visited:", nodes_visited, file=sys.stderr)
    for move in solution:
        print(move)


if __name__ == "__main__":
    main()
