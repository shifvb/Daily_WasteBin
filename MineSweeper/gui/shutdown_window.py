import tkinter as tk
from tkinter import messagebox
from tkinter import font


class ShutdownWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.top_level = self
        self.top_level.title("德玛西亚")
        self.top_level.geometry("400x120")
        self.top_level.resizable(False, False)
        self.big_font = font.Font(size=20)
        self.mid_font = font.Font(size=15)

        self.label_frame = tk.Frame(self.top_level, width=400, height=90)
        self.label_frame.propagate(False)
        self.label_frame.grid(row=0, column=0)
        self.label = tk.Label(self.label_frame, text="您的电脑即将关机", font=self.big_font)
        self.label.grid(row=0, column=0, padx=89, pady=15)

        self.button_frame = tk.Frame(self.top_level, width=400, height=30)
        self.button_frame.propagate(False)
        self.button_frame.grid(row=1, column=0, sticky=tk.NSEW)
        _padx = 23
        _pady = 12
        self.yes_btn = tk.Button(self.button_frame, text="是(Yes Yes Yes)", font=self.mid_font,
                                 command=lambda: self.top_level.destroy())
        self.yes_btn.grid(row=0, column=0, padx=_padx, pady=_pady)
        self.no_btn = tk.Button(self.button_frame, text="否(No No No)", font=self.mid_font,
                                command=lambda: self.top_level.destroy())
        self.no_btn.grid(row=0, column=1, padx=_padx, pady=_pady)
        self.top_level.focus_set()
