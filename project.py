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

        def bmw_engines():
            pass

        def car_models():
            #updating the score system if the user clicks on the correct answer
            def correct(next_question):
                point = 1
                query = "UPDATE car_models SET score = score + ? WHERE username = ?"
                cursor.execute(query, (point, username))
                if cursor.rowcount == 0:
                    cursor.execute(
                        "INSERT INTO car_models (username, score) VALUES (?, ?)",
                        (username, point)
                    )
                conn.commit()
                next_question()
                
            def incorrect(next_question):
                next_question()

            def question_1():
                for widget in app.winfo_children():
                    widget.destroy() 
                question = tk.Label(app, text = "What car is this?")
                question.place(x = 700, y = 40)
                    
                e92 = Image.open("e92_318i.jpeg")
                e92 = e92.resize((321, 300))
                icon = ImageTk.PhotoImage(e92)

                image = tk.Label(app, image = icon)
                image.image = icon
                image.place(x = 625, y = 100)

                option1 = tk.Button(app, text = "FERRARI 458", command = lambda: incorrect(question_2))
                option1.place(x = 200, y = 550)

                option2 = tk.Button(app, text = "BMW E92", command = lambda: correct(question_2))
                option2.place(x = 400, y = 550)

                option3 = tk.Button(app, text = "AUDI RS3", command = lambda: incorrect(question_2))
                option3.place(x = 600, y = 550)

                option4 = tk.Button(app, text = "MERCEDES C CLASS", command = lambda: incorrect(question_2))
                option4.place(x = 800, y = 550)

                option5 = tk.Button(app, text = "HONDA INTEGRA DC5", command = lambda: incorrect(question_2))
                option5.place(x = 1000, y = 550)

            def question_2():
                for widget in app.winfo_children():
                    widget.destroy()

                question = tk.Label(app, text = "What car is this?")
                question.place(x = 700, y = 40)

                e46 = Image.open("e46.jpg")
                e46 = e46.resize((321, 300))
                icon = ImageTk.PhotoImage(e46)

                image = tk.Label(app, image = icon)
                image.image = icon
                image.place(x = 625, y = 100)

                option1 = tk.Button(app, text = "FERRARI 458", command = lambda: incorrect(question_3))
                option1.place(x = 200, y = 550)

                option2 = tk.Button(app, text = "BMW E46", command = lambda: correct(question_3))
                option2.place(x = 400, y = 550)

                option3 = tk.Button(app, text = "AUDI RS3", command = lambda: incorrect(question_3))
                option3.place(x = 600, y = 550)

                option4 = tk.Button(app, text = "MERCEDES C CLASS", command = lambda: incorrect(question_3))
                option4.place(x = 800, y = 550)

                option5 = tk.Button(app, text = "HONDA INTEGRA DC5", command = lambda: incorrect(question_3))
                option5.place(x = 1000, y = 550)

            def question_3():
                for widget in app.winfo_children():
                    widget.destroy()

                question = tk.Label(app, text = "What car is this?")
                question.place(x = 700, y = 40)

                a5 = Image.open("audi_a5.JPG")
                a5 = a5.resize((321, 300))
                icon = ImageTk.PhotoImage(a5)

                image = tk.Label(app, image = icon)
                image.image = icon
                image.place(x = 625, y = 100)

                option1 = tk.Button(app, text = "FERRARI 458", command = lambda: incorrect(question_4))
                option1.place(x = 200, y = 550)

                option2 = tk.Button(app, text = "AUDI A5", command = lambda: correct(question_4))
                option2.place(x = 400, y = 550)

                option3 = tk.Button(app, text = "BMW M5", command = lambda: incorrect(question_4))
                option3.place(x = 600, y = 550)

                option4 = tk.Button(app, text = "MERCEDES C CLASS", command = lambda: incorrect(question_4))
                option4.place(x = 800, y = 550)

                option5 = tk.Button(app, text = "HONDA INTEGRA DC5", command = lambda: incorrect(question_4))
                option5.place(x = 1000, y = 550)

            def question_4():
                for widget in app.winfo_children():
                    widget.destroy()

                question = tk.Label(app, text = "What car is this?")
                question.place(x = 700, y = 40)

                r34 = Image.open("r34.jpeg")
                r34 = r34.resize((321, 300))
                icon = ImageTk.PhotoImage(r34)

                image = tk.Label(app, image = icon)
                image.image = icon
                image.place(x = 625, y = 100)

                option1 = tk.Button(app, text = "FERRARI 458", command = lambda: incorrect(question_5))
                option1.place(x = 200, y = 550)

                option2 = tk.Button(app, text = "R34 GTR", command = lambda: correct(question_5))
                option2.place(x = 400, y = 550)

                option3 = tk.Button(app, text = "BMW M5", command = lambda: incorrect(question_5))
                option3.place(x = 600, y = 550)

                option4 = tk.Button(app, text = "MERCEDES C CLASS", command = lambda: incorrect(question_5))
                option4.place(x = 800, y = 550)

                option5 = tk.Button(app, text = "HONDA INTEGRA DC5", command = lambda: incorrect(question_5))
                option5.place(x = 1000, y = 550)

            
            def question_5():
                for widget in app.winfo_children():
                    widget.destroy()

                question = tk.Label(app, text = "What car is this?")
                question.place(x = 700, y = 40)

                supra = Image.open("supra.jpeg")
                supra = supra.resize((321, 300))
                icon = ImageTk.PhotoImage(supra)

                image = tk.Label(app, image = icon)
                image.image = icon
                image.place(x = 625, y = 100)

                option1 = tk.Button(app, text = "FERRARI 458", command = lambda: incorrect(question_6))
                option1.place(x = 200, y = 550)

                option2 = tk.Button(app, text = "TOYTA SUPRA MK4", command = lambda: correct(question_6))
                option2.place(x = 400, y = 550)

                option3 = tk.Button(app, text = "BMW M5", command = lambda: incorrect(question_6))
                option3.place(x = 600, y = 550)

                option4 = tk.Button(app, text = "MERCEDES C CLASS", command = lambda: incorrect(question_6))
                option4.place(x = 800, y = 550)

                option5 = tk.Button(app, text = "HONDA INTEGRA DC5", command = lambda: incorrect(question_6))
                option5.place(x = 1000, y = 550)

            def question_6():
                for widget in app.winfo_children():
                    widget.destroy()

                question = tk.Label(app, text = "What car is this?")
                question.place(x = 700, y = 40)

                range_rover = Image.open("range.JPG")
                range_rover = range_rover.resize((321, 300))
                icon = ImageTk.PhotoImage(range_rover)

                image = tk.Label(app, image = icon)
                image.image = icon
                image.place(x = 625, y = 100)

                option1 = tk.Button(app, text = "FERRARI 458", command = lambda: incorrect(final_screen))
                option1.place(x = 200, y = 550)

                option2 = tk.Button(app, text = "RANGE ROVER", command = lambda: correct(final_screen))
                option2.place(x = 400, y = 550)

                option3 = tk.Button(app, text = "BMW M5", command = lambda: incorrect(final_screen))
                option3.place(x = 600, y = 550)

                option4 = tk.Button(app, text = "MERCEDES C CLASS", command = lambda: incorrect(final_screen))
                option4.place(x = 800, y = 550)

                option5 = tk.Button(app, text = "HONDA INTEGRA DC5", command = lambda: incorrect(final_screen))
                option5.place(x = 1000, y = 550)

            def final_screen():
                for widget in app.winfo_children():
                    widget.destroy()

                #fetching the final score from the database and displaying it to the user    
                query = "select * from car_models where username = ?"
                cursor.execute(query,(username,))
                row = cursor.fetchone()
                if row:
                    score = row[1] 
                else:
                    score = 0
                message = tk.Label(app, text = f"THE QUIZ HAS ENDED! YOUR SCORE: {score} ")
                message.place(x = 650, y = 300)

                try_again = tk.Button(app, text = "Try again", command = car_models)
                try_again.place(x = 500, y = 500)

                dashboard = tk.Button(app, text = "Back to dashboard", command = lambda: launch_dashboard(username))
                dashboard.place(x = 700, y = 500)
                
            question_1()
            
        def car_parts():
            pass

        def car_logos():
            pass

        #user chooses quiz type
        info = tk.Label(app, text = "Choose your quiz type")
        info.place(x = 650, y = 150)

        engine = tk.Button(app, text = "BMW engines", command = bmw_engines)
        engine.place(x = 300, y = 350)
        engine_highscore = tk.Label(app, text = "high score")
        engine_highscore.place(x = 300, y = 450)

        models = tk.Button(app, text = "Car models", command = car_models)
        models.place(x = 400, y = 350)
        models_highscore = tk.Label(app, text = "high score")
        models_highscore.place(x = 400, y = 450)

        car_parts = tk.Button(app, text = "Car parts", command = car_parts)
        car_parts.place(x = 500, y = 350)
        car_parts_highscore = tk.Label(app, text = "high score")
        car_parts_highscore.place(x = 500, y = 450)      

        car_logos = tk.Button(app, text = "Car Logos", command = car_logos)
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
