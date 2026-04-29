from sqlalchemy.orm import Session
from model.Psicologo import Psicologo


class PsicologoRepository:
    def __init__(self, session: Session):
        self._session = session

    def salvar(self, dados: dict) -> Psicologo:
        psicologo = Psicologo(**dados)
        self._session.add(psicologo)
        self._session.commit()
        self._session.refresh(psicologo)
        return psicologo

    def listar(self) -> list[Psicologo]:
        return self._session.query(Psicologo).all()

    def buscar_por_id(self, id: int) -> Psicologo | None:
        return self._session.get(Psicologo, id)

    def deletar(self, id: int) -> bool:
        psicologo = self.buscar_por_id(id)
        if not psicologo:
            return False
        self._session.delete(psicologo)
        self._session.commit()
        return True
