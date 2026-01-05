# mock_lib.py
# from ctypes import *
import ctypes
import numpy as np

class MockTLCCSLib:
    def __init__(self):
        print("MockTLCCS initialized")
        self.ccs_handle = 0
        self.point_num = 3648

    def tlccs_setIntegrationTime(self, ccs_handle, exposure_time):
        print(f"[Mock] tlccs_setIntegrationTime called with handle {ccs_handle} and exposure time {exposure_time}")
        return 0
    
    def tlccs_startScan(self, ccs_handle):
        # print(f"[Mock] tlccs_startScan called with handle {ccs_handle}")
        return 0
    
    def tlccs_getScanData(self, ccs_handle, array):
        # print(f"[Mock] tlccs_getScanData called with handle {ccs_handle}")
        data = np.random.rand(self.point_num)  # numpy で乱数生成
        arr = ctypes.cast(array, ctypes.POINTER(ctypes.c_double * self.point_num)).contents
        for i, v in enumerate(data):
            arr[i] = v
        return 0
        # Simulate scan data
    
    def _ensure_array(self, buf):
        """CArgObject でも ctypes 配列でも c_double*point_num に直す"""
        arr_type = ctypes.c_double * self.point_num
        return ctypes.cast(buf, ctypes.POINTER(arr_type)).contents

    def tlccs_getWavelengthData(self, ccs_handle, start_index, wavelengths, arg1, arg2):
        # wavelengths = self._ensure_array(wavelengths)
        arr = ctypes.cast(wavelengths, ctypes.POINTER(ctypes.c_double * self.point_num)).contents

        path = r"C:\Users\hayam\OneDrive - Science Tokyo\lab_research\1_codes\250721_gas_codes_new\wavelength.csv"
        imported = np.genfromtxt(path, delimiter=",", dtype=float)
        for i, v in enumerate(imported):
            arr[i] = v[0]
        # print(f"[Mock] tlccs_getWavelengthData called with handle {ccs_handle}, start_index {start_index}")
        return 0
    
    def tlccs_getDeviceStatus(self, ccs_handle, status):
        print(f"[Mock] tlccs_getDeviceStatus called with handle {ccs_handle}")
        status.value = 0x0010
        return 0
    
