## ui

import tkinter as tk
from tkinter import ttk
from common.eventbus import global_eventbus

class StageUI(tk.Frame):
    def __init__(self, master, instructions):
        super().__init__(master)
        self.handler = None  # Handler will be set later
        self.instructions = instructions

        self.jog_frame = tk.Frame(master, bg='LightBlue1', height=300, width=400, padx=20, pady=20)
        self.data_frame = tk.Frame(master, bg = 'LightYellow',  height=300, width=400, padx=20, pady=20)
        self.jogsp_frame = tk.Frame(master, bg='LightBlue', height=100, width=400, padx=20, pady=10)
        # self.sequence_frame = tk.Frame(master, bg = 'LightYellow2', height=100, width=400, padx=20, pady=10)
        self.status_frame = tk.Frame(master, bg = 'LightYellow2', height=100, width=400, padx=20, pady=10)
        
        self.jog_frame.grid(row=0, column=0)
        self.data_frame.grid(row=0, column=1)
        self.jogsp_frame.grid(row=1, column=0)
        # self.sequence_frame.grid(row=1, column=1)
        self.status_frame.grid(row=1, column=1)

        self._build_ui()

        global_eventbus.subscribe("stage_update_ui", self.update_info)

    def _build_ui(self):
        self.label = tk.Label(self, text="Stage Control")
        self.label.pack()

        self.up_button = tk.Button(self.jog_frame, text="↑\n[w]", font='Arial 15', width=6, height=4)
        # self.up_button.place(x=75, y=0)
        # self.up_button.bind('<ButtonPress-1>', lambda event: self.button_press("up", event))
        # self.up_button.bind('<ButtonRelease-1>', lambda event:self.handler.button_release(event))
        self.down_button = tk.Button(self.jog_frame, text="↓\n[s]", font='Arial 15', width=6, height=4)
        # self.down_button.place(x=75, y=140)
        # self.down_button.bind('<ButtonPress-1>', lambda event:self.button_press("down", event))
        # self.down_button.bind('<ButtonRelease-1>', lambda event:self.handler.button_release(event))
        self.right_button = tk.Button(self.jog_frame, text="→\n[d]", font='Arial 15', width=6, height=4)
        # self.right_button.place(x=150, y=70)
        # self.right_button.bind('<ButtonPress-1>', lambda event:self.button_press("right", event))
        # self.right_button.bind('<ButtonRelease-1>', lambda event:self.handler.button_release(event))
        self.left_button = tk.Button(self.jog_frame, text="←\n[a]", font='Arial 15', width=6, height=4)
        # self.left_button.place(x=0, y=70)
        # self.left_button.bind('<ButtonPress-1>', lambda event:self.button_press("left", event))
        # self.left_button.bind('<ButtonRelease-1>',lambda event: self.handler.button_release(event))

        self.jogamount_scale = tk.Scale(self.jog_frame, variable=self.instructions.jog_amount, from_=1, to=5.99, orient="vertical", length=180, resolution=0.01, showvalue=0)
        self.jogamount_scale.set(3)
        self.jogamount_scale.place(x=320, y=40)
        self.jogamount_scale_text = tk.Label(self.jog_frame, width=5)
        self.jogamount_scale_text.configure(text=int(self.instructions.jog_amount))
        self.jogamount_scale_text.place(x=310, y=230)
        self.jogamount_title = tk.Label(self.jog_frame)
        self.jogamount_title.configure(text="Jog\nstep", width=5)
        self.jogamount_title.place(x=310, y=0)

        self.stagespeed_scale = tk.Scale(self.jog_frame, variable=self.instructions.stage_speed, from_=1, to=5.99, orient="vertical", length=180, resolution=0.01, showvalue=0)
        self.stagespeed_scale.set(3)
        self.stagespeed_scale.place(x=270, y=40)
        self.stagespeed_scale_text = tk.Label(self.jog_frame, width=5)
        self.stagespeed_scale_text.configure(text=int(self.instructions.stage_speed))
        self.stagespeed_scale_text.place(x=260, y=230)
        self.stagespeed_title = tk.Label(self.jog_frame)
        self.stagespeed_title.configure(text="Stage\nspeed", width=5)
        self.stagespeed_title.place(x=260, y=0)

        self.x_goto_label = tk.Label(self.jogsp_frame, text="To x=")
        self.x_goto_label.place(x=0, y=0)
        self.y_goto_label = tk.Label(self.jogsp_frame, text="To y=")
        self.y_goto_label.place(x=0, y=30)
        self.x_goto_box = tk.Entry(self.jogsp_frame, font='Arial 10', width=20)
        self.x_goto_box.place(x=40, y=0)
        self.y_goto_box = tk.Entry(self.jogsp_frame, font='Arial 10', width=20)
        self.y_goto_box.place(x=40, y=30)
        self.goto_button = tk.Button(self.jogsp_frame, text="GO", width=7, height=2)
        self.goto_button.place(x=230, y=0)
        self.home_button = tk.Button(self.jogsp_frame, text="GO\nHOME", width=7, height=2)
        self.home_button.place(x=300, y=40)
        self.estop_button = tk.Button(self.jogsp_frame, text="STOP", bg="red", width=7, height=2)
        self.estop_button.place(x=300, y=0)
        

        self.position_x_label = tk.Label(self.status_frame, text="Current x=")
        self.position_x_label.place(x=0, y=0)
        self.position_x = tk.Label(self.status_frame)
        self.position_x.configure(state="normal", text = self.instructions.current_position_X, font='Arial 10', anchor="w", width=10)
        self.position_x.place(x=70, y=0)
        self.position_y_label = tk.Label(self.status_frame, text="Current y=")
        self.position_y_label.place(x=0, y=30)
        self.position_y = tk.Label(self.status_frame)
        self.position_y.configure(state="normal", text = self.instructions.current_position_Y, font='Arial 10', anchor="w", width=10)
        self.position_y.place(x=70, y=30)
        
        self.status_label_ = tk.Label(self.status_frame, text="Prog. Status")
        self.status_label_.place(x=190, y=0)
        self.status_label = tk.Label(self.status_frame, font='Arial 10', width=10, anchor="w")
        self.status_label.place(x=260, y=0)
        self.stage_status_label_ = tk.Label(self.status_frame, text="Stage Status")
        self.stage_status_label_.place(x=190, y=30)
        self.stage_status_label = tk.Label(self.status_frame, font='Arial 10', width=10, anchor="w")
        self.stage_status_label.place(x=260, y=30)

        self.record_button = tk.Button(self.data_frame, text="Record Position", width=20, height=8)
        self.record_button.place(x=0, y=0)
        # self.data_listbox = tk.Listbox(self.data_frame, width=32, height=12, listvariable=[])
        # self.data_listbox.place(x=160, y=0)
        self.data_listbox2 = ttk.Treeview(self.data_frame, columns=self.instructions.data_title, show="headings", height=8)
        self.data_listbox2.place(x=160, y=0)

        
        self.select_label = tk.Label(self.data_frame, text="Select Data", width=20)
        self.select_label.place(x=0, y=140)
        self.modify_label = tk.Label(self.data_frame, text="Modify Data", width=20)
        self.modify_label.place(x=0, y=200)

        self.prev_button = tk.Button(self.data_frame, text="|◀◀", width=7, height=1)
        self.prev_button.place(x=0, y=165)
        self.next_button = tk.Button(self.data_frame, text="▶▶|", width=7, height=1)
        self.next_button.place(x=60, y=165)
        
        self.delete_button = tk.Button(self.data_frame, text="|X|", width=3, height=1)
        self.delete_button.place(x=0, y=225)
        self.upward_button = tk.Button(self.data_frame, text="↑", width=3, height=1)
        self.upward_button.place(x=35, y=225)
        self.downward_button = tk.Button(self.data_frame, text="↓", width=3, height=1)
        self.downward_button.place(x=70, y=225)

        self.ExIm_label = tk.Label(self.data_frame, text="Export/Import position data", width=30)
        self.ExIm_label.place(x=160, y=200)
        self.export_button = tk.Button(self.data_frame, text="Export", width=10, height=1)
        self.export_button.place(x=160, y=225)
        self.import_button = tk.Button(self.data_frame, text="Import", width=10, height=1)
        self.import_button.place(x=240, y=225)

    def update_initial_ui(self):

        # self.up_button = tk.Button(self.jog_frame, text="↑\n[w]", font='Arial 15', width=6, height=4)
        self.up_button.place(x=75, y=0)
        self.up_button.bind('<ButtonPress-1>', lambda event: self.handler.button_press("up", event))
        self.up_button.bind('<ButtonRelease-1>', lambda event:self.handler.button_release(event))
        # self.down_button = tk.Button(self.jog_frame, text="↓\n[s]", font='Arial 15', width=6, height=4)
        self.down_button.place(x=75, y=140)
        self.down_button.bind('<ButtonPress-1>', lambda event:self.handler.button_press("down", event))
        self.down_button.bind('<ButtonRelease-1>', lambda event:self.handler.button_release(event))
        # self.right_button = tk.Button(self.jog_frame, text="→\n[d]", font='Arial 15', width=6, height=4)
        self.right_button.place(x=150, y=70)
        self.right_button.bind('<ButtonPress-1>', lambda event:self.handler.button_press("right", event))
        self.right_button.bind('<ButtonRelease-1>', lambda event:self.handler.button_release(event))
        # self.left_button = tk.Button(self.jog_frame, text="←\n[a]", font='Arial 15', width=6, height=4)
        self.left_button.place(x=0, y=70)
        self.left_button.bind('<ButtonPress-1>', lambda event:self.handler.button_press("left", event))
        self.left_button.bind('<ButtonRelease-1>',lambda event: self.handler.button_release(event))

        self.jogamount_scale = tk.Scale(self.jog_frame, variable=self.instructions.scaleval_jog, from_=1, to=4.99, orient="vertical", length=180, command=lambda val: self.handler.set_jogamount_value(val), resolution=0.01, showvalue=0)
        self.jogamount_scale.set(3)
        self.jogamount_scale.place(x=320, y=40)
        self.stagespeed_scale = tk.Scale(self.jog_frame, variable=self.instructions.stage_speed, from_=1, to=4.99, orient="vertical", length=180, command=lambda val:self.handler.set_stagespeed_value(val), resolution=0.01, showvalue=0)
        self.stagespeed_scale.place(x=270, y=40)
        self.goto_button = tk.Button(self.jogsp_frame, text="GO", width=7, height=2, command=self.handler._goto)
        self.goto_button.place(x=230, y=0)
        self.home_button = tk.Button(self.jogsp_frame, text="GO\nHOME", width=7, height=2, command=self.handler.Home)
        self.home_button.place(x=300, y=40)
        self.estop_button = tk.Button(self.jogsp_frame, text="STOP", bg="red", width=7, height=2, command=self.handler.custom_stop)
        self.estop_button.place(x=300, y=0)
        self.record_button = tk.Button(self.data_frame, text="Record Position", width=20, height=8, command=self.handler.RecordPositionButton)
        self.record_button.place(x=0, y=0)
        self.prev_button = tk.Button(self.data_frame, text="|◀◀", width=7, height=1, command=self.handler.prev)
        self.prev_button.place(x=0, y=165)
        self.next_button = tk.Button(self.data_frame, text="▶▶|", width=7, height=1, command=self.handler.next)
        self.next_button.place(x=60, y=165)
        self.delete_button = tk.Button(self.data_frame, text="|X|", width=3, height=1, command=self.handler.delete)
        self.delete_button.place(x=0, y=225)
        self.upward_button = tk.Button(self.data_frame, text="↑", width=3, height=1, command=self.handler.up)
        self.upward_button.place(x=35, y=225)
        self.downward_button = tk.Button(self.data_frame, text="↓", width=3, height=1, command=self.handler.down)
        self.downward_button.place(x=70, y=225)
        self.export_button = tk.Button(self.data_frame, text="Export", width=10, height=1, command=self.handler.ExportData)
        self.export_button.place(x=160, y=225)
        self.import_button = tk.Button(self.data_frame, text="Import", width=10, height=1, command=self.handler.ImportData)
        self.import_button.place(x=240, y=225)
        self.data_listbox2.bind('<<TreeviewSelect>>', self.handler.listclick)
        self.data_listbox2.place(x=160, y=0)

    def set_handler(self, handler):
        self.handler = handler
        self.update_initial_ui()
        self.update_listbox(self.data_listbox2)

    def update_info(self, *void): # あくまで情報を書き換えるだけ。情報の取得はほかの関数
        # update status
        self.status_label.configure(text = self.instructions.status)
        self.stage_status_label.configure(text = self.instructions.if_moving)

        self.update_listbox(self.data_listbox2, sel_index=self.instructions.selectIndex)

        self.position_x.configure(text = self.instructions.current_position_X)
        self.position_y.configure(text = self.instructions.current_position_Y)

    def update_listbox(self, tree, sel_index:int =0):
        # self.data_listbox2 = ttk.Treeview(self.preset_frame, columns=self.instructions.flow_title[0], show="headings", height=8)
        for title in self.instructions.data_title:
            tree.heading(title, text=title)
            tree.column(title, width=105, anchor="center")
        try:
            tree.delete(*tree.get_children())
        except:
            pass
        for row in self.instructions.data:
            tree.insert("", tk.END, values=list(row))
        tree.place(x=160, y=0)

        self.highlight_row(tree, sel_index)

    def highlight_row(self, tree, sel_index: int):
        tree.tag_configure("highlight", background="yellow")

        n_rows = len(tree.get_children())
        for i in range(n_rows):
            item = tree.get_children()[i]
            tree.item(item, tags=())

        try:
            # 新しい行をハイライト
            item = tree.get_children()[sel_index]
            tree.item(item, tags=("highlight",))
        except:
            pass






