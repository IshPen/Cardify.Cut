import re
import win32clipboard as wc
import win32con

def copy_rtf_to_clipboard(rtf_text):
    wc.OpenClipboard()
    wc.EmptyClipboard()
    wc.SetClipboardData(win32con.CF_TEXT, rtf_text.encode('utf-8'))  # Optional plain-text fallback
    wc.SetClipboardData(wc.RegisterClipboardFormat("Rich Text Format"), rtf_text.encode('utf-8'))
    wc.CloseClipboard()

# Sample article and highlights
article_sentence = "Some 40,000 measures taking effect range from sweeping, national mandates under Obamacare to Marijuana legalization in Colorado."
highlighted_words = ["Marijuana", "legalization", "in", "Colorado"]

# RTF header with light blue added as first color in table
# Highlighting uses the *background* color index
rtf_header = r"""{\rtf1\ansi\deff0{\colortbl ;\red204\green255\blue255;}"""  # Light blue highlight
rtf_footer = "}"

# Format article_sentence: bold, underline, *highlight* in light blue
for word in highlighted_words:
    pattern = rf"\b{re.escape(word)}\b"
    replacement = r"{\\highlight1\\b\\ul " + word + r"}"
    article_sentence = re.sub(pattern, replacement, article_sentence, flags=re.IGNORECASE)

# Wrap the body
rtf_body = article_sentence + r"\line "
full_rtf = rtf_header + rtf_body + rtf_footer

# ✅ Copy to clipboard as rich text
copy_rtf_to_clipboard(full_rtf)
print(full_rtf)
print("✔️ Copied! Paste into Word to see the blue highlight formatting.")
