import pysrt
from googletrans import Translator
from deep_translator import GoogleTranslator
import os

dest_languages = ["tr", "bg", "es", "fr", "de", "it", "ru"]


def translate_srt_deep(input_file, output_file, target_language="es"):
    # Load subtitles
    subs = pysrt.open(input_file, encoding="utf-8")

    # Initialize translator
    translator = GoogleTranslator(source="auto", target=target_language)

    # Translate subtitles
    for sub in subs:
        sub.text = translator.translate(sub.text)

    # Save the translated subtitles
    subs.save(output_file, encoding="utf-8")


def translate_srt(input_file, output_file, target_language="es"):
    # couldnot translate to es
    # Load subtitles
    subs = pysrt.open(input_file, encoding="utf-8")

    # Initialize translator
    translator = Translator()

    # Translate each subtitle
    for sub in subs:
        pre_text = sub.text
        try:
            translation = translator.translate(sub.text, dest=target_language)
            if translation is not None:
                translated_text = translation.text
            else:
                translated_text = (
                    pre_text  # Fallback to original text if translation fails
                )
        except Exception as e:
            print(f"Error translating subtitle: {pre_text} \nExption{e}")
            translated_text = (
                f"***{pre_text}"  # Fallback to original text if an exception occurs
            )

        # Update the subtitle text with the translated text
        sub.text = translated_text

    # Save the translated subtitles to the output file
    subs.save(output_file, encoding="utf-8")


def translate_srt_to_all_languages(input_file, output_dir):
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    # Create output directory if it doesn't exist
    os.makedirs(f"{output_dir}/{file_name}", exist_ok=True)
    for language in dest_languages:
        output_file = f"{output_dir}/{file_name}/{file_name}_to_{language}.srt"
        print(f"Translating to {language} and saving to {output_file}")
        translate_srt_deep(input_file, output_file, target_language=language)


if "__main__" == __name__:
    # Example usage
    # translate_srt_to_all_languages("Cernobil2024_en.srt", "/path/to/output_dir")
    if True:
        translate_srt_to_all_languages(
            "input/Cernobil2024_en.srt",
            "output",
        )
    else:
        # Example usage
        # translate_srt("Cernobil2024_en.srt", "Cernobil2024_tr.srt", target_language="tr")
        # translate_srt("sample.srt", "sample_es.srt", target_language="es")
        translate_srt_deep("sample.srt", "sample_es_deep.srt", target_language="es")
