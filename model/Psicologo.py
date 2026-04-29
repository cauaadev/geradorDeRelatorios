from sqlalchemy import Column, Integer, String
from db.database import Base
class Psicologo(Base):
    __tablename__ = "psicologos"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    nome       = Column(String(120), nullable=False)
    titulo     = Column(String(120), nullable=False)
    crp        = Column(String(30),  nullable=False, unique=True)
    cpf        = Column(String(14),  nullable=False, unique=True)
    telefone   = Column(String(20),  nullable=False)
    endereco   = Column(String(200), nullable=False)
    bairro     = Column(String(80),  nullable=False)
    cidade     = Column(String(80),  nullable=False)
    cep        = Column(String(10),  nullable=False)
    nome_curto = Column(String(60),  nullable=False)

    def para_dict(self) -> dict:
        return {
            "id":         self.id,
            "nome":       self.nome,
            "titulo":     self.titulo,
            "crp":        self.crp,
            "cpf":        self.cpf,
            "telefone":   self.telefone,
            "endereco":   self.endereco,
            "bairro":     self.bairro,
            "cidade":     self.cidade,
            "cep":        self.cep,
            "nome_curto": self.nome_curto,
        }
