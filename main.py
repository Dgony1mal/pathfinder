import tkinter as tk
from tkinter import messagebox
from collections import deque
import time

ROWS = 30
COLS = 30
CELL_SIZE = 20

COLORS = {
    0: "white",
    1: "black",
    2: "green",
    3: "red",
    4: "#6ec6ff",      # посещённая вершина
    5: "yellow"        # найденный путь
}

class PathfinderApp:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Визуализатор алгоритмов поиска пути")

        self.mode = "wall"

        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        self.start = None
        self.finish = None

        self.visited = 0
        self.path_length = 0
        self.execution_time = 0

        self.create_toolbar()

        body = tk.Frame(self.root)
        body.pack()

        self.canvas = tk.Canvas(
            body,
            width=COLS * CELL_SIZE,
            height=ROWS * CELL_SIZE,
            bg="white"
        )

        self.canvas.pack(side=tk.LEFT)

        self.info = tk.Frame(body)
        self.info.pack(side=tk.LEFT, padx=15, anchor="n")

        tk.Label(self.info, text="Статистика", font=("Arial", 12, "bold")).pack()

        self.status = tk.Label(
            self.info,
            justify="left",
            anchor="nw",
            width=24,
            height=10,
            font=("Consolas", 10)
        )

        self.status.pack(anchor="w")

        tk.Label(
            self.info,
            text="Очередь BFS",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(15, 5))

        self.queue_box = tk.Listbox(
            self.info,
            width=20,
            height=10
        )

        self.queue_box.pack(anchor="w")

        self.update_status()

        self.canvas.bind("<Button-1>", self.left_click)

        self.draw_grid()

    def create_toolbar(self):

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Стены",
                  command=lambda: self.set_mode("wall"),
                  width=10).pack(side=tk.LEFT, padx=2)

        tk.Button(frame, text="Старт",
                  command=lambda: self.set_mode("start"),
                  width=10).pack(side=tk.LEFT, padx=2)

        tk.Button(frame, text="Финиш",
                  command=lambda: self.set_mode("finish"),
                  width=10).pack(side=tk.LEFT, padx=2)

        tk.Button(frame, text="Очистить",
                  command=self.clear_grid,
                  width=10).pack(side=tk.LEFT, padx=2)

        tk.Button(frame, text="BFS",
                  command=self.run_bfs,
                  width=10).pack(side=tk.LEFT, padx=2)

        tk.Button(frame, text="DFS",
                  command=lambda: self.not_ready("DFS"),
                  width=10).pack(side=tk.LEFT, padx=2)

        tk.Button(frame, text="A*",
                  command=lambda: self.not_ready("A*"),
                  width=10).pack(side=tk.LEFT, padx=2)

    def not_ready(self, name):

        messagebox.showinfo(
            "Информация",
            f"Алгоритм {name} будет реализован на следующем этапе."
        )

    def set_mode(self, mode):
        self.mode = mode

    def clear_grid(self):

        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        self.start = None
        self.finish = None

        self.visited = 0
        self.path_length = 0
        self.execution_time = 0

        self.update_status()

        self.draw_grid()

    def left_click(self, event):

        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        if row >= ROWS or col >= COLS:
            return

        if self.mode == "wall":

            if self.grid[row][col] == 0:
                self.grid[row][col] = 1
            elif self.grid[row][col] == 1:
                self.grid[row][col] = 0

        elif self.mode == "start":

            if self.start:
                r, c = self.start
                self.grid[r][c] = 0

            self.start = (row, col)
            self.grid[row][col] = 2

        elif self.mode == "finish":

            if self.finish:
                r, c = self.finish
                self.grid[r][c] = 0

            self.finish = (row, col)
            self.grid[row][col] = 3

        self.draw_grid()

    def draw_grid(self):

        self.canvas.delete("all")

        for row in range(ROWS):
            for col in range(COLS):

                value = self.grid[row][col]
                color = COLORS[value]

                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE

                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="gray"
                )

    def update_status(self):

        text = (
            f"Алгоритм: BFS\n\n"
            f"Посещено: {self.visited}\n"
            f"Длина пути: {self.path_length}\n"
            f"Время: {self.execution_time:.6f} сек"
        )

        self.status.config(text=text)

    def run_bfs(self):

        if self.start is None or self.finish is None:
            messagebox.showwarning(
                "Ошибка",
                "Укажите старт и финиш."
            )
            return

        start_time = time.perf_counter()

        queue = deque([self.start])

        parents = {}

        visited = {self.start}

        found = False

        while queue:

            current = queue.popleft()

            row, col = current

            if self.grid[row][col] == 0:
                self.grid[row][col] = 4

            self.draw_grid()

            self.update_queue(queue)

            self.root.update()

            self.root.after(20)

            if current == self.finish:
                found = True
                break

            row, col = current

            directions = [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1)
            ]

            for dr, dc in directions:

                nr = row + dr
                nc = col + dc

                if not (0 <= nr < ROWS and 0 <= nc < COLS):
                    continue

                if self.grid[nr][nc] == 1:
                    continue

                neighbor = (nr, nc)

                if neighbor in visited:
                    continue

                visited.add(neighbor)

                parents[neighbor] = current

                queue.append(neighbor)

        end_time = time.perf_counter()

        self.execution_time = end_time - start_time

        self.visited = len(visited)

        if found:
            self.restore_path(parents)

        else:
            messagebox.showinfo(
                "BFS",
                "Путь не найден."
            )

        self.update_status()

        self.queue_box.delete(0, tk.END)

    def restore_path(self, parents):

        current = self.finish

        length = 0

        while current != self.start:

            row, col = current

            if self.grid[row][col] != 2 and self.grid[row][col] != 3:
                self.grid[row][col] = 5

            current = parents[current]

            length += 1

        self.path_length = length

        self.draw_grid()

    def update_queue(self, queue):

        self.queue_box.delete(0, tk.END)

        for cell in list(queue)[:20]:
            self.queue_box.insert(
                tk.END,
                str(cell)
            )

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    PathfinderApp().run()        