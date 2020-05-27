import interpretador
import orquestrador


class diana(interpretador.Interpretador, orquestrador.Orquestrador):
    def __init__(self):
        super().__init__()

    def getRun(self):
        print("Run")