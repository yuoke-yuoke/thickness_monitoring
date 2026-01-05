import tkinter as tk
from common.eventbus import global_eventbus

class SchedulerUI(tk.Frame):
    def __init__(self, master, instructions, logic):
        super().__init__(master)
        # self.parent = parent
        self.instructions = instructions
        self.logic = logic
        # self.scheduler = scheduler

        self.play_frame = tk.Frame(master, height=100, width=100, padx=10, pady=10)
        self.input_box_frame = tk.Frame(master, height=100, width=200, padx=10, pady=10)
        self.enable_frame = tk.Frame(master, height=100, width=150, padx=10, pady=10)

        self.play_frame.grid(row=0, column=0)
        self.input_box_frame.grid(row=0, column=1)
        self.enable_frame.grid(row=0, column=2)

        self._create_widgets()

        global_eventbus.subscribe("scheduler_update_ui", self.update_ui)

    def _create_widgets(self):
        self.move_label = tk.Label(self.play_frame, text="Move Sequentially")
        self.move_label.place(x=0, y=0)
        self.play_button = tk.Button(self.play_frame, text="▶", width=4, height=2, bg="red", fg="white")
        self.play_button.place(x=0, y=25)
        self.stop_button = tk.Button(self.play_frame, text="||", width=4, height=2, bg="grey", fg="white")
        self.stop_button.place(x=50, y=25)

        # self.loop_0_label = tk.Label(self.input_box_frame, text="Set Current Index = Zero")
        # self.loop_0_label.place(x=0,y=50)
        # self.loop_0_button = tk.Button(self.input_box_frame, text="0", width=3, height=1)
        # self.loop_0_button.place(x=150, y=50)

        self.interval_label = tk.Label(self.input_box_frame, text="Interval(ms): ")
        self.interval_label.place(x=0, y=0)
        self.interval_box = tk.Entry(self.input_box_frame, width=6)
        self.interval_box.place(x=150, y=0)
        self.pos_label = tk.Label(self.input_box_frame ,text="現在: ")
        self.pos_label.place(x=0, y=50)
        self.loop_label = tk.Label(self.input_box_frame, text="Loops (現在/回数): None/")
        self.loop_label.place(x=0, y=25)
        self.loop_box = tk.Entry(self.input_box_frame, width=6)
        self.loop_box.place(x=150, y=25)

        self.enable_label = tk.Label(self.enable_frame, text="Enable Devices")
        self.enable_label.place(x=0, y=0)
        # self.stage_enable_chebox = tk.Checkbutton(self.enable_frame, text="Stage", variable=self.instructions.stage_on)
        # self.stage_enable_chebox.place(x=0, y=20)
        # self.spec_enable_chebox = tk.Checkbutton(self.enable_frame, text="Spectrometer", variable=self.instructions.spec_on)
        # self.spec_enable_chebox.place(x=0, y=40)
        # self.gas_enable_chebox = tk.Checkbutton(self.enable_frame, text="MassFlowController", variable=self.instructions.gas_on)
        # self.gas_enable_chebox.place(x=0, y=60)
        

    def update_initial_ui(self):
        self.play_button = tk.Button(self.play_frame, text="▶", width=4, height=2, bg="red", fg="white", command=self.handler.play)
        self.play_button.place(x=0, y=25)
        self.stop_button = tk.Button(self.play_frame, text="||", width=4, height=2, bg="grey", fg="white", command=self.handler.stop)
        self.stop_button.place(x=50, y=25)
        # self.loop_0_button = tk.Button(self.play_frame, text="0", width=3, height=1, command=self.handler.loop_initialize)
        # self.loop_0_button.place(x=150, y=50)
        # self.data_listbox.bind('<<ListboxSelect>>', self.handler.listclick)
        self.interval_box.insert(tk.END, self.instructions.interval_time)
        self.interval_box.place(x=150, y=0)
        self.loop_box.insert(tk.END, self.instructions.num_loops)
        self.loop_box.place(x=150, y=25)

        self.stage_enable_chebox = tk.Checkbutton(self.enable_frame, text="Stage", variable=self.instructions.stage_on)
        self.stage_enable_chebox.place(x=0, y=20)
        self.spec_enable_chebox = tk.Checkbutton(self.enable_frame, text="Spectrometer", variable=self.instructions.spec_on)
        self.spec_enable_chebox.place(x=0, y=40)
        self.gas_enable_chebox = tk.Checkbutton(self.enable_frame, text="MassFlowController", variable=self.instructions.gas_on)
        self.gas_enable_chebox.place(x=0, y=60)

    def set_handler(self, handler):
        self.handler = handler
        self.update_initial_ui()

    def update_ui(self):
        self.interval_box.delete(0, tk.END)
        self.interval_box.insert(tk.END, self.logic.instructions.interval_time)
        self.loop_box.delete(0, tk.END)
        self.loop_box.insert(tk.END, self.logic.instructions.num_loops)
        self.pos_label.config(text=f"Position: {self.logic.instructions.cur_pos+1}/{self.logic.instructions.num_pos}")
        self.pos_label.place(x=0, y=50)
        self.loop_label.config(text=f"Loops (現在/回数): {self.logic.instructions.cur_loop + 1}/{self.logic.instructions.num_loops}")
        self.loop_label.place(x=0, y=25)
