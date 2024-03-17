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
import random

class HomePage(Screen):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(**kwargs)
        layout = BoxLayout(orientation = "vertical", spacing=10, padding=20)
        self.greeting = Label(text="Welcome", font_size=20, color=(1, 0.6, 0.48))
        self.startButton = Button(text='Start to Play', on_press=self.go_to_game, font_size=30, size_hint=(None, None), size=(350, 50))
        
        layout.add_widget(self.greeting)
        layout.add_widget(self.startButton)
        self.add_widget(layout)
    
    def go_to_game(self, instance):
        self.manager.current = 'GameScreen'


class AttackPower(Widget):
    image_source = StringProperty('./assets/power.png')
    velocity = NumericProperty(5)
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
                    if player_last_attack == 'hadoken' and enemy_last_attack == 'gun': 
                        game_widget.check_collision(self, power,'break_power_player') #เช็คว่าตัวมันเองชนกับpowerนี้อยู่มั้ย
                    elif player_last_attack == 'gun' and enemy_last_attack == 'hadoken': 
                        game_widget.check_collision(self, power,'break_power_enemy') #เช็คว่าตัวมันเองชนกับpowerนี้อยู่มั้ย
                    
                    else: 
                        game_widget.check_collision(self, power,'break_both') #เช็คว่าตัวมันเองชนกับpowerนี้อยู่มั้ย
                        
                if power.direction == 1: #ถ้าพลังมาจากplayerเช็คการชนกับenemy
                    game_widget.check_enemy_collision(game_widget.enemy,power)
                    
                if power.direction == -1: #ถ้าพลังมาจากenemyเช็คการชนกับplayer
                    if game_widget.player.last_power == 'shield': #ถ้าออกท่าป้องกันมาก็เช็คการชนแบบไม่ลดเลือด
                        game_widget.check_player_collision_not_hurt(game_widget.player,power)
                    else:
                        game_widget.check_player_collision(game_widget.player,power)
                    
            
class Player(Widget):
    energy = NumericProperty(3)
    health = NumericProperty(3)
    image_source = StringProperty('./assets/PPP.png')
    last_power = StringProperty('')
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
                
            elif attack_command == 'shield':
                self.image_source = './assets/shield.png'
                self.last_power = 'shield'
                self.parent.stage = 'attacking' #เปลี่ยนstageเมื่อผู้เล่นปล่อยท่าได้
                
            elif attack_command == 'hadoken' and self.energy >= 1:
                self.energy -= 1
                self.image_source = './assets/leftplayerattack.png'
                self.parent.release_attack_power(self.center_x, self.center_y, 1,attack_command) #กำหนดตำแหน่งปล่อยพลังจากตำแหน่งที่ตัวละครยืนอยู่
                self.last_power = attack_command
                self.parent.stage = 'attacking' #เปลี่ยนstageเมื่อผู้เล่นปล่อยท่าได้
            elif attack_command == 'gun' and self.energy >= 2:
                self.energy -= 2
                self.image_source = './assets/leftplayerattack.png'
                self.parent.release_attack_power(self.center_x, self.center_y, 1,attack_command) 
                self.last_power = attack_command
                self.parent.stage = 'attacking' #เปลี่ยนstageเมื่อผู้เล่นปล่อยท่าได้
        
class Enemy(Widget):
    energy = NumericProperty(3)
    health = NumericProperty(3)
    image_source = StringProperty('./assets/EPP.png')
    last_power = StringProperty('')
    
    
    def prepare_attack(self):
        self.image_source = './assets/EPP.png'
    
        
    def enemy_random_attack(self): #บอทสุ่มท่า
        if self.energy == 0:
            random_power = ['charge']
        elif self.energy == 1:
            random_power = ['charge','hadoken']
        elif self.energy >= 2:
            random_power = ['charge','hadoken','gun']
        attack = random.choice(random_power)
        print('enemy_random',attack)
        self.release_power(attack) #ส่งคำสั่งปล่อยท่าไปให้บอท

    def release_power(self, attack_command):# เช็คคำสั่งพลังงานและปล่อยพลัง
        if self.energy >= 0:
            if attack_command == 'charge':
                self.energy += 1
                self.image_source = './assets/EnemyCharge.png'
                self.last_power = 'charge'
            elif attack_command == 'hadoken' and self.energy >= 1:
                self.energy -= 1
                self.image_source = './assets/rightplayerattack.png'
                self.parent.release_attack_power(self.center_x, self.center_y, -1,attack_command) #กำหนดตำแหน่งปล่อยพลังจากตำแหน่งที่ตัวละครยืนอยู่
                self.last_power = 'hadoken'
            elif attack_command == 'gun' and self.energy >= 2:
                self.energy -= 2
                self.image_source = './assets/rightplayerattack.png'
                self.parent.release_attack_power(self.center_x, self.center_y, -1,attack_command) 
                self.last_power = 'gun'
                
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game_widget = GameWidget()
        self.add_widget(self.game_widget)



class GameWidget(Widget):
    player = ObjectProperty(None)
    enemy = ObjectProperty(None)
    attack_powers = []
    stage = StringProperty('prepare') #stage เริ่มต้น
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None
    

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if text == 'a':
            if self.stage == 'attack_finish': #ต้อง attackfinish ก่อนถึงจะกด a เพื่อเปลี่ยน stage ได้
                self.player.prepare_attack()
                self.enemy.prepare_attack()
                print('stage change to prepare')
                self.stage = 'prepare' #เปลี่ยนstage
                
        if self.stage == 'prepare':
            if text == 'j':
                self.player.release_power('charge')
                
            elif text == 'i':
                self.player.release_power('shield')
                
            elif text == 'k':
                self.player.release_power('hadoken')#ปล่อยพลังงานA
                
            elif text == 'l':
                self.player.release_power('gun')#ปล่อยพลังงานA
                
            if self.stage == 'attacking': #ให้ผู้เล่นปล่อยท่าได้ก่อนบอทถึงจะค่อยสุ่มออกท่า
                    self.enemy.enemy_random_attack()#ปล่อยพลังงานB
                    self.check_not_attack_both()#เช็คว่าไม่ได้โจมตีทั้งสองฝั่งมั้ย
        
                
    def check_not_attack_both(self):#เช็คว่าไม่ปล่อยพลังทั้งสองฝ่ายมั้ย
        if self.player.last_power == 'charge' and self.enemy.last_power == 'charge':
            self.stage = 'attack_finish'
        elif self.player.last_power == 'shield' and self.enemy.last_power == 'charge':
            self.stage = 'attack_finish'
        
    def release_attack_power(self, x, y, direction, attack_command):
        attack_power = AttackPower()
        attack_power.center = (x, y)
        attack_power.direction = direction
        if attack_command == 'hadoken':
            attack_power.image_source = './assets/power.png'
        elif attack_command == 'gun':
            attack_power.image_source = './assets/gun.png'
        self.add_widget(attack_power)
        self.attack_powers.append(attack_power)
        Clock.schedule_interval(attack_power.move, 1 / 60)
    
        
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
    
    def check_collision(self, power_a, power_b, command):
        if self.collides(power_a, power_b): #ใช้ฟังชันตรวจสอบการชนกับวัตถุสองอย่าง
            print("Collision detected between power A and power B")
            if command == 'break_power_player':
                self.remove_attack_power(power_a)
            elif command == 'break_power_enemy':
                self.remove_attack_power(power_b)
            elif command == 'break_both':
                self.remove_attack_power(power_a)
                self.remove_attack_power(power_b)
                self.stage = 'attack_finish' #เปลี่ยนstage
                  
    def check_player_collision(self, player, power):
        if self.collides(player, power):
            print("Player collided with power")
            self.remove_attack_power(power)
            self.stage = 'attack_finish' #เปลี่ยนstage
            self.player.health -= 1
            
    def check_player_collision_not_hurt(self, player, power):
        if self.collides(player, power):
            print("Player collided with power")
            self.remove_attack_power(power)
            self.stage = 'attack_finish' #เปลี่ยนstage
            
            
    def check_enemy_collision(self, enemy, power):
        if self.collides(enemy, power):
            print("Enemy collided with power")
            self.remove_attack_power(power)
            self.stage = 'attack_finish' #เปลี่ยนstage
            self.enemy.health -= 1
            
        

class PpcApp(App):
    def build(self):
        game = ScreenManager()
        game.add_widget(HomePage(name='HomePage'))
        game.add_widget(GameScreen(name='GameScreen'))
        return game

if __name__ == '__main__':
    PpcApp().run()