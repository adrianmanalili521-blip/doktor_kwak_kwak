from doctor_python import cebuano_doctor_pipeline

test_questions = [
    "Dok, hilantan ko ug duha ka adlaw ug sakit akong ulo. Unsay posible nga hinungdan ani?",
    "Sige ko ug ubo ug sip-on sulod na sa usa ka semana. Usahay lisod pud ko'g ginhawa labi na kung gabii. Kinahanglan ba ko magpakonsulta?",
    "Nakasinati ko ug kalibanga ug pagsuka sukad kagabii. Unsay akong buhaton aron malikayan ang dehydration?",
    "Taas pirmi akong blood pressure bisan nag-inom ko ug tambal. Unsay mga posibleng rason nganong dili kini mokunhod?",
    "Ako nga 58 anyos adunay diabetes. Sulod sa duha ka adlaw nakabantay ko nga dali ko kapuyon, usahay malipong, ug adunay gamay nga kasakit sa akong dughan kung maglakaw ko. Unsay angay nakong buhaton?"
]

print("=" * 60)
print("CEBUANO DOCTOR AUTOMATED EVALUATION")
print("=" * 60)

for i, question in enumerate(test_questions, start=1):
    print(f"\nTEST CASE #{i}")
    print(f"QUESTION: {question}")
    print("-" * 60)

    try:
        cebuano_doctor_pipeline(question)
    except Exception as e:
        print(f"Error: {e}")

print("\nEvaluation completed.")