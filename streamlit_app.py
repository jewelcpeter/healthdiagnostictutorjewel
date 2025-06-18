import streamlit as st
import os
#Spacy setup
try:
    nlp = spacy.load("en_core_sci_sm")
except:
    os.system("python -m pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_sm-0.4.0.tar.gz")
    import importlib
    importlib.invalidate_caches()
    nlp = spacy.load("en_core_sci_sm")

<<<<<<< HEAD
=======
# spaCy setup
try:
    import scispacy
    import en_core_sci_sm
    nlp = en_core_sci_sm.load()
except:
    import spacy
    nlp = spacy.load("en_core_web_sm")
>>>>>>> 1a94bab (Initial commit)

# Load transformer classifier safely
with st.spinner("Loading AI model..."):
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

        tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")
        model = AutoModelForSequenceClassification.from_pretrained("facebook/bart-large-mnli")
        model = model.to("cpu")  # Move model explicitly to CPU to avoid meta tensor error
        classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer, device=-1)
    except Exception as e:
        st.error(f"🚨 Failed to load AI model: {e}")
        st.stop()

# Streamlit page settings
st.set_page_config(page_title="🩺 AI Health Literacy Tutor", layout="centered")
st.title("🧠 MediLens: AI Symptom Explorer")

# Disclaimer
st.markdown(
    "> ⚠️ **Disclaimer:** This app does **not provide medical or scientific advice**. "
    "It is for educational and exploratory purposes only. The results are AI-generated **hypotheses**, "
    "not professional guidance or diagnosis."
)
user_agrees = st.checkbox("I understand this is NOT medical or scientific advice and agree to continue.")

# Input section
st.markdown("Enter a symptom or health case description. Get simplified insights.")
user_input = st.text_area("🔍 Enter symptoms or medical text:")

if st.button("Analyze"):
    if not user_agrees:
        st.warning("Please check the box to acknowledge the disclaimer before continuing.")
    elif not user_input.strip():
        st.warning("Please enter something.")
    else:
        doc = nlp(user_input)

        # Entities
        st.subheader("🧠 Key Entities:")
        ents = [(ent.text, ent.label_) for ent in doc.ents]
        if ents:
            for word, label in ents:
                st.markdown(f"- **{word}** _(label: {label})_")
        else:
            st.write("No clear medical terms found.")

        # Keywords
        st.subheader("📖 Simplified Terms:")
        simple_terms = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ"] and not token.is_stop]
        st.write(", ".join(simple_terms))

        # Zero-shot prediction
        st.subheader("🧭 Possible Medical Categories (AI Guess):")
        labels = [
            "cardiac issue", "infection", "neurological problem",
            "autoimmune disease", "emergency", "routine checkup"
        ]
        result = classifier(user_input, candidate_labels=labels)
        for label, score in zip(result["labels"], result["scores"]):
            st.write(f"**{label}** — {round(score * 100, 2)}%")

# Final reminder
st.markdown("---")
st.markdown(
    "🛑 **Reminder:** Always consult a licensed healthcare provider for health-related decisions. "
    "This app is not a substitute for professional care."
)
