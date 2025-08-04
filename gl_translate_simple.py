import re
import os
import argparse
from googletrans import Translator  # daha hizli ancak tam olarak dogru tercume yapmiyor
from deep_translator import (
    GoogleTranslator,
)  # daha kaliteli terc]me ediyor ancak zamanla duruyor
from show_progress import progress_bar

#  python gl_translate_simple.py --audio_file /Users/orhancavus/LocalDocuments/Podcast/CampoDelCielo/Campo_subs/Campo_En.srt --output_dir /Users/orhancavus/LocalDocuments/Podcast/CampoDelCielo/Campo_subs --language de


USE_DEEP_TRANSLATOR = True  # False


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


def read_srt_file(input_file):
    with open(input_file, "r", encoding="utf-8") as infile:
        subtitles = infile.readlines()
    return subtitles


def translate_subtitles(subtitles, translator):
    buffer = []
    translated_subtitles = []
    i = 0
    total_subs = round(len(subtitles) / 4)
    for line in subtitles:
        # for line in progress_bar(
        #    subtitles, total=len(subtitles), prefix="Progress", suffix="Complete", length=40
        # ):
        line = line.strip()
        # print(line)
        if re.match(r"^\d+$", line):  # Subtitle index
            if buffer:
                translated_subtitles.append("\n".join(buffer) + "\n\n")
                buffer = []
            buffer.append(line)
        elif "-->" in line:  # Timestamp line
            buffer.append(line)
        elif line:  # Text line
            try:
                if USE_DEEP_TRANSLATOR:
                    translated_text = translator.translate(line)
                else:
                    translated_text = translator.translate(line, dest="tr").text

                i += 1
                print(f"{i} / {total_subs} \n{translated_text}")
                buffer.append(translated_text)
            except Exception as e:
                print(f"Error translating text: {line} \nException: {e}")
                buffer.append(f"***{line}")

    if buffer:  # Add last subtitle block
        translated_subtitles.append("\n".join(buffer) + "\n")

    return translated_subtitles


def write_srt_file(output_file, translated_subtitles):
    with open(output_file, "w", encoding="utf-8") as outfile:
        for subtitle in translated_subtitles:
            outfile.write(subtitle)


def process_srt_file(input_file, output_dir, language):
    output_file = generate_output_file_path(input_file, output_dir, language)
    if output_file is None:
        return

    if USE_DEEP_TRANSLATOR:
        translator = GoogleTranslator(source="auto", target=language)
    else:
        translator = Translator()
    # Read the input file
    subtitles = read_srt_file(input_file)

    # Translate subtitles
    translated_subtitles = translate_subtitles(subtitles, translator)

    # Write the translated subtitles to the output file
    write_srt_file(output_file, translated_subtitles)


def main_simple():
    parser = argparse.ArgumentParser(
        description="Translate SRT files to different languages."
    )
    parser.add_argument("--audio_file", type=str, help="Path to the input SRT file.")
    parser.add_argument(
        "--output_dir", type=str, help="Directory to save the translated SRT files."
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
    ##function_to_use = args.function
    dest_langs = args.language

    print(f"\n\nTranslating {audio_file} to {dest_langs} and saving to {output_dir}")

    process_srt_file(audio_file, output_dir, language=dest_langs)


if __name__ == "__main__":
    #  python gl_translate_simple.py --audio_file /Users/orhancavus/LocalDocuments/Podcast/CampoDelCielo/Campo_subs/Campo_En.srt --output_dir /Users/orhancavus/LocalDocuments/Podcast/CampoDelCielo/Campo_subs --language de
    main_simple()
    # translate_srt_deep("input/archive/Dark_period_short.srt", "output", language="tr")

    # Example usage
    # process_srt_file(
    #    "/Users/orhancavus/LocalDocuments/Podcast/CompoDelCielo/Campo.srt",
    #    "/Users/orhancavus/LocalDocuments/Podcast/CompoDelCielo",
    #    "en",
    # )
