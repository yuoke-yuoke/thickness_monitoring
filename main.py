### main.py
import tkinter as tk
import asyncio
import threading

from common.async_tk import async_run_with_loop
from windows.main_window import MainWindow



def main():
    root = tk.Tk()
    root.title("Task GUI")

    loop = asyncio.new_event_loop()

    MainWindow(root, loop)

    async_run_with_loop(root, loop)


if __name__ == '__main__':
    main()