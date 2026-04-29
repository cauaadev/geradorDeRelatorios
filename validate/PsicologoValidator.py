import re


CAMPOS_PSICOLOGO = ["nome", "titulo", "crp", "cpf", "telefone",
                    "endereco", "bairro", "cidade", "cep", "nome_curto"]

CAMPOS_TEXTO_PURO = {
    "psicologo": ["nome", "titulo", "bairro", "cidade", "nome_curto"],
}

_RE_TELEFONE = re.compile(r"^\(\d{2}\) \d{5}-\d{4}$")
_RE_TEM_NUM = re.compile(r"\d")


class PsicologoValidator:
    @staticmethod
    def _validar_texto_puro(valor: str, campo: str) -> None:
        if valor.strip().isdigit():
            raise ValueError(
                f"psicologo.{campo}: esperado texto, mas recebeu apenas números: '{valor}'"
            )

    @staticmethod
    def _validar_tamanho_minimo(valor: str, campo: str, minimo: int) -> None:
        if len(valor.strip()) < minimo:
            raise ValueError(
                f"psicologo.{campo}: muito curto '{valor}'. Mínimo {minimo} caracteres."
            )

    @staticmethod
    def _validar_campos_especificos(campo: str, valor: str) -> None:
        if campo == "telefone" and not _RE_TELEFONE.match(valor):
            raise ValueError(
                f"psicologo.telefone: formato inválido '{valor}'. Esperado (DD) DDDDD-DDDD."
            )
        if campo == "crp" and not _RE_TEM_NUM.search(valor):
            raise ValueError(
                f"psicologo.crp: deve conter ao menos um número, recebeu '{valor}'."
            )
        if campo in ("endereco", "nome_curto", "titulo") and not isinstance(valor, str):
            raise ValueError(f"psicologo.{campo}: esperado texto (str).")
        if campo == "titulo":
            PsicologoValidator._validar_tamanho_minimo(valor, campo, 5)

    @staticmethod
    def validar(dados: dict) -> None:
        for campo in CAMPOS_PSICOLOGO:
            valor = dados.get(campo)
            print(f"Validando campo '{campo}' com valor '{valor}'")
            if not valor or not isinstance(valor, str):
                raise ValueError(
                    f"psicologo.{campo}: esperado texto (str), recebeu {type(valor).__name__}."
                )
            if campo in CAMPOS_TEXTO_PURO.get("psicologo", []):
                PsicologoValidator._validar_texto_puro(valor, campo)
            PsicologoValidator._validar_campos_especificos(campo, valor)
