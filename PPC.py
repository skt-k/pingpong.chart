from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,ObjectProperty,StringProperty
from kivy.core.window import Window
from kivy.uix.image import Image

class Player(Widget):
    energy = NumericProperty(3)
    image_source = StringProperty('./assets/leaf.png')
    
    def increase_energy(self):    
        self.energy += 1
        self.image_source = './assets/hot.png'
    def decrease_energy(self):
        self.energy -= 1
        self.image_source = './assets/leaf.png'
    
class Enemy(Widget):
    energy = NumericProperty(3)
    image_source = StringProperty('./assets/leaf2.png')
    
    def increase_energy(self):    
        self.energy += 1
        self.image_source = './assets/nurse.png'
    def decrease_energy(self):
        self.energy -= 1
        self.image_source = './assets/leaf2.png'

class GameWidget(Widget):
    player = ObjectProperty(None)
    enemy = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self,keyboard,keycode,text,modifiers):
        print('you press ', text)
        if text == 'j':
            self.player.increase_energy() 
            self.enemy.increase_energy()
        if text == 'k':
            self.player.decrease_energy()
            self.enemy.decrease_energy()



class PpcApp(App):
    def build(self):
        game = GameWidget()
        return game


if __name__ == '__main__':
    PpcApp().run()

