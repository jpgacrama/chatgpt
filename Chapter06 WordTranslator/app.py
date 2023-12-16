#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import filedialog, Text, Label, Button, OptionMenu
import docx
from openai import OpenAI

client = OpenAI(
    # Retrieve the API key from the environment variable
    api_key = os.environ.get('OPENAI_API_KEY')
)

def clear_screen():
    # Clear the screen based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

class TextTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Text Translator")
        self.root.configure(bg="white")

        self.create_header()
        self.create_browse_button()
        self.create_language_menu()
        self.create_text_field()

    def create_header(self):
        header_font = ("Open Sans", 16, "bold")
        header = Label(
            self.root,
            text="Text Translator",
            bg="white",
            font=header_font,
        )
        header.grid(row=0, column=0, columnspan=2, pady=20)

    def create_browse_button(self):
        browse_button = Button(
            self.root,
            text="Browse",
            command=self.browse_file,
            bg="#4267B2", fg="black", relief="flat",
            borderwidth=0, activebackground="#4267B2",
            activeforeground="white"
        )
        browse_button.config(font=("Arial", 12, "bold"), width=10, height=2)
        browse_button.grid(row=1, column=0, padx=20, pady=20)

    def create_language_menu(self):
        languages = ["Bulgarian", "Hindi", "Spanish", "French"]
        self.language_var = tk.StringVar(self.root)
        self.language_var.set(languages[0])
        language_menu = OptionMenu(self.root, self.language_var, *languages)
        language_menu.config(font=("Arial", 12), width=10)
        language_menu.grid(row=1, column=1, padx=20, pady=20)

    def create_text_field(self):
        self.text_field = Text(
            self.root,
            height=20, width=50, bg="white", fg="black",
            relief="flat", borderwidth=0, wrap="word"
        )
        self.text_field.grid(row=2, column=0, columnspan=2, padx=20, pady=20)
        self.text_field.grid_rowconfigure(0, weight=1)
        self.text_field.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def translate_text(self, file_location, target_language):
        doc = docx.Document(file_location)
        text = ""
        for para in doc.paragraphs:
            text += para.text
        model_engine = "gpt-3.5-turbo"
        response = client.chat.completions.create(
            model=model_engine,
            messages=[
                {"role": "user", "content": "You are a professional language translator. "
                                            "Below I will ask you to translate text. "
                                            "I expect from you to give me the correct translation"
                                            "Can you help me with that?"},
                {"role": "assistant", "content": "Yes, I can help you with that."},
                {"role": "user", "content": f"Translate the following text in {target_language} : {text}"}
            ]
        )

        translated_text = response.choices[0].message.content
        return translated_text

    def browse_file(self):
        file_location = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                   title="Select file",
                                                   filetypes=(("Word files", "*.docx"), ("all files", "*.*")))
        if file_location:
            target_language = self.language_var.get()

            translated_text = self.translate_text(file_location, target_language)
            self.text_field.delete("1.0", tk.END)
            self.text_field.insert(tk.END, translated_text)

def main():
    clear_screen()
    root = tk.Tk()
    app = TextTranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
