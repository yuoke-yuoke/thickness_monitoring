import tkinter as tk
from ctypes import *
# from tasks.stage.instructions import StageInstructions
# from tasks.stage.logic import StageLogic
# from tasks.stage.handler import StageHandler
# from tasks.stage.ui import StageUI
from scheduler.scheduler import TaskScheduler
from scheduler.instructions import SchedulerInstructions
from scheduler.logic import SchedulerLogic
from scheduler.handler import SchedulerHandler
from scheduler.ui import SchedulerUI

from tasks.stage.controller import StageController
from tasks.spectrometer.controller import SpecController
from tasks.massflow.controller import MassFlowController

class SchedulerWindow:
    _instance = None  # インスタンスをクラス変数で保持する

    def __init__(self, master, loop):
        if SchedulerWindow._instance is not None:
            # 既にウィンドウが存在していれば、前面に持ってくるだけ
            existing_window = SchedulerWindow._instance
            existing_window.deiconify()
            existing_window.lift()
            return

        self.top = tk.Toplevel(master)
        self.top.title("Scheduler Window")
        self.loop = loop

        usemock_spec = False
        if usemock_spec:
            from tasks.spectrometer.mock_lib import MockTLCCSLib
            self.spec_lib = MockTLCCSLib()
        else:
            from tasks.spectrometer.real_lib import RealTLCCSLib
            self.spec_lib = RealTLCCSLib()
            # self.lib = RealTLCCSLib()
            self.ccs_handle = c_int(0)
            self.lib = cdll.LoadLibrary(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLCCS_64.dll")
            self.lib.tlccs_init(b"USB0::0x1313::0x8089::M00301490::RAW", 1, 1, byref(self.ccs_handle))
            status = c_int(0)
            self.lib.tlccs_getDeviceStatus(self.ccs_handle, byref(status))
            print(status)

        self.massflow_controller = MassFlowController()

        usemock_masflow = False  # Trueならモックライブラリを使う
        if usemock_masflow:  # Trueならモックライブラリを使う
            from tasks.massflow.mock_lib import ul
            from tasks.massflow.mock_lib import DaqDeviceInfo
            from tasks.massflow.mock_lib import InterfaceType
            self.ul = ul()
            self.device_info = DaqDeviceInfo(0)
            self.interface_type = InterfaceType()
        else:
            from mcculw import ul
            from mcculw.device_info import DaqDeviceInfo
            from mcculw.enums import InterfaceType
            # self.ul = ul()
            self.device_info = DaqDeviceInfo(0)
            # self.interface_type = InterfaceType()

        self.stage_controller = StageController()
        self.spec_controller = SpecController()
        self.massflow_controller = MassFlowController()

        self.instructions = SchedulerInstructions(loop)
        self.logic = SchedulerLogic(self.instructions, self.loop, self.stage_controller._instance.logic, self.spec_controller._instance.logic, self.massflow_controller._instance.logic)
        # self.scheduler = TaskScheduler(loop)
        self.ui = SchedulerUI(self.top, self.instructions, self.logic)
        self.handler = SchedulerHandler(self.logic, self.ui)

        # ウィンドウを閉じるときの処理を設定
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

        SchedulerWindow._instance = self.top  # インスタンスを保存

    def on_close(self):
        # ウィンドウを閉じたらインスタンスをNoneに戻す
        SchedulerWindow._instance = None
        self.top.destroy()