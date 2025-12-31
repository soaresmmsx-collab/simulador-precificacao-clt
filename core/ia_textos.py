from openai import OpenAI

client = OpenAI()

def gerar_texto_comercial(contexto_bruto):
    prompt = f"""
    Gere um texto comercial profissional para uma proposta de prestação de serviços.
    Tom executivo, claro, objetivo e formal.
    Não use jargões técnicos excessivos.
    Não mencione impostos ou valores.

    Contexto fornecido:
    {contexto_bruto}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um especialista em propostas comerciais B2B."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()
