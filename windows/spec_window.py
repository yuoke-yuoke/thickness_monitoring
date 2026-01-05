import tkinter as tk
from tasks.spectrometer.instructions import SpecInstructions
from tasks.spectrometer.logic import SpecLogic
from tasks.spectrometer.handler import SpecHandler
from tasks.spectrometer.ui import SpecUI
from tasks.spectrometer.data_process import DataProcess
from tasks.spectrometer.controller import SpecController
from ctypes import *

class SpecWindow:
    _instance = None  # インスタンスをクラス変数で保持する

    def __init__(self, master, loop):
        if SpecWindow._instance is not None:
            # 既にウィンドウが存在していれば、前面に持ってくるだけ
            existing_window = SpecWindow._instance
            existing_window.deiconify()
            existing_window.lift()
            return
        self.top = tk.Toplevel(master)
        self.top.title("Spec Window")
        self.loop = loop


        # self.instructions = SpecInstructions()
        # self.data_process = DataProcess()
        self.controller = SpecController()

        usemock_spe = False  # Trueならモックライブラリを使う
        if usemock_spe:
            from tasks.spectrometer.mock_lib import MockTLCCSLib
            self.lib = MockTLCCSLib()
        else:
            pass
            # from tasks.spectrometer.real_lib import RealTLCCSLib
            # self.lib = RealTLCCSLib()
            # self.ccs_handle = c_int(0)
            # self.lib = cdll.LoadLibrary(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLCCS_64.dll")
            # self.lib.tlccs_init(b"USB0::0x1313::0x8089::M00301490::RAW", 1, 1, byref(self.ccs_handle))
            # status = c_int(0)
            # self.lib.tlccs_getDeviceStatus(self.ccs_handle, byref(status))
            # print(status)

        self.ui = SpecUI(self.top, self.controller._instance.instructions, self.controller._instance.logic)
        # self.ui.pack()
        # self.scheduler = TaskScheduler(loop)
        self.handler = SpecHandler(self.controller._instance.logic, self.ui)


        # ここにウィンドウのUIを構築するコードを追加
        label = tk.Label(self.top, text="This is the Spec Window")
        # label.pack(pady=20)

        # ウィンドウを閉じるときの処理を設定
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.top.destroy()