#!/usr/bin/env python3
"""
Tree Reaction Simulation - Real-time Fractal Tree Growth
A pygame-based simulation of natural tree growth using recursive branch placement

Author: PathForge Developer
License: MIT License
Description: This is the original "tree reaction" algorithm that inspired the layout algorithm.
             It simulates real-time tree growth with animated branches, creating beautiful
             fractal tree patterns that grow organically over time.

Key Features:
- Real-time animated tree growth
- Recursive branch placement with natural angles
- Dynamic branch creation and growth
- Configurable growth parameters
- Beautiful visual effects with color gradients
- Performance optimization with static rendering

This simulation demonstrates the core concepts that were later adapted into the
practical tree layout algorithm for PathForge.
"""

import pygame
import sys
import math
import random

# Initialize pygame
pygame.init()

# Configuration
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tree Reaction Simulation - Fractal Tree Growth")
clock = pygame.time.Clock()

# Growth parameters
GROWTH_SPEED = 1
BRANCH_ANGLE = math.radians(35)  # 35 degree spread for natural look
BRANCH_FACTOR = 0.85             # Length scaling factor
MIN_BRANCH_LENGTH = 18           # Minimum length for new branches
MAX_DEPTH = 14                   # Maximum tree depth
GROW_EVERY_N_FRAMES = 5          # Growth rate control
MAX_BRANCH_ENDS = 5000           # Performance limit

# UI Configuration
BUTTON_RADIUS = 15
BUTTON1_X = WIDTH // 2 - 60  # Left side of center
BUTTON2_X = WIDTH // 2       # Center
BUTTON3_X = WIDTH // 2 + 60  # Right side of center
BUTTON_Y = 30

# Color schemes for the tree (32 different colors)
COLOR_SCHEMES = [
    "green",      # Original green
    "autumn",     # Orange/red autumn colors
    "winter",     # Blue/white winter colors
    "spring",     # Pink/purple spring colors
    "summer",     # Bright yellow/green summer colors
    "fire",       # Red/orange fire colors
    "ocean",      # Blue/cyan ocean colors
    "sunset",     # Purple/pink sunset colors
    "forest",     # Dark green forest
    "desert",     # Sandy brown desert
    "arctic",     # Light blue/white arctic
    "tropical",   # Bright tropical colors
    "mountain",   # Gray/white mountain
    "sunrise",    # Yellow/orange sunrise
    "midnight",   # Dark blue/purple night
    "lavender",   # Purple/lavender
    "coral",      # Pink/coral reef
    "emerald",    # Bright emerald green
    "amber",      # Golden amber
    "crimson",    # Deep red
    "azure",      # Bright blue
    "violet",     # Deep purple
    "copper",     # Orange/brown copper
    "silver",     # Gray/silver
    "gold",       # Bright gold
    "rose",       # Pink/rose
    "teal",       # Blue-green teal
    "maroon",     # Dark red
    "navy",       # Dark blue
    "lime",       # Bright lime green
    "magenta",    # Bright magenta
    "cyan"        # Bright cyan
]

# Create static surface for performance optimization
static_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)


class Branch:
    """
    Represents a single branch in the tree.
    
    Each branch can grow over time and spawn child branches when it reaches
    its target length, creating a recursive tree structure.
    """
    
    def __init__(self, start: tuple, angle: float, length: float, depth: int):
        """
        Initialize a new branch.
        
        Args:
            start: Starting position (x, y)
            angle: Branch angle in radians
            length: Target length for this branch
            depth: Current depth in the tree (affects color and thickness)
        """
        self.start = start
        self.angle = angle
        self.length = 0                    # Current length (grows over time)
        self.target_length = length        # Final target length
        self.depth = depth
        self.finished = False              # Has this branch finished growing?
        self.children = []                 # Child branches
        self.static = False                # Is this branch fully grown and static?
    
    def grow(self) -> None:
        """
        Grow this branch and potentially create children.
        
        This is the core of the tree reaction algorithm - each branch grows
        over time and spawns new branches when it reaches its target length.
        """
        # Grow the branch length
        if self.length < self.target_length:
            self.length += GROWTH_SPEED
            if self.length > self.target_length:
                self.length = self.target_length
        else:
            # Branch has reached target length - create children
            if (not self.finished and 
                self.depth < MAX_DEPTH and 
                self.target_length > MIN_BRANCH_LENGTH):
                
                self.finished = True
                end = self.get_end()
                
                # Create 2-3 child branches (random for natural variation)
                num_branches = random.choice([2, 3])
                
                for _ in range(num_branches):
                    # Calculate branch angle
                    if self.depth == 1:
                        delta = 0  # First level branches go straight up
                    else:
                        # Random angle variation within the branch spread
                        delta = random.uniform(-BRANCH_ANGLE, BRANCH_ANGLE)
                    
                    # Calculate new branch length with random variation
                    new_length = self.target_length * random.uniform(0.8, BRANCH_FACTOR)
                    
                    # Only create branch if it's long enough
                    if new_length >= MIN_BRANCH_LENGTH:
                        child = Branch(
                            end,                           # Start from end of current branch
                            self.angle + delta,           # New angle
                            new_length,                   # New length
                            self.depth + 1                # Deeper in tree
                        )
                        self.children.append(child)
            
            # Mark as static if finished and all children are static
            if self.finished and all(child.static for child in self.children):
                self.static = True
                self.draw_static(static_surface)
    
    def get_end(self) -> tuple:
        """
        Calculate the end position of this branch using trigonometry.
        
        Returns:
            Tuple of (x, y) coordinates for the branch end
        """
        dx = self.length * math.cos(self.angle)
        dy = self.length * math.sin(self.angle)
        return (self.start[0] + dx, self.start[1] + dy)
    
    def get_color(self, color_scheme: str) -> tuple:
        """
        Get color for this branch based on depth and color scheme.
        
        Args:
            color_scheme: Current color scheme name
            
        Returns:
            RGB color tuple
        """
        depth_factor = min(self.depth * 15, 200)
        
        if color_scheme == "green":
            return (0, 255 - depth_factor, 0)
        elif color_scheme == "autumn":
            return (255 - depth_factor, 100 + depth_factor // 2, 0)
        elif color_scheme == "winter":
            return (200 - depth_factor, 200 - depth_factor, 255 - depth_factor)
        elif color_scheme == "spring":
            return (255 - depth_factor, 100 + depth_factor // 2, 200 - depth_factor)
        elif color_scheme == "summer":
            return (255 - depth_factor, 255 - depth_factor // 2, 0)
        elif color_scheme == "fire":
            return (255, 100 + depth_factor // 2, 0)
        elif color_scheme == "ocean":
            return (0, 150 + depth_factor // 2, 255 - depth_factor)
        elif color_scheme == "sunset":
            return (255 - depth_factor, 50 + depth_factor // 2, 150 + depth_factor // 2)
        elif color_scheme == "forest":
            return (0, 150 - depth_factor // 2, 0)
        elif color_scheme == "desert":
            return (200 - depth_factor // 2, 150 - depth_factor // 3, 50)
        elif color_scheme == "arctic":
            return (180 - depth_factor, 200 - depth_factor, 255 - depth_factor // 2)
        elif color_scheme == "tropical":
            return (255 - depth_factor, 100 + depth_factor, 0)
        elif color_scheme == "mountain":
            return (150 - depth_factor, 150 - depth_factor, 160 - depth_factor)
        elif color_scheme == "sunrise":
            return (255 - depth_factor // 2, 200 - depth_factor // 2, 0)
        elif color_scheme == "midnight":
            return (50 + depth_factor // 2, 0, 100 + depth_factor // 2)
        elif color_scheme == "lavender":
            return (200 - depth_factor, 150 - depth_factor // 2, 255 - depth_factor)
        elif color_scheme == "coral":
            return (255 - depth_factor, 100 - depth_factor // 2, 100 - depth_factor // 2)
        elif color_scheme == "emerald":
            return (0, 200 - depth_factor // 2, 100 - depth_factor // 3)
        elif color_scheme == "amber":
            return (255 - depth_factor // 2, 200 - depth_factor // 2, 0)
        elif color_scheme == "crimson":
            return (200 - depth_factor // 2, 0, 0)
        elif color_scheme == "azure":
            return (0, 150 - depth_factor // 2, 255 - depth_factor)
        elif color_scheme == "violet":
            return (150 - depth_factor // 2, 0, 200 - depth_factor // 2)
        elif color_scheme == "copper":
            return (200 - depth_factor // 2, 100 - depth_factor // 3, 50)
        elif color_scheme == "silver":
            return (180 - depth_factor, 180 - depth_factor, 180 - depth_factor)
        elif color_scheme == "gold":
            return (255 - depth_factor // 2, 215 - depth_factor // 2, 0)
        elif color_scheme == "rose":
            return (255 - depth_factor, 100 - depth_factor // 2, 150 - depth_factor // 2)
        elif color_scheme == "teal":
            return (0, 150 - depth_factor // 2, 150 - depth_factor // 2)
        elif color_scheme == "maroon":
            return (150 - depth_factor // 2, 0, 0)
        elif color_scheme == "navy":
            return (0, 0, 150 - depth_factor // 2)
        elif color_scheme == "lime":
            return (150 - depth_factor // 2, 255 - depth_factor, 0)
        elif color_scheme == "magenta":
            return (255 - depth_factor, 0, 255 - depth_factor)
        elif color_scheme == "cyan":
            return (0, 255 - depth_factor, 255 - depth_factor)
        else:
            return (0, 255 - depth_factor, 0)  # Default green
    
    def draw(self, surface: pygame.Surface, color_scheme: str = "green") -> None:
        """
        Draw this branch and all its children.
        
        Args:
            surface: Pygame surface to draw on
            color_scheme: Current color scheme
        """
        if self.static:
            return  # Skip drawing if already drawn to static surface
        
        end = self.get_end()
        color = self.get_color(color_scheme)
        thickness = max(1, 8 - self.depth)
        
        pygame.draw.line(surface, color, self.start, end, thickness)
        
        # Draw all children
        for child in self.children:
            child.draw(surface, color_scheme)
    
    def draw_static(self, surface: pygame.Surface, color_scheme: str = "green") -> None:
        """
        Draw this branch to the static surface for performance.
        
        Args:
            surface: Static surface for performance optimization
            color_scheme: Current color scheme
        """
        end = self.get_end()
        color = self.get_color(color_scheme)
        thickness = max(1, 8 - self.depth)
        
        pygame.draw.line(surface, color, self.start, end, thickness)
        
        # Draw all children
        for child in self.children:
            child.draw_static(surface, color_scheme)
    
    def update(self, grow_this_frame: bool) -> None:
        """
        Update this branch and all its children.
        
        Args:
            grow_this_frame: Whether to grow this frame
        """
        if not self.static:
            if grow_this_frame:
                self.grow()
            
            # Update all children
            for child in self.children:
                child.update(grow_this_frame)
    
    def count_branch_ends(self) -> int:
        """
        Count the total number of branch ends (leaf nodes) in this subtree.
        
        Returns:
            Number of branch ends
        """
        if not self.children:
            return 1  # This is a leaf
        
        return sum(child.count_branch_ends() for child in self.children)


def draw_button(surface: pygame.Surface, x: int, y: int, radius: int, color: tuple, text: str = "") -> None:
    """
    Draw a circular button with optional text.
    
    Args:
        surface: Pygame surface to draw on
        x, y: Button center coordinates
        radius: Button radius
        color: Button color
        text: Optional text to display
    """
    pygame.draw.circle(surface, color, (x, y), radius)
    
    if text:
        font = pygame.font.Font(None, 16)
        font.set_bold(True)
        text_surface = font.render(text, True, (0, 0, 0))  # Black text
        text_rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, text_rect)


def is_button_clicked(mouse_pos: tuple, button_x: int, button_y: int, radius: int) -> bool:
    """
    Check if mouse click is within button bounds.
    
    Args:
        mouse_pos: Mouse position (x, y)
        button_x, button_y: Button center coordinates
        radius: Button radius
        
    Returns:
        True if clicked within button
    """
    distance = math.sqrt((mouse_pos[0] - button_x)**2 + (mouse_pos[1] - button_y)**2)
    return distance <= radius


def instant_grow_all_branches(branches: list) -> None:
    """
    Instantly grow all branches to their full length.
    
    Args:
        branches: List of branch objects
    """
    for branch in branches:
        grow_branch_instantly(branch)


def grow_branch_instantly(branch) -> None:
    """
    Recursively grow a branch and all its children instantly.
    
    Args:
        branch: Branch object to grow
    """
    # Grow this branch to full length
    branch.length = branch.target_length
    
    # Create children if conditions are met
    if (not branch.finished and 
        branch.depth < MAX_DEPTH and 
        branch.target_length > MIN_BRANCH_LENGTH):
        
        branch.finished = True
        end = branch.get_end()
        num_branches = random.choice([2, 3])
        
        for _ in range(num_branches):
            if branch.depth == 1:
                delta = 0
            else:
                delta = random.uniform(-BRANCH_ANGLE, BRANCH_ANGLE)
            
            new_length = branch.target_length * random.uniform(0.8, BRANCH_FACTOR)
            
            if new_length >= MIN_BRANCH_LENGTH:
                child = Branch(end, branch.angle + delta, new_length, branch.depth + 1)
                branch.children.append(child)
                grow_branch_instantly(child)  # Recursively grow children


def main():
    """
    Main simulation loop.
    
    Handles user input, updates the tree growth, and renders the display.
    """
    global static_surface
    
    running = True
    growing = False
    paused = False
    branches = []
    frame_count = 0
    current_color_scheme = 0  # Index into COLOR_SCHEMES
    instant_grow_mode = False
    fast_grow_mode = False  # For button 3 (2x faster growth)
    
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Spacebar updates color for button 3 trees
                if fast_grow_mode and branches:
                    current_color_scheme = (current_color_scheme + 1) % len(COLOR_SCHEMES)
                    # Redraw static surface with new color
                    static_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    for branch in branches:
                        branch.draw_static(static_surface, COLOR_SCHEMES[current_color_scheme])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check button 1 (Instant Grow)
                if is_button_clicked(mouse_pos, BUTTON1_X, BUTTON_Y, BUTTON_RADIUS):
                    # Always create a new tree and grow it instantly
                    static_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    branches = [Branch((WIDTH // 2, HEIGHT - 50), -math.pi / 2, 100, 1)]
                    growing = True
                    paused = False
                    instant_grow_mode = False
                    fast_grow_mode = False
                    frame_count = 0
                    # Grow instantly
                    instant_grow_all_branches(branches)
                    instant_grow_mode = True
                    paused = True
                
                # Check button 2 (Color Change)
                elif is_button_clicked(mouse_pos, BUTTON2_X, BUTTON_Y, BUTTON_RADIUS):
                    current_color_scheme = (current_color_scheme + 1) % len(COLOR_SCHEMES)
                    # Don't clear static surface - just change colors for live trees
                
                # Check button 3 (Fast Grow)
                elif is_button_clicked(mouse_pos, BUTTON3_X, BUTTON_Y, BUTTON_RADIUS):
                    # Create a new tree and grow it 2x faster
                    static_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    branches = [Branch((WIDTH // 2, HEIGHT - 50), -math.pi / 2, 100, 1)]
                    growing = True
                    paused = False
                    instant_grow_mode = False
                    fast_grow_mode = True
                    frame_count = 0
        
        # Clear screen with dark background
        screen.fill((10, 10, 30))
        
        # Blit static surface (fully grown branches for performance)
        screen.blit(static_surface, (0, 0))
        
        # Determine if we should grow this frame
        if fast_grow_mode:
            # Button 3: 2x faster growth (every 2-3 frames instead of 5)
            grow_this_frame = (frame_count % 2 == 0)
        else:
            # Normal growth rate
            grow_this_frame = (frame_count % GROW_EVERY_N_FRAMES == 0)
        current_scheme = COLOR_SCHEMES[current_color_scheme]
        
        if growing and not paused and branches:
            # Update and draw growing branches
            for branch in branches:
                branch.update(grow_this_frame)
                branch.draw(screen, current_scheme)
            
            # Count total branch ends for performance monitoring
            total_ends = sum(branch.count_branch_ends() for branch in branches)
            
            # Pause if we've reached the performance limit
            if total_ends >= MAX_BRANCH_ENDS:
                paused = True
            
            # Check if tree is finished growing (all branches are static)
            if branches and all(branch.static for branch in branches):
                growing = False
        
        elif paused or instant_grow_mode:
            # Draw the finished tree
            for branch in branches:
                branch.draw(screen, current_scheme)
        
        # Draw UI elements
        # Button 1 (Instant Grow) - Bright green
        button1_color = (0, 255, 0)  # Bright green
        draw_button(screen, BUTTON1_X, BUTTON_Y, BUTTON_RADIUS, button1_color, "1")
        
        # Button 2 (Color Change) - Bright red
        button2_color = (255, 0, 0)  # Bright red
        draw_button(screen, BUTTON2_X, BUTTON_Y, BUTTON_RADIUS, button2_color, "2")
        
        # Button 3 (Fast Grow) - Bright blue
        button3_color = (0, 0, 255)  # Bright blue
        draw_button(screen, BUTTON3_X, BUTTON_Y, BUTTON_RADIUS, button3_color, "3")
        
        # Show button instructions in top left
        font = pygame.font.Font(None, 20)
        instructions = [
            "1 = Instant growth",
            "2 = Tree Color", 
            "3 = Slow Growth"
        ]
        for i, instruction in enumerate(instructions):
            text_surface = font.render(instruction, True, (255, 255, 255))
            screen.blit(text_surface, (10, 10 + i * 25))
        
        # Show spacebar instruction when button 3 tree is grown
        if fast_grow_mode and branches and not growing:
            space_font = pygame.font.Font(None, 18)
            space_text = space_font.render("SPACEBAR = Update Color", True, (255, 255, 255))
            screen.blit(space_text, (BUTTON3_X - 40, BUTTON_Y + 25))
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
        frame_count += 1
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
