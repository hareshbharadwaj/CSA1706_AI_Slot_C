# CSA1706 AI Slot C

Python implementations of Breadth-First Search (BFS), Depth-First Search (DFS), and the Water Jug Problem (WJP) using state-space search.

## Programs

- `BFS.py` builds each graph as an adjacency list and visits reachable nodes level by level using a queue.
- `DFS.py` builds the same adjacency lists and explores each path as far as possible before backtracking.
- Graphs 1-3 are undirected. Graph 4 is directed, so traversals follow only the listed edge directions.
- The traversal starts at node `1` for graphs 1-3 and node `0` for graph 4. A traversal reports only nodes reachable from its start node.
- `wjp.py` solves the multi-jug Water Jug Problem using Breadth-First Search (BFS) to find the shortest sequence of state transitions (Pour, Fill, Empty) from an initial state to a target volume. Includes cases such as `12/12 0/8 0/5 -> target 4` and `0/6 0/8 0/5 -> target 5`.

## Run

```bash
python BFS.py
python DFS.py
python wjp.py

# Optional: Run wjp.py with custom input
python wjp.py "12/12 0/8 0/5 target : 4"
python wjp.py "0/6 0/8 0/5 : target 5"
```

## Pseudocode

### BFS.py

```text
BUILD-GRAPH(nodes, edges, directed):
    create an empty neighbor list for every node
    for each (source, destination) edge:
        add destination to source's neighbors
        if graph is undirected:
            add source to destination's neighbors
    return graph

BFS(graph, start):
    mark start visited
    enqueue start
    traversal = empty list
    while queue is not empty:
        node = dequeue
        append node to traversal
        for each neighbor of node:
            if neighbor is not visited:
                mark neighbor visited
                enqueue neighbor
    return traversal

build the four graphs from their node and edge lists
print BFS(graph1, 1), BFS(graph2, 1), BFS(graph3, 1), BFS(graph4, 0)
```

### DFS.py

```text
BUILD-GRAPH(nodes, edges, directed):
    create an empty neighbor list for every node
    for each (source, destination) edge:
        add destination to source's neighbors
        if graph is undirected:
            add source to destination's neighbors
    return graph

DFS(graph, start):
    visited = empty set
    traversal = empty list

    VISIT(node):
        mark node visited
        append node to traversal
        for each neighbor of node:
            if neighbor is not visited:
                VISIT(neighbor)

    VISIT(start)
    return traversal

build the four graphs from their node and edge lists
print DFS(graph1, 1), DFS(graph2, 1), DFS(graph3, 1), DFS(graph4, 0)
```

### wjp.py

```text
SOLVE-WATER-JUG(capacities, initial_state, target):
    queue = empty queue
    visited = empty set
    enqueue (initial_state, path = [initial_state])
    add initial_state to visited

    while queue is not empty:
        (current_state, path) = dequeue
        if any amount in current_state equals target:
            return path

        for each valid action from current_state:
            # 1. Pour water from jug i into jug j (i != j):
            #    amount = min(current_state[i], capacities[j] - current_state[j])
            # 2. Fill jug i to its maximum capacity:
            #    next_state[i] = capacities[i]
            # 3. Empty jug i completely:
            #    next_state[i] = 0

            if next_state not in visited:
                add next_state to visited
                enqueue (next_state, path + [(action, next_state)])

    return no solution
```
