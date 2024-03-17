from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, ListProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
import random

class HomePage(Screen):
    def __init__(self, game_widget, **kwargs):
        super(HomePage, self).__init__(**kwargs)
        self.game_widget = game_widget
        layout = BoxLayout(orientation = "vertical", spacing=10, padding=200)
        self.greeting = Label(text="Ping Pong Charge", font_size=50, color=(1, 0.6, 0.48))
        self.startButton = Button(text='Start to Play', on_press=self.go_to_game, font_size=30)
        
        layout.add_widget(self.greeting)
        layout.add_widget(self.startButton)
        self.add_widget(layout)
    
    def go_to_game(self, instance):
        self.game_widget.can_play="canclick"
        self.manager.current = 'GameScreen'

class GameScreen(Screen):
    def __init__(self, game_widget, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game_widget = game_widget
        self.add_widget(self.game_widget)

class WinScreen(Screen):
    def __init__(self, **kwargs):
        super(WinScreen,self).__init__(**kwargs)

        layout=BoxLayout(orientation="vertical",spacing=10,padding=200)

        message_label = Label(text="Congratulations! Yon Win!", font_size=30, color=(0,1,0))
        back_button = Button(text="Back to Home", on_press=self.go_to_home, font_size=20)

        layout.add_widget(message_label)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_to_home(self,instance):
        self.manager.current="HomePage"

class LoseScreen(Screen):
    def __init__(self, **kwargs):
        super(LoseScreen,self).__init__(**kwargs)

        layout=BoxLayout(orientation="vertical",spacing=10,padding=200)

        message_label = Label(text="Game Over! You Lose!", font_size=30, color=(1,0,0))
        back_button = Button(text="Back to Home", on_press=self.go_to_home, font_size=20)

        layout.add_widget(message_label)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_to_home(self,instance):
        self.manager.current = "HomePage"

class AttackPower(Widget):
    image_source = StringProperty('')
    velocity = NumericProperty(10)
    direction = NumericProperty(1)  # 1 for right, -1 for left    
            
    def move(self, dt):  # Add dt as an argument
        self.x += self.velocity * self.direction
        game_widget = self.parent
        #และก่อนใช้ attack_powers คุณควรตรวจสอบก่อนว่า game_widget ไม่ใช่ NoneType
        if game_widget and game_widget.attack_powers:
            for power in game_widget.attack_powers:
                if power != self : #ถ้าpower ไม่ใช่ตัวมันเอง
                    player_last_attack = game_widget.player.last_power
                    enemy_last_attack = game_widget.enemy.last_power
                    if self.direction == 1 and power.direction == -1:
                        if player_last_attack == 'mangkudkuan' and enemy_last_attack == 'pong': 
                            game_widget.check_collision(self, power,'break_power_player', self.pos) #เช็คว่าตัวมันเองชนกับpowerนี้อยู่มั้ย
                        elif player_last_attack == 'pong' and enemy_last_attack == 'mangkudkuan': 
                            game_widget.check_collision(self, power,'break_power_enemy', self.pos) #เช็คว่าตัวมันเองชนกับpowerนี้อยู่มั้ย
                    
                        else: 
                            game_widget.check_collision(self, power,'break_both',self.pos) #เช็คว่าตัวมันเองชนกับpowerนี้อยู่มั้ย
                        
                if power.direction == 1: #ถ้าพลังมาจากplayerเช็คการชนกับenemy
                    game_widget.check_enemy_collision(game_widget.enemy,power,game_widget.enemy.pos)
                    
                if power.direction == -1: #ถ้าพลังมาจากenemyเช็คการชนกับplayer
                    if game_widget.player.last_power == 'shield': #ถ้าออกท่าป้องกันมาก็เช็คการชนแบบไม่ลดเลือด
                        game_widget.check_player_collision_not_hurt(game_widget.player,power,game_widget.player.pos)
                    elif game_widget.player.last_power == 'ghost':
                        game_widget.check_player_collision_not_hurt(game_widget.player,power,game_widget.player.pos)
                    else:
                        game_widget.check_player_collision(game_widget.player,power,game_widget.player.pos)
                    

class Health(Widget):
    def __init__(self):
        super().__init__()                  
            
class Player(Widget):
    energy = NumericProperty(100)
    health = NumericProperty(5)
    image_source = StringProperty('./assets/PPP.png')
    last_power = StringProperty('')
    healthPosition = NumericProperty(110)
    health_widgets = ListProperty([])
    # game_widget = self.parent
    
    def prepare_attack(self):
        self.image_source = './assets/PPP.png'
        

    def release_power(self, attack_command):# เช็คพลังงานและปล่อยพลัง
        if self.energy >= 0:  
            if attack_command == 'charge':
                self.energy += 1
                self.image_source = './assets/PlayerCharge.png'
                self.last_power = 'charge'
                self.parent.stage = 'attacking' #เปลี่ยนstageเมื่อผู้เล่นปล่อยท่าได้

            elif attack_command == 'supercharge' and self.energy >= 3:
                self.energy += 2
                self.image_source = './assets/PlayerSuperCharge.png'
                self.last_power = 'supercharge'
                self.parent.stage = 'attacking'

            elif attack_command == 'shield':
                self.image_source = './assets/PlayerShield.png'
                self.last_power = 'shield'
                self.parent.stage = 'attacking' #เปลี่ยนstageเมื่อผู้เล่นปล่อยท่าได้
                
            elif attack_command == 'ghost':
                self.image_source = './assets/Ghost.png'
                self.last_power = 'ghost'
                self.parent.stage = 'attacking' #เปลี่ยนstageเมื่อผู้เล่นปล่อยท่าได้
                
            elif attack_command == 'mangkudkuan' and self.energy >= 1:
                self.energy -= 1
                self.image_source = './assets/PlayerS.png'
                self.parent.release_attack_power(self.center_x, self.center_y, 1,attack_command) #กำหนดตำแหน่งปล่อยพลังจากตำแหน่งที่ตัวละครยืนอยู่
                self.last_power = attack_command
                self.parent.stage = 'attacking' #เปลี่ยนstageเมื่อผู้เล่นปล่อยท่าได้
            elif attack_command == 'pong' and self.energy >= 2:
                self.energy -= 2
                self.image_source = './assets/PlayerS.png'
                self.parent.release_attack_power(self.center_x, self.center_y, 1,attack_command) 
                self.last_power = attack_command
                self.parent.stage = 'attacking' #เปลี่ยนstageเมื่อผู้เล่นปล่อยท่าได้
        
    def update_health_widgets(self):
        for widget in self.health_widgets:
            self.parent.remove_widget(widget)
        self.health_widgets = []
        self.healthPosition = 110
        for i in range(self.health):
            health_obj = Health()
            health_obj.center =(200 + self.healthPosition, 600)
            self.parent.add_widget(health_obj)
            self.health_widgets.append(health_obj)
            self.healthPosition += 110

class Enemy(Widget):
    energy = NumericProperty(100)
    health = NumericProperty(5)
    image_source = StringProperty('./assets/EPP.png')
    last_power = StringProperty('')
    healthPosition = NumericProperty(110)
    health_widgets = ListProperty([])
    
    def prepare_attack(self):
        self.image_source = './assets/EPP.png'
    
        
    def enemy_random_attack(self): #บอทสุ่มท่า
        if self.energy == 0:
            random_power = ['charge']
        elif self.energy == 1:
            random_power = ['charge','mangkudkuan']
        elif self.energy >= 2:
            random_power = ['charge','mangkudkuan','pong']
        attack = random.choice(random_power)
        print('enemy_random',attack)
        self.release_power(attack) #ส่งคำสั่งปล่อยท่าไปให้บอท

    def release_power(self, attack_command):# เช็คคำสั่งพลังงานและปล่อยพลัง
        if self.energy >= 0:
            if attack_command == 'charge':
                self.energy += 1
                self.image_source = './assets/EnemyCharge.png'
                self.last_power = 'charge'

            elif attack_command == 'supercharge' and self.energy >= 3:
                self.energy += 2
                self.image_source = './assets/EnemySuperCharge.png'
                self.last_power = 'supercharge'
                
            elif attack_command == 'mangkudkuan' and self.energy >= 1:
                self.energy -= 1
                self.image_source = './assets/rightplayerattack.png'
                self.parent.release_attack_power(self.center_x, self.center_y, -1,attack_command) #กำหนดตำแหน่งปล่อยพลังจากตำแหน่งที่ตัวละครยืนอยู่
                self.last_power = 'mangkudkuan'
            elif attack_command == 'pong' and self.energy >= 2:
                self.energy -= 2
                self.image_source = './assets/rightplayerattack.png'
                self.parent.release_attack_power(self.center_x, self.center_y, -1,attack_command) 
                self.last_power = 'pong'
    def update_health_widgets(self):
        for widget in self.health_widgets:
            self.parent.remove_widget(widget)
        self.health_widgets = []
        self.healthPosition = 110
        for i in range(self.health):
            health_obj = Health()
            health_obj.center = (1110 + self.healthPosition, 600)
            self.parent.add_widget(health_obj)
            self.health_widgets.append(health_obj)
            self.healthPosition += 110



class ExplosionPower(Widget):
    image_source = StringProperty('./assets/explosion.png')
    sound_source = StringProperty('./assets/punch.wav')
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        sound = SoundLoader.load(self.sound_source)
        sound.play()
        Clock.schedule_once(self._remove_me, 0.3)
    
    def _remove_me(self,dt):
        self.parent.remove_widget(self)
        

class ExplosionPlayer(Widget):
    image_source = StringProperty('./assets/p_explosion.png')
    sound_source = StringProperty('./assets/toom.wav')
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        sound = SoundLoader.load(self.sound_source)
        sound.play()
        Clock.schedule_once(self._remove_me,0.3)

    def _remove_me(self,dt):
        self.parent.remove_widget(self)
        
class ExplosionPlayerNotHurt(Widget):
    image_source = StringProperty('./assets/p_explosion.png')
    sound_source = StringProperty('./assets/light.wav')
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        sound = SoundLoader.load(self.sound_source)
        sound.play()
        Clock.schedule_once(self._remove_me,0.3)

    def _remove_me(self,dt):
        self.parent.remove_widget(self)

class GameWidget(Widget):
    player = ObjectProperty(None)
    enemy = ObjectProperty(None)
    attack_powers = []
    stage = StringProperty('prepare') #stage เริ่มต้น
    can_play = StringProperty('cannotclick') 
    not_attack = ListProperty(['charge','supercharge','shield','ghost'])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self.show_health()

    def show_health(self):
        self.player.update_health_widgets()
        self.enemy.update_health_widgets()

    def reset_game(self):
        self.can_play = "cannotclick"
        self.stage = "prepare"
        self.player.image_source = './assets/PPP.png'
        self.player.energy = 100
        self.player.health = 5

        self.enemy.image_source = "./assets/EPP.png"
        self.enemy.energy = 100
        self.enemy.health = 5

        self.player.last_power = ''
        self.enemy.last_power = ''

        self.player.update_health_widgets()
        self.enemy.update_health_widgets()

        self.attack_powers = []

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None
    

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if self.can_play == 'canclick':
            if text == 'a':
                if self.stage == 'attack_finish': #ต้อง attackfinish ก่อนถึงจะกด a เพื่อเปลี่ยน stage ได้
                    self.player.prepare_attack()
                    self.enemy.prepare_attack()
                    print('stage change to prepare')
                    self.stage = 'prepare' #เปลี่ยนstage
                    
            if self.stage == 'prepare':
                if text == 'j':
                    self.player.release_power('charge')
                    
                elif text == 'u':
                    self.player.release_power('supercharge')

                elif text == 'i':
                    self.player.release_power('shield')
                    
                elif text == 'k':
                    self.player.release_power('mangkudkuan')#ปล่อยพลังงานA
                    
                elif text == 'l':
                    self.player.release_power('pong')#ปล่อยพลังงานA
                    
                elif text == 'o':
                    self.player.release_power('ghost')
                    
                if self.stage == 'attacking': #ให้ผู้เล่นปล่อยท่าได้ก่อนบอทถึงจะค่อยสุ่มออกท่า
                        self.enemy.enemy_random_attack()#ปล่อยพลังงานB
                        self.check_not_attack_both()#เช็คว่าไม่ได้โจมตีทั้งสองฝั่งมั้ย
            
                
    def check_not_attack_both(self):#เช็คว่าไม่ปล่อยพลังทั้งสองฝ่ายมั้ย
        if self.player.last_power in self.not_attack and self.enemy.last_power in self.not_attack:
            self.stage = 'attack_finish'
        
        
    def release_attack_power(self, x, y, direction, attack_command):
        attack_power = AttackPower()
        attack_power.center = (x, y)
        attack_power.direction = direction
        if attack_command == 'mangkudkuan':
            attack_power.image_source = './assets/KH.png'
        elif attack_command == 'pong':
            attack_power.image_source = './assets/Pong.png'
        self.add_widget(attack_power)
        self.attack_powers.append(attack_power)
        Clock.schedule_interval(attack_power.move, 1 / 120)
    
        
    def remove_attack_power(self, attack_power):
        self.remove_widget(attack_power)
        self.attack_powers.remove(attack_power)

    def on_touch_down(self, touch):
        pass
    
    #ฟังชันตรวจจับการชน
    def collides(self, obj1, obj2):
        r1x = obj1.x
        r1y = obj1.y
        r2x = obj2.x
        r2y = obj2.y
        r1w = obj1.width
        r1h = obj1.height
        r2w = obj2.width
        r2h = obj2.height

        if (r1x < r2x + r2w and r1x+r1w>r2x and r1y<r2y+r2h and r1y+r1h>r2y):
            return True
        else:
            return False
    
    def check_collision(self, power_a, power_b, command, power_position):
        if self.collides(power_a, power_b): #ใช้ฟังชันตรวจสอบการชนกับวัตถุสองอย่าง
            print("Collision detected between power A and power B")
            explosion_effect = ExplosionPower(power_position)
            self.add_widget(explosion_effect)
            if command == 'break_power_player':
                self.remove_attack_power(power_a)
            elif command == 'break_power_enemy':
                self.remove_attack_power(power_b)
            elif command == 'break_both':
                self.remove_attack_power(power_a)
                self.remove_attack_power(power_b)
                self.stage = 'attack_finish' #เปลี่ยนstage
                  
    def check_player_collision(self, player, power, power_position):
        if self.collides(player, power):
            explosion_effect = ExplosionPlayer(power_position)
            self.add_widget(explosion_effect)
            print("Player collided with power")
            self.remove_attack_power(power)
            self.stage = 'attack_finish' #เปลี่ยนstage
            self.player.health -= 1
            self.show_health()
            if self.player.health == 0:
                self.reset_game()
                App.get_running_app().root.current = "LoseScreen"
            
    def check_player_collision_not_hurt(self, player, power, power_position):
        if self.collides(player, power):
            explosion_effect = ExplosionPlayerNotHurt(power_position)
            self.add_widget(explosion_effect)
            print("Player collided with power")
            self.remove_attack_power(power)
            self.stage = 'attack_finish' #เปลี่ยนstage
            
            
    def check_enemy_collision(self, enemy, power, power_position):
        if self.collides(enemy, power):
            explosion_effect = ExplosionPlayer(power_position)
            self.add_widget(explosion_effect)
            print("Enemy collided with power")
            self.remove_attack_power(power)
            self.stage = 'attack_finish' #เปลี่ยนstage
            self.enemy.health -= 1
            self.show_health()
            if self.enemy.health == 0:
                self.reset_game()
                App.get_running_app().root.current = "WinScreen"

      

class PpcApp(App):
    def build(self):
        game_widget = GameWidget()
        game = ScreenManager()
        home_page = HomePage(name='HomePage',game_widget=game_widget)
        game_screen = GameScreen(name='GameScreen',game_widget=game_widget)
        win_screen = WinScreen(name='WinScreen')
        lose_screen = LoseScreen(name='LoseScreen')

        game.add_widget(home_page)
        game.add_widget(game_screen)
        game.add_widget(win_screen)
        game.add_widget(lose_screen)
        return game

if __name__ == '__main__':
    PpcApp().run()