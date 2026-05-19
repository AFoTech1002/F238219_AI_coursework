# COA207 - Foundations of AI
# Component 2: Implementation
# Route finding with BFS, UCS, and A* on a UK city graph

from collections import deque
import heapq

# Undirected graph: each city maps to a list of (neighbour, distance_in_miles).
# Experiment note: the Cambridge->Sheffield edge was increased from ~101 miles
# to 160 miles so that BFS and cost-based search return different routes.
GRAPH: dict[str, list[tuple[str, int]]] = {
    "London": [("Oxford", 57), ("Cambridge", 60)],
    "Oxford": [("London", 57), ("Birmingham", 63), ("Bristol", 75)],
    "Birmingham": [
        ("Oxford", 63),
        ("Bristol", 85),
        ("Cardiff", 110),
        ("Manchester", 86),
        ("Sheffield", 91),
    ],
    "Cambridge": [("London", 60), ("Sheffield", 160)],
    "Bristol": [("Oxford", 75), ("Birmingham", 85), ("Cardiff", 44)],
    "Cardiff": [("Bristol", 44), ("Birmingham", 110)],
    "Manchester": [("Birmingham", 86), ("Liverpool", 35), ("Sheffield", 38), ("Leeds", 43)],
    "Leeds": [("Manchester", 43), ("Sheffield", 30), ("Newcastle", 94)],
    "Liverpool": [("Manchester", 35)],
    "Sheffield": [("Cambridge", 160), ("Birmingham", 91), ("Manchester", 38), ("Leeds", 30)],
    "Newcastle": [("Leeds", 94), ("Edinburgh", 105)],
    "Edinburgh": [("Newcastle", 105)],
}

# Straight-line distances to Edinburgh in miles, used as h(n) for A*.
# These are admissible because they do not overestimate real road distance.
HEURISTIC: dict[str, int] = {
    "London": 335,
    "Oxford": 340,
    "Birmingham": 270,
    "Cambridge": 290,
    "Bristol": 360,
    "Cardiff": 380,
    "Manchester": 200,
    "Leeds": 160,
    "Liverpool": 220,
    "Sheffield": 190,
    "Newcastle": 105,
    "Edinburgh": 0,
}


def bfs(start: str, goal: str) -> tuple[list[str], int, int]:
    """BFS explores layer by layer, so it finds the fewest-hop path."""
    print("=" * 55)
    print("BFS (Breadth-First Search)")
    print("=" * 55)

    frontier: deque[tuple[list[str], int]] = deque([([start], 0)])
    explored: set[str] = set()
    nodes_expanded = 0

    while frontier:
        path, cost = frontier.popleft()
        current = path[-1]

        if current in explored:
            continue
        explored.add(current)
        nodes_expanded += 1
        print(f"  Expanding: {current:<12} | cost so far: {cost} mi | path: {' -> '.join(path)}")

        if current == goal:
            print(f"\n  Found: {' -> '.join(path)}")
            print(f"  Total: {cost} miles | Nodes expanded: {nodes_expanded}\n")
            return path, cost, nodes_expanded

        for neighbour, edge_cost in GRAPH[current]:
            if neighbour not in explored:
                frontier.append((path + [neighbour], cost + edge_cost))

    return [], 0, nodes_expanded


def ucs(start: str, goal: str) -> tuple[list[str], int, int]:
    """UCS expands the cheapest node so far, so it finds the minimum-distance path."""
    print("=" * 55)
    print("UCS (Uniform Cost Search)")
    print("=" * 55)

    frontier: list[tuple[int, str, list[str]]] = []
    heapq.heappush(frontier, (0, start, [start]))
    explored: set[str] = set()
    nodes_expanded = 0

    while frontier:
        cost, current, path = heapq.heappop(frontier)

        if current in explored:
            continue
        explored.add(current)
        nodes_expanded += 1
        print(f"  Expanding: {current:<12} | g={cost:<5} | path: {' -> '.join(path)}")

        if current == goal:
            print(f"\n  Found: {' -> '.join(path)}")
            print(f"  Total: {cost} miles | Nodes expanded: {nodes_expanded}\n")
            return path, cost, nodes_expanded

        for neighbour, edge_cost in GRAPH[current]:
            if neighbour not in explored:
                heapq.heappush(frontier, (cost + edge_cost, neighbour, path + [neighbour]))

    return [], 0, nodes_expanded


def astar(start: str, goal: str) -> tuple[list[str], int, int]:
    """A* uses f(n) = g(n) + h(n), combining cost so far and estimated remaining cost."""
    print("=" * 55)
    print("A* Search")
    print("=" * 55)

    frontier: list[tuple[int, int, str, list[str]]] = []
    heapq.heappush(frontier, (HEURISTIC[start], 0, start, [start]))
    explored: set[str] = set()
    nodes_expanded = 0

    while frontier:
        f, g, current, path = heapq.heappop(frontier)

        if current in explored:
            continue
        explored.add(current)
        nodes_expanded += 1
        h = HEURISTIC[current]
        print(
            f"  Expanding: {current:<12} | g={g:<5} h={h:<5} f={f:<5} | path: {' -> '.join(path)}"
        )

        if current == goal:
            print(f"\n  Found: {' -> '.join(path)}")
            print(f"  Total: {g} miles | Nodes expanded: {nodes_expanded}\n")
            return path, g, nodes_expanded

        for neighbour, edge_cost in GRAPH[current]:
            if neighbour not in explored:
                new_g = g + edge_cost
                new_f = new_g + HEURISTIC[neighbour]
                heapq.heappush(frontier, (new_f, new_g, neighbour, path + [neighbour]))

    return [], 0, nodes_expanded


def print_comparison(results: dict[str, tuple[list[str], int, int]]) -> None:
    print("=" * 55)
    print("COMPARISON TABLE")
    print("=" * 55)
    header = f"{'Algorithm':<10} | {'Nodes':>6} | {'Cost (mi)':>10} | Path"
    print(header)
    print("-" * 80)
    for algo, (path, cost, expanded) in results.items():
        print(f"{algo:<10} | {expanded:>6} | {cost:>10} | {' -> '.join(path)}")

    print("\nNotes:")
    print("  BFS  - fewest hops (5 edges), but ignores costs -> not distance-optimal")
    print("  UCS  - optimal distance (440 mi); explores all 12 nodes uninformedly")
    print("  A*   - same optimal cost as UCS, only 9 nodes thanks to heuristic guidance")


if __name__ == "__main__":
    START = "London"
    GOAL = "Edinburgh"
    print(f"\nRoute Finding: {START} --> {GOAL}\n")
    results = {
        "BFS": bfs(START, GOAL),
        "UCS": ucs(START, GOAL),
        "A*": astar(START, GOAL),
    }
    print_comparison(results)
