import os

def gerar_texto_comercial(contexto_bruto):
    """
    Gera texto comercial com IA (OpenAI).
    Se a dependência ou a API Key não existirem,
    retorna uma mensagem padrão sem quebrar o app.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return (
            "Texto não gerado automaticamente.\n\n"
            "Motivo: API Key da OpenAI não configurada.\n"
            "Você pode editar este texto manualmente."
        )

    try:
        from openai import OpenAI
    except ImportError:
        return (
            "Texto não gerado automaticamente.\n\n"
            "Motivo: biblioteca OpenAI não instalada no ambiente.\n"
            "Você pode editar este texto manualmente."
        )

    try:
        client = OpenAI(api_key=api_key)

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
                {
                    "role": "system",
                    "content": "Você é um especialista em propostas comerciais B2B."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return (
            "Erro ao gerar texto automaticamente.\n\n"
            f"Detalhes: {str(e)}\n"
            "Você pode editar este texto manualmente."
        )
