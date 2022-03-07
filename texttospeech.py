
#from google.cloud import texttospeech

#speech_api = texttospeech.TextToSpeechClient()

def text_to_audio_file(text, audio_filename):
    """
    Convert `text` into an audio file, written at `audio_filename`
    """
    # input_text = texttospeech.SynthesisInput(text=text)
    # voice = texttospeech.VoiceSelectionParams(
    #             language_code='en-US',
    #             name='en-US-Wavenet-F')
    # audio_config = texttospeech.AudioConfig(
    #             speaking_rate=1.3,
    #             audio_encoding=texttospeech.AudioEncoding.MP3)

    # response = speech_api.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    with open(audio_filename, 'wb') as out:
        out.write(response.audio_content)
