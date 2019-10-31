# Imports ###############################################################################

import configparser
import time

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from google.cloud import texttospeech_v1 as texttospeech

import todoist


# Configuration & constants #############################################################

config = configparser.ConfigParser()
config.read('audiochecklist.cfg')
config = config['AudioChecklist']


# Classes ###############################################################################

class AudioChecklistApp(App):
    def __init__(self, *args, **kwargs):
        super(AudioChecklistApp, self).__init__(*args, **kwargs)
        self.speech_api = texttospeech.TextToSpeechClient()
        self.sound = None
        self.checklist_items = self.get_checklist_items()

    def intro_wizard(self):
        """
        TODO: Initial welcome screen, with wizard to setup
        """
        intro_text = "Welcome to AudioChecklist. We'll get you setup quickly! " \
                     "You will be editing your checklists on Todoist. " \
                     "Click on the following button to go create and link your Todoist account."

    def build(self):
        b = BoxLayout(orientation='horizontal', spacing=10, width=1600, height=900)
        self.title_label = Label(text="Welcome", font_size=30)
        b.add_widget(self.title_label)
        checkbtn = Button(text='Next')
        checkbtn.bind(on_release=self.show_next_checklist_item)
        b.add_widget(checkbtn)
        return b

    def show_next_checklist_item(self, obj):
        checklist_item = self.checklist_items.pop(0)
        self.title_label.text = checklist_item
        self.text2audio(checklist_item)

    def get_checklist_items(self):
        api = todoist.TodoistAPI(config['TODOIST_API_KEY'])
        api.sync()
        project = api.projects.get_by_id(config['TODOIST_PROJECT_ID'])
        checklist = api.projects.get_data(config['TODOIST_PROJECT_ID'])
        return [item['content'] for item in checklist['items']]

    def text2audio(self, text):
        print(text)

        if self.sound:
            self.sound.stop()
            self.sound.unload()

        input_text = texttospeech.types.SynthesisInput(text=text)
        voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    name='en-US-Wavenet-F')
        audio_config = texttospeech.types.AudioConfig(
                    speaking_rate=1.3,
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        response = self.speech_api.synthesize_speech(input_text, voice, audio_config)

        with open('/tmp/output.mp3', 'wb') as out:
            out.write(response.audio_content)

        self.sound = SoundLoader.load('/tmp/output.mp3')
        self.sound.play()


# Main ##################################################################################

if __name__ == "__main__":
    AudioChecklistApp().run()
