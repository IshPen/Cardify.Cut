import re

def highlight_extracted_words(sentence, extracted_phrase):
    # Extract pure words from the phrase (ignores punctuation)
    extracted_words = re.findall(r'\w+', extracted_phrase)
    output = sentence
    offset = 0  # How far we've modified the sentence due to inserted tags

    for word in extracted_words:
        # Match the word as a whole word, case-insensitive
        pattern = re.compile(rf'\b({re.escape(word)})\b', re.IGNORECASE)

        search_start = offset
        while True:
            match = pattern.search(output, pos=search_start)
            if not match:
                break

            start, end = match.span()

            # Avoid tagging inside an already-tagged region
            before = output[:start]
            if '<' in before and before.rfind('<') > before.rfind('>'):
                search_start = end
                continue

            # Insert highlight
            tagged = f"<{match.group(0)}>"
            output = output[:start] + tagged + output[end:]

            # Move offset forward to continue after this tagged word
            offset = start + len(tagged)
            break

    return output

sentence = ("Colorado: Marijuana becomes legal in the state for buyers over 21 at a licensed retail dispensary.")
extracted = "Colorado: Marijuana becomes legal in the state for buyers over 21 at a licensed retail dispensary.\n\n"

print(highlight_extracted_words(sentence, extracted))
