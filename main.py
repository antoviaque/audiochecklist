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

from checklist import get_all_checklists, get_audio_filename


# Configuration & constants #############################################################

config = configparser.ConfigParser()
config.read('audiochecklist.cfg')
config = config['AudioChecklist']


# Classes ###############################################################################

class AudioChecklistApp(App):
    def __init__(self, *args, **kwargs):
        super(AudioChecklistApp, self).__init__(*args, **kwargs)
        self.sound = None
        self.selected_checklist_name = None
        self.buttons = []
        self.update_checklist_items()

    def get_checklists_names(self):
        return [checklist.heading for checklist in get_all_checklists().children]

    def build(self):
        self.body = BoxLayout(orientation='vertical', spacing=10, width=1600, height=900)

        self.build_checklist_selector()
        self.build_checklist_body()
        self.build_check_button()
        
        return self.body

    def build_checklist_selector(self):
        """
        Layout: Checklist selector dropdown
        """
        self.checklist_selector = Spinner(
            # default value shown
            text=self.selected_checklist_name,
            # available values
            values=self.get_checklists_names(),
            # positioning
            size_hint=(1, 0.1),
            pos_hint={'center_x': .5, 'center_y': .5})
        self.body.add_widget(self.checklist_selector)

        def on_selected_checklist_change(spinner, text):
            print('Checklist changed by user to', text)
            self.selected_checklist_name = text
            self.update_checklist_items()
            self.reset_checklist_items_buttons()
            self.show_next_checklist_item(None)

        self.checklist_selector.bind(text=on_selected_checklist_change)

    def build_checklist_body(self):
        """
        Layout: Checklist body - list of items
        """
        self.checklist_items_buttons_box = BoxLayout(orientation='vertical', spacing=10, width=1600)
        self.body.add_widget(self.checklist_items_buttons_box)
        self.reset_checklist_items_buttons()

    def build_check_button(self):
        """
        Layout: Check button - Mark item as done
        """
        self.checkbtn = Button(text='Next', size_hint=(1,0.2))
        self.checkbtn.bind(on_release=self.show_next_checklist_item)
        self.body.add_widget(self.checkbtn)

    def update_checklist_items(self):
        """
        Update the current list of items in the checklist, based on `self.selected_checklist_name`
        """
        all_checklists = get_all_checklists()
        if self.selected_checklist_name is None:
            self.selected_checklist_name = all_checklists.children[0].heading
        
        # Find the checklist with the same name
        print('Updating checklist items from selected checklist', self.selected_checklist_name)
        for checklist in all_checklists.children:
            if self.selected_checklist_name == checklist.heading:
                self.selected_checklist = checklist
                self.selected_checklist_items = [item.heading for item in checklist][1:]
                self.selected_checklist_items_done = []
                self.current_item_name = None
                print('Refreshed checklist items from selected checklist', self.selected_checklist_name)
                print('Checklist items:', self.selected_checklist_items)

    def reset_checklist_items_buttons(self):
        # Clear existing buttons
        for button in self.buttons:
            self.checklist_items_buttons_box.remove_widget(button)
        self.buttons = []

        for checklist_item in self.selected_checklist_items:
            button = Button(text=checklist_item, size_hint=(1,0.02), halign='left')#, text_size=(1,1))
            button.text_size = [self.body.width, None]
            def callback(instance):
                print('The button <%s> is being pressed' % instance.text)
            button.bind(on_press=callback)
            self.buttons.append(button)
            self.checklist_items_buttons_box.add_widget(button)

    def show_next_checklist_item(self, obj):
        if not self.selected_checklist_items:
            return # TODO: What do we do when we reach the end of the list?

        done_item_name = self.current_item_name
        self.selected_checklist_items_done.append(done_item_name)
        self.current_item_name = self.selected_checklist_items.pop(0)

        if done_item_name is not None:
            done_item_button = self.find_button_by_name(done_item_name)
            done_item_button.disabled = True
            done_item_button.state = 'normal'

        current_item_button = self.find_button_by_name(self.current_item_name)
        current_item_button.state = 'down'
        
        self.read_text(self.current_item_name)

    def find_button_by_name(self, name):
        for button in self.buttons:
            if button.text == name:
                return button
        else:
            raise IndexError(name)

    def read_text(self, text):
        if self.sound:
            self.sound.stop()
            self.sound.unload()

        audio_filename = get_audio_filename(text)
        if not os.path.exists(audio_filename):
            raise FileNotFoundError(audio_filename)

        self.sound = SoundLoader.load(audio_filename)
        self.sound.play()



# Main ##################################################################################

if __name__ == "__main__":
    AudioChecklistApp().run()
