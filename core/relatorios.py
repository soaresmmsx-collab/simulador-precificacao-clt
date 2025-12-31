from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


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

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 800, "PROPOSTA COMERCIAL")

    c.setFont("Helvetica", 10)
    c.drawString(50, 770, f"Cliente: {cliente}")
    c.drawString(50, 750, f"Título: {titulo}")
    c.drawString(50, 730, f"Validade: {validade}")
    c.drawString(50, 710, f"Valor mensal: {valor_nf}")

    c.save()


def gerar_pdf_tecnico(
    caminho_pdf,
    cargos,
    clt_detalhado,
    das,
    lucro
):
    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    largura, altura = A4

    y = altura - 40

    # TÍTULO
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "PROPOSTA TÉCNICA – DETALHAMENTO DE CUSTOS")
    y -= 30

    # CARGOS
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "1. Custos por Cargo")
    y -= 20

    c.setFont("Helvetica", 9)
    for cargo in cargos:
        c.drawString(
            40,
            y,
            f"{cargo['Cargo']} | Qtd: {cargo['Quantidade']} | "
            f"Custo Unitário: {cargo['Custo Unitário']}"
        )
        y -= 14

        if y < 80:
            c.showPage()
            y = altura - 40
            c.setFont("Helvetica", 9)

    # CLT DETALHADO
    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "2. Encargos CLT Consolidados")
    y -= 20

    c.setFont("Helvetica", 9)
    for nome, valor in clt_detalhado.items():
        c.drawString(40, y, f"{nome}: {valor}")
        y -= 14

        if y < 80:
            c.showPage()
            y = altura - 40
            c.setFont("Helvetica", 9)

    # DAS
    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "3. Impostos – Simples Nacional (DAS)")
    y -= 20

    c.setFont("Helvetica", 9)
    c.drawString(40, y, f"DAS Total Mensal: {das}")
    y -= 20

    # RESULTADO
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "4. Resultado")
    y -= 20

    c.setFont("Helvetica", 9)
    c.drawString(40, y, f"Lucro Mensal: {lucro}")

    c.save()
