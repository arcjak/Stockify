import tkinter as tk
from model import DataHandler
from view import DataView
from controller import DataController

if __name__ == "__main__":
    root = tk.Tk()
    model = DataHandler()
    view = DataView(root, None)
    controller = DataController(view, model)
    view.controller = controller
    root.mainloop()
