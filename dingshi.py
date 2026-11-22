import platform
import subprocess
import tkinter as tk
from tkinter import messagebox

SYSTEM = platform.system()


# ---------- 系统相关操作 ----------
def set_shutdown(seconds: int):
    """安排 seconds 秒后关机"""
    if SYSTEM == "Windows":
        # Windows 的 /t 参数单位是秒
        subprocess.run(["shutdown", "/s", "/t", str(seconds)], check=True)

    elif SYSTEM in ("Linux", "Darwin"):
        # Unix 系 shutdown -h +N，单位是分钟
        minutes = max(1, round(seconds / 60))
        cmd = ["shutdown", "-h", f"+{minutes}"]
        if SYSTEM == "Darwin":          # macOS 通常需要管理员权限
            cmd.insert(0, "sudo")
        subprocess.run(cmd, check=True)
    else:
        raise RuntimeError(f"暂不支持的系统：{SYSTEM}")


def cancel_shutdown() -> bool:
    """取消已设置的关机任务，成功返回 True"""
    try:
        if SYSTEM == "Windows":
            subprocess.run(["shutdown", "/a"], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(["shutdown", "-c"], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


# ---------- 图形界面 ----------
class ShutdownTimer:
    def __init__(self, root):
        self.root = root
        self.remaining = 0
        self.job = None

        root.title("定时关机小工具")
        root.resizable(False, False)

        tk.Label(root, text="多少分钟后关机：",
                 font=("Microsoft YaHei", 12)).pack(pady=(15, 5))

        self.entry = tk.Entry(root, justify="center",
                              font=("Microsoft YaHei", 14), width=10)
        self.entry.insert(0, "60")
        self.entry.pack()

        self.label = tk.Label(root, text="未设置",
                              font=("Microsoft YaHei", 11), fg="gray")
        self.label.pack(pady=12)

        frame = tk.Frame(root)
        frame.pack(pady=(0, 15))
        tk.Button(frame, text="开始", width=10,
                  command=self.start).grid(row=0, column=0, padx=6)
        tk.Button(frame, text="取消", width=10,
                  command=self.cancel).grid(row=0, column=1, padx=6)

    def start(self):
        try:
            minutes = float(self.entry.get())
            if minutes <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("输入错误", "请输入大于 0 的数字（分钟）")
            return

        seconds = int(minutes * 60)
        try:
            set_shutdown(seconds)
        except Exception as e:
            messagebox.showerror(
                "设置失败",
                f"{e}\n\nLinux / macOS 可能需要管理员权限运行。")
            return

        self.remaining = seconds
        self.tick()

    def tick(self):
        """每秒刷新一次倒计时显示"""
        if self.remaining <= 0:
            self.label.config(text="⏰ 时间到，正在关机…", fg="red")
            self.job = None
            return

        h, rem = divmod(self.remaining, 3600)
        m, s = divmod(rem, 60)
        self.label.config(text=f"剩余：{h:02d}:{m:02d}:{s:02d}", fg="green")
        self.remaining -= 1
        self.job = self.root.after(1000, self.tick)

    def cancel(self):
        if self.job is not None:
            self.root.after_cancel(self.job)
            self.job = None
        if cancel_shutdown():
            self.label.config(text="✅ 已取消定时关机", fg="gray")
        else:
            self.label.config(text="没有待执行的关机任务", fg="gray")


if __name__ == "__main__":
    root = tk.Tk()
    ShutdownTimer(root)
    root.mainloop()