from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window

class GameWidget(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_key_down)

        with self.canvas:
            Rectangle(pos=(0,0),size=(100,100))

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self,keyboard,keycode,text,modifiers):
        print('you click ',text,' button')

        

class PccApp(App):
    def build(self):
        return GameWidget()

if __name__ == '__main__':
    app = PccApp()
    app.run()

