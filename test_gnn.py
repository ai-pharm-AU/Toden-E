from torch_geometric.loader import NeighborSampler
from torch_geometric.datasets import Planetoid
import torch_geometric.transforms as T

# Load a dataset (for demonstration purposes)
dataset = Planetoid(root='/tmp/Cora', name='Cora', transform=T.NormalizeFeatures())

data = dataset[0]

# Define a NeighborSampler
loader = NeighborSampler(data.edge_index, sizes=[10, 5], batch_size=128, shuffle=True, num_nodes=data.num_nodes)

# Example training loop
for batch_size, n_id, adjs in loader:
    # `adjs` holds a list of `(edge_index, e_id, size)` tuples.
    edge_index, _, size = adjs[0]
    
    # Subsampled adjacency matrix
    # Target nodes are mapped to the first `batch_size` entries.
    # Input nodes are mapped to the remaining entries.
    
    # Select the features of the sampled nodes, and labels of the target nodes
    x = data.x[n_id]  # Node features of the sampled nodes
    y = data.y[n_id[:batch_size]]  # Labels of the target nodes
    
    # Forward pass with subgraph
    out = model(x, edge_index)
    loss = criterion(out, y)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

