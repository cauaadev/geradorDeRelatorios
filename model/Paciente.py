from sqlalchemy import Column, Integer, String
from model.Person import Person

class Paciente(Person):
    __tablename__ = "pacientes"

    tipo_terapia = Column(String(80),  nullable=False)
    diagnostico  = Column(String(200), nullable=False)
    cid          = Column(String(10),  nullable=False)

    def para_dict(self) -> dict:
        return {
            "id":           self.id,
            "nome":         self.nome,
            "tipo_terapia": self.tipo_terapia,
            "diagnostico":  self.diagnostico,
            "cid":          self.cid,
        }
