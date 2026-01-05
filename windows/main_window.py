# windows/main_window.py

import asyncio
import tkinter as tk
from scheduler.scheduler import TaskScheduler
from windows.stage_window import StageWindow
from windows.spec_window import SpecWindow
from windows.massflow_window import MassFlowWindow

# from scheduler.ui import SchedulerUI
from windows.scheduler_window import SchedulerWindow
# from windows.task_b_window import TaskBWindow

class MainWindow:
    def __init__(self, master, loop):
        self.master = master
        self.loop = loop

        self.scheduler = TaskScheduler(loop)

        self._build_ui()

    def _build_ui(self):
        self.master.title("Main Launcher")

        # # スケジューラを開始するボタン
        # start_button = tk.Button(self.master, text="Start Scheduler", command=self._start_scheduler)
        # start_button.pack()

        # # スケジューラを停止するボタン
        # stop_button = tk.Button(self.master, text="Stop Scheduler", command=self._stop_scheduler)
        # stop_button.pack()

        for col in range(3):
            self.master.grid_columnconfigure(col, weight=1)

        # テキストを
        label = tk.Label(self.master, text="Open Programs")
        label.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Stageウィンドウを開くボタン
        button_stage = tk.Button(self.master, text="Stage\n🎛️", command=self._open_task_a)
        button_stage.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        button_spec = tk.Button(self.master, text="Spectrometer\n🌈", command=self._open_task_b)
        button_spec.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        button_masflow = tk.Button(self.master, text="MassFlowController\n💭", command=self._open_task_c)
        button_masflow.grid(row=1, column=2, sticky="ew", padx=5, pady=5)

        button_scheduler = tk.Button(self.master, text="Scheduler\n⏱", command=self._open_shceduler)
        button_scheduler.grid(row=2, column=1, sticky="ew", padx=5, pady=5)


    def _start_scheduler(self):
        # スケジューラを開始
        asyncio.run_coroutine_threadsafe(self.scheduler.start(), self.loop)

    def _stop_scheduler(self):
        # スケジューラを停止
        asyncio.run_coroutine_threadsafe(self.scheduler.stop(), self.loop)

    def _open_task_a(self):
        # Stageウィンドウを開く
        StageWindow(self.master, self.loop)
    
    def _open_task_b(self):
        # Spectrometerウィンドウを開く
        SpecWindow(self.master, self.loop)

    def _open_task_c(self):
        # MassFlowControllerウィンドウを開く
        MassFlowWindow(self.master, self.loop)

    def _open_shceduler(self):
        SchedulerWindow(self.master,  self.loop)

