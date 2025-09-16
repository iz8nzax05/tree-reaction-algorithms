Tree Reaction Algorithms

A collection of novel recursive tree algorithms for hierarchical data visualization and real-time tree growth simulation. These algorithms create natural-looking trees using trigonometric positioning and natural growth patterns.

- What's Included

- 1. tree_layout_algorithm.py - Practical Tree Layout
A production-ready algorithm for positioning nodes in hierarchical structures, used in PathForge.

- 2. tree_reaction_simulation.py - Real-time Tree Growth Simulation  
The original pygame-based fractal tree growth simulation that inspired the layout algorithm.

- The Story Behind These Algorithms

These algorithms were discovered in an archived development file that contained a nice solution. The original tree reaction.py was a real-time fractal tree growth simulation using pygame. The layout algorithm was later adapted from this simulation for practical use in the PathForge interactive story creation tool.

- Tree Reaction Simulation

The simulation demonstrates the core concepts in real-time:

- Animated Growth. Watch trees grow organically over time
- Recursive Branching. Each branch spawns 2-3 children with natural angles
- Performance Optimization. Uses static rendering for fully grown branches
- Visual Effects. Color gradients and thickness variations based on depth
- Interactive Controls. Multiple growth modes and color options

- Running the Simulation

```bash
python tree_reaction_simulation.py
```

Interactive Features:
- Button 1. Instant tree growth
- Button 2. Color cycling
- Button 3. Slow growth mode

- Tree Layout Algorithm

- What Makes This Algorithm Unique?

Unlike traditional tree layout algorithms that focus on compactness and tidiness, this algorithm creates natural-looking trees that mimic biological growth patterns. It's based on a tree reaction concept where each branch reacts to its parent's position and angle.

- Key Innovations:

1. Trigonometric Positioning. Uses math.cos and math.sin for natural branch angles
2. Recursive Branch Placement. Each branch calculates its position based on parent's angle
3. Dynamic Scaling. Automatically adjusts spacing based on tree size
4. Length Decay. Branches get shorter as they grow, creating natural tree shapes
5. Configurable Spread. 35-degree branch spread creates realistic tree structures

- Features

- Natural Tree Aesthetics. Creates organic, visually appealing tree layouts
- Arbitrary Tree Structures. Works with any tree structure, not just binary trees
- Dynamic Scaling. Automatically adjusts for different tree sizes, 10, 30, 60+ nodes
- Configurable Parameters. Customizable branch angles, length factors, and depth limits
- High Performance. Efficient recursive algorithm with minimal computational overhead

- Comparison with Other Algorithms

| Algorithm | Focus | Method | Result |
|-----------|-------|--------|---------|
| Reingold-Tilford | Tidiness | Horizontal alignment | Rigid, grid-like |
| Walker's Algorithm | Compactness | Width calculations | Professional but stiff |
| Tree Reaction | Natural Growth | Trigonometric positioning | Organic, tree-like |

- Usage

```python
from tree_layout_algorithm import TreeLayoutAlgorithm
import math

# Create algorithm instance
tree_layout = TreeLayoutAlgorithm(
    branch_angle=math.radians(35),  # 35 degree spread
    branch_factor=0.85,             # 85% length scaling
    min_branch_length=30.0,         # Minimum branch length
    max_depth=10000                 # No depth limit
)

# Your tree data
nodes = {
    '1': {'name': 'Root'},
    '2': {'name': 'Child 1'},
    '3': {'name': 'Child 2'},
    # ... more nodes
}

links = [
    {'from': '1', 'to': '2'},
    {'from': '1', 'to': '3'},
    # ... more links
]

# Layout the tree
positions = tree_layout.layout_tree(nodes, links)

# Get node positions
for node_id, (x, y) in positions.items():
    print(f"Node {node_id}: ({x:.1f}, {y:.1f})")
```

- Algorithm Details

- Core Concept: Tree Reaction

Each branch reacts to its parent's position and angle:

```python
# Calculate angle for this branch
if num_branches == 1:
    delta = 0  # Single child goes straight up
else:
    # Spread branches evenly
    spread = branch_angle * 2
    delta = (i / (num_branches - 1)) * spread - spread / 2

child_angle = angle + delta

# Calculate position using trigonometry
end_x = start_x + length * math.cos(child_angle)
end_y = start_y + length * math.sin(child_angle)
```

- Dynamic Scaling

The algorithm automatically adjusts parameters based on tree size:

- 10 nodes or less. Base length 100, spacing 60
- 11-30 nodes. Base length 120, spacing 80  
- 31-60 nodes. Base length 150, spacing 100
- 60+ nodes. Base length 180, spacing 120

- Length Decay

Each level gets shorter branches with random variation:

```python
new_length = length * random.uniform(0.8, branch_factor)
```

This creates natural tree shapes where branches get thinner and shorter as they grow.

- Use Cases

- Interactive Story Visualization. Perfect for PathForge's story node layouts
- Organizational Charts. Natural-looking company hierarchies
- Family Trees. Organic genealogical displays
- Decision Trees. Intuitive flow chart layouts
- Mind Maps. Creative brainstorming visualizations
- File System Trees. Natural directory structures

- Performance

- Time Complexity. O(n) where n is the number of nodes
- Space Complexity. O(n) for storing positions and tree structure
- Memory Efficient. Minimal overhead, suitable for large trees
- Real-time Capable. Fast enough for interactive applications

- Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| branch_angle | 35° | Maximum spread angle for branches |
| branch_factor | 0.85 | Length scaling factor for child branches |
| min_branch_length | 30.0 | Minimum length before stopping |
| max_depth | 10000 | Maximum recursion depth |

- License

MIT License

- Contributing

This algorithm was found in an old development file that had a nice solution. If you find improvements or have ideas for enhancements, contributions are welcome.

- Acknowledgments

Originally made as part of the PathForge interactive story creation tool. The algorithm was refined from a pygame-based fractal tree growth simulation into a practical layout algorithm for hierarchical data visualization.
