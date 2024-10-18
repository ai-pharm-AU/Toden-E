import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import community as community_louvain
import random
import hdbscan
import time
import itertools
import seaborn as sns
import argparse
import matplotlib.cm as cm
import matplotlib.patches as mpatches

from transformers import pipeline, GPT2Tokenizer, GPT2LMHeadModel, GPT2TokenizerFast
from scipy.stats import ttest_ind
from consensusclustering import ConsensusClustering
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
from collections import Counter, deque, defaultdict
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics import adjusted_rand_score,  normalized_mutual_info_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.manifold import TSNE   
from networkx.algorithms.community import girvan_newman
from sklearn.cluster import SpectralClustering
from matplotlib.font_manager import FontProperties


from communities_detection import plot_communities_w_names
from PAGER.PAGER import PAGER

# font.set_weight('bold')

PAGER = PAGER()
VERI_GRAGH_PATH = 'go_metadata/2024_graph_w_verification.graphml'
WHOLE_GRAPH_PATH = 'go_metadata/2024_GO_wholegraph.graphml'
BP_GRAPH_PATH = 'go_metadata/2024_biological_process_graph_w_verification.graphml'
META_DATA_PATH = 'go_metadata/filterpaginf2024.csv'   # 'pager_3_all_metadata.csv'


class GraphAnalysis:
    def __init__(self, G, root):
        self.G = G
        self.root = root
        self.parent = {root: None}  # Parent of each node
        self.level = {root: 0}  # Level of each node
        self._bfs()  # Perform BFS to populate parent and level information
        
    def _bfs(self):
        """Perform BFS to populate parent and level information."""
        queue = deque([self.root])
        while queue:
            current_node = queue.popleft()
            for neighbor in self.G.successors(current_node):
                if neighbor not in self.parent:  # If neighbor has not been visited
                    self.parent[neighbor] = current_node
                    self.level[neighbor] = self.level[current_node] + 1
                    queue.append(neighbor)
    
    def check_same_parent(self, node1, node2):
        """Check if two nodes have the same parent and determine their level."""
        if node1 not in self.parent or node2 not in self.parent:
            return None, None
        
        have_same_parent = self.parent[node1] == self.parent[node2]
        if have_same_parent:
            return have_same_parent, self.level[node1]  # Assuming they are at the same level
        else:
            return have_same_parent, (self.level[node1], self.level[node2])
        
    def find_lowest_level_nodes_and_common_parent(self, nodes):

        lowest_level = min(self.level[node] for node in nodes if node in self.level)
        highest_level = max(self.level[node] for node in nodes if node in self.level)
        lowest_level_nodes = [ node for node in nodes if self.level[node] == lowest_level]

        if len(lowest_level_nodes) == 1:
            common_parent= lowest_level_nodes[0]
        else:
            # Find the common parent (LCA) of the lowest level nodes
            common_parent = nx.lowest_common_ancestor(self.G, lowest_level_nodes[0], lowest_level_nodes[1])
            for node in lowest_level_nodes[2:]:
                common_parent = nx.lowest_common_ancestor(self.G, common_parent, node)
        
        return lowest_level_nodes, common_parent, highest_level
    
    def create_subgraph_from_nodes(self, nodes):
        return self.G.subgraph(nodes)

    def add_intermediate_nodes_to_keep_connected(self, nodes_list):
        lowest_level_nodes, common_parent, highest_level = self.find_lowest_level_nodes_and_common_parent(nodes_list)
        # Set to keep track of all nodes that need to be included in the subgraph
        # print(f"The common parent is {common_parent}, the highest level is {highest_level}, lowest_level_nodes are {lowest_level_nodes}")
        # candidates_list = [common_parent] + nodes_list
        candidates_list = nodes_list
        all_nodes_included = set(candidates_list)
        
        # Find the shortest paths between all pairs in the list
        for i, node_start in enumerate(candidates_list):
            for node_end in nodes_list[i+1:]:
                if nx.has_path(self.G, node_start, node_end):
                    shortest_path = nx.shortest_path(self.G, source=node_start, target=node_end)
                    # Add the nodes in the shortest path to the set
                    all_nodes_included.update(shortest_path)
        
        return all_nodes_included

    
    def find_descendants_to_level(self, start_node, highest_level):
        # Calculate the depth of each node from start_node
        depths = nx.single_source_shortest_path_length(self.G, start_node)
        
        # Filter nodes by depth, including only those at or below the specified highest level
        descendants = {node for node, depth in depths.items() if depth <= highest_level}
        
        return descendants

    


def tsne_2d_plot(pags_embeddings, save_name='test'):
    print(len(pags_embeddings))
    tsne = TSNE(n_components=2, perplexity=5,  random_state=323)
    embeddings_2d = tsne.fit_transform(pags_embeddings)
    plt.figure(figsize=(10, 8))
    plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])
    plt.title("2D Visualization of Embeddings")
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.savefig(f"{save_name}.jpg")

# from communities_detection import run_eval
def evaluate_algorithm(true_labels, pred_labels):
    ari = adjusted_rand_score(true_labels, pred_labels)
    nmi = normalized_mutual_info_score(true_labels, pred_labels)
    return ari, nmi

def run_eval(algorithm, G, true_labels, is_plot=False, num_clusters = 2, save_results=False):
    
    if algorithm == 'louvain':
        partition = community_louvain.best_partition(G)
        title = "Louvain Method"
    elif algorithm == 'girvan_newman':
        gn_comm = next(girvan_newman(G))
        partition = {node: i for i, comm in enumerate(gn_comm) for node in comm}
        title = "Girvan-Newman Algorithm"
    elif algorithm == 'spectral_clustering':
        adj_matrix = nx.to_numpy_array(G)
        sc = SpectralClustering(n_clusters=num_clusters, affinity='precomputed', n_init=100, random_state=42)
        sc.fit(adj_matrix)
        nodes = list(G.nodes())
        partition = {nodes[i]: sc.labels_[i] for i in range(len(nodes))}
        title = "Spectral Clustering"
    elif algorithm == "agglomerative_clustering":
        adj_matrix = nx.to_numpy_array(G)
        ac = AgglomerativeClustering(n_clusters=num_clusters, affinity='euclidean', linkage='ward')
        ac.fit(adj_matrix)
        nodes = list(G.nodes())
        partition = {nodes[i]: ac.labels_[i] for i in range(len(nodes))}
        title = "Agglomerative Clustering"

    else:
        raise ValueError("Invalid algorithm")
    
    # print(partition)
    
    labels = [partition[node] for node in G.nodes()]
    ari, nmi = evaluate_algorithm(true_labels, labels)

    if is_plot:
        print(f"{title}: ARI = {ari}, NMI = {nmi}")
        # plot_communities(G, partition, title)
        plot_communities_w_names(G, partition, f"{algorithm}_ari_{ari:0.2f}_nmi_{nmi:0.2f}")

    return ari, nmi



def plot_communities(G, partition, title=""):
    cmap = plt.colormaps.get_cmap('viridis')
    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                           cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.title(title)
    plt.axis('off')
    plt.savefig(f"{title.replace(' ', '_')}_results.jpg")
    plt.close()  # Close the plot to avoid displaying it inline if not desired


def talbe_2_graph(file_path = 'topdown2018.txt'):

    G = nx.DiGraph()

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):  # Enumerate to keep track of line numbers
            try:
                parent, child = line.strip().split(' ')
                if (parent, child) not in G.edges():  # Check to avoid adding duplicate edges
                    G.add_edge(parent, child)
            except ValueError:
                # Handle the error (e.g., wrong number of values to unpack)
                print(f"Skipping malformed line: {line.strip()}")
            except Exception as e:
                # Handle other possible errors
                print(f"An error occurred: {e}. Skipping line: {line.strip()}")

    nx.write_graphml(G, "graph.graphml")


def node_belongs_to_tree(graph, root, target):
    """
    Check if the target node belongs to the tree rooted at the given root node.
    
    Parameters:
    - graph: A networkx Graph representing the tree.
    - root: The root node of the tree.
    - target: The node to check for its presence in the tree.
    
    Returns:
    - True if the target node belongs to the tree rooted at the given root node, False otherwise.
    """
    # Use DFS to find if the target node is reachable from the root
    reachable_nodes = list(nx.dfs_preorder_nodes(graph, source=root))
    return target in reachable_nodes


def find_validate_set(graph_path = 'subgraph_for_test.graphml'):
    meta_data_path = 'pager_3_all_metadata.csv'
    df = pd.read_csv(meta_data_path)
    print(df.head())

    # Path to your GraphML file
    G = nx.read_graphml(graph_path)
    list_of_nodes = list(G.nodes())

    column_to_check = 'NAME'

    # Construct a regular expression pattern to match any of the elements in name_parts
    pattern = '|'.join(list_of_nodes)

    # Find rows where the name contains any of the substrings in name_parts
    matching_rows = df[df[column_to_check].str.contains(pattern, case=False, na=False)]
    desc_list = matching_rows['DESCRIPTION'].tolist()

    return matching_rows, desc_list



def clean_data():

    df = pd.read_csv(META_DATA_PATH)
    print(df.head())
    three_parts = ['biological_process', 'molecular_function', 'cellular_component']

    for part in three_parts:
        # Filter the DataFrame for rows where 'NAME' contains the current part
        filtered_df = df[df['NAME'].str.contains(part)]
    
        # Apply the lambda function to the filtered DataFrame and convert to list
        go_key_list = filtered_df['NAME'].apply(lambda x: x.split(' ')[0]).tolist()
        
        table_2_graph_with_verfication('topdown2024.txt', go_key_list, part)

def get_embedding(desc):
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return embedder.encode(desc)

def table_2_graph(file_path='topdown2024.txt'):

    G = nx.DiGraph()

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            try:
                parent, child = line.strip().split('\t')
                G.add_edge(parent, child)

            except ValueError:
                # Handle the error (e.g., wrong number of values to unpack)
                print(f"Skipping malformed line {line_number}: {line.strip()}")
            except Exception as e:
                # Handle other possible errors
                print(f"Error on line {line_number}: {e}. Skipping line: {line.strip()}")

    nx.write_graphml(G, WHOLE_GRAPH_PATH)



def table_2_graph_with_verfication(file_path, valid_nodes, part_name):
    G = nx.DiGraph()

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            try:
                parent, child = line.strip().split('\t')
                # Verify both nodes are in the valid_nodes list before adding
                if parent in valid_nodes and child in valid_nodes:
                    if (parent, child) not in G.edges():  # Check to avoid adding duplicate edges
                        print(f'adding nodes {parent} and {child}')
                        G.add_edge(parent, child)
                else:
                    print(f"Skipping line {line_number}: Node not in valid_nodes list.")
            except ValueError:
                # Handle the error (e.g., wrong number of values to unpack)
                print(f"Skipping malformed line {line_number}: {line.strip()}")
            except Exception as e:
                # Handle other possible errors
                print(f"Error on line {line_number}: {e}. Skipping line: {line.strip()}")

    nx.write_graphml(G, f"2024_{part_name}_graph_w_verification.graphml")


def extract_groundtrue_dataset(graph_path = 'subgraph_GO:0140096_GO:0051239.graphml'):

    G = nx.read_graphml(graph_path)
    labels = {}
    for node in nx.descendants(G, 'GO:0140096'):
        labels['GO:0140096'] = 0
        labels[node] = 0
    for node in nx.descendants(G, 'GO:0051239'):
        labels['GO:0051239'] = 1
        labels[node] = 1
    return G, [labels.get(node, -1) for node in sorted(G.nodes())], labels
      
def graph_based_clustering_eval():
    G, true_labels = extract_groundtrue_dataset()
    print(f"The number of nodes: {len(G.nodes())}")
    G_undirected = G.to_undirected()
    for algorithm in ['girvan_newman',  'louvain', 'spectral_clustering']: #'girvan_newman',  'louvain', 
        ari, nmi = run_eval(algorithm, G_undirected, true_labels, is_plot=True)
        
        print(f"{algorithm}: ARI: {ari}, NMI: {nmi}")


def find_subtree_with_criteria(G, root, upper_num=100, lower_num=50):
    # Perform a BFS to find nodes at each level and compute subtree sizes
    queue = [(root, 0)]  # Each element is a tuple (node, level)
    level_nodes = {}  # {level: [nodes]}
    subtree_sizes = {}  # {node: size_of_subtree}

    while queue:
        current_node, level = queue.pop(0)
        # Compute the size of the subtree rooted at `current_node`
        subtree_size = len(nx.descendants(G, current_node)) + 1  # Including the node itself
        subtree_sizes[current_node] = subtree_size

        if level not in level_nodes:
            level_nodes[level] = []
        level_nodes[level].append(current_node)

        queue.extend((neighbor, level + 1) for neighbor in G.successors(current_node))
    # Filter for nodes that meet the minimum size requirement
    eligible_nodes = {node: size for node, size in subtree_sizes.items() if size <= upper_num and size > lower_num}

    # Find the subtree rooted at the lowest level that meets the size criterion
    for level in sorted(level_nodes.keys()):
        for node in level_nodes[level]:
            if node in eligible_nodes:
                return node, eligible_nodes[node]  # Return the node and the size of its subtree

    return None, None  # If no such subtree is found


  
def filtered_outdegree_in_G(graph_path= '2024_biological_process_graph_w_verification.graphml', lower_bound=10, upper_bound= 100):
    G = nx.read_graphml(graph_path)
    roots = [node for node, in_degree in G.in_degree() if in_degree == 0]
    # node_out_degrees = G.out_degree()
    filtered_list = []

    node_out_degrees = {}
    for root in roots:
        root_out_degree = G.out_degree(root)
        node_out_degrees[root] = root_out_degree
        if root_out_degree <= upper_bound and root_out_degree >= lower_bound:
            filtered_list.append(root)
            print(f'{root}: {root_out_degree}')
    
    # ranked_nodes = sorted(node_out_degrees, key=lambda x: x[1], reverse=False)
    return filtered_list

def extract_subgraph_given_nodes(G, nodes_to_extract):

    # GO:0140096 and GO:0051239
    edges_to_add = []  # A list to store the subtree graphs

    for node in nodes_to_extract:
        # Find direct children of the node
        children = list(G.successors(node))
        
        # Create edges from the node to its direct children
        for child in children:
            edges_to_add.append((node, child))
        
        # Create a new graph for the subtree
    subgraph = nx.DiGraph(edges_to_add)
    
    nx.write_graphml(subgraph, f"subgraph_{'_'.join(nodes_to_extract)}.graphml")

    
def find_edges_among_neighbors(G, target_vertex):
    """
    Finds the edges among the neighbors of a given target vertex, excluding edges to the target vertex itself.
    
    Parameters:
    - G: A NetworkX graph.
    - target_vertex: The vertex for which neighbors' connections are analyzed.
    
    Returns:
    - edges: A set of tuples where each tuple represents an edge between two neighbors of the target vertex.
    """
    # Find neighbors of the target vertex
    neighbors = set(nx.neighbors(G, target_vertex))
    print(f"the neighbors of the vertex {target_vertex}: {neighbors}")
    
    # Initialize an empty set to store edges among neighbors
    edges_among_neighbors = set()
    
    # Check for edges among the neighbors
    for neighbor in neighbors:
        # For each neighbor, find its neighbors and check if they are also neighbors of the target vertex
        for potential_neighbor_edge in nx.neighbors(G, neighbor):
            if potential_neighbor_edge in neighbors and neighbor < potential_neighbor_edge:
                # Add the edge if both nodes are neighbors of the target vertex (and avoid adding an edge twice)
                edges_among_neighbors.add((neighbor, potential_neighbor_edge))
    
    return edges_among_neighbors, neighbors


def read_m_type_file(txt_path="go_metadata/m_type_biological_process.txt"):
    return pd.read_csv(txt_path, sep='\t')

def convert_weighted_graph_2_non_weighted(G_weighted):
    # Create an empty non-weighted graph
    G_non_weighted = nx.Graph()

    # Iterate through the weighted edges and add them based on their weight probability
    for u, v, data in G_weighted.edges(data=True):
        if np.random.rand() <= data['weight']:  # data['weight'] is treated as the probability
            G_non_weighted.add_edge(u, v)

    return G_non_weighted





def find_node_levels(G, root, nodes):
    level = {root: 0}
    queue = deque([root])
    result = {}
    
    while queue:
        current_node = queue.popleft()
        for neighbor in G.neighbors(current_node):
            if neighbor not in level:  # If neighbor hasn't been assigned a level
                level[neighbor] = level[current_node] + 1
                queue.append(neighbor)
    
    # For each node in the list, save its level in the result dictionary
    for node in nodes:
        result[node] = level.get(node, None)  # Use None for nodes not found in the graph
    
    return result

def have_same_parent(G, node1, node2):
    # Initialize a dictionary to hold the parent of each node
    parents = {}

    # Populate the parents dictionary by iterating over the edges
    for parent, child in G.edges():
        parents[child] = parent

    # Check if both nodes are in the parents dictionary and have the same parent
    if node1 in parents and node2 in parents and parents[node1] == parents[node2]:
        return True
    else:
        return False
    
def all_have_different_parent(G, nodes):
    # Initialize a dictionary to hold the parent of each node
    parents = {}

    # Populate the parents dictionary by iterating over the edges
    for parent, child in G.edges():
        parents[child] = parent

    # Use a set to keep track of unique parents of the nodes in the list
    unique_parents = set(parents[node] for node in nodes if node in parents)

    # If the set of unique parents has exactly one element, all nodes have the same parent
    return len(unique_parents) == len(nodes)

def filter_exp_dataset(target_graph_path='2024_biological_process_graph_w_verification.graphml', taget_graph_root = 'GO:0008150', num_of_groups = 2):
    '''
    biological_process: 'GO:0008150'
    molecular_function: 'GO:0003674'
    cellular_component: 'GO:0005575'
    '''
    
    G_GOA = nx.read_graphml(WHOLE_GRAPH_PATH)
    filtered_roots = filtered_outdegree_in_G(target_graph_path, lower_bound=5, upper_bound= 10)
    node_2_level_dict = find_node_levels(G_GOA, taget_graph_root, filtered_roots)

    level_2_nodes_dict = {}
    exp_candidates = []

    for key, value in node_2_level_dict.items():
        if value not in level_2_nodes_dict:
            level_2_nodes_dict[value] = [key]
        else:
            level_2_nodes_dict[value].append(key)

    for level, nodes in level_2_nodes_dict.items():
        group_list = list(itertools.combinations(nodes, num_of_groups))
        for nodes in group_list:
            if all_have_different_parent(G_GOA, nodes):
                exp_candidates.append(nodes)
            else:
                print(f"The {nodes} share the same parent!!")

    print(len(exp_candidates))
    return exp_candidates


def gen_gt_labels(graph_path, roots_list):

    G = nx.read_graphml(graph_path)
    labels_dict = {}
    all_gt_nodes = []

    # Assign labels starting from 0 for each root and its neighbors
    for label, root in enumerate(roots_list):
        labels_dict[root] = label
        all_gt_nodes.append(root)
        for node in nx.neighbors(G, root):
            # Avoid re-labeling a node if it has already been labeled
            if node not in labels_dict:
                labels_dict[node] = label
                all_gt_nodes.append(node)

    # Ensure uniqueness of nodes
    all_gt_nodes = list(set(all_gt_nodes))
    
    # Generate labels for all nodes, sorted to ensure consistent order
    labels = [labels_dict.get(node, -1) for node in sorted(all_gt_nodes)]

    return all_gt_nodes, labels, labels_dict


def find_gt_valid_set(valid_nodes):
    
    df = pd.read_csv(META_DATA_PATH)
    column_to_check = 'NAME'
    pattern = '|'.join(valid_nodes)
    matching_rows = df[df[column_to_check].str.contains(pattern, case=False, na=False)]
    desc_list = matching_rows['DESCRIPTION'].tolist()

    return matching_rows, desc_list


def get_normalized_embeddings(df, opt='desc'):
    """Extract and normalize embeddings."""
    df['NAMEDESC'] = df['NAME'].apply(lambda x: ' '.join(x.split(' ')[2:]) if len(x.split(' ')) > 2 else 'none')
     
    if opt == 'name':
        df['EMBEDDING'] = df['NAMEDESC'].apply(get_embedding)
    elif opt == 'desc':
        df['EMBEDDING'] = df['DESCRIPTION'].apply(get_embedding)
    elif opt == 'name+desc':
        df['EMBEDDING'] = (df['NAMEDESC'] + ' ' + df['DESCRIPTION']).apply(get_embedding)
    else:
        print(f"The option {opt} is invalid..")

    embeddings = np.stack(df['EMBEDDING'].values)
    return embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

def perform_clustering(algo, name, embeddings, true_labels):
    """Fit clustering algorithm and print ARI score."""
    start_time = time.time()
    predictions = algo.fit_predict(embeddings)
    ari_score = adjusted_rand_score(true_labels, predictions)
    end_time = time.time()
    duration = end_time - start_time
    print(f"ARI Score {name}: {ari_score}, time spent: {duration}")

    return ari_score, duration

def pred_clusters(algo, name, embeddings):
    start_time = time.time()
    predictions = algo.fit_predict(embeddings)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Algo {name} time spent: {duration}")

    return predictions, duration


def eval_m_type_relation_clustering(graph_path, roots_list, num_clusters=2):

    df = read_m_type_file("go_metadata/m_type_biological_process.txt")
    valid_nodes, true_labels, true_labels_dict = gen_gt_labels(graph_path, roots_list)
    print(len(valid_nodes))
    nodes_dict = {f"Root{label}": root for label, root in enumerate(roots_list)}
    filtered_df = df[df['GS_A_ID'].isin(valid_nodes) & df['GS_B_ID'].isin(valid_nodes)]

    G = nx.Graph()
    for _, row in filtered_df.iterrows():
        G.add_edge(row['GS_A_ID'], row['GS_B_ID'], weight=row['SIMILARITY'])

    true_labels = [true_labels_dict[node] for node in G.nodes()]

    results = []

    for algorithm in [ 'louvain', 'spectral_clustering', 'agglomerative_clustering']:  #'girvan_newman',  'louvain', 'girvan_newman', 
        ari, nmi = run_eval(algorithm, G, true_labels, is_plot=False, num_clusters=num_clusters)
        result_dict = {'Algorithm': algorithm, 'ARI Score': ari, 'NMI': nmi, 'Sample size': len(valid_nodes)}
        result_dict.update(nodes_dict)
        results.append(result_dict)

    return results

def find_connections(G):

    connection_list = []
    for node in G.nodes():
        # target_vertex = int(node_id)
        edges, neighbors = find_edges_among_neighbors(G, node)
        number_of_neighbors = len(neighbors)
        connection = len(edges) *2 / (number_of_neighbors*(number_of_neighbors-1))
        connection_list.append(connection)

    return connection_list



def eval_llm_clustering(graph_path, roots_list, num_clusters = 2):
    
    valid_nodes, true_labels, _ = gen_gt_labels(graph_path, roots_list)
    print(len(valid_nodes))
    nodes_dict = {f"Root{label}": root for label, root in enumerate(roots_list)}
    df, _ = find_gt_valid_set(valid_nodes)

    # Data preprocessing
    df['KEYNAME'] = df['NAME'].str.split(" ").str[0]
    
    # Sort and normalize embeddings
    df_sorted = df.sort_values(by='KEYNAME')
    pags_embeddings = get_normalized_embeddings(df_sorted)

    # Clustering and evaluation
    clustering_algorithms = {
        'K-Means': KMeans(n_clusters=num_clusters),
        'Agglomerative': AgglomerativeClustering(n_clusters=num_clusters),
        'DBSCAN': DBSCAN(eps=0.1, min_samples=40),
        'HDBSCAN': hdbscan.HDBSCAN(min_cluster_size=5, gen_min_span_tree=True)
    }

    results = []

    # Perform clustering with each algorithm
    for name, algo in clustering_algorithms.items():
        print(f"Start algo {name} evaluation...")
        ari_score, duration = perform_clustering(algo, name, pags_embeddings, true_labels)
        result_dict = {'Algorithm': name, 'ARI Score': ari_score, 'Duration': duration, 'Sample size': len(valid_nodes)}
        result_dict.update(nodes_dict)
        results.append(result_dict)
    
    return results

def save_llm_clustering_results(graph_path, roots_list):
    
    valid_nodes, true_labels, _ = gen_gt_labels(graph_path, roots_list)
    print(len(valid_nodes))
    df, _ = find_gt_valid_set(valid_nodes)

    # Data preprocessing
    df['KEYNAME'] = df['NAME'].str.split(" ").str[0]
    
    # Sort and normalize embeddings
    df_sorted = df.sort_values(by='KEYNAME')
    pags_embeddings = get_normalized_embeddings(df_sorted)

    # Clustering and evaluation
    clustering_algorithms = {
        # 'K-Means': KMeans(n_clusters=2),
        'Agglomerative': AgglomerativeClustering(n_clusters=2),
        # 'DBSCAN': DBSCAN(eps=0.1, min_samples=40),
        # 'HDBSCAN': hdbscan.HDBSCAN(min_cluster_size=5, gen_min_span_tree=True)
    }

    results = {}

    # Perform clustering with each algorithm
    for name, algo in clustering_algorithms.items():
        print(f"Start algo {name} evaluation...")
        prediction, duration = pred_clusters(algo, name, pags_embeddings)
        pred_array = np.array(prediction)
        results[name] = {}
        for idx in set(prediction):
            results[name][idx] = ",".join(df[pred_array == idx]['KEYNAME'].to_list())
            print(f"{idx}: {len(results[name][idx])}")

    df = pd.DataFrame.from_dict(results, orient='index').reset_index().rename(columns={'index': 'ID'})
    df.to_csv(f"{' '.join(roots_list)}_data_clustering_results.csv",  index=False)
    print("finish!!!")

    return results



def ari_results_box_plots(csv_file_path = 'clustering_3_groups_results.csv'):
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.title("ARI Scores by Clustering Algorithm")
    boxplot = df.boxplot(column='ARI Score', by='Algorithm', grid=False)
    plt.suptitle('')
    plt.xlabel('Algorithm')
    plt.ylabel('ARI Score')
    plt.xticks(rotation=60)
    plt.savefig(f"{csv_file_path.split('.')[0]}.jpg")

# def ari_comparison_box_plots(csv_file_path1, csv_file_path2, method='llm'):

#     label_fontsize = 18
#     font_size = 16
#     annot_font_size = 16

#     cmap = plt.get_cmap('tab10')

#     custom_palette = {
#         'K-Means': cmap(0),
#         'Agglomerative': cmap(1),
#         'DBSCAN': cmap(2),
#         'HDBSCAN': cmap(3),
#         'Spectral Clustering': cmap(4),
#         'Louvain' : cmap(5),
#         'spectral_clustering': cmap(4),
#         'louvain' : cmap(5),
#         'agglomerative_clustering' : cmap(1),
#         # Add more mappings as needed
#     }

#     # Read the CSV files into DataFrames
#     df1 = pd.read_csv(csv_file_path1)
#     df2 = pd.read_csv(csv_file_path2)

#     # Add a column to distinguish the data sets
#     df1['DataSet'] = 'Two Groups Dataset'
#     df2['DataSet'] = 'Three Groups Dataset'

#     # Concatenate the DataFrames
#     df_combined = pd.concat([df1, df2], ignore_index=True)
#     df_filtered = df_combined[df_combined['Algorithm'] != 'DBSCAN']
#     # df_filtered = df_combined[df_combined['Algorithm'] != 'louvain']

#     algorithms = df_filtered['Algorithm'].unique()
#     algo_p_value = {}

#     for algo in algorithms:

#         df_scores = df_filtered[df_filtered['Algorithm'] == algo]
#         # Compute t-test between the two groups for the selected algorithm
#         group1_scores = df_scores[df_scores['DataSet'] == 'Two Groups Dataset']['ARI Score']
#         group2_scores = df_scores[df_scores['DataSet'] == 'Three Groups Dataset']['ARI Score']
#         t_stat, p_value = ttest_ind(group1_scores, group2_scores, equal_var=False) 
#         algo_p_value[algo] = p_value
#         print(f"T-test for {algo}: t-statistic = {t_stat}, p-value = {p_value}")

#     # Plotting using seaborn for better control over aesthetics
#     plt.figure(figsize=(8, 6))
#     ax = sns.boxplot(data=df_filtered, x='DataSet', y='ARI Score', hue='Algorithm', width=0.6, palette= custom_palette)
#     sns.pointplot(data=df_filtered, x='DataSet', y='ARI Score', hue='Algorithm', 
#               dodge=True, join=False, markers='D', capsize=0, errwidth=0, palette=custom_palette)

#     # Adjust the legend
#     handles, labels = ax.get_legend_handles_labels()

#     new_handles = handles[:int(len(handles)/2)]
#     new_labels = labels[:int(len(labels)/2)]
#     #   Add a label for the mean values
#     new_handles.append(plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='k', label='Mean'))
#     new_labels.append('Mean')
#     ax.legend(handles=new_handles, labels=new_labels, title='Algorithm')


#     # plt.title("ARI Scores Comparison")
#     plt.ylabel('ARI Score', fontsize=label_fontsize)
    
#     # Get current y-axis ticks and labels
#     ticks = ax.get_yticks()

#     # Define the maximum value you want to display on the y-axis
#     max_display_value = 1.1

#     # Generate new tick labels, replace those above max_display_value with an empty string
#     new_tick_labels = [str(round(tick, 1)) if tick <= max_display_value else '' for tick in ticks]

#     # Apply the new tick labels
#     ax.set_yticklabels(new_tick_labels)


#     # plt.xticks(rotation=60)
#     plt.legend(title='Algorithm', bbox_to_anchor=(1.05, 1), loc='upper left')
#     plt.xticks(fontsize=font_size)  # Change font size for x-axis
#     plt.yticks(fontsize=font_size)  # Ch

#     hue_order = ax.get_legend_handles_labels()[1]
#     # n_hues = len(hue_order)

#     # # Get the current color palette, assuming it has at least as many colors as there are hues
#     # palette = sns.color_palette()[:n_hues]

#     # Map the hue order to the colors
#     hue_colors = {k: custom_palette[k] for k in hue_order if k in custom_palette}

#     y = df_filtered['ARI Score'].max()
#     h = 0.1
#     # Optionally, print or return the color for each hue level (Algorithm)
#     for idx, (algo, col) in enumerate(hue_colors.items()):
#         plt.plot([ -0.2+idx*0.2, -0.2+idx*0.2 , 0.8 + idx*0.2 , 0.8 + idx*0.2 ], 
#                  [y+0.05, y+0.2+h*idx, y+0.2+ h*idx, y+0.05], 
#                  lw=1.5, c=col)
#         plt.text(0.35+idx*0.2, y+0.2+h*idx, f"p = {algo_p_value[algo]:.4f}", ha='center', va='bottom', color=col)
#         print(f"Algorithm: {algo}, Color: {col}")

#     # Save the plot
#     plt.savefig(f"{method}_ari_scores_comparison_new.jpg", bbox_inches='tight')
#     # plt.show()
    
def ari_comparison_box_plots(csv_file_path1, csv_file_path2, method='llm'):

    label_fontsize = 18
    font_size = 16
    cmap = plt.get_cmap('tab10')
    custom_palette = {
        'K-Means': cmap(0), 'Agglomerative': cmap(1), 'DBSCAN': cmap(2),
        'HDBSCAN': cmap(3), 'Spectral Clustering': cmap(4), 'Louvain': cmap(5),
        'spectral_clustering': cmap(4), 'louvain': cmap(5),
        'agglomerative_clustering': cmap(1)
    }

    df_combined = pd.concat([
        pd.read_csv(csv_file_path1).assign(DataSet='Two Groups Dataset'),
        pd.read_csv(csv_file_path2).assign(DataSet='Three Groups Dataset')
    ], ignore_index=True)
    
    df_filtered = df_combined[df_combined['Algorithm'] != 'DBSCAN']
    algorithms = df_filtered['Algorithm'].unique()

    algo_p_value = {}
    for algo in algorithms:
        df_scores = df_filtered[df_filtered['Algorithm'] == algo]
        group1_scores = df_scores[df_scores['DataSet'] == 'Two Groups Dataset']['ARI Score']
        group2_scores = df_scores[df_scores['DataSet'] == 'Three Groups Dataset']['ARI Score']
        t_stat, p_value = ttest_ind(group1_scores, group2_scores, equal_var=False)
        algo_p_value[algo] = p_value
        print(f"T-test for {algo}: t-statistic = {t_stat:.4f}, p-value = {p_value:.4f}")

    plt.figure(figsize=(12, 6))
    ax = sns.boxplot(data=df_filtered, x='DataSet', y='ARI Score', hue='Algorithm', width=0.6, palette=custom_palette)
    
    # Calculate mean positions
    means = df_filtered.groupby(['DataSet', 'Algorithm'])['ARI Score'].mean().unstack()
    
    # Get the order of algorithms from the legend
    handles, labels = ax.get_legend_handles_labels()
    algorithm_order = labels

    # Plot mean markers
    for i, dataset in enumerate(means.index):
        for j, algo in enumerate(algorithm_order):
            if algo in means.columns:
                x = i + (j - (len(algorithm_order) - 1) / 2) * 0.6 / len(algorithm_order)
                y = means.loc[dataset, algo]
                ax.plot(x, y, marker='D', color=custom_palette[algo], markersize=8, markeredgewidth=1, markeredgecolor='black')

    new_handles = handles + [plt.Line2D([0], [0], marker='D', color='k', linestyle='', label='Mean')]
    new_labels = labels + ['Mean']
    ax.legend(handles=new_handles, labels=new_labels, title='Algorithm', bbox_to_anchor=(1.05, 1), loc='upper left')

    # plt.title("ARI Scores Comparison")
    plt.ylabel('ARI Score', fontsize=label_fontsize)
    plt.xticks(fontsize=label_fontsize)  # Change font size for x-axis
    plt.yticks(fontsize=font_size)  # Ch
    ax.set_xlabel('')

    # Add p-value annotations
    y_max = df_filtered['ARI Score'].max()
    for i, algo in enumerate(algorithm_order):
        if algo in algo_p_value:
            plt.text(0.5, y_max + 0.21 + 0.1 * i, 
                     f"{algo}: p = {algo_p_value[algo]:.4f}", 
                     ha='center', va='bottom', color=custom_palette[algo], fontsize=8)
            # Plot lines for p-value
            plt.plot([ -0.2 + i * 0.2, -0.2 + i * 0.2, 0.8 + i * 0.2, 0.8 + i * 0.2 ], 
                        [y_max + 0.05, y_max + 0.2 + 0.1 * i, y_max + 0.2 + 0.1 * i, y_max + 0.05], 
                        lw=1.5, c=custom_palette[algo])

    plt.tight_layout()
    plt.savefig(f"{method}_ari_scores_comparison_new.jpg", bbox_inches='tight')
    plt.close()


# Example usage
# ari_comparison_box_plots('clustering_results.csv', 'clustering_3_groups_results.csv')

def eval_real_data(pags_csv_path = "Leukemia_drug_resistantVSsensitive.csv"):
    df_real = pd.read_csv(pags_csv_path)
    filtered_df = df_real[~df_real['Name'].str.contains('cellular component') & ~df_real['Name'].str.contains('molecular function')]
    valid_nodes = filtered_df['Name'].str.split(" ").str[0].to_list()
    df, _ = find_gt_valid_set(valid_nodes)  

    df['KEYNAME'] = df['NAME'].str.split(" ").str[0]

    df_sorted = df.sort_values(by='KEYNAME')
    pags_embeddings = get_normalized_embeddings(df_sorted)

    # tsne_2d_plot(pags_embeddings=pags_embeddings)
    # Clustering and evaluation
    clustering_algorithms = {
        # 'K-Means': KMeans(n_clusters=2),
        'Agglomerative': AgglomerativeClustering(n_clusters=2),
        # 'DBSCAN': DBSCAN(eps=0.1, min_samples=40),
        # 'HDBSCAN': hdbscan.HDBSCAN(min_cluster_size=5, gen_min_span_tree=True)
    }

    results = {}

    # Perform clustering with each algorithm
    for name, algo in clustering_algorithms.items():
        print({f"Start algo {name} evaluation..."})
        prediction, duration = pred_clusters(algo, name, pags_embeddings)
        pred_array = np.array(prediction)
        results[name] = {}
        for idx in set(prediction):
            results[name][idx] = df[pred_array == idx]['KEYNAME'].to_list()
            print(f"{idx}: {len(results[name][idx])}")

    df = pd.DataFrame.from_dict(results, orient='index').reset_index().rename(columns={'index': 'ID'})
    df.to_csv("test_real_data_clustering_results.csv",  index=False)
    print("finish!!!")

    return results

def generate_text_chunks(text, prompt, max_length=1024, llm_model= 'gpt2'):
    # tokenizer = GPT2Tokenizer.from_pretrained(llm_model)
    tokenizer = GPT2TokenizerFast.from_pretrained("openai-community/gpt2")
    model = GPT2LMHeadModel.from_pretrained(llm_model)
    gpt2_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)  # Use device=0 for GPU if available


    prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
    text_ids = tokenizer.encode(text, add_special_tokens=False)
    # tokens = tokenizer.tokenize(text)
    # prompt_tokens = tokenizer.tokenize(prompt)
    # Calculate the maximum chunk size, accounting for prompt tokens
    max_chunk_size = max_length - len(prompt_ids) - 1
    output_text = []
    
    for i in range(0, len(text_ids), max_chunk_size):
        chunk_ids = text_ids[i:i + max_chunk_size]
        # No need to prepend prompt_ids to each chunk, just ensure the first chunk starts with it
        if i == 0:
            chunk_ids = prompt_ids + chunk_ids
        chunk_text = tokenizer.decode(chunk_ids, clean_up_tokenization_spaces=True)

        # Generate text from the chunk
        generated_outputs = gpt2_generator(chunk_text, max_length=max_length, num_return_sequences=1)
        # print(generated_outputs)
        generated_text = generated_outputs[0]['generated_text'].strip()

        # Optionally, remove the input part from the generated text
        if i == 0:
            generated_text = generated_text[len(tokenizer.decode(prompt_ids)):].strip()

        output_text.append(generated_text)
    
    concatenated_output = " ".join(output_text)
    return concatenated_output


def summarize_text(text, chunk_size=1024):
    summarizer = pipeline("summarization")
    # Split the text into sentences
    summaries = summarize_chunk(text, chunk_size, summarizer)
    
    # Optional: summarize the summaries if still too long
    final_summary = ' '.join(summaries)
    if len(final_summary.split()) > 100:  # Adjust based on your needs
        if len(final_summary) > chunk_size:
            print("DO IT AGAIN!!")
            final_summary = ' '.join(summarize_chunk(final_summary, chunk_size, summarizer))
        else:
            final_summary = summarizer(final_summary)[0]['summary_text']
    
    return final_summary

def summarize_chunk(text, chunk_size, summarizer):
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    
    # Chunk the text properly based on the chunk_size
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + '. '
    chunks.append(current_chunk)  # Add the last chunk
    
    # Summarize each chunk
    summaries = [summarizer(chunk)[0]['summary_text'] for chunk in chunks]
    return summaries



def summarize_cluster_results(clusering_results_path= "real_data_clustering_results.csv"):
    
    # generator = pipeline('text-generation', model='gpt2')
    # Initialize the model and tokenizer
    max_length = 1024  # Adjust as needed
    df = pd.read_csv(clusering_results_path)
    df_desc = pd.read_csv(META_DATA_PATH)

    # summarize_prompt = lambda input_text: f"Summarize the following sentences into a single sentence: {input_text}"
    summarize_prompt = "Summarize the following text in a concise manner, aiming for a brief summary of about 50 words or less:"

    
    df.head()
    for idx, row in df.iterrows():
        algo = row['ID']
        # pred_list = [row[label].split(',') for label in ['0', '1', '-1'] if not pd.isna(row[label])]
        pred_list = [row[label].split(',') for label in ['0', '1'] if not pd.isna(row[label])]

        pred_desc = {}
        results_dict = {}
        for idx, preds in enumerate(pred_list):
            pred_desc[idx] = df_desc[df_desc['GOID'].isin(preds)]['DESCRIPTION'].tolist()
            input_text = " ".join(pred_desc[idx])
            # prompt = summarize_prompt(input_text)
            summary = summarize_text(input_text)
            results_dict[idx] = [summary]
            # first_try = generate_text_chunks(input_text, summarize_prompt, max_length, max_new_tokens=100)
            # while len(first_try) > 50:
            #     print("make it shorter....")
            #     first_try = generate_text_chunks(first_try, summarize_prompt, max_length, max_new_tokens=50)

            # save_result =first_try

        df_result = pd.DataFrame(results_dict)
        save_name = clusering_results_path.split('.')[0][:-24]
        save_path = f"{algo}_{save_name}_cluster_summarizatoin.csv"
        df_result.to_csv(save_path, index=False)
        print(results_dict)




def visulize_pred_results(G_path= "2024_biological_process_graph_w_verification.graphml", pred_dict_path= "real_data_clustering_results.csv"):
    G = nx.read_graphml(G_path)
    vis_graph = GraphAnalysis(nx.read_graphml(WHOLE_GRAPH_PATH), 'GO:0008150')
    df = pd.read_csv(pred_dict_path)
    df.head()
    
    for idx, row in df.iterrows():

        algo = row['ID']
        pred_list = [row[label].split(',') for label in ['0', '1', '-1'] if not pd.isna(row[label])]
        all_nodes = [item for sublist in pred_list for item in sublist]
        color_map = cm.get_cmap('viridis', len(pred_list) + 1)
        all_connected_nodes = vis_graph.add_intermediate_nodes_to_keep_connected(all_nodes)
        subG = vis_graph.create_subgraph_from_nodes(all_connected_nodes)

        # Reverse only the direction of the edges, keep the node positions same
        pos = graphviz_layout(subG, prog='dot')
        reversed_edges = [(v, u) for u, v in subG.edges()]  # Reverse the direction of each edge
        reversed_subG = nx.DiGraph()  # Create a new directed graph
        reversed_subG.add_nodes_from(subG.nodes())  # Keep nodes the same
        reversed_subG.add_edges_from(reversed_edges)  # Add reversed edges

        node_colors = []
        border_colors = []
        label_colors = {}
        labels = {}
        label_names = ['Cluster 0', 'Cluster 1', 'Cluster -1']  # Names for the labels
        legend_patches = []  # List to store patches for the legend

        for node in reversed_subG.nodes():
            if node not in all_nodes:
                node_colors.append((1,1,1,1))  # White color for nodes not in the clusters
                border_colors.append((0,0,0,1))  # Black border
            else:
                for i, node_list in enumerate(pred_list):
                    if node in node_list:
                        # Map each list index to a color in the colormap
                        color = color_map(i)
                        node_colors.append(color)
                        border_colors.append(color)
                        labels[node] = node
                        label_colors[node] = color
                        
                        # Add patch to the legend for this label if not already added
                        if len(legend_patches) <= i:
                            patch = mpatches.Patch(color=color, label=label_names[i])
                            legend_patches.append(patch)

        # Plotting
        plt.figure(figsize=(16, 10))
        # plt.title(f"The visualization for LLM embedding clustering by Algorithm {algo}")
        
        # Draw the reversed graph with arrows pointing in the opposite direction, using the same node positions
        nx.draw_networkx(reversed_subG, pos, with_labels=False, node_color=border_colors, node_size=240, arrows=True)
        nx.draw_networkx(reversed_subG, pos, with_labels=False, node_color=node_colors, node_size=200)

        # Drawing labels with the same color as nodes and rotated
        for node, (x, y) in pos.items():
            if node in label_colors:
                plt.text(x, y-18, s=node, color=label_colors[node],  # Adjust indexing if node_colors is a list
                         horizontalalignment='center', verticalalignment='center',
                         rotation=30, fontsize=10)

        # Add legend
        plt.legend(handles=legend_patches, loc='lower right', bbox_to_anchor=(1, 0), prop={'size': 20})


        # Remove borders and axis from the plot
        plt.gca().set_axis_off()
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove margins

        save_name = pred_dict_path[:-4]
        plt.savefig(f"visualization_{save_name}_w_{algo.lower()}_reversed_direction.jpg", dpi=300, bbox_inches='tight', pad_inches=0)


def comparison_two_methods(group_size = 2):

    methods = ['m-type', 'llm']
    df_dict = { }

    for method in methods:
        df_dict[method] =  pd.read_csv(f"{method}_clustering_{group_size}_groups_results.csv")
        df_dict[method]['Method'] = method
    
    df_combined = pd.concat([df_dict[method] for method in methods], ignore_index=True)
    df_combined.to_csv(f"comparison_{'_'.join(methods)}_{group_size}_groups_results.csv", index=False)


def methods_comparison_box_plots(csv_file_path="comparison_m-type_llm_2_groups_results.csv"):

    # Read the CSV files into DataFrames
    df = pd.read_csv(csv_file_path)

    df_filtered = df[df['Algorithm'] != 'DBSCAN']

    plt.figure(figsize=(12, 6))
    plt.title("ARI Scores by Clustering Algorithm")
    # boxplot = df_filtered.boxplot(column='ARI Score', by='Algorithm', grid=False)
    ax = sns.boxplot(x='Alpha', y='ARI Score', hue='Algorithm', data=df)
    means = df_filtered.groupby(['Alpha', 'Algorithm'])['ARI Score'].mean().reset_index()

    # Retrieve tick labels and positions
    tick_labels = [label.get_text() for label in ax.get_xticklabels()]
    tick_positions = ax.get_xticks()

    # Assuming the hue results in multiple groups per x-tick, calculate their positions
    # Determine how many hues or groups per DataSet
    num_hues = len(df_filtered['Algorithm'].unique())
    group_width = 0.6 / num_hues  # based on the width used in boxplot

    # Annotate each group
    for index, row in means.iterrows():
        alpha = row['Alpha']
        algorithm = row['Algorithm']
        mean_value = row['ARI Score']
        
        # Find the base position of the DataSet
        base_pos = tick_positions[tick_labels.index(str(alpha))] if str(alpha) in tick_labels else None
        
        if base_pos is not None:
            # Adjust position based on the algorithm index
            algo_index = list(df_filtered['Algorithm'].unique()).index(algorithm)
            adjusted_pos = base_pos + (algo_index * group_width) - group_width / 2 - 0.1
            
            # Annotate the mean value
            ax.text(adjusted_pos, mean_value + 0.01, f'{mean_value:.2f}', color='black', ha='center', va='bottom')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, title='Algorithm', loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)


    plt.suptitle('')
    plt.xlabel('Algorithm')
    plt.ylabel('ARI Score')
    plt.xticks(rotation=20)
    plt.savefig(f"{csv_file_path.split('.')[0]}_mean.jpg")





def merge_feature_to_embeddings_clustering(roots_list, alpha = 0.5, num_clusters=2, is_visualized=False):
    save_file_path = f"{'_'.join(roots_list)}_embedding_alpha_{alpha}_num_{num_clusters}_clustering_results.csv".replace(':','')

    clustering_algorithms = {
        # 'K-Means': KMeans(n_clusters=num_clusters),
        'Agglomerative': AgglomerativeClustering(n_clusters=num_clusters),
        # 'DBSCAN': DBSCAN(eps=0.1, min_samples=40),
        # 'HDBSCAN': hdbscan.HDBSCAN(min_cluster_size=5, gen_min_span_tree=True)
    }

    # read data from files
    bp_graph_path ='2024_biological_process_graph_w_verification.graphml'
    df_relationship = read_m_type_file("go_metadata/m_type_biological_process.txt")
    valid_nodes, true_labels, true_labels_dict = gen_gt_labels(bp_graph_path, roots_list)
    nodes_dict = {f"Root{label}": root for label, root in enumerate(roots_list)}

    # convert the embeddings of description to a matrix
    df_embeddings, _ = find_gt_valid_set(valid_nodes)
    df_embeddings['KEYNAME'] = df_embeddings['NAME'].str.split(" ").str[0]
    
    # Sort and normalize embeddings
    df_sorted = df_embeddings.sort_values(by='KEYNAME')
    pags_embeddings = get_normalized_embeddings(df_sorted)

    # convert the m-type relationship to a matrix
    filtered_df = df_relationship[df_relationship['GS_A_ID'].isin(valid_nodes) & df_relationship['GS_B_ID'].isin(valid_nodes)]
    results = []
    G = nx.Graph()
    for _, row in filtered_df.iterrows():
        G.add_edge(row['GS_A_ID'], row['GS_B_ID'], weight=row['SIMILARITY'])

    sorted_nodes_by_names = sorted(G.nodes())
    adj_matrix = nx.to_numpy_array(G, nodelist=sorted_nodes_by_names)
    con_matrix = np.concatenate((alpha*pags_embeddings, (1-alpha)*adj_matrix), axis=1)

    results = {}
    # Perform clustering with each algorithm
    for name, algo in clustering_algorithms.items():
        print({f"Start algo {name} evaluation..."})
        cc = ConsensusClustering(
            clustering_obj=algo,
            min_clusters=2,
            max_clusters=10,
            n_resamples=1000,
            resample_frac=0.8,
            k_param='n_clusters'
        )

        cc.fit(con_matrix, progress_bar=True)   
        _, ax = plt.subplots(figsize=(12, 8))
        cc.plot_cdf(ax=ax)
        ax.legend(bbox_to_anchor=(1, 1))
        plt.savefig(f"cc_cdf_plot_w_{name}.jpg")
        print(f"The best K: {cc.best_k('change_in_auc')}")


        # prediction, duration = pred_clusters(algo, name, con_matrix)
        # pred_array = np.array(prediction)
        # results[name] = {}
        # for idx in set(prediction):
        #     results[name][idx] = ",".join(df_embeddings[pred_array == idx]['KEYNAME'].to_list())
        #     print(f"{idx}: {len(results[name][idx])}")

    # df = pd.DataFrame.from_dict(results, orient='index').reset_index().rename(columns={'index': 'ID'})
    # df.to_csv(save_file_path, index=False)

    if is_visualized:
        visulize_pred_results(pred_dict_path= save_file_path)

    return results

def merge_feature_to_graph_clustering(roots_list, alpha = 0.5, num_clusters=2, is_visualized=True):
    save_file_path = f"{'_'.join(roots_list)}_m-type_alpha_{alpha}_num_{num_clusters}_clustering_results.csv".replace(':','')

    clustering_algorithms = {
        # 'K-Means': KMeans(n_clusters=2),
        'Agglomerative': AgglomerativeClustering(n_clusters=2),
        # 'DBSCAN': DBSCAN(eps=0.1, min_samples=40),
        # 'HDBSCAN': hdbscan.HDBSCAN(min_cluster_size=5, gen_min_span_tree=True)
    }

    # read data from files
    bp_graph_path ='2024_biological_process_graph_w_verification.graphml'
    df_relationship = read_m_type_file("go_metadata/m_type_biological_process.txt")
    valid_nodes, true_labels, true_labels_dict = gen_gt_labels(bp_graph_path, roots_list)

    # convert the embeddings of description to a matrix
    df_embeddings, _ = find_gt_valid_set(valid_nodes)
    df_embeddings['KEYNAME'] = df_embeddings['NAME'].str.split(" ").str[0]
    
    # Sort and normalize embeddings
    df_sorted = df_embeddings.sort_values(by='KEYNAME')
    pags_embeddings = get_normalized_embeddings(df_sorted)

    embed_similar_matrix = cosine_similarity(pags_embeddings)

    # convert the m-type relationship to a matrix
    nodes_dict = {f"Root{label}": root for label, root in enumerate(roots_list)}
    filtered_df = df_relationship[df_relationship['GS_A_ID'].isin(valid_nodes) & df_relationship['GS_B_ID'].isin(valid_nodes)]
    results = []
    G = nx.Graph()
    for _, row in filtered_df.iterrows():
        GS_A_embeddings = df_sorted.loc[df_sorted['GOID']==row['GS_A_ID']]['EMBEDDING'].values[0]
        GS_B_embeddings = df_sorted.loc[df_sorted['GOID']==row['GS_B_ID']]['EMBEDDING'].values[0]
        embedding_similarity = cosine_similarity([GS_A_embeddings], [GS_B_embeddings])

        corelation_weight = alpha * row['SIMILARITY'] + (1-alpha)* embedding_similarity[0][0]
        G.add_edge(row['GS_A_ID'], row['GS_B_ID'], weight=corelation_weight)

    true_labels = [true_labels_dict[node] for node in G.nodes()]

    adj_matrix = nx.to_numpy_array(G)

    results = {}

    # Perform clustering with each algorithm
    for name, algo in clustering_algorithms.items():
        print({f"Start algo {name} evaluation..."})
        prediction, duration = pred_clusters(algo, name, adj_matrix)
        pred_array = np.array(prediction)
        results[name] = {}
        for idx in set(prediction):
            results[name][idx] = ",".join(df_embeddings[pred_array == idx]['KEYNAME'].to_list())
            print(f"{idx}: {len(results[name][idx])}")

    df = pd.DataFrame.from_dict(results, orient='index').reset_index().rename(columns={'index': 'ID'})
    df.to_csv(save_file_path, index=False)
    print("finish!!!")

    if is_visualized:
        visulize_pred_results(pred_dict_path= save_file_path)

    # for algorithm in ['spectral_clustering', 'agglomerative_clustering']:  #'girvan_newman',  'louvain', 'girvan_newman', 
    #     ari, nmi = run_eval(algorithm, G, true_labels, is_plot=False, num_clusters=num_clusters)
    #     result_dict = {'Algorithm': algorithm, 'ARI Score': ari, 'NMI': nmi, 'Sample size': len(valid_nodes)}
    #     result_dict.update(nodes_dict)
    #     results.append(result_dict)

    return results

def eval_merge_feature_to_embeddings_clustering(roots_list, alpha = 0.5, num_clusters=2):
    save_file_path = f"{'_'.join(roots_list)}_embedding_alpha_{alpha}_num_{num_clusters}_clustering_results.csv".replace(':','')

    clustering_algorithms = {
        'K-Means': KMeans(n_clusters=2),
        'Agglomerative': AgglomerativeClustering(n_clusters=2),
        # 'DBSCAN': DBSCAN(eps=0.1, min_samples=40),
        'HDBSCAN': hdbscan.HDBSCAN(min_cluster_size=5, gen_min_span_tree=True)
    }

    # read data from files
    bp_graph_path ='2024_biological_process_graph_w_verification.graphml'
    df_relationship = read_m_type_file("go_metadata/m_type_biological_process.txt")
    valid_nodes, true_labels, true_labels_dict = gen_gt_labels(bp_graph_path, roots_list)
    nodes_dict = {f"Root{label}": root for label, root in enumerate(roots_list)}

    # convert the embeddings of description to a matrix
    df_embeddings, _ = find_gt_valid_set(valid_nodes)
    df_embeddings['KEYNAME'] = df_embeddings['NAME'].str.split(" ").str[0]
    
    # Sort and normalize embeddings
    df_sorted = df_embeddings.sort_values(by='KEYNAME')
    pags_embeddings = get_normalized_embeddings(df_sorted)

    # convert the m-type relationship to a matrix
    filtered_df = df_relationship[df_relationship['GS_A_ID'].isin(valid_nodes) & df_relationship['GS_B_ID'].isin(valid_nodes)]
    results = []
    G = nx.Graph()
    for _, row in filtered_df.iterrows():
        G.add_edge(row['GS_A_ID'], row['GS_B_ID'], weight=row['SIMILARITY'])

    sorted_nodes_by_names = sorted(G.nodes())
    adj_matrix = nx.to_numpy_array(G, nodelist=sorted_nodes_by_names)

    con_matrix = np.concatenate((alpha*pags_embeddings, (1-alpha)*adj_matrix), axis=1)

    results = []

    # Perform clustering with each algorithm
    for name, algo in clustering_algorithms.items():
        print({f"Start algo {name} evaluation..."})
        ari_score, duration = perform_clustering(algo, name, con_matrix, true_labels)
        result_dict = {'Algorithm': name, 'ARI Score': ari_score, 'Duration': duration, 'Sample size': len(valid_nodes)}
        result_dict.update(nodes_dict)
        results.append(result_dict)

    return results


def analyze_outdegree(G_path='2024_biological_process_graph_w_verification.graphml'):

    G = nx.read_graphml(G_path)
    # Compute outdegree for all nodes
    outdegrees = list(dict(G.out_degree()).values())
    filtered_outdegrees = [x for x in outdegrees if x != 0]
    threshold_min = 1

    # Create the histogram data (consider using bins for continuous data)
    counts, bins = np.histogram(filtered_outdegrees, np.arange(min(filtered_outdegrees), max(filtered_outdegrees)+1))

    # Create the main plot
    fig, ax1 = plt.subplots()
    ax1.hist(filtered_outdegrees, bins=bins, edgecolor='black')  # Plot histogram with black edges
    ax1.set_xlabel("Outdegree")
    ax1.set_ylabel("Original Scale")

    # Create the secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(bins[:-1] + (bins[1:] - bins[:-1]) / 2, counts, color='red', linestyle='--')  # Plot on bin centers with dashed line

    # Define different y-axis scales for each axis
    ax1.set_ylim(0, 50)
    ax2.set_ylim(0, max(counts))  # Adjust scaling based on threshold and max count

    # Customize labels and title
    ax1.set_title("Outdegree Distribution with Different Y-axis Scales")
    ax2.set_ylabel("Whole Values", color='blue')  # Set color for secondary axis label


    plt.grid(True)
    # plt.show()

    plt.savefig("2024_biological_process_graph_w_verification_outdegree_distribution.jpg")


    return filtered_outdegrees


def analyze_logarithmic_outdegree(G_path='2024_biological_process_graph_w_verification.graphml'):
    G = nx.read_graphml(G_path)
    label_font_size = 16
    # Compute outdegree for all nodes
    outdegrees = list(dict(G.out_degree()).values())
    filtered_outdegrees = [x for x in outdegrees if x != 0]

    # Create the histogram data (consider using bins for continuous data)
    counts, bins = np.histogram(filtered_outdegrees, np.arange(min(filtered_outdegrees), max(filtered_outdegrees)+1))

    # Compute log of the counts
    log_counts = np.log1p(counts)  # log1p to avoid log(0)

    # Create the main plot
    fig, ax1 = plt.subplots(figsize=(12, 9))
    plt.grid(True)
    ax1.hist(filtered_outdegrees, bins=bins, edgecolor='black')  # Plot histogram with black edges
    ax1.set_xlabel("Outdegree", fontsize=label_font_size)
    ax1.set_ylabel("Original Scale", fontsize=label_font_size)
    ax1.tick_params(axis='both', labelsize=label_font_size)  # Change font size for x-axis

    # Create the secondary y-axis with logarithmic scale
    ax2 = ax1.twinx()
    ax2.plot(bins[:-1] + (bins[1:] - bins[:-1]) / 2, log_counts, color='red', linestyle='--')  # Logarithmic plot
    ax2.set_yscale('log')  # Set y-axis to logarithmic scale
    ax2.set_ylabel("Log of Counts", fontsize=label_font_size)
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position('right')

    ax2.set_yticks([1, 10])
    # ax2.yaxis.set_major_formatter(ticker.ScalarFormatter())

    ax2.tick_params(axis='y', labelsize=label_font_size)

    # Customize labels and title
    ax1.set_title(r"Outdegree Distribution with Logarithmic Y-axis: $\log(y+1)$")

    
    plt.savefig("2024_biological_process_graph_w_verification_outdegree_distribution_log.jpg")

    return filtered_outdegrees



def test():
    # ['GO:0042127','GO:0097435'], ['GO:0061024','GO:0098662'],['GO:2000241','GO:0030154']
    bp_graph_path ='2024_biological_process_graph_w_verification.graphml'
    exp_candidates = [ ['GO:0051128','GO:0061024','GO:0080135'] ]
    results = []
    num = 3
    # step_list = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    step_list = [0.8]
    for roots, alpha in itertools.product(exp_candidates, step_list):
        # eval_merge_feature_clustering(roots, alpha=alpha)
        
        merge_feature_to_embeddings_clustering(roots, alpha, num_clusters=num)
        # visulize_pred_results(pred_dict_path=save_file_path)
        # save_llm_clustering_results(bp_graph_path, roots)
        # visulize_pred_results(pred_dict_path=save_file_path)

    # Convert results to DataFrame and save to CSV
    # results_df = pd.DataFrame(results)
    # results_df.to_csv(f'merge_features_clustering_{num}_groups_results.csv', index=False)

    # summarize_cluster_results("real_data_clustering_results.csv")


def methods_comparison_violin_plots(csv_file_path):

    label_fontsize = 24
    font_size = 20
    annot_font_size=16
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Set up the plot
    plt.figure(figsize=(30, 10))
    # plt.title("ARI Scores by Clustering Algorithms",fontdict={'fontsize': 18,})


    # Create a violin plot
    ax = sns.violinplot(x='Alpha', y='ARI Score', hue='Algorithm', data=df, cut=0)

    # Calculate means for each group within each alpha level
    means = df.groupby(['Alpha', 'Algorithm'])['ARI Score'].mean().reset_index()

    # Retrieve tick labels and positions
    tick_labels = [label.get_text() for label in ax.get_xticklabels()]
    tick_positions = ax.get_xticks()

    # Annotate each group with its mean value
    num_hues = len(df['Algorithm'].unique())
    group_width = 0.8 / num_hues  # adjust the group width based on number of algorithms

    for index, row in means.iterrows():
        alpha = row['Alpha']
        algorithm = row['Algorithm']
        mean_value = row['ARI Score']

        # Find the base position of the alpha label
        base_pos = tick_positions[tick_labels.index(str(alpha))] if str(alpha) in tick_labels else None

        if base_pos is not None:
            # Adjust position based on the algorithm index
            algo_index = list(df['Algorithm'].unique()).index(algorithm)
            # adjusted_pos = base_pos + (algo_index * group_width) - group_width / 2
            adjusted_pos = base_pos + (algo_index * group_width) - group_width 

            # Annotate the mean value
            ax.text(
                    adjusted_pos, 
                    mean_value + 0.01, 
                    f'{mean_value:.2f}', 
                    color='black', 
                    ha='left', 
                    va='center',
                    fontdict={'fontsize': 14}
                )


    # Adjust the legend and layout
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, loc='lower right', prop={'size': 18})
    # ax.legend(handles=handles, labels=labels, title='Algorithms', loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0.)     
    # Further layout settings
    plt.suptitle('')
    plt.xlabel(r"Coeffient $\alpha$", fontsize=label_fontsize)
    plt.ylabel('ARI Score', fontsize=label_fontsize)

    plt.xticks(fontsize=font_size)  # Change font size for x-axis
    plt.yticks(fontsize=font_size)  # Ch
    plt.grid(True)  # Optionally add grid for better visibility of ticks
    plt.tight_layout()  # Adjust layout to fit all elements

    # Save the plot to a file
    plt.savefig(f"{csv_file_path.split('.')[0]}_ARI_scores_violin.jpg")

def analyze_zoomin_outdegree(G_path='2024_biological_process_graph_w_verification.graphml'):
    
    label_font_size  = 14
    G = nx.read_graphml(G_path)
    
    # Compute outdegree for all nodes
    outdegrees = list(dict(G.out_degree()).values())
    filtered_outdegrees = [x for x in outdegrees if x != 0]

    # Create the histogram data
    counts, bins = np.histogram(filtered_outdegrees, np.arange(min(filtered_outdegrees), max(filtered_outdegrees) + 1))

    # Create the main plot
    fig, ax1 = plt.subplots(figsize=(12, 9))
    ax1.hist(filtered_outdegrees, bins=bins, edgecolor='black')  # Plot histogram with black edges
    ax1.set_xlabel("Outdegree", fontsize=label_font_size)
    ax1.set_ylabel("Count", fontsize=label_font_size)

    # Move the y-axis to the right
    # ax1.yaxis.tick_right()
    # ax1.yaxis.set_label_position("right")

    # Add zoomed-in plot for x-values between 10 and 100
    axins1 = fig.add_axes([0.6, 0.57, 0.3, 0.3])  # Define position and size of the zoomed-in plot
    axins1.hist(filtered_outdegrees, bins=bins, edgecolor='black')
    axins1.set_xlim(10, 100)  # Limit for zoom-in
    axins1.set_ylim(0, 40)  # Y-axis limit for the inset
    axins1.set_xlabel('Outdegree 10-100', fontsize=label_font_size)
    axins1.set_ylabel('', fontsize=label_font_size)
    axins1.yaxis.tick_right()
    axins1.yaxis.set_label_position('right')


    # Add zoomed-in plot for x-values between 5 and 10
    axins2 = fig.add_axes([0.6, 0.17, 0.3, 0.3])  # Define position and size of the zoomed-in plot
    axins2.hist(filtered_outdegrees, bins=bins, edgecolor='black')
    axins2.set_xlim(5, 10)  # Limit for zoom-in
    axins2.set_ylim(0, 300)  # Y-axis limit for the inset
    axins2.set_xlabel('Outdegree 5-10', fontsize=label_font_size)
    axins2.set_ylabel('', fontsize=label_font_size)
    axins2.yaxis.tick_right()
    axins2.yaxis.set_label_position('right')

    # Customize labels and title
    ax1.set_title("Outdegree Distribution with Zoomed-in Views (5-10, 10-100)")

    # Save the plot as an image
    plt.savefig("2024_biological_process_graph_w_verification_outdegree_distribution_zoom.jpg")

    return filtered_outdegrees


def toden_e_predict(pags_txt_path = "Leukemia_drug_resistantVSsensitive.txt", alpha = 0.5, num_clusters=2, is_visualized=False):

    
    # Read gene names from a text file into a list
    with open(pags_txt_path, 'r') as file:
        valid_nodes = [line.strip() for line in file if line.strip()]  # Read lines and strip whitespace

    save_file_path = "toden_predict_results.csv"

    clustering_algorithms = {'Agglomerative': AgglomerativeClustering(n_clusters=num_clusters),}

    # read data from files
    df_relationship = read_m_type_file("go_metadata/m_type_biological_process.txt")

    # convert the embeddings of description to a matrix
    df_embeddings, _ = find_gt_valid_set(valid_nodes)
    df_embeddings['KEYNAME'] = df_embeddings['NAME'].str.split(" ").str[0]
    
    # Sort and normalize embeddings
    df_sorted = df_embeddings.sort_values(by='KEYNAME')
    pags_embeddings = get_normalized_embeddings(df_sorted)

    # convert the m-type relationship to a matrix
    filtered_df = df_relationship[df_relationship['GS_A_ID'].isin(valid_nodes) & df_relationship['GS_B_ID'].isin(valid_nodes)]
    results = []
    G = nx.Graph()
    for _, row in filtered_df.iterrows():
        G.add_edge(row['GS_A_ID'], row['GS_B_ID'], weight=row['SIMILARITY'])

    sorted_nodes_by_names = sorted(G.nodes())
    adj_matrix = nx.to_numpy_array(G, nodelist=sorted_nodes_by_names)
    con_matrix = np.concatenate((alpha*pags_embeddings, (1-alpha)*adj_matrix), axis=1)

    results = {}
    # Perform clustering with each algorithm
    for name, algo in clustering_algorithms.items():

        prediction, duration = pred_clusters(algo, name, con_matrix)
        pred_array = np.array(prediction)
        results[name] = {}
        for idx in set(prediction):
            results[name][idx] = ",".join(df_embeddings[pred_array == idx]['KEYNAME'].to_list())

    df = pd.DataFrame.from_dict(results, orient='index').reset_index().rename(columns={'index': 'ID'})
    df.to_csv(save_file_path, index=False)

    if is_visualized:
        visulize_pred_results(pred_dict_path= save_file_path)



def main():

    parser = argparse.ArgumentParser(description ='LLM embedding clustering')
    parser.add_argument('--num', type=int, default=2, help ='the number of groups for the evaluation')
    parser.add_argument('--file_path', type=str, default="Leukemia_drug_resistantVSsensitive.txt", help ='the path to a txt file including a list of gene names. ')
    
    args = parser.parse_args()
    toden_e_predict(pags_txt_path = args.file_path, num_clusters=args.num)



if __name__ == "__main__":

    main()
   



        




