def find_levels_and_same_tree(G, node1, node2):
    # Find all root nodes (no incoming edges)
    roots = [n for n, d in G.in_degree() if d == 0]
    
    # Data structure to store the level of each node, initialized with None
    levels = {node: None for node in G.nodes()}
    
    # Data structure to track which tree (root) each node belongs to
    node_trees = {node: None for node in G.nodes()}
    
    # Perform BFS from each root to find levels and tree membership
    for root in roots:
        queue = deque([(root, 0)])  # Queue of tuples (node, level)
        while queue:
            current_node, level = queue.popleft()
            # Update level and tree membership if not already visited
            if levels[current_node] is None:
                levels[current_node] = level
                node_trees[current_node] = root
                # Add neighbors to the queue
                for neighbor in G.neighbors(current_node):
                    queue.append((neighbor, level + 1))
    
    # Check if node1 and node2 are in the same tree and find their levels
    same_tree = node_trees[node1] == node_trees[node2]
    level1 = levels[node1]
    level2 = levels[node2]
    
    return same_tree, level1, level2
