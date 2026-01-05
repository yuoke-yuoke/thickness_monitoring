## logic

### tasks/task_a/logic.py
import asyncio
import threading
import serial
import time
from textwrap import wrap
from tasks.stage.handler import Axis, Command
from common.eventbus import global_eventbus

"""
物理的な転送速度 = (バイト数 x 10 bits/bytes) / (ボーレート[bit/s])

今回は最大で (100 bytes x 10 bits/bytes) / (38400 bits/s) ~ 26 ms
writeなら26ms, write and read なら52msかかる。
"""

class StageLogic_test:
    def __init__(self, instructions):
        self.instructions = instructions

    async def run(self):
        value = self.instructions.command_param
        command = self.instructions.command_template(value)

        delay = self.instructions.delay
        print(f"[Logic] Start Task A (wait {delay}s)")
        print(f"[Logic] Sending command (Command: {command})")
        # print(self.instructions.param)
        await asyncio.sleep(delay)
        print("[Logic] End Task A")



class StageLogic:
    MAXCHAR = 100
    def __init__(self, instructions, com_port=7, mock=True): # initially com_port=5
        self.instructions = instructions

        self.com_port = 'COM' + str(com_port)
        self.baud_rate =38400 # initially baud_rate=38400
        self.transfer_rate = 100*10/self.baud_rate * 1.1
        self.mock = mock

        if mock:
            self.ser = None
            print("[StageLogic] Using mock serial port")
        else:
            self.ser = serial.Serial(self.com_port, self.baud_rate, timeout=0.1)
            self.instructions.stopped_event.clear()
            self.start_polling()

    def _serial_write_read(self, write_data):
        if self.mock:
            print(f"[Mock] Writing and Reading to serial: {write_data}")
            time.sleep(0.05)  # Simulate delay
            return b"Mock response"
        else:
            try:
                self.ser.write(write_data)
                self.ser.flush()
                res = self.ser.read_until()
                return res
            except serial.serialutil.SerialTimeoutException:
                print("timeout")
                time.sleep(0.1)
                self._serial_write_read(write_data)

    def _serial_write(self, write_data):
        # not using
        if self.mock:
            print(f"[Mock] Writing to serial: {write_data}")
            asyncio.sleep(self.transfer_rate)
            return b"Mock response"
        else:
            self.ser.write(write_data)
            self.ser.flush()
            # asyncio.sleep(self.transfer_rate)
            print(f"[Stage] Writing to serial: {write_data}")
            # return "Sent: " + write_data

    def _clean(self, output):
        return output.decode('utf-8').split()

    def query(self, axes, attributes):
        query = [(i, j) for i in axes for j in attributes]
        # print(query, "query")
        write = ''.join([m[0].text + ':' + str(m[1].value) + '?' + '\r' for m in query])
        # if len(write) > Stagelogic.MAXCHAR: return query, self._multi_write(write)
        return query, self._clean(self._serial_write_read(write.encode('utf-8')))

    def _multi_write(self, write):
        multiwrite = wrap(write, StageLogic.MAXCHAR, replace_whitespace=False)
        multiwrite = [m + '\r' for m in multiwrite]
        result = []
        for m in multiwrite:
            result.append(self._serial_write_read(( m.split('\n')[0]).encode('utf-8') ))
            # time.sleep(0.2)
        return [item for sublist in [self._clean(r) for r in result] for item in sublist]

    def set(self, axis, attribute, value):  # one axis and attribute at a time
        write = axis.text + ':' + str(attribute.value) + ' ' + str(value) + '\r'
        print('Tx: ', write)
        return self._serial_write_read(write.encode('utf-8'))

    def set_query(self, axes: list, attributes: list, values: list):
        query = [[i, j, k] for i in axes for j in attributes for k in values]
        write = ''.join([m[0].text + ':' + str(m[1].value) + ' ' + str(m[2]) + '\r' for m in query])
        # if len(write) > Stagelogic.MAXCHAR: return query, self._multi_write(write)
        return query, self._clean(self._serial_write_read(write.encode('utf-8')))

    def jog_query(self, axes: list, steps: list, dirs: list, spds: list):
        query = [[axes[i], steps[i], dirs[i], spds[i]] for i in range(len(axes))]
        # print(query, "query")
        write = ''.join(m[0].text + ':L0 100:R0 100:S0 100:F0 ' + str(int(m[3])) + ':PULS ' + str(m[1]) + ':GO ' + str(m[2]) + '\r' for m in query)
        # print(write, len(write))
        # if len(write) > Stagelogic.MAXCHAR: return query, self._multi_write(write)
        return query, self._clean(self._serial_write_read(write.encode('utf-8')))


    def continuous(self, axis: str, spd: int=1000, dir="CW"):
        write = (axis + ":L0 100:R0 100:S0 100:F0 " +  str(int(spd))+ ":GO " + dir + "J" + "\r").encode("utf-8")
        print(write)
        self._serial_write(write)

    def jog(self, axis, data, dir='CW'): # axis, data and dir are originally str type.
        print(axis + ":PULS " + str(int(data)) + \
            ':GO ' + str(dir) + ':DW' )
        writedata = (axis + ":PULS " + str(int(data)) + \
            ':GO ' + str(dir) + ':DW' + '\r').encode('utf-8')
        self._serial_write(writedata)

    def emergency_stop(self):
        writedata = ('STOP 0' + '\r').encode('utf-8')
        self._serial_write(writedata)
        if self.mock:
            time.sleep(0.05)
            self.instructions.if_moving = False

    def slow_stop(self):
        writedata = ('STOP 1' + '\r').encode('utf-8')
        self._serial_write_read(writedata)

    # Parameter query
    def identify(self):
        writedata = ('*IDN?' + '\r').encode('utf-8')
        return self._serial_write_read(writedata)

    def close(self):
        if self.ser.is_open:
            self.ser.close()

    def _verify_home(self, axis):  # (0), 1: (un)detected
        writedata = axis.text + ':HOME?'
        w_data = (writedata + '\r').encode('utf-8')
        return self._serial_write_read(w_data)

    def _verify_all_moving(self):
        writedata = 'MOTIONAll?'
        w_data = (writedata + '\r').encode('utf-8')
        return self._serial_write_read(w_data)

    def check_moving3(self, axlist: list):
        query = self.query(axlist, [Command.SB3])
        time.sleep(0.03)
        print("SB3" , query)

        if len(query) == 0 or all(x is None for x in query):
            self.instructions.if_moving = False
            return

        try:
            if any(int(x) & 0x01 for x in query[1]):
                query = self.query(axlist, [Command.SB1])
                time.sleep(0.03)
                print("SB1", query)

                try:
                    # query = query[1][0]
                    query = query[1]
                    self.instructions.if_moving = True

                    if any(int(x) & 0x40 for x in query):
                        self.instructions.status = "Running"
                    elif any(int(x) & 0x10 for x in query):
                        self.instructions.status = "Org detected"
                    elif any(int(x) & 0x20 for x in query):
                        query = self.query(axlist, [Command.SB2])
                        time.sleep(0.03)
                        try:
                            query = query[1]
                            print("SB2", query)
                            self.instructions.if_moving = False

                            if any(int(x) & 0x30 for x in query):
                                self.instructions.status = "Stage not detected"
                            elif any(int(x) & 0x01 for x in query):
                                self.instructions.status = "CW limit detected"
                            elif any(int(x) & 0x02 for x in query):
                                self.instructions.status = "CCW limit detected"
                            elif any(int(x) & 0x04 for x in query):
                                self.instructions.status = "CW soft limit detected"
                            if any(int(x) & 0x08 for x in query):
                                self.instructions.status = "CCW soft limit detected"
                        except IndexError:
                            pass
                    else:
                        self.instructions.status = "Stop"
                        self.instructions.if_moving = False
                except IndexError:
                    pass

            elif query is None:
                self.instructions.if_moving = False
                self.instructions.status = "Stop"
            else:
                self.instructions.if_moving = False
                self.instructions.status = "Unable to choose Axis"
            self.get_current_position(axlist)
        except ValueError:
            self.instructions.if_moving = False
            self.instructions.status = "Stop"
        except IndexError:
            pass


    def GoTo(self, xy=["0", "0"], speed=10000):
        x, y = xy
        print(f"GOTO ({x}, {y})")
        print(f"current position ({self.instructions.current_position_X}, {self.instructions.current_position_Y})")

        axes = []
        steps = []
        dirs = []
        spds = []

        try:
            print("X", self.instructions.current_position_X)
            dx = int(x)-int(self.instructions.current_position_X)
            if dx:
                axes.append(Axis(2))
                steps.append(str(abs(dx)))
                if dx>0:
                    dirs.append("CW")
                else:
                    dirs.append("CCW")
                spds.append(speed) # self.logic.instructions.stage_speed
        except ValueError:
            pass

        try:
            dy = int(y)-int(self.instructions.current_position_Y)
            if dy:
                axes.append(Axis(1))
                steps.append(str(abs(dy)))
                if dy>0:
                    dirs.append("CW")
                else:
                    dirs.append("CCW")
                spds.append(speed)
        except ValueError:
            pass

        if axes:
            a = self.jog_query(axes, steps, dirs, spds)
            # sleep(2)
            print(a)
        # self.get_current_position()
        # self.ui.update_info()

    def get_current_position(self, axlist: list = [Axis(2), Axis(1)]): # ax = Axis(n) n: int = 1, 2
        query, position = self.query(axlist, [Command.POS])
        print(query, position)
        # axlist の長さによってqueryが変わってくる可能性があって困るなあ。あとで確認しよう
        try:
            for i in range(len(axlist)):
                axis = axlist[i]
                if axis == Axis(2):
                    self.instructions.current_position_X = position[i]
                else:
                    self.instructions.current_position_Y = position[i]
        except IndexError:
            pass
        return query


    def start_polling(self, axlist: list =[Axis(2), Axis(1)]):
        # print("polling started")
        # print("start_polling", self.instructions._poll_thread.is_alive() if self.instructions._poll_thread else None)
        if self.instructions._poll_thread and self.instructions._poll_thread.is_alive():
            # print("polling exists")
            return  # すでにポーリング中
        self.instructions._stop_event.clear()
        self.instructions._poll_thread = threading.Thread(target=self._poll_loop, args=(axlist,), daemon=True)
        self.instructions._poll_thread.start()
        print("after start_polling", self.instructions._poll_thread.is_alive() if self.instructions._poll_thread else None)

    def stop_polling(self):
        self.instructions._stop_event.set()

    # def _poll_loop(self, axlist: list):
    #     print("poll loop in")
    #     try:
    #         while not self.instructions._stop_event.is_set():
    #             # print("not emergent stop")
    #             # print(self.instructions.if_moving, "if_moving")
    #             try:
    #                 if self.instructions.if_moving:
    #                     with self.instructions.ser_lock:
    #                         self.get_stage_status(axlist)
    #                 else:
    #                     if not self.instructions.stopped_event.is_set():
    #                         self.instructions.stopped_event.set()
    #                         with self.instructions.ser_lock:
    #                             self.get_current_position(axlist)
    #             except Exception as e:
    #                 print("poll innner error  ", e)
    #             time.sleep(0.1)
    #     except Exception as e:
    #         print("poll loop crashed  ", e)


    def _poll_loop(self, axlist):
        lock = self.instructions.ser_lock
        while not self.instructions._stop_event.is_set():
            acquired = lock.acquire(blocking=False)
            if acquired:
                try:
                    if self.instructions.if_moving:
                        self.get_stage_status(axlist)
                    else:
                        if not self.instructions.stopped_event.is_set():
                            self.instructions.stopped_event.set()
                            self.get_current_position(axlist)
                finally:
                    lock.release()
            # ロック取れなかった → UI がシリアルを使っている → スキップ
            time.sleep(0.1)

    def get_stage_status(self, axlist: list = [Axis(2), Axis(1)]):
        self.check_moving3(axlist)
        # print(self.instructions.if_moving, "moving")
        # global_eventbus.publish("stage_update_ui")

    def wait_until_stopped(self, timeout=None):
        finished = self.instructions.stopped_event.wait(timeout=timeout)
        if not finished:
            # ステージ停止待ちがタイムアウト
            return False
        return True