#importing required libraries
import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import pyodbc
import google.generativeai as genai

#defining the API key and and ai model
genai.configure(api_key="AIzaSyA4CQOpalzBSTv6a9fWfsXgtR6Lh2cTFDs")
model = genai.GenerativeModel("gemini-2.0-flash")


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

    def bmw_engines():
        def correct(next_question):
            point = 1
            query = "UPDATE bmw_engines SET score = score + ? WHERE username = ?"
            cursor.execute(query, (point, username))
            if cursor.rowcount == 0:
                cursor.execute(
                    "INSERT INTO bmw_engines (username, score) VALUES (?, ?)",
                    (username, point)
                )
            conn.commit()
            next_question()
            
        def incorrect(next_question):
            next_question()

        def question_1():
            for widget in app.winfo_children():
                widget.destroy() 
            question = tk.Label(app, text = "What engine does this car have?", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            s65 = Image.open("e92_m3.jpg")
            s65 = s65.resize((421, 400))
            icon = ImageTk.PhotoImage(s65)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "S85",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "S65",bootstyle = "dark", width = 20, command = lambda: correct(question_2))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "B58",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "N55",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "S58",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option5.place(x = 1150, y = 550)

            def get_hint():
                def get_car_hint(image_path):
                    with open(image_path, "rb") as img:
                        image_bytes = img.read()

                    response = model.generate_content(
                        [
                            "Give me a short hint about what engine this car has. Never reveal the exact engine.",
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )

                    return response.text
                hint = get_car_hint("e92_m3.jpg")
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

            
        def question_2():
            for widget in app.winfo_children():
                widget.destroy() 
            question = tk.Label(app, text = "What engine does this car have?", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            s55 = Image.open("f82.jpg")
            s55 = s55.resize((421, 400))
            icon = ImageTk.PhotoImage(s55)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "S85",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "S55",bootstyle = "dark", width = 20, command = lambda: correct(question_3))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "B58",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "N55",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "S58",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option5.place(x = 1150, y = 550)

            def get_hint():
                def get_car_hint(image_path):
                    with open(image_path, "rb") as img:
                        image_bytes = img.read()

                    response = model.generate_content(
                        [
                            "Give me a short hint about what engine this car has. Never reveal the exact engine.",
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )

                    return response.text
                hint = get_car_hint("f82.jpg")
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)


        def question_3():
            for widget in app.winfo_children():
                widget.destroy() 
            question = tk.Label(app, text = "What engine does this car have?", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            g80 = Image.open("g80.jpg")
            g80 = g80.resize((421, 400))
            icon = ImageTk.PhotoImage(g80)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "S85",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "S58",bootstyle = "dark", width = 20, command = lambda: correct(question_4))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "B58",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "N55",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "S58",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option5.place(x = 1150, y = 550)

            def get_hint():
                def get_car_hint(image_path):
                    with open(image_path, "rb") as img:
                        image_bytes = img.read()

                    response = model.generate_content(
                        [
                            "Give me a short hint about what engine this car has. Never reveal the exact engine.",
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )

                    return response.text
                hint = get_car_hint("g80.jpg")
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def question_4():
            for widget in app.winfo_children():
                widget.destroy() 
            question = tk.Label(app, text = "What engine does this car have?", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            e60 = Image.open("e60.jpg")
            e60 = e60.resize((421, 400))
            icon = ImageTk.PhotoImage(e60)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "S85",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "S65",bootstyle = "dark", width = 20, command = lambda: correct(question_5))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "B58",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "N55",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "S58",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option5.place(x = 1150, y = 550)

            def get_hint():
                def get_car_hint(image_path):
                    with open(image_path, "rb") as img:
                        image_bytes = img.read()

                    response = model.generate_content(
                        [
                            "Give me a short hint about what engine this car has. Never reveal the exact engine.",
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )

                    return response.text
                hint = get_car_hint("e60.jpg")
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def question_5():
            for widget in app.winfo_children():
                widget.destroy() 
            question = tk.Label(app, text = "What engine does this car have?", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            m2 = Image.open("m2.jpg")
            m2 = m2.resize((421, 400))
            icon = ImageTk.PhotoImage(m2)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "S85",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "N55",bootstyle = "dark", width = 20, command = lambda: correct(final_screen))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "B58",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "N55",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "S58",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option5.place(x = 1150, y = 550)

            def get_hint():
                def get_car_hint(image_path):
                    with open(image_path, "rb") as img:
                        image_bytes = img.read()

                    response = model.generate_content(
                        [
                            "Give me a short hint about what engine this car has. Never reveal the exact engine.",
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )

                    return response.text
                hint = get_car_hint("m2.jpg")
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def final_screen():
            for widget in app.winfo_children():
                widget.destroy()

            #fetching the final score from the database and displaying it to the user    
            query = "select * from bmw_engines where username = ?"
            cursor.execute(query,(username,))
            row = cursor.fetchone()
            if row:
                score = row[1] 
            else:
                score = 0

            card = ttk.Frame(app, padding=40, borderwidth=2, relief="ridge")
            card.place(relx=0.5, rely=0.4, anchor="center")

            message = tk.Label(app, text = f"THE QUIZ HAS ENDED! YOUR SCORE: {score} ", font=("Segoe UI", 18, "bold"), justify="center")
            message.place(x = 750, y = 150)

            img = Image.open("trophy.png")
            img = img.resize((120, 120))
            icon = ImageTk.PhotoImage(img)

            icon_label = tk.Label(app, image=icon)
            icon_label.image = icon
            icon_label.place(x = 1350, y = 250)


            try_again = ttk.Button(app, text="Try Again", bootstyle="info-pill", padding=10, width=15, command = bmw_engines)
            try_again.place(x = 800, y = 500)

            back_btn = ttk.Button(app, text="Back to Dashboard", bootstyle="success-pill", padding=10, width=20, command = lambda: launch_dashboard(username))
            back_btn.place(x = 1150, y = 500)

            logout = ttk.Button(app, text="Log out", bootstyle="danger", padding=10, width=20, command = show_login_screen)
            logout.place(x = 975, y = 650)

            global animation_id, gif_label
            animation_id = True

            gif_label = tk.Label(app, bg='#f5f5f5')
            gif_label.place(x = 0, y= 0)

            animate()

            
        question_1()
        

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
            question = tk.Label(app, text = "What car is this", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            e92 = Image.open("e92_318i.jpeg")
            e92 = e92.resize((421, 400))
            icon = ImageTk.PhotoImage(e92)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "FERRARI 458",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "BMW E92",bootstyle = "dark", width = 20, command = lambda: correct(question_2))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "AUDI RS3",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "MERCEDES C CLASS",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "HONDA INTEGRA DC5",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option5.place(x = 1150, y = 550)

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
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def question_2():
            for widget in app.winfo_children():
                widget.destroy()

            question = tk.Label(app, text = "What car is this", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))

            e46 = Image.open("e46.jpg")
            e46 = e46.resize((421, 400))
            icon = ImageTk.PhotoImage(e46)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)
            
            option1 = ttk.Button(app, text = "CHEVERLOT ORLANDO",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "BMW E46",bootstyle = "dark", width = 20, command = lambda: correct(question_3))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "MASERATI GHIBLI",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "HONDA ACCORD",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "BMW X5",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option5.place(x = 1150, y = 550)

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
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def question_3():
            for widget in app.winfo_children():
                widget.destroy()

            question = tk.Label(app, text = "What car is this", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))

            a5 = Image.open("audi_a5.JPG")
            a5 = a5.resize((421, 400))
            icon = ImageTk.PhotoImage(a5)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "BMW E90",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "AUDI A5",bootstyle = "dark", width = 20, command = lambda: correct(question_4))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "LEXUS LFA",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "TOYTA COROLLA",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "DODGE CHALLENGER",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option5.place(x = 1150, y = 550)

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
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def question_4():
            for widget in app.winfo_children():
                widget.destroy()

            question = tk.Label(app, text = "What car is this", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))

            r34 = Image.open("r34.jpeg")
            r34 = r34.resize((421, 400))
            icon = ImageTk.PhotoImage(r34)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "MITSUBISHI EVO",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "NISSAN R34 GTR",bootstyle = "dark", width = 20, command = lambda: correct(question_5))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "TOYOTA SUPRA",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "MAZDA RX 7",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "NISSAN R33 SKYLINE",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option5.place(x = 1150, y = 550)

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
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        
        def question_5():
            for widget in app.winfo_children():
                widget.destroy()

            question = tk.Label(app, text = "What car is this", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))

            supra = Image.open("supra.jpeg")
            supra = supra.resize((421, 400))
            icon = ImageTk.PhotoImage(supra)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "FERRARI SF90",bootstyle = "dark", width = 20, command = lambda: incorrect(question_6))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "TOYTA SUPRA MK4",bootstyle = "dark", width = 20, command = lambda: correct(question_6))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "HONDA CIVIC",bootstyle = "dark", width = 20, command = lambda: incorrect(question_6))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "BMW M3",bootstyle = "dark", width = 20, command = lambda: incorrect(question_6))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "MERCEDES C63",bootstyle = "dark", width = 20, command = lambda: incorrect(question_6))
            option5.place(x = 1150, y = 550)


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
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def question_6():
            for widget in app.winfo_children():
                widget.destroy()

            question = tk.Label(app, text = "What car is this", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))

            range_rover = Image.open("range.JPG")
            range_rover = range_rover.resize((421, 400))
            icon = ImageTk.PhotoImage(range_rover)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "LAND ROVER",bootstyle = "dark", width = 20, command = lambda: incorrect(question_7))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "RANGE ROVER",bootstyle = "dark", width = 20, command = lambda: correct(question_7))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "BMW X7",bootstyle = "dark", width = 20, command = lambda: incorrect(question_7))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "MERCEDES GLE",bootstyle = "dark", width = 20, command = lambda: incorrect(question_7))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "AUDI Q7",bootstyle = "dark", width = 20, command = lambda: incorrect(question_7))
            option5.place(x = 1150, y = 550)

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
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)


        def question_7():
            for widget in app.winfo_children():
                widget.destroy()

            question = tk.Label(app, text = "What car is this", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))

            range_rover = Image.open("G20.JPG")
            range_rover = range_rover.resize((421, 400))
            icon = ImageTk.PhotoImage(range_rover)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "FERRARI F430",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "BMW G20",bootstyle = "dark", width = 20, command = lambda: correct(final_screen))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "BMW M760 Li",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "HYUNDAI i30N",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "FERRARI SF-90",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option5.place(x = 1150, y = 550)

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
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

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

            card = ttk.Frame(app, padding=40, borderwidth=2, relief="ridge")
            card.place(relx=0.5, rely=0.4, anchor="center")

            message = tk.Label(app, text = f"THE QUIZ HAS ENDED! YOUR SCORE: {score} ", font=("Segoe UI", 18, "bold"), justify="center")
            message.place(x = 750, y = 150)

            img = Image.open("trophy.png")
            img = img.resize((120, 120))
            icon = ImageTk.PhotoImage(img)

            icon_label = tk.Label(app, image=icon)
            icon_label.image = icon
            icon_label.place(x = 1350, y = 250)


            try_again = ttk.Button(app, text="Try Again", bootstyle="info-pill", padding=10, width=15, command = car_models)
            try_again.place(x = 800, y = 500)

            back_btn = ttk.Button(app, text="Back to Dashboard", bootstyle="success-pill", padding=10, width=20, command = lambda: launch_dashboard(username))
            back_btn.place(x = 1150, y = 500)

            logout = ttk.Button(app, text="Log out", bootstyle="danger", padding=10, width=20, command = show_login_screen)
            logout.place(x = 975, y = 650)

            global animation_id, gif_label
            animation_id = True

            gif_label = tk.Label(app, bg='#f5f5f5')
            gif_label.place(x = 0, y= 0)

            animate()
            
        question_1()
        
    def car_parts1():
        #updating the score system if the user clicks on the correct answer
        def correct(next_question):
            point = 1
            query = "UPDATE car_parts SET score = score + ? WHERE username = ?"
            cursor.execute(query, (point, username))
            if cursor.rowcount == 0:
                cursor.execute(
                    "INSERT INTO car_parts (username, score) VALUES (?, ?)",
                    (username, point)
                )
            conn.commit()
            next_question()
        
            
        def incorrect(next_question):
            next_question()

        def question_1():
            for widget in app.winfo_children():
                widget.destroy() 
            question = tk.Label(app, text = "What car part is this?", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            piston = Image.open("piston.jpg")
            piston = piston.resize((421, 400))
            icon = ImageTk.PhotoImage(piston)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "gearbox",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "piston",bootstyle = "dark", width = 20, command = lambda: correct(question_2))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "wiper",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "fuel pump",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "injector",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option5.place(x = 1150, y = 550)

            def get_hint():
                def get_car_hint(image_path):
                    with open(image_path, "rb") as img:
                        image_bytes = img.read()

                    response = model.generate_content(
                        [
                            "Give me a short hint about what car part this is. Never reveal the exact car part.",
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )

                    return response.text
                hint = get_car_hint("piston.jpg")
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)
            
        def question_2():
            for widget in app.winfo_children():
                widget.destroy() 
            question = tk.Label(app, text = "What car part is this?", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            clutch = Image.open("clutch.jpg")
            clutch = clutch.resize((421, 400))
            icon = ImageTk.PhotoImage(clutch)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "gearbox",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "clutch",bootstyle = "dark", width = 20, command = lambda: correct(question_3))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "wiper",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "fuel pump",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "injector",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option5.place(x = 1150, y = 550)
            def get_hint():
                def get_car_hint(image_path):
                    with open(image_path, "rb") as img:
                        image_bytes = img.read()

                    response = model.generate_content(
                        [
                            "Give me a short hint about what car part this is. Never reveal the exact car part.",
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )

                    return response.text
                hint = get_car_hint("clutch.jpg")
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def question_3():
            for widget in app.winfo_children():
                widget.destroy() 
            question = tk.Label(app, text = "What car part is this?", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            transmission = Image.open("transmission.jpg")
            transmission = transmission.resize((421, 400))
            icon = ImageTk.PhotoImage(transmission)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "gearbox",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "transmission",bootstyle = "dark", width = 20, command = lambda: correct(question_4))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "wiper",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "fuel pump",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "injector",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option5.place(x = 1150, y = 550)
            def get_hint():
                def get_car_hint(image_path):
                    with open(image_path, "rb") as img:
                        image_bytes = img.read()

                    response = model.generate_content(
                        [
                            "Give me a short hint about what car part this is. Never reveal the exact car part.",
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )

                    return response.text
                hint = get_car_hint("transmission.jpg")
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def question_4():
            for widget in app.winfo_children():
                widget.destroy() 
            question = tk.Label(app, text = "What car part is this?", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            radiator = Image.open("radiator.jpg")
            radiator = radiator.resize((421, 400))
            icon = ImageTk.PhotoImage(radiator)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "gearbox",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "radiator",bootstyle = "dark", width = 20, command = lambda: correct(question_5))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "wiper",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "fuel pump",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "injector",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option5.place(x = 1150, y = 550)
            def get_hint():
                def get_car_hint(image_path):
                    with open(image_path, "rb") as img:
                        image_bytes = img.read()

                    response = model.generate_content(
                        [
                            "Give me a short hint about what car part this is. Never reveal the exact car part.",
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )

                    return response.text
                hint = get_car_hint("radiator.jpg")
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def question_5():
            for widget in app.winfo_children():
                widget.destroy() 
            question = tk.Label(app, text = "What car part is this?", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            brake = Image.open("brake.jpg")
            brake = brake.resize((421, 400))
            icon = ImageTk.PhotoImage(brake)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "gearbox",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "brake",bootstyle = "dark", width = 20, command = lambda: correct(final_screen))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "wiper",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "fuel pump",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "injector",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option5.place(x = 1150, y = 550)
            def get_hint():
                def get_car_hint(image_path):
                    with open(image_path, "rb") as img:
                        image_bytes = img.read()

                    response = model.generate_content(
                        [
                            "Give me a short hint about what car part this is. Never reveal the exact car part.",
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )

                    return response.text
                hint = get_car_hint("brake.jpg")
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def final_screen():
            for widget in app.winfo_children():
                widget.destroy()

            #fetching the final score from the database and displaying it to the user    
            query = "select * from car_parts where username = ?"
            cursor.execute(query,(username,))
            row = cursor.fetchone()
            if row:
                score = row[1] 
            else:
                score = 0

            card = ttk.Frame(app, padding=40, borderwidth=2, relief="ridge")
            card.place(relx=0.5, rely=0.4, anchor="center")

            message = tk.Label(app, text = f"THE QUIZ HAS ENDED! YOUR SCORE: {score} ", font=("Segoe UI", 18, "bold"), justify="center")
            message.place(x = 750, y = 150)

            img = Image.open("trophy.png")
            img = img.resize((120, 120))
            icon = ImageTk.PhotoImage(img)

            icon_label = tk.Label(app, image=icon)
            icon_label.image = icon
            icon_label.place(x = 1350, y = 250)


            try_again = ttk.Button(app, text="Try Again", bootstyle="info-pill", padding=10, width=15, command = car_parts1)
            try_again.place(x = 800, y = 500)

            back_btn = ttk.Button(app, text="Back to Dashboard", bootstyle="success-pill", padding=10, width=20, command = lambda: launch_dashboard(username))
            back_btn.place(x = 1150, y = 500)

            logout = ttk.Button(app, text="Log out", bootstyle="danger", padding=10, width=20, command = show_login_screen)
            logout.place(x = 975, y = 650)

            global animation_id, gif_label
            animation_id = True

            gif_label = tk.Label(app, bg='#f5f5f5')
            gif_label.place(x = 0, y= 0)

            animate()

        question_1()


    def car_logos1():
        #updating the score system if the user clicks on the correct answer
        def correct(next_question):
            point = 1
            query = "UPDATE car_logos SET score = score + ? WHERE username = ?"
            cursor.execute(query, (point, username))
            if cursor.rowcount == 0:
                cursor.execute(
                    "INSERT INTO car_logos (username, score) VALUES (?, ?)",
                    (username, point)
                )
            conn.commit()
            next_question()
        
            
        def incorrect(next_question):
            next_question()

        def question_1():
            for widget in app.winfo_children():
                widget.destroy() 
            question = tk.Label(app, text = "What brad has this car logo?", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            ferrari = Image.open("ferrari.jpg")
            ferrari = ferrari.resize((421, 400))
            icon = ImageTk.PhotoImage(ferrari)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "laborghini",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "ferrari",bootstyle = "dark", width = 20, command = lambda: correct(question_2))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "porsche",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "aston martin",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "bmw",bootstyle = "dark", width = 20, command = lambda: incorrect(question_2))
            option5.place(x = 1150, y = 550)

            def get_hint():
                def get_car_hint(image_path):
                    with open(image_path, "rb") as img:
                        image_bytes = img.read()

                    response = model.generate_content(
                        [
                            "Give me a short hint about what car logo this is. Never reveal the exact car logo.",
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )

                    return response.text
                hint = get_car_hint("ferrari.jpg")
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def question_2():
            for widget in app.winfo_children():
                widget.destroy() 
            question = tk.Label(app, text = "What brad has this car logo?", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            mercedes = Image.open("mercedes.jpg")
            mercedes = mercedes.resize((421, 400))
            icon = ImageTk.PhotoImage(mercedes)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "laborghini",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "mercedes",bootstyle = "dark", width = 20, command = lambda: correct(question_3))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "porsche",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "aston martin",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "bmw",bootstyle = "dark", width = 20, command = lambda: incorrect(question_3))
            option5.place(x = 1150, y = 550)

            def get_hint():
                def get_car_hint(image_path):
                    with open(image_path, "rb") as img:
                        image_bytes = img.read()

                    response = model.generate_content(
                        [
                            "Give me a short hint about what car logo this is. Never reveal the exact car logo.",
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )

                    return response.text
                hint = get_car_hint("mercedes.jpg")
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def question_3():
            for widget in app.winfo_children():
                widget.destroy() 
            question = tk.Label(app, text = "What brad has this car logo?", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            audi = Image.open("audi.jpg")
            audi = audi.resize((421, 400))
            icon = ImageTk.PhotoImage(audi)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "laborghini",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "audi",bootstyle = "dark", width = 20, command = lambda: correct(question_4))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "porsche",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "aston martin",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "bmw",bootstyle = "dark", width = 20, command = lambda: incorrect(question_4))
            option5.place(x = 1150, y = 550)

            def get_hint():
                def get_car_hint(image_path):
                    with open(image_path, "rb") as img:
                        image_bytes = img.read()

                    response = model.generate_content(
                        [
                            "Give me a short hint about what car logo this is. Never reveal the exact car logo.",
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )

                    return response.text
                hint = get_car_hint("audi.jpg")
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def question_4():
            for widget in app.winfo_children():
                widget.destroy() 
            question = tk.Label(app, text = "What brad has this car logo?", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            rr = Image.open("rr.jpg")
            rr = rr.resize((421, 400))
            icon = ImageTk.PhotoImage(rr)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "laborghini",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "Rolls Royce",bootstyle = "dark", width = 20, command = lambda: correct(question_5))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "porsche",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "aston martin",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "bmw",bootstyle = "dark", width = 20, command = lambda: incorrect(question_5))
            option5.place(x = 1150, y = 550)

            def get_hint():
                def get_car_hint(image_path):
                    with open(image_path, "rb") as img:
                        image_bytes = img.read()

                    response = model.generate_content(
                        [
                            "Give me a short hint about what car logo this is. Never reveal the exact car logo.",
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )

                    return response.text
                hint = get_car_hint("rr.jpg")
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def question_5():
            for widget in app.winfo_children():
                widget.destroy() 
            question = tk.Label(app, text = "What brad has this car logo?", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
            question.pack(pady=(0, 30))
                
            honda = Image.open("honda.jpg")
            honda = honda.resize((421, 400))
            icon = ImageTk.PhotoImage(honda)

            image = tk.Label(app, image = icon)
            image.image = icon
            image.place(x = 540, y = 100)

            option1 = ttk.Button(app, text = "laborghini",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option1.place(x = 150, y = 550)

            option2 = ttk.Button(app, text = "honda",bootstyle = "dark", width = 20, command = lambda: correct(final_screen))
            option2.place(x = 400, y = 550)

            option3 = ttk.Button(app, text = "porsche",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option3.place(x = 650, y = 550)

            option4 = ttk.Button(app, text = "aston martin",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option4.place(x = 900, y = 550)

            option5 = ttk.Button(app, text = "bmw",bootstyle = "dark", width = 20, command = lambda: incorrect(final_screen))
            option5.place(x = 1150, y = 550)

            def get_hint():
                def get_car_hint(image_path):
                    with open(image_path, "rb") as img:
                        image_bytes = img.read()

                    response = model.generate_content(
                        [
                            "Give me a short hint about what car logo this is. Never reveal the exact car logo.",
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )

                    return response.text
                hint = get_car_hint("honda.jpg")
                
                hint_label = tk.Label(app, text = f"HINT: {hint}", font=("Segoe UI", 20, "bold"), bg="#f5f5f5")
                hint_label.place(x = 200, y = 650)
                
            
            hint = ttk.Button(app, text = "CLICK HERE FOR A HINT",bootstyle = "success", width = 20,  padding=10, command = get_hint)
            hint.place(x = 1200, y = 200)

        def final_screen():
            for widget in app.winfo_children():
                widget.destroy()

            #fetching the final score from the database and displaying it to the user    
            query = "select * from car_logos where username = ?"
            cursor.execute(query,(username,))
            row = cursor.fetchone()
            if row:
                score = row[1] 
            else:
                score = 0

            card = ttk.Frame(app, padding=40, borderwidth=2, relief="ridge")
            card.place(relx=0.5, rely=0.4, anchor="center")

            message = tk.Label(app, text = f"THE QUIZ HAS ENDED! YOUR SCORE: {score} ", font=("Segoe UI", 18, "bold"), justify="center")
            message.place(x = 750, y = 150)

            img = Image.open("trophy.png")
            img = img.resize((120, 120))
            icon = ImageTk.PhotoImage(img)

            icon_label = tk.Label(app, image=icon)
            icon_label.image = icon
            icon_label.place(x = 1350, y = 250)


            try_again = ttk.Button(app, text="Try Again", bootstyle="info-pill", padding=10, width=15, command = car_logos1)
            try_again.place(x = 800, y = 500)

            back_btn = ttk.Button(app, text="Back to Dashboard", bootstyle="success-pill", padding=10, width=20, command = lambda: launch_dashboard(username))
            back_btn.place(x = 1150, y = 500)

            logout = ttk.Button(app, text="Log out", bootstyle="danger", padding=10, width=20, command = show_login_screen)
            logout.place(x = 975, y = 650)

            global animation_id, gif_label
            animation_id = True

            gif_label = tk.Label(app, bg='#f5f5f5')
            gif_label.place(x = 0, y= 0)

            animate()

        
        question_1()

    #user will choose what type of quiz they want to play
    def engine():
        engine = ttk.Label(app, text = "Test your automotive knowledge with the BMW Engines Quiz! Answer questions about iconic BMW engine \nfamilies, key specs, performance traits, and the innovations that shaped the brand. From classic inline-six \nengines to modern turbocharged designs, see how well you know the power behind “The Ultimate Driving Machine.”", font=("Segoe UI", 12, "bold"), width = 150)
        engine.place(x = 150, y = 500)
        
        launch = ttk.Button(app, text = "Play quiz!", bootstyle = "info", width = 20, command = bmw_engines)
        launch.place(x = 650, y = 650)

    def models():
        models = ttk.Label(app, text = "Explore the full range of car models—from compact city cars and versatile hatchbacks to sporty coupes, powerful sedans, \n rugged SUVs, and advanced electric vehicles. Each model type offers its own blend of performance, comfort, and design, \n giving drivers options suited for every lifestyle and road.", font = ("Segoe UI", 12, "bold"))
        models.place(x = 150, y = 500)
        
        launch = ttk.Button(app, text = "Play quiz!", bootstyle = "info", width = 20, command = car_models)
        launch.place(x = 650, y = 650)

    def car_parts():
        car_parts = ttk.Label(app, text = "Discover the essential car parts that keep every vehicle running—from engines, transmissions, and \nsuspensions to brakes, electronics, and interior components. Each part plays a vital role in performance,\n safety, and comfort, coming together to create a reliable and enjoyable driving experience.", font = ("Segoe UI", 12, "bold"), width = 150)
        car_parts.place(x = 150, y = 500)
        
        launch = ttk.Button(app, text = "Play quiz!", bootstyle = "info", width = 20, command = car_parts1)
        launch.place(x = 650, y = 650)

    def car_logos():
        car_logos = ttk.Label(app, text = "Explore the wide range of car logos—from iconic luxury emblems and bold performance badges to modern \n electric brand symbols. Each logo represents a brand’s identity, heritage, and design philosophy, serving as a \nvisual signature that drivers around the world instantly recognize.", font = ("Segoe UI", 12, "bold"), width = 150)
        car_logos.place(x = 150, y = 500)
        
        launch = ttk.Button(app, text = "Play quiz!", bootstyle = "info", width = 20, command = car_logos1)
        launch.place(x = 650, y = 650)


    #engine
    engine = ttk.Button(app, text = "BMW engines", bootstyle = "dark-outline", width = 30, command = engine )
    engine.place(x = 150, y = 350)

    img = Image.open("n54.jpeg")     
    img = img.resize((259, 200))            
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(app, image=photo)
    label.image = photo                    
    label.place(x = 150, y = 130)
    
    #car models
    models = ttk.Button(app, text = "Car models", bootstyle = "dark-outline", width = 30, command = models)
    models.place(x = 450, y = 350)

    img = Image.open("golf_r.jpg")     
    img = img.resize((259, 200))            
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(app, image=photo)
    label.image = photo                    
    label.place(x = 450, y = 130)

    #car parts
    car_parts = ttk.Button(app, text = "Car parts", bootstyle = "dark-outline", width = 30, command = car_parts)
    car_parts.place(x = 750, y = 350)

    img = Image.open("car_parts.png")     
    img = img.resize((259, 200))            
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(app, image=photo)
    label.image = photo                    
    label.place(x = 750, y = 130)

    #car logos
    car_logos = ttk.Button(app, text = "Car Logos",bootstyle = "dark-outline", width = 30, command = car_logos)
    car_logos.place(x = 1050, y = 350)

    img = Image.open("car_logos.png")     
    img = img.resize((259, 200))            
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(app, image=photo)
    label.image = photo                    
    label.place(x = 1050, y = 130)

    
    #welcome and log out buttons
    welcome = tk.Label(app, text = "Choose your quiz", font=("Segoe UI", 28, "bold"), bg="#f5f5f5")
    welcome.pack(pady=(0, 30))

    logout = ttk.Button(app, text="Logout", bootstyle="danger", width=20, command = show_login_screen)
    logout.place(x = 650, y = 750)




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

    back_to_login = ttk.Button(app, text="Back to Login", width=35, bootstyle="info", command = show_login_screen)
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
        error_message = tk.Label(app, text = "incorrect username or password", font = ("Segoe UI", 15, "bold"))
        error_message.place(x = 750, y = 650)
                           

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
