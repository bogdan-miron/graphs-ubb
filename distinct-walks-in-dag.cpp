#include <iostream>
#include <vector>
#include <queue>

using namespace std;

/*
Write a program that, given a graph that has no cycles (a directed acyclic graph, DAG) and a pair of vertices, finds the number of distinct walks between the given vertices.
*/

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cout << "Enter the number of vertices and edges: ";
    cin >> n >> m;

    // compute the in-degs
    vector<vector<int>> graph(n);
    vector<int> indegree(n, 0);
    cout << "Enter the directed edges (u v means an edge from u to v): \n";
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
        indegree[v]++;
    }

    int start, target;
    cout << "Enter the start and target vertices: ";
    cin >> start >> target;

    // top sort
    vector<int> topo_order;
    queue<int> q;
    for (int i = 0; i < n; i++) {
        if (indegree[i] == 0) {
            q.push(i);
        }
    }

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        topo_order.push_back(u);
        for (int v : graph[u]) {
            if (--indegree[v] == 0) {
                q.push(v);
            }
        }
    }
    
    if (topo_order.size() != n) {
        cerr << "Error: The graph is not a DAG.\n";
        return 1;
    }
    
    vector<long long> dp(n, 0);
    dp[start] = 1;
    
    for (int u : topo_order) {
        for (int v : graph[u]) {
            dp[v] += dp[u];
        }
    }
    cout << "Number of distinct walks from " << start << " to " << target << " is: " << dp[target] << "\n";
    
    return 0;
}
