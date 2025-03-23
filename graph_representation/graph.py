import random
import heapq

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

