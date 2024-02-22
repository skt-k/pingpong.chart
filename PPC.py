from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

class GameWidget(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Rectangle(pos=(0,0),size=(100,100))

class PccApp(App):
    def build(self):
        return GameWidget()

if __name__ == '__main__':
    app = PccApp()
    app.run()

