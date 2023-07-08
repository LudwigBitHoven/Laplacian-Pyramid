from kivymd.app import MDApp
from kivy.lang import Builder
from processor import ImgProcessor
from kivy.uix.gridlayout import GridLayout
from img import ImgWidget
from kivy.graphics.texture import Texture
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
import numpy as np
import os


class MainLayout(GridLayout):
    pass


class Laplas(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.processor = ImgProcessor()
        self.path = os.path.dirname(os.path.abspath(__file__))

    def build(self):
        self.load_kvs()
        self.root = MainLayout()
        self.theme_cls.material_style = "M2"
        return self.root

    def load_kvs(self):
        Builder.load_file('kv/data.kv')
        Builder.load_file('kv/img_widgets.kv')

    def setdir(self):
        os.chdir(self.path)

    def BuildPyramid(self):
        path = self.root.ids['img_frame'].ids['img'].source
        img = self.processor.open_img(path)
        from io import BytesIO
        result = self.processor.lap_pyramid(img)
        result = self.processor.img_to_byte(result)
        w, h, rgb = result[0].shape
        for img in result:
            buf = bytes(img)
            texture = Texture.create(size=(h, w))
            texture.blit_buffer(buf, colorfmt='rgb')
            texture.flip_vertical()
            temp = Image()
            temp.texture = CoreImage(texture).texture
            temp.texture = temp.texture
            temp2 = ImgWidget()
            temp2.add_widget(temp)
            self.root.ids['result_scroll'].add_widget(temp2)

if __name__ == '__main__':
    Laplas().run()