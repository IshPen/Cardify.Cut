import subprocess
import nltk
from nltk.tokenize import sent_tokenize

# Download sentence tokenizer model (only once)
nltk.download('punkt')


def split_into_sentences(text):
    return sent_tokenize(text)


def build_sentence_prompt(sentence, argument):
    return f"""
You are helping a high school debater cut evidence cards.

Read the sentence below. If it supports the following argument, return the sentence **exactly as it is**. If it does not, return nothing.

Argument: {argument}

Sentence: {sentence}
"""


def run_ollama_mistral(prompt):
    ollama_path = r"C:\Users\ishpe\AppData\Local\Programs\Ollama\ollama.exe"
    result = subprocess.run(
        [ollama_path, "ollama", "run", "mistral"],
        input=prompt.encode("utf-8"),
        capture_output=True
    )
    return result.stdout.decode().strip()


def extract_evidence_agentically(article, argument):
    sentences = split_into_sentences(article)
    highlighted = []

    print(f"\nProcessing {len(sentences)} sentences...\n")

    for i, sentence in enumerate(sentences, 1):
        print(f"Analyzing sentence {i}/{len(sentences)}")
        prompt = build_sentence_prompt(sentence, argument)
        result = run_ollama_mistral(prompt)
        if result and sentence in result:
            highlighted.append(f"**{sentence}**")

    return "\n\n".join(highlighted)


def main():
    print("🧠 Debate Evidence Cutter (Agentic Mistral Edition)")
    print("--------------------------------------------------")

    argument = input("Enter the argument you're cutting for: ").strip()
    print("\nPaste the article (press Enter twice to end input):")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    article = "\n".join(lines)
    print("\n⏳ Running Mistral on your article...\n")

    cut_card = extract_evidence_agentically(article, argument)

    print("\n✅ Cut Card:\n")
    print(cut_card if cut_card else "⚠️ No supporting sentences were found.")


if __name__ == "__main__":
    main()
