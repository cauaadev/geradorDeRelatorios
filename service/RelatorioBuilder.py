from validate.PsicologoValidator import PsicologoValidator
from validate.PacienteValidator import PacienteValidator
from validate.SessaoValidator import SessaoValidator

MESES = {
    "01": "janeiro", "02": "fevereiro", "03": "março", "04": "abril",
    "05": "maio", "06": "junho", "07": "julho", "08": "agosto",
    "09": "setembro", "10": "outubro", "11": "novembro", "12": "dezembro",
}


class RelatorioBuilder:
    def __init__(self, dados: dict):
        self.dados = dados
        self._validar()
        self.psi = dados["psicologo"]
        self.pac = dados["paciente"]
        self.sessoes = dados["sessoes"]

    def _validar(self) -> None:
        PsicologoValidator.validar(self.dados.get("psicologo", {}))
        PacienteValidator.validar(self.dados.get("paciente", {}))
        SessaoValidator.validar(self.dados.get("sessoes", []))

    def _data_extenso(self, ano_fallback: str = "2026") -> str:
        try:
            p = self.sessoes[-1]["data"].split("/")
            cidade = self.psi["cidade"].split("/")[0].strip()
            mes = MESES.get(p[1], p[1])
            ano = p[2] if len(p) > 2 else ano_fallback
            return f"{cidade}, {p[0]} de {mes} de {ano}"
        except Exception:
            return ""

    def _lista_dias(self) -> str:
        return ", ".join(
            f"{s['data']} ({s['num_sessoes']} {'sessao' if s['num_sessoes'] == 1 else 'sessoes'})"
            for s in self.sessoes
        )

    def _linhas_cabecalho(self) -> list:
        return [
            self.psi["nome"].upper(), self.psi["titulo"].upper(),
            self.psi["crp"], self.psi["cpf"], self.psi["telefone"],
            self.psi["endereco"], self.psi["bairro"], self.psi["cidade"], self.psi["cep"],
        ]

    def _texto_relatorio(self) -> str:
        total = sum(s["num_sessoes"] for s in self.sessoes)
        return (
            f"Atendimento de psicoterapia {self.pac['tipo_terapia']} realizado "
            f"({total} sessoes de uma hora cada) nos dias {self._lista_dias()} "
            f"ao paciente {self.pac['nome']}, diagnosticado com "
            f"{self.pac['diagnostico']} ({self.pac['cid']})."
        )

    def construir(self) -> dict:
        ano = self.dados.get("ano", "2026")
        return {
            "psi": self.psi,
            "pac": self.pac,
            "sessoes": self.sessoes,
            "cabecalho": self._linhas_cabecalho(),
            "texto": self._texto_relatorio(),
            "data_extenso": self._data_extenso(ano),
        }
