from kivymd.app import MDApp
from kivy.lang import Builder
from processor import ImgProcessor
from kivy.uix.gridlayout import GridLayout
from img import ImgWidget
from kivy.graphics.texture import Texture
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy import platform
from io import BytesIO
import numpy as np
import os

from functools import partial


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

    def on_start(self):
        if platform == "android":
            from android.permissions import Permission, request_permissions
            from jnius import autoclass
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

    def load_kvs(self):
        Builder.load_file('kv/data.kv')
        Builder.load_file('kv/img_widgets.kv')

    def setdir(self):
        os.chdir(self.path)

    def TriggerBuilding(self):
        self.root.ids['result_scroll'].clear_widgets()
        Clock.schedule_once(self.BuildPyramid)

    def BuildPyramid(self, *args):
        path = self.root.ids['img_frame'].ids['img'].source
        start_img = self.processor.open_img(path)
        result = self.processor.lap_pyramid(start_img)
        Clock.schedule_once(partial(self.DrawPyramid, result), 0)

    def DrawPyramid(self, result, *args):
        result = self.processor.img_to_byte(result)
        w, h, rgb = result[0].shape
        for img in result:
            Clock.schedule_once(partial(self.DrawWidget, img, w, h), 0.5)

    def DrawWidget(self, img, w, h, p):
        buf = bytes(img)
        texture = Texture.create(size=(h, w))
        texture.blit_buffer(buf, colorfmt='rgb')
        texture.flip_vertical()
        temp = Image()
        temp.texture = CoreImage(texture).texture
        temp2 = ImgWidget()
        temp2.add_widget(temp)
        self.root.ids['result_scroll'].add_widget(temp2)

    def SaveImages(self):
        content = self.root.ids['result_scroll'].children
        for i, j in enumerate(content):
            j.export_to_png(f"laplacian/{i}_laplacian.png")


if __name__ == '__main__':
    Laplas().run()