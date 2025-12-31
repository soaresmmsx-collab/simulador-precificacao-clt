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
MARGEM_INF = 4.0 * cm

LARGURA_TEXTO = A4[0] - (MARGEM_ESQ + MARGEM_DIR)

FONT_TEXTO = "Helvetica"
FONT_TITULO = "Helvetica-Bold"

SIZE_TEXTO = 11
SIZE_TITULO = 14
SIZE_TITULO_GRANDE = 16

LEADING = 16
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


def _nova_pagina(c, pagina, titulo, subtitulo):
    _footer(c, pagina)
    c.showPage()
    pagina += 1
    y = _cabecalho(c, titulo, subtitulo)
    return y, pagina


# ======================================================
# CABEÇALHO (SEGURO)
# ======================================================

def _cabecalho(c, titulo, subtitulo):
    largura, altura = A4
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "..", "assets", "logo.png")

    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        c.drawImage(
            logo,
            MARGEM_ESQ,
            altura - 4.5 * cm,
            width=3.5 * cm,
            height=3.5 * cm,
            preserveAspectRatio=True,
            mask="auto"
        )

    y = altura - 2.5 * cm

    # Título
    c.setFont(FONT_TITULO, SIZE_TITULO_GRANDE)
    c.drawRightString(A4[0] - MARGEM_DIR, y, titulo)
    y -= 18

    # Subtítulo quebrado manualmente (direita)
    c.setFont(FONT_TEXTO, 11)
    palavras = subtitulo.split()
    linha = ""
    for palavra in palavras:
        teste = linha + palavra + " "
        if stringWidth(teste, FONT_TEXTO, 11) <= (A4[0] - MARGEM_DIR - MARGEM_ESQ - 4.5 * cm):
            linha = teste
        else:
            c.drawRightString(A4[0] - MARGEM_DIR, y, linha.strip())
            y -= 14
            linha = palavra + " "
    if linha:
        c.drawRightString(A4[0] - MARGEM_DIR, y, linha.strip())

    c.line(
        MARGEM_ESQ,
        y - 10,
        largura - MARGEM_DIR,
        y - 10
    )

    return y - 30


# ======================================================
# TEXTO JUSTIFICADO (ÚNICO PARA CORPO)
# ======================================================

def _draw_linha_justificada(c, palavras, y):
    largura_palavras = sum(stringWidth(p, FONT_TEXTO, SIZE_TEXTO) for p in palavras)
    espaco = (LARGURA_TEXTO - largura_palavras) / (len(palavras) - 1)

    x = MARGEM_ESQ
    for p in palavras:
        c.drawString(x, y, p)
        x += stringWidth(p, FONT_TEXTO, SIZE_TEXTO) + espaco


def _draw_texto_justificado(c, texto, y, pagina, titulo, subtitulo):
    c.setFont(FONT_TEXTO, SIZE_TEXTO)

    for paragrafo in texto.split("\n"):
        paragrafo = paragrafo.strip()

        if not paragrafo:
            y -= ESPACO_PARAGRAFO
            continue

        # Títulos vindos da IA (**Texto**)
        if paragrafo.startswith("**") and paragrafo.endswith("**"):
            t = paragrafo.replace("**", "").strip()
            if y < MARGEM_INF:
                y, pagina = _nova_pagina(c, pagina, titulo, subtitulo)

            c.setFont(FONT_TITULO, SIZE_TITULO)
            c.drawString(MARGEM_ESQ, y, t)
            y -= LEADING
            c.setFont(FONT_TEXTO, SIZE_TEXTO)
            continue

        palavras = paragrafo.split()
        linha = []
        largura = 0

        for palavra in palavras:
            w = stringWidth(palavra + " ", FONT_TEXTO, SIZE_TEXTO)
            if largura + w <= LARGURA_TEXTO:
                linha.append(palavra)
                largura += w
            else:
                if y < MARGEM_INF:
                    y, pagina = _nova_pagina(c, pagina, titulo, subtitulo)
                _draw_linha_justificada(c, linha, y)
                y -= LEADING
                linha = [palavra]
                largura = stringWidth(palavra + " ", FONT_TEXTO, SIZE_TEXTO)

        if linha:
            if y < MARGEM_INF:
                y, pagina = _nova_pagina(c, pagina, titulo, subtitulo)
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

    # TÍTULO DA PROPOSTA (QUEBRA SIMPLES)
    c.setFont(FONT_TITULO, SIZE_TITULO)
    palavras = titulo_proposta.split()
    linha = ""
    for palavra in palavras:
        teste = linha + palavra + " "
        if stringWidth(teste, FONT_TITULO, SIZE_TITULO) <= LARGURA_TEXTO:
            linha = teste
        else:
            c.drawString(MARGEM_ESQ, y, linha.strip())
            y -= LEADING
            linha = palavra + " "
    if linha:
        c.drawString(MARGEM_ESQ, y, linha.strip())
        y -= LEADING

    y, pagina = _draw_texto_justificado(
        c,
        resumo_executivo,
        y,
        pagina,
        "PROPOSTA COMERCIAL",
        cliente
    )

    y -= 10
    c.setFont(FONT_TITULO, 18)
    c.drawString(MARGEM_ESQ, y, valor_nf)

    _footer(c, pagina)

    y, pagina = _nova_pagina(
        c,
        pagina,
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
            cliente
        )

    y, pagina = _draw_texto_justificado(
        c,
        texto_comercial,
        y,
        pagina,
        "PROPOSTA COMERCIAL",
        cliente
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
        cliente
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
