#!/usr/bin/env python

# Imports ###############################################################################

import configparser
import hashlib
import sys
import time

import orgparse
import webdav3.client

from os import path

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from texttospeech import text_to_audio_file
from utils import get_valid_filename


# Configuration & constants #############################################################

config = configparser.ConfigParser()
config.read('audiochecklist.cfg')
config = config['AudioChecklist']


# Classes ###############################################################################

class AudioChecklistApp(App):
    def __init__(self, *args, **kwargs):
        super(AudioChecklistApp, self).__init__(*args, **kwargs)
        self.sound = None
        self.checklist_items = self.get_checklist_items()

    def build(self):
        b = BoxLayout(orientation='horizontal', spacing=10, width=1600, height=900)
        self.title_label = Label(text="Welcome", font_size=30)
        b.add_widget(self.title_label)
        checkbtn = Button(text='Next')
        checkbtn.bind(on_release=self.show_next_checklist_item)
        b.add_widget(checkbtn)
        return b

    def show_next_checklist_item(self, obj):
        if not self.checklist_items:
            return # TODO: What do we do when we reach the end of the list?

        checklist_item = self.checklist_items.pop(0)
        self.title_label.text = checklist_item
        self.read_text(checklist_item)

    def get_checklist_items(self):
        # TODO: Fix disabled webdav retrieval
        # self.webdav = webdav3.client.Client({
        #         'webdav_hostname': config['REPOSITORY_WEBDAV_URL'],
        #         'webdav_login':    config['REPOSITORY_WEBDAV_USER'],
        #         'webdav_password': config['REPOSITORY_WEBDAV_PASSWORD'],
        # })
        # self.webdav.check('/checklist_flight_planning.org')
        # self.webdav.download_sync(
        #         remote_path='/checklist_flight_planning.org',
        #         local_path='/tmp/checklist_flight_planning.org')
        #
        # self.checklist = orgparse.load('/tmp/checklist_flight_planning.org')

        self.checklist = orgparse.load('checklist_flight_planning.org')
        checklist_items = self.checklist.children[6][1:]

        return [item.heading for item in checklist_items]

    def read_text(self, text):
        print(text)

        if self.sound:
            self.sound.stop()
            self.sound.unload()

        audio_filename = self.get_audio_filename(text)
        if not path.exists(audio_filename):
            text_to_audio_file(text, audio_filename)

        self.sound = SoundLoader.load(audio_filename)
        self.sound.play()

    def get_audio_filename(self, text):
        return './audio/{}_{}.mp3'.format(get_valid_filename(text), hashlib.md5(text.encode('utf8')).hexdigest())


# Main ##################################################################################

if __name__ == "__main__":
    sys.stderr.write('DEBUG-AUDIOCHECKLIST-TEST')
    AudioChecklistApp().run()
