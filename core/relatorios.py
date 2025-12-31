import os
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader

# -------------------- Helpers --------------------

def _draw_paragraph(c, texto, x, y, largura, font="Helvetica", size=10, leading=14):
    c.setFont(font, size)
    t = c.beginText(x, y)
    t.setLeading(leading)
    for linha in texto.split("\n"):
        palavras = linha.split(" ")
        atual = ""
        for p in palavras:
            teste = atual + p + " "
            if stringWidth(teste, font, size) <= largura:
                atual = teste
            else:
                t.textLine(atual)
                atual = p + " "
        t.textLine(atual)
    c.drawText(t)
    return t.getY()

def _footer(c, pagina):
    c.setFont("Helvetica-Oblique", 8)
    c.drawRightString(A4[0] - 2*cm, 1.5*cm, f"Página {pagina}")

def _nova_pagina(c, pagina):
    _footer(c, pagina)
    c.showPage()
    return A4[1] - 5.5*cm, pagina + 1

# -------------------- Cabeçalho Padrão --------------------

def _cabecalho(c, titulo, subtitulo):
    largura, altura = A4
    margem = 2.5*cm

    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.normpath(os.path.join(base_dir, "..", "assets", "logo.png"))

    # Logo (centralizada verticalmente na faixa do cabeçalho)
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        logo_w = 3.5*cm
        logo_h = 3.5*cm
        topo = altura - 2.2*cm
        base = altura - 3.7*cm
        y_logo = base + ((topo - base - logo_h) / 2)
        c.drawImage(logo, margem, y_logo, width=logo_w, height=logo_h,
                    preserveAspectRatio=True, mask="auto")

    # Título / subtítulo à direita
    c.setFont("Helvetica-Bold", 16)
    c.drawRightString(largura - margem, altura - 2.2*cm, titulo)
    c.setFont("Helvetica", 11)
    c.drawRightString(largura - margem, altura - 2.9*cm, subtitulo)

    # Linha divisória (não passa sob a logo)
    c.setLineWidth(0.6)
    c.line(margem + 4.5*cm, altura - 3.7*cm, largura - margem, altura - 3.7*cm)

    # y inicial seguro do corpo
    return altura - 5.5*cm

# -------------------- PDF COMERCIAL (com Capa Executiva) --------------------

def gerar_proposta_comercial_pdf(
    caminho,
    cliente,
    titulo,
    resumo_executivo,
    texto_institucional,
    texto_comercial,
    validade,
    valor_nf,
    margem,
    cargos
):
    c = canvas.Canvas(caminho, pagesize=A4)
    pagina = 1
    largura_texto = A4[0] - 2*(2.5*cm)

    # --- CAPA EXECUTIVA ---
    y = _cabecalho(c, "PROPOSTA EXECUTIVA", f"{cliente} | Validade: {validade}")

    y = _draw_paragraph(c, titulo, 2.5*cm, y, largura_texto,
                        font="Helvetica-Bold", size=14, leading=18)
    y -= 20
    y = _draw_paragraph(c, resumo_executivo, 2.5*cm, y, largura_texto,
                        font="Helvetica", size=11, leading=16)

    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2.5*cm, y, "Valor mensal da proposta")
    y -= 18
    c.setFont("Helvetica-Bold", 18)
    c.drawString(2.5*cm, y, valor_nf)

    _footer(c, pagina)

    # --- PROPOSTA COMERCIAL ---
    y, pagina = _nova_pagina(c, pagina)
    y = _cabecalho(c, "PROPOSTA COMERCIAL",
                   f"{cliente} | {date.today().strftime('%d/%m/%Y')}")

    y = _draw_paragraph(c, texto_institucional, 2.5*cm, y, largura_texto)
    y -= 15
    y = _draw_paragraph(c, texto_comercial, 2.5*cm, y, largura_texto)
    y -= 20

    c.setFont("Helvetica-Bold", 11)
    c.drawString(2.5*cm, y, "Escopo de Alocação")
    y -= 10
    for cargo in cargos:
        y = _draw_paragraph(
            c,
            f"- {cargo['Cargo']} (Quantidade: {cargo['Quantidade']})",
            2.5*cm, y, largura_texto
        )

    y -= 20
    c.rect(2.5*cm, y-45, largura_texto, 45)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2.5*cm+10, y-20, f"Valor mensal: {valor_nf}")
    c.drawString(2.5*cm+10, y-35, f"Margem aplicada: {margem}")

    _footer(c, pagina)
    c.save()

# -------------------- PDF TÉCNICO --------------------

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
    largura_texto = A4[0] - 2*(2.5*cm)

    y = _cabecalho(c, "PROPOSTA TÉCNICA", "Memória de Cálculo – Custos e Tributos")

    y = _draw_paragraph(c, "1. Custos por Cargo", 2.5*cm, y, largura_texto,
                        font="Helvetica-Bold", size=11)
    for cargo in cargos:
        y = _draw_paragraph(
            c,
            f"{cargo['Cargo']} | Qtd: {cargo['Quantidade']} | "
            f"Salário Base: {cargo['Salário Base']} | "
            f"Custo Unitário: {cargo['Custo Unitário']}",
            2.5*cm, y, largura_texto
        )

    y -= 20
    y = _draw_paragraph(c, "2. Encargos CLT Consolidados", 2.5*cm, y, largura_texto,
                        font="Helvetica-Bold", size=11)
    for nome, valor in clt_detalhado.items():
        y = _draw_paragraph(c, f"{nome}: {valor}", 2.5*cm, y, largura_texto)

    y -= 20
    y = _draw_paragraph(c, "3. Simples Nacional – DAS", 2.5*cm, y, largura_texto,
                        font="Helvetica-Bold", size=11)
    y = _draw_paragraph(c, f"DAS Total Mensal: {das_total}", 2.5*cm, y, largura_texto)

    y -= 10
    y = _draw_paragraph(c, "4. DAS – Detalhamento por Tributo", 2.5*cm, y, largura_texto,
                        font="Helvetica-Bold", size=11)
    for tributo, valor in das_detalhado.items():
        y = _draw_paragraph(c, f"{tributo}: {valor}", 2.5*cm, y, largura_texto)

    y -= 20
    y = _draw_paragraph(c, "5. Resultado Final", 2.5*cm, y, largura_texto,
                        font="Helvetica-Bold", size=11)
    y = _draw_paragraph(c, f"Lucro Mensal: {lucro}", 2.5*cm, y, largura_texto)

    _footer(c, pagina)
    c.save()
