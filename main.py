import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from random import randint, choice
from collections import deque
import time
import matplotlib.pyplot as plt


def unconnected_adjacent_cells(img, x, y):
    neighbors = []
    for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < img.width and 0 <= ny < img.height:
            if img.getpixel((nx, ny)) == (128, 128, 128):
                neighbors.append((nx, ny))
    return neighbors


def create_maze(w, h):
    img = Image.new("RGB", (w, h), (0, 0, 0))
    for i in range(1, w, 2):
        for j in range(1, h, 2):
            img.putpixel((i, j), (128, 128, 128))

    x, y = randint(0, w // 2 - 1) * 2 + 1, randint(0, h // 2 - 1) * 2 + 1
    img.putpixel((x, y), (255, 255, 255))
    path = []

    while True:
        neighbors = unconnected_adjacent_cells(img, x, y)
        if not neighbors:
            if not path:
                break
            x, y = path.pop()
            continue
        nx, ny = choice(neighbors)
        img.putpixel((nx, ny), (255, 255, 255))
        img.putpixel(((x + nx) // 2, (y + ny) // 2), (255, 255, 255))
        path.append((x, y))
        x, y = nx, ny

    entrance = randint(0, w // 2 - 1) * 2 + 1
    exit_ = randint(0, w // 2 - 1) * 2 + 1
    img.putpixel((entrance, 0), (255, 255, 255))
    img.putpixel((exit_, h - 1), (255, 255, 255))
    return img


def unvisited_neighbors(img, x, y):
    neighbors = []
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < img.width and 0 <= ny < img.height:
            if img.getpixel((nx, ny)) == (255, 255, 255):
                neighbors.append((nx, ny))
    return neighbors


def find_start(img):
    for x in range(img.width):
        if img.getpixel((x, 0)) == (255, 255, 255):
            return (x, 0)
    raise ValueError("No start point found.")


def draw_path(img, path):
    for x, y in path:
        img.putpixel((x, y), (255, 0, 0))


def solve(img, algorithm="BFS"):
    start = find_start(img)
    if algorithm == "BFS":
        queue = deque([start])
        origins = {}
        while queue:
            n = queue.popleft()
            img.putpixel(n, (128, 128, 128))
            if n[1] == img.height - 1:
                path = [n]
                while n in origins:
                    n = origins[n]
                    path.append(n)
                return list(reversed(path))
            for v in unvisited_neighbors(img, *n):
                if v not in origins:
                    queue.append(v)
                    origins[v] = n
        return None
    else:  # DFS
        path = []
        node = start
        while node[1] < img.height - 1:
            neighbors = unvisited_neighbors(img, *node)
            if not neighbors:
                if not path:
                    return None
                node = path.pop()
                continue
            path.append(node)
            node = neighbors[0]
            img.putpixel(node, (128, 128, 128))
        path.append(node)
        return path


class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Explorer")
        self.maze = None

        self._create_form()
        self._create_buttons()
        self._create_display()

    def _create_form(self):
        frm = tk.Frame(self.root)
        frm.pack(pady=10)

        tk.Label(frm, text="Width (odd)").grid(row=0, column=0)
        tk.Label(frm, text="Height (odd)").grid(row=1, column=0)
        tk.Label(frm, text="Iterations per point (graph)").grid(row=2, column=0)

        self.entry_w = tk.Entry(frm)
        self.entry_w.insert(0, "51")
        self.entry_h = tk.Entry(frm)
        self.entry_h.insert(0, "51")
        self.entry_iter = tk.Entry(frm)
        self.entry_iter.insert(0, "5")

        self.entry_w.grid(row=0, column=1)
        self.entry_h.grid(row=1, column=1)
        self.entry_iter.grid(row=2, column=1)

    def _create_buttons(self):
        frm = tk.Frame(self.root)
        frm.pack(pady=5)

        tk.Button(frm, text="Generate", command=self.generate).grid(row=0, column=0, padx=5)
        tk.Button(frm, text="Solve BFS", command=lambda: self.solve_maze("BFS")).grid(row=0, column=1, padx=5)
        tk.Button(frm, text="Solve DFS", command=lambda: self.solve_maze("DFS")).grid(row=0, column=2, padx=5)
        tk.Button(frm, text="Compare BFS vs DFS", command=self.compare_time).grid(row=1, column=0, columnspan=2, pady=5)
        tk.Button(frm, text="Time vs Size Graph", command=self.graph_time_vs_size).grid(row=1, column=2, pady=5)

    def _create_display(self):
        self.label_img = tk.Label(self.root)
        self.label_img.pack(pady=10)

    def generate(self):
        try:
            w = int(self.entry_w.get())
            h = int(self.entry_h.get())
            if w % 2 == 0 or h % 2 == 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid dimensions (must be odd numbers)")
            return

        self.maze = create_maze(w, h)
        self.display(self.maze)
        messagebox.showinfo("Success", f"Maze {w}x{h} generated successfully.")

    def solve_maze(self, method):
        if not self.maze:
            messagebox.showwarning("Warning", "Please generate a maze first.")
            return

        copy = self.maze.copy()
        path = solve(copy, algorithm=method)
        if path:
            draw_path(copy, path)
            self.display(copy)
        else:
            messagebox.showerror("Error", "No path found.")

    def compare_time(self):
        if not self.maze:
            messagebox.showerror("Error", "Please generate a maze first.")
            return

        img_bfs = self.maze.copy()
        t1 = time.time()
        solve(img_bfs, "BFS")
        t2 = time.time()

        img_dfs = self.maze.copy()
        t3 = time.time()
        solve(img_dfs, "DFS")
        t4 = time.time()

        times = [t2 - t1, t4 - t3]
        plt.bar(["BFS", "DFS"], times, color=["blue", "green"])
        plt.ylabel("Time (seconds)")
        plt.title("BFS vs DFS Comparison")
        plt.tight_layout()
        plt.show()

    def graph_time_vs_size(self):
        try:
            n_iter = int(self.entry_iter.get())
            if n_iter < 1:
                raise ValueError
        except:
            messagebox.showerror("Error", "Please enter a valid number of iterations.")
            return

        sizes = [11, 21, 31, 41, 51]
        pixels, times_bfs, times_dfs = [], [], []

        for size in sizes:
            total_bfs = 0
            total_dfs = 0
            for _ in range(n_iter):
                img = create_maze(size, size)
                t1 = time.time()
                solve(img.copy(), "BFS")
                t2 = time.time()
                t3 = time.time()
                solve(img.copy(), "DFS")
                t4 = time.time()
                total_bfs += (t2 - t1)
                total_dfs += (t4 - t3)
            pixels.append(size * size)
            times_bfs.append(total_bfs / n_iter)
            times_dfs.append(total_dfs / n_iter)

        plt.plot(pixels, times_bfs, marker='o', label="BFS", color='blue')
        plt.plot(pixels, times_dfs, marker='o', label="DFS", color='green')
        plt.xlabel("Number of pixels")
        plt.ylabel("Average time (s)")
        plt.title(f"Time vs Size ({n_iter} iterations)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def display(self, img):
        zoom = img.resize((img.width * 3, img.height * 3), Image.NEAREST)
        self.tk_img = ImageTk.PhotoImage(zoom)
        self.label_img.config(image=self.tk_img)
        self.label_img.image = self.tk_img


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
