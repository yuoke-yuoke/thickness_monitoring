from tasks.spectrometer.instructions import SpecInstructions
from tasks.spectrometer.logic import SpecLogic
from tasks.spectrometer.data_process import DataProcess

class SpecController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.instructions = SpecInstructions()
            cls._instance.data_process = DataProcess()
            cls._instance.logic = SpecLogic(cls._instance.instructions, cls._instance.data_process)
            # cls._instance.ui = StageUI()
            # cls._instance.handler = StageHandler(cls._instance.logic)

        return cls._instance