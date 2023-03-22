import os
import sys
import time
import json
import random
import struct
import pyaudio
import requests
import pyttsx3
import winsound
import webbrowser
import pvporcupine
import openai as assistant
import speech_recognition as sprecog


def speak_evo(evotext):
    speaker = pyttsx3.init("sapi5")
    speaker.setProperty("rate", 145)
    voices = speaker.getProperty("voices")
    speaker.setProperty("voice", voices[0].id)
    print(f"E.V.O: {evotext}")
    speaker.say(evotext)
    speaker.runAndWait()


def evo_command():
    recog = sprecog.Recognizer()
    with sprecog.Microphone() as mic:
        userquery = ""
        recog.adjust_for_ambient_noise(mic, duration=0.2)
        winsound.Beep(600, 200)
        print("LISTENING: ")
        recog.pause_threshold = 4
        recog.operation_timeout = 4
        audio = recog.listen(mic)
        try:
            winsound.Beep(400, 200)
            print(f"RECOGNIZING: {audio}")
            userquery = recog.recognize_google(
                audio_data=audio, language="en-us")
            print(f"USER SAID: {userquery}")
        except Exception as e:
            print(e)
            speak_evo("Sorry, I did not get that.")
            return "none"
        return userquery.lower()


greetings = ["hello", "hey", "hi"]
goodbye = ["bye", "goodbye", "tata"]
feeling = ["how are you feeling"]
areyou = ["who are you", "what are you"]
shutdown = ["shutdown", "poweroff"]


def evo_flow():
    resp = open("models/responses.json")
    evoresponses = json.load(resp)
    while True:
        usersaid = evo_command()
        if usersaid in greetings:
            speak_evo(random.choice(evoresponses["greetings"]["responses"]))
            break
        elif usersaid in goodbye:
            speak_evo(random.choice(evoresponses["goodbye"]["responses"]))
            break
        elif usersaid in feeling:
            speak_evo(random.choice(evoresponses["feeling"]["responses"]))
            break
        elif usersaid in areyou:
            speak_evo(random.choice(evoresponses["areyou"]["responses"]))
            break
        elif usersaid in areyou:
            speak_evo(random.choice(evoresponses["areyou"]["responses"]))
            break
        elif usersaid in shutdown:
            speak_evo(random.choice(evoresponses["shutdown"]["responses"]))
            os.system("shutdown /s /t 1")
        elif "play" in usersaid:
            songname = usersaid.split("play", 1)[1]
            try:
                api = requests.get(
                    f"https://magneum.vercel.app/api/youtube_sr?q={songname}")
                speak_evo(f"Playing {songname} on youtube browser.")
                webbrowser.open(api.json()["youtube_search"][0]["LINK"], new=2)
            except Exception as e:
                speak_evo(f"Sorry could not play {songname} on youtube.")
                break
            break
        else:
            try:
                assistant.api_key = "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"
                # print(openai.Model.list())
                response = assistant.Completion.create(
                    engine="text-davinci-003",
                    prompt=usersaid.capitalize(),
                    temperature=1,
                    max_tokens=4000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                resp = response["choices"][0]["text"].capitalize()
                print(f"E.V.O: {resp}")
                speak_evo(resp)
                break
            except Exception as e:
                print(f"ERROR: {e}")
                speak_evo(f"Sorry I could not understand that.")
                break


greetInit = ["hi there smart human", "hello sir"]


def evoai():
    pa = None
    porcupine = None
    audio_stream = None
    speak_evo(random.choice(greetInit))
    try:
        porcupine = pvporcupine.create(
            access_key="kHRZWPKCJGzWJpxesmNHzYJNBSdpxc5MR0TgdIuwxf8TRMyPTvwtGw==", keyword_paths=["models/hey-evo-windows.ppn"])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            channels=1,
            input=True,
            format=pyaudio.paInt16,
            rate=porcupine.sample_rate,
            frames_per_buffer=porcupine.frame_length
        )
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            wake_index = porcupine.process(pcm)
            if wake_index == 0:
                print("WAKE WORD DETECTED: ")
                evo_flow()
                print("ON HOLD: ")
    except Exception as e:
        print(f"ERROR: {e}")
        pass
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()


evoai()


# ================================================================ GREETINGS
# Hi there!
# Hey, how are you?
# Good morning/afternoon/evening!
# Nice to see you!
# Howdy!
# Greetings!
# Yo!
# Hi, how's it going?
# Hey, what's up?
# How are things?
# Hello, how can I assist you?
# Hi, nice to meet you!
# Good to see you!
# Hi, what brings you here?
# Hello, how have you been?
# Hey, long time no see!
# Hiya!
# Hi, how can I help you today?
# Hello, what's on your mind?
# Hi, it's good to hear from you!
# Hey, what have you been up to?
# Hello, what's new?
# Hi, what's happening?
# Hey, how's your day going?
# Good day!
# Hello, I hope you're doing well!
# Hi, how can I be of service?
# Hey, how's life treating you?
# Hello, what's the latest news?
# Hi, how's your week been so far?
# Hey, nice to talk to you!
# Hello, what's the plan for today?
# Hi, how's the weather treating you?
# Hey, how's your family doing?
# Hello, what brings you joy?
# Hi, what's your name?
# Hey, what are your interests?
# Hello, how do you spend your free time?
# Hi, what's your favorite hobby?
# Hey, what's your favorite food?
# Hello, where are you from?
# Hi, what's your occupation?
# Hey, what's your favorite movie?
# Hello, what's your favorite book?
# Hi, what's your favorite music genre?
# Hey, what's your favorite sport?
# Hello, what's your favorite travel destination?
# Hi, what's your favorite TV show?
# Hey, what's your favorite season?
# Hello, what's your favorite way to relax?

# ================================================================ GOODBYE
# Goodbye, take care!
# See you later!
# Farewell!
# Have a nice day!
# Bye for now!
# Catch you later!
# See you soon!
# So long!
# Until next time!
# Have a great day!
# Bye-bye!
# See you tomorrow!
# Take it easy!
# Have a safe trip!
# Until we meet again!
# See you next week/month/year!
# Have a good one!
# Take care of yourself!
# Goodbye, it was nice seeing you!
# I'll miss you!
# Have a great weekend!
# Goodbye, stay in touch!
# Have a pleasant evening/night!
# Goodbye, thanks for coming!
# It's been great talking to you!
# Goodbye, I hope to see you soon!
# Have a wonderful day!
# Goodbye, keep in touch!
# Have a good evening/night!
# Goodbye, have a safe journey!
# It was nice to meet you, goodbye!
# Goodbye, I wish you all the best!
# Until next time, take care!
# Goodbye, I'll be thinking of you!
# Have a happy holiday!
# Goodbye, it's been a pleasure!
# See you on the flip side!
# Goodbye, have a great time!
# Have a good trip!
# Goodbye, enjoy your day!
# See you around!
# Goodbye, I'll see you soon!
# Have a nice weekend!
# Goodbye, I'll catch up with you later!
# Have a great vacation!
# Goodbye, I'll be in touch!
# Have a great time!
# Goodbye, I'll see you next time!
# Until we meet again, goodbye!
# Have a fantastic day!

# ================================================================ FEELING
# I'm doing well, thank you for asking.
# I'm fine, thanks for asking.
# I'm good, how about you?
# Not too bad, how are you doing?
# I'm great, thanks for asking.
# I'm okay, thanks for asking.
# I'm doing well, how about yourself?
# I'm pretty good, thanks for asking.
# I'm alright, how are you?
# I'm doing well, and you?
# I'm doing great, how about you?
# I'm fantastic, thank you for asking.
# I'm doing fine, thanks for asking.
# I'm doing alright, how about yourself?
# I'm excellent, thanks for asking.
# I'm doing pretty well, how about you?
# I'm doing very well, thanks for asking.
# I'm not too bad, how about you?
# I'm doing good, and you?
# I'm doing great, thanks for asking.
# I'm good, and yourself?
# I'm doing well, how's everything with you?
# I'm doing just fine, thank you for asking.
# I'm doing pretty good, how about yourself?
# I'm doing fantastic, how are you?
# I'm okay, how about you?
# I'm doing well, thank you. How are you doing?
# I'm doing very well, and you?
# I'm doing great, how are you?
# I'm doing fine, and you?
# I'm good, how about you?
# I'm alright, thanks for asking.
# I'm doing well, and yourself?
# I'm doing pretty well, thanks for asking.
# I'm doing great, how's everything going with you?
# I'm good, thank you for asking.
# I'm doing well, and you?
# I'm doing pretty good, how about you?
# I'm doing fantastic, and you?
# I'm okay, how are you?
# I'm doing well, thank you. And you?
# I'm good, how are you doing?
# I'm doing fine, and yourself?
# I'm great, thanks for asking.
# I'm doing pretty well, how about yourself?
# I'm doing well, and how about yourself?
# I'm good, how's everything with you?
# I'm doing well, thanks for asking. How are you?
# I'm doing great, and how about you?
# I'm fine, how are you doing?

# ================================================================ ERROR
# Sorry, there seems to be an error.
# Oops! Something went wrong.
# Looks like we've hit a snag.
# Sorry, the system is experiencing an error.
# Error! Please try again later.
# Sorry, something seems to have gone awry.
# There seems to be a problem.
# Oops! There was an error.
# Sorry, an error has occurred.
# The system encountered an error.
# Sorry, we're having trouble processing your request.
# There was an error. Please try again later.
# Something went wrong. Please try again.
# Sorry, we're experiencing some technical difficulties.
# Oops! There was an issue.
# There was a glitch. Please try again later.
# Sorry, something went wrong on our end.
# It seems there was an error with the system.
# Sorry, there's been a hiccup.
# Something's not working as expected.
# Oops! There seems to be an error.
# We're sorry, something went wrong.
# There was an error in the process.
# Sorry, the system is experiencing an issue.
# We're having trouble completing your request due to an error.
# Sorry, an error occurred while processing your request.
# There was an unexpected error.
# Sorry, something has gone wrong with the system.
# We're sorry, there was an error in the system.
# Oops! The system is encountering an error.
# There was an issue with the system.
# Sorry, we're having trouble with the system at the moment.
# There was an error during the process.
# Sorry, we're experiencing some technical issues.
# Something has gone wrong. Please try again later.
# There was an error with the request.
# Sorry, we've encountered an error and are working to resolve it.
# There seems to be a problem with the system.
# We're sorry, there was an error with your request.
# Oops! There was a technical issue.
# Sorry, there was an error and your request could not be completed.
# There was an error in the system. Please try again later.
# Sorry, something went wrong and we're working on it.
# There was an error processing your request. Please try again later.
# We're sorry, there was an error and we're investigating it.
# Oops! Something has gone wrong with the system.
# Sorry, we're having trouble with the system. Please try again later.
# There was an error in the process. Please try again later.
# We're sorry, there was an error and we're trying to fix it.
# Sorry, we're experiencing an error and are working to resolve it.

# ================================================================ OWNER GREET
# Hello, sir! How are you doing today?
# Good day, sir. How can I assist you?
# Hi there, sir. What brings you here?
# Greetings, sir. How can I be of service?
# Hey, sir. What's new in your world?
# Welcome, sir. How can I help you today?
# Hello, sir. I hope you're having a great day!
# Good morning/afternoon/evening, sir. How may I assist you?
# Hi, sir. It's nice to see you here.
# Welcome back, sir. What can I help you with?
# Hello, sir. How's everything going?
# Hey there, sir. What brings you by today?
# Hi, sir. It's great to have you here.
# Good to see you, sir. How can I be of assistance?
# Hello, sir. How can I support you today?
# Hey, sir. Is there anything I can do for you?
# Hi, sir. What can I help you with today?
# Welcome, sir. How's your day going?
# Good day, sir. What can I assist you with?
# Hello, sir. How can I make your day better?
# Hey, sir. How can I help you achieve your goals?
# Hi there, sir. How can I support your work?
# Good morning/afternoon/evening, sir. What brings you in today?
# Hello, sir. What can I do to help you succeed?
# Hi, sir. How can I help you optimize your workflow?
# Welcome back, sir. How can I help you stay productive?
# Hey, sir. What's on your mind today?
# Hi there, sir. What can I help you with right now?
# Hello, sir. What can I do to assist you?
# Good to see you, sir. How can I help you reach your goals?
# Hi, sir. How can I support your work to be more efficient?
# Hey, sir. How can I help you improve your performance?
# Hello, sir. How can I be of service to you today?
# Hi there, sir. What can I help you with to make your life easier?
# Welcome, sir. How can I support your success?
# Hey, sir. What can I do to help you achieve your objectives?
# Good day, sir. What brings you by today?
# Hi, sir. What can I do to help you be more productive?
# Hello, sir. How can I help you get the most out of your day?
# Hey there, sir. How can I help you optimize your resources?
# Hi, sir. What can I do to support your growth?
# Hello, sir. How can I help you be more successful?
# Hey, sir. What's on your agenda for today?
# Hi there, sir. What can I help you with to maximize your potential?

# ================================================================ SMALL TALKS
# How's your day going so far?
# Have you seen any good movies or TV shows lately?
# Do you have any fun plans for the weekend?
# What do you like to do in your free time?
# What kind of music do you enjoy listening to?
# Have you traveled anywhere interesting lately?
# Do you have any pets?
# How do you like to spend your evenings?
# What's your favorite food?
# Do you enjoy reading? What kind of books do you like?
# Are you a morning person or a night owl?
# Do you play any sports or enjoy any outdoor activities?
# Have you tried any new restaurants recently?
# What's your favorite hobby?
# Do you prefer coffee or tea?
# What's your favorite season?
# Do you have any upcoming vacations planned?
# Have you watched any good documentaries lately?
# Are you a fan of any particular sports team?
# Do you have a favorite book or author?
# What kind of TV shows do you like to watch?
# Do you have any siblings?
# Have you attended any concerts or live events recently?
# What's your favorite type of cuisine?
# Are you into any particular type of exercise or workout?
# Do you have any favorite podcasts or YouTubers?
# What kind of technology do you use the most?
# Do you have any hidden talents or hobbies?
# Have you tried any new recipes lately?
# What's your favorite type of dessert?
# Do you prefer the city or the countryside?
# Do you have any upcoming events or special occasions?
# Have you ever lived in another country or culture?
# What's your favorite type of art or creative expression?
# Do you enjoy hiking or camping?
# What's your favorite type of weather?
# Have you ever met anyone famous?
# Do you have any favorite quotes or sayings?
# What's your favorite type of exercise or activity to do with friends?
# Do you have any interesting or unique life experiences?
# Are you involved in any volunteering or charity work?
# Have you tried any new hobbies or activities recently?
# What's your favorite type of wine or beer?
# Do you have any favorite comedians or stand-up comedy specials?
# Do you have any favorite board games or card games?
# Have you tried any new apps or technology tools recently?
# What's your favorite type of flower or plant?
# Do you have any favorite motivational or self-help books?
# What's your favorite type of exercise or activity to do alone?
# Do you have any favorite podcasts or audiobooks?

# ================================================================ SHUTDOWN
