import tkinter as tk

# Размер сетки
ROWS = 30
COLS = 30
CELL_SIZE = 20

class PathfinderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Визуализатор алгоритмов поиска пути")

        width = COLS * CELL_SIZE
        height = ROWS * CELL_SIZE

        self.canvas = tk.Canvas(
            self.root,
            width=width,
            height=height,
            bg="white"
        )

        self.canvas.pack(padx=10, pady=10)

        self.draw_grid()

    def draw_grid(self):
        """Рисование сетки"""

        for row in range(ROWS):
            for col in range(COLS):

                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE

                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    outline="lightgray"
                )

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PathfinderApp()
    app.run()