"""
A* Maze Solver - Core Implementation
=====================================
Solves mazes using the A* pathfinding algorithm with Manhattan/Euclidean heuristics.

Author: Your Name
Project: Syntecxhub AI Internship - Project 1
"""

import heapq
from typing import List, Tuple, Optional, Set, Dict
from dataclasses import dataclass, field
from enum import Enum


class CellType(Enum):
    """Types of cells in the maze"""
    EMPTY = 0      # Walkable path
    WALL = 1       # Blocked cell
    START = 2      # Starting position
    GOAL = 3       # Goal position
    PATH = 4       # Solution path
    VISITED = 5    # Explored during search


@dataclass(order=True)
class Node:
    """
    Represents a node in the A* search.
    
    Attributes:
        f_score: Total estimated cost (g + h)
        position: (row, col) coordinates
        g_score: Cost from start to this node
        h_score: Estimated cost from this node to goal
        parent: Previous node in the path
    """
    f_score: float
    position: Tuple[int, int] = field(compare=False)
    g_score: float = field(compare=False)
    h_score: float = field(compare=False)
    parent: Optional['Node'] = field(default=None, compare=False)


class HeuristicType(Enum):
    """Available heuristic functions"""
    MANHATTAN = "manhattan"
    EUCLIDEAN = "euclidean"
    CHEBYSHEV = "chebyshev"


class MazeSolver:
    """
    A* Pathfinding Algorithm Implementation
    
    Features:
    - Multiple heuristic options (Manhattan, Euclidean, Chebyshev)
    - 4-directional and 8-directional movement
    - Step-by-step search tracking for visualization
    - Handles unreachable goals gracefully
    """
    
    # 4-directional movement: Up, Down, Left, Right
    DIRECTIONS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # 8-directional movement: includes diagonals
    DIRECTIONS_8 = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # Cardinal
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
    ]
    
    def __init__(
        self,
        maze: List[List[int]],
        heuristic: HeuristicType = HeuristicType.MANHATTAN,
        allow_diagonal: bool = False
    ):
        """
        Initialize the maze solver.
        
        Args:
            maze: 2D grid where 0=empty, 1=wall, 2=start, 3=goal
            heuristic: Which heuristic function to use
            allow_diagonal: Whether to allow 8-directional movement
        """
        self.maze = [row[:] for row in maze]  # Deep copy
        self.rows = len(maze)
        self.cols = len(maze[0]) if maze else 0
        self.heuristic_type = heuristic
        self.directions = self.DIRECTIONS_8 if allow_diagonal else self.DIRECTIONS_4
        
        # Find start and goal positions
        self.start: Optional[Tuple[int, int]] = None
        self.goal: Optional[Tuple[int, int]] = None
        self._find_start_goal()
        
        # Tracking for visualization
        self.visited_order: List[Tuple[int, int]] = []
        self.search_steps: List[Dict] = []
    
    def _find_start_goal(self) -> None:
        """Locate start (2) and goal (3) positions in the maze."""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == CellType.START.value:
                    self.start = (i, j)
                elif self.maze[i][j] == CellType.GOAL.value:
                    self.goal = (i, j)
    
    def heuristic(self, pos: Tuple[int, int]) -> float:
        """
        Calculate heuristic distance from position to goal.
        
        Args:
            pos: Current position (row, col)
            
        Returns:
            Estimated distance to goal
        """
        if not self.goal:
            return 0
        
        dr = abs(pos[0] - self.goal[0])
        dc = abs(pos[1] - self.goal[1])
        
        if self.heuristic_type == HeuristicType.MANHATTAN:
            return dr + dc
        elif self.heuristic_type == HeuristicType.EUCLIDEAN:
            return (dr ** 2 + dc ** 2) ** 0.5
        else:  # Chebyshev
            return max(dr, dc)
    
    def _is_valid(self, row: int, col: int) -> bool:
        """Check if position is within bounds and not a wall."""
        return (
            0 <= row < self.rows and
            0 <= col < self.cols and
            self.maze[row][col] != CellType.WALL.value
        )
    
    def _get_movement_cost(self, dr: int, dc: int) -> float:
        """Get cost for moving in a direction (diagonal = √2)."""
        return 1.414 if (dr != 0 and dc != 0) else 1.0
    
    def _reconstruct_path(self, node: Node) -> List[Tuple[int, int]]:
        """Trace back from goal to start to get the path."""
        path = []
        current = node
        while current:
            path.append(current.position)
            current = current.parent
        return path[::-1]  # Reverse to get start-to-goal order
    
    def solve(self) -> Tuple[Optional[List[Tuple[int, int]]], Dict]:
        """
        Execute A* search to find the shortest path.
        
        Returns:
            Tuple of (path, stats) where:
            - path: List of (row, col) from start to goal, or None if unreachable
            - stats: Dictionary with search statistics
        """
        if not self.start or not self.goal:
            return None, {"error": "Start or goal not found in maze"}
        
        # Reset tracking
        self.visited_order = []
        self.search_steps = []
        
        # Initialize open and closed sets
        open_set: List[Node] = []
        closed_set: Set[Tuple[int, int]] = set()
        g_scores: Dict[Tuple[int, int], float] = {}
        
        # Create start node
        h = self.heuristic(self.start)
        start_node = Node(
            f_score=h,
            position=self.start,
            g_score=0,
            h_score=h,
            parent=None
        )
        heapq.heappush(open_set, start_node)
        g_scores[self.start] = 0
        
        nodes_explored = 0
        
        while open_set:
            # Get node with lowest f_score
            current = heapq.heappop(open_set)
            
            # Skip if already processed
            if current.position in closed_set:
                continue
            
            nodes_explored += 1
            closed_set.add(current.position)
            self.visited_order.append(current.position)
            
            # Record step for visualization
            self.search_steps.append({
                "position": current.position,
                "f_score": current.f_score,
                "g_score": current.g_score,
                "h_score": current.h_score,
                "open_count": len(open_set),
                "closed_count": len(closed_set)
            })
            
            # Goal reached!
            if current.position == self.goal:
                path = self._reconstruct_path(current)
                stats = {
                    "path_found": True,
                    "path_length": len(path),
                    "path_cost": current.g_score,
                    "nodes_explored": nodes_explored,
                    "heuristic": self.heuristic_type.value
                }
                return path, stats
            
            # Explore neighbors
            for dr, dc in self.directions:
                new_row = current.position[0] + dr
                new_col = current.position[1] + dc
                neighbor_pos = (new_row, new_col)
                
                if not self._is_valid(new_row, new_col):
                    continue
                
                if neighbor_pos in closed_set:
                    continue
                
                # Calculate tentative g_score
                move_cost = self._get_movement_cost(dr, dc)
                tentative_g = current.g_score + move_cost
                
                # Skip if we've found a better path before
                if neighbor_pos in g_scores and tentative_g >= g_scores[neighbor_pos]:
                    continue
                
                # This is a better path, record it
                g_scores[neighbor_pos] = tentative_g
                h = self.heuristic(neighbor_pos)
                neighbor_node = Node(
                    f_score=tentative_g + h,
                    position=neighbor_pos,
                    g_score=tentative_g,
                    h_score=h,
                    parent=current
                )
                heapq.heappush(open_set, neighbor_node)
        
        # No path found
        stats = {
            "path_found": False,
            "nodes_explored": nodes_explored,
            "heuristic": self.heuristic_type.value,
            "error": "Goal is unreachable - no valid path exists"
        }
        return None, stats
    
    def get_solution_maze(self, path: List[Tuple[int, int]]) -> List[List[int]]:
        """Create a copy of maze with solution path marked."""
        result = [row[:] for row in self.maze]
        
        # Mark visited cells
        for pos in self.visited_order:
            if result[pos[0]][pos[1]] == CellType.EMPTY.value:
                result[pos[0]][pos[1]] = CellType.VISITED.value
        
        # Mark path (overwrites visited)
        for pos in path:
            if result[pos[0]][pos[1]] not in [CellType.START.value, CellType.GOAL.value]:
                result[pos[0]][pos[1]] = CellType.PATH.value
        
        return result


def create_sample_maze() -> List[List[int]]:
    """Create a sample maze for testing."""
    # 0 = empty, 1 = wall, 2 = start, 3 = goal
    return [
        [2, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 3],
    ]


if __name__ == "__main__":
    # Quick test
    maze = create_sample_maze()
    solver = MazeSolver(maze, HeuristicType.MANHATTAN)
    path, stats = solver.solve()
    
    print("=" * 50)
    print("A* Maze Solver - Quick Test")
    print("=" * 50)
    print(f"\nStats: {stats}")
    if path:
        print(f"\nPath: {path}")
