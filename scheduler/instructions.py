import tkinter as tk
import asyncio
import numpy as np

class SchedulerInstructions:
    def __init__(self, loop):
        self.loop = loop
        
        self.num_loops = 30
        self.num_pos = 4
        self.interval_time = 10000   # [ms]

        self.cur_pos = 0
        self.cur_loop = 0
        self.running = False
        self.scheduler_log = []

        self.stage_on = tk.BooleanVar(value=False)
        self.spec_on = tk.BooleanVar(value=False)
        self.gas_on = tk.BooleanVar(value=False)

        self._cancel_event = asyncio.Event()
        # self.scheduler = TaskScheduler(loop)
        # self.ui = SchedulerUI(self.loop, self.scheduler)
        # self.handler = StageHandler(self.logic, self.ui, self.scheduler)
        # self.ui.set_handler(self.handler)