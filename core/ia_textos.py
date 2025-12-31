import os

CONTEXTO_FARMACEUTICO = """
Você redige propostas comerciais para empresas do setor farmacêutico.
Essas empresas operam sob forte regulação, auditorias frequentes,
exigência rigorosa de conformidade trabalhista, fiscal e tributária,
e ambientes críticos que demandam alta confiabilidade operacional.
"""

def _openai_ok():
    return bool(os.getenv("OPENAI_API_KEY"))

def _fallback(msg):
    return (
        f"{msg}\n\n"
        "Você pode editar este texto manualmente antes de gerar o PDF."
    )

def gerar_resumo_executivo(contexto, tom):
    if not _openai_ok():
        return _fallback("Resumo executivo não gerado automaticamente (API Key ausente).")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = f"""
        {CONTEXTO_FARMACEUTICO}

        Gere um RESUMO EXECUTIVO curto (5–7 linhas).
        Tom: {tom}.
        Linguagem estratégica, clara e objetiva.
        Não mencionar impostos nem cálculos.

        Contexto:
        {contexto}
        """
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"Você é um consultor executivo sênior."},
                {"role":"user","content":prompt}
            ],
            temperature=0.3
        )
        return r.choices[0].message.content.strip()
    except Exception as e:
        return _fallback(f"Erro ao gerar resumo executivo: {e}")

def gerar_texto_comercial(contexto, tom):
    if not _openai_ok():
        return _fallback("Texto comercial não gerado automaticamente (API Key ausente).")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = f"""
        {CONTEXTO_FARMACEUTICO}

        Gere um TEXTO COMERCIAL para proposta B2B.
        Tom: {tom}.
        Público: compras, jurídico e gestão.
        Enfatizar previsibilidade financeira, mitigação de riscos,
        conformidade regulatória e eficiência operacional.
        Não detalhar cálculos.

        Contexto:
        {contexto}
        """
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"Você é um especialista em propostas B2B."},
                {"role":"user","content":prompt}
            ],
            temperature=0.4
        )
        return r.choices[0].message.content.strip()
    except Exception as e:
        return _fallback(f"Erro ao gerar texto comercial: {e}")
