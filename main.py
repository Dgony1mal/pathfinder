import tkinter as tk
from file_manager import save_map, load_map, save_result
from tkinter import messagebox
from collections import deque
import time

from constants import *
from algorithms import bfs, dfs, astar

class PathfinderApp:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Поиск пути | Бородихин А.Д. | БИС-24-3")

        self.mode = "wall"

        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        self.start = None
        self.finish = None

        self.search_running = False

        self.visited = 0
        self.path_length = 0
        self.execution_time = 0

        self.current_algorithm = "-"

        # ИЗМЕНЕНО: теперь храним словарь с путём и временем для каждого алгоритма
        self.results = {
            "BFS": {"path": "-", "time": "-"},
            "DFS": {"path": "-", "time": "-"},
            "A*": {"path": "-", "time": "-"}
        }

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

        tk.Label(
            self.info,
            text="Бородихин А. Д.\nБИС-24-3",
            font=("Arial", 11, "bold"),
            fg="navy"
        ).pack(pady=(0, 15))

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

        self.queue_title = tk.Label(
            self.info,
            text="Структура данных",
            font=("Arial", 10, "bold")
        )
        
        self.queue_title.pack(anchor="w", pady=(15, 5))

        self.queue_box = tk.Listbox(
            self.info,
            width=20,
            height=10
        )

        self.queue_box.pack(anchor="w")

        tk.Label(
            self.info,
            text="Сравнение алгоритмов",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(15, 5))

        self.compare = tk.Label(
            self.info,
            justify="left",
            anchor="nw",
            width=35,
            font=("Consolas", 10)
        )

        self.compare.pack(anchor="w")

        self.update_compare()

        self.update_status()

        self.canvas.bind("<Button-1>", self.left_click)

        self.draw_grid()

    def create_toolbar(self):
        # Основной фрейм для всей панели
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # ---------- Верхний ряд: режимы и файловые операции ----------
        top_frame = tk.Frame(frame)
        top_frame.pack()

        buttons_top = [
            ("Стены", "wall"),
            ("Старт", "start"),
            ("Финиш", "finish"),
            ("Очистить", "clear"),
            ("Открыть", "open"),
            ("Сохранить", "save"),
            ("Экспорт", "export")
        ]

        for text, cmd in buttons_top:
            if cmd == "wall":
                btn = tk.Button(top_frame, text=text, command=lambda: self.set_mode("wall"), width=10)
            elif cmd == "start":
                btn = tk.Button(top_frame, text=text, command=lambda: self.set_mode("start"), width=10)
            elif cmd == "finish":
                btn = tk.Button(top_frame, text=text, command=lambda: self.set_mode("finish"), width=10)
            elif cmd == "clear":
                btn = tk.Button(top_frame, text=text, command=self.clear_grid, width=10)
            elif cmd == "open":
                btn = tk.Button(top_frame, text=text, command=lambda: load_map(self), width=10)
            elif cmd == "save":
                btn = tk.Button(top_frame, text=text, command=lambda: save_map(self), width=10)
            elif cmd == "export":
                btn = tk.Button(top_frame, text=text, command=lambda: save_result(self), width=10)
            btn.pack(side=tk.LEFT, padx=2)

        # ---------- Нижний ряд: алгоритмы ----------
        bottom_frame = tk.Frame(frame)
        bottom_frame.pack(pady=(5, 0))

        tk.Button(bottom_frame, text="BFS", command=self.run_bfs, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(bottom_frame, text="DFS", command=self.run_dfs, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(bottom_frame, text="A*", command=self.run_astar, width=10).pack(side=tk.LEFT, padx=2)

    def run_dfs(self):

        if self.start is None or self.finish is None:
            messagebox.showwarning(
                "Ошибка",
                "Укажите старт и финиш."
            )
            return

        self.reset_search()

        self.search_running = True

        self.current_algorithm = "DFS"

        self.queue_title.config(text="Стек DFS")

        dfs(self)   # внутри теперь замеряется время и обновляется статус

    def run_astar(self):

        if self.start is None or self.finish is None:
            messagebox.showwarning(
                "Ошибка",
                "Укажите старт и финиш."
            )
            return

        if self.search_running:
            return

        self.reset_search()

        self.search_running = True

        self.current_algorithm = "A*"

        self.queue_title.config(text="Приоритетная очередь А*")

        astar(self)   # внутри теперь замеряется время и обновляется статус

    def set_mode(self, mode):
        self.mode = mode

    def clear_grid(self):

        self.search_running = False

        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        self.start = None
        self.finish = None

        self.search_running = False

        self.visited = 0
        self.path_length = 0
        self.execution_time = 0

        self.current_algorithm = "-"

        # Сброс результатов сравнения
        self.results = {
            "BFS": {"path": "-", "time": "-"},
            "DFS": {"path": "-", "time": "-"},
            "A*": {"path": "-", "time": "-"}
        }

        self.update_status()
        self.update_compare()
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
            "Статистика\n\n"
            f"Алгоритм : {self.current_algorithm}\n"
            f"Посещено : {self.visited}\n"
            f"Путь      : {self.path_length}\n"
            f"Время     : {self.execution_time:.3f} сек"
        )

        self.status.config(text=text)

    def update_compare(self):
        # ИЗМЕНЕНО: теперь отображаем и путь, и время
        text = (
            "Алгоритм   Путь     Время(с)\n\n"
            f"BFS        {self.results['BFS']['path']:>3}      {self.results['BFS']['time']:>6}\n"
            f"DFS        {self.results['DFS']['path']:>3}      {self.results['DFS']['time']:>6}\n"
            f"A*         {self.results['A*']['path']:>3}      {self.results['A*']['time']:>6}"
        )
        self.compare.config(text=text)

    def reset_search(self):
        """Очистить результаты предыдущего поиска."""

        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c] in (VISITED, PATH):
                    self.grid[r][c] = EMPTY

        self.visited = 0
        self.path_length = 0
        self.execution_time = 0

        self.current_algorithm = "-"

        self.queue_title.config(text="Структура данных")

        self.queue_box.delete(0, tk.END)

        self.update_status()
        self.draw_grid()

    def run_bfs(self):

        if self.start is None or self.finish is None:
            messagebox.showwarning(
                "Ошибка",
                "Укажите старт и финиш."
            )
            return

        if self.search_running:
            return

        self.reset_search()

        self.search_running = True

        self.current_algorithm = "BFS"

        self.queue_title.config(text="Очередь BFS")

        bfs(self)   # внутри теперь замеряется время и обновляется статус

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