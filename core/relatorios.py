import os
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader


# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================

def _draw_paragraph(c, texto, x, y, largura_max, font="Helvetica", size=10, leading=14):
    c.setFont(font, size)
    textobject = c.beginText(x, y)
    textobject.setLeading(leading)

    for linha in texto.split("\n"):
        palavras = linha.split(" ")
        linha_atual = ""

        for palavra in palavras:
            teste = linha_atual + palavra + " "
            if stringWidth(teste, font, size) <= largura_max:
                linha_atual = teste
            else:
                textobject.textLine(linha_atual)
                linha_atual = palavra + " "

        textobject.textLine(linha_atual)

    c.drawText(textobject)
    return textobject.getY()


def _footer(c, pagina):
    c.setFont("Helvetica-Oblique", 8)
    c.drawRightString(
        A4[0] - 2 * cm,
        1.5 * cm,
        f"Página {pagina}"
    )


def _verificar_pagina(c, y, pagina):
    if y < 4 * cm:
        _footer(c, pagina)
        c.showPage()
        return A4[1] - 4 * cm, pagina + 1
    return y, pagina


# ======================================================
# CABEÇALHO PADRÃO (ÚNICO)
# ======================================================

def _desenhar_cabecalho_padrao(c, titulo_principal, subtitulo):
    """
    Cabeçalho profissional padronizado para todos os relatórios
    """
    largura, altura = A4

    margem_esq = 2.5 * cm
    margem_dir = 2.5 * cm

    # Logo
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_logo = os.path.normpath(
        os.path.join(base_dir, "..", "assets", "logo.png")
    )

    if os.path.exists(caminho_logo):
        logo = ImageReader(caminho_logo)
        c.drawImage(
            logo,
            margem_esq,
            altura - 3.2 * cm,
            width=3.5 * cm,
            height=3.5 * cm,
            preserveAspectRatio=True,
            mask="auto"
        )

    # Título principal
    c.setFont("Helvetica-Bold", 16)
    c.drawRightString(
        largura - margem_dir,
        altura - 2.2 * cm,
        titulo_principal
    )

    # Subtítulo
    c.setFont("Helvetica", 11)
    c.drawRightString(
        largura - margem_dir,
        altura - 2.9 * cm,
        subtitulo
    )

    # Linha divisória
    c.setLineWidth(0.6)
    c.line(
        margem_esq,
        altura - 3.7 * cm,
        largura - margem_dir,
        altura - 3.7 * cm
    )

    # Retorna Y inicial do conteúdo
    return altura - 4.5 * cm


# ======================================================
# PDF COMERCIAL
# ======================================================

def gerar_proposta_comercial_pdf(
    caminho_pdf,
    cliente,
    titulo,
    texto_institucional,
    texto_comercial,
    validade,
    valor_nf,
    margem,
    cargos
):
    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    pagina = 1

    largura_texto = A4[0] - (2 * 2.5 * cm)

    y = _desenhar_cabecalho_padrao(
        c,
        "PROPOSTA COMERCIAL",
        f"Cliente: {cliente} | Validade: {validade}"
    )

    # Título da proposta
    y = _draw_paragraph(
        c, titulo, 2.5 * cm, y, largura_texto,
        font="Helvetica-Bold", size=12, leading=16
    )
    y -= 20

    # Texto institucional
    y = _draw_paragraph(c, texto_institucional, 2.5 * cm, y, largura_texto)
    y -= 15
    y, pagina = _verificar_pagina(c, y, pagina)

    # Texto comercial
    y = _draw_paragraph(c, texto_comercial, 2.5 * cm, y, largura_texto)
    y -= 20
    y, pagina = _verificar_pagina(c, y, pagina)

    # Escopo
    y = _draw_paragraph(
        c, "Escopo de Alocação:",
        2.5 * cm, y, largura_texto,
        font="Helvetica-Bold", size=11
    )

    for cargo in cargos:
        y = _draw_paragraph(
            c,
            f"- {cargo['Cargo']} (Quantidade: {cargo['Quantidade']})",
            2.5 * cm,
            y,
            largura_texto
        )
        y, pagina = _verificar_pagina(c, y, pagina)

    # Resumo Comercial
    y -= 20
    y, pagina = _verificar_pagina(c, y, pagina)

    c.setFont("Helvetica-Bold", 11)
    c.drawString(2.5 * cm, y, "Resumo Comercial")
    y -= 10

    c.rect(2.5 * cm, y - 50, largura_texto, 50, stroke=1, fill=0)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(2.5 * cm + 10, y - 20, f"Valor mensal da proposta: {valor_nf}")
    c.drawString(2.5 * cm + 10, y - 38, f"Margem aplicada: {margem}")

    _footer(c, pagina)
    c.save()


# ======================================================
# PDF TÉCNICO
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

    largura_texto = A4[0] - (2 * 2.5 * cm)

    y = _desenhar_cabecalho_padrao(
        c,
        "PROPOSTA TÉCNICA",
        "Memória de Cálculo – Custos, Encargos e Tributos"
    )

    # Cargos
    y = _draw_paragraph(
        c, "1. Custos por Cargo",
        2.5 * cm, y, largura_texto,
        font="Helvetica-Bold", size=11
    )

    for cargo in cargos:
        y = _draw_paragraph(
            c,
            f"{cargo['Cargo']} | Qtd: {cargo['Quantidade']} | "
            f"Salário Base: {cargo['Salário Base']} | "
            f"Custo Unitário: {cargo['Custo Unitário']}",
            2.5 * cm,
            y,
            largura_texto
        )
        y, pagina = _verificar_pagina(c, y, pagina)

    # Encargos CLT
    y -= 20
    y = _draw_paragraph(
        c, "2. Encargos CLT Consolidados",
        2.5 * cm, y, largura_texto,
        font="Helvetica-Bold", size=11
    )

    for nome, valor in clt_detalhado.items():
        y = _draw_paragraph(c, f"{nome}: {valor}", 2.5 * cm, y, largura_texto)
        y, pagina = _verificar_pagina(c, y, pagina)

    # DAS
    y -= 20
    y = _draw_paragraph(
        c, "3. Simples Nacional – DAS",
        2.5 * cm, y, largura_texto,
        font="Helvetica-Bold", size=11
    )

    y = _draw_paragraph(c, f"DAS Total Mensal: {das_total}", 2.5 * cm, y, largura_texto)
    y, pagina = _verificar_pagina(c, y, pagina)

    # DAS detalhado
    y -= 10
    y = _draw_paragraph(
        c, "4. DAS – Detalhamento por Tributo",
        2.5 * cm, y, largura_texto,
        font="Helvetica-Bold", size=11
    )

    for tributo, valor in das_detalhado.items():
        y = _draw_paragraph(c, f"{tributo}: {valor}", 2.5 * cm, y, largura_texto)
        y, pagina = _verificar_pagina(c, y, pagina)

    # Resultado
    y -= 20
    y = _draw_paragraph(
        c, "5. Resultado Final",
        2.5 * cm, y, largura_texto,
        font="Helvetica-Bold", size=11
    )

    y = _draw_paragraph(c, f"Lucro Mensal: {lucro}", 2.5 * cm, y, largura_texto)

    _footer(c, pagina)
    c.save()
