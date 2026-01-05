from tkinter import filedialog
import tkinter as tk
import ctypes
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import os
from common.eventbus import global_eventbus

class SpecHandler:
    def __init__(self, logic, ui):
        self.logic = logic
        self.ui = ui
        self.ui.set_handler(self)
        self.logic = logic
        global_eventbus.subscribe("spec_export", self.export_data_button)

    def set_wavelength(self, wavelength):
        self.logic.set_wavelength(wavelength)

    def get_spectrum(self):
        return self.logic.get_spectrum()
    
    def export_data_button(self):
        spec = self.logic.instructions.spec_array
        for i, s in enumerate(spec):
            if np.any(s[0] != 0):
                name = self.logic.instructions.prefix
                name += str(i)
                self.ExportData(s, name)

    def ExportData(self, int_ndarray, name:str):
        # with文を使った場合、f is NoneならAttributeErrorがraiseされる。例外処理しようとするとプログラムが気持ち悪くなるので、finallyを使うようにした
        # f = filedialog.asksaveasfile(initialdir=".", defaultextension="csv", filetypes=[("Comma-Separated Value", "*.csv"), ("Tab-Separated Value", "*.tsv")])
        # f = filedialog.askdirectory(initialdir=".")
        f = self.logic.instructions.dest_folder_path
        # print(self.data)
        # int_ndarray = self.logic.instructions.spec_array
        if f is not None:
            try:
                # separator = " "
                # if f.name.endswith(".csv"):
                #     separator = ","
                # elif f.name.endswith(".tsv"):
                #     separator = "	"
                # d = np.concatenate([[self.logic.wavelength_array], self.logic.reference_array])
                # print(self.logic.instructions.wavelength_array)
                # print(int_ndarray)
                d = np.concatenate([[self.logic.instructions.wavelength_array], int_ndarray])
                d = d.T
                filename = os.path.join(f, (name + self.logic.instructions.extension))
                self.logic.save_spec(d, filename)
                # filename.close()

                try:
                    di = np.concatenate([[self.logic.instructions.wavelength_array], int_ndarray / self.logic.instructions.reference_array])
                    di = di.T
                    filenamei = os.path.join(f, ("abs_" + name + self.logic.instructions.extension))
                    self.logic.save_spec(di, filenamei)
                    # filenamei.close()
                except:
                    pass
            finally:
                # f.close()
                pass
        else:
            print("Directory not detected")

    def ImportData(self):
        f = filedialog.askopenfile(initialdir=".", filetypes=[("Comma-Separated Value", "*.csv"), ("Tab-Separated Value", "*.tsv")])
        if f is not None:
            try:
                separator = " "
                if f.name.endswith(".csv"):
                    separator = ","
                elif f.name.endswith(".tsv"):
                    separator = "	"
                df = pd.read_csv(f, header=None)
                # print("df[0]", df[0])
                # print("df[0][0]", df[0])
                # df.shape
                # df = df.T
                self.logic.instructions.wavelength_array = df[0]
                i=1
                while i<df.ndim:
                    self.logic.instructions.spec_array[self.logic.instructions.cur_pos][self.logic.instructions.cur_loop] = df[i]
                    self.logic.instructions.time_array[self.logic.instructions.cur_pos][self.logic.instructions.cur_loop] = time.time()
                    i+=1
                    self.logic.instructions.cur_pos += 1
            finally:
                f.close()
            self.ui.update_info()

    def _get_button(self) -> None:
        self.logic.get_wavelength()
        self.logic.get_spec_ave()
        self.ui.update_info()

    def spec_settings(self):
        # self.take_spectra = self.take_spectra.get()
        # if self.take_spectra:
        if self.logic.wavelength_array[0] == 0:
            self.logic.get_wavelength()

        et = int(self.exposure_box.get())
        et = ctypes.c_double(et)
        self.logic.exposuretime = et
        self.logic.set_exposuretime()

        self.logic.spec_ave = int(self.spec_ave_box.get())

        self.logic.create_arrays(pos_num=len(self.data), loop_num=self.loop)

        self.if_ready_spectra = True

    def spec_directory_button(self):
        self.logic.instructions.dest_folder_path = filedialog.askdirectory(initialdir=".")
        self.ui.update_info()

    def spec_directory(self): # 使ってない
        self.f = filedialog.askdirectory(initialdir=".")
        # self.spec_filename_GUI()
        self.pre1 = "Dlimonene"
        self.pre2 = ""
        self.logic.pos_num = len(self.data)
        self.logic.loop_num = int(self.loop)
        self.logic.save_spec_all(daughter_folder=self.f, pre1=self.pre1, pre2=self.pre2)
        self.logic.save_spec(self.time_table, self.f+"/timetable.txt")
    
    def spec_filename_GUI(self): # 使ってないよ
        # 使ってないよ
        gui = tk.Toplevel(self.master)
        gui.title("Set file name")
        gui.geometry("500x120")
        
        frame = tk.Frame(gui)
        folder_label = tk.Label(frame, text="Set folder")
        self.folder_box = tk.Entry(frame, text="")
        #folder_button = tk.Button(frame, text="参照...", command=filedialog.askdirectory(initialdir="."))
        folder_button = tk.Button(frame, text="参照...")

        pre1_label =tk.Label(frame, text="pre1 接頭辞1")
        self.pre1_box = tk.Entry(frame)
        pre2_label = tk.Label(frame, text="pre2 接頭辞2")
        self.pre2_box = tk.Entry(frame)

        filename_label = tk.Label(frame, text="file name is; pre1_pre2_positionindex")

        app_button = tk.Button(frame, text="実行", command=self.apply)

        folder_label.grid(column=0, row=0)
        self.folder_box.grid(column=1, row=0, sticky=tk.EW, padx=5)
        folder_button.grid(column=2, row=0)
        pre1_label.grid(column=0, row=1)
        self.pre1_box.grid(column=1, row=1, sticky=tk.EW)
        pre2_label.grid(column=0, row=2)
        self.pre2_box.grid(column=1, row=2, sticky=tk.EW)
        filename_label.grid(column=0, row=3)
        app_button.grid(column=0, row=4)

        gui.columnconfigure(0, weight=1)
        gui.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        gui.mainloop()

    def apply(self): #使ってない
        self.f = self.folder_box.get()
        self.pre1 = self.pre1_box.get()
        self.pre2 = self.pre2_box.get()

    def show_spectra(self): # spec_result.py を使ってる。これは使ってないよ
        pos = self.selectIndex
        loop = self.loop_index

        plotx = self.logic.wavelength_array
        for pos in range(len(self.data)):
            ploty = self.logic.spec_array[pos][loop]
            plt.plot(plotx, ploty, label=f"pos{pos}")
            plt.title("Current spectra")
            plt.xlabel("Wavelength [nm]")
            plt.ylabel("Intensity [a.u.]")
        
        plt.legend()
        plt.show()

    def get_values_from_gui(self): 
        self.logic.instructions.exposuretime = ctypes.c_double( float( self.ui.exposure_box.get()))
        self.logic.instructions.spec_ave = int( self.ui.spec_ave_box.get())
        # self.logic.instructions.dest_folder_path = self.ui.save_directory_box.get()
        self.logic.instructions.prefix = self.ui.spec_name_box.get()

    def listclick(self, event):
        tree = self.ui.legend_treeview
        index = tree.selection()
        if index:
            for item in index:
                sel_index = tree.get_children().index(item)
                i = tree.item(item)["values"][0]
                j = tree.item(item)["values"][1]
                self.logic.instructions.sel_index = i
                self.ui.SpecRF.bring_to_front(self.logic.instructions.wavelength_array, self.logic.instructions.reference_array, self.logic.instructions.spec_array, i, j)

    def set_as_reference(self): 
        print(self.logic.instructions.cur_pos)
        if self.logic.instructions.cur_pos == 0:
            self.logic.get_wavelength()
            self.logic.get_spec_ave()

        # self.logic.instructions.cur_pos -= 1


        # self.logic.instructions.reference_array = self.logic.instructions.spec_array[self.logic.instructions.cur_pos][self.logic.instructions.cur_loop]
        self.logic.instructions.reference_array = (
        self.logic.instructions.spec_array[self.logic.instructions.sel_index][self.logic.instructions.cur_loop].copy()
        )
        self.logic.instructions.spec_array[self.logic.instructions.sel_index][self.logic.instructions.cur_loop] = np.zeros(self.logic.instructions.point_num)
        # self.logic.instructions.reference_array = spec

        self.logic.instructions.ref_time = (self.logic.instructions.time_array[self.logic.instructions.sel_index][self.logic.instructions.cur_loop]).copy()
        self.logic.instructions.time_array[self.logic.instructions.sel_index][self.logic.instructions.cur_loop] = 0

        self.ui.update_info()

        print("Set as reference successfully")
