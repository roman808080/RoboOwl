#!/usr/bin/env python3

import csv
import io
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

# Function to add pause
def add_pause(audio, pause_duration=500):
    pause = AudioSegment.silent(duration=pause_duration)
    return audio + pause

# Function to process each line
def process_line(term, example, translation):
    audio = AudioSegment.empty()

    # Translation
    with io.BytesIO() as fp:
        tts = gTTS(text=translation, lang='en')
        tts.write_to_fp(fp)
        fp.seek(0)
        translation_audio = AudioSegment.from_file(fp, format="mp3")
        audio += add_pause(translation_audio)

    # Word repeated three times
    for _ in range(3):
        with io.BytesIO() as fp:
            tts = gTTS(text=term, lang='cs')
            tts.write_to_fp(fp)
            fp.seek(0)
            word_audio = AudioSegment.from_file(fp, format="mp3")
            audio += add_pause(word_audio)

    # Example repeated twice
    for _ in range(2):
        with io.BytesIO() as fp:
            tts = gTTS(text=example, lang='cs')
            tts.write_to_fp(fp)
            fp.seek(0)
            example_audio = AudioSegment.from_file(fp, format="mp3")
            audio += add_pause(example_audio)

    return audio

# Main script
with open('your_file.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header

    combined_audio = AudioSegment.empty()
    for i, row in enumerate(reader):
        if i >= 15:  # Process only first 15 lines
            break
        term, example, _, translation, _, _ = row
        combined_audio += process_line(term, example, translation)

# Save final audio
combined_audio.export("final_audio.mp3", format="mp3")

