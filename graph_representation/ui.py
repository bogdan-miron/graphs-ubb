from graph import Graph


def main():
    g = Graph()

    while True:
        print("\nGraph Operations:")
        print("1. Add node")
        print("2. Add edge")
        print("3. Remove edge")
        print("4. Print graph")
        print("5. Get node count")
        print("6. Get edge count")
        print("7. Write to file")
        print("8. Read from file")
        print("9. Run Dijkstra's Algorithm")
        print("10. Find lowest cost walk")
        print("11. Check if DAG and perform Topological Sort")
        print("12. Find Highest Cost Path (only for DAGs)")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            node = int(input("Enter node value: "))
            g.add_node(node)

        elif choice == "2":
            u = int(input("Enter first node: "))
            v = int(input("Enter second node: "))
            weight = int(input("Enter weight: "))
            g.add_edge(u, v, weight)

        elif choice == "3":
            u = int(input("Enter first node: "))
            v = int(input("Enter second node: "))
            try:
                g.remove_edge(u, v)
            except ValueError as e:
                print(e)

        elif choice == "4":
            g.print_graph()

        elif choice == "5":
            print("Node count:", g.get_node_count())

        elif choice == "6":
            print("Edge count:", g.get_edge_count())

        elif choice == "7":
            filename = input("Enter filename to write to: ")
            g.write_to_file(filename)
            print("Graph written to file.")

        elif choice == "8":
            filename = input("Enter filename to read from: ")
            g.read_from_file(filename)
            print("Graph loaded from file.")

        elif choice == "9":
            start = int(input("Enter start node: "))
            distances, prev = g.dijkstra(start)
            print("Shortest distances from node", start)
            for node in distances:
                print(f"{node}: {distances[node]}")

        elif choice == "10":
            start = int(input("Enter start node: "))
            end = int(input("Enter end node: "))
            result = g.lowest_cost_walk(start, end)
            print("Lowest cost walk from", start, "to", end, ":", result)

        elif choice == "11":
            is_dag, order = g.is_dag_and_topological_sort()
            if is_dag:
                print("Graph is a DAG. Topological Sort:", order)
            else:
                print("Graph is NOT a DAG. Topological sort not possible.")

        elif choice == "12":
            start = int(input("Enter start node: "))
            end = int(input("Enter end node: "))
            try:
                cost, path = g.highest_cost_path(start, end)
                if cost is None:
                    print(f"No path from {start} to {end}.")
                else:
                    print(f"Highest cost path from {start} to {end} has cost {cost}: {path}")
            except ValueError as e:
                print(e)

        elif choice == "0":
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
