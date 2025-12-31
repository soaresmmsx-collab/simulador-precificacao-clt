import os
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader

# ======================================================
# CONFIGURAÇÕES
# ======================================================

MARGEM_ESQ = 2.5 * cm
MARGEM_DIR = 2.5 * cm
MARGEM_INF = 4.5 * cm
LARGURA_TEXTO = A4[0] - (MARGEM_ESQ + MARGEM_DIR)

LEADING_TEXTO = 18
LEADING_TITULO = 22

# ======================================================
# UTILIDADES
# ======================================================

def _brl(valor):
    try:
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return str(valor)

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
# TEXTO PAGINADO (ROBUSTO)
# ======================================================

def _draw_texto_paginado(
    c, texto, y, pagina, titulo, subtitulo,
    font="Helvetica", size=11, leading=LEADING_TEXTO
):
    c.setFont(font, size)

    linhas = []
    for p in texto.split("\n"):
        palavras = p.split(" ")
        linha = ""
        for w in palavras:
            teste = linha + w + " "
            if stringWidth(teste, font, size) <= LARGURA_TEXTO:
                linha = teste
            else:
                linhas.append(linha.rstrip())
                linha = w + " "
        linhas.append(linha.rstrip())
        linhas.append(None)

    for linha in linhas:
        if linha is None:
            y -= leading / 2
            continue

        if y < MARGEM_INF:
            y, pagina = _nova_pagina(c, pagina, titulo, subtitulo)
            c.setFont(font, size)

        c.drawString(MARGEM_ESQ, y, linha)
        y -= leading

    return y, pagina

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

    y, pagina = _draw_texto_paginado(
        c, titulo, y, pagina,
        "PROPOSTA EXECUTIVA", f"{cliente} | Validade: {validade}",
        font="Helvetica-Bold", size=14, leading=LEADING_TITULO
    )

    y -= 10
    y, pagina = _draw_texto_paginado(
        c, resumo_executivo, y, pagina,
        "PROPOSTA EXECUTIVA", f"{cliente} | Validade: {validade}"
    )

    y -= 20
    c.setFont("Helvetica-Bold", 18)
    c.drawString(MARGEM_ESQ, y, valor_nf)

    _footer(c, pagina)

    # COMERCIAL
    y, pagina = _nova_pagina(
        c, pagina,
        "PROPOSTA COMERCIAL",
        f"{cliente} | {date.today().strftime('%d/%m/%Y')}"
    )

    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGEM_ESQ, y, "Contexto Institucional")
    y -= LEADING_TITULO / 2

    y, pagina = _draw_texto_paginado(
        c, texto_institucional, y, pagina,
        "PROPOSTA COMERCIAL",
        f"{cliente} | {date.today().strftime('%d/%m/%Y')}"
    )

    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGEM_ESQ, y, "Proposta Comercial")
    y -= LEADING_TITULO / 2

    y, pagina = _draw_texto_paginado(
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

    y, pagina = _draw_texto_paginado(
        c, assinatura, y, pagina,
        "PROPOSTA COMERCIAL",
        f"{cliente} | {date.today().strftime('%d/%m/%Y')}"
    )

    _footer(c, pagina)
    c.save()

# ======================================================
# PDF TÉCNICO (RESTURADO)
# ======================================================

def gerar_pdf_tecnico(
    caminho_pdf,
    cargos,
    clt_detalhado,
    das_total,
    lucro,
    das_detalhado
):
    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    pagina = 1

    y = _cabecalho(
        c,
        "PROPOSTA TÉCNICA",
        "Memória de Cálculo – Custos, Encargos e Tributos"
    )

    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGEM_ESQ, y, "Custos por Cargo")
    y -= LEADING_TITULO / 2

    for cargo in cargos:
        linha = (
            f"{cargo['Cargo']} | "
            f"Qtd: {cargo['Quantidade']} | "
            f"Salário Base: {_brl(cargo['Salário Base'])} | "
            f"Custo Unitário: {_brl(cargo['Custo Unitário'])}"
        )
        y, pagina = _draw_texto_paginado(
            c, linha, y, pagina,
            "PROPOSTA TÉCNICA",
            "Memória de Cálculo – Custos, Encargos e Tributos",
            size=10
        )

    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGEM_ESQ, y, "Encargos CLT Consolidados")
    y -= LEADING_TITULO / 2

    for nome, valor in clt_detalhado.items():
        y, pagina = _draw_texto_paginado(
            c, f"{nome}: {_brl(valor)}",
            y, pagina,
            "PROPOSTA TÉCNICA",
            "Memória de Cálculo – Custos, Encargos e Tributos",
            size=10
        )

    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGEM_ESQ, y, "Resultado Final")
    y -= LEADING_TITULO / 2

    y, pagina = _draw_texto_paginado(
        c, f"Lucro Mensal: {_brl(lucro)}",
        y, pagina,
        "PROPOSTA TÉCNICA",
        "Memória de Cálculo – Custos, Encargos e Tributos"
    )

    _footer(c, pagina)
    c.save()
