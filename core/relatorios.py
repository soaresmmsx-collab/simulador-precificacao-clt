import base64
import tempfile
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth


# ======================================================
# LOGO EMBUTIDA (BASE64)
# ======================================================
LOGO_BASE64 = """
COLE_AQUI_SUA_LOGO_BASE64
"""


def _criar_logo_temp():
    if not LOGO_BASE64.strip():
        return None

    try:
        logo_bytes = base64.b64decode(LOGO_BASE64)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        tmp.write(logo_bytes)
        tmp.close()
        return tmp.name
    except Exception:
        return None


# ======================================================
# FUNÇÕES DE LAYOUT
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


# ======================================================
# PDF COMERCIAL
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
    logo = _criar_logo_temp()
    if logo:
        c.drawImage(
            logo,
            margem_esq,
            altura - 2.8 * cm,
            width=4 * cm,
            preserveAspectRatio=True,
            mask="auto"
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
        c, titulo, margem_esq, y, largura_texto,
        font="Helvetica-Bold", size=12, leading=16
    ) - 20

    # TEXTO COMERCIAL
    texto = (
        "A J Talent apresenta a presente proposta comercial visando fornecer "
        "profissionais qualificados, com conformidade legal, previsibilidade "
        "financeira e excelência operacional.\n\n"
        f"{descricao}\n\n"
        "A precificação considera custos reais, encargos legais e margem sustentável."
    )

    y = _draw_paragraph(c, texto, margem_esq, y, largura_texto)

    # ESCOPO
    y -= 20
    y = _draw_paragraph(
        c, "Escopo de Alocação:",
        margem_esq, y, largura_texto,
        font="Helvetica-Bold", size=11
    )

    for cargo in cargos:
        y = _draw_paragraph(
            c,
            f"- {cargo['Cargo']} (Quantidade: {cargo['Quantidade']})",
            margem_esq, y, largura_texto
        )

    # VALOR
    y -= 20
    y = _draw_paragraph(
        c, "Condições Comerciais:",
        margem_esq, y, largura_texto,
        font="Helvetica-Bold", size=11
    )

    y = _draw_paragraph(
        c,
        f"Valor mensal da proposta: {valor_nf}\nMargem aplicada: {margem}",
        margem_esq, y, largura_texto
    )

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
    largura, altura = A4

    margem_esq = 2.5 * cm
    margem_dir = 2.5 * cm
    largura_texto = largura - margem_esq - margem_dir

    pagina = 1
    y = altura - 3 * cm

    # LOGO
    logo = _criar_logo_temp()
    if logo:
        c.drawImage(
            logo,
            margem_esq,
            altura - 2.8 * cm,
            width=4 * cm,
            preserveAspectRatio=True,
            mask="auto"
        )

    # TÍTULO
    y = _draw_paragraph(
        c,
        "PROPOSTA TÉCNICA – MEMÓRIA DE CÁLCULO",
        margem_esq, y, largura_texto,
        font="Helvetica-Bold", size=14, leading=18
    )

    # CARGOS
    y -= 20
    y = _draw_paragraph(
        c, "1. Custos por Cargo",
        margem_esq, y, largura_texto,
        font="Helvetica-Bold", size=11
    )

    for cargo in cargos:
        y = _draw_paragraph(
            c,
            f"{cargo['Cargo']} | Qtd: {cargo['Quantidade']} | "
            f"Salário Base: {cargo['Salário Base']} | "
            f"Custo Unitário: {cargo['Custo Unitário']}",
            margem_esq, y, largura_texto
        )

    # CLT
    y -= 20
    y = _draw_paragraph(
        c, "2. Encargos CLT Consolidados",
        margem_esq, y, largura_texto,
        font="Helvetica-Bold", size=11
    )

    for nome, valor in clt_detalhado.items():
        y = _draw_paragraph(c, f"{nome}: {valor}", margem_esq, y, largura_texto)

    # DAS
    y -= 20
    y = _draw_paragraph(
        c, "3. Simples Nacional – DAS",
        margem_esq, y, largura_texto,
        font="Helvetica-Bold", size=11
    )

    y = _draw_paragraph(c, f"DAS Total Mensal: {das_total}", margem_esq, y, largura_texto)

    y -= 10
    y = _draw_paragraph(
        c, "4. DAS – Detalhamento por Tributo",
        margem_esq, y, largura_texto,
        font="Helvetica-Bold", size=11
    )

    for tributo, valor in das_detalhado.items():
        y = _draw_paragraph(c, f"{tributo}: {valor}", margem_esq, y, largura_texto)

    # RESULTADO
    y -= 20
    y = _draw_paragraph(
        c, "5. Resultado Final",
        margem_esq, y, largura_texto,
        font="Helvetica-Bold", size=11
    )

    y = _draw_paragraph(c, f"Lucro Mensal: {lucro}", margem_esq, y, largura_texto)

    _footer(c, pagina)
    c.save()
