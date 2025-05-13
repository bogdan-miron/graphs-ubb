#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <climits>

using namespace std;

/*
Write a program that, given a graph with costs, having no negative cost cycles, and a pair of vertices, finds the number of distinct walks of minimum cost between the given vertices.
*/

struct Edge {
    int u, v, cost;
};

const long long INF = LLONG_MAX;

int main() {
    int n, m;
    cin >> n >> m;

    vector<Edge> edges;
    for (int i = 0; i < m; ++i) {
        int u, v, cost;
        cin >> u >> v >> cost;
        edges.push_back({u, v, cost});
    }

    int source, dest;
    cin >> source >> dest;

    vector<long long> dist(n, INF);
    dist[source] = 0;

    for (int i = 0; i < n - 1; ++i) {
        bool updated = false;
        for (const Edge& e : edges) {
            if (dist[e.u] != INF && dist[e.u] + e.cost < dist[e.v]) {
                dist[e.v] = dist[e.u] + e.cost;
                updated = true;
            }
        }
        if (!updated) break;
    }

    if (dist[dest] == INF) {
        cout << 0 << endl;
        return 0;
    }

    vector<vector<int>> s_adj(n);
    vector<vector<int>> reversed_s_adj(n);

    for (const Edge& e : edges) {
        if (dist[e.u] != INF && dist[e.u] + e.cost == dist[e.v]) {
            s_adj[e.u].push_back(e.v);
            reversed_s_adj[e.v].push_back(e.u);
        }
    }

    vector<bool> reachable_from_source(n, false);
    queue<int> q;
    q.push(source);
    reachable_from_source[source] = true;

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : s_adj[u]) {
            if (!reachable_from_source[v]) {
                reachable_from_source[v] = true;
                q.push(v);
            }
        }
    }

    vector<bool> can_reach_dest(n, false);
    queue<int> q_rev;
    q_rev.push(dest);
    can_reach_dest[dest] = true;

    while (!q_rev.empty()) {
        int u = q_rev.front();
        q_rev.pop();
        for (int v : reversed_s_adj[u]) {
            if (!can_reach_dest[v]) {
                can_reach_dest[v] = true;
                q_rev.push(v);
            }
        }
    }

    for (const Edge& e : edges) {
        if (e.u == e.v) {
            if (dist[e.u] != INF && dist[e.u] + e.cost == dist[e.v]) {
                if (reachable_from_source[e.u] && can_reach_dest[e.u]) {
                    cout << -1 << endl;
                    return 0;
                }
            }
        }
    }

    vector<bool> visited(n, false);
    stack<int> order;

    for (int u = 0; u < n; ++u) {
        if (dist[u] != INF && !visited[u]) {
            stack<pair<int, bool>> dfs_stack;
            dfs_stack.push({u, false});
            while (!dfs_stack.empty()) {
                auto [current, processed] = dfs_stack.top();
                dfs_stack.pop();
                if (processed) {
                    order.push(current);
                    continue;
                }
                if (visited[current]) continue;
                visited[current] = true;
                dfs_stack.push({current, true});
                for (int v : s_adj[current]) {
                    if (!visited[v]) {
                        dfs_stack.push({v, false});
                    }
                }
            }
        }
    }

    visited.assign(n, false);
    bool has_infinite = false;

    while (!order.empty()) {
        int u = order.top();
        order.pop();
        if (!visited[u]) {
            stack<int> component_stack;
            component_stack.push(u);
            visited[u] = true;
            vector<int> component;
            component.push_back(u);

            while (!component_stack.empty()) {
                int current = component_stack.top();
                component_stack.pop();
                for (int v : reversed_s_adj[current]) {
                    if (!visited[v]) {
                        visited[v] = true;
                        component_stack.push(v);
                        component.push_back(v);
                    }
                }
            }

            if (component.size() >= 2) {
                for (int node : component) {
                    if (reachable_from_source[node] && can_reach_dest[node]) {
                        has_infinite = true;
                        break;
                    }
                }
            }
        }
        if (has_infinite) break;
    }

    if (has_infinite) {
        cout << -1 << endl;
        return 0;
    }

    vector<int> filtered_nodes;
    vector<vector<int>> filtered_adj(n);
    vector<int> in_degree(n, 0);

    for (int u = 0; u < n; ++u) {
        if (reachable_from_source[u] && can_reach_dest[u]) {
            filtered_nodes.push_back(u);
        }
    }

    for (const Edge& e : edges) {
        if (dist[e.u] != INF && dist[e.u] + e.cost == dist[e.v]) {
            int u = e.u, v = e.v;
            if (reachable_from_source[u] && can_reach_dest[u] && reachable_from_source[v] && can_reach_dest[v]) {
                filtered_adj[u].push_back(v);
                in_degree[v]++;
            }
        }
    }

    queue<int> kahn_q;
    vector<int> topo_order;

    for (int u : filtered_nodes) {
        if (in_degree[u] == 0) {
            kahn_q.push(u);
        }
    }

    while (!kahn_q.empty()) {
        int u = kahn_q.front();
        kahn_q.pop();
        topo_order.push_back(u);
        for (int v : filtered_adj[u]) {
            in_degree[v]--;
            if (in_degree[v] == 0) {
                kahn_q.push(v);
            }
        }
    }

    vector<long long> dp(n, 0);
    dp[source] = 1;

    for (int u : topo_order) {
        for (int v : filtered_adj[u]) {
            dp[v] += dp[u];
        }
    }

    cout << dp[dest] << endl;

    return 0;
}