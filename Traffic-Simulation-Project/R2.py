import networkx as nx

# Initialize the graph
G = nx.Graph()

# Add edges between nodes with weights
G.add_edge(1, 0, length=0.4, traffic=100)  # Example traffic value
G.add_edge(1, 3, length=0.8, traffic=100)
G.add_edge(3, 4, length=0.7, traffic=100)
G.add_edge(4, 0, length=0.1, traffic=100)
G.add_edge(4, 2, length=1.0, traffic=100)

def calculate_specific_benefits(G, new_roads, f):
    benefits = {}
    for (u, v) in new_roads:
        if not G.has_edge(u, v):
            # Calculate the shortest path and its length before adding the new road
            shortest_path_length = nx.shortest_path_length(G, source=u, target=v, weight='length')
            direct_distance = f * shortest_path_length
            # Assume a default traffic volume for calculation purposes
            traffic = 100  # Simplification for this example
            benefit = (shortest_path_length - direct_distance) * traffic
            benefits[(u, v)] = benefit
    return benefits

def recommend_roads(G, proposed_roads, f, k):
    # Calculate initial benefits
    benefits = calculate_specific_benefits(G, proposed_roads, f)
    
    # Select the first road
    first_road = max(benefits, key=benefits.get)
    print(f"First recommended road to build: {first_road} with benefit {benefits[first_road]}")
    
    # Add the first road to the graph
    G.add_edge(*first_road, length=0.5, traffic=100)  # Example length and traffic
    
    # Recalculate benefits for the remaining roads
    remaining_roads = [road for road in proposed_roads if road != first_road]
    new_benefits = calculate_specific_benefits(G, remaining_roads, f)
    
    # Select the second road
    second_road = max(new_benefits, key=new_benefits.get)
    print(f"Second recommended road to build: {second_road} with benefit {new_benefits[second_road]}")

# Proposed new roads
proposed_roads = [(0, 2), (0, 3), (1, 2), (1, 4), (2, 3)]

# Execute the recommendation
recommend_roads(G, proposed_roads, f=0.6, k=2)