import pysrt
from googletrans import Translator
from deep_translator import GoogleTranslator
from show_progress import progress_bar
import os

# dest_languages = ["tr", "bg", "es", "fr", "de", "it", "ru"]
destination_languages = ["ru", "es", "fr", "de", "it"]


def translate_srt_deep(input_file, output_dir, language="es"):
    # Load subtitles
    subs = pysrt.open(input_file, encoding="utf-8")

    file_name = os.path.splitext(os.path.basename(input_file))[0]
    # Create output directory if it doesn't exist
    output_path = os.path.join(output_dir, file_name)
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, f"{file_name}_to_{language}.srt")

    # Initialize translator
    translator = GoogleTranslator(source="auto", target=language)

    for sub in progress_bar(
        subs, total=len(subs), prefix="Progress", suffix="Complete", length=40
    ):
        try:
            sub.text = translator.translate(sub.text)
        except Exception as e:
            print(f"Error translating subtitle: {sub.text} \nException: {e}")
            sub.text = (
                f"***{sub.text}"  # Fallback to original text if an exception occurs
            )

    # Save the translated subtitles
    subs.save(output_file, encoding="utf-8")


def translate_srt(input_file, output_dir, language="es"):
    # in some cases could not translate to es
    # Load subtitles
    subs = pysrt.open(input_file, encoding="utf-8")

    # Initialize translator
    translator = Translator()

    file_name = os.path.splitext(os.path.basename(input_file))[0]
    # Create output directory if it doesn't exist
    output_path = os.path.join(output_dir, file_name)
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, f"{file_name}_to_{language}.srt")

    # Translate each subtitle
    for sub in progress_bar(
        subs, total=len(subs), prefix="Progress", suffix="Complete", length=40
    ):
        pre_text = sub.text
        try:
            translation = translator.translate(sub.text, dest=language)
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


def translate_srt_to_all_languages(
    input_file, output_dir, dest_languages=destination_languages
):
    for language in dest_languages:
        print(f"Translating to {language} and saving to folder : {output_dir}")
        translate_srt_deep(input_file, output_dir, language=language)


# TODO1 add the main function
# TODO2 summarize the subtitles with local LLM

if "__main__" == __name__:
    audio_file = "input/Bulgaria1984.srt"
    output_dir = "output"

    # Example usage
    function_to_use = (
        "all"  # Change this to "deep", "google", or "all" to use different functions
    )

    language = "no"

    if function_to_use == "deep":
        print(f"\n\nTranslating {audio_file} to {language} and saving to {output_dir}")
        translate_srt_deep(audio_file, output_dir, language=language)
    elif function_to_use == "google":
        print(f"\n\nTranslating {audio_file} to {language} and saving to {output_dir}")
        translate_srt(audio_file, output_dir, language=language)
    elif function_to_use == "all":
        dest_langs = ["no"]  # destination_languages
        print(
            f"\n\nTranslating {audio_file} to {dest_langs} and saving to {output_dir}"
        )

        translate_srt_to_all_languages(
            audio_file, output_dir, dest_languages=dest_langs
        )
    else:
        print("Invalid function specified. Please choose 'deep', 'google', or 'all'.")
