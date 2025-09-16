#!/usr/bin/env python3
"""
Example usage of the Tree Reaction Layout Algorithm
Demonstrates how to use the algorithm with sample data
"""

from tree_layout_algorithm import TreeLayoutAlgorithm
import math

def main():
    # Create algorithm instance
    tree_layout = TreeLayoutAlgorithm(
        branch_angle=math.radians(35),  # 35 degree spread
        branch_factor=0.85,             # 85% length scaling
        min_branch_length=30.0,         # Minimum branch length
        max_depth=10000                 # No depth limit
    )
    
    # Example tree data - a simple organizational chart
    nodes = {
        'CEO': {'name': 'Chief Executive Officer'},
        'CTO': {'name': 'Chief Technology Officer'},
        'CFO': {'name': 'Chief Financial Officer'},
        'Dev1': {'name': 'Senior Developer'},
        'Dev2': {'name': 'Junior Developer'},
        'QA': {'name': 'Quality Assurance'},
        'Acc1': {'name': 'Senior Accountant'},
        'Acc2': {'name': 'Junior Accountant'}
    }
    
    links = [
        {'from': 'CEO', 'to': 'CTO'},
        {'from': 'CEO', 'to': 'CFO'},
        {'from': 'CTO', 'to': 'Dev1'},
        {'from': 'CTO', 'to': 'Dev2'},
        {'from': 'CTO', 'to': 'QA'},
        {'from': 'CFO', 'to': 'Acc1'},
        {'from': 'CFO', 'to': 'Acc2'}
    ]
    
    # Layout the tree
    positions = tree_layout.layout_tree(nodes, links, root_x=400, root_y=100)
    
    # Print results
    print("Tree Layout Results:")
    print("=" * 50)
    for node_id, (x, y) in positions.items():
        node_name = nodes[node_id]['name']
        print(f"{node_name:25} ({node_id:5}): ({x:6.1f}, {y:6.1f})")
    
    print("\nTree Structure:")
    print("=" * 50)
    print("CEO")
    print("├── CTO")
    print("│   ├── Dev1")
    print("│   ├── Dev2")
    print("│   └── QA")
    print("└── CFO")
    print("    ├── Acc1")
    print("    └── Acc2")

if __name__ == "__main__":
    main()
