#importing required libraries
import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import pyodbc


#creating the window
app = ttk.Window()
app.geometry("1500x800")
app.title("The Car Quiz App")
app.resizable(False, False)


#connecting to the databse
conn = pyodbc.connect(r'''
    DRIVER={ODBC Driver 17 for SQL Server};
    SERVER=(localdb)\MSSQLLocalDB;
    DATABASE=quiz_app;
    Trusted_Connection=yes;
''')

cursor = conn.cursor()

#confirmation message displayed to the IDE
print("connected to database")

#this is what the user will see after successfully logging in
def launch_dashboard(username):
    for widget in app.winfo_children():
        widget.destroy()

    #user will choose what type of quiz they want to play
    def quiz_type():
        for widget in app.winfo_children():
            widget.destroy()

        info = tk.Label(app, text = "Choose your quiz type")
        info.place(x = 650, y = 150)

        engine = tk.Button(app, text = "BMW engines")
        engine.place(x = 300, y = 350)
        engine_highscore = tk.Label(app, text = "high score")
        engine_highscore.place(x = 300, y = 450)

        models = tk.Button(app, text = "Car models")
        models.place(x = 400, y = 350)
        models_highscore = tk.Label(app, text = "high score")
        models_highscore.place(x = 400, y = 450)

        car_parts = tk.Button(app, text = "Car parts")
        car_parts.place(x = 500, y = 350)
        car_parts_highscore = tk.Label(app, text = "high score")
        car_parts_highscore.place(x = 500, y = 450)      

        car_logos = tk.Button(app, text = "Car Logos")
        car_logos.place(x = 600, y = 350)
        car_logos_highscore = tk.Label(app, text = "high score")
        car_logos_highscore.place(x = 600, y = 450)

     
        
    welcome_message = tk.Label(app, text = f"welcome {username}")
    welcome_message.place(x = 550, y = 60)

    play = tk.Button(app, text = "play quiz", command = quiz_type)
    play.place(x = 550, y = 200)


#function to register a new user
def register():
    for widget in app.winfo_children():
        widget.destroy()

    #saving the users credentials to the database
    def update_credentials():
        try:
            username = new_username_entry.get()
            password = new_password_entry.get()
            query = "insert into credentials (username, password) values (?,?)"
            cursor.execute(query,(username, password))
            conn.commit()
            confirmation_label = tk.Label(app, text = "You have been registered successfuly, Enjoy the game", width = 70)
            confirmation_label.place(x = 400, y = 400)
            
        except:
            error_label = tk.Label(app, text = "A user with the same username already exists, please try another username", width = 70)
            error_label.place(x = 400, y = 400)

    
    new_username_label = tk.Label(app, text = "please enter a username")
    new_username_label.place(x = 600, y = 200)

    new_username_entry = tk.Entry(app, width = 30)
    new_username_entry.place(x = 600, y = 225)

    new_password_label = tk.Label(app, text = "please enter a password")
    new_password_label.place(x = 600, y = 250)

    new_password_entry = tk.Entry(app, width = 30)
    new_password_entry.place(x = 600, y = 275)

    register_new_user = tk.Button(app, text = "register", width = 30, command = update_credentials)
    register_new_user.place(x = 600, y = 300)

#log in function 
def login(): 
    username = username_entry.get()
    password = password_entry.get()

    query = "select * from credentials where username = ? and password = ?"
    cursor.execute(query,(username, password))
    outcome = cursor.fetchone()
    conn.commit()

    if outcome:
        launch_dashboard(username)

    else:
        error_message = tk.Label(app, text = "incorrect username or password")
        error_message.place(x = 600, y = 400)
                           

#creating the login screen for the app
welcome_label = tk.Label(app, text = "Welcome to the car quiz app!")
welcome_label.place(x = 625, y = 200)

username_label = tk.Label(app,  text = "username")
username_label.place(x = 600, y = 325)

username_entry =tk.Entry(app, width= 30)
username_entry.place(x = 600, y = 350)

password_label = tk.Label(app, text = "password")
password_label.place(x = 600, y = 425)

password_entry = tk.Entry(app, width = 30)
password_entry.place(x = 600, y = 450)

login_button = tk.Button(app, text = "Log in", width = 10, command = login)
login_button.place(x = 650, y = 500)

register_button = tk.Button(app, text = "new to the quiz? Click here to register", width = 40, command = register)
register_button.place(x = 600, y = 550)
