import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from .manager import PseudonymManager
from .detector import Detector
from .processors.docx_proc import DocxProcessor
from .processors.pdf_proc import PdfProcessor


class App:
    def __init__(self, root):
        self.root = root
        root.title("敏感信息假名化工具")
        self.mode = tk.StringVar(value="anonymize")
        self.inp_var = tk.StringVar()
        self.out_var = tk.StringVar()

        ttk.Label(root, text="敏感信息假名化工具", font=("TkDefaultFont", 14, "bold")).pack(pady=8)

        mode_frame = ttk.Frame(root)
        mode_frame.pack(pady=4)
        ttk.Radiobutton(mode_frame, text="假名化（anonymize）", variable=self.mode, value="anonymize").pack(side="left", padx=4)
        ttk.Radiobutton(mode_frame, text="还原（restore）", variable=self.mode, value="restore").pack(side="left", padx=4)

        in_frame = ttk.Frame(root)
        in_frame.pack(fill="x", padx=8, pady=4)
        ttk.Label(in_frame, text="输入文件：").pack(side="left")
        ttk.Entry(in_frame, textvariable=self.inp_var, state="readonly", width=50).pack(side="left", padx=4)
        ttk.Button(in_frame, text="浏览...", command=self.browse_input).pack(side="left")

        out_frame = ttk.Frame(root)
        out_frame.pack(fill="x", padx=8, pady=4)
        ttk.Label(out_frame, text="输出文件：").pack(side="left")
        ttk.Entry(out_frame, textvariable=self.out_var, state="readonly", width=50).pack(side="left", padx=4)
        ttk.Button(out_frame, text="另存为...", command=self.browse_output).pack(side="left")

        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=8)
        self.run_btn = ttk.Button(btn_frame, text="开始处理", command=self.run)
        self.run_btn.pack(side="left", padx=4)
        ttk.Button(btn_frame, text="清理映射表", command=self.clear).pack(side="left", padx=4)

        log_frame = ttk.Frame(root)
        log_frame.pack(fill="both", expand=True, padx=8, pady=4)
        self.log_text = tk.Text(log_frame, height=10, state="disabled")
        self.log_text.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        sb.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=sb.set)

    def log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def browse_input(self):
        path = filedialog.askopenfilename(filetypes=[("Word/PDF", "*.docx *.pdf"), ("所有文件", "*.*")])
        if path:
            self.inp_var.set(path)

    def browse_output(self):
        inp = self.inp_var.get()
        if inp:
            in_dir = os.path.dirname(inp)
            in_name = os.path.basename(inp)
            base, ext = os.path.splitext(in_name)
            default_name = f"{base}_pseudo{ext}" if self.mode.get() == "anonymize" else f"{base}_restored{ext}"
            initial_file = os.path.join(in_dir, default_name)
        else:
            initial_file = ""
        path = filedialog.asksaveasfilename(initialfile=initial_file, defaultextension=ext if inp else ".docx", filetypes=[("Word", "*.docx"), ("PDF", "*.pdf")])
        if path:
            self.out_var.set(path)

    def run(self):
        inp = self.inp_var.get()
        out = self.out_var.get()
        if not inp or not out:
            self.log("请先选择输入和输出文件")
            return
        ext = os.path.splitext(inp)[1].lower()
        if ext == ".docx":
            proc = DocxProcessor()
        elif ext == ".pdf":
            proc = PdfProcessor()
        else:
            self.log("仅支持 .docx / .pdf")
            return
        self.run_btn.config(state="disabled")
        self.log("开始处理...")
        self.root.update()
        try:
            mgr = PseudonymManager()
            det = Detector()
            if self.mode.get() == "anonymize":
                proc.anonymize(inp, out, mgr, det)
                self.log(f"假名化完成：{out}")
            else:
                proc.restore(inp, out, mgr)
                self.log(f"还原完成：{out}")
        except Exception as e:
            self.log(f"错误：{e}")
        finally:
            self.run_btn.config(state="normal")

    def clear(self):
        if messagebox.askyesno("确认", "确定删除映射表和密钥？此操作不可撤销。"):
            mgr = PseudonymManager()
            mgr.clear()
            self.log("映射表已清理")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()

