## instructions

### tasks/task_a/instructions.py
import tkinter as tk
import threading
from tasks.stage.handler import Axis
class StageInstructions:
    # _instance = None

    def __init__(self, delay=1.0):
        # if StageInstructions._instance is not None:
        #     return
        self.param = "Default instructions"
        self.delay = delay
        # 他の設定や状態があればここに書く
        self.command_template = lambda value: bytes([0x01, 0x02, value])
        self.command_param = 0x10  # GUIでセットされる値
        
        self.busy = False   # XYステージと通信するための外部プログラム呼び出し中はbusyになる。busyな間、Pythonはフリーズするので、マルチスレッドにする
        self.ser_lock = threading.Lock()
        self.if_moving: bool = False
        self.stopped_event = threading.Event() # ステージが動いているかを確認する
        self.stopped_event.set()
        self._poll_thread = None
        self._stop_event = threading.Event() # ステージを急に止める指令を出す
        
        self.status: str = "Free"
        self.current_position_X = "Not Get"
        self.current_position_Y = "Not Get"
        self.error_nums = 0

        self.data_title = ["X", "Y"]
        self.data = [["0", "0"]]

        self.selectIndex = 0

        self.jog_amount = "1000"
        self.stage_speed = "1000"
        self.scaleval_jog = tk.IntVar(value=3)
        self.scaleval_spd = tk.IntVar(value=3)
        self.ax = Axis(1)
        self.dir = "CW"

        self.waig_time = 10000

