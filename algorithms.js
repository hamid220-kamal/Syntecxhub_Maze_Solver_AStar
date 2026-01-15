// Advanced Pathfinding Algorithms Module
// Syntecxhub AI Internship - Project 1 (Enhanced)

const Algorithms = {
    // Dijkstra's Algorithm (A* without heuristic)
    dijkstra: function (maze, start, goal) {
        return this.astar(maze, start, goal, () => 0, "Dijkstra");
    },

    // Greedy Best-First (only heuristic, no g-cost)
    greedy: function (maze, start, goal) {
        return this.astar(maze, start, goal, (pos) => {
            return Math.abs(pos[0] - goal[0]) + Math.abs(pos[1] - goal[1]);
        }, "Greedy", true);
    },

    // BFS (Breadth-First Search)
    bfs: function (maze, start, goal) {
        const rows = maze.length, cols = maze[0].length;
        const queue = [[start, [start]]];
        const visited = new Set([start.join(',')]);
        const visitedOrder = [];

        while (queue.length > 0) {
            const [current, path] = queue.shift();
            visitedOrder.push(current);

            if (current[0] === goal[0] && current[1] === goal[1]) {
                return { path, visitedOrder, name: "BFS" };
            }

            for (const [dr, dc] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) {
                const nr = current[0] + dr, nc = current[1] + dc;
                const key = `${nr},${nc}`;
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols &&
                    maze[nr][nc] !== 1 && !visited.has(key)) {
                    visited.add(key);
                    queue.push([[nr, nc], [...path, [nr, nc]]]);
                }
            }
        }
        return { path: null, visitedOrder, name: "BFS" };
    },

    // A* with configurable heuristic
    astar: function (maze, start, goal, heuristic, name = "A*", greedy = false) {
        const rows = maze.length, cols = maze[0].length;
        const openSet = [{ pos: start, g: 0, f: heuristic(start), path: [start] }];
        const visited = new Set();
        const visitedOrder = [];
        const gScores = { [start.join(',')]: 0 };

        while (openSet.length > 0) {
            openSet.sort((a, b) => a.f - b.f);
            const current = openSet.shift();
            const key = current.pos.join(',');

            if (visited.has(key)) continue;
            visited.add(key);
            visitedOrder.push(current.pos);

            if (current.pos[0] === goal[0] && current.pos[1] === goal[1]) {
                return { path: current.path, visitedOrder, name, cost: current.g };
            }

            for (const [dr, dc] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) {
                const nr = current.pos[0] + dr, nc = current.pos[1] + dc;
                const nKey = `${nr},${nc}`;

                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols &&
                    maze[nr][nc] !== 1 && !visited.has(nKey)) {
                    const tentativeG = greedy ? 0 : current.g + 1;
                    if (!(nKey in gScores) || tentativeG < gScores[nKey]) {
                        gScores[nKey] = tentativeG;
                        const h = heuristic([nr, nc]);
                        openSet.push({
                            pos: [nr, nc],
                            g: tentativeG,
                            f: tentativeG + h,
                            path: [...current.path, [nr, nc]]
                        });
                    }
                }
            }
        }
        return { path: null, visitedOrder, name };
    },

    // Manhattan heuristic
    manhattan: (pos, goal) => Math.abs(pos[0] - goal[0]) + Math.abs(pos[1] - goal[1])
};

// Maze Generation Algorithms
const MazeGenerators = {
    // Recursive Backtracking (DFS)
    recursiveBacktrack: function (rows, cols) {
        const maze = Array(rows).fill(null).map(() => Array(cols).fill(1));
        const stack = [[1, 1]];
        maze[1][1] = 0;

        while (stack.length > 0) {
            const [r, c] = stack[stack.length - 1];
            const neighbors = [];

            for (const [dr, dc] of [[-2, 0], [2, 0], [0, -2], [0, 2]]) {
                const nr = r + dr, nc = c + dc;
                if (nr > 0 && nr < rows - 1 && nc > 0 && nc < cols - 1 && maze[nr][nc] === 1) {
                    neighbors.push([nr, nc, r + dr / 2, c + dc / 2]);
                }
            }

            if (neighbors.length > 0) {
                const [nr, nc, wr, wc] = neighbors[Math.floor(Math.random() * neighbors.length)];
                maze[wr][wc] = 0;
                maze[nr][nc] = 0;
                stack.push([nr, nc]);
            } else {
                stack.pop();
            }
        }

        maze[1][1] = 2; // Start
        maze[rows - 2][cols - 2] = 3; // Goal
        return maze;
    },

    // Prim's Algorithm
    prims: function (rows, cols) {
        const maze = Array(rows).fill(null).map(() => Array(cols).fill(1));
        const walls = [];

        const addWalls = (r, c) => {
            for (const [dr, dc] of [[-2, 0], [2, 0], [0, -2], [0, 2]]) {
                const nr = r + dr, nc = c + dc;
                if (nr > 0 && nr < rows - 1 && nc > 0 && nc < cols - 1) {
                    walls.push([nr, nc, r + dr / 2, c + dc / 2]);
                }
            }
        };

        maze[1][1] = 0;
        addWalls(1, 1);

        while (walls.length > 0) {
            const idx = Math.floor(Math.random() * walls.length);
            const [nr, nc, wr, wc] = walls.splice(idx, 1)[0];

            if (maze[nr][nc] === 1) {
                maze[wr][wc] = 0;
                maze[nr][nc] = 0;
                addWalls(nr, nc);
            }
        }

        maze[1][1] = 2;
        maze[rows - 2][cols - 2] = 3;
        return maze;
    },

    // Random with density
    random: function (rows, cols, density = 0.3) {
        const maze = Array(rows).fill(null).map(() =>
            Array(cols).fill(null).map(() => Math.random() < density ? 1 : 0)
        );
        maze[0][0] = 2;
        maze[rows - 1][cols - 1] = 3;
        // Clear around start/goal
        [[0, 1], [1, 0], [1, 1]].forEach(([dr, dc]) => {
            if (maze[dr]) maze[dr][dc] = 0;
            if (maze[rows - 1 - dr]) maze[rows - 1 - dr][cols - 1 - dc] = 0;
        });
        return maze;
    }
};

// Export for use
if (typeof module !== 'undefined') {
    module.exports = { Algorithms, MazeGenerators };
}
