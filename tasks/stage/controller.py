# stage controller 
from tasks.stage.instructions import StageInstructions
from tasks.stage.logic import StageLogic

class StageController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.instructions = StageInstructions()
            cls._instance.logic = StageLogic(cls._instance.instructions, mock=False)
            # cls._instance.ui = StageUI()
            # cls._instance.handler = StageHandler(cls._instance.logic)

        return cls._instance
    
