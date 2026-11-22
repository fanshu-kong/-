# 定时关机小工具

一个轻量的图形化定时关机工具，基于 Python + Tkinter 编写，支持 Windows / Linux / macOS。
输入分钟数即可倒计时关机，并随时一键取消。

> 无需命令行操作，双击打开、填数字、点「开始」即可。

## 功能特性

- **定时关机**：输入多少分钟后关机，实时显示 `时:分:秒` 倒计时
- **一键取消**：随时取消已设置的关机任务
- **图形界面**：Tkinter 原生窗口，体积小、启动快
- **跨平台**：Windows 用 `shutdown /s /t`，Linux / macOS 用 `shutdown -h +N`
- **零依赖**：仅使用 Python 标准库，无需安装任何第三方包

## 快速开始

### 方式一：直接使用（推荐普通用户）

到 [Releases](../../releases) 页面下载 `定时关机.exe`，**双击运行**即可，无需安装 Python。

> 适用于 64 位 Windows。

### 方式二：从源码运行

需要 Python 3.8 及以上（自带 tkinter）：

```bash
python dingshi.py
```

Linux / macOS 若提示权限不足，请用管理员权限运行：

```bash
sudo python3 dingshi.py
```

## 使用说明

1. 在输入框中填入「多少分钟后关机」，默认为 60
2. 点击 **开始**，界面会显示倒计时
3. 若想放弃关机，点击 **取消** 即可清除任务

> 小技巧：把 exe 发送到桌面快捷方式，日常使用更方便。

## 自行打包 exe

Windows 下如需重新生成可执行文件：

```bash
pip install pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name "定时关机" dingshi.py
```

生成的 `定时关机.exe` 位于 `dist/` 目录（单文件、无控制台窗口）。

## 项目结构

```
├── dingshi.py     # 程序源码（唯一程序文件）
├── README.md
└── .gitignore
```

## 注意事项

- Windows 的定时关机由系统 `shutdown` 命令实现，关机前会弹出系统提示
- 程序关闭后，已设置的关机任务**仍然有效**（任务由系统持有），可用「取消」或 `shutdown /a` 撤销
- 部分系统取消了关机操作需要管理员权限

## License

如无特别说明，本项目未指定开源协议。若希望他人自由使用，建议补充 [MIT License](https://choosealicense.com/licenses/mit/)。
