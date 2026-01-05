import tkinter as tk
from tasks.stage.instructions import StageInstructions
from tasks.stage.logic import StageLogic
from tasks.stage.handler import StageHandler
from tasks.stage.ui import StageUI
from scheduler.scheduler import TaskScheduler
from tasks.stage.controller import StageController

class StageWindow:
    _instance = None  # インスタンスをクラス変数で保持する

    def __init__(self, master, loop):
        if StageWindow._instance is not None:
            # 既にウィンドウが存在していれば、前面に持ってくるだけ
            existing_window = StageWindow._instance
            existing_window.deiconify()
            existing_window.lift()
            return

        self.top = tk.Toplevel(master)
        self.top.title("Stage Window")
        self.loop = loop

        self.controller = StageController() # instructions, logic
        self.ui = StageUI(self.top, self.controller._instance.instructions)
        self.scheduler = TaskScheduler(loop)
        self.handler = StageHandler(self.controller._instance.logic, self.ui, self.scheduler)

        # ウィンドウを閉じるときの処理を設定
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

        StageWindow._instance = self.top  # インスタンスを保存

    def on_close(self):
        # ウィンドウを閉じたらインスタンスをNoneに戻す
        StageWindow._instance = None
        self.top.destroy()
        # self.controller._instance.logic.ser.close()