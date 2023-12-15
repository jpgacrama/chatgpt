#!/usr/bin/env python3
import docx, os

def clear_screen():
    # Clear the screen based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

# Get the absolute path of the current directory
current_directory = os.path.dirname(__file__)

# Construct the relative path to info.docx
relative_path = "info.docx"

# Combine the current directory and the relative path to get the absolute path
absolute_path = os.path.join(current_directory, relative_path)

doc = docx.Document("/Users/jonasgacrama/work/chatgpt/Chapter06 WordTranslator/info.docx")

text = ""

for para in doc.paragraphs:
    text += para.text
print(text)