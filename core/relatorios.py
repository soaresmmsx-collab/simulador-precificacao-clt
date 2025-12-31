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

LEADING = 18
ESPACO_PARAGRAFO = 6

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

    # LOGO
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
            anchor="sw",
            mask="auto"
        )

    # TÍTULO (direita)
    c.setFont("Helvetica-Bold", 16)
    c.drawRightString(largura - MARGEM_DIR, altura - 2.2 * cm, titulo)

    # SUBTÍTULO (direita, COM QUEBRA AUTOMÁTICA)
    c.setFont("Helvetica", 11)
    x_sub = MARGEM_ESQ + 4.5 * cm
    y_sub = altura - 2.9 * cm
    largura_sub = largura - MARGEM_DIR - x_sub

    text = c.beginText()
    text.setTextOrigin(x_sub, y_sub)
    text.setLeading(14)

    palavras = subtitulo.split()
    linha = ""

    for palavra in palavras:
        teste = linha + palavra + " "
        if stringWidth(teste, "Helvetica", 11) <= largura_sub:
            linha = teste
        else:
            text.textLine(linha.rstrip())
            linha = palavra + " "

    if linha:
        text.textLine(linha.rstrip())

    c.drawText(text)

    # LINHA SEPARADORA
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
# TEXTO JUSTIFICADO
# ======================================================

def _draw_linha_justificada(c, palavras, y, font, size):
    if len(palavras) <= 1:
        c.drawString(MARGEM_ESQ, y, palavras[0])
        return

    largura_palavras = sum(stringWidth(p, font, size) for p in palavras)
    espaco = (LARGURA_TEXTO - largura_palavras) / (len(palavras) - 1)

    x = MARGEM_ESQ
    for p in palavras:
        c.drawString(x, y, p)
        x += stringWidth(p, font, size) + espaco

def _draw_texto_justificado(
    c, texto, y, pagina, titulo, subtitulo,
    font=FONT_TEXTO, size=SIZE_TEXTO
):
    c.setFont(font, size)

    for paragrafo in texto.split("\n"):
        paragrafo = paragrafo.strip()
        if not paragrafo:
            y -= ESPACO_PARAGRAFO
            continue

        if paragrafo.startswith("**") and paragrafo.endswith("**"):
            t = paragrafo.replace("**", "").strip()
            if y < MARGEM_INF:
                y, pagina = _nova_pagina(c, pagina, titulo, subtitulo)
            c.setFont(FONT_TITULO, SIZE_TITULO)
            c.drawString(MARGEM_ESQ, y, t)
            y -= LEADING
            c.setFont(font, size)
            continue

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
                y -= LEADING
                linha = [palavra]
                largura_linha = stringWidth(palavra + " ", font, size)

        if linha:
            if y < MARGEM_INF:
                y, pagina = _nova_pagina(c, pagina, titulo, subtitulo)
                c.setFont(font, size)
            c.drawString(MARGEM_ESQ, y, " ".join(linha))
            y -= LEADING

        y -= ESPACO_PARAGRAFO

    return y, pagina

# ======================================================
# PROPOSTA COMERCIAL
# ======================================================

def gerar_proposta_comercial_pdf(
    caminho,
    cliente,
    titulo_proposta,
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

    y = _cabecalho(c, "PROPOSTA COMERCIAL", f"{cliente} | Validade: {validade}")

    c.setFont(FONT_TITULO, SIZE_TITULO)
    y, pagina = _draw_texto_justificado(
        c,
        titulo_proposta,
        y,
        pagina,
        "PROPOSTA COMERCIAL",
        f"{cliente} | Validade: {validade}",
        font=FONT_TITULO,
        size=SIZE_TITULO
    )

    y, pagina = _draw_texto_justificado(
        c,
        resumo_executivo,
        y,
        pagina,
        "PROPOSTA COMERCIAL",
        f"{cliente} | Validade: {validade}"
    )

    y -= 12
    c.setFont("Helvetica-Bold", 18)
    c.drawString(MARGEM_ESQ, y, valor_nf)

    _footer(c, pagina)

    y, pagina = _nova_pagina(
        c, pagina,
        "PROPOSTA COMERCIAL",
        f"{cliente} | {date.today().strftime('%d/%m/%Y')}"
    )

    if texto_institucional:
        y, pagina = _draw_texto_justificado(
            c,
            texto_institucional,
            y,
            pagina,
            "PROPOSTA COMERCIAL",
            f"{cliente} | {date.today().strftime('%d/%m/%Y')}"
        )

    y, pagina = _draw_texto_justificado(
        c,
        texto_comercial,
        y,
        pagina,
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
        c,
        assinatura,
        y,
        pagina,
        "PROPOSTA COMERCIAL",
        f"{cliente} | {date.today().strftime('%d/%m/%Y')}"
    )

    _footer(c, pagina)
    c.save()

# ======================================================
# PROPOSTA TÉCNICA
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

    c.setFont(FONT_TITULO, SIZE_TITULO)
    c.drawString(MARGEM_ESQ, y, "Custos por Cargo")
    y -= LEADING

    for cargo in cargos:
        linha = (
            f"{cargo['Cargo']} | "
            f"Qtd: {cargo['Quantidade']} | "
            f"Salário Base: {_brl(cargo['Salário Base'])}"
        )
        y, pagina = _draw_texto_justificado(
            c,
            linha,
            y,
            pagina,
            "PROPOSTA TÉCNICA",
            "Memória de Cálculo – Custos, Encargos e Tributos"
        )

    c.setFont(FONT_TITULO, SIZE_TITULO)
    c.drawString(MARGEM_ESQ, y, "Resultado Final")
    y -= LEADING

    y, pagina = _draw_texto_justificado(
        c,
        f"Lucro Mensal: {_brl(lucro)}",
        y,
        pagina,
        "PROPOSTA TÉCNICA",
        "Memória de Cálculo – Custos, Encargos e Tributos"
    )

    _footer(c, pagina)
    c.save()
