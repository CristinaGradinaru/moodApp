from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob, random
from datetime import datetime
from pathlib import Path
from hoverable import HoverBehavior

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def signup(self):
        self.manager.current= "signup_screen"
    
    def login(self, username, password):
        with open('users.json') as file:
            users= json.load(file)
            if username in users and users[username]['password'] == password:
                self.manager.current= "login_success"
            else:
                self.ids.login_wrong.text = "Wrong Username or Password!"

class LoginSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction= "right"
        self.manager.current= "login_screen"

    def get_quote(self, feels):
        feel = feels.lower()
        feeling_list= glob.glob("quotes/*txt")
        feeling_list = [Path(filename).stem for filename in feeling_list]
        if feel in feeling_list:
            with open(f'quotes/{feel}.txt') as file:
                quotes = file.readlines()
            print(quotes)
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text="Try another feeling!"

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def adduser(self, username, password):
        # open json file
        with open("users.json") as file:
            users=json.load(file)
        # add new username to the file
        users[username]={'username': username, 'password': password, 'created': datetime.now().strftime('%Y-%m-%d %H-%M-%S')}
        # rewrite the existing json file plus the new user
        with open('users.json', 'w') as file:
            json.dump(users, file)

        self.manager.current='sign_up_success'

class SignUpSuccess(Screen):
    def renderlogin(self):
        self.manager.transition.direction= "right"
        self.manager.current= "login_screen"

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()

