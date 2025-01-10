import pysrt
from googletrans import Translator
from deep_translator import GoogleTranslator
from show_progress import progress_bar
import os

# dest_languages = ["tr", "bg", "es", "fr", "de", "it", "ru"]
dest_languages = ["ru", "es", "fr", "de", "it"]


def translate_srt_deep(input_file, output_dir, language="es"):
    # Load subtitles
    subs = pysrt.open(input_file, encoding="utf-8")

    file_name = os.path.splitext(os.path.basename(input_file))[0]
    # Create output directory if it doesn't exist
    os.makedirs(f"{output_dir}/{file_name}", exist_ok=True)

    # Initialize translator
    translator = GoogleTranslator(source="auto", target=language)

    for sub in progress_bar(
        subs, total=len(subs), prefix="Progress", suffix="Complete", length=40
    ):
        sub.text = translator.translate(sub.text)

    """               
    # Translate subtitles
    for sub in subs:
        pre_text = sub.text
        sub.text = translator.translate(sub.text)
        print(f"Translating: {pre_text} -> {sub.text}")
    """
    output_file = f"{output_dir}/{file_name}/{file_name}_to_{language}.srt"

    # Save the translated subtitles
    subs.save(output_file, encoding="utf-8")


def translate_srt(input_file, output_file, target_language="es"):
    # in some cases could not translate to es
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


# TODO1 add the main function
# TODO2 summarize the subtitles with local LLM

if "__main__" == __name__:
    audio_file = "input/Bulgaria1984.srt"
    output_dir = "output"

    # Example usage
    function_to_use = (
        "all"  # Change this to "deep", "google", or "all" to use different functions
    )
    print(f"\n\nTranslating {audio_file} and saving to {output_dir}")

    if function_to_use == "deep":
        translate_srt_deep(audio_file, output_dir, language="tr")
    elif function_to_use == "google":
        output_file = f"{output_dir}/{os.path.splitext(os.path.basename(audio_file))[0]}_to_tr.srt"
        translate_srt(audio_file, output_file, target_language="tr")
    elif function_to_use == "all":
        translate_srt_to_all_languages(audio_file, output_dir)
    else:
        print("Invalid function specified. Please choose 'deep', 'google', or 'all'.")
