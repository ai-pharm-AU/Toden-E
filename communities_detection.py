import argparse
import textwrap
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import community as community_louvain
import numpy as np
import ast

from networkx.algorithms.community import girvan_newman
from sklearn.cluster import SpectralClustering, AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, mean_squared_error, r2_score , accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier


ALGORITHMS = ['louvain', 'girvan_newman', 'spectral_clustering', 'agglomerative_clustering']
# ALGORITHMS = ['agglomerative_clustering']
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


def plot_communities(G, partition, title="", node_size=40, edge_width=1.0):
    title_fontsize = 18

    cmap = plt.colormaps.get_cmap('tab10')  # Get the colormap
    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(G, seed=42)  # Layout for positioning nodes
    
    # Plot the nodes with customizable node size
    nx.draw_networkx_nodes(
        G, pos, 
        nodelist=partition.keys(), 
        node_size=node_size,  # Control node size
        cmap=cmap, 
        node_color=list(partition.values())
    )
    
    # Plot the edges with customizable edge width
    nx.draw_networkx_edges(
        G, pos, 
        alpha=0.5, 
        width=edge_width  # Control edge width
    )
    
    plt.title(title, fontsize = title_fontsize)
    plt.axis('off')  # Turn off axis
    plt.savefig(f"{title.replace(' ', '_')}_results.jpg")  # Save the figure
    plt.close()  # Close the plot


def evaluate_algorithm(true_labels, pred_labels):
    ari = adjusted_rand_score(true_labels, pred_labels)
    nmi = normalized_mutual_info_score(true_labels, pred_labels)
    return ari, nmi


def generate_sbm_graph(sizes, p_within, p_between):
    # Dynamically create the probability matrix for connections
    prob_matrix = [[p_within if i == j else p_between for j in range(len(sizes))] for i in range(len(sizes))]
    # Generate the graph
    G = nx.stochastic_block_model(sizes, prob_matrix, seed=323)
    true_labels = []
    for label_index, size in enumerate(sizes):
        true_labels.extend([label_index] * size)
    return G, true_labels


def run_eval(algorithm, G, true_labels, is_plot=True, node_size=40, edge_width=1.0):
    
    if algorithm == 'louvain':
        partition = community_louvain.best_partition(G)
        title = "Louvain Method"
    elif algorithm == 'girvan_newman':
        gn_comm = next(girvan_newman(G))
        partition = {node: i for i, comm in enumerate(gn_comm) for node in comm}
        title = "Girvan-Newman Algorithm"
    elif algorithm == 'spectral_clustering':
        adj_matrix = nx.to_numpy_array(G)
        sc = SpectralClustering(n_clusters=3, affinity='precomputed', n_init=100, random_state=42)
        sc.fit(adj_matrix)
        partition = {i: sc.labels_[i] for i in range(len(G.nodes()))}
        title = "Spectral Clustering"
    elif algorithm == "agglomerative_clustering":
        adj_matrix = nx.to_numpy_array(G)
        ac = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')
        ac.fit(adj_matrix)
        partition = {i: ac.labels_[i] for i in range(len(G.nodes()))}
        title = "Agglomerative Clustering"

    else:
        raise ValueError("Invalid algorithm")
    
    # print(partition)
    
    labels = [partition[node] for node in G.nodes()]
    ari, nmi = evaluate_algorithm(true_labels, labels)

    if is_plot:
        print(f"{title}: ARI = {ari}, NMI = {nmi}")
        print(partition)
        plot_communities(G, partition, title=title, node_size=node_size, edge_width=edge_width)

    return ari, nmi

# Function to plot heatmap for given metric ('ARI' or 'NMI')
def plot_heatmap_for_metric(metric, results_df, prefix = "sbm_50_50"):
    label_fontsize = 18
    font_size = 16
    annot_font_size = 16
    colorbar_font_size = 16

    for alg in results_df['Algorithm'].unique():
        # Filter DataFrame for the current algorithm
        alg_data = results_df[results_df['Algorithm'] == 'spectral_clustering']
        
        # Pivot the data to get a matrix where rows are p_within, columns are p_between, and values are the metric
        pivot_table = alg_data.pivot(index="p_within", columns="p_between", values=metric)
        
        # Convert the data to numeric in case there are any non-numeric values
        pivot_table = pivot_table.apply(pd.to_numeric, errors='coerce')

        pivot_table = pivot_table.round(2)

        pivot_table = pivot_table.fillna(0) 

        mask = np.triu(np.ones_like(pivot_table, dtype=bool))
    
        print(pivot_table)


        # Plotting the heatmap
        plt.figure(figsize=(10, 8))
        heatmap = sns.heatmap(
            pivot_table, annot=True, cmap="coolwarm", fmt=".2f", mask=mask, cbar=True,
            annot_kws={"size": annot_font_size}  # Control the font size of the annotation
        )
        
        # Modify the font of the color bar (color scale)
        colorbar = heatmap.collections[0].colorbar
        colorbar.ax.yaxis.set_tick_params(labelsize=colorbar_font_size)  
        # plt.title(f"{alg.capitalize()} - {metric}")
        plt.ylabel('Intra-cluster connection probability', fontsize=label_fontsize)
        plt.xlabel('Inter-cluster connection probability', fontsize=label_fontsize)
        plt.xticks(fontsize=font_size)  # Change font size for x-axis
        plt.yticks(fontsize=font_size)  # Ch
        plt.tight_layout()  # Ensure the layout fits well
        plt.savefig(f"{prefix}_{alg}_{metric}_heatmap.jpg")
        plt.close()  # Close the figure to avoid inline display if not needed

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


def eval_cross_all_for_3_methods(args):
    exp = f"sbm_{'_'.join(str(item) for item in args.sizes)}"
    save_csv_name = f'{exp}_clustering_results.csv'

    results = []
    for alg in ALGORITHMS:
        for i in range(10):
            p_within = (i+1) / 10
            for j in range(i+1):
                p_between= (j+1) / 10
                G, true_labels = generate_sbm_graph(args.sizes, p_within, p_between)
                print(f"{alg}: {p_within}, {p_between}")
                ari, nmi = run_eval(alg, G, true_labels)
                # Append results to the DataFrame
                results.append({'Algorithm': alg, 'p_within': p_within, 'p_between': p_between, 'ARI': ari, 'NMI': nmi})
    

    # Save the results to a CSV file
    results_df = pd.DataFrame(results)
    results_df.to_csv(save_csv_name, index=False)
    return exp,save_csv_name

def plot_heatmaps(clustering_result_file, exp):
    results_df = pd.read_csv(clustering_result_file)
    for metric in ['ARI']: #, 'NMI'
        plot_heatmap_for_metric(metric, results_df, exp)


def generate_all_sbm_graphs(sizes=None):
    if sizes is None:
        sizes = [50, 50]

    exp = f"sbm_{'_'.join(str(item) for item in sizes)}"
    save_csv_name = f'{exp}_distribution_of_connection_results.csv'

    community_dict = {}
    columns = ['p_within', 'p_between', 'node', 'connection']
    connection_df = pd.DataFrame(columns=columns)

    for i in range(10):
        p_within = (i+1) / 10
        for j in range(i+1):
            p_between= (j+1) / 10
            G, true_labels = generate_sbm_graph(sizes, p_within, p_between)

            # Generate community labels based on sizes
            start = 0
            for label, size in enumerate(sizes):
                for node in range(start, start + size):
                    community_dict[node] = label
                start += size

            for node_id in range(G.number_of_nodes()):
                # Choose a target vertex
                target_vertex = int(node_id)

                # Find the existing edges among the neighbors of the target vertex
                edges, neighbors = find_edges_among_neighbors(G, target_vertex)
                number_of_neighbors = len(neighbors)
                result = {'p_within': p_within, 'p_between': p_between, 'node': target_vertex, 'connection': len(edges) *2 / (number_of_neighbors*(number_of_neighbors-1))}
                connection_df = connection_df.append(result, ignore_index=True)

                print(f"Edges among neighbors of vertex {target_vertex}: {edges}")

            plot_communities_w_names(G, community_dict, f"{exp}_p_within_{p_within}_p_between_{p_between}")

    connection_df.to_csv(save_csv_name, index=False)

def plot_all_connection_dist(df, exp):

    desired_width_px = 1200
    desired_height_px = 800
    dpi = 100  # Desired DPI

    # Calculate figure size in inches
    figsize_inches = (desired_width_px / dpi, desired_height_px / dpi)

    df['node'] = df['node'].astype(int)
    for i in range(10):
        p_within = (i+1) / 10
        for j in range(i+1):
            p_between= (j+1) / 10
            
            filtered_df = df[(df['p_within'] == p_within) & (df['p_between'] == p_between)][['node', 'connection']]
            plt.figure(figsize=figsize_inches)
            sns.displot(filtered_df, x="connection", kind="kde", fill=True)
            # sns.barplot(x="node", y="connection", data=filtered_df, palette="viridis")
            plt.xlim(0, 1)
            title_text = f"Distribution of Connection Values for p_within={p_within} and p_between={p_between}"
            wrapped_title = textwrap.fill(title_text, width=50)
            plt.title(wrapped_title)
            plt.xlabel("Connection Strength")
            plt.ylabel("Density")
            plt.tight_layout()
            plt.savefig(f"{exp}_p_within_{p_within}_p_between_{p_between}_distribution.jpg", dpi=dpi)
            plt.close()

def merge_clustering_results():

    df = pd.DataFrame()
    for exp in ['50_50', '70_30', '90_10']:
        exp_name = f"sbm_{exp}"

        df_exp = pd.read_csv(f"{exp_name}_clustering_results.csv")
        df_dist = pd.read_csv(f"{exp_name}_distribution_of_connection_results.csv")

        # Add a column to distinguish the data sets
        df_exp['exp'] = exp_name

        column_dist = []

        for idx, row in df_exp.iterrows():
            filtered_df = df_dist[(df_dist['p_within'] == row['p_within']) & (df_dist['p_between'] == row['p_between'])]
            dist_values_list = filtered_df['connection'].tolist()
            column_dist.append(dist_values_list)
        df_exp['distribution'] = column_dist
        df = df_exp if df.empty else pd.concat([df, df_exp], ignore_index=True)

    df.to_csv("synthetic_exp_distribution_results.csv", index=False)
    print(df)


def to_float_list(value):
    # If the value is a string representation of a list, convert it to a list
    if isinstance(value, str):
        value = ast.literal_eval(value)
    # Convert list elements to floats
    return [float(item) for item in value]


def train_two_group_dist_model(csv_path = "synthetic_exp_distribution_results.csv"):
    df = pd.read_csv(csv_path)

    df_sc = df[df['Algorithm'] == 'spectral_clustering']

    # Apply the conversion to the 'list_column'
    df_sc['distribution'] = df_sc['distribution'].apply(to_float_list)

    X = df_sc['distribution']
    y = df_sc['ARI']
    

    # # Example dataset
    # X = [[1.2, 2.3, 3.4], [2.2, 3.5], [4.5, 5.5, 6.7, 7.8], [2.1]]
    # y = [3.1, 2.2, 6.3, 1.1]

    # Transforming variable-length lists into fixed-length features
    # Here, we use mean and standard deviation as example features
    X_transformed = [[np.mean(lst), np.std(lst) if len(lst) > 1 else 0] for lst in X]

    # Splitting dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=42)

    # Training a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Making predictions
    y_pred = model.predict(X_test)

    print(y_pred)
    # Evaluating the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse}, R2: {r2}")


def train_binary_two_group_dist_group(csv_path = "synthetic_exp_distribution_results.csv", method = 'logistic_regression'):
    
    df = pd.read_csv(csv_path)

    df_sc = df[df['Algorithm'] == 'spectral_clustering']

    # Apply the conversion to the 'list_column'
    df_sc['distribution'] = df_sc['distribution'].apply(to_float_list)

    X = df_sc['distribution']
    y_continuous = df_sc['ARI']
    y_binary = (y_continuous >= 0.7).astype(int)

    X_transformed = [[np.mean(lst), np.std(lst) if len(lst) > 1 else 0] for lst in X]

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_transformed, y_binary, test_size=0.25, random_state=42)

    # Initialize and train the logistic regression model
    if method == 'logistic_regression':
        model = LogisticRegression()
    elif method == 'svm':
        model = SVC(kernel='linear')
    elif method == 'reandom_forest':
        model = RandomForestClassifier(n_estimators=100, random_state=323)
    elif method == 'knn':
        model = KNeighborsClassifier(n_neighbors=2)

    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # Assuming `predictions` and `y_test` are available from the previous steps
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    print(f"Method {method}:")
    print(f"Accuracy: {accuracy:.02f}")
    print(f"Precision: {precision:.02f}")
    print(f"Recall: {recall:.02f}")
    print(f"F1 Score: {f1:.02f}")

def min_max_normalize(lst, min_value=0, max_value=1):
    min_lst = min(lst)
    max_lst = max(lst)
    return [
        (x - min_lst) / (max_lst - min_lst) * (max_value - min_value)
        + min_value
        for x in lst
    ]

def plot_distribution_train(csv_path = "synthetic_exp_distribution_results.csv", algo ="girvan_newman"):
    df = pd.read_csv(csv_path)
    df_sc = df[df['Algorithm'] == algo]

    def to_float_list(value):
        # If the value is a string representation of a list, convert it to a list
        if isinstance(value, str):
            value = ast.literal_eval(value)
        # Convert list elements to floats
        return [float(item) for item in value]

    # Apply the conversion to the 'list_column'
    df_sc['distribution'] = df_sc['distribution'].apply(to_float_list)

    X = df_sc['distribution']
    y = df_sc['ARI']

    X_transformed = [[np.mean(lst), np.var(lst) if len(lst) > 1 else 0] for lst in X]
    X_means = [ item[0] for item in X_transformed ]
    X_stds = [ item[1] for item in X_transformed ]

    X_stds_normalized = [x*1000 for x in min_max_normalize(X_stds)]

   # Creating the plot
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(X_means, y, s=X_stds_normalized, alpha=0.7)  # s controls the size of scatter points
    plt.title('ARI Score vs Mean with Var as Size')
    plt.xlabel('Mean')
    plt.ylabel('ARI Score')

    # Adding a colorbar to represent the std sizes, if desired
    plt.colorbar(scatter, label='Var')
    plt.savefig(f"ari_vs_mean(var)_distribution_study_{algo}.jpg", dpi=300)
    # plt.show()



def main():

    parser = argparse.ArgumentParser(description ='Community detection!!')
    parser.add_argument('--alg', type=str, default="louvain", help ='the algorithm to be evaluated.')
    parser.add_argument('--sizes', nargs='+', type=int, help='List of sizes (integers).')
    parser.add_argument('--p_within', type=float, default=0.3, help ='the probability of edge creation within a cluster.')
    parser.add_argument('--p_between', type=float, default=0.1, help ='the probability for edge creation between the clusters. ')
    args = parser.parse_args()

    # multiple evaluations 
    print(args.sizes)
    # exp = f"sbm_{'_'.join(str(item) for item in args.sizes)}"
    # save_csv_name = f'{exp}_distribution_of_connection_results.csv'
    # save_csv_name = f'{exp}_clustering_results.csv'
    # exp = f"sbm_{'_'.join(str(item) for item in args.sizes)}"
    # plot_heatmaps(save_csv_name, exp)

    # algorithm = args.alg

    for algo in ['louvain', 'girvan_newman', 'spectral_clustering']: # 
        G, true_labels = generate_sbm_graph(args.sizes, args.p_within, args.p_between)
        print(true_labels)
        ground_truth_partition = dict(enumerate(true_labels))
        # print(ground_truth_partition)
        plot_communities(G, ground_truth_partition, title="Ground Truth", node_size=100, edge_width=0.4)
        ari, nmi = run_eval(algo, G, true_labels, is_plot=True, node_size=100, edge_width=0.4)
    
    # generate_all_sbm_graphs(args.sizes)
    # df = pd.read_csv(save_csv_name)
    # plot_all_connection_dist(df, exp)

    # merge_clustering_results()

    # train_two_group_dist_model()
    # banary_classifier = [ 'knn'] # 'logistic_regression' , 'svm', 'reandom_forest',
    # for method in banary_classifier:
    #     train_binary_two_group_dist_group(method=method)

    # for algo in ['louvain', 'girvan_newman', 'spectral_clustering']:
    #     plot_distribution_train(algo=algo)

if __name__ == "__main__":
    main() 

# Example usage:
# python communities_detection.py --sizes 50 50 --p_within 0.5 --p_between
