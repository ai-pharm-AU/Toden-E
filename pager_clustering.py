import numpy as np
import pandas as pd
import networkx as nx
import random
import time

import matplotlib.pyplot as plt

from PAGER.PAGER import PAGER
from sentence_transformers import SentenceTransformer, util
from sklearn.cluster import AgglomerativeClustering
from sklearn.manifold import TSNE
import community as community_louvain
from sklearn.cluster import SpectralClustering
from scipy.cluster.hierarchy import linkage, dendrogram

PAGER = PAGER()

def find_validate_set():
    meta_data_path = 'pager_3_all_metadata.csv'
    df = pd.read_csv(meta_data_path)
    print(df.head())

    # talbe_2_graph(file_path = 'topdown2018.txt')
    # Path to your GraphML file
    graph_path = 'subgraph_for_test.graphml'
    G = nx.read_graphml(graph_path)
    children_of_root = list(G.successors('GO:0016817'))
    print(children_of_root)

    list_of_nodes = list(G.nodes())

    # print(counts)
    column_to_check = 'NAME'
    # Construct a regular expression pattern to match any of the elements in name_parts
    pattern = '|'.join(list_of_nodes)

    # Find rows where the name contains any of the substrings in name_parts
    matching_rows = df[df[column_to_check].str.contains(pattern, case=False, na=False)]
    desc_list = matching_rows['DESCRIPTION'].tolist()
    print(matching_rows)
    return desc_list, matching_rows

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

def plot_communities_w_names(G, partition, title=""):
    cmap = plt.get_cmap('Pastel1')  # Corrected method to get colormap
    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(G, seed=42)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                           cmap=cmap, node_color=list(partition.values()))
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    
    # Draw node labels
    labels = {node: str(node) for node in G.nodes()}  # Create a label for each node (using the node itself as the label)
    nx.draw_networkx_labels(G, pos, labels, font_size=8)  # Adjust font_size as needed
    
    plt.title(title)
    plt.axis('off')
    plt.savefig(f"{title.replace(' ', '_')}_results.jpg", dpi=300)  # Adjusted DPI for better image quality

def tsne_2d_plot(pags_embeddings, save_name='test'):

    tsne = TSNE(n_components=2, perplexity=5,  random_state=323)
    embeddings_2d = tsne.fit_transform(pags_embeddings)
    plt.figure(figsize=(10, 8))
    plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])
    plt.title("2D Visualization of Embeddings")
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.savefig(f"{save_name}.jpg")





def main():



    # PAGint = PAGER.pathInt(list(PAG_result.GS_ID)) #Get table of GS relations
    # PAG_member = PAGER.pathMember(list(PAG_result.GS_ID)) #Get table of GS and their Genes

    # array = PAGint.to_numpy() #Turn into numpy array
    # np.savetxt('data.txt', array, fmt='%s', delimiter=', ') #Print the array into 'data.txt'
    # array2 = PAG_member.to_numpy() #Turn into numpy array
    # np.savetxt('data2.txt', array2, fmt='%s', delimiter=', ') #Print the array into 'data2.txt'

    # #Make graph and get degrees of each node
    # G = nx.Graph()
    # for row in array:
    #     node1 = row[0]
    #     node2 = row[2]
    #     weight = float(row[5])
    #     G.add_edge(node1, node2, weight=weight)

    # print(G)
    # # Convert the NetworkX graph to an adjacency matrix (NumPy array)
    # adj_matrix = nx.to_numpy_array(G)

    # # Apply Spectral Clustering
    # # n_clusters is the number of clusters you wish to find in the graph
    # sc = SpectralClustering(n_clusters=2, affinity='precomputed', random_state=42)
    # sc.fit(adj_matrix)

    # partition = {i: sc.labels_[i] for i in range(len(G.nodes()))}

    # # partition = community_louvain.best_partition(G, weight='weight')
    
    # print(partition)

    # color_map = ['blue' if label == 0 else 'red' for label in sc.labels_]
    # pos = nx.spring_layout(G)  # positions for all nodes

    # nx.draw(G, pos, node_color=color_map, with_labels=True, edge_color='gray')
    # plt.show()
    # plot_communities(G, partition, "sc_pags_clustering"




    # desc_list = PAG_result['DESCRIPTION'].tolist()
    desc_list, desc_df = find_validate_set()
    print(desc_df.head)
    print(desc_list)
    # embedder = SentenceTransformer("all-MiniLM-L6-v2")
    # pags_embeddings = embedder.encode(desc_list)
    
    def get_embedding(desc):
        embedder = SentenceTransformer("all-MiniLM-L6-v2")
        return embedder.encode(desc)
    
    desc_df['EMBEDDING'] = desc_df['DESCRIPTION'].apply(get_embedding)
    desc_df['KEYNAME'] = desc_df['NAME'].str.split(" ").str[0]
    pags_embeddings = np.stack(desc_df['EMBEDDING'].values)

    # Normalize the embeddings to unit length
    pags_embeddings = pags_embeddings / np.linalg.norm(pags_embeddings, axis=1, keepdims=True)
    
    tsne_2d_plot(pags_embeddings)
    Z = linkage(pags_embeddings, 'ward')
    # hierarchy_clustering(pags_embeddings)
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Names')
    plt.ylabel('Distance')
    dendrogram(Z, labels=desc_df['KEYNAME'].values, leaf_rotation=90.)
    plt.show()


def hierarchy_clustering(embeddings):

    Z = linkage(embeddings, method='ward', metric='euclidean')
    # Plot the dendrogram
    # plt.figure(figsize=(20, 16))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Data Points')
    plt.ylabel('Distance')

    dendrogram(Z)
    plt.show()


def hierarchical_clustering_sklearn(desc_list, embeddings):
    # Perform kmean clustering
    clustering_model = AgglomerativeClustering(
        n_clusters=None, distance_threshold=1.5
    )  # , affinity='cosine', linkage='average', distance_threshold=0.4)
    clustering_model.fit(embeddings)
    cluster_assignment = clustering_model.labels_

    clustered_sentences = {}
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        if cluster_id not in clustered_sentences:
            clustered_sentences[cluster_id] = []

        clustered_sentences[cluster_id].append(desc_list[sentence_id])

    for i, cluster in clustered_sentences.items():
        print("Cluster ", i + 1)
        print(cluster)
        print("")

    # print("Start clustering")
    # start_time = time.time()

    # # Two parameters to tune:
    # # min_cluster_size: Only consider cluster that have at least 25 elements
    # # threshold: Consider sentence pairs with a cosine-similarity larger than threshold as similar
    # clusters = util.community_detection(pags_embeddings, min_community_size=5, threshold=0.70)
    # print(clusters)
    # print("Clustering done after {:.2f} sec".format(time.time() - start_time))

    # # Print for all clusters the top 3 and bottom 3 elements
    # for i, cluster in enumerate(clusters):
    #     print("\nCluster {}, #{} Elements ".format(i + 1, len(cluster)))
    #     for sentence_id in cluster[0:3]:
    #         print("\t", desc_list[sentence_id])
    #     print("\t", "...")
    #     for sentence_id in cluster[-3:]:
    #         print("\t", desc_list[sentence_id])



if __name__ == "__main__":
    main()
