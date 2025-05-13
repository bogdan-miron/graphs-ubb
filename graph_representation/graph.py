import random
import heapq
import copy

class Graph:
    def __init__(self):
        self.__nodes = 0
        self.__edges = 0
        self.__adj = {}  # key: node, value: list of [neighbor, cost]

    def add_node(self, value: int):
        if value not in self.__adj:
            self.__nodes += 1
            self.__adj[value] = []

    def add_edge(self, a: int, b: int, cost: int):
        if a not in self.__adj:
            self.add_node(a)
        if b not in self.__adj:
            self.add_node(b)

        # supports multi-graph
        self.__adj[a].append([b, cost])
        self.__edges += 1

    def remove_edge(self, a: int, b: int):
        if a not in self.__adj or not any(edge[0] == b for edge in self.__adj[a]):
            raise ValueError("No such edge exists. No operation executed.")

        self.__adj[a] = [edge for edge in self.__adj[a] if edge[0] != b]
        self.__edges -= 1

    def remove_node(self, a: int):
        if a not in self.__adj:
            raise ValueError("No such node exists. No operation executed.")

        # remove outgoing edges from a
        self.__edges -= len(self.__adj[a])
        del self.__adj[a]
        self.__nodes -= 1

        # remove incoming edges to a
        for key in list(self.__adj):
            initial_edge_count = len(self.__adj[key])
            self.__adj[key] = [edge for edge in self.__adj[key] if edge[0] != a]
            self.__edges -= initial_edge_count - len(self.__adj[key])

    def get_node_count(self) -> int:
        return self.__nodes

    def get_edge_count(self) -> int:
        return self.__edges

    def out_degree(self, a: int) -> int:
        if a not in self.__adj:
            raise ValueError(f"Node {a} does not exist.")
        return len(self.__adj[a])

    def in_degree(self, a: int) -> int:
        if a not in self.__adj:
            raise ValueError(f"Node {a} does not exist.")
        return sum(1 for key in self.__adj for edge in self.__adj[key] if edge[0] == a)

    def read_from_file(self, filename: str):
        with open(filename, 'r') as file:
            V, E = map(int, file.readline().split())

            self.__nodes = 0
            self.__edges = 0
            self.__adj = {}

            for _ in range(E):
                a, b, cost = map(int, file.readline().split())
                self.add_edge(a, b, cost)

    def write_to_file(self, filename: str):
        with open(filename, 'w') as file:
            file.write(f"{self.__nodes} {self.__edges}\n")
            for a in self.__adj:
                for b, cost in self.__adj[a]:
                    file.write(f"{a} {b} {cost}\n")

    def print_graph(self):
        print("Graph Representation (Adjacency List):")
        for node in self.__adj:
            edges = ", ".join(f"({neighbor}, cost={cost})" for neighbor, cost in self.__adj[node])
            print(f"{node}: [{edges}]")

    def generate_random_graph(self, V: int, E: int, min_cost: int = 1, max_cost: int = 100):
        if E > V * (V - 1):
            raise ValueError("Too many edges for the number of nodes.")

        # reset graph
        self.__nodes = V
        self.__edges = 0
        self.__adj = {i: [] for i in range(V)}

        possible_edges = [(i, j) for i in range(V) for j in range(V) if i != j]
        random.shuffle(possible_edges)

        for i in range(E):
            a, b = possible_edges[i]
            cost = random.randint(min_cost, max_cost)
            self.add_edge(a, b, cost)

    def dijkstra(self, start: int):
        distances = {node: float('inf') for node in self.__adj}
        previous_nodes = {node: None for node in self.__adj}
        distances[start] = 0

        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_distance > distances[current_node]:
                continue
            for neighbor, weight in self.__adj[current_node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))
        return distances, previous_nodes

    def lowest_cost_walk(self, start: int, end: int):

        # d[k][x] = lowest cost from start to x in at most k steps
        nodes = list(self.__adj.keys())
        n = len(nodes)
        max_length = n  # maximum possible length without cycles is n-1, n allows cycle detection

        d = [[float('inf')] * n for _ in range(max_length + 1)]
        # predecessor table to reconstruct the path
        predecessor = [[None for _ in range(n)] for _ in range(max_length + 1)]

        # map node values to indices for easier access
        node_to_index = {node: idx for idx, node in enumerate(nodes)}
        start_idx = node_to_index[start]

        # base case: starting node has cost 0 with 0 steps
        d[0][start_idx] = 0

        for k in range(1, max_length + 1):
            d[k] = d[k - 1].copy()
            predecessor[k] = predecessor[k - 1].copy()

            for node in nodes:
                node_idx = node_to_index[node]
                for neighbor, cost in self.__adj[node]:
                    neighbor_idx = node_to_index[neighbor]
                    if d[k - 1][node_idx] + cost < d[k][neighbor_idx]:
                        d[k][neighbor_idx] = d[k - 1][node_idx] + cost
                        predecessor[k][neighbor_idx] = node

        # check for negative cost cycles
        for node in nodes:
            node_idx = node_to_index[node]
            if d[max_length][node_idx] < d[max_length - 1][node_idx]:
                return "Negative cost cycle detected"

        end_idx = node_to_index.get(end, -1)
        if end_idx == -1 or d[max_length][end_idx] == float('inf'):
            return "No path exists between the given vertices"

        # reconstruct the path
        path = []
        current_node = end
        current_idx = node_to_index[current_node]
        k = max_length

        # find the first k where the cost changes
        while k > 0 and d[k][current_idx] == d[k - 1][current_idx]:
            k -= 1

        # reconstruct the path
        while current_node is not None and k >= 0:
            path.append(current_node)
            current_idx = node_to_index[current_node]
            current_node = predecessor[k][current_idx]
            k -= 1

        path.reverse()

        return (d[max_length][end_idx], path)

    def copy(self):
        new_graph = Graph()
        new_graph.__nodes = self.__nodes
        new_graph.__edges = self.__edges
        new_graph.__adj = copy.deepcopy(self.__adj)
        return new_graph

    def is_dag_and_topological_sort(self):
        visited = {}
        topological_order = []
        has_cycle = [False]  # Using a list to allow modification in nested function

        for node in self.__adj:
            visited[node] = 'unvisited'

        def dfs(u):
            if visited[u] == 'visiting':
                has_cycle[0] = True
                return
            if visited[u] == 'visited':
                return
            visited[u] = 'visiting'
            for v, _ in self.__adj[u]:
                dfs(v)
                if has_cycle[0]:
                    return
            visited[u] = 'visited'
            topological_order.append(u)

        for node in self.__adj:
            if visited[node] == 'unvisited':
                dfs(node)
                if has_cycle[0]:
                    break  # Early exit if cycle detected

        if has_cycle[0]:
            return (False, None)
        else:
            topological_order.reverse()
            return (True, topological_order)

    def highest_cost_path(self, start, end):
        if start not in self.__adj:
            raise ValueError(f"Start node {start} not in graph.")
        if end not in self.__adj:
            raise ValueError(f"End node {end} not in graph.")

        is_dag, topo_order = self.is_dag_and_topological_sort()
        if not is_dag:
            raise ValueError("Graph is not a DAG. Cannot compute highest cost path.")

        dist = {node: float('-inf') for node in self.__adj}
        pred = {node: None for node in self.__adj}
        dist[start] = 0

        for u in topo_order:
            if dist[u] == float('-inf'):
                continue
            for v, cost in self.__adj[u]:
                if dist[v] < dist[u] + cost:
                    dist[v] = dist[u] + cost
                    pred[v] = u

        if dist[end] == float('-inf'):
            return (None, [])

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = pred[current]
        path.reverse()

        return (dist[end], path)

