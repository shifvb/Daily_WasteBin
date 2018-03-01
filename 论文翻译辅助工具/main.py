import tkinter as tk
import threading
from utils.translate_from_google_api import translate_text


class PaperTranslatorApp(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1280x480")

        # 用户粘贴英文原文区域
        paste_frame = tk.LabelFrame(text="在此粘贴英文原文")
        paste_frame.grid(row=0, column=0)
        self.paste_text = tk.Text(paste_frame)
        self.paste_text.grid(row=0, column=0)
        paste_scrollbar = tk.Scrollbar(paste_frame, command=self.paste_text.yview)
        paste_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.paste_text.configure(yscrollcommand=paste_scrollbar.set)
        self.paste_text.bind("<Control-KeyRelease-v>", self.paste_callback)
        self.paste_text.focus_set()

        # 显示翻译区域
        translate_frame = tk.LabelFrame(text="翻译")
        translate_frame.grid(row=0, column=1)

        trans_btn = tk.Button(translate_frame, text="translate", command=self.translate_callback)
        trans_btn.grid(row=0, column=0)

        self.trans_text = tk.Text(translate_frame)
        self.trans_text.grid(row=1, column=0)
        trans_scrollbar = tk.Scrollbar(translate_frame, command=self.trans_text.yview)
        trans_scrollbar.grid(row=1, column=1, sticky=tk.NS)
        self.trans_text.configure(yscrollcommand=trans_scrollbar.set)

        tk.mainloop()

    def paste_callback(self, event):
        # 处理粘贴的文本
        _str = self.paste_text.get("1.0", tk.END)
        self.paste_text.delete("1.0", tk.END)
        _str = _str.replace("-\n", "")
        _str = _str.replace("[\n", "[")
        _str = _str.replace("\n]", "]")
        _str = _str.replace("\n", " ")
        self.paste_text.insert("1.0", _str)

    def translate_callback(self):
        """翻译"""

        def _():
            source_text = self.paste_text.get("1.0", tk.END)
            rsp = translate_text("zh_cn", source_text)
            self.trans_text.delete("1.0", tk.END)
            self.trans_text.insert("1.0", rsp['translatedText'])

        threading.Thread(target=_).start()


if __name__ == '__main__':
    app = PaperTranslatorApp()
