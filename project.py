#importing required libraries
import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import pyodbc
import google.generativeai as genai

#defining the API key and and ai model
genai.configure(api_key="AIzaSyAO3xpll0Z4uGtc3NLRhoMLJZIeX60WtII")
model = genai.GenerativeModel("gemini-2.0-flash")

def set_background(app, image_path):
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((1500, 800))
    app.bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(app, image=app.bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)



#creating the window
app = ttk.Window()
app.geometry("1500x800")
app.title("The Car Quiz App")
app.resizable(False, False)

#loading the GIF
gif = Image.open("992.gif")
frames = gif.n_frames

RESIZE_W = 475   
RESIZE_H = 800  

frame_list = []
for i in range(frames):
    gif.seek(i)
    frame = gif.copy().resize((RESIZE_W, RESIZE_H), Image.Resampling.LANCZOS)
    frame_list.append(ImageTk.PhotoImage(frame))


animation_id = True
current_frame = 0

def animate():
    global current_frame, animation_id, gif_label, frame_list
    
    if not animation_id:
        return
    
    gif_label.config(image=frame_list[current_frame])
    current_frame = (current_frame + 1) % frames
    app.after(10, animate)


gif_label = tk.Label(app, bg='#f5f5f5')
gif_label.place(x = 0, y= 0)

animate()

def stop_animation():
    global animation_id
    animation_id = False

def login_from_button(user_entry, pass_entry):
    global username_entry, password_entry
    username_entry = user_entry
    password_entry = pass_entry
    login()

    #creating placeholders for the entries 
def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(foreground="gray")

    #when user clicks on the entry entry it will get rid of the palce holder
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(foreground="black")

    #if the user does not type anything it will insert the placeholder back into the entry box
    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(foreground="gray")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


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

                def get_hint():
                    def get_car_hint(image_path):
                        with open(image_path, "rb") as img:
                            image_bytes = img.read()

                        response = model.generate_content(
                            [
                                "Give me a short hint about what car this is. Never reveal the exact car.",
                                {"mime_type": "image/jpeg", "data": image_bytes}
                            ]
                        )

                        return response.text
                    hint = get_car_hint("e92_318i.jpeg")
                    
                    hint_label = tk.Label(app, text = f"HINT: {hint}")
                    hint_label.place(x = 400, y = 650)
                    
                
                hint = tk.Button(app, text = "HINT", command = get_hint)
                hint.place(x = 1200, y = 100)

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

                option1 = tk.Button(app, text = "CHEVERLOT ORLANDO", command = lambda: incorrect(question_3))
                option1.place(x = 200, y = 550)

                option2 = tk.Button(app, text = "BMW E46", command = lambda: correct(question_3))
                option2.place(x = 400, y = 550)

                option3 = tk.Button(app, text = "MASERATI GHIBLI", command = lambda: incorrect(question_3))
                option3.place(x = 600, y = 550)

                option4 = tk.Button(app, text = "HONDA ACCORD", command = lambda: incorrect(question_3))
                option4.place(x = 800, y = 550)

                option5 = tk.Button(app, text = "BMW X5", command = lambda: incorrect(question_3))
                option5.place(x = 1000, y = 550)

                def get_hint():
                    def get_car_hint(image_path):
                        with open(image_path, "rb") as img:
                            image_bytes = img.read()

                        response = model.generate_content(
                            [
                                "Give me a short hint about what car this is. Never reveal the exact car.",
                                {"mime_type": "image/jpeg", "data": image_bytes}
                            ]
                        )

                        return response.text
                    hint = get_car_hint("e46.jpg")
                    
                    hint_label = tk.Label(app, text = f"HINT: {hint}")
                    hint_label.place(x = 400, y = 650)
                    
                
                hint = tk.Button(app, text = "HINT", command = get_hint)
                hint.place(x = 1200, y = 100)

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

                option1 = tk.Button(app, text = "BMW E90", command = lambda: incorrect(question_4))
                option1.place(x = 200, y = 550)

                option2 = tk.Button(app, text = "AUDI A5", command = lambda: correct(question_4))
                option2.place(x = 400, y = 550)

                option3 = tk.Button(app, text = "LEXUS LFA", command = lambda: incorrect(question_4))
                option3.place(x = 600, y = 550)

                option4 = tk.Button(app, text = "TOYTA COROLLA", command = lambda: incorrect(question_4))
                option4.place(x = 800, y = 550)

                option5 = tk.Button(app, text = "DODGE CHALLENGER", command = lambda: incorrect(question_4))
                option5.place(x = 1000, y = 550)

                def get_hint():
                    def get_car_hint(image_path):
                        with open(image_path, "rb") as img:
                            image_bytes = img.read()

                        response = model.generate_content(
                            [
                                "Give me a short hint about what car this is. Never reveal the exact car.",
                                {"mime_type": "image/jpeg", "data": image_bytes}
                            ]
                        )

                        return response.text
                    hint = get_car_hint("audi_a5.JPG")
                    
                    hint_label = tk.Label(app, text = f"HINT: {hint}")
                    hint_label.place(x = 400, y = 650)
                    
                
                hint = tk.Button(app, text = "HINT", command = get_hint)
                hint.place(x = 1200, y = 100)

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

                option1 = tk.Button(app, text = "MITSUBISHI EVO", command = lambda: incorrect(question_5))
                option1.place(x = 200, y = 550)

                option2 = tk.Button(app, text = "NISSAN R34 GTR", command = lambda: correct(question_5))
                option2.place(x = 400, y = 550)

                option3 = tk.Button(app, text = "TOYOTA SUPRA", command = lambda: incorrect(question_5))
                option3.place(x = 600, y = 550)

                option4 = tk.Button(app, text = "MAZDA RX 7", command = lambda: incorrect(question_5))
                option4.place(x = 800, y = 550)

                option5 = tk.Button(app, text = "NISSAN R33 SKYLINE", command = lambda: incorrect(question_5))
                option5.place(x = 1000, y = 550)

                def get_hint():
                    def get_car_hint(image_path):
                        with open(image_path, "rb") as img:
                            image_bytes = img.read()

                        response = model.generate_content(
                            [
                                "Give me a short hint about what car this is. Never reveal the exact car.",
                                {"mime_type": "image/jpeg", "data": image_bytes}
                            ]
                        )

                        return response.text
                    hint = get_car_hint("r34.jpeg")
                    
                    hint_label = tk.Label(app, text = f"HINT: {hint}")
                    hint_label.place(x = 400, y = 650)
                    
                
                hint = tk.Button(app, text = "HINT", command = get_hint)
                hint.place(x = 1200, y = 100)

            
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

                option1 = tk.Button(app, text = "FERRARI SF90", command = lambda: incorrect(question_6))
                option1.place(x = 200, y = 550)

                option2 = tk.Button(app, text = "TOYTA SUPRA MK4", command = lambda: correct(question_6))
                option2.place(x = 400, y = 550)

                option3 = tk.Button(app, text = "HONDA CIVIC", command = lambda: incorrect(question_6))
                option3.place(x = 600, y = 550)

                option4 = tk.Button(app, text = "BMW M3", command = lambda: incorrect(question_6))
                option4.place(x = 800, y = 550)

                option5 = tk.Button(app, text = "MERCEDES C63", command = lambda: incorrect(question_6))
                option5.place(x = 1000, y = 550)

                def get_hint():
                    def get_car_hint(image_path):
                        with open(image_path, "rb") as img:
                            image_bytes = img.read()

                        response = model.generate_content(
                            [
                                "Give me a short hint about what car this is. Never reveal the exact car.",
                                {"mime_type": "image/jpeg", "data": image_bytes}
                            ]
                        )

                        return response.text
                    hint = get_car_hint("supra.jpeg")
                    
                    hint_label = tk.Label(app, text = f"HINT: {hint}")
                    hint_label.place(x = 400, y = 650)
                    
                
                hint = tk.Button(app, text = "HINT", command = get_hint)
                hint.place(x = 1200, y = 100)

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

                option1 = tk.Button(app, text = "LAND ROVER", command = lambda: incorrect(question_7))
                option1.place(x = 200, y = 550)

                option2 = tk.Button(app, text = "RANGE ROVER", command = lambda: correct(question_7))
                option2.place(x = 400, y = 550)

                option3 = tk.Button(app, text = "BMW X7", command = lambda: incorrect(question_7))
                option3.place(x = 600, y = 550)

                option4 = tk.Button(app, text = "MERCEDES GLE", command = lambda: incorrect(question_7))
                option4.place(x = 800, y = 550)

                option5 = tk.Button(app, text = "AUDI Q7", command = lambda: incorrect(question_7))
                option5.place(x = 1000, y = 550)

                def get_hint():
                    def get_car_hint(image_path):
                        with open(image_path, "rb") as img:
                            image_bytes = img.read()

                        response = model.generate_content(
                            [
                                "Give me a short hint about what car this is. Never reveal the exact car.",
                                {"mime_type": "image/jpeg", "data": image_bytes}
                            ]
                        )

                        return response.text
                    hint = get_car_hint("range.JPG")
                    
                    hint_label = tk.Label(app, text = f"HINT: {hint}")
                    hint_label.place(x = 400, y = 650)
                    
                
                hint = tk.Button(app, text = "HINT", command = get_hint)
                hint.place(x = 1200, y = 100)


            def question_7():
                for widget in app.winfo_children():
                    widget.destroy()

                question = tk.Label(app, text = "What car is this?")
                question.place(x = 700, y = 40)

                range_rover = Image.open("G20.JPG")
                range_rover = range_rover.resize((321, 300))
                icon = ImageTk.PhotoImage(range_rover)

                image = tk.Label(app, image = icon)
                image.image = icon
                image.place(x = 625, y = 100)

                option1 = tk.Button(app, text = "FERRARI F430", command = lambda: incorrect(final_screen))
                option1.place(x = 200, y = 550)

                option2 = tk.Button(app, text = "BMW G20", command = lambda: correct(final_screen))
                option2.place(x = 400, y = 550)

                option3 = tk.Button(app, text = "BMW M760 Li", command = lambda: incorrect(final_screen))
                option3.place(x = 600, y = 550)

                option4 = tk.Button(app, text = "HYUNDAI i30N", command = lambda: incorrect(final_screen))
                option4.place(x = 800, y = 550)

                option5 = tk.Button(app, text = "FERRARI SF-90", command = lambda: incorrect(final_screen))
                option5.place(x = 1000, y = 550)

                def get_hint():
                    def get_car_hint(image_path):
                        with open(image_path, "rb") as img:
                            image_bytes = img.read()

                        response = model.generate_content(
                            [
                                "Give me a short hint about what car this is. Never reveal the exact car.",
                                {"mime_type": "image/jpeg", "data": image_bytes}
                            ]
                        )

                        return response.text
                    hint = get_car_hint("G20.JPG")
                    
                    hint_label = tk.Label(app, text = f"HINT: {hint}")
                    hint_label.place(x = 400, y = 650)
                    
                
                hint = tk.Button(app, text = "HINT", command = get_hint)
                hint.place(x = 1200, y = 100)

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

#where user will be diverted after registering 
def show_login_screen():
    global animation_id, gif_label
    stop_animation()

    for widget in app.winfo_children():
        widget.destroy()

    animation_id = True

    gif_label = tk.Label(app, bg='#f5f5f5')
    gif_label.place(x=0, y=0)
    animate()

    welcome_label = tk.Label(app, text="Welcome to the car quiz app!", font=("Segoe UI", 29, "bold"))
    welcome_label.place(x=650, y=150)

    username_entry = ttk.Entry(app, width=35, bootstyle="dark")
    username_entry.place(x=800, y=350)
    add_placeholder(username_entry, "Username")

    password_entry = ttk.Entry(app, width=35, bootstyle="dark")
    password_entry.place(x=800, y=400)
    add_placeholder(password_entry, "Password")

    login_button = ttk.Button(app, text="Log in", width=34, bootstyle="dark", command=lambda: login_from_button(username_entry, password_entry))
    login_button.place(x=800, y=475)

    register_button = ttk.Button(app, text="New to the quiz? Click here to register", width=34, bootstyle="info", command=register)
    register_button.place(x=800, y=550)

#function to register a new user
def register():
    global animation_id, gif_label
    stop_animation()
    for widget in app.winfo_children():
        widget.destroy()

    animation_id = True

    gif_label = tk.Label(app, bg='#f5f5f5')
    gif_label.place(x = 0, y= 0)

    animate()

    #saving the users credentials to the database
    def update_credentials():
        try:
            username = new_username_entry.get()
            password = new_password_entry.get()
            query = "insert into credentials (username, password) values (?,?)"
            cursor.execute(query,(username, password))
            conn.commit()
            confirmation_label = tk.Label(app, text = "You have been registered successfuly, Return back to log in", font = ("Segoe UI", 15, "bold"))
            confirmation_label.place(x = 650, y = 650)
            
        except:
            error_label = tk.Label(app, text = "username already exists, please try another username", font = ("Segoe UI", 15, "bold"))
            error_label.place(x = 650, y = 650)

    register_label = tk.Label(app, text = "Register a new account", font = ("Segoe UI", 29, "bold"))
    register_label.place(x = 700, y = 150)

    new_username_entry = ttk.Entry(app, width = 35, bootstyle = "dark")
    new_username_entry.place(x = 800, y = 350)
    add_placeholder(new_username_entry, "Username")


    new_password_entry = ttk.Entry(app, width = 35, bootstyle = "dark")
    new_password_entry.place(x = 800, y = 400)
    add_placeholder(new_password_entry, "Password")

    register_new_user = ttk.Button(app, text = "register", width = 35, bootstyle = "dark", command = update_credentials)
    register_new_user.place(x = 800, y = 475)

    back_to_login = ttk.Button(app, text="Back to Login", width=35, bootstyle="info", command=show_login_screen)
    back_to_login.place(x = 800, y = 550)

#log in function 
def login(): 
    username = username_entry.get()
    password = password_entry.get()

    query = "select * from credentials where username = ? and password = ?"
    cursor.execute(query,(username, password))
    outcome = cursor.fetchone()
    conn.commit()

    if outcome:
        stop_animation()
        launch_dashboard(username)

    else:
        error_message = tk.Label(app, text = "incorrect username or password")
        error_message.place(x = 600, y = 400)
                           

#creating the login screen for the app
welcome_label = tk.Label(app, text = "Welcome to the car quiz app!", font = ("Segoe UI", 29, "bold"))
welcome_label.place(x = 650, y = 150)


username_entry =ttk.Entry(app, width= 35, bootstyle = "dark")
username_entry.place(x = 800, y = 350)
add_placeholder(username_entry, "Username")

password_entry = ttk.Entry(app, width= 35, bootstyle = "dark")
password_entry.place(x = 800, y = 400)
add_placeholder(password_entry, "Password")

login_button = ttk.Button(app, text = "Log in", width = 34, bootstyle= "dark", command = login)
login_button.place(x = 800, y = 475)

register_button = ttk.Button(app, text = "New to the quiz? Click here to register", width = 34, bootstyle = "info", command = register)
register_button.place(x = 800, y = 550)

app.mainloop()
