import subprocess
import sys
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

APP_NAME = "Douyin2Text GUI"


def run_yt_dlp(url, cookies_path):
    try:
        python_exe = sys.executable  # exe 内置 python

        cmd = [
            python_exe,
            "-m", "yt_dlp",
            "--no-check-certificates",   # ✅ 解决 SSL 问题
            "--cookies", cookies_path,
            "-f", "bv*",
            "-o", "video.%(ext)s",
            url
        ]

        subprocess.run(
            cmd,
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        messagebox.showinfo(APP_NAME, "视频下载成功")

    except subprocess.CalledProcessError as e:
        messagebox.showerror(APP_NAME, f"下载失败：\n{e}")
    except Exception as e:
        messagebox.showerror(APP_NAME, f"错误：\n{e}")


def start_download():
    url = url_entry.get().strip()
    cookies = cookies_path.get().strip()

    if not url:
        messagebox.showwarning(APP_NAME, "请输入抖音视频链接")
        return

    if not cookies or not os.path.exists(cookies):
        messagebox.showwarning(APP_NAME, "请加载 cookies.txt")
        return

    threading.Thread(
        target=run_yt_dlp,
        args=(url, cookies),
        daemon=True
    ).start()


def load_cookies():
    path = filedialog.askopenfilename(
        title="选择 cookies.txt",
        filetypes=[("Text File", "*.txt")]
    )
    if path:
        cookies_path.set(path)


# ---------------- GUI ----------------

root = tk.Tk()
root.title(APP_NAME)
root.geometry("520x260")
root.resizable(False, False)

tk.Label(root, text="抖音视频链接：").pack(pady=8)
url_entry = tk.Entry(root, width=70)
url_entry.pack()

tk.Button(root, text="加载 cookies.txt", command=load_cookies).pack(pady=10)
cookies_path = tk.StringVar()
tk.Label(root, textvariable=cookies_path, fg="green").pack()

tk.Button(
    root,
    text="开始下载",
    command=start_download,
    bg="#1aad19",
    fg="white",
    width=30,
    height=2
).pack(pady=18)

root.mainloop()
