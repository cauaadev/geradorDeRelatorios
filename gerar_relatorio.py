

import sys
import json
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak,
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

from get_dados import preparar

ESTILOS = {
    "cab":        ParagraphStyle("cab",        fontName="Helvetica", fontSize=14, leading=18, alignment=TA_CENTER),
    "titulo":     ParagraphStyle("titulo",     fontName="Helvetica", fontSize=18, leading=24, alignment=TA_CENTER, spaceBefore=14, spaceAfter=14),
    "corpo":      ParagraphStyle("corpo",      fontName="Helvetica", fontSize=14, leading=20, alignment=TA_JUSTIFY, spaceAfter=4),
    "rodape":     ParagraphStyle("rodape",     fontName="Helvetica", fontSize=14, leading=18, alignment=TA_LEFT, spaceBefore=16),
    "tab_titulo": ParagraphStyle("tab_titulo", fontName="Helvetica", fontSize=14, leading=18, alignment=TA_LEFT, spaceBefore=16, spaceAfter=6),
}


def _pagina_relatorio(d: dict) -> list:
    st = ESTILOS
    story = []

    for linha in d["cabecalho"]:
        story.append(Paragraph(linha, st["cab"]))

    story.append(Spacer(1, 8))
    story.append(Paragraph("RELATORIO", st["titulo"]))
    story.append(Paragraph(d["texto"], st["corpo"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Endereco do consultorio:", st["corpo"]))

    for linha in [d["psi"]["endereco"], d["psi"]["bairro"],
                  d["psi"]["cidade"],   d["psi"]["cep"]]:
        story.append(Paragraph(linha, st["corpo"]))

    story.append(Spacer(1, 20))
    story.append(Paragraph(d["psi"]["nome"], st["rodape"]))
    story.append(Paragraph(d["data_extenso"], st["rodape"]))

    return story


def _pagina_ficha(d: dict, W: float) -> list:
    st = ESTILOS
    story = [PageBreak()]

    for linha in d["cabecalho"]:
        story.append(Paragraph(linha, st["cab"]))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "FICHA DE FREQUENCIA DE ATENDIMENTO DE PSICOTERAPIA:", st["tab_titulo"]
    ))

    col_w = [W*0.12, W*0.22, W*0.12, W*0.18, W*0.18, W*0.18]
    header = [["Data", "Horario", "Sessoes", "Terapeuta", "Assinatura", "Responsavel"]]
    rows = [
        [s["data"], s["horario"], str(s["num_sessoes"]), d["psi"]["nome_curto"], "", ""]
        for s in d["sessoes"]
    ]

    row_colors = []
    for i in range(1, len(rows) + 1):
        bg = colors.white if i % 2 == 1 else colors.HexColor("#F2F2F2")
        row_colors.append(("BACKGROUND", (0, i), (-1, i), bg))

    tabela = Table(header + rows, colWidths=col_w, repeatRows=1)
    tabela.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), colors.HexColor("#D9D9D9")),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 11),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.black),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ] + row_colors))

    story.append(tabela)
    story.append(Spacer(1, 30))
    story.append(Paragraph(d["psi"]["nome"], st["rodape"]))

    return story


# ── Função principal ──────────────────────────────────────────────────────────

def gerar_pdf(dados: dict) -> bytes:
    d = preparar(dados)  # valida + prepara — toda lógica está no get_dados.py

    W = A4[0] - 5 * cm
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=2.5*cm, leftMargin=2.5*cm,
        topMargin=2*cm,     bottomMargin=2*cm,
    )

    story = _pagina_relatorio(d) + _pagina_ficha(d, W)
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


if __name__ == "__main__":
    dados = json.loads(sys.stdin.read())
    saida = dados.get("saida", "relatorio.pdf")
    pdf_bytes = gerar_pdf(dados)
    with open(saida, "wb") as f:
        f.write(pdf_bytes)
    print(f"PDF gerado: {saida}", flush=True)
