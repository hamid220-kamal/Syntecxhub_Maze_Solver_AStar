// A* Maze Solver Pro - Main Application
// Syntecxhub AI Internship - Project 1 (Enhanced)

const CELL = { EMPTY: 0, WALL: 1, START: 2, GOAL: 3, PATH: 4, VISITED: 5 };
let maze = [], gridSize = 15, drawMode = 'wall', isAnimating = false;
let savedMaze = null;

// DOM Elements
const $ = id => document.getElementById(id);
const gridEl = $('maze-grid');
const speedSlider = $('speed');
const learningMode = $('learning-mode');
const learningPanel = $('learning-panel');
const learningContent = $('learning-content');

// Initialize
function init() {
    gridSize = parseInt($('grid-size').value);
    createEmptyMaze();
    renderMaze(gridEl, maze);
    setupEventListeners();
}

function createEmptyMaze() {
    maze = Array(gridSize).fill(null).map(() => Array(gridSize).fill(CELL.EMPTY));
    maze[1][1] = CELL.START;
    maze[gridSize - 2][gridSize - 2] = CELL.GOAL;
}

function renderMaze(container, mazeData, cellSize = 28) {
    const size = mazeData.length;
    container.innerHTML = '';
    container.style.gridTemplateColumns = `repeat(${size}, ${cellSize}px)`;

    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            const cell = document.createElement('div');
            cell.className = 'cell ' + getCellClass(mazeData[i][j]);
            cell.dataset.row = i;
            cell.dataset.col = j;
            cell.style.width = cellSize + 'px';
            cell.style.height = cellSize + 'px';

            if (mazeData[i][j] === CELL.START) cell.textContent = 'S';
            if (mazeData[i][j] === CELL.GOAL) cell.textContent = 'G';

            cell.addEventListener('click', () => handleCellClick(i, j));
            cell.addEventListener('mouseenter', e => { if (e.buttons === 1) handleCellClick(i, j); });
            container.appendChild(cell);
        }
    }
}

function getCellClass(type) {
    return ['empty', 'wall', 'start', 'goal', 'path', 'visited'][type] || 'empty';
}

function handleCellClick(row, col) {
    if (isAnimating) return;
    clearPathVisited();

    if (drawMode === 'start') {
        maze.forEach((r, i) => r.forEach((c, j) => { if (c === CELL.START) maze[i][j] = CELL.EMPTY; }));
        maze[row][col] = CELL.START;
    } else if (drawMode === 'goal') {
        maze.forEach((r, i) => r.forEach((c, j) => { if (c === CELL.GOAL) maze[i][j] = CELL.EMPTY; }));
        maze[row][col] = CELL.GOAL;
    } else if (drawMode === 'wall' && maze[row][col] === CELL.EMPTY) {
        maze[row][col] = CELL.WALL;
    } else if (drawMode === 'empty' && maze[row][col] === CELL.WALL) {
        maze[row][col] = CELL.EMPTY;
    }
    renderMaze(gridEl, maze);
}

function clearPathVisited() {
    maze.forEach((row, i) => row.forEach((c, j) => {
        if (c === CELL.PATH || c === CELL.VISITED) maze[i][j] = CELL.EMPTY;
    }));
}

function findStartGoal() {
    let start = null, goal = null;
    maze.forEach((row, i) => row.forEach((c, j) => {
        if (c === CELL.START) start = [i, j];
        if (c === CELL.GOAL) goal = [i, j];
    }));
    return { start, goal };
}

// Heuristics
const heuristics = {
    manhattan: (pos, goal) => Math.abs(pos[0] - goal[0]) + Math.abs(pos[1] - goal[1]),
    euclidean: (pos, goal) => Math.sqrt((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2),
    chebyshev: (pos, goal) => Math.max(Math.abs(pos[0] - goal[0]), Math.abs(pos[1] - goal[1]))
};

// A* with learning mode support
function astarSolve(mazeData, heuristicName = 'manhattan') {
    const { start, goal } = findStartGoal();
    if (!start || !goal) return { path: null, error: 'Missing start/goal' };

    const h = (pos) => heuristics[heuristicName](pos, goal);
    const rows = mazeData.length, cols = mazeData[0].length;
    const openSet = [{ pos: start, g: 0, f: h(start), path: [start] }];
    const visited = new Set();
    const visitedOrder = [];
    const gScores = { [start.join(',')]: 0 };
    const steps = [];

    while (openSet.length) {
        openSet.sort((a, b) => a.f - b.f);
        const current = openSet.shift();
        const key = current.pos.join(',');

        if (visited.has(key)) continue;
        visited.add(key);
        visitedOrder.push(current.pos);

        steps.push({
            pos: current.pos,
            g: current.g,
            h: h(current.pos),
            f: current.f,
            openSize: openSet.length,
            closedSize: visited.size
        });

        if (current.pos[0] === goal[0] && current.pos[1] === goal[1]) {
            return { path: current.path, visitedOrder, steps, cost: current.g };
        }

        for (const [dr, dc] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) {
            const nr = current.pos[0] + dr, nc = current.pos[1] + dc;
            const nKey = `${nr},${nc}`;

            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols &&
                mazeData[nr][nc] !== CELL.WALL && !visited.has(nKey)) {
                const tentativeG = current.g + 1;
                if (!(nKey in gScores) || tentativeG < gScores[nKey]) {
                    gScores[nKey] = tentativeG;
                    openSet.push({
                        pos: [nr, nc],
                        g: tentativeG,
                        f: tentativeG + h([nr, nc]),
                        path: [...current.path, [nr, nc]]
                    });
                }
            }
        }
    }
    return { path: null, visitedOrder, steps };
}

// Animation
async function animateSolution(visitedOrder, path, speed) {
    isAnimating = true;
    $('solve-btn').textContent = '⏹️ Stop';

    for (const [r, c] of visitedOrder) {
        if (!isAnimating) break;
        if (maze[r][c] === CELL.EMPTY) {
            maze[r][c] = CELL.VISITED;
            updateCell(r, c);
        }
        await delay(speed);
    }

    if (path && isAnimating) {
        for (const [r, c] of path) {
            if (!isAnimating) break;
            if (maze[r][c] !== CELL.START && maze[r][c] !== CELL.GOAL) {
                maze[r][c] = CELL.PATH;
                updateCell(r, c);
            }
            await delay(speed * 2);
        }
    }

    isAnimating = false;
    $('solve-btn').textContent = '▶️ Solve';
}

function updateCell(row, col) {
    const idx = row * gridSize + col;
    const cell = gridEl.children[idx];
    if (cell) cell.className = 'cell ' + getCellClass(maze[row][col]);
}

function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

// Solve handler
async function solve() {
    if (isAnimating) { isAnimating = false; return; }

    clearPathVisited();
    renderMaze(gridEl, maze);

    const start = performance.now();
    const result = astarSolve(maze, $('heuristic').value);
    const time = performance.now() - start;

    if (!result.path) {
        alert('❌ No path found!');
        updateStats(0, result.visitedOrder?.length || 0, time, 0);
        return;
    }

    if (learningMode.checked) showLearningInfo(result);

    await animateSolution(result.visitedOrder, result.path, parseInt(speedSlider.value));

    const efficiency = ((result.path.length / result.visitedOrder.length) * 100).toFixed(1);
    updateStats(result.path.length, result.visitedOrder.length, time, efficiency);
}

function updateStats(pathLen, explored, time, efficiency) {
    $('stat-path').textContent = pathLen || '-';
    $('stat-explored').textContent = explored || '-';
    $('stat-time').textContent = time ? time.toFixed(1) : '-';
    $('stat-efficiency').textContent = efficiency ? efficiency + '%' : '-';
}

function showLearningInfo(result) {
    learningPanel.style.display = 'block';
    const lastStep = result.steps[result.steps.length - 1];
    learningContent.innerHTML = `
        <p><strong>How A* Works:</strong></p>
        <p>1. Start at <code>S</code>, add to open set</p>
        <p>2. Pick node with lowest <code>f = g + h</code></p>
        <p>3. <code>g</code> = actual distance from start</p>
        <p>4. <code>h</code> = estimated distance to goal</p>
        <hr style="margin: 10px 0; border-color: rgba(255,255,255,0.1)">
        <p><strong>Final Stats:</strong></p>
        <p>Path Cost: <code>${result.cost}</code></p>
        <p>Nodes Explored: <code>${result.visitedOrder.length}</code></p>
        <p>Path Length: <code>${result.path.length}</code></p>
    `;
}

// Algorithm Race
async function algorithmRace() {
    const raceView = $('race-view');
    const singleView = $('single-view');
    document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
    document.querySelector('[data-view="race"]').classList.add('active');
    singleView.classList.remove('active');
    raceView.classList.add('active');

    const { start, goal } = findStartGoal();
    if (!start || !goal) { alert('Set start and goal first!'); return; }

    const algos = [
        { id: 'astar', name: 'A*', fn: () => astarSolve(maze, $('heuristic').value) },
        { id: 'dijkstra', name: 'Dijkstra', fn: () => Algorithms.dijkstra(maze, start, goal) },
        { id: 'greedy', name: 'Greedy', fn: () => Algorithms.greedy(maze, start, goal) },
        { id: 'bfs', name: 'BFS', fn: () => Algorithms.bfs(maze, start, goal) }
    ];

    for (const algo of algos) {
        const container = $(`maze-${algo.id}`);
        const statsEl = $(`stats-${algo.id}`);

        const mazeCopy = maze.map(r => [...r]);
        renderMaze(container, mazeCopy, 18);

        const startTime = performance.now();
        const result = algo.fn();
        const time = performance.now() - startTime;

        // Animate this algorithm
        if (result.visitedOrder) {
            for (const [r, c] of result.visitedOrder) {
                if (mazeCopy[r][c] === CELL.EMPTY) mazeCopy[r][c] = CELL.VISITED;
            }
        }
        if (result.path) {
            for (const [r, c] of result.path) {
                if (mazeCopy[r][c] !== CELL.START && mazeCopy[r][c] !== CELL.GOAL)
                    mazeCopy[r][c] = CELL.PATH;
            }
        }

        renderMaze(container, mazeCopy, 18);
        statsEl.textContent = result.path
            ? `Path: ${result.path.length} | Explored: ${result.visitedOrder?.length || 0} | ${time.toFixed(1)}ms`
            : 'No path';
    }
}

// Maze Generators
function generateMaze(type) {
    if (isAnimating) return;
    const size = gridSize % 2 === 0 ? gridSize + 1 : gridSize;

    if (type === 'backtrack') {
        maze = MazeGenerators.recursiveBacktrack(size, size);
    } else if (type === 'prims') {
        maze = MazeGenerators.prims(size, size);
    } else {
        maze = MazeGenerators.random(gridSize, gridSize, 0.3);
    }

    gridSize = maze.length;
    renderMaze(gridEl, maze);
    updateStats(0, 0, 0, 0);
}

// Features: Save/Load, Export, Theme
function saveMaze() {
    localStorage.setItem('savedMaze', JSON.stringify({ maze, gridSize }));
    alert('✅ Maze Saved!');
}

function loadMaze() {
    const data = localStorage.getItem('savedMaze');
    if (!data) { alert('❌ No saved maze found!'); return; }
    const parsed = JSON.parse(data);
    maze = parsed.maze;
    gridSize = parsed.gridSize;
    $('grid-size').value = gridSize > 25 ? 25 : (gridSize < 10 ? 10 : gridSize); // Approximate
    renderMaze(gridEl, maze);
    updateStats(0, 0, 0, 0);
}

function exportImage() {
    html2canvas(document.querySelector('.maze-card')).then(canvas => {
        const link = document.createElement('a');
        link.download = 'maze_solution.png';
        link.href = canvas.toDataURL();
        link.click();
    });
}

function toggleTheme() {
    const body = document.body;
    const btn = $('theme-btn');
    if (body.getAttribute('data-theme') === 'light') {
        body.removeAttribute('data-theme');
        btn.textContent = '🌙';
    } else {
        body.setAttribute('data-theme', 'light');
        btn.textContent = '☀️';
    }
}

// Event Listeners
function setupEventListeners() {
    $('solve-btn').onclick = solve;
    $('race-btn').onclick = algorithmRace;
    $('clear-btn').onclick = () => { createEmptyMaze(); renderMaze(gridEl, maze); updateStats(0, 0, 0, 0); };
    $('gen-backtrack').onclick = () => generateMaze('backtrack');
    $('gen-prims').onclick = () => generateMaze('prims');
    $('gen-random').onclick = () => generateMaze('random');

    $('save-btn').onclick = saveMaze;
    $('load-btn').onclick = loadMaze;
    $('export-btn').onclick = exportImage;
    $('theme-btn').onclick = toggleTheme;

    $('grid-size').onchange = () => { gridSize = parseInt($('grid-size').value); createEmptyMaze(); renderMaze(gridEl, maze); };
    speedSlider.oninput = () => $('speed-value').textContent = speedSlider.value;

    learningMode.onchange = () => learningPanel.style.display = learningMode.checked ? 'block' : 'none';

    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            drawMode = btn.dataset.mode;
        };
    });

    document.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.querySelectorAll('.maze-view').forEach(v => v.classList.remove('active'));
            $(`${btn.dataset.view}-view`).classList.add('active');
        };
    });
}

// Start
document.addEventListener('DOMContentLoaded', init);
