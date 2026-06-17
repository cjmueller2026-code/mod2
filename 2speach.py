import re
import pandas as pd
from collections import Counter
from PyPDF2 import PdfReader

# ----------------------------------
# Hard-code the file location here
# ----------------------------------

pdf_path = r"C:\speach.pdf"

# Example:
# pdf_path = r"C:\Users\Jen\Downloads\full-transcript-of--president-trump-sotu_2026.pdf"

try:

    # Read the PDF
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + " "

    # ----------------------------------
    # Basic Statistics
    # ----------------------------------

    words = re.findall(r"\b[a-zA-Z']+\b", text)

    word_count = len(words)

    character_count = len(text)

    average_word_length = round(
        sum(len(word) for word in words) / word_count,
        2
    )

    # ----------------------------------
    # Sentence Statistics
    # ----------------------------------

    sentences = re.split(r"[.!?]+", text)

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    average_sentence_length = round(
        word_count / len(sentences),
        2
    )

    # ----------------------------------
    # Word Distribution
    # ----------------------------------

    word_frequency = Counter(
        word.lower() for word in words
    )

    word_distribution = (
        pd.DataFrame(
            word_frequency.items(),
            columns=["Word", "Frequency"]
        )
        .sort_values(
            by="Frequency",
            ascending=False
        )
    )

    # ----------------------------------
    # Top 10 Longest Words
    # ----------------------------------

    unique_words = sorted(
        set(words),
        key=len,
        reverse=True
    )

    top_10_longest = unique_words[:10]

    # ----------------------------------
    # Summary Table
    # ----------------------------------

    summary = pd.DataFrame({

        "Metric": [
            "Word Count",
            "Character Count",
            "Average Word Length",
            "Average Sentence Length"
        ],

        "Value": [
            word_count,
            character_count,
            average_word_length,
            average_sentence_length
        ]

    })

    print("\n===== SUMMARY =====")

    print(summary.to_string(index=False))

    print("\n===== WORD DISTRIBUTION (Top 25 Words) =====")

    print(word_distribution.head(25).to_string(index=False))

    print("\n===== TOP 10 LONGEST WORDS =====")

    for i, word in enumerate(top_10_longest, start=1):

        print(f"{i}. {word}")

except FileNotFoundError:

    print("Error: File not found.")

except Exception as e:

    print(f"An error occurred: {e}")