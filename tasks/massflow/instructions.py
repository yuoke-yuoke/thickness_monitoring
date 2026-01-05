import tkinter as tk
import pandas as pd

class MassFlowInstructions:
    def __init__(self):
        self.flow_rate = [0, 0, 0,]
        self.duration = 0
        self.status = "Idle"

        self.flow_title = [["Total ind.", "Ind. length", "N2", "Water", "Odorant"]]
        # self.flow_list = pd.core.frame.DataFrame([["20", "20", "10", "20", "40"], ["30", "10", "0", "20", "50"]])
        self.flow_list = [["20", "20", "10", "20", "40"], ["30", "10", "0", "20", "50"]]

        self.cur_loop = 0
        self.num_loops = 30

        self.V_N2 = 0
        self.V_water = 0
        self.V_VOC = 0

        self.board_num = 0
        self.use_device_detection = False

        self.ao_info = None
        self.ao_range = None
        self.daq_dev_info = None
