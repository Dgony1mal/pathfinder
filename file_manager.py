from tkinter import filedialog

def save_map(app):
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )

    if not filename:
        return

    with open(filename, "w", encoding="utf-8") as file:
        for row in app.grid:
            file.write(" ".join(map(str, row)) + "\n")

def load_map(app):
    filename = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt")]
    )

    if not filename:
        return

    with open(filename, "r", encoding="utf-8") as file:
        rows = file.readlines()

    app.start = None
    app.finish = None

    for r, line in enumerate(rows):

        values = list(map(int, line.split()))

        for c, value in enumerate(values):

            app.grid[r][c] = value

            if value == 2:
                app.start = (r, c)

            elif value == 3:
                app.finish = (r, c)

    app.visited = 0
    app.path_length = 0
    app.execution_time = 0

    app.update_status()

    app.queue_box.delete(0, "end")

    app.draw_grid()

def save_result(app):
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )

    if not filename:
        return

    with open(filename, "w", encoding="utf-8") as file:

        file.write("Результат поиска пути\n\n")

        file.write(f"Алгоритм: {app.current_algorithm}\n")
        file.write(f"Посещено вершин: {app.visited}\n")
        file.write(f"Длина пути: {app.path_length}\n")
        file.write(f"Время: {app.execution_time:.3f} сек\n\n")

        file.write("Карта:\n")

        for row in app.grid:
            file.write(" ".join(map(str, row)) + "\n")