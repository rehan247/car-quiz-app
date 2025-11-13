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

login_button = tk.Button(app, text = "Log in", width = 10)
login_button.place(x = 650, y = 500)
