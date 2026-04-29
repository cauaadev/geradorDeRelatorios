class Sessao:
    def __init__(self, data: str, horario: str, num_sessoes: int):
        self.data = data
        self.horario = horario
        self.num_sessoes = num_sessoes

    def para_dict(self) -> dict:
        return {
            "data": self.data,
            "horario": self.horario,
            "num_sessoes": self.num_sessoes,
        }
