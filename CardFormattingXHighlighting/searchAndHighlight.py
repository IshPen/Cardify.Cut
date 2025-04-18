import re

import win32clipboard as wc
import win32con

rtf_header = r"""{\rtf1\ansi\deff0{\colortbl ;\red204\green255\blue255;}"""  # Light blue highlight
rtf_footer = "}"

def copy_rtf_to_clipboard(rtf_text):
    wc.OpenClipboard()
    wc.EmptyClipboard()
    wc.SetClipboardData(win32con.CF_TEXT, rtf_text.encode('utf-8'))  # Optional plain-text fallback
    wc.SetClipboardData(wc.RegisterClipboardFormat("Rich Text Format"), rtf_text.encode('utf-8'))
    wc.CloseClipboard()

def highlight_extracted_words(sentence, extracted_phrase, beginning_marker, ending_marker):
    # Extract only alphanumeric words from the extracted phrase
    extracted_words = re.findall(r'\w+', extracted_phrase)

    # Escape literal braces only in the sentence, not in tags
    sentence = sentence.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}")

    output = sentence
    offset = 0  # Track how much we've shifted positions due to insertion

    for word in extracted_words:
        pattern = re.compile(rf'\b({re.escape(word)})\b', re.IGNORECASE)
        search_start = offset

        while True:
            match = pattern.search(output, pos=search_start)
            if not match:
                break

            start, end = match.span()

            # Ensure we’re not already inside a highlight group
            before = output[:start]
            if beginning_marker in before and before.rfind(beginning_marker) > before.rfind(ending_marker):
                search_start = end
                continue

            # Replace the matched word with formatting
            tagged = beginning_marker + match.group(0) + ending_marker
            output = output[:start] + tagged + output[end:]

            offset = start + len(tagged)
            break

    return output



if __name__ == "__main__":
    sentence = "Colorado: Marijuana becomes legal in the state for buyers over 21 at a licensed retail dispensary."
    extracted = "Colorado: Marijuana becomes legal in the state for buyers"

    rtf_header = r"{\rtf1\ansi\deff0{\colortbl ;\red204\green255\blue255;}"
    rtf_footer = "}"
    begin = r"{\highlight1\b\ul "
    end = r"}"

    rtf_body = highlight_extracted_words(sentence, extracted, begin, end)
    full_rtf = rtf_header + rtf_body + r"\line " + rtf_footer
    copy_rtf_to_clipboard(full_rtf)
    print("✔️ Copied to clipboard.")
