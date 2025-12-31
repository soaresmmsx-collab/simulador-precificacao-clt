import os
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader


# ======================================================
# CONFIGURAÇÕES GERAIS
# ======================================================

MARGEM_ESQ = 2.5 * cm
MARGEM_DIR = 2.5 * cm
MARGEM_INF = 3.0 * cm   # margem de segurança inferior
LARGURA_TEXTO = A4[0] - (MARGEM_ESQ + MARGEM_DIR)


# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================

def _draw_paragraph(c, texto, x, y, largura, font="Helvetica", size=10, leading=14):
    c.setFont(font, size)
    t = c.beginText(x, y)
    t.setLeading(leading)

    for linha in texto.split("\n"):
        palavras = linha.split(" ")
        atual = ""
        for p in palavras:
            teste = atual + p + " "
            if stringWidth(teste, font, size) <= largura:
                atual = teste
            else:
                t.textLine(atual)
                atual = p + " "
        t.textLine(atual)

    c.drawText(t)
    return t.getY()


def _footer(c, pagina):
    c.setFont("Helvetica-Oblique", 8)
    c.drawRightString(A4[0] - MARGEM_DIR, 1.5 * cm, f"Página {pagina}")


def _nova_pagina(c, pagina, titulo, subtitulo):
    _footer(c, pagina)
    c.showPage()
    pagina += 1
    y = _cabecalho(c, titulo, subtitulo)
    return y, pagina


def _quebra_pagina_se_necessario(c, y, pagina, titulo, subtitulo):
    if y < MARGEM_INF:
        return _nova_pagina(c, pagina, titulo, subtitulo)
    return y, pagina


# ======================================================
# CABEÇALHO PADRÃO
# ======================================================

def _cabecalho(c, titulo, subtitulo):
    largura, altura = A4

    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.normpath(os.path.join(base_dir, "..", "assets", "logo.png"))

    # Logo
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        logo_w = 3.5 * cm
        logo_h = 3.5 * cm
        topo = altura - 2.2 * cm
        base = altura - 3.7 * cm
        y_logo = base + ((topo - base - logo_h) / 2)

        c.drawImage(
            logo,
            MARGEM_ESQ,
            y_logo,
            width=logo_w,
            height=logo_h,
            preserveAspectRatio=True,
            mask="auto"
        )

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawRightString(largura - MARGEM_DIR, altura - 2.2 * cm, titulo)

    c.setFont("Helvetica", 11)
    c.drawRightString(largura - MARGEM_DIR, altura - 2.9 * cm, subtitulo)

    # Linha divisória (respeita logo)
    c.setLineWidth(0.6)
    c.line(
        MARGEM_ESQ + 4.5 * cm,
        altura - 3.7 * cm,
        largura - MARGEM_DIR,
        altura - 3.7 * cm
    )

    return altura - 5.5 * cm


# ======================================================
# PDF COMERCIAL (COM CAPA + PAGINAÇÃO CORRETA)
# ======================================================

def gerar_proposta_comercial_pdf(
    caminho,
    cliente,
    titulo,
    resumo_executivo,
    texto_institucional,
    texto_comercial,
    validade,
    valor_nf,
    margem,
    cargos
):
    c = canvas.Canvas(caminho, pagesize=A4)
    pagina = 1

    # ---------- CAPA EXECUTIVA ----------
    y = _cabecalho(c, "PROPOSTA EXECUTIVA", f"{cliente} | Validade: {validade}")

    y = _draw_paragraph(
        c, titulo, MARGEM_ESQ, y, LARGURA_TEXTO,
        font="Helvetica-Bold", size=14, leading=18
    )
    y -= 20

    y = _draw_paragraph(
        c, resumo_executivo, MARGEM_ESQ, y, LARGURA_TEXTO,
        font="Helvetica", size=11, leading=16
    )

    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGEM_ESQ, y, "Valor mensal da proposta")
    y -= 18
    c.setFont("Helvetica-Bold", 18)
    c.drawString(MARGEM_ESQ, y, valor_nf)

    _footer(c, pagina)

    # ---------- PROPOSTA COMERCIAL ----------
    y, pagina = _nova_pagina(
        c, pagina,
        "PROPOSTA COMERCIAL",
        f"{cliente} | {date.today().strftime('%d/%m/%Y')}"
    )

    # Texto institucional
    y = _draw_paragraph(c, texto_institucional, MARGEM_ESQ, y, LARGURA_TEXTO)
    y -= 15
    y, pagina = _quebra_pagina_se_necessario(
        c, y, pagina,
        "PROPOSTA COMERCIAL",
        f"{cliente} | {date.today().strftime('%d/%m/%Y')}"
    )

    # Texto comercial (IA)
    y = _draw_paragraph(c, texto_comercial, MARGEM_ESQ, y, LARGURA_TEXTO)
    y -= 20
    y, pagina = _quebra_pagina_se_necessario(
        c, y, pagina,
        "PROPOSTA COMERCIAL",
        f"{cliente} | {date.today().strftime('%d/%m/%Y')}"
    )

    # Escopo
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGEM_ESQ, y, "Escopo de Alocação")
    y -= 10

    for cargo in cargos:
        y = _draw_paragraph(
            c,
            f"- {cargo['Cargo']} (Quantidade: {cargo['Quantidade']})",
            MARGEM_ESQ,
            y,
            LARGURA_TEXTO
        )
        y, pagina = _quebra_pagina_se_necessario(
            c, y, pagina,
            "PROPOSTA COMERCIAL",
            f"{cliente} | {date.today().strftime('%d/%m/%Y')}"
        )

    # Resumo comercial
    y -= 20
    y, pagina = _quebra_pagina_se_necessario(
        c, y, pagina,
        "PROPOSTA COMERCIAL",
        f"{cliente} | {date.today().strftime('%d/%m/%Y')}"
    )

    c.rect(MARGEM_ESQ, y - 45, LARGURA_TEXTO, 45)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGEM_ESQ + 10, y - 20, f"Valor mensal: {valor_nf}")
    c.drawString(MARGEM_ESQ + 10, y - 35, f"Margem aplicada: {margem}")

    _footer(c, pagina)
    c.save()
