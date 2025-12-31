from jinja2 import Template
from weasyprint import HTML

def gerar_pdf(template_path, contexto, output_path):
    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())

    html = template.render(contexto)
    HTML(string=html).write_pdf(output_path)
