import ollama

# Models
MODEL_TRANSLATOR = "gemma2:2b"
MODEL_MEDICAL = "alibayram/medgemma:latest"

# Create/overwrite evaluation file when program starts
with open(
    "evaluation_results.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write(
        "CEBUANO DOCTOR EVALUATION RESULTS\n"
        "=================================\n\n"
    )


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
        max_tokens=150
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
        max_tokens=700
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
        max_tokens=1000
    )


def save_result(text: str):

    with open(
        "evaluation_results.txt",
        "a",
        encoding="utf-8"
    ) as file:
        file.write(text)


def cebuano_doctor_pipeline(cebuano_prompt: str):

    print("\nProcessing with Gemma and MedGemma...\n")

    try:

        english_query = translate_cebuano_to_english(
            cebuano_prompt
        )

        if not english_query.strip():
            english_query = "[TRANSLATION FAILED]"

        english_response = ""

        if english_query != "[TRANSLATION FAILED]":
            english_response = get_medical_advice(
                english_query
            )

        if not english_response.strip():
            english_response = "[MEDICAL RESPONSE FAILED]"

        cebuano_response = ""

        if english_response != "[MEDICAL RESPONSE FAILED]":
            cebuano_response = translate_english_to_cebuano(
                english_response
            )

        if not cebuano_response.strip():
            cebuano_response = "[CEBUANO TRANSLATION FAILED]"

        result = f"""
============================================================
QUESTION
============================================================
{cebuano_prompt}

[1] English Translation
--------------------------------------------------
{english_query}

[2] Medical Advice
--------------------------------------------------
{english_response}

[3] Final Cebuano Response
--------------------------------------------------
{cebuano_response}

============================================================

"""

        print(result)
        save_result(result)

    except Exception as e:

        error_result = f"""
============================================================
QUESTION
============================================================
{cebuano_prompt}

ERROR:
{str(e)}

============================================================

"""

        print(error_result)
        save_result(error_result)


def main():

    print("==================================================")
    print("           WELCOME TO THE CEBUANO DOCTOR")
    print("==================================================")
    print("Type 'exit' or 'quit' to end.\n")

    while True:

        user_input = input(
            "Pangutana (Cebuano Query): "
        ).strip()

        if not user_input:
            continue

        if user_input.lower() in [
            "exit",
            "quit"
        ]:
            print("\nSalamat!")
            break

        cebuano_doctor_pipeline(user_input)


if __name__ == "__main__":
    main()