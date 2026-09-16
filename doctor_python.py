import ollama

# Smaller and more stable translator for your hardware
MODEL_TRANSLATOR = "gemma2:2b"
MODEL_MEDICAL = "alibayram/medgemma:latest"


def generate_llm_response(
    model_name: str,
    prompt: str,
    max_tokens: int = 500
):
    response = ollama.chat(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        keep_alive=0,
        options={
            "temperature": 0.2,
            "num_predict": max_tokens
        }
    )

    return response["message"]["content"].strip()


def translate_cebuano_to_english(cebuano_text: str):
    prompt = f"""
Translate the following Cebuano healthcare question into English.

Output ONLY the English translation.

Cebuano:
{cebuano_text}

English:
"""

    return generate_llm_response(
        MODEL_TRANSLATOR,
        prompt,
        max_tokens=100
    )


def get_medical_advice(english_query: str):
    prompt = f"""
You are a medical information assistant.

Provide:
- General medical information
- Possible causes
- Self-care recommendations
- When to seek medical attention

Do not claim certainty.
Do not replace a licensed physician.

Patient Question:
{english_query}
"""

    return generate_llm_response(
        MODEL_MEDICAL,
        prompt,
        max_tokens=600
    )


def translate_english_to_cebuano(english_text: str):
    prompt = f"""
Translate the following English medical response into natural Cebuano.

Do not summarize.
Preserve all information.

English:
{english_text}

Cebuano:
"""

    return generate_llm_response(
        MODEL_TRANSLATOR,
        prompt,
        max_tokens=800
    )


def cebuano_doctor_pipeline(cebuano_prompt: str):

    print("\nProcessing with Gemma and MedGemma...\n")

    try:

        english_query = translate_cebuano_to_english(
            cebuano_prompt
        )

        print("[1] English Translation")
        print("-" * 50)
        print(english_query)
        print()

        if not english_query.strip():
            print("[ERROR] Translation failed.")
            return

        english_response = get_medical_advice(
            english_query
        )

        print("[2] Medical Advice")
        print("-" * 50)
        print(english_response)
        print()

        if not english_response.strip():
            print("[ERROR] Medical response failed.")
            return

        cebuano_response = translate_english_to_cebuano(
            english_response
        )

        print("[3] Final Cebuano Response")
        print("-" * 50)
        print(cebuano_response)
        print()

        if not cebuano_response.strip():
            print("[WARNING] Cebuano translation incomplete.")

        print("=" * 60)

    except Exception as e:
        print(f"\nERROR: {e}\n")


def main():

    print("==================================================")
    print("           WELCOME TO THE CEBUANO DOCTOR")
    print("==================================================")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input(
            "Pangutana (Cebuano Query): "
        ).strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("\nSalamat!")
            break

        cebuano_doctor_pipeline(user_input)


if __name__ == "__main__":
    main()