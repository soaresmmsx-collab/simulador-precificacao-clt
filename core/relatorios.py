from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def gerar_pdf_comercial(caminho, valor_nf, margem, cargos):
    c = canvas.Canvas(caminho, pagesize=A4)
    w, h = A4

    y = h - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "PROPOSTA COMERCIAL")
    y -= 40

    c.setFont("Helvetica", 11)
    c.drawString(40, y, f"Valor mensal da proposta: {valor_nf}")
    y -= 20
    c.drawString(40, y, f"Margem aplicada: {margem}")
    y -= 30

    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Cargos:")
    y -= 20

    c.setFont("Helvetica", 10)
    for cargo in cargos:
        c.drawString(
            40,
            y,
            f"- {cargo['Cargo']} | Qtd: {cargo['Quantidade']}"
        )
        y -= 15

    c.save()


def gerar_pdf_tecnico(caminho, cargos, clt, das, lucro):
    c = canvas.Canvas(caminho, pagesize=A4)
    w, h = A4

    y = h - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "PROPOSTA TÉCNICA")
    y -= 40

    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Custos por cargo:")
    y -= 20

    c.setFont("Helvetica", 9)
    for cargo in cargos:
        c.drawString(
            40,
            y,
            f"{cargo['Cargo']} | Custo Unit.: {cargo['Custo Unitário']}"
        )
        y -= 14

    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Encargos CLT Consolidados:")
    y -= 20

    c.setFont("Helvetica", 9)
    for nome, valor in clt.items():
        c.drawString(40, y, f"{nome}: {valor}")
        y -= 14

    y -= 20
    c.drawString(40, y, f"DAS mensal: {das}")
    y -= 14
    c.drawString(40, y, f"Lucro mensal: {lucro}")

    c.save()
