from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image

class AttackPower(Widget):
    image_source = StringProperty('./assets/power.png')
    velocity = NumericProperty(5)
    direction = NumericProperty(1)  # 1 for right, -1 for left

    def move(self, dt):  # Add dt as an argument
        self.x += self.velocity * self.direction

class Player(Widget):
    energy = NumericProperty(3)
    image_source = StringProperty('./assets/leaf.png')

    def increase_energy(self):
        self.energy += 1
        self.image_source = './assets/leaf.png'

    def decrease_energy(self):
        self.energy -= 1
        self.image_source = './assets/hot.png'
        # Release attack power go to the Enemy (go to right)
        self.parent.release_attack_power(self.center_x, self.center_y, 1)

class Enemy(Widget):
    energy = NumericProperty(3)
    image_source = StringProperty('./assets/leaf2.png')

    def increase_energy(self):
        self.energy += 1
        self.image_source = './assets/leaf2.png'

    def decrease_energy(self):
        self.energy -= 1
        self.image_source = './assets/nurse.png'
        # Release attack power go to the Player (go to left)
        self.parent.release_attack_power(self.center_x, self.center_y, -1)

class GameWidget(Widget):
    player = ObjectProperty(None)
    enemy = ObjectProperty(None)
    attack_powers = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if text == 'j':
            self.player.increase_energy()
            self.enemy.increase_energy()
        if text == 'k':
            self.player.decrease_energy()
            self.enemy.decrease_energy()

    def release_attack_power(self, x, y, direction):
        attack_power = AttackPower()
        attack_power.center = (x, y)
        attack_power.direction = direction
        self.add_widget(attack_power)
        self.attack_powers.append(attack_power)
        print('attackpw',self.attack_powers)
        Clock.schedule_interval(attack_power.move, 1 / 60)

    def remove_attack_power(self, attack_power):
        self.remove_widget(attack_power)
        self.attack_powers.remove(attack_power)

    def on_touch_down(self, touch):
        pass

class PpcApp(App):
    def build(self):
        game = GameWidget()
        return game

if __name__ == '__main__':
    PpcApp().run()
