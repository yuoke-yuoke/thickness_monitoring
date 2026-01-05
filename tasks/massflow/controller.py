# stage controller 
from tasks.massflow.instructions import MassFlowInstructions
from tasks.massflow.logic import MassFlowLogic

from mcculw import ul
from mcculw.device_info import DaqDeviceInfo
from mcculw.enums import InterfaceType

class MassFlowController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.instructions = MassFlowInstructions()
            cls._instance.device_info = DaqDeviceInfo(0)
            cls._instance.logic = MassFlowLogic(cls._instance.instructions, cls._instance.device_info)
            # cls._instance.ui = StageUI()
            # cls._instance.handler = StageHandler(cls._instance.logic)

        return cls._instance
    
