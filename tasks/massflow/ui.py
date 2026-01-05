import tkinter as tk
from tkinter import ttk


class MassFlowUI(tk.Frame):
    def __init__(self, master, instructions, logic):
        super().__init__(master)
        self.instructions = instructions
        self.logic = logic
        self.handler = None

        self.preset_frame = tk.Frame(master, height=200, width=320, padx=10, pady=10)
        self.control_frame = tk.Frame(master, height=30, width=320, padx=10, pady=10)
        # self.status_frame = tk.Frame(master, height=100, width=200, padx=10, pady=10)

        self.control_frame.grid(row=0, column=0)
        self.preset_frame.grid(row=1, column=0)
        # self.status_frame.grid(row=1, column=1)

        self._create_widgets()

    def _create_widgets(self):
        self.import_button = tk.Button(self.control_frame, text="Import Preset")
        self.import_button.place(x=0, y=0)

        # self.data_listbox = tk.Listbox(self.preset_frame, width=30, height=10, listvariable=self.instructions.flow_list)
        # self.data_listbox.place(x=10, y=50)

        self.data_listbox2 = ttk.Treeview(self.preset_frame, columns=self.instructions.flow_title[0], show="headings", height=8)
        # for title in self.instructions.flow_title[0]:
        #     self.data_listbox2.heading(title, text=title)
        #     self.data_listbox2.column(title, width=36)
        # for row in self.instructions.flow_list:
        #     self.data_listbox2.insert("", tk.END, values=list(row))
        self.data_listbox2.place(x=0, y=0)

        # self.start_button = tk.Button(self.control_frame, text="Start")
        # self.start_button.place(x=10, y=50)

        # self.stop_button = tk.Button(self.control_frame, text="Stop")
        # self.stop_button.place(x=50, y=50)

        # self.flow_rate_label = tk.Label(self.status_frame, text="Flow Rate (L/min):")
        # self.flow_rate_label.place(x=10, y=10)
        
        # self.flow_rate_value = tk.Label(self.status_frame, text="0.0")
        # self.flow_rate_value.place(x=150, y=10)

        # self.status_label = tk.Label(self.status_frame, text="Status:")
        # self.status_label.place(x=10, y=40)

        # self.status_value = tk.Label(self.status_frame, text="Idle")
        # self.status_value.place(x=150, y=40)

    def update_initial_ui(self):
        self.import_button = tk.Button(self.control_frame, text="Import Preset", command=self._import_preset)
        self.import_button.place(x=0, y=0)


    def set_handler(self, handler):
        self.handler = handler
        self.update_initial_ui()
        self.handler.update_listbox(self.data_listbox2)
    
    def _import_preset(self):
        # print(self.handler)
        self.handler.import_preset()
        self.handler.update_listbox(self.data_listbox2)
