from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder


class MainWidget(Widget):
    pass

# stworzenie ekranu głownego
class HomeScreen(Screen):
    pass

# stworzenie ekranu harmonogramu
class ScheduleScreen(Screen):
    pass

# tworzenie managera ekranow
class ScreenManagement(ScreenManager):
    pass



# aplikacja główna
class WeddingApp(MDApp):
    is_logged_in = False

    def build(self):
        # wczytanie pliku .kv
        return Builder.load_file('wedding.kv')
    
    def on_start(self):
        self.update_login_buttons()

    def login(self):
        self.is_logged_in = True
        self.update_login_buttons()
    
    def sign_up(self):
        print("Konto zostało utworzone")

    def log_out(self):
        self.is_logged_in = False
        self.update_login_buttons()

    def update_login_buttons(self):
        login_button = self.root.ids.home.ids.login_button
        signup_button = self.root.ids.home.ids.signup_button
        logout_button = self.root.ids.home.ids.logout_button


        if self.is_logged_in:
            login_button.opacity = 0  # ukryj przycisk logowania
            signup_button.opacity = 0  # ukryj przycisk rejestracji
            logout_button .opacity= 1 # wyswietla przycisk wylogowania
        else:
            login_button.opacity = 1  
            signup_button.opacity = 1 
            logout_button.opacity = 0 


    


if __name__ == "__main__":
    WeddingApp().run()
