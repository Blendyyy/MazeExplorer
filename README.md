MazeExplorer
============

This program generates, displays, and solves a random maze using a Tkinter graphical interface.
It implements two classic pathfinding algorithms:

- BFS (Breadth-First Search): explores level by level and guarantees the shortest path.
- DFS (Depth-First Search): explores deeply and is often faster, but not always optimal.

The program also allows you to compare execution times and display performance analysis graphs.

Main Features
--------------
- Generate a random maze (odd dimensions only).
- Automatically solve it using BFS or DFS.
- Compare execution time between BFS and DFS.
- Display a performance graph showing average time versus maze size.

Notes
------
- The larger the maze, the longer generation and solving will take.
- The display zoom can be adjusted in the function afficher() (default ×3).
- Required libraries:
  - tkinter (included with Python)
  - Pillow
  - matplotlib
