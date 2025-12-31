import os
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth


# ======================================================
# FUNÇÕES AUXILIARES DE LAYOUT
# ======================================================

def _draw_paragraph(
    c,
    texto,
    x,
    y,
    largura_max,
    font="Helvetica",
    size=10,
    leading=14
):
    """
    Escreve texto com quebra automática de linha respeitando margem direita.
    Retorna a nova posição Y.
    """
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


def _desenhar_logo(c, x, y, largura_cm=4):
    """
    Desenha a logo usando caminho absoluto baseado no arquivo relatorios.py
    (compatível com Streamlit Cloud)
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_logo = os.path.join(base_dir, "..", "assets", "logo.png")
    caminho_logo = os.path.normpath(caminho_logo)

    if not os.path.exists(caminho_logo):
        raise FileNotFoundError(
            f"Logo não encontrada em: {caminho_logo}"
        )

    c.drawImage(
        caminho_logo,
        x,
        y,
        width=largura_cm * cm,
        preserveAspectRatio=True,
        mask="auto"
    )



# ======================================================
# PDF COMERCIAL (EXECUTIVO)
# ======================================================

def gerar_proposta_comercial_pdf(
    caminho_pdf,
    cliente,
    titulo,
    descricao,
    validade,
    valor_nf,
    margem,
    cargos
):
    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    largura, altura = A4

    margem_esq = 2.5 * cm
    margem_dir = 2.5 * cm
    largura_texto = largura - margem_esq - margem_dir

    pagina = 1
    y = altura - 3 * cm

    # LOGO
    _desenhar_logo(
        c,
        margem_esq,
        altura - 2.8 * cm
    )

    # CABEÇALHO
    c.setFont("Helvetica-Bold", 16)
    c.drawRightString(
        largura - margem_dir,
        altura - 2 * cm,
        "PROPOSTA COMERCIAL"
    )

    c.setFont("Helvetica", 10)
    c.drawRightString(
        largura - margem_dir,
        altura - 2.7 * cm,
        f"Cliente: {cliente}"
    )
    c.drawRightString(
        largura - margem_dir,
        altura - 3.2 * cm,
        f"Data: {date.today().strftime('%d/%m/%Y')} | Validade: {validade}"
    )

    y -= 2 * cm

    # TÍTULO
    y = _draw_paragraph(
        c,
        titulo,
        margem_esq,
        y,
        largura_texto,
        font="Helvetica-Bold",
        size=12,
        leading=16
    ) - 20

    # TEXTO COMERCIAL
    texto_comercial = (
        "A J Talent apresenta a presente proposta comercial com o objetivo de "
        "disponibilizar profissionais qualificados, alinhados às necessidades "
        "do cliente, assegurando conformidade legal, previsibilidade financeira "
        "e excelência operacional.\n\n"
        f"{descricao}\n\n"
        "A estrutura desta proposta foi elaborada com base em custos reais, "
        "encargos legais aplicáveis e margem sustentável, garantindo segurança "
        "jurídica e financeira para ambas as partes."
    )

    y = _draw_paragraph(
        c,
        texto_comercial,
        margem_esq,
        y,
        largura_texto
    )

    # ESCOPO
    y -= 20
    y = _draw_paragraph(
        c,
        "Escopo de Alocação:",
        margem_esq,
        y,
        largura_texto,
        font="Helvetica-Bold",
        size=11
    )

    for cargo in cargos:
        y = _draw_paragraph(
            c,
            f"- {cargo['Cargo']} (Quantidade: {cargo['Quantidade']})",
            margem_esq,
            y,
            largura_texto
        )

    # CONDIÇÕES
    y -= 20
    y = _draw_paragraph(
        c,
        "Condições Comerciais:",
        margem_esq,
        y,
        largura_texto,
        font="Helvetica-Bold",
        size=11
    )

    y = _draw_paragraph(
        c,
        f"Valor mensal da proposta: {valor_nf}\n"
        f"Margem aplicada: {margem}",
        margem_esq,
        y,
        largura_texto
    )

    _footer(c, pagina)
    c.save()


# ======================================================
# PDF TÉCNICO (AUDITÁVEL)
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
    largura, altura = A4

    margem_esq = 2.5 * cm
    margem_dir = 2.5 * cm
    largura_texto = largura - margem_esq - margem_dir

    pagina = 1
    y = altura - 3 * cm

    # LOGO
    _desenhar_logo(
        c,
        margem_esq,
        altura - 2.8 * cm
    )

    # TÍTULO
    y = _draw_paragraph(
        c,
        "PROPOSTA TÉCNICA – MEMÓRIA DE CÁLCULO",
        margem_esq,
        y,
        largura_texto,
        font="Helvetica-Bold",
        size=14,
        leading=18
    )

    # 1. CARGOS
    y -= 20
    y = _draw_paragraph(
        c,
        "1. Custos por Cargo",
        margem_esq,
        y,
        largura_texto,
        font="Helvetica-Bold",
        size=11
    )

    for cargo in cargos:
        texto = (
            f"{cargo['Cargo']} | "
            f"Qtd: {cargo['Quantidade']} | "
            f"Salário Base: {cargo['Salário Base']} | "
            f"Custo Unitário: {cargo['Custo Unitário']}"
        )
        y = _draw_paragraph(
            c,
            texto,
            margem_esq,
            y,
            largura_texto
        )

    # 2. CLT
    y -= 20
    y = _draw_paragraph(
        c,
        "2. Encargos CLT Consolidados",
        margem_esq,
        y,
        largura_texto,
        font="Helvetica-Bold",
        size=11
    )

    for nome, valor in clt_detalhado.items():
        y = _draw_paragraph(
            c,
            f"{nome}: {valor}",
            margem_esq,
            y,
            largura_texto
        )

    # 3. DAS
    y -= 20
    y = _draw_paragraph(
        c,
        "3. Simples Nacional – DAS",
        margem_esq,
        y,
        largura_texto,
        font="Helvetica-Bold",
        size=11
    )

    y = _draw_paragraph(
        c,
        f"DAS Total Mensal: {das_total}",
        margem_esq,
        y,
        largura_texto
    )

    # 4. DAS DETALHADO
    y -= 10
    y = _draw_paragraph(
        c,
        "4. DAS – Detalhamento por Tributo",
        margem_esq,
        y,
        largura_texto,
        font="Helvetica-Bold",
        size=11
    )

    for tributo, valor in das_detalhado.items():
        y = _draw_paragraph(
            c,
            f"{tributo}: {valor}",
            margem_esq,
            y,
            largura_texto
        )

    # 5. RESULTADO
    y -= 20
    y = _draw_paragraph(
        c,
        "5. Resultado Final",
        margem_esq,
        y,
        largura_texto,
        font="Helvetica-Bold",
        size=11
    )

    y = _draw_paragraph(
        c,
        f"Lucro Mensal: {lucro}",
        margem_esq,
        y,
        largura_texto
    )

    _footer(c, pagina)
    c.save()
