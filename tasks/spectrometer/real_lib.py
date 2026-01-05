

# real_lib.py
from ctypes import cdll, c_int, byref

class RealTLCCSLib:
    def __init__(self):
        self.lib = cdll.LoadLibrary(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLCCS_64.dll")
        self.ccs_handle = c_int(0)
        # self.lib.tlccs_init(b"USB0::0x1313::0x8089::M00301490::RAW", 1, 1, byref(ccs_handle))

        self.lib.tlccs_init(b"USB0::0x1313::0x8089::M00301490::RAW", 1, 1, byref(self.ccs_handle))
