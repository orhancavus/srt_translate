import os
from googletrans import Translator

from deep_translator import GoogleTranslator


def translate_file(file_path, dest_language="en"):
    if not os.path.isfile(file_path):
        print(f"The file {file_path} does not exist.")
        return

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    translator = Translator()
    translated = translator.translate(content, dest=dest_language)

    translated_file_path = f"{os.path.splitext(file_path)[0]}_translated.txt"
    with open(translated_file_path, "w", encoding="utf-8") as file:
        file.write(translated.text)

    print(f"Translated content saved to {translated_file_path}")


# Example usage
directory = "input/archive/"
file_name = "Cernobil2024_en.srt"
file_path = os.path.join(directory, file_name)
translate_file(file_path, dest_language="tr")
