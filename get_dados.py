"""
get_dados.py
------------
Responsável por receber o dicionário bruto do formulário,
validar campos obrigatórios, tipos e formatos,
e preparar os dados prontos para o gerar_relatorio.py usar.
"""

import re
from datetime import datetime

MESES = {
    "01": "janeiro", "02": "fevereiro", "03": "marco", "04": "abril",
    "05": "maio",    "06": "junho",     "07": "julho", "08": "agosto",
    "09": "setembro","10": "outubro",   "11": "novembro","12": "dezembro",
}

CAMPOS_PSICOLOGO = ["nome", "titulo", "crp", "cpf", "telefone",
                    "endereco", "bairro", "cidade", "cep", "nome_curto"]

CAMPOS_PACIENTE  = ["nome", "tipo_terapia", "diagnostico", "cid"]

CAMPOS_TEXTO_PURO = {
    "psicologo": ["nome", "titulo", "bairro", "cidade", "nome_curto"],
    "paciente":  ["nome", "diagnostico"],
}

# Regex
_RE_DATA     = re.compile(r"^\d{2}/\d{2}/\d{4}$")
_RE_HORARIO  = re.compile(r"^\d{2}:\d{2}-\d{2}:\d{2}$")
_RE_TELEFONE = re.compile(r"^\(\d{2}\) \d{5}-\d{4}$")
_RE_TEM_NUM  = re.compile(r"\d")  # contém ao menos um dígito (CRP)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _validar_texto_puro(valor: str, campo: str, secao: str) -> None:
    if valor.strip().isdigit():
        raise ValueError(
            f"{secao}.{campo}: esperado texto, mas recebeu apenas números: '{valor}'"
        )

def _validar_tamanho_minimo(valor: str, campo: str, secao: str, minimo: int) -> None:
    if len(valor.strip()) < minimo:
        raise ValueError(
            f"{secao}.{campo}: muito curto '{valor}'. Mínimo {minimo} caracteres."
        )

def _validar_data(valor: str, campo: str) -> None:
    if not _RE_DATA.match(valor):
        raise ValueError(f"{campo}: formato inválido '{valor}'. Esperado DD/MM/AAAA.")
    try:
        datetime.strptime(valor, "%d/%m/%Y")
    except ValueError:
        raise ValueError(f"{campo}: '{valor}' não é uma data válida.")

def _validar_horario(valor: str, campo: str) -> None:
    if not _RE_HORARIO.match(valor):
        raise ValueError(f"{campo}: formato inválido '{valor}'. Esperado HH:MM-HH:MM.")
    inicio, fim = valor.split("-")
    if inicio >= fim:
        raise ValueError(f"{campo}: início '{inicio}' deve ser anterior ao fim '{fim}'.")

def _validar_campos_especificos(campo: str, valor: str, secao: str) -> None:
    """Validações de formato específicas por campo."""
    if secao == "psicologo":
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
            _validar_tamanho_minimo(valor, campo, secao, 5)

    if secao == "paciente":
        if campo == "nome":
            _validar_tamanho_minimo(valor, campo, secao, 4)
        if campo in ("cid", "tipo_terapia", "diagnostico") and not isinstance(valor, str):
            raise ValueError(f"paciente.{campo}: esperado texto (str).")

def _validar_secao(secao: str, campos: list, valores: dict) -> None:
    for campo in campos:
        valor = valores.get(campo)
        if not valor or not isinstance(valor, str):
            raise ValueError(
                f"{secao}.{campo}: esperado texto (str), recebeu {type(valor).__name__}."
            )
        if campo in CAMPOS_TEXTO_PURO.get(secao, []):
            _validar_texto_puro(valor, campo, secao)
        _validar_campos_especificos(campo, valor, secao)


# ── Validação principal ───────────────────────────────────────────────────────

def validar(dados: dict) -> None:
    _validar_secao("psicologo", CAMPOS_PSICOLOGO, dados.get("psicologo", {}))
    _validar_secao("paciente",  CAMPOS_PACIENTE,  dados.get("paciente", {}))

    sessoes = dados.get("sessoes", [])
    if not sessoes or not isinstance(sessoes, list):
        raise ValueError("É necessário ao menos uma sessão.")

    for i, s in enumerate(sessoes):
        prefixo = f"sessoes[{i}]"

        data = s.get("data")
        if not data:
            raise ValueError(f"{prefixo}: campo 'data' ausente.")
        _validar_data(data, prefixo + ".data")

        horario = s.get("horario")
        if not horario:
            raise ValueError(f"{prefixo}: campo 'horario' ausente.")
        _validar_horario(horario, prefixo + ".horario")

        num = s.get("num_sessoes")
        if not isinstance(num, int) or num < 1:
            raise ValueError(
                f"{prefixo}: 'num_sessoes' deve ser inteiro >= 1, recebeu '{num}'."
            )


# ── Preparação ────────────────────────────────────────────────────────────────

def _data_extenso(sessoes: list, psi: dict, ano_fallback: str = "2026") -> str:
    try:
        p = sessoes[-1]["data"].split("/")
        cidade = psi["cidade"].split("/")[0].strip()
        mes = MESES.get(p[1], p[1])
        ano = p[2] if len(p) > 2 else ano_fallback
        return f"{cidade}, {p[0]} de {mes} de {ano}"
    except Exception:
        return ""

def _lista_dias(sessoes: list) -> str:
    return ", ".join(
        f"{s['data']} ({s['num_sessoes']} {'sessao' if s['num_sessoes'] == 1 else 'sessoes'})"
        for s in sessoes
    )

def _linhas_cabecalho(psi: dict) -> list:
    return [
        psi["nome"].upper(), psi["titulo"].upper(),
        psi["crp"], psi["cpf"], psi["telefone"],
        psi["endereco"], psi["bairro"], psi["cidade"], psi["cep"],
    ]

def _texto_relatorio(pac: dict, sessoes: list) -> str:
    total = sum(s["num_sessoes"] for s in sessoes)
    return (
        f"Atendimento de psicoterapia {pac['tipo_terapia']} realizado "
        f"({total} sessoes de uma hora cada) nos dias {_lista_dias(sessoes)} "
        f"ao paciente {pac['nome']}, diagnosticado com "
        f"{pac['diagnostico']} ({pac['cid']})."
    )


# ── Função principal exportada ────────────────────────────────────────────────

def preparar(dados: dict) -> dict:
    validar(dados)
    psi     = dados["psicologo"]
    pac     = dados["paciente"]
    sessoes = dados["sessoes"]
    return {
        "psi":          psi,
        "pac":          pac,
        "sessoes":      sessoes,
        "cabecalho":    _linhas_cabecalho(psi),
        "texto":        _texto_relatorio(pac, sessoes),
        "data_extenso": _data_extenso(sessoes, psi, dados.get("ano", "2026")),
    }
