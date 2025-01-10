import os
import argparse
import pysrt
from googletrans import Translator
from deep_translator import GoogleTranslator
from show_progress import progress_bar

# Common languages to translate to
destination_languages = ["tr", "bg", "ru", "es", "fr", "de", "it"]


def translate_srt_deep(input_file, output_dir, language="es"):
    """
    Translates the subtitles in an SRT file to a specified language using Google Translate.
    Args:
        input_file (str): Path to the input SRT file.
        output_dir (str): Directory where the translated SRT file will be saved.
        language (str, optional): Target language code for translation. Defaults to "es" (Spanish).
    Raises:
        Exception: If an error occurs during translation, the original subtitle text is retained with a prefix "***".
    """

    # Load subtitles
    subs = pysrt.open(
        input_file,
        encoding="utf-8",
    )

    output_file = generate_output_file_path(input_file, output_dir, language)
    if output_file is None:
        return

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


def generate_output_file_path(input_file, output_dir, language):
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    # Create output directory if it doesn't exist
    output_path = os.path.join(output_dir, file_name)
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, f"{file_name}_to_{language}.srt")

    if os.path.exists(output_file):
        print(f"Output file {output_file} already exists.")
        return None
    return output_file


def translate_srt(input_file, output_dir, language="es"):
    """
    Translates the subtitles in an SRT file to a specified language and saves the translated subtitles to a new file.
    Args:
        input_file (str): The path to the input SRT file.
        output_dir (str): The directory where the translated SRT file will be saved.
        language (str, optional): The target language code for translation (default is "es" for Spanish).
    Raises:
        Exception: If an error occurs during translation, the original text is used with an error message printed.
    Returns:
        None
    """

    # in some cases could not translate to es
    # Load subtitles
    subs = pysrt.open(input_file, encoding="utf-8")

    # Initialize translator
    translator = Translator()

    output_file = generate_output_file_path(input_file, output_dir, language)
    if output_file is None:
        return

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


# TODO2 summarize the subtitles with local LLM


def main():
    parser = argparse.ArgumentParser(
        description="Translate SRT files to different languages."
    )
    parser.add_argument("--audio_file", type=str, help="Path to the input SRT file.")
    parser.add_argument(
        "--output_dir", type=str, help="Directory to save the translated SRT files."
    )
    parser.add_argument(
        "--function",
        type=str,
        choices=["deep", "google", "multi_deep"],
        default="multi_deep",
        help="Function to use for translation.",
    )
    parser.add_argument(
        "--language",
        type=str,
        default="es",
        help="Target language for translation (only used with 'deep' or 'google' functions).",
    )

    args = parser.parse_args()

    audio_file = args.audio_file
    output_dir = args.output_dir
    function_to_use = args.function
    language = args.language

    if function_to_use == "deep":
        print(f"\n\nTranslating {audio_file} to {language} and saving to {output_dir}")
        translate_srt_deep(audio_file, output_dir, language=language)
    elif function_to_use == "google":
        print(f"\n\nTranslating {audio_file} to {language} and saving to {output_dir}")
        translate_srt(audio_file, output_dir, language=language)
    elif function_to_use == "multi_deep":
        dest_langs = destination_languages
        print(
            f"\n\nTranslating {audio_file} to {dest_langs} and saving to {output_dir}"
        )

        translate_srt_to_all_languages(
            audio_file, output_dir, dest_languages=dest_langs
        )
    else:
        print(
            "Invalid function specified. Please choose 'deep', 'google', or 'multi_deep'."
        )


if __name__ == "__main__":
    main()
