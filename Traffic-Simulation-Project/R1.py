import networkx as nx
import random

def create_graph(N, p, L):
#   """Creates a connected graph with N nodes, edge probability p, and edge lengths in range L."""
    G = nx.Graph()
    # Add nodes
    G.add_nodes_from(range(N))
    # Try to add edges until the graph is connected
    while True:
        for i in range(N):
            for j in range(i+1, N):
                if random.random() < p and not G.has_edge(i, j):
                    G.add_edge(i, j, length=random.randint(L[0], L[1]))
        if nx.is_connected(G):
            break
        else:
            G.clear()
            G.add_nodes_from(range(N))
    return G

def simulate_traffic(G, T):
#   """Simulates T trips between random nodes and tracks traffic volume on each edge."""
    traffic_vol = nx.get_edge_attributes(G, 'traffic')
    if not traffic_vol:
        for edge in G.edges():
            G[edge[0]][edge[1]]['traffic'] = 0
    
    nodes_list = list(G.nodes())  # Convert nodes to a list
    for _ in range(T):
        start, end = random.sample(nodes_list, 2)  # Use the list of nodes here
        path = nx.shortest_path(G, source=start, target=end, weight='length')
        for i in range(len(path)-1):
            G[path[i]][path[i+1]]['traffic'] += 1

def calculate_benefits(G, f, k):
#    """Calculates and ranks potential new roads by their benefits."""
    benefits = []
    for u in G.nodes():
        for v in G.nodes():
            if u != v and not G.has_edge(u, v):
                # Calculate the shortest path and its length
                shortest_path_length = nx.shortest_path_length(G, source=u, target=v, weight='length')
                path = nx.shortest_path(G, source=u, target=v, weight='length')  # Calculate the shortest path
                direct_distance = f * shortest_path_length
                # Estimate traffic as the sum of traffic on the shortest current path
                traffic = sum(G[path[i]][path[i+1]]['traffic'] for i in range(len(path)-1))
                benefit = (shortest_path_length - direct_distance) * traffic
                benefits.append(((u, v), benefit))
    # Sort by benefit
    benefits.sort(key=lambda x: x[1], reverse=True)
    return benefits[:k]


def main():
    N = 10  # Simplified number of nodes for educational purposes
    p = 0.2  # Higher probability to ensure connectivity in a smaller graph
    L = (1, 10)  # Range of road lengths
    T = 100  # Number of trips to simulate
    k = 2  # Number of roads to build
    f = 0.6  # Shrinkage factor

    G = create_graph(N, p, L)
    simulate_traffic(G, T)
    new_roads = calculate_benefits(G, f, k)
    
    print("Recommended new roads to build (with benefits):")
    for road in new_roads:
        print(road)

main()
