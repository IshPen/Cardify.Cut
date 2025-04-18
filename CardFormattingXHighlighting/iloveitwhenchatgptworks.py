import re
import pyperclip

formatted_rtf = r"""{\rtf1\ansi\deff0{\colortbl ;\red0\green112\blue192;}"""  # light blue highlight

formatted_rtf += "\n"

# Simulated data
# Replace these with your actual inputs
mistral_output = [["Marijuana legalization in Colorado", "tag"]]
sample_text = "Some 40,000 measures taking effect range from sweeping, national mandates under Obamacare to Marijuana legalization in Colorado, drone prohibition in Illinois and transgender protections in California."

# ========================
# BUILDING THE RTF OUTPUT
# ========================
for i, (highlighted_text, article_sentence) in enumerate(zip(mistral_output, sample_text.split("\n"))):
    highlighted_text = highlighted_text[0].replace("\"", "")

    if highlighted_text.startswith("NOTHING") or not highlighted_text.strip():
        formatted_rtf += article_sentence + r"\line "
        continue

    # Get words to highlight
    mistral_words = highlighted_text.split()


    def highlight_word(match):
        word = match.group(0)
        return r"{\highlight1\b\ul " + word + "}"


    # Build a pattern that matches whole words only
    for mistral_word in mistral_words:
        pattern = rf"\b{re.escape(mistral_word)}\b"
        article_sentence = re.sub(pattern, highlight_word, article_sentence, flags=re.IGNORECASE)

    formatted_rtf += article_sentence + r"\line "

formatted_rtf += "}"

# ========================
# COPY TO CLIPBOARD
# ========================
pyperclip.copy(formatted_rtf)
print("Formatted card copied to clipboard! Paste it into Word.")
