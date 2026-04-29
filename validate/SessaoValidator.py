import re
from datetime import datetime


class SessaoValidator:
    _RE_DATA = re.compile(r"^\d{2}/\d{2}/\d{4}$")
    _RE_HORARIO = re.compile(r"^\d{2}:\d{2}-\d{2}:\d{2}$")

    @staticmethod
    def validar_data(valor: str, campo: str) -> None:
        if not SessaoValidator._RE_DATA.match(valor):
            raise ValueError(f"{campo}: formato inválido '{valor}'. Esperado DD/MM/AAAA.")
        try:
            datetime.strptime(valor, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"{campo}: '{valor}' não é uma data válida.")

    @staticmethod
    def validar_horario(valor: str, campo: str) -> None:
        if not SessaoValidator._RE_HORARIO.match(valor):
            raise ValueError(f"{campo}: formato inválido '{valor}'. Esperado HH:MM-HH:MM.")
        inicio, fim = valor.split("-")
        if inicio >= fim:
            raise ValueError(f"{campo}: início '{inicio}' deve ser anterior ao fim '{fim}'.")

    @staticmethod
    def validar_num_sessoes(valor: int, campo: str) -> None:
        if not isinstance(valor, int) or valor < 1:
            raise ValueError(
                f"{campo}: 'num_sessoes' deve ser inteiro >= 1, recebeu '{valor}'."
            )

    @staticmethod
    def validar(sessoes: list) -> None:
        if not sessoes or not isinstance(sessoes, list):
            raise ValueError("É necessário ao menos uma sessão.")

        for i, s in enumerate(sessoes):
            prefixo = f"sessoes[{i}]"

            data = s.get("data")
            if not data:
                raise ValueError(f"{prefixo}: campo 'data' ausente.")
            SessaoValidator.validar_data(data, prefixo + ".data")

            horario = s.get("horario")
            if not horario:
                raise ValueError(f"{prefixo}: campo 'horario' ausente.")
            SessaoValidator.validar_horario(horario, prefixo + ".horario")

            num = s.get("num_sessoes")
            SessaoValidator.validar_num_sessoes(num, prefixo)
