#!/usr/bin/env python

# Imports ###############################################################################

import configparser
import os
import sys
import time

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from checklist import get_checklist_items, get_audio_filename


# Configuration & constants #############################################################

config = configparser.ConfigParser()
config.read('audiochecklist.cfg')
config = config['AudioChecklist']


# Classes ###############################################################################

class AudioChecklistApp(App):
    def __init__(self, *args, **kwargs):
        super(AudioChecklistApp, self).__init__(*args, **kwargs)
        self.sound = None
        self.checklist_items = get_checklist_items()

    def build(self):
        b = BoxLayout(orientation='vertical', spacing=10, width=1600, height=900)

        self.checklist_selector = Spinner(
            # default value shown
            text=self.checklist_items[0],
            # available values
            values=self.checklist_items,
            # positioning
            size_hint=(1, 0.1),
            pos_hint={'center_x': .5, 'center_y': .5})
        b.add_widget(self.checklist_selector)

        self.title_label = Label(text="Welcome", font_size=30)
        b.add_widget(self.title_label)

        checkbtn = Button(text='Next', size_hint=(1,0.2))
        checkbtn.bind(on_release=self.show_next_checklist_item)
        b.add_widget(checkbtn)

        return b

    def show_next_checklist_item(self, obj):
        if not self.checklist_items:
            return # TODO: What do we do when we reach the end of the list?

        checklist_item = self.checklist_items.pop(0)
        self.title_label.text = checklist_item
        self.read_text(checklist_item)

    def read_text(self, text):
        if self.sound:
            self.sound.stop()
            self.sound.unload()

        audio_filename = get_audio_filename(text)
        if not os.path.exists(audio_filename):
            raise FileNotFoundError

        self.sound = SoundLoader.load(audio_filename)
        self.sound.play()


# Main ##################################################################################

if __name__ == "__main__":
    AudioChecklistApp().run()
