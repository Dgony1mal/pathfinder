import tkinter as tk

class PathfinderApp:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Визуализатор алгоритмов поиска пути")

        self.root.geometry("900x700")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PathfinderApp()
    app.run()