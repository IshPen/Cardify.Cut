import subprocess
import textwrap

text_1 = f"""
You are a debate coach helping students cut cards from articles.
As you're reading through the article text provided, output the most important phrases/words from the article VERBATIM verbatim from the text as you read it that matches with the argument. It has to make sense. 
"""
text_2 = f"""
You are helping a high school debater cut evidence cards.

Read the article sentence below. If it supports the provided argument below it, return the sentence **exactly as it is**. If it does not, return the text "NOTHING". Do not summarize or explain. Return text verbatim from the provided article.
"""


def build_verbatim_prompt(article_text, argument):
    global text_2
    return text_2 + f"""
    Article: {article_text} 
    My argument: {argument}"""


def cut_evidence_with_ollama(article_text, argument_prompt):
    ollama_path = r"C:\Users\ishpe\AppData\Local\Programs\Ollama\ollama.exe"
    full_prompt = build_verbatim_prompt(article_text, argument_prompt)
    print("\nSending to Mistral...\n--")
    result = subprocess.run(
        [ollama_path, "run", "mistral"],
        input=full_prompt.encode("utf-8"),
        capture_output=True
    )
    return result.stdout.decode("utf-8")


def display_card(citation, highlighted_text):
    # print("=" * 80)
    print(f"\033[1m{citation}\033[0m\n")  # bold citation
    print(highlighted_text)
    print("=" * 80)


if __name__ == "__main__":
    # ⬇️ Sample input (replace with article text from Step 1)
    sample_text = open(rf"C:\Users\ishpe\PycharmProjects\MISC_PROJECTS\Cardify.Cut\MistralCardCutting\sample_article.txt", encoding="utf-8").read()
    print(sample_text)
    # ⬇️ What argument are you trying to support?
    argument = "marijuana legalized"

    # ⬇️ Manually set citation for now
    citation = "Jarrod Tudor — Compulsory Licensing in the European Union — George Mason Journal of International Commercial Law — 2012"

    output_sentences = []

    for sentence in sample_text.split("\n"):
        print(sentence)
        highlighted = cut_evidence_with_ollama(sentence, argument)
        output_sentences.append([highlighted])
        display_card(citation, highlighted)

    for i, o in enumerate(output_sentences): print(o)