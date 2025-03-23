from graph import *

g = Graph()
# g.read_from_file('graph1k.txt')

g.add_edge(3, 2, 50)
g.add_node(70)
g.add_edge(2, 3, 90)
g.remove_edge(3, 2)
g.add_edge(4, 7, 60)
g.add_edge(1, 2, 40)

g.print_graph()
print(g.get_node_count())
print(g.get_edge_count())

g.write_to_file('output_file')

g.read_from_file('graph1k.txt')
g.print_graph()

# g.generate_random_graph(100, 200)
# g.print_graph()

# print(g.out_degree(3))
print(g.dijkstra(0))