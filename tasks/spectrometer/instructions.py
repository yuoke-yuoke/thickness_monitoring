import tkinter as tk
from ctypes import *
import numpy as np
import time

class SpecInstructions:
    def __init__(self):
        self.if_ready_spectra: bool = False
        # self.take_spectra = tk.IntVar()
        # self.take_spectra.set(1)

        self.spec_ave: int = 10
        self.exposuretime: c_double = c_double( 1e-2) # [s]
        # self.lib.tlccs_setIntegrationTime(ccs_handle, self.exposuretime)

        self.pos_num: int = 30
        self.loop_num: int = 1
        self.point_num: int = 3648
        
        self.cur_pos: int = 0 # 連続稼働以外の時も利用する
        self.cur_loop: int = 0 # 連続稼働しないときは0

        self.sel_index: int = 0
        
        self.dest_folder_path: str = r"C:\Users\user\Documents\nishiyama\250721_gas_codes_new\test_results"
        self.extension: str = ".csv"
        self.prefix: str = "limonene_"

        self.wavelength_array: np.ndarray = np.array([0]*self.point_num)
        self.reference_array: np.ndarray = np.array([0]*self.point_num)
        self.spec_array = np.zeros((self.pos_num, self.loop_num, self.point_num))
        self.intfere_array = np.zeros((self.pos_num, self.loop_num, self.point_num))

        self.time_array: np.ndarray = np.zeros((self.pos_num, self.loop_num))
        self.ref_time:float = 0
        self.legend_title = ["Pos.", "Loop", "Time"]

        self.spec_array[0][0] = np.array([0.3]*self.point_num)
        # self.time_array[0][0] = time.time()