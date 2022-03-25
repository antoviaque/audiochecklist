#!/usr/bin/env python

# Imports ###############################################################################

import os
import subprocess
import sys

from google.cloud import texttospeech

from checklist import get_audio_filename, get_all_checklists_items_names


# Globals ###############################################################################

speech_api = texttospeech.TextToSpeechClient()


# Functions #############################################################################

def generate_audio_files():
    """
    Generate a voice synthetized audio file for each item contained in the checklist
    """
    for text in get_all_checklists_items_names() + ['skipped']:
        sys.stderr.write('CHECKLIST-ITEM: {}\n'.format(text))

        audio_filename = get_audio_filename(text, 'mp3')
        if not os.path.exists(audio_filename):
            text_to_audio_file(text, audio_filename)
            convert_to_ogg(text)
    

def text_to_audio_file(text, audio_filename):
    """
    Convert `text` into an audio file, written at `audio_filename`
    """
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
                language_code='en-US',
                name='en-US-Wavenet-F')
    audio_config = texttospeech.AudioConfig(
                speaking_rate=1.3,
                audio_encoding=texttospeech.AudioEncoding.MP3)

    response = speech_api.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    with open(audio_filename, 'wb') as out:
        out.write(response.audio_content)

def convert_to_ogg(text):
    mp3_filename = get_audio_filename(text, 'mp3')
    ogg_filename = get_audio_filename(text, 'ogg')

    process = subprocess.Popen(['ffmpeg','-i', mp3_filename, ogg_filename],
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()


# Main ##################################################################################

if __name__ == "__main__":
    generate_audio_files()
