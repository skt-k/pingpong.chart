from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window


class GameWidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self._keyboard = Window.request_keyboard(
            self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        
        self._entities = set()
        

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        print('you click ', text, ' button')

    def add_entity(self, entity):
        self._entities.add(entity)
        self.canvas.add(entity._instruction)


class Entity(object):
    def __init__(self):
        self._pos = (0, 0)
        self._size = (100, 100)
        self._source = './assets/leaf.png'
        self._instruction = Rectangle(
            pos=self._pos, size=self._size, source=self._source)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self._instruction.pos = self._pos

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._instruction.size = self._size

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value
        self._instruction.source = self._source


class Player(Entity):
    def __init__(self):
        super().__init__()
        self.source = "./assets/nurse.png"
        self.pos = (400,100)


class PpcApp(App):
    def build(self):
        game = GameWidget()
        game.player = Player()
        game.add_entity(game.player)
        return game


if __name__ == '__main__':
    app = PpcApp()
    app.run()
