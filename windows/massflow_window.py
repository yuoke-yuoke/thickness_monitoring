import tkinter as tk
from tasks.massflow.instructions import MassFlowInstructions
from tasks.massflow.logic import MassFlowLogic
from tasks.massflow.handler import MassFlowHandler
from tasks.massflow.ui import MassFlowUI
from tasks.massflow.controller import MassFlowController

class MassFlowWindow:
    _instance = None  # Class variable to hold the instance

    def __init__(self, master, loop):
        if MassFlowWindow._instance is not None:
            # If an instance already exists, bring it to the front
            existing_window = MassFlowWindow._instance
            existing_window.deiconify()
            existing_window.lift()
            return
        
        self.top = tk.Toplevel(master)
        self.top.title("Mass Flow Window")
        self.loop = loop

        self.controller = MassFlowController()
        # self.instructions = MassFlowInstructions()

        usemock_masflow = False  # Trueならモックライブラリを使う
        if usemock_masflow:  # Trueならモックライブラリを使う
            from tasks.massflow.mock_lib import ul
            from tasks.massflow.mock_lib import DaqDeviceInfo
            from tasks.massflow.mock_lib import InterfaceType
            self.ul = ul()
            self.device_info = DaqDeviceInfo(0)
            # self.interface_type = InterfaceType()
        else:
            from mcculw import ul
            from mcculw.device_info import DaqDeviceInfo
            from mcculw.enums import InterfaceType
            # self.ul = ul()
            self.device_info = DaqDeviceInfo(0)
            # self.interface_type = InterfaceType()

        # self.logic = MassFlowLogic(self.instructions, self.device_info)
        self.ui = MassFlowUI(self.top, self.controller._instance.instructions, self.controller._instance.logic)
        self.handler = MassFlowHandler(self.controller._instance.logic, self.ui)

        # Store the instance for future reference
        MassFlowWindow._instance = self.top

        # Set up the window close protocol
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        MassFlowWindow._instance = None
        self.top.destroy()