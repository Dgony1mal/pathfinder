import tkinter as tk

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

        self.canvas = tk.Canvas(
            self.root,
            width=COLS * CELL_SIZE,
            height=ROWS * CELL_SIZE,
            bg="white"
        )

        self.canvas.pack(pady=10)

        self.canvas.bind("<Button-1>", self.left_click)

        self.draw_grid()

    def create_toolbar(self):

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(
            frame,
            text="Стены",
            width=12,
            command=lambda: self.set_mode("wall")
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame,
            text="Старт",
            width=12,
            command=lambda: self.set_mode("start")
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame,
            text="Финиш",
            width=12,
            command=lambda: self.set_mode("finish")
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame,
            text="Очистить",
            width=12,
            command=self.clear_grid
        ).pack(side=tk.LEFT, padx=5)

    def set_mode(self, mode):
        self.mode = mode

    def clear_grid(self):

        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        self.start = None
        self.finish = None

        self.draw_grid()

    def left_click(self, event):

        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        if row >= ROWS or col >= COLS:
            return

        if self.mode == "wall":

            if self.grid[row][col] == 0:
                self.grid[row][col] = 1
            else:
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

                if value == 0:
                    color = "white"

                elif value == 1:
                    color = "black"

                elif value == 2:
                    color = "green"

                elif value == 3:
                    color = "red"

                else:
                    color = "white"

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