from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from datetime import date
import os

def draw_paragraph(c, text, x, y, max_width, leading=14):
    textobject = c.beginText()
    textobject.setTextOrigin(x, y)
    textobject.setLeading(leading)

    for line in text.split("\n"):
        words = line.split(" ")
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if stringWidth(test_line, "Helvetica", 10) <= max_width:
                current_line = test_line
            else:
                textobject.textLine(current_line)
                current_line = word + " "

        textobject.textLine(current_line)

    c.drawText(textobject)
    return textobject.getY()

def draw_footer(c, page_number):
    c.setFont("Helvetica-Oblique", 8)
    c.drawRightString(
        A4[0] - 2 * cm,
        1.5 * cm,
        f"Página {page_number}"
    )


def gerar_proposta_comercial_pdf(
    caminho_pdf,
    logo_path,
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

    page = 1
    y = altura - 3 * cm

    # LOGO
    if os.path.exists(logo_path):
        c.drawImage(
            logo_path,
            margem_esq,
            altura - 2.5 * cm,
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
        f"Validade: {validade}"
    )

    y -= 2 * cm

    # TÍTULO
    c.setFont("Helvetica-Bold", 12)
    y = draw_paragraph(c, titulo, margem_esq, y, largura_texto, 16) - 20

    # TEXTO DA PROPOSTA (IA-FRIENDLY)
    c.setFont("Helvetica", 10)
    texto_comercial = (
        f"A J Talent apresenta a presente proposta comercial com o objetivo de "
        f"fornecer profissionais qualificados conforme escopo abaixo descrito.\n\n"
        f"{descricao}\n\n"
        f"A estrutura de custos foi elaborada com base em conformidade legal, "
        f"previsibilidade financeira e sustentabilidade operacional."
    )

    y = draw_paragraph(c, texto_comercial, margem_esq, y, largura_texto)

    # QUEBRA DE PÁGINA
    if y < 5 * cm:
        draw_footer(c, page)
        c.showPage()
        page += 1
        y = altura - 3 * cm

    # ESCOPO
    c.setFont("Helvetica-Bold", 11)
    y -= 20
    y = draw_paragraph(c, "Escopo de Alocação:", margem_esq, y, largura_texto)

    c.setFont("Helvetica", 10)
    for cargo in cargos:
        y = draw_paragraph(
            c,
            f"- {cargo['Cargo']} (Quantidade: {cargo['Quantidade']})",
            margem_esq,
            y,
            largura_texto
        )

    # VALOR
    y -= 20
    c.setFont("Helvetica-Bold", 11)
    y = draw_paragraph(c, "Condições Comerciais:", margem_esq, y, largura_texto)

    c.setFont("Helvetica", 10)
    y = draw_paragraph(
        c,
        f"Valor mensal da proposta: {valor_nf}\n"
        f"Margem aplicada: {margem}",
        margem_esq,
        y,
        largura_texto
    )

    draw_footer(c, page)
    c.save()


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

    page = 1
    y = altura - 3 * cm

    c.setFont("Helvetica-Bold", 14)
    y = draw_paragraph(
        c,
        "PROPOSTA TÉCNICA – MEMÓRIA DE CÁLCULO",
        margem_esq,
        y,
        largura_texto,
        18
    )

    # CARGOS
    c.setFont("Helvetica-Bold", 11)
    y -= 20
    y = draw_paragraph(c, "1. Custos por Cargo", margem_esq, y, largura_texto)

    c.setFont("Helvetica", 9)
    for cargo in cargos:
        texto = (
            f"{cargo['Cargo']} | Qtd: {cargo['Quantidade']} | "
            f"Salário: {cargo['Salário Base']} | "
            f"Custo Unitário: {cargo['Custo Unitário']}"
        )
        y = draw_paragraph(c, texto, margem_esq, y, largura_texto)

        if y < 4 * cm:
            draw_footer(c, page)
            c.showPage()
            page += 1
            y = altura - 3 * cm

    # CLT
    c.setFont("Helvetica-Bold", 11)
    y -= 20
    y = draw_paragraph(c, "2. Encargos CLT Consolidados", margem_esq, y, largura_texto)

    c.setFont("Helvetica", 9)
    for nome, valor in clt_detalhado.items():
        y = draw_paragraph(c, f"{nome}: {valor}", margem_esq, y, largura_texto)

    # DAS
    c.setFont("Helvetica-Bold", 11)
    y -= 20
    y = draw_paragraph(c, "3. Simples Nacional – DAS", margem_esq, y, largura_texto)

    c.setFont("Helvetica", 9)
    y = draw_paragraph(c, f"DAS Total Mensal: {das_total}", margem_esq, y, largura_texto)

    c.setFont("Helvetica-Bold", 11)
    y -= 20
    y = draw_paragraph(c, "4. DAS – Detalhamento por Tributo", margem_esq, y, largura_texto)

    c.setFont("Helvetica", 9)
    for tributo, valor in das_detalhado.items():
        y = draw_paragraph(c, f"{tributo}: {valor}", margem_esq, y, largura_texto)

    # RESULTADO
    c.setFont("Helvetica-Bold", 11)
    y -= 20
    y = draw_paragraph(c, "5. Resultado Final", margem_esq, y, largura_texto)

    c.setFont("Helvetica", 9)
    y = draw_paragraph(c, f"Lucro Mensal: {lucro}", margem_esq, y, largura_texto)

    draw_footer(c, page)
    c.save()


