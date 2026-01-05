# mock_mcculw

from types import SimpleNamespace

class ul:
    def __init__(self):
        print("[MockMSF] Mockmcculw initialized")
        self.ccs_handle = 0

    def v_out(self, board_num, channel, ao_range, value):
        print(f"[MockMSF] v_out called with board_num {board_num}, channel {channel}, ao_range {ao_range}, value {value}")
        return 0.0
        
    def ingore_instacal(self):
        print("[MockMSF] ignore_instacal called")
    
    def get_daq_device_inventory(self, interface_type):
        print(f"[MockMSF] get_daq_device_inventory called with interface_type {interface_type}")
        return [SimpleNamespace(product_name="Mock Device", unique_id="12345", product_id=1001)]

    def create_daq_device(self, board_num, device):
        print(f"[MockMSF] create_daq_device called with board_num {board_num}, device {device.product_name}")
        return 0

    def release_daq_device(self, board_num):
        print(f"[MockMSF] release_daq_device called with board_num {board_num}")
        return 0

class DaqDeviceInfo:
    def __init__(self, board_num):
        print(f"[MockMSF] Mock DaqDeviceInfo initialized for board {board_num}")
        self.product_name = "Mock DAQ Device"
        self.unique_id = "MockUniqueID"
        self.supports_analog_output = True

class InterfaceType:
    ANY = 0