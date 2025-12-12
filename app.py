import streamlit as st
import PyPDF2
import nltk
import re
from nltk.tokenize import sent_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nltk.download("punkt")

st.title("Keyword-Based Paragraph Extractor & WordCloud Generator")
st.write("Upload a PDF and enter multiple keywords to extract paragraphs and generate a wordcloud.")


# FILE UPLOAD

uploaded_file = st.file_uploader("Upload Annual Report PDF", type=["pdf"])
keywords_input = st.text_input("Enter keywords (comma-separated):")

if uploaded_file and keywords_input:

 
    # READ PDF

    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        try:
            text += page.extract_text() + " "
        except:
            continue

# CLEAN KEYWORDS

    keywords = [k.strip().lower() for k in keywords_input.split(",")]


# SENTENCE TOKENIZE

    sentences = sent_tokenize(text)


# EXTRACT PARAGRAPHS WITH KEYWORDS

    extracted_sentences = []
    for s in sentences:
        s_clean = s.lower()
        if any(k in s_clean for k in keywords):
            extracted_sentences.append(s)

    st.subheader("Extracted Paragraphs:")

    if len(extracted_sentences) == 0:
        st.warning("No paragraphs found containing the specified keywords.")
    else:
        for para in extracted_sentences:
            st.write("• " + para)


# WORDCLOUD FROM EXTRACTED TEXT

        extracted_text_joined = " ".join(extracted_sentences)

        # clean text for wordcloud
        extracted_text_clean = re.sub(r"[^a-zA-Z\s]", "", extracted_text_joined)

        wc = WordCloud(width=800, height=400).generate(extracted_text_clean)

        st.subheader("WordCloud Generated from Extracted Paragraphs")
        fig, ax = plt.subplots()
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
        