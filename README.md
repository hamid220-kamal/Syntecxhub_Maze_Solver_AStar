# 🧩 A* Maze Solver

> **Syntecxhub AI Internship - Project 1**  
> Implementation of the A* pathfinding algorithm with visualization

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![AI](https://img.shields.io/badge/AI-Pathfinding-orange.svg)

## 📖 Overview

This project implements the **A* (A-Star) Search Algorithm** to find the shortest path through a maze. A* is an informed search algorithm that combines:

- **g(n)**: Actual cost from start to current node
- **h(n)**: Heuristic estimate from current node to goal
- **f(n) = g(n) + h(n)**: Total estimated cost

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Multiple Heuristics** | Manhattan, Euclidean, and Chebyshev distance |
| 🔄 **Diagonal Movement** | Optional 8-directional movement support |
| 📊 **Console Visualization** | Colorful ASCII art display in terminal |
| 📈 **Graphical Visualization** | Matplotlib plots with animated search |
| 🎲 **Random Maze Generator** | Create mazes with adjustable wall density |
| 📝 **Custom Maze Input** | Enter your own mazes interactively |
| ❌ **Unreachable Detection** | Gracefully handles unsolvable mazes |

## 🚀 Quick Start

### 🌐 Web Version (Recommended!)

Simply open `index.html` in your browser for an interactive experience:
- Draw walls, set start/goal positions
- Watch A* algorithm animate in real-time
- Compare different heuristics

```bash
start index.html
```

### Run Interactive Demo (Console)

```bash
cd "D:\SYNTEXHUB PROJECTS\Syntecxhub_Maze_Solver_AStar"
python main.py
```

### Run Automatic Demo

```bash
python main.py --demo
```

### Run with Animation

```bash
python main.py --animate
```

## 📁 Project Structure

```
Syntecxhub_Maze_Solver_AStar/
├── maze_solver.py      # Core A* algorithm implementation
├── visualizer.py       # Console & graphical visualization
├── main.py             # Interactive demo & CLI
├── requirements.txt    # Optional dependencies
└── README.md           # This file
```

## 🔧 Installation

### Basic (No Dependencies)
```bash
# Just run it - core functionality needs no external packages!
python main.py
```

### With Graphical Visualization
```bash
pip install -r requirements.txt
python main.py
```

## 🎮 Usage Examples

### 1. Using as a Library

```python
from maze_solver import MazeSolver, HeuristicType

# Define maze (0=empty, 1=wall, 2=start, 3=goal)
maze = [
    [2, 0, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 3],
]

# Create solver
solver = MazeSolver(maze, HeuristicType.MANHATTAN)

# Find path
path, stats = solver.solve()

if path:
    print(f"Path found: {path}")
    print(f"Length: {stats['path_length']}")
    print(f"Nodes explored: {stats['nodes_explored']}")
else:
    print(f"No path: {stats['error']}")
```

### 2. Console Visualization

```python
from visualizer import ConsoleVisualizer

# Display maze with colors
ConsoleVisualizer.print_maze(maze, "My Maze")

# Show solution
solution_maze = solver.get_solution_maze(path)
ConsoleVisualizer.print_maze(solution_maze, "Solution")
```

### 3. Graphical Visualization

```python
from visualizer import GraphicalVisualizer

# Static plot with path arrows
GraphicalVisualizer.plot_maze(solution_maze, path=path)

# Animated search visualization
GraphicalVisualizer.animate_search(solver, path)
```

## 📊 Algorithm Explanation

### A* Search Steps:

1. **Initialize** open set with start node
2. **Loop** while open set is not empty:
   - Select node with lowest f-score
   - If goal reached, reconstruct path
   - Expand neighbors, calculate g, h, f scores
   - Add unvisited neighbors to open set
3. **Return** path or indicate unreachable

### Heuristics:

| Heuristic | Formula | Best For |
|-----------|---------|----------|
| Manhattan | `|x₁-x₂| + |y₁-y₂|` | 4-directional movement |
| Euclidean | `√[(x₁-x₂)² + (y₁-y₂)²]` | Any-angle movement |
| Chebyshev | `max(|x₁-x₂|, |y₁-y₂|)` | 8-directional movement |

## 📸 Screenshots

### Console Output
```
   +---------------------+
 0 | S · · · █ · · · · · |
 1 | · █ █ · █ · █ █ █ · |
 2 | · ★ ★ ★ ★ · · · · · |
 3 | · █ █ █ █ █ █ █ ★ · |
 4 | · · · · · · · █ ★ · |
 5 | █ █ █ █ █ · · █ ★ · |
 6 | · · · · · · · █ ★ · |
 7 | · █ █ █ █ █ · █ ★ · |
 8 | · · · · · · · · ★ · |
 9 | · · · █ █ █ █ █ ★ G |
   +---------------------+
```

## 🏆 Learning Outcomes

- Graph representation and traversal
- Priority queues and heaps
- Heuristic functions and admissibility
- Pathfinding algorithms (A*, Dijkstra)
- Algorithm visualization techniques

## 👨‍💻 Author

**Your Name**  
Syntecxhub AI Internship Program

## 📄 License

This project is licensed under the MIT License.

---

<p align="center">
  Made with ❤️ for Syntecxhub Internship Program
</p>
