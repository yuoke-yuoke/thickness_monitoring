from tasks.massflow.console_examples_util import config_first_detected_device
from mcculw import ul
from mcculw.device_info import DaqDeviceInfo
from mcculw.enums import InterfaceType
from mcculw.enums import FunctionType
from common.eventbus import global_eventbus

# usemock = True  # Set to True to use mock for testing, False to use actual MCCULW library
# if usemock:
#     from tasks.massflow.mock_lib import ul
#     from tasks.massflow.mock_lib import DaqDeviceInfo
# else:
#     from mcculw import ul
#     from mcculw.device_info import DaqDeviceInfo

class MassFlowLogic:
    def __init__(self, instructions, device_info):
        self.instructions = instructions
        self.ul = ul
        self.device_info = device_info
        self.dev_id_list = []

        self.board_num = None
        self.use_device_detection = False
        self.ao_info = None
        self.ao_range = None
        self.daq_dev_info = None
        # self.interface_type = interface_type

    def veryfy_massflow(self):
        self.board_num = 0
        self.use_device_detection = True

        try:
            if self.instructions.use_device_detection:
                config_first_detected_device(self.board_num, self.dev_id_list)

            self.daq_dev_info = DaqDeviceInfo(self.board_num)
            if not self.daq_dev_info.supports_analog_output:
                raise Exception('Error: The DAQ device does not support analog output')

            print('\nActive DAQ device: ', self.daq_dev_info.product_name, ' (',
                self.daq_dev_info.unique_id, ')\n', sep='')

            self.ao_info = self.daq_dev_info.get_ao_info()
            self.ao_range = self.ao_info.supported_ranges[0]
            print("ao_range",self.ao_range)
            print("ao_info", self.ao_info)

            # input("\n✅ Hit Enter to start gas output\n")
        except Exception as e:
            print("Error:", e)
        # finally:
        #     if use_device_detection:
        #         ul.release_daq_device(board_num)


    def run_flow_loop(self, cur_loop):
        for j in range(len(self.instructions.flow_list)):
            if int(self.instructions.flow_list[j][0]) < cur_loop:
                continue  # Skip if the loop number is less than current loop
            else:
                # row = df_excel.iloc[i]
                row = self.instructions.flow_list[j]
                print(f"\nStep {j+1}:")
                self.change_flow_voltage(row)

                break  # Exit after the first matching loop

    def change_flow_voltage(self, row):
        # row = [total_ind, hold_ind, self.instructions.V_N2, self.instructions.V_water, self.instructions.V_VOC]
        self.instructions.V_N2 = float( row[2])
        self.instructions.V_water = float(row[3])
        self.instructions.V_VOC = float(row[4])
        hold_time = row[1]
        # self.check_status()

        print(f"N2 = {self.instructions.V_N2} V, Water = {self.instructions.V_water} V, VOC = {self.instructions.V_VOC} V")
        # print(f"Hold time = {hold_time} sec")

        # print(self.ao_range)
        ul.v_out(self.board_num, 0, self.ao_range, self.instructions.V_N2)
        ul.v_out(self.board_num, 1, self.ao_range, self.instructions.V_water)
        ul.v_out(self.board_num, 2, self.ao_range, self.instructions.V_VOC)
        print("changed voldatage")

    def check_status(self):
        print(ul.get_status(self.board_num, FunctionType(2)))
        # 1: 応答なし
        # 2: StatusResult(status=<Status.IDLE: 0>, cur_count=0, cur_index=0)
        # 3: 応答なし
        # 4: 応答なし
        # 5: 応答なし
        # 6: 応答なし
        # 7: 応答なし

    def _update_ui(self, cur_index=0):
        # 使えません！
        # なぜならinstructions.ui は無いので。
        if self.instructions.ui:
            self.instructions.ui.handler.update_listbox(self.instructions.ui.data_listbox2, cur_index=cur_index)
