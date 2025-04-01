#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

vector<bool> visited;

void dfs(int v, vector<vector<int>> const& adj, vector<int> &output) {
    visited[v] = true;
    for (auto u : adj[v])
        if (!visited[u])
            dfs(u, adj, output);
    output.push_back(v);
}

void strongly_connected_components(vector<vector<int>> const& adj,
                                  vector<vector<int>> &components,
                                  vector<vector<int>> &adj_cond) {
    int n = adj.size();
    components.clear(), adj_cond.clear();

    vector<int> order;
    visited.assign(n, false);

    for (int i = 0; i < n; i++)
        if (!visited[i])
            dfs(i, adj, order);

    vector<vector<int>> adj_rev(n);
    for (int v = 0; v < n; v++)
        for (int u : adj[v])
            adj_rev[u].push_back(v);

    visited.assign(n, false);
    reverse(order.begin(), order.end());

    vector<int> roots(n, 0);

    for (auto v : order)
        if (!visited[v]) {
            vector<int> component;
            dfs(v, adj_rev, component);
            components.push_back(component);
            int root = *min_element(begin(component), end(component));
            for (auto u : component)
                roots[u] = root;
        }

    adj_cond.assign(n, {});
    for (int v = 0; v < n; v++)
        for (auto u : adj[v])
            if (roots[v] != roots[u])
                adj_cond[roots[v]].push_back(roots[u]);
}

int main() {
    int n = 8;
    vector<vector<int>> adj(n);
    
    adj[0] = {1};
    adj[1] = {2, 4, 5};
    adj[2] = {3, 6};
    adj[3] = {2, 7};
    adj[4] = {0, 5};
    adj[5] = {6};
    adj[6] = {5, 7};
    adj[7] = {7};
    
    vector<vector<int>> components;
    vector<vector<int>> adj_cond;
    
    strongly_connected_components(adj, components, adj_cond);
    
    cout << "Strongly Connected Components:\n";
    for (size_t i = 0; i < components.size(); i++) {
        cout << "Component " << i + 1 << ": ";
        for (int v : components[i]) {
            cout << v << " ";
        }
        cout << "\n";
    }
    
    cout << "\nCondensation Graph Adjacency List:\n";
    for (size_t v = 0; v < adj_cond.size(); v++) {
        if (!adj_cond[v].empty()) {
            cout << v << ": ";
            for (int u : adj_cond[v]) {
                cout << u << " ";
            }
            cout << "\n";
        }
    }
    
    return 0;
}