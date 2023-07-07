from kivymd.app import MDApp
from kivy.lang import Builder
from processor import ImgProcessor
from kivymd.uix.scrollview import ScrollView
import os

class Layout(ScrollView):
    pass

class Laplas(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.processor = ImgProcessor()
        self.path = os.path.dirname(os.path.abspath(__file__))

    def build(self):
        self.load_kvs()
        self.root = Layout()
        self.theme_cls.material_style = "M2"
        return self.root

    def load_kvs(self):
        Builder.load_file('kv/data.kv')

    def setdir(self):
        os.chdir(self.path)

if __name__ == '__main__':
    Laplas().run()