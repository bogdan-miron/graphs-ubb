#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>
using namespace std;

const int UNVISITED = -1;

struct Connection {
    int from, to;
    Connection(int f, int t) : from(f), to(t) {}
};

class GraphAnalyzer {
    int vertexCount;
    vector<vector<int>> connections;
    int componentTotal = 0;

    void findComponents(int current, int discovery[], int earliest[], 
                       vector<Connection>& edgeStack, int parent[]) {
        static int timeCounter = 0;
        discovery[current] = earliest[current] = ++timeCounter;
        int childCount = 0;

        for (int neighbor : connections[current]) {
            if (discovery[neighbor] == UNVISITED) {
                childCount++;
                parent[neighbor] = current;
                edgeStack.emplace_back(current, neighbor);
                findComponents(neighbor, discovery, earliest, edgeStack, parent);

                earliest[current] = min(earliest[current], earliest[neighbor]);

                if ((discovery[current] == 1 && childCount > 1) || 
                    (discovery[current] > 1 && earliest[neighbor] >= discovery[current])) {
                    while (edgeStack.back().from != current || edgeStack.back().to != neighbor) {
                        cout << edgeStack.back().from << "-" << edgeStack.back().to << " ";
                        edgeStack.pop_back();
                    }
                    cout << edgeStack.back().from << "-" << edgeStack.back().to;
                    edgeStack.pop_back();
                    cout << "\n";
                    componentTotal++;
                }
            }
            else if (neighbor != parent[current]) {
                earliest[current] = min(earliest[current], discovery[neighbor]);
                if (discovery[neighbor] < discovery[current]) {
                    edgeStack.emplace_back(current, neighbor);
                }
            }
        }
    }

public:
    GraphAnalyzer(int vertices) : vertexCount(vertices), connections(vertices) {}

    void linkVertices(int a, int b) {
        connections[a].push_back(b);
    }

    void identifyComponents() {
        int* discovery = new int[vertexCount];
        int* earliest = new int[vertexCount];
        int* parent = new int[vertexCount];
        vector<Connection> edgeStack;

        fill(discovery, discovery + vertexCount, UNVISITED);
        fill(earliest, earliest + vertexCount, UNVISITED);
        fill(parent, parent + vertexCount, UNVISITED);

        for (int i = 0; i < vertexCount; i++) {
            if (discovery[i] == UNVISITED) {
                findComponents(i, discovery, earliest, edgeStack, parent);

                bool printed = false;
                while (!edgeStack.empty()) {
                    printed = true;
                    cout << edgeStack.back().from << "-" << edgeStack.back().to << " ";
                    edgeStack.pop_back();
                }
                if (printed) {
                    cout << "\n";
                    componentTotal++;
                }
            }
        }

        cout << "Total biconnected components found: " << componentTotal << "\n";
        delete[] discovery;
        delete[] earliest;
        delete[] parent;
    }
};

int main() {
    GraphAnalyzer network(12);
    
    network.linkVertices(0, 1);
    network.linkVertices(1, 0);
    network.linkVertices(1, 2);
    network.linkVertices(2, 1);
    network.linkVertices(1, 3);
    network.linkVertices(3, 1);
    network.linkVertices(2, 3);
    network.linkVertices(3, 2);
    network.linkVertices(2, 4);
    network.linkVertices(4, 2);
    network.linkVertices(3, 4);
    network.linkVertices(4, 3);
    network.linkVertices(1, 5);
    network.linkVertices(5, 1);
    network.linkVertices(0, 6);
    network.linkVertices(6, 0);
    network.linkVertices(5, 6);
    network.linkVertices(6, 5);
    network.linkVertices(5, 7);
    network.linkVertices(7, 5);
    network.linkVertices(5, 8);
    network.linkVertices(8, 5);
    network.linkVertices(7, 8);
    network.linkVertices(8, 7);
    network.linkVertices(8, 9);
    network.linkVertices(9, 8);
    network.linkVertices(10, 11);
    network.linkVertices(11, 10);

    network.identifyComponents();
    return 0;
}