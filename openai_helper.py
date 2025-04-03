import openai
import os

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_response(contexte_patient, question):
    prompt = (
        f"Voici le contexte d’un patient en rééducation :\n"
        f"{contexte_patient}\n\n"
        f"Le patient pose la question suivante :\n"
        f"{question}\n\n"
        f"Réponds de manière professionnelle, bienveillante et claire. Tu es un assistant kinésithérapeute."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )
    return response.choices[0].message.content