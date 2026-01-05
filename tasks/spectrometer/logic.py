import os
from ctypes import *
import numpy
import time
from common.eventbus import global_eventbus
# from data_process import DataProcess

#os.chdir(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin")



# lib = cdll.LoadLibrary(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLCCS_64.dll")


ccs_handle=c_int(0)
# self.lib.tlccs_init(b"USB0::0x1313::0x8089::M00301490::RAW", 1, 1, byref(ccs_handle))

# self.data_process = DataProcess()

class SpecLogic:
    def __init__(self, instructions, data_process):
        self.instructions = instructions
        self.data_process = data_process
        self.ccs_handle = ccs_handle
        self.lib = cdll.LoadLibrary(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLCCS_64.dll")
        a = self.lib.tlccs_init(b"USB0::0x1313::0x8089::M00301490::RAW", 1, 1, byref(self.ccs_handle))
        print(a)

        # print(type(self.instructions.exposuretime))
        self.lib.tlccs_setIntegrationTime(self.ccs_handle, self.instructions.exposuretime)
        status = c_int(0)
        self.lib.tlccs_getDeviceStatus(self.ccs_handle, byref(status))
        print(status ,self.ccs_handle)
        # self.lib.tlccs_error_message(ccs_handle, 0)

    def create_arrays(self, pos_num: int, loop_num: int):
        # self.spec_array = numpy.array([[[[0]*self.instructions.point_num]*self.loop_num+1]*self.pos_num], dtype=float)
        self.spec_array = numpy.zeros((pos_num, loop_num, self.instructions.point_num))
        # self.spec_array[position][loop][wavelength] = intensity

    def save_spec(self, data_array: numpy.ndarray, file_path: str) -> None:
        numpy.savetxt(file_path, data_array, delimiter=",")
        print("Saved successfully" , file_path)

    def set_exposuretime(self):
        self.lib.tlccs_setIntegrationTime(ccs_handle, self.instructions.exposuretime)

    def set_file_path(self, daughter_folder: str, pre1: str, pre2: str, posindex: int, loopindex: int) -> str:
        file_name = ""
        if pre1:
            file_name = pre1
        if pre2:
            if file_name:
                file_name = file_name + "_" + pre2
            else:
                file_name = pre2
        # if posindex:
        posindex = str(posindex).zfill(3)
        if file_name:
            file_name = file_name + "_" + posindex
        else:
            file_name = posindex
        if loopindex:
            loopindex = str(loopindex).zfill(3)
            if file_name:
                file_name = file_name + "_" + loopindex
            else:
                file_name = loopindex

        file_name = file_name + self.extension

        file_path = os.path.join(self.dest_folder_path,  file_name)
        if daughter_folder:
            file_path = os.path.join(self.dest_folder_path, daughter_folder, file_name)
        return file_path
    
    def cal_absorption(self, array: numpy.array) -> numpy.ndarray:
        try:
            res = array/self.reference_array
            return res
        except ValueError:
            return "One of the array sizes might be wrong"

    
    # def get_spec_ave(self) -> numpy.ndarray:
    #     res_array = numpy.array([[0]*self.instructions.point_num], dtype=float)
    #     for _ in range(int(self.spec_ave)):
    #         # numpy.concatenate([res_array, numpy.array(self.get_spec_one(), dtype=float)])
    #         res_array = res_array + self.get_spec_one()
    #         # float がオーバーフローしないならこっちがいい
    #         # 時間も測りたい
        
    #     # res = numpy.average(res_array, axis=0)
    #     res = res_array/self.spec_ave

    #     # res = res/self.reference_array
    #     return res
    
    def get_spec_ave(self) -> numpy.ndarray:
        # self.get_status()
        # print("taking")
        res_array = numpy.array([[0]*self.instructions.point_num], dtype=float)
        for _ in range(int(self.instructions.spec_ave)):
            res_array = res_array + self.get_spec_one()
            # print(res_array)
            # 時間も測りたい
        # print("took")
        # self.reference_array = numpy.average(res_array, axis=0)
        res_array = res_array/self.instructions.spec_ave
        print(res_array.shape, res_array[:10])
        self.instructions.spec_array[self.instructions.cur_pos][self.instructions.cur_loop] = res_array[0]
        self.instructions.time_array[self.instructions.cur_pos][self.instructions.cur_loop] = time.time()

        # 毎回計算すると、どこまで計算したかややこしくなる。特に途中でreferenceに移行する可能性があるので。
        # res_array_intfere = res_array/self.instructions.reference_array
        # self.instructions.intfere_array[self.instructions.cur_pos][self.instructions.cur_loop] = res_array_intfere[0]
        # print(res_array_intfere[0][:10])
        # print("hoge")

        self.instructions.sel_index = self.instructions.cur_pos
        self.instructions.cur_pos += 1
        # print("res array ", res_array[0])
        print("[Spectrometer] Got spectrum successfully")

    
    def get_spec_one(self):
        # self.get_status()
        array = (c_double*self.instructions.point_num)()

        a = self.lib.tlccs_startScan(ccs_handle)
        b = self.lib.tlccs_getScanData(ccs_handle, byref(array))
        # print(array.value())
        # print("a", a, "b", b)
        return numpy.array(array, dtype=float)
    
    def get_wavelength(self):
        # self.get_status()

        wavelengths=(c_double*self.instructions.point_num)()
        # print(wavelengths[:10])
        self.lib.tlccs_getWavelengthData(ccs_handle, 0, byref(wavelengths), c_void_p(None), c_void_p(None))
        self.instructions.wavelength_array = numpy.array(wavelengths, dtype=float)
        # print(self.instructions.wavelength_array[:10])
        print("Got wavelengths successfully")


    def get_status(self, status=c_int(0)) -> None:
        while (status.value & 0x0010) == 0:
            status = c_int(0)
            self.lib.tlccs_getDeviceStatus(ccs_handle, byref(status))
            # print(status.value&0x0010)
        return
        # if (status.value & 0x0010):
        #     self.lib.tlccs_getDeviceStatus(ccs_handle, byref(status))
        #     return

    def append_spec(self, loopindex, posindex):
        spec = self.get_spec_ave()
        self.spec_array[posindex][loopindex] = spec

    def save_spec_all(self, daughter_folder="", pre1="", pre2=""):
        self.data_process.wl_range_array(self.wavelength_array)
        start_row = self.data_process.start_row
        end_row = self.data_process.end_row
        print(self.spec_array)
        print(self.wavelength_array)
        print(self.reference_array)

        for pos in range(self.pos_num):
            spec_array_pos = self.spec_array[pos]
            print(spec_array_pos)
            ar = numpy.concatenate([[self.wavelength_array], spec_array_pos])
            ar = ar.T
            ar = ar[start_row:end_row]
            file_path = self.set_file_path(daughter_folder=daughter_folder, pre1=pre1, pre2=pre2, posindex=pos, loopindex=0)

            self.save_spec(ar, file_path)

            if self.reference_array[0]:
                spec_array_pos = spec_array_pos/self.reference_array
                ar_ref = numpy.concatenate([[self.wavelength_array], spec_array_pos])
                ar_ref = ar_ref.T
                ar_ref = ar_ref[start_row:end_row]
                file_path = self.set_file_path(daughter_folder=daughter_folder, pre1=pre1+"_abs", pre2=pre2, posindex=pos, loopindex=0)
                self.save_spec(ar_ref, file_path)

    def get_exposuretime_value(self) -> int:
        return int(self.ui.exposure_box.get())
    
    def get_spec_average_value(self) -> int:
        return int(self.ui.spec_ave_box.get())