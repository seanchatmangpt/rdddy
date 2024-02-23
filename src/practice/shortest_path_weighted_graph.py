import heapq


class WeightedGraph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]

    def add_edge(self, u, v, w):
        self.graph[u].append((v, w))


def dijkstra_with_min_edges(graph, src, target):
    min_heap = [(0, 0, src)]
    distances = {i: float("inf") for i in range(graph.V)}
    edges_count = {i: float("inf") for i in range(graph.V)}
    distances[src] = 0
    edges_count[src] = 0

    while min_heap:
        current_distance, current_edges, u = heapq.heappop(min_heap)

        if u == target:
            break

        for neighbor, weight in graph.graph[u]:
            distance = current_distance + weight

            if distance < distances[neighbor] or (
                distance == distances[neighbor]
                and current_edges + 1 < edges_count[neighbor]
            ):
                distances[neighbor] = distance
                edges_count[neighbor] = current_edges + 1
                heapq.heappush(min_heap, (distance, current_edges + 1, neighbor))

    return distances[target], edges_count[target]


vertices = 6
graph = WeightedGraph(vertices)
graph.add_edge(0, 1, 1)
graph.add_edge(1, 2, 1)
graph.add_edge(0, 2, 2)
graph.add_edge(1, 3, 1)
graph.add_edge(2, 3, 2)
graph.add_edge(3, 4, 1)
graph.add_edge(4, 5, 1)

src = 0
target = 5
distance, edges = dijkstra_with_min_edges(graph, src, target)
print(
    f"Shortest path from {src} to {target} has distance {distance} using {edges} edges."
)
