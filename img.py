from kivymd.uix.card import MDCard
from kivy.uix.button import ButtonBehavior
from kivymd.app import MDApp
from plyer import filechooser
from kivy.properties import ObjectProperty
import os


class ImgWidget(MDCard):
    pass

class MainImg(MDCard, ButtonBehavior):
    selection = ObjectProperty()

    def on_press(self):
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        self.selection = selection

    def on_selection(self, *args):
        if self.selection:
            file_path = str(self.selection[0])
            self.ids['img'].source = file_path
        MDApp.get_running_app().setdir()