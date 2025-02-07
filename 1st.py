import pyttsx3
import speech_recognition as sr
import datetime as dt
import wikipedia
import webbrowser
import os
import smtplib
import random as r2
import sys
import wolframalpha
import sqlite3 as sq
from threading import Thread
from tkinter import *

# Initialize the main window
win = Tk()
win.title('Gideon AI')
win.geometry('630x700')
win.config(background="black")

# Mock database connection (you need to replace this with real DB queries)
conn = sq.connect('database.db')
cursor = conn.cursor()
eid = "your_email@gmail.com"  # Replace with your email
enc = "your_password"  # Replace with your email password (or use app password)

# Setup initial variables
usertext = StringVar()
comtext = StringVar()
name = "User"  # Default name, can be changed

# Initialize speech engine
engine = pyttsx3.init('sapi5')
client = wolframalpha.Client('497K74-LQ93WJ8229')  # Your WolframAlpha App ID
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Select a voice

# GUI Setup
def new_GUI():
    root = Tk()
    root.geometry('650x700')
    root.title('Commands List')
    cmds = """                 
    1) Search Google keyword
    2) Search Wikipedia keyword
    3) Email to recipient (ROSAN, ABHISHEK, RANA)
    4) API services (WOLFRAM ALPHA)
    5) Google Maps keyword
    6) Open Visual Code
    7) Open C Drive
    8) Open D Drive
    9) Play music
    10) Play video
    11) Search YouTube keyword
    12) Open Google
    13) Open YouTube
    14) Go Offline/Nothing/Bye
    15) Shutdown
    """
    hpframe = LabelFrame(root, text="Commands:- ", font=('Black ops one', 12, 'bold'), highlightthickness=3)
    hpframe.pack(fill='both', expand='yes')
    hpmsg = Message(hpframe, text=cmds, bg='black', fg='#7adb1e', font=('Comic Sans MS', 10, 'bold'), justify="left")
    hpmsg.pack(fill='both', expand='no')
    exitbtn = Button(root, text='EXIT', font=('#7adb1e', 11, 'bold'), bg='blue', fg='white', borderwidth=5, command=root.destroy)
    exitbtn.pack(fill='x', expand='no')
    root.mainloop()

# Setup the main window
compframe = LabelFrame(win, text="Gideon", font=('Lucida', 10, 'bold'), highlightthickness=2)
compframe.pack(fill='both', expand='yes')
left2 = Message(compframe, textvariable=comtext, bg='#7adb1e', fg='black', justify='left', font=('Lucida', 12, 'bold'), aspect=250)
left2.pack(fill='both', expand='yes')

userframe = LabelFrame(win, text="User", font=('Lucida', 10, 'bold'), highlightthickness=2)
userframe.pack(fill='both', expand='yes')
left1 = Message(userframe, textvariable=usertext, bg='black', fg='#7adb1e', justify='left', font=('Lucida', 12, 'bold'), aspect=250)
left1.pack(fill='both', expand='yes')

comtext.set("Hello! I am your Personal Assistant Gideon. Click on Start button to give your Commands.")
usertext.set(' ')

# Speak function
def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()

# Wish the user based on time of day
def wishMe():
    hour = int(dt.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak(f"Good Morning, {name}!")
    elif hour >= 12 and hour < 18:
        speak(f"Good Afternoon, {name}!")
    else:
        speak(f"Good Evening, {name}!")
    speak(f"How can I assist you today, {name}?")
    usertext.set('Click start speaking button to give Commands')

# Get user name via speech recognition
def Name():
    global name
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("What is your name?")
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        name = r.recognize_google(audio)
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't hear your name. Please try again.")
        Name()
    wishMe()

# Listen for commands and process them
def Commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for commands...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        usertext.set(f"User said: {query}")
        return query.lower()
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't hear that. Please try again.")
        return None

# Define command processing functions
def srch_google(query):
    search_url = f'https://www.google.com/search?q={query}'
    speak(f'Searching Google for: {query}')
    webbrowser.open(search_url)

def srch_yt(query):
    search_url = f'https://www.youtube.com/results?search_query={query}'
    speak(f'Searching YouTube for: {query}')
    webbrowser.open(search_url)

def search_wikipedia(query):
    speak('Searching Wikipedia...')
    results = wikipedia.summary(query, sentences=3)
    speak(f"According to Wikipedia: {results}")
    print(results)

def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(eid, enc)
        server.sendmail(eid, to, content)
        server.close()
        speak(f"Email sent to {to} successfully!")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't send the email.")

# Process the command after listening
def process_command():
    query = Commands()
    if query is None:
        return

    if 'search google' in query:
        query = query.replace('search google', '').strip()
        srch_google(query)

    elif ' youtube' in query:
        query = query.replace(' youtube', '').strip()
        srch_yt(query)

    elif 'wikipedia' in query:
        query = query.replace('wikipedia', '').strip()
        search_wikipedia(query)

    elif 'email' in query:
        speak("Who is the recipient?")
        recipient = Commands()
        speak("What should I say?")
        content = Commands()
        send_email(recipient, content)

    elif 'shutdown' in query:
        speak("Shutting down the system.")
        os.system('shutdown /s')

    elif 'exit' in query or 'bye' in query:
        speak("Goodbye! Have a great day!")
        win.quit()
        sys.exit()

    else:
        speak("Sorry, I didn't understand that.")

# Main function to start the assistant
def mainfn():
    Name()
    while True:
        process_command()

# Start the assistant in a separate thread
def start_assistant():
    Thread(target=mainfn).start()

# GUI buttons
btn = Button(win, text='Start!', font=('#7adb1e', 11, 'bold'), bg='black', fg='#7adb1e', borderwidth=5, command=start_assistant)
btn.pack(fill='x', expand='no')

btn1 = Button(win, text='Command List', font=('#7adb1e', 11, 'bold'), bg='black', fg='#7adb1e', borderwidth=5, command=new_GUI)
btn1.pack(fill='x', expand='no')

btn2 = Button(win, text='EXIT', font=('#7adb1e', 11, 'bold'), bg='red', fg='white', borderwidth=5, command=sys.exit)
btn2.pack(fill='x', expand='no')

win.mainloop()
