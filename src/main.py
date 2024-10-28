from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
import sqlite3
import hashlib


def initialize_database():
    conn = sqlite3.connect("wedding_app.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT
        )
    """)
    conn.commit()
    conn.close()

class MainWidget(Widget):
    pass

# stworzenie ekranu głownego
class HomeScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class SignUpScreen(Screen):
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
        initialize_database()
        # wczytanie pliku .kv
        return Builder.load_file('wedding.kv')
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def on_start(self):
        self.update_login_buttons()

    def login(self, username, password):
        hashed_password = self.hash_password(password)
        conn = sqlite3.connect("wedding_app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = cursor.fetchone()
        conn.close()
        if user:
            self.is_logged_in = True
            self.update_login_buttons()
            print("zalogowano pomyslnie")
        else:
            print("Nieprawidłowa nazwa uzytkownika lub haslo")

    
    def sign_up(self, username, password):
        hashed_password = self.hash_password(password)
        conn = sqlite3.connect("wedding_app.db")
        cursor = conn.cursor()
        try: 
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            self.is_logged_in = True
            self.update_login_buttons()
            print("rejestracja zakonczona sukcesem")
        except sqlite3.IntegrityError:
            print("Uzytkownik o tej nazwie juz istnieje")
        finally:
            conn.close()


    def log_out(self):
        self.is_logged_in = False
        self.update_login_buttons()
        self.root.current = 'home'

    def update_login_buttons(self):
        home_screen = self.root.get_screen('home')
        login_button = home_screen.ids.login_button
        signup_button = home_screen.ids.signup_button
        logout_button = home_screen.ids.logout_button

        if self.is_logged_in:
            login_button.opacity = 0  # ukryj przycisk logowania
            signup_button.opacity = 0  # ukryj przycisk rejestracji
            logout_button.opacity = 1  # wyświetl przycisk wylogowania
        else:
            login_button.opacity = 1  
            signup_button.opacity = 1 
            logout_button.opacity = 0



    


if __name__ == "__main__":
    WeddingApp().run()
