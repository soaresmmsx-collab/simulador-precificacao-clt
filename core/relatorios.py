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

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 800, "PROPOSTA TÉCNICA")

    y = 770
    c.setFont("Helvetica", 9)

    for cargo in cargos:
        c.drawString(
            50,
            y,
            f"{cargo['Cargo']} | Custo Unitário: {cargo['Custo Unitário']}"
        )
        y -= 15

    c.drawString(50, y - 20, f"DAS: {das}")
    c.drawString(50, y - 40, f"Lucro: {lucro}")

    c.save()
