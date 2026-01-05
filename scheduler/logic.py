import asyncio
import time
import numpy as np
import os
from common.eventbus import global_eventbus

class SchedulerLogic:
    def __init__(self, instructions, loop, stage_logic, spec_logic, massflow_logic):
        self.instructions = instructions
        self.loop = loop
        self.stage_logic = stage_logic
        # self.stage_handler = stage_handler
        self.spec_logic = spec_logic
        self.massflow_logic = massflow_logic
        
        self._scheduler_ui_callback = None
        self._stage_ui_callback = None
        self._massflow_ui_callback = None
        self._spec_ui_callback = None

        print(f"[SchedulerLogic] Initialized with loop: {loop}, stage_logic: {stage_logic}, spec_logic: {spec_logic}, massflow_logic: {massflow_logic}")


    def get_loop_box(self):
        return self.instructions.num_loops

    def get_interval_time(self):
        return self.instructions.interval_time
    
    # async def spec_take_one(self):
    def spec_take_one(self):
        self.spec_logic.instructions.cur_pos = self.instructions.cur_pos
        self.spec_logic.instructions.cur_loop = self.instructions.cur_loop
        print("getting spec...")
        self.spec_logic.get_spec_ave()

    def stage_move(self, position):
        # position = [x, y] str
        # print(position)
        self.stage_logic.instructions.stopped_event.clear()
        self.stage_logic.instructions.if_moving = True
        time.sleep(0.1)
        self.stage_logic.GoTo(position, speed=50000)
        # while self.stage_logic.instructions.if_moving:
        # self.stage_logic.start_polling()
        # time.sleep(3)
        # self.stage_logic.get_current_position()

    async def start(self):
        print("start here")
        if self.instructions.running:
            print("[Scheduler] Already running")
            return
        self.instructions.running = True
        self.instructions._cancel_event = asyncio.Event()  # ←ここで再作成！

        # self.handler.get_variables()
        self.initialize_instructions()
        self.initialize_devices()
        print(self.instructions.interval_time, self.instructions.num_loops)

        for self.instructions.cur_loop in range(self.instructions.num_loops):
            print(f"[Scheduler] Loop {self.instructions.cur_loop + 1}/{self.instructions.num_loops} started")
            self.update_instructions()

            if self.instructions._cancel_event.is_set():
                break

            if self.instructions.gas_on.get():
                # print("[Scheduler] Gas flow started", self.instructions.cur_loop)
                self.massflow_logic.run_flow_loop(self.instructions.cur_loop)

            for self.instructions.cur_pos in range(self.instructions.num_pos):
                # s_time = time.time()
                print(f"[Scheduler] position {self.instructions.cur_pos+1}/{self.instructions.num_pos} ")
                s_time = asyncio.get_event_loop().time()
                self.update_instructions()

                if self.instructions._cancel_event.is_set():
                    break

                if self.instructions.stage_on.get():
                    position = self.stage_logic.instructions.data[self.instructions.cur_pos]
                    self.stage_move(position)
                    print("if moving", self.stage_logic.instructions.if_moving)
                    a = self.stage_logic.wait_until_stopped()
                    print(f"[Scheduler] Stage stoped", a)
                    print("if moving", self.stage_logic.instructions.if_moving)
                if self.instructions.spec_on.get():
                    print(f"[Scheduler] Taking one spectrum")
                    self.spec_take_one()
                    print(f"[Scheduler] Took one spectrum")
                
                self.update_ui_all()
                e_time = asyncio.get_event_loop().time() - s_time

                remaining = max(0, self.instructions.interval_time / 1000 - e_time)
                

                
                print(f"[Scheduler] Waiting {remaining:.2f} seconds before next cycle")
                if self.instructions.cur_loop%10 == 0:
                    # global_eventbus.publish("spec_export")
                    self.export_log()
                await asyncio.sleep(remaining)  # Yield control to the event loop
                

            else: # 多重 for から抜けたりする用
                continue
            break

        global_eventbus.publish("spec_export")
        self.export_log()
        self.stop()


    def stop(self):
        if self.instructions.gas_on.get():
            self.massflow_logic.change_flow_voltage([0, 0, 0,0,0])
        if self.instructions.running:
            print("[Scheduler] Stop requested")
            self.instructions._cancel_event.set()
            self.instructions.running = False
            print("[Scheduler] Stopped")
        else:
            print("[Scheduler] Not running")

    def export_log(self):
        # print("export")
        # f = self.spec_logic.instructions.data_folder_path
        f = r"C:\Users\user\Documents\nishiyama\250721_gas_codes_new\test_results"
        # print("export log", f)
        if f is not None:
            filename = os.path.join(f, "scheduler_log.csv")
            data = self.instructions.scheduler_log
            data = np.array(data)
            # print(data, type(data), data.shape)
            np.savetxt(filename, data, delimiter=",", fmt="%s", encoding="utf-8")
            print("exported")

    def update_ui_all(self):
        # ui だけ更新。中身については別のところに任せる。
        # でもここでhandler使いたくないよなあ
        # self.handler.ui.update_ui()
        global_eventbus.publish("scheduler_update_ui")
        global_eventbus.publish("spec_update_ui")
        # self.massflow_logic._update_ui は動かない。依存関係が微妙だねえ
        # self.massflow_logic._update_ui(cur_pos=self.instructions.cur_pos)

    def initialize_devices(self):
        if self.instructions.gas_on.get():
            self.massflow_logic.veryfy_massflow()
        if self.instructions.stage_on.get():
            self.stage_logic.get_current_position()
            self.stage_logic.stop_polling()
            time.sleep(1)
            self.stage_logic.instructions.stopped_event.clear()
            self.stage_logic.start_polling() # 流しっぱなしにしておく


    def initialize_instructions(self):
        # self.handler.get_variables()

        # self.instructions.num_loops はhandler.get_variables() で取得済
        self.instructions.cur_loop = 0
        self.instructions.cur_pos = 0
        self.instructions.num_pos = len( self.stage_logic.instructions.data)
        # self.instructions.num_loops = int(self.instructions.num_loops)
        if self.instructions.gas_on.get():
            self.instructions.num_loops = max(int(self.instructions.num_loops), int(self.massflow_logic.instructions.flow_list[-1][0]))
        self.instructions.scheduler_log = []
        print(self.instructions.cur_loop, self.instructions.cur_pos, self.instructions.num_pos, self.instructions.num_loops)

        self.spec_logic.instructions.spec_array = np.zeros((self.instructions.num_pos, self.instructions.num_loops, self.spec_logic.instructions.point_num))
        self.spec_logic.instructions.intfere_array = np.zeros((self.instructions.num_pos, self.instructions.num_loops, self.spec_logic.instructions.point_num))

        self.spec_logic.instructions.time_array = np.zeros((self.instructions.num_pos, self.instructions.num_loops))

        self.update_instructions()

    def update_instructions(self):
        # 使う値は
        # cur_loop, cur_pos, num_loops, num_pos
        self.instructions.scheduler_log.append([self.instructions.cur_loop, self.instructions.cur_pos, time.time(), self.stage_logic.instructions.current_position_X, self.stage_logic.instructions.current_position_Y, self.massflow_logic.instructions.V_N2, self.massflow_logic.instructions.V_water, self.massflow_logic.instructions.V_VOC])
        
        self.stage_logic.instructions.cur_loop = self.instructions.cur_loop
        self.stage_logic.instructions.cur_pos = self.instructions.cur_pos
        self.stage_logic.instructions.num_loops = self.instructions.num_loops
        self.stage_logic.instructions.num_pos = self.instructions.num_pos
        self.stage_logic.instructions.selectIndex = self.instructions.cur_pos

        self.spec_logic.instructions.cur_loop = self.instructions.cur_loop
        self.spec_logic.instructions.cur_pos = self.instructions.cur_pos
        self.spec_logic.instructions.loop_num = self.instructions.num_loops
        self.spec_logic.instructions.pos_num = self.instructions.num_pos
        
        self.massflow_logic.instructions.cur_loop = self.instructions.cur_loop
        self.massflow_logic.instructions.num_loops = self.instructions.num_loops
