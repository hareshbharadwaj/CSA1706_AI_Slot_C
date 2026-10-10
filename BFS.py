from collections import deque


def build_graph(nodes, edges, directed=False):
	graph = {node: [] for node in nodes}
	for source, destination in edges:
		graph[source].append(destination)
		if not directed:
			graph[destination].append(source)
	return graph


def bfs(graph, start):
	visited = {start}
	queue = deque([start])
	traversal = []

	while queue:
		node = queue.popleft()
		traversal.append(node)
		for neighbor in graph[node]:
			if neighbor not in visited:
				visited.add(neighbor)
				queue.append(neighbor)

	return traversal


graph1 = build_graph(
	nodes=[1, 2, 3, 4, 5],
	edges=[(1, 2), (1, 3), (2, 4), (2, 5), (4, 5)],
)

graph2 = build_graph(
	nodes=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
	edges=[
		(1, 2), (1, 7), (2, 3), (2, 6), (3, 4),
		(3, 5), (7, 8), (7, 10), (8, 9),
	],
)

graph3 = build_graph(
	nodes=[1, 2, 3, 4, 5, 6, 7, 8],
	edges=[
		(1, 2), (1, 3), (2, 5), (2, 6),
		(3, 4), (3, 7), (4, 8), (7, 8),
	],
)

graph4 = build_graph(
	nodes=[0, 1, 2, 3, 4, 5, 6, 7],
	edges=[
		(0, 1), (1, 3), (3, 2), (2, 1),
		(3, 4), (4, 5), (6, 4), (6, 7), (7, 5),
	],
	directed=True,
)


print("Graph 1:", bfs(graph1, 1))
print("Graph 2:", bfs(graph2, 1))
print("Graph 3:", bfs(graph3, 1))
print("Graph 4:", bfs(graph4, 0))
