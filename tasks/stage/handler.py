## handler

import asyncio
import threading
from time import sleep
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import pandas as pd

from enum import Enum
from enum import IntEnum
from aenum import AutoNumberEnum
class Axis(AutoNumberEnum):
    _init_ = 'value text'
    YAxis =  1, 'AXI1'
    XAxis= 2, 'AXI2'

class Units(IntEnum):
    PULSE = 0
    UM = 1
    MM = 2
    DEG = 3
    MRAD = 4

class Command(Enum):
    IDN = '*IDN' # ?
    SPD = 'SELSP' # select speed
    POS = 'POS' # position
    UNT = 'UNIT' # ?
    GOA = 'GOABS' # go absolute position
    DRD = 'DRDIV' # ?
    RES = 'RESOLUT' # ?
    JOG = 'PULS' # +_ in position
    STOP = 'STOP 0'
    ESTOP = 'STOP 1' # emergency stop
    HOME = 'HOME' # home
    MOVING = 'MOTIONAll' # motion all ?
    SB1 = 'SB1' # 動作中かなど
    SB2 = 'SB2' # ステージの限界などを検出
    SB3 = 'SB3' # 0x01 で正常

class StageHandler:
    def __init__(self, logic, ui, scheduler, loop = None):
        self.logic = logic
        self.ui = ui
        self.ui.set_handler(self)
        self.scheduler = scheduler
        self.loop = loop

    def run(self):
        asyncio.run_coroutine_threadsafe(self.logic.run(), self.loop)

    def schedule(self):
        asyncio.run_coroutine_threadsafe(self.scheduler.start(), self.loop)

    def stop(self):
        asyncio.run_coroutine_threadsafe(self.scheduler.stop(), self.loop)

    def set_delay(self, delay):
        self.logic.instructions.delay = delay

    def set_param(self, value):
        self.logic.instructions.command_param = value

    def set_jogamount_value(self, val):
        self.jog_amount = (10**float(val))
        self.ui.jogamount_scale_text.configure(text=str(int(10**float(val))))

    def custom_stop(self):
        self.logic.emergency_stop()
        self.logic.get_stage_status([Axis(2), Axis(1)])
        # if int(self.logic._verify_all_moving().strip().decode("utf-8")) != 0:
        #     self.logic.slow_stop()
        self.logic.start_polling()
        self.ui.update_info()
    
    def ExportData(self, dtype="pos"):
        # with文を使った場合、f is NoneならAttributeErrorがraiseされる。例外処理しようとするとプログラムが気持ち悪くなるので、finallyを使うようにした
        f = filedialog.asksaveasfile(initialdir=".", defaultextension="csv", filetypes=[("Comma-Separated Value", "*.csv"), ("Tab-Separated Value", "*.tsv")])
        print(self.logic.instructions.data)
        if f is not None:
            try:
                separator = " "
                if f.name.endswith(".csv"):
                    separator = ","
                elif f.name.endswith(".tsv"):
                    separator = "	"
                for datum in self.logic.instructions.data:
                    print(separator.join(datum), file=f)
            finally:
                f.close()

    def ImportData(self, dtype="pos"):
        # f = filedialog.askopenfile(initialdir=".", filetypes=[("Comma-Separated Value", "*.csv"), ("Tab-Separated Value", "*.tsv")], mode="r")
        file_path = filedialog.askopenfilename(
            initialdir=".", filetypes=[("Comma-Separated Value", "*.csv"), ("Tab-Separated Value", "*.tsv")])
        if file_path:
            separator = " "
            if file_path.endswith(".csv"):
                separator = ","
            elif file_path.name.endswith(".tsv"):
                separator = "	"
            try:
                with open(file_path, mode="r", encoding="utf-8") as f:
                    self.logic.instructions.data = [list(line.rstrip("\r\n").split(separator)) for line in f]
                self.currentIndex = 0
                self.logic.instructions.selectIndex = 0
            finally:
                f.close()
            self.ui.update_info()

    def RecordPositionButton(self):
        if self.logic.instructions.busy:
            self.play_button.after(100, self.RecordPositionButton)
            return
        self.ref()
        self.InsertData()
        self.ui.update_info()

    def InsertData(self):
        datum = [self.logic.instructions.current_position_X, self.logic.instructions.current_position_Y]
        self.logic.instructions.selectIndex += 1
        self.currentIndex = self.logic.instructions.selectIndex - 1
        self.logic.instructions.data.insert(self.logic.instructions.selectIndex, datum)
        # (self.logic.instructions.current_position_X, self.logic.instructions.current_position_Y) = datum
        self.logic.instructions.status = "Free"

    def Stop(self): # 使ってない
        self.play_status = False
        if not self.logic.instructions.busy:
            self.logic.instructions.status = "Free"
            # self.logic.set_query([Axis(2), Axis(1)], [Command.SPD], [self.logic.instructions.stage_speed])
            self.ui.update_info()

    def indexIncrement(self, *void):
        self.currentIndex = self.logic.instructions.selectIndex
        self.logic.instructions.selectIndex += 1
        self.ui.update_info()

    def statusFree(self):
        self.logic.instructions.status = "Free"

    def Home(self):
        if self.logic.instructions.busy:
            self.play_button.after(100, self.Home)
            return
        else:
            self.play_status = False
            # self.logic.set(Axis(1), Command.GOA, "0")
            # self.logic.set(Axis(2), Command.GOA, "0")
            # self.logic.set_query([Axis(2), Axis(1)], [Command.GOA, Command.GOA], ["0", "0"])
            self.logic.GoTo(xy = ["0", "0"])
            # self.logic.get_current_position()
            # self.ui.update_info()
            self.logic.instructions.stopped_event.clear()
            # self.logic.start_polling()
            self.currentIndex = None

    def _goto(self, *void):
        self.logic.GoTo(xy = [self.ui.x_goto_box.get(), self.ui.y_goto_box.get()], speed=self.logic.instructions.stage_speed)
        print("goto started")
        self.logic.instructions.if_moving = True
        self.logic.instructions.stopped_event.clear()
        print("waiting til stop")
        self.logic.wait_until_stopped()
        print("stopped")
        # self.logic.start_polling()
        # self.logic.get_current_position()
        self.ui.update_info()

    def pause_while_moving(self): # 使ってない
        
        self.check_moving()
        while self.logic.instructions.if_moving != False:
            sleep(0.5)
            self.check_moving()
            if self.error_nums > 10:
                print("BREAK HERE DUE TO STAGE ERROR")
                return 1
        return 0

    def ref(self): # get coordinate from xystage_program
        self.logic.instructions.busy = True
        self.logic.instructions.status = "Busy"
        self.ui.update_info()

        _ = self.logic.get_current_position()
        print("current position: " + str(self.logic.instructions.current_position_X) + ", " + str(self.logic.instructions.current_position_Y))
        
        self.logic.instructions.busy = False
        self.logic.instructions.status = "Sleep"

        # return [self.logic.instructions.current_position_X[0], self.logic.instructions.current_position_Y[0]]

    def next(self):
        if self.logic.instructions.selectIndex < len(self.logic.instructions.data)-1:
            self.logic.instructions.selectIndex += 1
            self.ui.update_info()

    def prev(self):
        if self.logic.instructions.selectIndex > 0:
            self.logic.instructions.selectIndex -= 1
            self.ui.update_info()

    def delete(self):
        print(self.logic.instructions.selectIndex, len(self.logic.instructions.data))
        if self.logic.instructions.selectIndex < len(self.logic.instructions.data)+1:
            self.logic.instructions.data.pop(self.logic.instructions.selectIndex)
            self.logic.instructions.selectIndex = min(self.logic.instructions.selectIndex, len(self.logic.instructions.data)-1)
            self.ui.update_info()

    def up(self):
        if 0 < self.logic.instructions.selectIndex < len(self.logic.instructions.data):
            self.logic.instructions.data[self.logic.instructions.selectIndex], self.logic.instructions.data[self.logic.instructions.selectIndex-1] = self.logic.instructions.data[self.logic.instructions.selectIndex-1], self.logic.instructions.data[self.logic.instructions.selectIndex]
            self.logic.instructions.selectIndex -= 1
            self.ui.update_info()

    def down(self):
        if self.logic.instructions.selectIndex < len(self.logic.instructions.data) - 1:
            self.logic.instructions.data[self.logic.instructions.selectIndex], self.logic.instructions.data[self.logic.instructions.selectIndex+1] = self.logic.instructions.data[self.logic.instructions.selectIndex+1], self.logic.instructions.data[self.logic.instructions.selectIndex]
            self.logic.instructions.selectIndex += 1
            self.ui.update_info()

    def axis_dir(self, jog_button):
        if jog_button == "up":
            self.logic.instructions.dir = "CCW"
            self.logic.instructions.ax = Axis(1)
        if jog_button == "down":
            self.logic.instructions.dir = "CW"
            self.logic.instructions.ax = Axis(1)
        if jog_button == "right":
            self.logic.instructions.dir = "CW"
            self.logic.instructions.ax = Axis(2)
        if jog_button == "left":
            self.logic.instructions.dir = "CCW"
            self.logic.instructions.ax = Axis(2)

    def button_press(self, jog_button, event):
        print("direction button pressed")
        self.jog(jog_button)
    
    def button_release(self, event):
        print("direction button released")
        self.logic.stop_polling()
        self.logic.emergency_stop()
        ax = self.logic.instructions.ax
        self.logic.get_stage_status([ax])
        self.ui.update_info()
        self.logic.start_polling()

    def listclick(self, event):
        tree = self.ui.data_listbox2
        index = tree.selection()
        if index:
            for item in index:
                # print(tree.get_children().index(item))
                # data_i が選択された行のindex
                data_i = tree.get_children().index(item)
                self.ui.x_goto_box.delete(0, tk.END)
                self.ui.y_goto_box.delete(0, tk.END)
                self.ui.x_goto_box.insert(0, self.logic.instructions.data[data_i][0])
                self.ui.y_goto_box.insert(0, self.logic.instructions.data[data_i][1])
                print(data_i, item)
            
    def jog(self, jog_button):
        self.axis_dir(jog_button)
        ax: Axis = self.logic.instructions.ax
        if self.logic.instructions.if_moving == False:
            self.logic.instructions.if_moving = True
            self.logic.instructions.stopped_event.clear()
        # self.logic.start_polling()
        self.logic.continuous(ax.text, int(self.logic.instructions.stage_speed), self.logic.instructions.dir)
        

    def set_jogamount_value(self, val):
        self.logic.instructions.jog_amount = int(10**float(val))
        self.ui.jogamount_scale_text.configure(text=str(self.logic.instructions.jog_amount))


    def set_stagespeed_value(self, val):
        self.logic.instructions.stage_speed = int(10**float(val))
        self.ui.stagespeed_scale_text.configure(text=str(self.logic.instructions.stage_speed))


    def apply(self):
        self.f = self.folder_box.get()
        self.pre1 = self.pre1_box.get()
        self.pre2 = self.pre2_box.get()

