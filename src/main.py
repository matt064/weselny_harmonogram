from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime

import sqlite3
import hashlib


def initialize_database():
    conn = sqlite3.connect("wedding_app.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT,
        wedding_date TEXT DEFAULT NULL
        )""")
    conn.commit()
    conn.close()



class MainWidget(Widget):
    pass


# stworzenie ekranu głownego
class HomeScreen(Screen):
    pass


# tworzenie ekranu logowania
class LoginScreen(Screen):
    pass


# tworzenie ekranu rejestracji
class SignUpScreen(Screen):
    pass


# stworzenie ekranu harmonogramu
class ScheduleScreen(Screen):
    pass


# dodanie nowego zadania
class AddTaskScreen(Screen):
    pass


class ProfileScreen(Screen):
    pass


# tworzenie managera ekranow
class ScreenManagement(ScreenManager):
    pass



# aplikacja główna
class WeddingApp(MDApp):
    is_logged_in = False


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tasks = [
            {"name": "Znalezienie DJ", 'completed': False},
            {"name": "Ogarniecie fotografa", "completed": False},
            {"name": "Kupienie alkoholu", "completed": False}
        ]
        self.current_user = None


    def open_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save = self.set_wedding_date)
        date_dialog.open()


    def save_wedding_date(self):
        if self.current_user and self.wedding_date:
            conn = sqlite3.connect("wedding_app.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET wedding_date = ? WHERE username = ?", 
                (self.wedding_date, self.current_user)
            )
            conn.commit()
            conn.close()
            print(f"Wedding date saved successfully: {self.wedding_date}")


    def set_wedding_date(self, instance, value, date_range):
        "Wybor daty slubu"
        formatted_date = value.strftime("%d.%m.%Y")
        self.wedding_date = formatted_date
        # aktualizacja etykiety z data na ekranie profilu
        profile_screen = self.root.get_screen("profile")
        profile_screen.ids.wedding_date_label.text = f'Wedding date: {formatted_date}'

        self.save_wedding_date()


    def toggle_task(self, task_name):
        for task in self.tasks:
            if task['name'] == task_name:
                task['completed'] = not task['completed']
                return


    def build(self):
        initialize_database()
        # wczytanie pliku .kv tylko jeden raz
        if not hasattr(self, '_kv_loaded'):
            Builder.load_file('wedding.kv')
            self._kv_loaded = True
        return self.root
    

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    

    def on_start(self):
        self.update_login_buttons()
        self.update_task_list()


    def update_task_list(self):
        schedule_screen = self.root.get_screen('schedule')
        task_list = schedule_screen.ids.task_list

        # usuwa istniejace elementy z listy zadan
        task_list.clear_widgets()

        for task in self.tasks:
            # poziomy boxlayout dla kozdego zadania
            task_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')

            # checkbox
            checkbox = MDCheckbox(
                active = task['completed'],
                on_active = lambda x, task_name=task['name']: self.toogle_task(task_name)
            )

            # etykieta z nazwa zadania
            label = MDLabel(text = task['name'], size_hint_x=0.8)

            # dodanie etykiet do layout zadania
            task_layout.add_widget(checkbox)
            task_layout.add_widget(label)

            # dodanie laout do listy
            task_list.add_widget(task_layout)


    def add_task(self, task_name):
        # dodaje nowe zadanie do listy
        # usuwa biale znaki
        task_name = task_name.strip()

        if task_name:
            new_task = {'name': task_name, 'completed': False}
            self.tasks.append(new_task)
            self.update_task_list()
            self.root.current = 'schedule'


    def login(self, username, password):
        # logowanie do aplikacji
        hashed_password = self.hash_password(password)
        print(f'{hashed_password} takie cos wychodzi z logowania')
        conn = sqlite3.connect("wedding_app.db")
        cursor = conn.cursor()
        user = cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        conn.close()
        if user:
            self.is_logged_in = True
            self.current_user = username  #zapamietuje zalogowanego uzytkownika
            self.update_login_buttons()
            self.root.current = 'profile'
            print("zalogowano pomyslnie")
        else:
            print("Nieprawidłowa nazwa uzytkownika lub haslo")

    
    def sign_up(self, username, password):
        # rejestracja uzytkownika
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
        # wylogowanie
        self.is_logged_in = False
        self.update_login_buttons()
        self.root.current = 'home'


    def update_login_buttons(self):
        # akutalizacja przyciskow 
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
