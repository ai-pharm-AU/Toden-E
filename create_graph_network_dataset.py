import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def generate_weighted_graph_with_clusters(k, nodes_per_cluster, intra_weight_range, inter_weight_range):
    G = nx.Graph()
    
    # Track the last node id in the graph to ensure unique ids across clusters
    last_node_id = 0
    
    # Generate clusters
    for _ in range(k):
        # Generate nodes for this cluster
        nodes = range(last_node_id, last_node_id + nodes_per_cluster)
        last_node_id += nodes_per_cluster
        
        # Add edges within the cluster
        for i in nodes:
            for j in nodes:
                if i < j:  # Avoid self-loops and duplicate edges
                    weight = np.random.uniform(*intra_weight_range)
                    G.add_edge(i, j, weight=weight)
    
    # Connect clusters with some edges
    for i in range(k - 1):
        for j in range(i + 1, k):
            # Pick a random node from each cluster to connect
            node_i = np.random.choice(range(i * nodes_per_cluster, (i + 1) * nodes_per_cluster))
            node_j = np.random.choice(range(j * nodes_per_cluster, (j + 1) * nodes_per_cluster))
            
            # Add an inter-cluster edge with lower weight
            weight = np.random.uniform(*inter_weight_range)
            G.add_edge(node_i, node_j, weight=weight)
    
    return G

# Example usage
k = 3  # Number of clusters
nodes_per_cluster = 10  # Nodes per cluster
intra_weight_range = (5, 8)  # Weight range for edges within a cluster
inter_weight_range = (1, 5)  # Weight range for edges between clusters

# Generate the graph
G = generate_weighted_graph_with_clusters(k, nodes_per_cluster, intra_weight_range, inter_weight_range)

# Visualize the graph
pos = nx.spring_layout(G)  # Compute layout
edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())
plt.savefig("network_dataset.png", format="PNG")
nx.draw_networkx(G, pos, edgelist=edges, edge_color=weights, width=4.0, edge_cmap=plt.cm.Blues)
plt.show()
