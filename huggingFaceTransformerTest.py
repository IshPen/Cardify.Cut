from transformers import pipeline
import re


# Step 1: Define the function to process the text using a Hugging Face model
def cut_evidence_hf(raw_text: str, search_criteria: str) -> str:
    """
    This function processes the raw text using a Hugging Face model and applies formatting
    (bold/underline) to highlight the most important evidence based on search criteria.
    """

    # Step 2: Load a Hugging Face pipeline for text classification or feature extraction
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")  # You can change this model

    # Step 3: Generate a summary (or extractive key points) from the raw text
    summary = summarizer(raw_text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']

    # Step 4: Highlight important sections using the search criteria
    # We can do this by matching the search criteria within the text and applying formatting
    highlighted_text = highlight_text(summary, search_criteria)

    return highlighted_text


def highlight_text(text: str, search_criteria: str) -> str:
    """
    Highlights key phrases in the text that match the search criteria.
    Matches keywords and applies bold and underline formatting.
    """
    keywords = search_criteria.split()

    # Step 5: Apply formatting to the summary text based on the keywords
    for keyword in keywords:
        # Use regex to find and replace with bold and underline formatting
        text = re.sub(f"(?i)\\b({keyword})\\b", r"**\1**", text)  # Bolds the keyword in the text

    return text


# Example Usage:
raw_text_input = """
In the current political climate, it is important to consider the impacts of economic sanctions on
global markets. Studies have shown that sanctions can destabilize economies, particularly in 
developing nations. Additionally, there is evidence that sanctions rarely achieve their intended 
outcomes and can lead to unforeseen consequences.
"""
search_criteria_input = "economic sanctions outcomes"

formatted_text = cut_evidence_hf(raw_text_input, search_criteria_input)

# Output the formatted text, which should have bolded and highlighted sections
print(formatted_text)
