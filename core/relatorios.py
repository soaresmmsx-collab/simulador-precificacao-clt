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
MARGEM_INF = 4.5 * cm
LARGURA_TEXTO = A4[0] - (MARGEM_ESQ + MARGEM_DIR)

FONT_TEXTO = "Helvetica"
FONT_TITULO = "Helvetica-Bold"

SIZE_TEXTO = 11
SIZE_TITULO = 14

LEADING = 18            # ~1,5
ESPACO_PARAGRAFO = 6    # espaço reduzido entre parágrafos

# ======================================================
# UTILIDADES
# ======================================================

def _footer(c, pagina):
    c.setFont("Helvetica-Oblique", 8)
    c.drawRightString(A4[0] - MARGEM_DIR, 1.5 * cm, f"Página {pagina}")

def _cabecalho(c, titulo, subtitulo):
    largura, altura = A4
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "..", "assets", "logo.png")

    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        logo_w = 3.5 * cm
        logo_h = 3.5 * cm
        topo = altura - 2.2 * cm
        base = altura - 3.7 * cm
        y_logo = base + ((topo - base - logo_h) / 2)
        c.drawImage(logo, MARGEM_ESQ, y_logo, logo_w, logo_h, mask="auto")

    c.setFont("Helvetica-Bold", 16)
    c.drawRightString(largura - MARGEM_DIR, altura - 2.2 * cm, titulo)

    c.setFont("Helvetica", 11)
    c.drawRightString(largura - MARGEM_DIR, altura - 2.9 * cm, subtitulo)

    c.line(
        MARGEM_ESQ + 4.5 * cm,
        altura - 3.7 * cm,
        largura - MARGEM_DIR,
        altura - 3.7 * cm
    )

    return altura - 5.5 * cm

def _nova_pagina(c, pagina, titulo, subtitulo):
    _footer(c, pagina)
    c.showPage()
    pagina += 1
    y = _cabecalho(c, titulo, subtitulo)
    return y, pagina

# ======================================================
# TEXTO JUSTIFICADO + PAGINAÇÃO PREVENTIVA
# ======================================================

def _draw_texto_justificado(
    c, texto, y, pagina, titulo, subtitulo,
    font=FONT_TEXTO, size=SIZE_TEXTO, leading=LEADING
):
    c.setFont(font, size)

    for paragrafo in texto.split("\n"):
        palavras = paragrafo.split()
        linha = []
        largura_linha = 0

        for palavra in palavras:
            w = stringWidth(palavra + " ", font, size)
            if largura_linha + w <= LARGURA_TEXTO:
                linha.append(palavra)
                largura_linha += w
            else:
                if y < MARGEM_INF:
                    y, pagina = _nova_pagina(c, pagina, titulo, subtitulo)
                    c.setFont(font, size)

                _draw_linha_justificada(c, linha, y, font, size)
                y -= leading
                linha = [palavra]
                largura_linha = stringWidth(palavra + " ", font, size)

        if linha:
            if y < MARGEM_INF:
                y, pagina = _nova_pagina(c, pagina, titulo, subtitulo)
                c.setFont(font, size)
            c.drawString(MARGEM_ESQ, y, " ".join(linha))
            y -= leading

        y -= ESPACO_PARAGRAFO

    return y, pagina

def _draw_linha_justificada(c, palavras, y, font, size):
    if len(palavras) == 1:
        c.drawString(MARGEM_ESQ, y, palavras[0])
        return

    largura_palavras = sum(stringWidth(p, font, size) for p in palavras)
    espaco_total = LARGURA_TEXTO - largura_palavras
    espaco = espaco_total / (len(palavras) - 1)

    x = MARGEM_ESQ
    for p in palavras:
        c.drawString(x, y, p)
        x += stringWidth(p, font, size) + espaco

# ======================================================
# PDF COMERCIAL
# ======================================================

def gerar_proposta_comercial_pdf(
    caminho, cliente, titulo, resumo_executivo,
    texto_institucional, texto_comercial,
    validade, valor_nf, margem, cargos
):
    c = canvas.Canvas(caminho, pagesize=A4)
    pagina = 1

    # CAPA
    y = _cabecalho(c, "PROPOSTA EXECUTIVA", f"{cliente} | Validade: {validade}")

    c.setFont(FONT_TITULO, SIZE_TITULO)
    c.drawString(MARGEM_ESQ, y, titulo)
    y -= LEADING

    y, pagina = _draw_texto_justificado(
        c, resumo_executivo, y, pagina,
        "PROPOSTA EXECUTIVA", f"{cliente} | Validade: {validade}"
    )

    y -= 20
    c.setFont(FONT_TITULO, 18)
    c.drawString(MARGEM_ESQ, y, valor_nf)

    _footer(c, pagina)

    # COMERCIAL
    y, pagina = _nova_pagina(
        c, pagina,
        "PROPOSTA COMERCIAL",
        f"{cliente} | {date.today().strftime('%d/%m/%Y')}"
    )

    c.setFont(FONT_TITULO, SIZE_TITULO)
    c.drawString(MARGEM_ESQ, y, "Contexto Institucional")
    y -= LEADING

    y, pagina = _draw_texto_justificado(
        c, texto_institucional, y, pagina,
        "PROPOSTA COMERCIAL",
        f"{cliente} | {date.today().strftime('%d/%m/%Y')}"
    )

    c.setFont(FONT_TITULO, SIZE_TITULO)
    c.drawString(MARGEM_ESQ, y, "Proposta Comercial")
    y -= LEADING

    y, pagina = _draw_texto_justificado(
        c, texto_comercial, y, pagina,
        "PROPOSTA COMERCIAL",
        f"{cliente} | {date.today().strftime('%d/%m/%Y')}"
    )

    assinatura = (
        "Atenciosamente,\n\n"
        "Jhonny Souza\n"
        "J Talent – Equipe Comercial\n"
        "Telefone: +55 38 98422 4399\n"
        "E-mail: contato@jtalent.com.br"
    )

    y, pagina = _draw_texto_justificado(
        c, assinatura, y, pagina,
        "PROPOSTA COMERCIAL",
        f"{cliente} | {date.today().strftime('%d/%m/%Y')}",
        font=FONT_TEXTO, size=SIZE_TEXTO
    )

    _footer(c, pagina)
    c.save()
