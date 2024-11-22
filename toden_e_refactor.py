from pathlib import Path
import networkx as nx
import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import adjusted_rand_score
from matplotlib import pyplot as plt
import seaborn as sns
import argparse
from time import time

# Base path for the data files
DATA_PATH = Path("go_metadata")

class GraphAnalyzer:
    def __init__(self, graph_path: str):
        self.graph_path = graph_path
        self.graph = nx.read_graphml(graph_path)

    def analyze_outdegree_distribution(self, zoomed: bool = False):
        outdegrees = list(dict(self.graph.out_degree()).values())
        filtered_outdegrees = [x for x in outdegrees if x != 0]
        counts, bins = np.histogram(filtered_outdegrees, bins=np.arange(min(filtered_outdegrees), max(filtered_outdegrees)+1))
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(filtered_outdegrees, bins=bins, edgecolor='black')
        ax.set_xlabel("Outdegree")
        ax.set_ylabel("Count")
        ax.set_title("Outdegree Distribution")

        if zoomed:
            self._add_zoomed_insets(ax, filtered_outdegrees, bins)
        
        plt.grid(True)
        plt.savefig(f"{self.graph_path.stem}_outdegree_distribution.png")

    def _add_zoomed_insets(self, ax, data, bins):
        """ Add zoomed-in insets for specific ranges in the distribution plot """
        for zoom_range in [(10, 100), (5, 10)]:
            ax_ins = plt.axes([0.6, 0.2, 0.2, 0.2])
            ax_ins.hist(data, bins=bins, edgecolor='black')
            ax_ins.set_xlim(*zoom_range)
            ax_ins.set_title(f"Zoomed: {zoom_range}")

    def get_adjacency_matrix(self):
        return nx.to_numpy_array(self.graph, nodelist=sorted(self.graph.nodes()))


class EmbeddingProcessor:
    def __init__(self, embeddings_df: pd.DataFrame):
        self.embeddings_df = embeddings_df
        self.embeddings_df['KEYNAME'] = self.embeddings_df['NAME'].str.split(" ").str[0]
        self.sorted_embeddings = self.embeddings_df.sort_values(by='KEYNAME')

    def get_normalized_embeddings(self):
        embeddings = self.sorted_embeddings['EMBEDDING'].tolist()
        return (embeddings - np.mean(embeddings, axis=0)) / np.std(embeddings, axis=0)

    def get_similarity_matrix(self):
        return cosine_similarity(self.get_normalized_embeddings())


class ClusteringEvaluator:
    def __init__(self, algorithms: dict, num_clusters=2):
        self.algorithms = algorithms
        self.num_clusters = num_clusters
        self.results = {}

    def evaluate(self, data_matrix):
        for name, algo in self.algorithms.items():
            print(f"Evaluating with {name}...")
            start_time = time()
            algo.fit(data_matrix)
            duration = time() - start_time
            labels = algo.labels_
            self.results[name] = {
                "labels": labels,
                "duration": duration,
                "algorithm": name
            }
        return self.results

    def display_results(self):
        for algo_name, result in self.results.items():
            print(f"Algorithm: {algo_name}, Duration: {result['duration']} seconds")


class Visualizer:
    @staticmethod
    def violin_plot(data: pd.DataFrame, x: str, y: str, hue: str, save_path: str):
        plt.figure(figsize=(12, 6))
        sns.violinplot(x=x, y=y, hue=hue, data=data, cut=0)
        plt.title("Violin Plot of Clustering Evaluation")
        plt.savefig(save_path)
        plt.close()


def main(file_path: str, num_clusters: int):
    # Load gene data from file
    valid_nodes = pd.read_csv(file_path, header=None).squeeze().tolist()
    
    # Load relationships and embeddings
    df_relationship = pd.read_csv(DATA_PATH / "m_type_biological_process.txt", sep="\t")
    embeddings_df = pd.read_csv(DATA_PATH / "embeddings.csv")  # Placeholder path

    # Graph Analysis
    graph_analyzer = GraphAnalyzer("2024_biological_process_graph_w_verification.graphml")
    adj_matrix = graph_analyzer.get_adjacency_matrix()

    # Embedding Processing
    embedding_processor = EmbeddingProcessor(embeddings_df)
    normalized_embeddings = embedding_processor.get_normalized_embeddings()

    # Clustering
    clustering_algorithms = {
        "Agglomerative": AgglomerativeClustering(n_clusters=num_clusters)
    }
    evaluator = ClusteringEvaluator(clustering_algorithms, num_clusters)
    combined_matrix = np.hstack((0.5 * normalized_embeddings, 0.5 * adj_matrix))
    results = evaluator.evaluate(combined_matrix)

    # Display results
    evaluator.display_results()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LLM embedding clustering')
    parser.add_argument('--num', type=int, default=2, help='Number of clusters')
    parser.add_argument('--file_path', type=str, help='Path to gene data file')
    args = parser.parse_args()
    main(args.file_path, args.num)

 