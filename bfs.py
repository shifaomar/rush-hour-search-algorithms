#bfs 
import sys
from collections import deque

from rushhour import parse_board_file, is_goal, get_successors


def bfs(initial_state, max_nodes=None):

    queue = deque([(initial_state, [])])
    visited = {initial_state}
    nodes_visited = 0

    while queue:
        if max_nodes is not None and nodes_visited >= max_nodes:
            return None, nodes_visited
        state, path = queue.popleft()
        nodes_visited += 1

        if is_goal(state):
            return path, nodes_visited

        for move, new_state in get_successors(state):
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, path + [move]))

    return None, nodes_visited


def main():
    if len(sys.argv) != 2:
        print("missing input file", file=sys.stderr)
        sys.exit(1)

    board_path = sys.argv[1]
    state = parse_board_file(board_path)
    # set max_nodes to sotp laptop from melting if needed
    solution, nodes_visited = bfs(state) 

    if solution is None:
        print("No solution found :(", file=sys.stderr)
        sys.exit(1)

    # for report (remove maybe later)
    print("Nodes visited:", nodes_visited, file=sys.stderr)
    for move in solution:
        print(move)


if __name__ == "__main__":
    main()





