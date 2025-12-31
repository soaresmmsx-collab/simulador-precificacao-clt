import os
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader

# ================= CONFIG =================
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

# ================= UTIL =================
def _brl(v):
    try:
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return str(v)

def _footer(c, p):
    c.setFont("Helvetica-Oblique", 8)
    c.drawRightString(A4[0]-MARGEM_DIR, 1.5*cm, f"Página {p}")

def _cabecalho(c, titulo, subtitulo):
    largura, altura = A4
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "..", "assets", "logo.png")

    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        topo = altura - 2.2*cm
        base = altura - 3.7*cm
        y_logo = base + ((topo - base - 3.5*cm)/2)
        c.drawImage(
            logo,
            MARGEM_ESQ,
            y_logo,
            width=3.5*cm,
            height=3.5*cm,
            preserveAspectRatio=True,
            anchor="sw",
            mask="auto"
        )

    c.setFont(FONT_TITULO, 16)
    c.drawRightString(largura-MARGEM_DIR, altura-2.2*cm, titulo)
    c.setFont("Helvetica", 11)
    c.drawRightString(largura-MARGEM_DIR, altura-2.9*cm, subtitulo)

    c.line(MARGEM_ESQ+4.5*cm, altura-3.7*cm, largura-MARGEM_DIR, altura-3.7*cm)
    return altura - 5.5*cm

def _nova_pagina(c, p, titulo, subtitulo):
    _footer(c, p)
    c.showPage()
    return _cabecalho(c, titulo, subtitulo), p+1

def _remover_encerramento(txt):
    marc = ["atenciosamente", "att", "cordialmente"]
    out = []
    for l in txt.splitlines():
        if l.strip().lower() in marc:
            break
        out.append(l)
    return "\n".join(out).strip()

# ================= JUSTIFICADO =================
def _linha_justificada(c, palavras, y, font, size):
    if len(palavras) <= 1:
        c.drawString(MARGEM_ESQ, y, palavras[0] if palavras else "")
        return
    total = sum(stringWidth(p, font, size) for p in palavras)
    esp = (LARGURA_TEXTO - total) / (len(palavras)-1)
    x = MARGEM_ESQ
    for p in palavras:
        c.drawString(x, y, p)
        x += stringWidth(p, font, size) + esp

def _texto_justificado(c, texto, y, p, titulo, subtitulo, font=FONT_TEXTO, size=SIZE_TEXTO):
    c.setFont(font, size)
    for par in texto.split("\n"):
        par = par.strip()
        if not par:
            y -= ESPACO_PARAGRAFO
            continue

        # títulos vindos como **Titulo**
        if par.startswith("**") and par.endswith("**"):
            t = par.replace("**","").strip()
            if y < MARGEM_INF:
                y, p = _nova_pagina(c, p, titulo, subtitulo)
            c.setFont(FONT_TITULO, SIZE_TITULO)
            c.drawString(MARGEM_ESQ, y, t)
            y -= LEADING
            c.setFont(font, size)
            continue

        palavras = par.split()
        linha = []
        w = 0
        for palavra in palavras:
            pw = stringWidth(palavra+" ", font, size)
            if w + pw <= LARGURA_TEXTO:
                linha.append(palavra)
                w += pw
            else:
                if y < MARGEM_INF:
                    y, p = _nova_pagina(c, p, titulo, subtitulo)
                    c.setFont(font, size)
                _linha_justificada(c, linha, y, font, size)
                y -= LEADING
                linha = [palavra]
                w = stringWidth(palavra+" ", font, size)

        if linha:
            if y < MARGEM_INF:
                y, p = _nova_pagina(c, p, titulo, subtitulo)
                c.setFont(font, size)
            c.drawString(MARGEM_ESQ, y, " ".join(linha))
            y -= LEADING

        y -= ESPACO_PARAGRAFO
    return y, p

# ================= COMERCIAL =================
def gerar_proposta_comercial_pdf(
    caminho, cliente, titulo, resumo_executivo,
    texto_institucional, texto_comercial,
    validade, valor_nf, margem, cargos
):
    c = canvas.Canvas(caminho, pagesize=A4)
    p = 1

    y = _cabecalho(c, "PROPOSTA EXECUTIVA", f"{cliente} | Validade: {validade}")
    c.setFont(FONT_TITULO, SIZE_TITULO)
    c.drawString(MARGEM_ESQ, y, titulo)
    y -= LEADING

    y, p = _texto_justificado(c, resumo_executivo, y, p, "PROPOSTA EXECUTIVA", f"{cliente} | Validade: {validade}")
    y -= 20
    c.setFont(FONT_TITULO, 18)
    c.drawString(MARGEM_ESQ, y, valor_nf)
    _footer(c, p)

    y, p = _nova_pagina(c, p, "PROPOSTA COMERCIAL", f"{cliente} | {date.today().strftime('%d/%m/%Y')}")
    y, p = _texto_justificado(c, texto_institucional, y, p, "PROPOSTA COMERCIAL", f"{cliente} | {date.today().strftime('%d/%m/%Y')}")

    texto_comercial = _remover_encerramento(texto_comercial)
    y, p = _texto_justificado(c, texto_comercial, y, p, "PROPOSTA COMERCIAL", f"{cliente} | {date.today().strftime('%d/%m/%Y')}")

    assinatura = (
        "Atenciosamente,\n\n"
        "Jhonny Souza\n"
        "J Talent – Equipe Comercial\n"
        "Telefone: +55 38 98422 4399\n"
        "E-mail: contato@jtalent.com.br"
    )
    y, p = _texto_justificado(c, assinatura, y, p, "PROPOSTA COMERCIAL", f"{cliente} | {date.today().strftime('%d/%m/%Y')}")
    _footer(c, p)
    c.save()

# ================= TÉCNICO =================
def gerar_pdf_tecnico(caminho_pdf, cargos, clt_detalhado, das_total, lucro, das_detalhado):
    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    p = 1
    y = _cabecalho(c, "PROPOSTA TÉCNICA", "Memória de Cálculo – Custos, Encargos e Tributos")

    c.setFont(FONT_TITULO, SIZE_TITULO)
    c.drawString(MARGEM_ESQ, y, "Custos por Cargo")
    y -= LEADING

    for cargo in cargos:
        linha = (
            f"{cargo['Cargo']} | Qtd: {cargo['Quantidade']} | "
            f"Salário Base: {_brl(cargo['Salário Base'])} | "
            f"Custo Unitário: {_brl(cargo['Custo Unitário'])}"
        )
        y, p = _texto_justificado(c, linha, y, p, "PROPOSTA TÉCNICA", "Memória de Cálculo – Custos, Encargos e Tributos")

    c.setFont(FONT_TITULO, SIZE_TITULO)
    c.drawString(MARGEM_ESQ, y, "Resultado Final")
    y -= LEADING
    y, p = _texto_justificado(c, f"Lucro Mensal: {_brl(lucro)}", y, p, "PROPOSTA TÉCNICA", "Memória de Cálculo – Custos, Encargos e Tributos")

    _footer(c, p)
    c.save()
