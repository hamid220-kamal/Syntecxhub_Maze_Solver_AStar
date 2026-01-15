"""
A* Maze Solver - Interactive Demo
=================================
Main entry point with interactive menu and demo capabilities.

Author: Hamid Kamal
Project: Syntecxhub AI Internship - Project 1

Usage:
    python main.py              # Run interactive menu
    python main.py --demo       # Run automatic demo
    python main.py --animate    # Run with animation
"""

import sys
import random
from typing import List

from maze_solver import MazeSolver, CellType, HeuristicType, create_sample_maze
from visualizer import ConsoleVisualizer, GraphicalVisualizer, MATPLOTLIB_AVAILABLE


def generate_random_maze(rows: int, cols: int, wall_density: float = 0.3) -> List[List[int]]:
    """
    Generate a random maze with specified dimensions.
    
    Args:
        rows: Number of rows
        cols: Number of columns
        wall_density: Probability of a cell being a wall (0.0 to 1.0)
    
    Returns:
        2D maze grid with random walls, start, and goal
    """
    maze = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if random.random() < wall_density:
                row.append(CellType.WALL.value)
            else:
                row.append(CellType.EMPTY.value)
        maze.append(row)
    
    # Set start (top-left area)
    start_row, start_col = 0, 0
    maze[start_row][start_col] = CellType.START.value
    
    # Set goal (bottom-right area)
    goal_row, goal_col = rows - 1, cols - 1
    maze[goal_row][goal_col] = CellType.GOAL.value
    
    # Ensure start and goal neighbors are clear
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = start_row + dr, start_col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if maze[nr][nc] == CellType.WALL.value:
                maze[nr][nc] = CellType.EMPTY.value
        nr, nc = goal_row + dr, goal_col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if maze[nr][nc] == CellType.WALL.value:
                maze[nr][nc] = CellType.EMPTY.value
    
    return maze


def get_predefined_mazes() -> dict:
    """Return a collection of predefined test mazes."""
    return {
        "Simple Path": [
            [2, 0, 0, 0, 3],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        "With Obstacles": [
            [2, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0],
            [0, 0, 0, 0, 3],
        ],
        "Complex Maze": create_sample_maze(),
        "Unreachable Goal": [
            [2, 0, 0, 1, 3],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
        ],
        "Large Maze": generate_random_maze(15, 20, 0.25),
    }


def print_header():
    """Print application header."""
    print("\n" + "=" * 60)
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║          🧩 A* MAZE SOLVER 🧩                         ║
    ║          Syntecxhub AI Internship                     ║
    ║          Project 1: Pathfinding Algorithm             ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    print("=" * 60)


def select_heuristic() -> HeuristicType:
    """Interactive heuristic selection."""
    print("\n  Select Heuristic Function:")
    print("    1. Manhattan Distance (recommended for 4-way movement)")
    print("    2. Euclidean Distance (straight-line distance)")
    print("    3. Chebyshev Distance (allows diagonal consideration)")
    
    while True:
        choice = input("\n  Enter choice (1-3) [default: 1]: ").strip()
        if choice == "" or choice == "1":
            return HeuristicType.MANHATTAN
        elif choice == "2":
            return HeuristicType.EUCLIDEAN
        elif choice == "3":
            return HeuristicType.CHEBYSHEV
        else:
            print("    Invalid choice. Please enter 1, 2, or 3.")


def demo_mode():
    """Run automatic demonstration of all features."""
    print_header()
    print("\n  [DEMO MODE - Automatic Demonstration]")
    
    mazes = get_predefined_mazes()
    
    for name, maze in mazes.items():
        print(f"\n{'='*60}")
        print(f"  Testing: {name}")
        print("="*60)
        
        # Show original maze
        ConsoleVisualizer.print_maze(maze, f"Original: {name}")
        
        # Solve with all heuristics
        for heuristic in [HeuristicType.MANHATTAN, HeuristicType.EUCLIDEAN]:
            solver = MazeSolver(maze, heuristic)
            path, stats = solver.solve()
            
            print(f"\n  Heuristic: {heuristic.value.upper()}")
            if path:
                print(f"    ✓ Path found!")
                print(f"      Length: {stats['path_length']} steps")
                print(f"      Cost: {stats['path_cost']:.2f}")
                print(f"      Nodes explored: {stats['nodes_explored']}")
            else:
                print(f"    ✗ {stats.get('error', 'No path found')}")
        
        # Show solution for last solver
        if path:
            solution_maze = solver.get_solution_maze(path)
            ConsoleVisualizer.print_maze(solution_maze, f"Solution: {name}")
        
        input("\n  Press Enter to continue...")


def interactive_mode():
    """Run interactive menu."""
    print_header()
    
    while True:
        print("\n  MAIN MENU")
        print("  " + "-" * 30)
        print("    1. Solve predefined maze")
        print("    2. Generate random maze")
        print("    3. Create custom maze")
        print("    4. Compare heuristics")
        print("    5. Graphical visualization")
        print("    6. Run full demo")
        print("    0. Exit")
        
        choice = input("\n  Enter choice: ").strip()
        
        if choice == "0":
            print("\n  Thank you for using A* Maze Solver!")
            print("  Project by: Hamid Kamal | Syntecxhub Internship")
            break
        
        elif choice == "1":
            # Predefined mazes
            mazes = get_predefined_mazes()
            print("\n  Available Mazes:")
            for i, name in enumerate(mazes.keys(), 1):
                print(f"    {i}. {name}")
            
            try:
                idx = int(input("\n  Select maze (1-5): ").strip()) - 1
                name = list(mazes.keys())[idx]
                maze = mazes[name]
            except (ValueError, IndexError):
                print("    Invalid selection.")
                continue
            
            heuristic = select_heuristic()
            diagonal = input("\n  Allow diagonal movement? (y/n) [n]: ").strip().lower() == 'y'
            
            ConsoleVisualizer.print_maze(maze, f"Original: {name}")
            
            solver = MazeSolver(maze, heuristic, diagonal)
            path, stats = solver.solve()
            
            if path:
                solution_maze = solver.get_solution_maze(path)
                ConsoleVisualizer.print_maze(solution_maze, f"Solution: {name}")
                print(f"\n  ✓ Path found!")
                print(f"    Path: {path}")
                print(f"    Length: {stats['path_length']} steps")
                print(f"    Cost: {stats['path_cost']:.2f}")
                print(f"    Nodes explored: {stats['nodes_explored']}")
            else:
                print(f"\n  ✗ {stats.get('error', 'No path found')}")
        
        elif choice == "2":
            # Random maze
            try:
                rows = int(input("\n  Enter rows (5-30) [10]: ").strip() or "10")
                cols = int(input("  Enter cols (5-40) [15]: ").strip() or "15")
                density = float(input("  Wall density (0.1-0.5) [0.25]: ").strip() or "0.25")
            except ValueError:
                print("    Invalid input. Using defaults.")
                rows, cols, density = 10, 15, 0.25
            
            rows = max(5, min(30, rows))
            cols = max(5, min(40, cols))
            density = max(0.1, min(0.5, density))
            
            maze = generate_random_maze(rows, cols, density)
            heuristic = select_heuristic()
            
            ConsoleVisualizer.print_maze(maze, "Random Maze")
            
            solver = MazeSolver(maze, heuristic)
            path, stats = solver.solve()
            
            if path:
                solution_maze = solver.get_solution_maze(path)
                ConsoleVisualizer.print_maze(solution_maze, "Solution")
                print(f"\n  ✓ Path found! Length: {stats['path_length']}, Cost: {stats['path_cost']:.2f}")
            else:
                print(f"\n  ✗ {stats.get('error')}")
        
        elif choice == "3":
            # Custom maze input
            print("\n  Enter maze (0=empty, 1=wall, 2=start, 3=goal)")
            print("  Enter rows one at a time, empty line to finish:")
            print("  Example row: 2 0 0 1 0 3")
            
            maze = []
            while True:
                row_input = input("    Row: ").strip()
                if not row_input:
                    break
                try:
                    row = [int(x) for x in row_input.split()]
                    maze.append(row)
                except ValueError:
                    print("    Invalid input. Use space-separated numbers.")
            
            if maze:
                heuristic = select_heuristic()
                ConsoleVisualizer.print_maze(maze, "Custom Maze")
                
                solver = MazeSolver(maze, heuristic)
                path, stats = solver.solve()
                
                if path:
                    solution_maze = solver.get_solution_maze(path)
                    ConsoleVisualizer.print_maze(solution_maze, "Solution")
                    print(f"\n  ✓ Path: {path}")
                else:
                    print(f"\n  ✗ {stats.get('error')}")
        
        elif choice == "4":
            # Compare heuristics
            print("\n  [Heuristic Comparison Test]")
            maze = create_sample_maze()
            ConsoleVisualizer.print_maze(maze, "Test Maze")
            
            print("\n  Results:")
            print("  " + "-" * 50)
            print(f"  {'Heuristic':<15} {'Path Length':<12} {'Cost':<10} {'Explored':<10}")
            print("  " + "-" * 50)
            
            for h in HeuristicType:
                solver = MazeSolver(maze, h)
                path, stats = solver.solve()
                if path:
                    print(f"  {h.value:<15} {stats['path_length']:<12} {stats['path_cost']:<10.2f} {stats['nodes_explored']:<10}")
                else:
                    print(f"  {h.value:<15} {'N/A':<12} {'N/A':<10} {stats['nodes_explored']:<10}")
            
            print("  " + "-" * 50)
        
        elif choice == "5":
            # Graphical visualization
            if not MATPLOTLIB_AVAILABLE:
                print("\n  ✗ Matplotlib not installed!")
                print("    Install with: pip install matplotlib numpy")
                continue
            
            print("\n  [Graphical Visualization]")
            maze = create_sample_maze()
            heuristic = select_heuristic()
            
            solver = MazeSolver(maze, heuristic)
            path, stats = solver.solve()
            
            if path:
                solution_maze = solver.get_solution_maze(path)
                print("  Opening graphical window...")
                
                animate = input("  Show animated search? (y/n) [n]: ").strip().lower() == 'y'
                if animate:
                    GraphicalVisualizer.animate_search(solver, path, interval=150)
                else:
                    GraphicalVisualizer.plot_maze(
                        solution_maze,
                        title=f"A* Solution ({heuristic.value} heuristic)",
                        path=path
                    )
            else:
                print(f"\n  ✗ {stats.get('error')}")
        
        elif choice == "6":
            demo_mode()
        
        else:
            print("\n  Invalid choice. Please try again.")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['--demo', '-d']:
            demo_mode()
        elif arg in ['--animate', '-a']:
            maze = create_sample_maze()
            solver = MazeSolver(maze, HeuristicType.MANHATTAN)
            path, stats = solver.solve()
            if MATPLOTLIB_AVAILABLE and path:
                GraphicalVisualizer.animate_search(solver, path)
            else:
                ConsoleVisualizer.animate_search(solver, delay=0.2)
        elif arg in ['--help', '-h']:
            print(__doc__)
        else:
            print(f"Unknown argument: {arg}")
            print("Use --help for usage information.")
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
