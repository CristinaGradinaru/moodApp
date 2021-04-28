from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from datetime import datetime

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

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()

