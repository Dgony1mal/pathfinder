import tkinter as tk

# Размер поля
ROWS = 30
COLS = 30
CELL_SIZE = 20

class PathfinderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Визуализатор алгоритмов поиска пути")

        width = COLS * CELL_SIZE
        height = ROWS * CELL_SIZE

        # Карта:
        # 0 - пустая клетка
        # 1 - препятствие
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        self.canvas = tk.Canvas(
            self.root,
            width=width,
            height=height,
            bg="white"
        )

        self.canvas.pack(padx=10, pady=10)

        # Нажатие левой кнопкой мыши
        self.canvas.bind("<Button-1>", self.left_click)

        self.draw_grid()

    def draw_grid(self):
        """Рисует всю карту."""

        self.canvas.delete("all")

        for row in range(ROWS):
            for col in range(COLS):

                if self.grid[row][col] == 1:
                    color = "black"
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

    def left_click(self, event):
        """Рисование препятствий."""

        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        if row >= ROWS or col >= COLS:
            return

        # Переключение клетки
        if self.grid[row][col] == 0:
            self.grid[row][col] = 1
        else:
            self.grid[row][col] = 0

        self.draw_grid()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PathfinderApp()
    app.run()