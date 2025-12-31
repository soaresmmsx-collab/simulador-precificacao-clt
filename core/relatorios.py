from jinja2 import Template
from weasyprint import HTML

def gerar_pdf(template_html, dados, nome):
    html = Template(template_html).render(dados)
    HTML(string=html).write_pdf(nome)
