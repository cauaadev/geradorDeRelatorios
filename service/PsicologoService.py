from repository.PsicologoRepository import PsicologoRepository


class PsicologoService:
    def __init__(self, session):
        self._repo = PsicologoRepository(session)

    def cadastrar(self, dados: dict) -> dict:
        psicologo = self._repo.salvar(dados)
        return psicologo.para_dict()

    def listar(self) -> list[dict]:
        return [p.para_dict() for p in self._repo.listar()]

    def buscar_por_id(self, id: int) -> dict | None:
        p = self._repo.buscar_por_id(id)
        return p.para_dict() if p else None

    def deletar(self, id: int) -> bool:
        return self._repo.deletar(id)
    
    
    def validarDadosPsi(self, dados: dict) -> None:
        if not dados.get("nome"):
            raise ValueError("Campo 'nome' é obrigatório.")
        elif not isinstance(dados["nome"], str):
            raise ValueError("Campo 'nome' deve ser do tipo string.")
        if not dados.get("crp"):
            raise ValueError("Campo 'crp' é obrigatório.")
        elif not isinstance(dados["crp"], str):
            raise ValueError("Campo 'crp' deve ser do tipo string.")
        if not dados.get("nome_curto"):
            nome_curto = dados["nome"][:20].strip()
            dados["nome_curto"] = nome_curto
        
        
