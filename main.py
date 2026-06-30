import tkinter as tk
from tkinter import messagebox

ROWS = 30
COLS = 30
CELL_SIZE = 20

class PathfinderApp:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Визуализатор алгоритмов поиска пути")

        self.mode = "wall"

        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        self.start = None
        self.finish = None

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
            text="Алгоритм не выбран",
            justify="left"
        )

        self.status.pack(anchor="w", pady=10)

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
                  command=lambda: self.not_ready("BFS"),
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

        self.status.config(text="Карта очищена")

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

                color = "white"

                if value == 1:
                    color = "black"

                elif value == 2:
                    color = "green"

                elif value == 3:
                    color = "red"

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

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    PathfinderApp().run()        