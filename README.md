
# SRT Translator

This project provides a tool to translate SRT subtitle files into multiple languages using the `deep_translator` library.

## Features

- Translate SRT files to multiple languages.
- Supports translation to Turkish, Bulgarian, Spanish, French, German, Italian, and Russian.
- Handles translation failures gracefully.

## Requirements

- Python 3.6+
- `deep_translator` library
- `pysrt` library

## Installation

1.Clone the repository:

```sh
git clone https://github.com/yourusername/srt_translator.git
cd srt_translator
```

2.Install the required libraries:

```sh
pip install deep_translator pysrt
```

## Usage

### Translate a single SRT file

To translate a single SRT file to a specific language, use the [translate_srt_deep](http://_vscodecontentref_/0) function:

```python
from gl_translate import translate_srt_deep

translate_srt_deep("input/sample.srt", "output/sample_es.srt", target_language="es")

