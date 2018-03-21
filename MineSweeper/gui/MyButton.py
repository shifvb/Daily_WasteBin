import tkinter as tk


class MyButton(tk.Button):
    def __init__(self, master, row_num=0, col_num=0, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.row_num = row_num
        self.col_num = col_num


if __name__ == '__main__':
    def callback(event):
        print(event.widget.row_num)


    root = tk.Tk()
    btn = MyButton(root, text="btn")
    btn.bind("<Button-1>", callback)
    btn.pack()
    tk.mainloop()
