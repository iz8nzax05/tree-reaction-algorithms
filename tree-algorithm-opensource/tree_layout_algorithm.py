#!/usr/bin/env python3
"""
Tree Reaction Layout Algorithm
A novel recursive tree positioning algorithm for hierarchical data visualization

Author: PathForge Developer
License: MIT License
Description: This algorithm creates natural-looking tree layouts using recursive branch placement
             with trigonometric positioning, dynamic scaling, and natural growth patterns.

Key Features:
- Recursive branch angle calculation with configurable spread
- Trigonometric positioning using math.cos/sin for natural angles
- Dynamic scaling based on node count and tree depth
- Length decay with random variation for organic appearance
- Support for arbitrary tree structures (not just binary trees)
- Natural tree growth patterns similar to biological trees

This algorithm is unique in that it focuses on natural tree aesthetics rather than
compactness or tidiness, creating visually appealing hierarchical layouts.
"""

import math
import random
from typing import Dict, List, Tuple, Optional, Set


class TreeLayoutAlgorithm:
    """
    Tree Reaction Layout Algorithm
    
    Creates natural-looking tree layouts by recursively placing nodes using
    trigonometric positioning and natural branch angles.
    """
    
    def __init__(self, 
                 branch_angle: float = math.radians(35),
                 branch_factor: float = 0.85,
                 min_branch_length: float = 30.0,
                 max_depth: int = 10000):
        """
        Initialize the tree layout algorithm.
        
        Args:
            branch_angle: Maximum spread angle for branches (in radians)
            branch_factor: Length scaling factor for child branches
            min_branch_length: Minimum length before stopping branch creation
            max_depth: Maximum recursion depth
        """
        self.branch_angle = branch_angle
        self.branch_factor = branch_factor
        self.min_branch_length = min_branch_length
        self.max_depth = max_depth
        
        # Dynamic scaling parameters
        self.scaling_configs = {
            (0, 10): {"base_length": 100, "base_spacing": 60},
            (11, 30): {"base_length": 120, "base_spacing": 80},
            (31, 60): {"base_length": 150, "base_spacing": 100},
            (61, float('inf')): {"base_length": 180, "base_spacing": 120}
        }
    
    def calculate_dynamic_parameters(self, node_count: int) -> Tuple[float, float]:
        """
        Calculate dynamic tree parameters based on node count.
        
        Args:
            node_count: Total number of nodes in the tree
            
        Returns:
            Tuple of (base_length, base_spacing)
        """
        for (min_count, max_count), config in self.scaling_configs.items():
            if min_count <= node_count <= max_count:
                return config["base_length"], config["base_spacing"]
        
        # Fallback to largest configuration
        return self.scaling_configs[(61, float('inf'))]["base_length"], \
               self.scaling_configs[(61, float('inf'))]["base_spacing"]
    
    def build_tree_structure(self, root_node: str, nodes: Dict, links: List[Dict]) -> Dict[str, List[str]]:
        """
        Build tree structure from node links.
        
        Args:
            root_node: The root node ID
            nodes: Dictionary of all nodes
            links: List of link dictionaries with 'from' and 'to' keys
            
        Returns:
            Dictionary mapping node IDs to their children
        """
        tree_structure = {}
        
        # Initialize all nodes
        for node_id in nodes.keys():
            tree_structure[node_id] = []
        
        # Build parent-child relationships from links
        for link in links:
            parent = link.get('from')
            child = link.get('to')
            if parent in tree_structure and child in tree_structure:
                tree_structure[parent].append(child)
        
        return tree_structure
    
    def find_root_nodes(self, nodes: Dict, links: List[Dict]) -> List[str]:
        """
        Find root nodes (nodes with no incoming links).
        
        Args:
            nodes: Dictionary of all nodes
            links: List of link dictionaries
            
        Returns:
            List of root node IDs
        """
        all_node_ids = set(nodes.keys())
        linked_to = set()
        
        for link in links:
            if 'to' in link:
                linked_to.add(link['to'])
        
        root_nodes = list(all_node_ids - linked_to)
        
        # If no clear roots, use first node as fallback
        if not root_nodes:
            root_nodes = [list(nodes.keys())[0]]
        
        return root_nodes
    
    def place_nodes_recursively(self, 
                               node_id: str,
                               tree_structure: Dict[str, List[str]],
                               start_x: float,
                               start_y: float,
                               angle: float,
                               length: float,
                               depth: int,
                               positioned_nodes: Set[str],
                               node_positions: Dict[str, Tuple[float, float]]) -> None:
        """
        Recursively place nodes using tree reaction algorithm.
        
        This is the core of the algorithm - it places each node based on its parent's
        position and angle, creating natural branch patterns.
        
        Args:
            node_id: Current node being positioned
            tree_structure: Dictionary mapping nodes to their children
            start_x, start_y: Starting position for this branch
            angle: Current branch angle
            length: Current branch length
            depth: Current recursion depth
            positioned_nodes: Set of already positioned nodes
            node_positions: Dictionary to store final node positions
        """
        # Stop if we've reached max depth or minimum length
        if depth >= self.max_depth or length < self.min_branch_length:
            return
        
        # Get children for this node
        children = tree_structure.get(node_id, [])
        
        if not children:
            return  # No children, end of branch
        
        # Calculate number of branches (children)
        num_branches = len(children)
        
        # Place each child node
        for i, child_id in enumerate(children):
            # Skip if already positioned
            if child_id in positioned_nodes:
                continue
            
            # Calculate angle for this branch
            if num_branches == 1:
                delta = 0  # Single child goes straight up
            else:
                # Spread branches evenly with configurable angle
                spread = self.branch_angle * 2
                delta = (i / (num_branches - 1)) * spread - spread / 2
            
            child_angle = angle + delta
            
            # Calculate position using trigonometry
            end_x = start_x + length * math.cos(child_angle)
            end_y = start_y + length * math.sin(child_angle)
            
            # Store the child's position
            node_positions[child_id] = (end_x, end_y)
            positioned_nodes.add(child_id)
            
            # Calculate new length (shorter for next level with random variation)
            new_length = length * random.uniform(0.8, self.branch_factor)
            
            # Recursively place children of this child
            self.place_nodes_recursively(
                child_id, tree_structure, end_x, end_y,
                child_angle, new_length, depth + 1,
                positioned_nodes, node_positions
            )
    
    def layout_tree(self, 
                   nodes: Dict, 
                   links: List[Dict], 
                   root_x: float = 600, 
                   root_y: float = 650) -> Dict[str, Tuple[float, float]]:
        """
        Main method to layout a tree structure.
        
        Args:
            nodes: Dictionary of all nodes (format: {node_id: node_data})
            links: List of link dictionaries (format: [{'from': 'node1', 'to': 'node2'}])
            root_x, root_y: Position for the root node
            
        Returns:
            Dictionary mapping node IDs to (x, y) positions
        """
        if not nodes:
            return {}
        
        # Calculate dynamic parameters based on node count
        total_nodes = len(nodes)
        base_length, base_spacing = self.calculate_dynamic_parameters(total_nodes)
        
        # Find root nodes
        root_nodes = self.find_root_nodes(nodes, links)
        
        # If multiple roots, use the first one (could be enhanced to handle multiple roots)
        root_node = root_nodes[0]
        
        # Build tree structure from links
        tree_structure = self.build_tree_structure(root_node, nodes, links)
        
        # Initialize position tracking
        node_positions = {}
        positioned_nodes = set()
        
        # Place root node
        node_positions[root_node] = (root_x, root_y)
        positioned_nodes.add(root_node)
        
        # Recursively place all other nodes
        self.place_nodes_recursively(
            root_node, tree_structure, root_x, root_y,
            -math.pi / 2,  # Start pointing upward
            base_length, 1, positioned_nodes, node_positions
        )
        
        return node_positions


# Example usage and testing
def example_usage():
    """
    Example of how to use the TreeLayoutAlgorithm.
    """
    # Create algorithm instance
    tree_layout = TreeLayoutAlgorithm(
        branch_angle=math.radians(35),  # 35 degree spread
        branch_factor=0.85,             # 85% length scaling
        min_branch_length=30.0,         # Minimum branch length
        max_depth=10000                 # No depth limit
    )
    
    # Example tree data
    nodes = {
        '1': {'name': 'Root'},
        '2': {'name': 'Child 1'},
        '3': {'name': 'Child 2'},
        '4': {'name': 'Grandchild 1'},
        '5': {'name': 'Grandchild 2'},
        '6': {'name': 'Great-grandchild'}
    }
    
    links = [
        {'from': '1', 'to': '2'},
        {'from': '1', 'to': '3'},
        {'from': '2', 'to': '4'},
        {'from': '2', 'to': '5'},
        {'from': '4', 'to': '6'}
    ]
    
    # Layout the tree
    positions = tree_layout.layout_tree(nodes, links)
    
    # Print results
    print("Tree Layout Results:")
    for node_id, (x, y) in positions.items():
        print(f"Node {node_id}: ({x:.1f}, {y:.1f})")
    
    return positions


if __name__ == "__main__":
    # Run example
    example_usage()
