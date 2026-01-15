"""
Maze Visualizer - Console & Graphical Display
==============================================
Provides both console-based ASCII visualization and matplotlib animated plots.

Author: Hamid Kamal
Project: Syntecxhub AI Internship - Project 1
"""

import time
import os
from typing import List, Tuple, Optional

try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from matplotlib.colors import ListedColormap
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from maze_solver import MazeSolver, CellType, HeuristicType


class ConsoleVisualizer:
    """
    ASCII-based console visualization for the maze solver.
    Works in any terminal without additional dependencies.
    """
    
    # Unicode characters for prettier display
    SYMBOLS = {
        CellType.EMPTY.value: '·',      # Empty cell
        CellType.WALL.value: '█',       # Wall
        CellType.START.value: 'S',      # Start
        CellType.GOAL.value: 'G',       # Goal
        CellType.PATH.value: '★',       # Solution path
        CellType.VISITED.value: '○',    # Visited during search
    }
    
    # ANSI color codes
    COLORS = {
        CellType.EMPTY.value: '\033[90m',     # Gray
        CellType.WALL.value: '\033[97m',      # White
        CellType.START.value: '\033[92m',     # Green
        CellType.GOAL.value: '\033[91m',      # Red
        CellType.PATH.value: '\033[93m',      # Yellow
        CellType.VISITED.value: '\033[94m',   # Blue
    }
    RESET = '\033[0m'
    
    @classmethod
    def clear_screen(cls):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @classmethod
    def print_maze(
        cls,
        maze: List[List[int]],
        title: str = "",
        use_colors: bool = True
    ) -> None:
        """
        Print the maze to console with optional colors.
        
        Args:
            maze: 2D grid to display
            title: Optional title above the maze
            use_colors: Whether to use ANSI colors
        """
        if title:
            print(f"\n{'='*50}")
            print(f"  {title}")
            print(f"{'='*50}\n")
        
        # Print column numbers
        print("    ", end="")
        for j in range(len(maze[0])):
            print(f"{j%10}", end=" ")
        print("\n   +" + "-" * (len(maze[0]) * 2 + 1) + "+")
        
        # Print maze with row numbers
        for i, row in enumerate(maze):
            print(f"{i:2} |", end=" ")
            for cell in row:
                symbol = cls.SYMBOLS.get(cell, '?')
                if use_colors:
                    color = cls.COLORS.get(cell, '')
                    print(f"{color}{symbol}{cls.RESET}", end=" ")
                else:
                    print(symbol, end=" ")
            print("|")
        
        print("   +" + "-" * (len(maze[0]) * 2 + 1) + "+")
        
        # Legend
        print("\n  Legend:")
        print(f"    {cls.COLORS[2]}S{cls.RESET} = Start  ", end="")
        print(f"    {cls.COLORS[3]}G{cls.RESET} = Goal  ", end="")
        print(f"    {cls.COLORS[1]}█{cls.RESET} = Wall")
        print(f"    {cls.COLORS[4]}★{cls.RESET} = Path   ", end="")
        print(f"    {cls.COLORS[5]}○{cls.RESET} = Visited", end="")
        print(f"    {cls.COLORS[0]}·{cls.RESET} = Empty")
    
    @classmethod
    def animate_search(
        cls,
        solver: MazeSolver,
        delay: float = 0.1
    ) -> None:
        """
        Animate the A* search step by step in console.
        
        Args:
            solver: MazeSolver instance (must have already solved)
            delay: Seconds between frames
        """
        if not solver.search_steps:
            print("No search steps recorded. Run solve() first.")
            return
        
        maze_copy = [row[:] for row in solver.maze]
        
        for step in solver.search_steps:
            cls.clear_screen()
            pos = step["position"]
            
            # Mark current position
            if maze_copy[pos[0]][pos[1]] == CellType.EMPTY.value:
                maze_copy[pos[0]][pos[1]] = CellType.VISITED.value
            
            cls.print_maze(maze_copy, f"A* Search - Exploring ({pos[0]}, {pos[1]})")
            print(f"\n  f={step['f_score']:.2f}  g={step['g_score']:.2f}  h={step['h_score']:.2f}")
            print(f"  Open: {step['open_count']}  Closed: {step['closed_count']}")
            
            time.sleep(delay)


class GraphicalVisualizer:
    """
    Matplotlib-based graphical visualization with animation support.
    Requires matplotlib and numpy.
    """
    
    # Color map for cell types
    COLORMAP = ListedColormap([
        '#2d2d2d',  # 0: Empty - dark gray
        '#1a1a2e',  # 1: Wall - dark blue
        '#00ff88',  # 2: Start - green
        '#ff4757',  # 3: Goal - red
        '#ffd700',  # 4: Path - gold
        '#5f9ea0',  # 5: Visited - cadet blue
    ]) if MATPLOTLIB_AVAILABLE else None
    
    @classmethod
    def plot_maze(
        cls,
        maze: List[List[int]],
        title: str = "Maze",
        path: Optional[List[Tuple[int, int]]] = None,
        save_path: Optional[str] = None
    ) -> None:
        """
        Create a static plot of the maze.
        
        Args:
            maze: 2D grid to display
            title: Plot title
            path: Optional path to highlight with arrows
            save_path: If provided, save figure to this path
        """
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib not available. Install with: pip install matplotlib")
            return
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Convert to numpy array
        maze_array = np.array(maze)
        
        # Plot maze
        im = ax.imshow(maze_array, cmap=cls.COLORMAP, vmin=0, vmax=5)
        
        # Add grid
        ax.set_xticks(np.arange(-0.5, len(maze[0]), 1), minor=True)
        ax.set_yticks(np.arange(-0.5, len(maze), 1), minor=True)
        ax.grid(which='minor', color='#404040', linestyle='-', linewidth=0.5)
        
        # Add path arrows if provided
        if path and len(path) > 1:
            for i in range(len(path) - 1):
                y1, x1 = path[i]
                y2, x2 = path[i + 1]
                dx, dy = x2 - x1, y2 - y1
                ax.annotate(
                    '', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(
                        arrowstyle='->',
                        color='#ffffff',
                        lw=2
                    )
                )
        
        # Labels and title
        ax.set_title(title, fontsize=16, fontweight='bold', color='#ffffff', pad=20)
        ax.set_xlabel('Column', fontsize=12, color='#ffffff')
        ax.set_ylabel('Row', fontsize=12, color='#ffffff')
        
        # Style
        fig.patch.set_facecolor('#1a1a2e')
        ax.set_facecolor('#1a1a2e')
        ax.tick_params(colors='#ffffff')
        
        # Legend
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, facecolor='#00ff88', label='Start'),
            plt.Rectangle((0, 0), 1, 1, facecolor='#ff4757', label='Goal'),
            plt.Rectangle((0, 0), 1, 1, facecolor='#1a1a2e', label='Wall'),
            plt.Rectangle((0, 0), 1, 1, facecolor='#ffd700', label='Path'),
            plt.Rectangle((0, 0), 1, 1, facecolor='#5f9ea0', label='Visited'),
        ]
        ax.legend(
            handles=legend_elements,
            loc='upper left',
            bbox_to_anchor=(1, 1),
            facecolor='#2d2d2d',
            edgecolor='#ffffff',
            labelcolor='#ffffff'
        )
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, facecolor='#1a1a2e', bbox_inches='tight')
            print(f"Saved figure to: {save_path}")
        
        plt.show()
    
    @classmethod
    def animate_search(
        cls,
        solver: MazeSolver,
        path: Optional[List[Tuple[int, int]]] = None,
        interval: int = 100,
        save_path: Optional[str] = None
    ) -> None:
        """
        Create an animated visualization of the A* search.
        
        Args:
            solver: MazeSolver instance with search_steps populated
            path: Final solution path
            interval: Milliseconds between frames
            save_path: If provided, save animation as GIF
        """
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib not available. Install with: pip install matplotlib")
            return
        
        if not solver.search_steps:
            print("No search steps. Run solve() first.")
            return
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Initialize with original maze
        maze_array = np.array(solver.maze, dtype=float)
        im = ax.imshow(maze_array, cmap=cls.COLORMAP, vmin=0, vmax=5)
        
        # Add grid
        ax.set_xticks(np.arange(-0.5, solver.cols, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, solver.rows, 1), minor=True)
        ax.grid(which='minor', color='#404040', linestyle='-', linewidth=0.5)
        
        # Title (will be updated)
        title = ax.set_title('A* Search Animation', fontsize=14, fontweight='bold', color='#ffffff')
        
        # Stats text
        stats_text = ax.text(
            0.02, 0.98, '', transform=ax.transAxes,
            fontsize=10, color='#ffffff', verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#2d2d2d', alpha=0.8)
        )
        
        fig.patch.set_facecolor('#1a1a2e')
        ax.set_facecolor('#1a1a2e')
        ax.tick_params(colors='#ffffff')
        
        # Animation frames
        frames = []
        current_maze = solver.maze.copy()
        current_maze = [row[:] for row in solver.maze]
        
        for i, step in enumerate(solver.search_steps):
            pos = step['position']
            if current_maze[pos[0]][pos[1]] == CellType.EMPTY.value:
                current_maze[pos[0]][pos[1]] = CellType.VISITED.value
            frames.append({
                'maze': [row[:] for row in current_maze],
                'step': step,
                'index': i + 1
            })
        
        # Add final path frames
        if path:
            for pos in path:
                if current_maze[pos[0]][pos[1]] not in [CellType.START.value, CellType.GOAL.value]:
                    current_maze[pos[0]][pos[1]] = CellType.PATH.value
                frames.append({
                    'maze': [row[:] for row in current_maze],
                    'step': solver.search_steps[-1],
                    'index': len(solver.search_steps),
                    'path_found': True
                })
        
        def update(frame_data):
            maze_array = np.array(frame_data['maze'])
            im.set_array(maze_array)
            
            step = frame_data['step']
            title.set_text(f"A* Search - Step {frame_data['index']}/{len(solver.search_steps)}")
            
            if frame_data.get('path_found'):
                stats_text.set_text("✓ PATH FOUND!")
            else:
                stats_text.set_text(
                    f"Position: ({step['position'][0]}, {step['position'][1]})\n"
                    f"f = {step['f_score']:.2f}\n"
                    f"g = {step['g_score']:.2f}\n"
                    f"h = {step['h_score']:.2f}\n"
                    f"Open: {step['open_count']}\n"
                    f"Closed: {step['closed_count']}"
                )
            
            return [im, title, stats_text]
        
        anim = animation.FuncAnimation(
            fig, update, frames=frames,
            interval=interval, blit=True, repeat=False
        )
        
        if save_path:
            anim.save(save_path, writer='pillow', fps=1000//interval)
            print(f"Saved animation to: {save_path}")
        
        plt.tight_layout()
        plt.show()


def demo_visualizers():
    """Demonstrate both console and graphical visualizers."""
    from maze_solver import create_sample_maze
    
    print("\n" + "=" * 60)
    print("   A* MAZE SOLVER - VISUALIZATION DEMO")
    print("=" * 60)
    
    # Create and solve maze
    maze = create_sample_maze()
    solver = MazeSolver(maze, HeuristicType.MANHATTAN)
    path, stats = solver.solve()
    
    # Console visualization
    print("\n[Console Visualization]")
    ConsoleVisualizer.print_maze(maze, "Original Maze")
    
    if path:
        solution_maze = solver.get_solution_maze(path)
        ConsoleVisualizer.print_maze(solution_maze, "Solved Maze with Path")
        
        print(f"\n  ✓ Path found!")
        print(f"    Length: {stats['path_length']} steps")
        print(f"    Cost: {stats['path_cost']:.2f}")
        print(f"    Nodes explored: {stats['nodes_explored']}")
    else:
        print(f"\n  ✗ No path found: {stats.get('error', 'Unknown error')}")
    
    # Graphical visualization
    if MATPLOTLIB_AVAILABLE:
        print("\n[Graphical Visualization]")
        print("Opening matplotlib window...")
        
        if path:
            solution_maze = solver.get_solution_maze(path)
            GraphicalVisualizer.plot_maze(
                solution_maze,
                title=f"A* Solution (Path Length: {len(path)})",
                path=path
            )
        else:
            GraphicalVisualizer.plot_maze(maze, title="Maze (No Solution)")
    else:
        print("\n[!] Matplotlib not installed. Run: pip install matplotlib")


if __name__ == "__main__":
    demo_visualizers()
