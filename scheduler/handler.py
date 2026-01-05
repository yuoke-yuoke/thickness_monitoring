import asyncio
from tkinter import END

class SchedulerHandler:
    def __init__(self, logic, ui):
        self.logic = logic
        self.ui = ui
        # self.scheduler = scheduler
        self.ui.set_handler(self)
        # self.logic.set_handler(self)
        # Additional initialization if needed

    def play(self):
        if not self.logic.instructions.running:
            print("[SchedulerHandler] Starting scheduler")
            # asyncio.create_task(self.logic.start())
            self.get_variables()
            asyncio.run_coroutine_threadsafe(self.logic.start(), self.logic.instructions.loop)

    def stop(self):
        if self.logic.instructions.running:
            # asyncio.create_task(self.logic.stop())
            self.logic.stop()
    
    # def loop_initialize(self):
    #     self.logic.instructions.cur_loop = 0
    #     self.logic.instructions.cur_pos = 0
    #     self.ui.update_ui()
    
    def get_variables(self):
        # self.logic.instructions.running = True

        self.logic.instructions.interval_time = int(self.ui.interval_box.get())
        self.logic.instructions.num_loops = int(self.ui.loop_box.get())
        self.logic.initialize_instructions()

        print(f"[SchedulerHandler] Variables set: interval_time={self.logic.instructions.interval_time}, num_loops={self.logic.instructions.num_loops}, stage_on={self.logic.instructions.stage_on.get()}, spec_on={self.logic.instructions.spec_on.get()}, gas_on={self.logic.instructions.gas_on.get()}")


    # def update_ui(self):
    #     self.ui.interval_box.delete(0, END)
    #     self.ui.interval_box.insert(END, self.logic.instructions.interval_time)
    #     self.ui.loop_box.delete(0, END)
    #     self.ui.loop_box.insert(END, self.logic.instructions.num_loops)
    #     self.ui.pos_label.config(text=f"Position: {self.logic.instructions.cur_pos}/{len(self.logic.instructions.loop)}")
    #     self.ui.loop_label.config(text=f"Loops (現在/回数): {self.logic.instructions.cur_loop + 1}/{self.logic.instructions.num_loops}")
