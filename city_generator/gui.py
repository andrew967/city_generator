from city_generator.main_generation import main_generation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


def create_gui():
    root = tk.Tk()
    root.title("City Generation")

    def on_button_click(n_points):
        fig = main_generation(n_points)
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=0, columnspan=3)
        canvas.draw()

    tk.Button(root, text="Small", command=lambda: on_button_click(20)).grid(row=0, column=0)
    tk.Button(root, text="Medium", command=lambda: on_button_click(50)).grid(row=0, column=1)
    tk.Button(root, text="Large", command=lambda: on_button_click(100)).grid(row=0, column=2)

    root.mainloop()