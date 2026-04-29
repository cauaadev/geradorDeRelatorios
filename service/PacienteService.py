from repository.PacienteRepository import PacienteRepository


class PacienteService:
    def __init__(self, session):
        self._repo = PacienteRepository(session)

    def cadastrar(self, dados: dict) -> dict:
        paciente = self._repo.salvar(dados)
        return paciente.para_dict()

    def listar(self) -> list[dict]:
        return [p.para_dict() for p in self._repo.listar()]

    def buscar_por_id(self, id: int) -> dict | None:
        p = self._repo.buscar_por_id(id)
        if not p: 
            raise ValueError(f"Paciente com id {id} não encontrado.") 
        else:
            return p.para_dict()

    def deletar(self, id: int) -> bool:
        return self._repo.deletar(id)
