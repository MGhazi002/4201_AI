# R3: Code from R1 adapted to R3, Project 1 group 3

import networkx as nx
import random

# Below values are for this pseudo code to code example. Also has default values
N = 60  # Number of nodes to create
p = 0.05  # Higher probability to ensure connectivity in a smaller graph
L = (5, 25)  # Range of possible road lengths
T = 100  # Number of trips to simulate
k = 3  # Number of roads to build
f = 0.6  # Shrinkage factor

# Create graph, add nodes and edges
def prepare_graph(N, p_initial, L):
    # Initialize graph
    simGraph = nx.Graph()

    # Create N nodes
    simGraph.add_nodes_from(range(N))

    # Initial probability for edge creation
    p = p_initial

    # Connect nodes based on the initial p value and increment p if not fully connected
    while not nx.is_connected(simGraph):
        for u in range(N):
            for v in range(u + 1, N):
                if random.random() < p and not simGraph.has_edge(u, v):
                    simGraph.add_edge(u, v, length=random.randint(*L), traffic_volume=0)
        p += 0.01  # Increment p as defined by project


    # Return the generated graph
    return simGraph

def cache_shortest_paths (graph):
    shortestPaths = {}
    for u in graph.nodes():
        for v in graph.nodes():
            if u != v:
                # Calculate the shortest path length using Dijkstra's algorithm
                # This also considers neighbors
                path = nx.dijkstra_path(graph, source=u, target=v, weight='length')
                shortestPaths[(u, v)] = path



    # Return the cached shortest paths
    return shortestPaths


def simulate_traffic(G, T, shortestPaths, total_seconds=36000):
    for second in range(1, total_seconds + 1):
        for _ in range(T):
            # Select a random start node and a different end node
            start_node = random.randint(0, len(G.nodes()) - 1)
            end_node = start_node
            while end_node == start_node:
                end_node = random.randint(0, len(G.nodes()) - 1)

            # If there's a precomputed path, use it
            if (start_node, end_node) in shortestPaths:
                # Turn the path into usable edges
                path_edges = zip(shortestPaths[(start_node, end_node)][:-1], shortestPaths[(start_node, end_node)][1:])
            else:
                # Directly compute the shortest path using Dijkstra's, shouldn't need this but just in case - safety
                path_edges = zip(nx.dijkstra_path(G, source=start_node, target=end_node, weight='length')[:-1],
                                 nx.dijkstra_path(G, source=start_node, target=end_node, weight='length')[1:])

            # Increment traffic volume for each edge in the path
            # To avoid mixups we include both notations of the edge
            for u, v in path_edges:
                if G.has_edge(u, v):
                    G[u][v]['traffic_volume'] += 1
                elif G.has_edge(v, u):  # For undirected graphs
                    G[v][u]['traffic_volume'] += 1


# Calculate benefit function
def calculate_benefit(X, Y, G, shortestPaths, f):
    # First get all the values we will need
    # Calculate the shortest path distance (spd) and direct distance (d) between X and Y
    if (X, Y) in shortestPaths:
        path_XY = shortestPaths[(X, Y)]
    else:
        path_XY = nx.dijkstra_path(G, source=X, target=Y, weight='length')

    # Get the sum of all lengths for all edges in the path
    spd_XY = sum(G[path_XY[i]][path_XY[i + 1]]['length'] for i in range(len(path_XY) - 1))

    # Distance is the shortest path * shrinkage factor
    d_XY = spd_XY * f

    # Directly calculate nt as the sum of trips (traffic_volume) between X and Y and Y to X
    # This calculation is from the pseudo: (nt(X, Y) + nt(Y, X))
    nt_XY = 0
    if (X, Y) in shortestPaths:
        nt_XY += sum(G[path_XY[i]][path_XY[i + 1]]['traffic_volume'] for i in range(len(path_XY) - 1))
    if (Y, X) in shortestPaths:  # Add the traffic from Y, X now according to instructions pseudo
        path_YX = shortestPaths[(Y, X)]
        nt_XY += sum(G[path_YX[i]][path_YX[i + 1]]['traffic_volume'] for i in range(len(path_YX) - 1))

    # Initialize benefit calculation
    benefit = (spd_XY - d_XY) * nt_XY

    # Calculate benefits from neighbors of X
    for neighbor in nx.all_neighbors(G, X):
        if neighbor != Y:

            # Distance between X and neighbor x
            spd_XNx = G[X][neighbor]['length']

            # Traffic on that edge
            nt_XNx = G[X][neighbor]['traffic_volume']

            # The direct paths distance between X's neighbor and Y

            # For Y to neighbor
            if (Y, neighbor) in shortestPaths:
                shortPath = shortestPaths[(Y, neighbor)]
            else:
                # Handle the missing path - Safety
                shortPath = nx.dijkstra_path(G, source=Y, target=neighbor, weight='length')

            spdShortPath = sum(G[shortPath[i]][shortPath[i + 1]]['length'] for i in range(len(shortPath) - 1))

            d_YNx = f * spdShortPath
            benefit += max(spd_XNx - d_XY - d_YNx, 0) * nt_XNx

    # Calculate benefits from neighbors of Y
    for neighbor in nx.all_neighbors(G, Y):
        if neighbor != X:
            # Distance between Y and neighbor y
            spd_YNy = G[Y][neighbor]['length']

            # Traffic on that edge
            nt_YNy = G[Y][neighbor]['traffic_volume']

            # The direct paths distance between Y's neighbor and X

            # Handle X to Y neighbor
            if (X, neighbor) in shortestPaths:
                shortPath = shortestPaths[(X, neighbor)]
            else:
                # Handle the missing path - Safety
                shortPath = nx.dijkstra_path(G, source=X, target=neighbor, weight='length')

            spdShortPath = sum(G[shortPath[i]][shortPath[i + 1]]['length'] for i in range(len(shortPath) - 1))

            d_XNy = f * spdShortPath

            benefit += max(spd_YNy - d_XY - d_XNy, 0) * nt_YNy

    # After adding the benefits a new road would add to all the neighbors, return
    return benefit


def main():
    # Create the graph
    simGraph = prepare_graph(N, p, L)

    # Cache the shortest paths
    cachedPaths = cache_shortest_paths(simGraph)

    # Simulate traffic
    simulate_traffic(simGraph, T, cachedPaths)

    # Create the benefit matrix
    benefitsMatrix = {}

    # A dictionary of all the roads we are going to build
    roadsToBuild = {}

    # We need to run the next logic for as many roads as we build
    i = 0
    while i < k:
        # Get the starting and finishing node of each path and calculate its benefit
        for (start, end), path in cachedPaths.items():
            if simGraph.has_edge(start, end):
                continue  # Dont consider roads that exist
            benefitsMatrix[(start, end)] = calculate_benefit(start, end, simGraph, cachedPaths, f)

        # Find the edge with the highest benefit
        max_benefit_edge = max(benefitsMatrix, key=benefitsMatrix.get)
        max_benefit = benefitsMatrix[max_benefit_edge]

        # Add this edge to roadsToBuild if not already present and it has a positive benefit
        if max_benefit_edge not in roadsToBuild and max_benefit > 0:
            # Retrieve the shortest path for the max benefit edge from cachedPaths
            shortest_path = cachedPaths[max_benefit_edge]

            # Calculate the total length of this path
            path_length = sum(
                simGraph[shortest_path[i]][shortest_path[i + 1]]['length'] for i in range(len(shortest_path) - 1))

            # Multiply the path length by f to get the new length
            new_length = path_length * f

            # Add the edge to simGraph with the calculated length
            simGraph.add_edge(max_benefit_edge[0], max_benefit_edge[1], length=new_length, traffic_volume=0)

            roadsToBuild[max_benefit_edge] = max_benefit

            # Recompute the shortest paths because the graph has changed
            cachedPaths = cache_shortest_paths(simGraph)

            # Clear the benefits matrix because we added a new edge
            benefitsMatrix.clear()

            i += 1  # Increment only if a road was added
        else:
            # If the highest benefit road is already in roadsToBuild or its benefit is not positive, break to avoid infinite loop
            break

    # Once we come out of this loop, then we have calculated all the roads to build and we can display them

    print("Recommended new roads to build:")
    for (start, end), benefit in roadsToBuild.items():
        print(f"Road from {start} to {end}: Benefit = {benefit}")

main()
