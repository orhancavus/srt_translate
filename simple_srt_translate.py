import srt


def translate_text(text):
    # Dummy translation function (replace this with an actual translation logic)
    return text[::-1]  # Example: reversing the text as a placeholder


def process_srt(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile:
        subtitles = list(srt.parse(infile.read()))

    for subtitle in subtitles:
        subtitle.content = translate_text(subtitle.content)

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(srt.compose(subtitles))


# Example usage
process_srt(
    "input/archive/Dark_period_short.srt",
    "output/archive/Dark_Period/Dark_period_short_output.srt",
)
