from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import date

from assets.texto_institucional import TEXTO_J_TALENT


def gerar_proposta_comercial_pdf(
    caminho_pdf: str,
    logo_path: str,
    cliente: str,
    titulo: str,
    descricao: str,
    validade: str,
    valor_nf: str,
    margem: str,
    cargos: list
):
    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    largura, altura = A4

    # LOGO
    c.drawImage(
        logo_path,
        2 * cm,
        altura - 3 * cm,
        width=4 * cm,
        preserveAspectRatio=True,
        mask="auto"
    )

    # CABEÇALHO
    c.setFont("Helvetica-Bold", 16)
    c.drawString(7 * cm, altura - 2 * cm, "PROPOSTA COMERCIAL")

    c.setFont("Helvetica", 10)
    c.drawString(7 * cm, altura - 2.7 * cm, f"Cliente: {cliente}")
    c.drawString(
        7 * cm,
        altura - 3.2 * cm,
        f"Data: {date.today().strftime('%d/%m/%Y')}"
    )
    c.drawString(7 * cm, altura - 3.7 * cm, f"Validade: {validade}")

    y = altura - 5 * cm

    # TÍTULO
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, titulo)
    y -= 1 * cm

    # DESCRIÇÃO
    c.setFont("Helvetica", 10)
    for linha in descricao.split("\n"):
        c.drawString(2 * cm, y, linha)
        y -= 0.45 * cm

    y -= 0.8 * cm

    # TEXTO INSTITUCIONAL
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2 * cm, y, "Sobre a J Talent")
    y -= 0.6 * cm

    c.setFont("Helvetica", 9.5)
    for linha in TEXTO_J_TALENT.split("\n"):
        c.drawString(2 * cm, y, linha)
        y -= 0.4 * cm

    y -= 0.8 * cm

    # ESCOPO
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2 * cm, y, "Escopo da Proposta")
    y -= 0.6 * cm

    c.setFont("Helvetica", 10)
    for cargo in cargos:
        c.drawString(
            2 * cm,
            y,
            f"- {cargo['Cargo']} (Quantidade: {cargo['Quantidade']})"
        )
        y -= 0.45 * cm

    y -= 0.8 * cm

    # VALORES
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2 * cm, y, "Condições Comerciais")
    y -= 0.6 * cm

    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, y, f"Valor mensal da proposta: {valor_nf}")
    y -= 0.45 * cm
    c.drawString(2 * cm, y, f"Margem aplicada: {margem}")

    # RODAPÉ
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(
        2 * cm,
        1.5 * cm,
        "Proposta elaborada com base em custos reais, encargos legais e regime Simples Nacional."
    )

    c.save()


def gerar_pdf_tecnico(
    caminho_pdf: str,
    cargos: list,
    clt_detalhado: dict,
    das: str,
    lucro: str
):
    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    largura, altura = A4

    y = altura - 2 * cm

    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, y, "PROPOSTA TÉCNICA")
    y -= 1 * cm

    c.setFont("Helvetica-Bold", 11)
    c.drawString(2 * cm, y, "Custos por cargo")
    y -= 0.7 * cm

    c.setFont("Helvetica", 9)
    for cargo in cargos:
        c.drawString(
            2 * cm,
            y,
            f"{cargo['Cargo']} | Custo Unitário: {cargo['Custo Unitário']}"
        )
        y -= 0.45 * cm

    y -= 0.8 * cm

    c.setFont("Helvetica-Bold", 11)
    c.drawString(2 * cm, y, "Encargos CLT Consolidados")
    y -= 0.7 * cm

    c.setFont("Helvetica", 9)
    for nome, valor in clt_detalhado.items():
        c.drawString(2 * cm, y,*
