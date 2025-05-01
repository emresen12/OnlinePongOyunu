import kivy
import subprocess
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
Builder.load_file("interface.kv")
class MyLayout(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = SoundLoader.load("oyununarayüzsesi.mp3")
        if self.sound:
            self.sound.loop = True
            self.sound.volume = 0.5
            self.sound.play()
    def start_pong_game(self):
        subprocess.Popen(["python", "pong_game.py"])
class PongApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return MyLayout()
if __name__=='__main__':
    PongApp().run()