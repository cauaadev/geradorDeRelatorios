from sqlalchemy.orm import Session
from model.Paciente import Paciente


class PacienteRepository:
    def __init__(self, session: Session):
        self._session = session

    def salvar(self, dados: dict) -> Paciente:
        paciente = Paciente(**dados)
        self._session.add(paciente)
        self._session.commit()
        self._session.refresh(paciente)
        return paciente

    def listar(self) -> list[Paciente]:
        return self._session.query(Paciente).all()

    def buscar_por_id(self, id: int) -> Paciente | None:
        return self._session.get(Paciente, id)

    def deletar(self, id: int) -> bool:
        paciente = self.buscar_por_id(id)
        if not paciente:
            return False
        self._session.delete(paciente)
        self._session.commit()
        return True
