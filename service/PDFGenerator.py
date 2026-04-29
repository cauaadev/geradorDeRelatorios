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
from service.RelatorioBuilder import RelatorioBuilder


class PDFGenerator:
    ESTILOS = {
        "cab":        ParagraphStyle("cab",        fontName="Helvetica", fontSize=14, leading=18, alignment=TA_CENTER),
        "titulo":     ParagraphStyle("titulo",     fontName="Helvetica", fontSize=18, leading=24, alignment=TA_CENTER, spaceBefore=14, spaceAfter=14),
        "corpo":      ParagraphStyle("corpo",      fontName="Helvetica", fontSize=14, leading=20, alignment=TA_JUSTIFY, spaceAfter=4),
        "rodape":     ParagraphStyle("rodape",     fontName="Helvetica", fontSize=14, leading=18, alignment=TA_LEFT, spaceBefore=16),
        "tab_titulo": ParagraphStyle("tab_titulo", fontName="Helvetica", fontSize=14, leading=18, alignment=TA_LEFT, spaceBefore=16, spaceAfter=6),
    }

    def __init__(self, dados: dict):
        self.d = RelatorioBuilder(dados).construir()

    def _pagina_relatorio(self) -> list:
        story = []
        st = self.ESTILOS

        for linha in self.d["cabecalho"]:
            story.append(Paragraph(linha, st["cab"]))

        story.append(Spacer(1, 8))
        story.append(Paragraph("RELATORIO", st["titulo"]))
        story.append(Paragraph(self.d["texto"], st["corpo"]))
        story.append(Spacer(1, 10))
        story.append(Paragraph("Endereco do consultorio:", st["corpo"]))

        for linha in [self.d["psi"]["endereco"], self.d["psi"]["bairro"],
                      self.d["psi"]["cidade"],   self.d["psi"]["cep"]]:
            story.append(Paragraph(linha, st["corpo"]))

        story.append(Spacer(1, 20))
        story.append(Paragraph(self.d["psi"]["nome"], st["rodape"]))
        story.append(Paragraph(self.d["data_extenso"], st["rodape"]))

        return story

    def _pagina_ficha(self, W: float) -> list:
        story = [PageBreak()]
        st = self.ESTILOS

        for linha in self.d["cabecalho"]:
            story.append(Paragraph(linha, st["cab"]))

        story.append(Spacer(1, 10))
        story.append(Paragraph(
            "FICHA DE FREQUENCIA DE ATENDIMENTO DE PSICOTERAPIA:", st["tab_titulo"]
        ))

        col_w = [W*0.12, W*0.22, W*0.12, W*0.18, W*0.18, W*0.18]
        header = [["Data", "Horario", "Sessoes", "Terapeuta", "Assinatura", "Responsavel"]]
        rows = [
            [s["data"], s["horario"], str(s["num_sessoes"]), self.d["psi"]["nome_curto"], "", ""]
            for s in self.d["sessoes"]
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
        story.append(Paragraph(self.d["psi"]["nome"], st["rodape"]))

        return story

    def gerar(self) -> bytes:
        W = A4[0] - 5 * cm
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A4,
            rightMargin=2.5*cm, leftMargin=2.5*cm,
            topMargin=2*cm,     bottomMargin=2*cm,
        )

        story = self._pagina_relatorio() + self._pagina_ficha(W)
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
