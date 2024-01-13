#!/usr/bin/env python3

import csv
import io
from gtts import gTTS
from pydub import AudioSegment
from mutagen.id3 import ID3, TIT2, TPE1, TALB, COMM
from mutagen.mp3 import MP3

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
first_15_words = []
with open('your_file.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header

    combined_audio = AudioSegment.empty()
    for i, row in enumerate(reader):
        if i >= 15:  # Process only first 15 lines
            break
        term, example, _, translation, _, _ = row
        first_15_words.append(term)
        combined_audio += process_line(term, example, translation)

# Create a description from the first 15 words
description = ', '.join(first_15_words)

# Save final audio
output_file = "final_audio.mp3"
combined_audio.export(output_file, format="mp3")

# Add ID3 tags
audio_file = MP3(output_file)
audio_file.tags = ID3()
audio_file.tags.add(TIT2(encoding=3, text=description))  # Using the description as title
audio_file.tags.add(TPE1(encoding=3, text="Robo Owl"))
audio_file.tags.add(TALB(encoding=3, text="Czech"))
audio_file.tags.add(COMM(encoding=3, desc="Description", text=description))  # Adding description
audio_file.save()

