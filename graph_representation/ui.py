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
            g.remove_edge(u, v)
        elif choice == "4":
            g.print_graph()
        elif choice == "5":
            print("Node count:", g.get_node_count())
        elif choice == "6":
            print("Edge count:", g.get_edge_count())
        elif choice == "7":
            filename = input("Enter filename: ")
            g.write_to_file(filename)
        elif choice == "8":
            filename = input("Enter filename: ")
            g.read_from_file(filename)
        elif choice == "9":
            start = int(input("Enter start node: "))
            print("Dijkstra's result:", g.dijkstra(start))
        elif choice == "10":
            start = int(input("Enter start node: "))
            end = int(input("Enter end node: "))
            result = g.lowest_cost_walk(start, end)
            if isinstance(result, tuple):
                cost, path = result
                print(f"Lowest cost walk from {start} to {end}:")
                print(f"Cost: {cost}")
                print(f"Path: {' -> '.join(map(str, path))}")
            else:
                print(result)  # Prints error message
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()