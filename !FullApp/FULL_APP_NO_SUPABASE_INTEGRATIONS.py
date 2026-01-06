# Old, don't use (5min)
# nuitka --output-filename=Cardify-Cut-SAJGETSLOST0 --mingw64 --standalone --onefile --remove-output=no --windows-disable-console --enable-plugin=tk-inter --include-data-dir=certifi=certifi --include-module=win32clipboard --include-module=win32con --enable-plugin=pylint-warnings --follow-imports cardify-cut.py

# FASTER: (2min 30s)
# nuitka --output-filename=Cardify-Cut-LICENSENAME --mingw64 --standalone --onefile --windows-disable-console --enable-plugin=tk-inter --include-module=win32clipboard --include-module=win32con --enable-plugin=pylint-warnings --nofollow-import-to=nltk --follow-imports --lto=no cardify-cut.py

# import os
# LICENSE = os.getenv("CARDIFY_LICENSE", "DEFAULT_LICENSE")

import customtkinter as ctk
import tkinter as tk
import threading
import uuid
from datetime import datetime

import win32clipboard as wc
import win32con
import re


def get_machine_id():
    return hex(uuid.getnode())

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

def copy_rtf_to_clipboard(rtf_text):
    wc.OpenClipboard()
    wc.EmptyClipboard()
    wc.SetClipboardData(win32con.CF_TEXT, rtf_text.encode('windows-1252'))  # Optional plain-text fallback
    wc.SetClipboardData(wc.RegisterClipboardFormat("Rich Text Format"), rtf_text.encode('windows-1252'))
    wc.CloseClipboard()


def output_formatted_rtf(article_sentence, mistral_output):
    # ========================
    # BUILDING THE RTF OUTPUT
    # ========================
    # Use this for RTF highlight
    begin = r"{\highlight1\b\ul "
    end = r"}"

    # Process
    formatted_rtf_body = ""
    highlighted_phrase = article_sentence
    if "NOTHING" not in mistral_output:   # check if we can skip if phrase starts with "NOTHING"
        highlighted_phrase = highlight_extracted_words(article_sentence, mistral_output, beginning_marker=begin, ending_marker=end)

    formatted_rtf_body += highlighted_phrase + r"\line "
    formatted_rtf_body = formatted_rtf_body.replace(end + " " + begin, " ") # Make the highlights continuous with each other

    print("=="*50 + "\n\n" + formatted_rtf_body)
    print(formatted_rtf_body)

    return formatted_rtf_body

from newspaper import Article

def getArticleText(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text


import subprocess
import os

def find_ollama_path():
    local_appdata = os.getenv('LOCALAPPDATA')
    ollama_path = os.path.join(local_appdata, "Programs", "Ollama", "ollama.exe")
    if os.path.exists(ollama_path):
        return ollama_path
    return None


def build_verbatim_prompt(article_text, argument, pickycut):
    REGULARCUTPROMPT = f"""
        You are helping a high school debater cut evidence cards.

        Read the article sentence below. If it supports the provided argument below it, return the sentence 
        **exactly as it is**. If it does not, return the text "NOTHING". Do not summarize or explain. 
        Return text verbatim from the provided article.
        """
    PICKYCUTPROMPT = f"""
            You are helping a high school debater cut evidence cards.
            Read the article sentence below. If it supports the provided argument below it, return the sentence **exactly as it is**. If it does not, return the text "NOTHING". Do not summarize or explain. Return text verbatim from the provided article. Be selective in what you choose: ignore anecdotes, quotes, or statistics. Only return the small phrases from the sentences that functionally say what the argument says.
            """
    if pickycut == "pickycut":
        return PICKYCUTPROMPT + f"""
        Article: {article_text} 
        My argument: {argument}"""

    return REGULARCUTPROMPT + f"""
            Article: {article_text} 
            My argument: {argument}"""

def cut_evidence_with_ollama(subsentence_article_text, argument_prompt, pickycut):
    OLLAMA_PATH = find_ollama_path()
    full_prompt = build_verbatim_prompt(subsentence_article_text, argument_prompt, pickycut)
    print("\nSending to Mistral...\n--")
    result = subprocess.run(
        [OLLAMA_PATH, "run", "mistral"],
        input=full_prompt.encode("utf-8"),
        capture_output=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    return result.stdout.decode("utf-8")


def display_card(highlighted_text):
    print(highlighted_text)
    print("=" * 80)

def mistralCutSentence(sentence, argument, pickycut):
    highlighted = cut_evidence_with_ollama(sentence, argument, pickycut)
    display_card(highlighted)

    # splitArt = sentence.split("\n")
    # print(f"Full Article: {len(splitArt)}")
    # print(f"Output Sentences: {len(output_sentences)}")
    # for i, o in enumerate(output_sentences): print(str(o) + ",")
    return highlighted

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class RTFApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cardify.Cut")

        self.geometry("700x800")
        self.MACHINE_ID = get_machine_id()

        self.input_mode = tk.StringVar(value="Link")
        self.selected_color_button = None  # Tracks selected color button

        # Header
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(pady=(10, 0), fill="x", padx=20)

        # Left: license status
        self.status_label = ctk.CTkLabel(header_frame, text="", text_color="red", anchor="w")
        self.status_label.pack(side="left", padx=(5, 0), expand=True)

        # Right: expiry + card stats
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=20)

        # Left: Title
        title_label = ctk.CTkLabel(title_frame, text="Cardify.Cut", font=ctk.CTkFont(size=36, weight="bold"))
        title_label.pack(side="left")

        # Right: Color buttons
        color_button_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        color_button_frame.pack(side="right")

        self.color_buttons = []
        self.color_options = ["#FFFF00", "#00FF00", "#05FAFA"]
        self.stats_label = ctk.CTkLabel(header_frame, text="", anchor="e")
        self.stats_label.pack(side="right", padx=(0, 5))

        for color in self.color_options:
            btn = ctk.CTkButton(
                master=color_button_frame,
                width=24,
                height=24,
                text="",
                fg_color=color,
                hover_color=color,
                border_width=0,
                corner_radius=6,
                command=lambda c=color, b=None: None  # Temporary
            )
            btn.pack(side="right", padx=4)
            self.color_buttons.append(btn)

            # Select the first button by default
        self.selected_color_button = self.color_buttons[2]
        self.selected_color_button.configure(border_width=2, border_color="white")
        self.RTF_HEADER = r"""{\rtf1\ansi\deff0{\colortbl ;\red204\green255\blue255;}"""  # Light blue highlight
        self.RTF_FOOTER = "}"

        # Assign command now that buttons are created
        for i, btn in enumerate(self.color_buttons):
            btn.configure(command=lambda c=self.color_options[i], b=btn: self.select_color(c, b))

        # Title
        ctk.CTkLabel(self, text="Developed by Ishan Pendyala | Friendswood Debate", font=ctk.CTkFont(size=12)).pack(pady=(0, 2))
        ctk.CTkLabel(self, text="Contact at pengames2020@gmail.com", font=ctk.CTkFont(size=12)).pack(pady=(0, 2))

        # Update labels
        # self.update_license_labels()

        # Toggle for input type
        self.toggle_frame = ctk.CTkFrame(self)
        self.toggle_frame.pack(pady=10)
        self.link_toggle = ctk.CTkRadioButton(self.toggle_frame, text="Link", variable=self.input_mode, value="Link", command=self.clear_output)
        self.paragraph_toggle = ctk.CTkRadioButton(self.toggle_frame, text="Paragraph", variable=self.input_mode, value="Paragraph", command=self.clear_output)
        self.link_toggle.grid(row=0, column=0, padx=10)
        self.paragraph_toggle.grid(row=0, column=1, padx=10)
        self.pickycut_toggle = ctk.CTkSwitch(self.toggle_frame, text="PickyCut",offvalue="regularcut",onvalue="pickycut")
        self.pickycut_toggle.grid(row=0, column=2, padx=10)

        # Input box
        ctk.CTkLabel(self, text="Enter Link or Paragraph:").pack(anchor='w', padx=20)
        self.input_box = ctk.CTkTextbox(self, height=120, wrap="word")
        self.input_box.pack(padx=20, pady=5, fill="x")

        # Argument input
        ctk.CTkLabel(self, text="Argument:").pack(anchor='w', padx=20)
        self.argument_box = ctk.CTkTextbox(self, height=80, wrap="word")
        self.argument_box.pack(padx=20, pady=5, fill="x")

        # Process button
        self.process_button = ctk.CTkButton(self, text="Process", command=self.start_process_thread)
        self.process_button.pack(pady=10)

        # Loading label (initially hidden)
        self.loading_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.loading_label.pack()

        # Output label and text
        ctk.CTkLabel(self, text="RTF Output:").pack(anchor='w', padx=20)
        self.output_box = ctk.CTkTextbox(self, height=180, wrap="word")
        self.output_box.pack(padx=20, pady=5, fill="x")
        self.output_box.configure(state="disabled")

        self.rtf_result = ""

        self.copy_button = ctk.CTkButton(self, text="Copy RTF to Clipboard", command=self.copy_rtf_to_clipboard)
        self.copy_button.pack(pady=10)

    def select_color(self, color, button):
        # Unselect previous
        if self.selected_color_button:
            self.selected_color_button.configure(border_width=0)
        # Select new
        button.configure(border_width=2, border_color="white")
        self.selected_color_button = button
        print(self.selected_color_button.cget("fg_color"))

        fg_color = self.selected_color_button.cget("fg_color")
        if fg_color == self.color_options[2]:
            self.RTF_HEADER = r"""{\rtf1\ansi\deff0{\colortbl ;\red204\green255\blue255;}"""  # Light blue highlight
        elif fg_color == self.color_options[1]:
            self.RTF_HEADER = r"""{\rtf1\ansi\deff0{\colortbl ;\red5\green252\blue5;}"""  # Green highlight
        elif fg_color == self.color_options[0]:
            self.RTF_HEADER = r"""{\rtf1\ansi\deff0{\colortbl ;\red252\green252\blue4;}"""  # Yellow highlight

    def validate_license(self):
        ## Removed logic code for MIT Maker Portfolio
        return True

    def clear_output(self):
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.configure(state="disabled")

    def start_process_thread(self):
        self.loading_label.configure(text="Processing...")
        self.process_button.configure(state="disabled")
        self.copy_button.configure(state="disabled")
        self.rtf_result = ""
        self.clear_output()
        thread = threading.Thread(target=self.process_inputs)
        thread.start()

    def process_inputs(self):
        # Re-validate license before every action
        # self.LICENSE_DATA = fetch_license_data(self.LICENSE)
        # self.is_valid_license = self.validate_license()

        # if not self.is_valid_license:
        #    self.clear_output()
        #    self.output_box.configure(state="normal")
        #    self.output_box.insert("1.0", "License expired or not valid for this device.")
        #    self.output_box.configure(state="disabled")
        #    return

        input_type = self.input_mode.get()
        article_content = self.input_box.get("1.0", "end").strip()
        argument = self.argument_box.get("1.0", "end").strip()

        if input_type == "Link":
            article = getArticleText(article_content)
        else:
            article = article_content


        for sentence in article.split("\n"): # Dynamically cut cards and add into output
            highlighted_sentence = mistralCutSentence(sentence, argument, self.pickycut_toggle.get())
            self.rtf_result += output_formatted_rtf(sentence, highlighted_sentence)
            self.output_box.configure(state="normal")
            self.output_box.delete("1.0", "end")
            self.output_box.insert("1.0", self.RTF_HEADER + self.rtf_result + self.RTF_FOOTER)
            self.output_box.configure(state="disabled")

        ## Update RTF Output for Final Time
        self.output_box.delete("1.0", "end")
        self.rtf_result = self.RTF_HEADER + self.rtf_result + self.RTF_FOOTER
        self.output_box.insert("1.0", self.rtf_result)
        self.output_box.configure(state="disabled")

        # License update
        # increment_cards_cut(self.LICENSE)
        # self.LICENSE_DATA = fetch_license_data(self.LICENSE)
        # self.update_license_labels()

        def finish_up():
            # self.update_license_labels()
            self.loading_label.configure(text="")
            self.process_button.configure(state="normal")
            self.copy_button.configure(state="normal")

        self.after(0, finish_up)

    def copy_rtf_to_clipboard(self):
        wc.OpenClipboard()
        wc.EmptyClipboard()
        wc.SetClipboardData(win32con.CF_TEXT, self.rtf_result.encode('windows-1252'))
        wc.SetClipboardData(wc.RegisterClipboardFormat("Rich Text Format"), self.rtf_result.encode('windows-1252'))
        wc.CloseClipboard()


if __name__ == "__main__":
    app = RTFApp()
    app.mainloop()
