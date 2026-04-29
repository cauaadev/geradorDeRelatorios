CAMPOS_PACIENTE = ["nome", "tipo_terapia", "diagnostico", "cid"]

CAMPOS_TEXTO_PURO = {
    "paciente": ["nome", "diagnostico"],
}


class PacienteValidator:
    @staticmethod
    def _validar_texto_puro(valor: str, campo: str) -> None:
        if valor.strip().isdigit():
            raise ValueError(
                f"paciente.{campo}: esperado texto, mas recebeu apenas números: '{valor}'"
            )

    @staticmethod
    def _validar_tamanho_minimo(valor: str, campo: str, minimo: int) -> None:
        if len(valor.strip()) < minimo:
            raise ValueError(
                f"paciente.{campo}: muito curto '{valor}'. Mínimo {minimo} caracteres."
            )

    @staticmethod
    def _validar_campos_especificos(campo: str, valor: str) -> None:
        if campo == "nome":
            PacienteValidator._validar_tamanho_minimo(valor, campo, 4)
        if campo in ("cid", "tipo_terapia", "diagnostico") and not isinstance(valor, str):
            raise ValueError(f"paciente.{campo}: esperado texto (str).")

    @staticmethod
    def validar(dados: dict) -> None:
        for campo in CAMPOS_PACIENTE:
            valor = dados.get(campo)
            if not valor or not isinstance(valor, str):
                raise ValueError(
                    f"paciente.{campo}: esperado texto (str), recebeu {type(valor).__name__}."
                )
            if campo in CAMPOS_TEXTO_PURO.get("paciente", []):
                PacienteValidator._validar_texto_puro(valor, campo)
            PacienteValidator._validar_campos_especificos(campo, valor)
