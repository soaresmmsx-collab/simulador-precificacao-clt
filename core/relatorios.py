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
    largura, altura = A4

    # LOGO
    c.drawImage(
        logo_path,
        40,
        altura - 100,
        width=120,
        preserveAspectRatio=True,
        mask="auto"
    )

    # CABEÇALHO
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, altura - 60, "PROPOSTA COMERCIAL")

    c.setFont("Helvetica", 10)
    c.drawString(200, altura - 80, f"Cliente: {cliente}")
    c.drawString(200, altura - 95, f"Validade: {validade}")

    y = altura - 140

    # TÍTULO
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, titulo)
    y -= 25

    # DESCRIÇÃO / ESCOPO
    c.setFont("Helvetica", 10)
    for linha in descricao.split("\n"):
        c.drawString(40, y, linha)
        y -= 14

    y -= 20

    # CARGOS
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Escopo de Alocação")
    y -= 18

    c.setFont("Helvetica", 10)
    for cargo in cargos:
        c.drawString(
            40,
            y,
            f"- {cargo['Cargo']} (Quantidade: {cargo['Quantidade']})"
        )
        y -= 14

    y -= 20

    # VALOR
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Condições Comerciais")
    y -= 18

    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Valor mensal da proposta: {valor_nf}")
    y -= 14
    c.drawString(40, y, f"Margem aplicada: {margem}")

    # RODAPÉ
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(
        40,
        40,
        "Proposta elaborada pela J Talent com base em custos reais, encargos legais e regime Simples Nacional."
    )

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
    y = altura - 40

    # TÍTULO
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "PROPOSTA TÉCNICA – MEMÓRIA DE CÁLCULO")
    y -= 30

    # 1. CARGOS
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "1. Custos por Cargo")
    y -= 20

    c.setFont("Helvetica", 9)
    for cargo in cargos:
        c.drawString(
            40,
            y,
            f"{cargo['Cargo']} | Qtd: {cargo['Quantidade']} | "
            f"Salário: {cargo['Salário Base']} | "
            f"Custo Unitário: {cargo['Custo Unitário']}"
        )
        y -= 14

        if y < 80:
            c.showPage()
            y = altura - 40
            c.setFont("Helvetica", 9)

    # 2. CLT
    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "2. Encargos CLT Consolidados")
    y -= 20

    c.setFont("Helvetica", 9)
    for nome, valor in clt_detalhado.items():
        c.drawString(40, y, f"{nome}: {valor}")
        y -= 14

    # 3. DAS TOTAL
    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "3. Simples Nacional – DAS")
    y -= 20

    c.setFont("Helvetica", 9)
    c.drawString(40, y, f"DAS Total Mensal: {das_total}")
    y -= 20

    # 4. DAS DETALHADO
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "4. DAS – Detalhamento por Tributo")
    y -= 20

    c.setFont("Helvetica", 9)
    for tributo, valor in das_detalhado.items():
        c.drawString(40, y, f"{tributo}: {valor}")
        y -= 14

    # 5. RESULTADO
    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "5. Resultado Final")
    y -= 20

    c.setFont("Helvetica", 9)
    c.drawString(40, y, f"Lucro Mensal: {lucro}")

    c.save()

