import os

CONTEXTO_FARMACEUTICO = """
Você redige propostas comerciais para empresas do setor farmacêutico.
Essas empresas operam sob forte regulação, auditorias frequentes,
exigência rigorosa de conformidade trabalhista, fiscal e tributária,
e ambientes críticos que demandam alta confiabilidade operacional.
"""

def _openai_disponivel():
    return os.getenv("OPENAI_API_KEY") is not None


def gerar_resumo_executivo(contexto, tom):
    if not _openai_disponivel():
        return (
            "Resumo executivo não gerado automaticamente. "
            "Motivo: API Key da OpenAI não configurada."
        )

    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""
        {CONTEXTO_FARMACEUTICO}

        Gere um RESUMO EXECUTIVO curto (5 a 7 linhas) para uma proposta comercial.
        Tom: {tom}.
        Linguagem estratégica, clara e objetiva.
        Não mencionar valores detalhados nem impostos.

        Contexto da proposta:
        {contexto}
        """

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um consultor executivo sênior."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return resp.choices[0].message.content.strip()

    except Exception as e:
        return f"Erro ao gerar resumo executivo: {str(e)}"


def gerar_texto_comercial(contexto, tom):
    if not _openai_disponivel():
        return (
            "Texto comercial não gerado automaticamente. "
            "Motivo: API Key da OpenAI não configurada."
        )

    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""
        {CONTEXTO_FARMACEUTICO}

        Gere um TEXTO COMERCIAL para proposta de prestação de serviços.
        Tom: {tom}.
        Público: áreas de compras, jurídico e gestão.
        Enfatizar previsibilidade financeira, mitigação de riscos,
        conformidade regulatória e eficiência operacional.
        Não detalhar cálculos.

        Contexto da proposta:
        {contexto}
        """

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um especialista em propostas B2B."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        return resp.choices[0].message.content.strip()

    except Exception as e:
        return f"Erro ao gerar texto comercial: {str(e)}"
