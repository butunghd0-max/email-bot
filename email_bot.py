"""
Voice-Activated Email Bot
=========================
Inspired by my sister's MYP Personal Project (2021-2022).

This bot lets you compose and send emails entirely by voice.
It uses speech recognition to listen, text-to-speech to talk back,
and Gmail's SMTP server to deliver your messages.

Setup:
  1. pip install -r requirements.txt
  2. Generate a Gmail App Password:
     Google Account > Security > 2-Step Verification > App Passwords
  3. Copy .env and fill in your Gmail address and App Password.
  4. Update the CONTACTS dictionary with your own contacts.
  5. Run:  python email_bot.py
"""

import os
import smtplib
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from email.message import EmailMessage

# -- Configuration ------------------------------------------------------------
# Credentials are loaded from a .env file in the same directory.
# See .env.example for the required variables.
load_dotenv()
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# ── Contact Dictionary ───────────────────────────────────────────────────────
# Map easy-to-say nicknames to real email addresses so the bot doesn't have
# to parse complex email strings from speech.
CONTACTS = {
    "dude": "erenatsuidesu@gmail.com",
    "car": "bicycleandcar@gmail.com",
    # Add your own contacts here, e.g.:
    # "mom": "mom.email@gmail.com",
    # "best friend": "friend@gmail.com",
}

# ── Initialize Speech Engines ────────────────────────────────────────────────
listener = sr.Recognizer()
engine = pyttsx3.init()


# ── Step 2: The "Mouth" (Text-to-Speech) ────────────────────────────────────
def talk(text):
    """Make the bot speak the given text aloud."""
    print(f"[Bot] {text}")
    engine.say(text)
    engine.runAndWait()


# ── Step 3: The "Ears" (Speech-to-Text) ──────────────────────────────────────
def get_info(retries=3):
    """
    Listen through the microphone, convert speech to text using
    Google's speech recognition API, and return the result as
    a lowercase string.  Returns None if recognition fails.

    Retries up to `retries` times on unrecognized speech before
    giving up, to avoid infinite recursion from background noise.
    """
    if retries <= 0:
        talk("I still couldn't understand. Let's move on.")
        return None

    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source, duration=0.5)
            voice = listener.listen(source)
            info = listener.recognize_google(voice)
            print(f"You said: {info}")
            return info.lower()
    except sr.UnknownValueError:
        talk("Sorry, I didn't catch that. Could you repeat?")
        return get_info(retries - 1)
    except sr.RequestError:
        talk("Sorry, my speech service is down right now.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# ── Step 4: The Email Engine ─────────────────────────────────────────────────
def send_email(receiver, subject, message):
    """
    Connect to Gmail's SMTP server, authenticate, build an
    EmailMessage, and send it.
    """
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)

    email = EmailMessage()
    email["From"] = GMAIL_ADDRESS
    email["To"] = receiver
    email["Subject"] = subject
    email.set_content(message)

    server.send_message(email)
    server.quit()


# ── Step 5: Main Conversation Loop ──────────────────────────────────────────
def get_email_info():
    """
    Walk the user through composing an email entirely by voice:
    recipient, subject, body, send, ask to repeat.
    """
    # --- Who to send to ---
    talk("To whom do you want to send an email?")
    available = ", ".join(CONTACTS.keys())
    talk(f"Your contacts are: {available}")
    name = get_info()

    if name is None:
        talk("I couldn't understand the contact name. Let's try again.")
        return get_email_info()

    receiver = CONTACTS.get(name)
    if receiver is None:
        talk(f"I don't have a contact called '{name}'. Please try again.")
        return get_email_info()

    print(f"Sending to: {receiver}")

    # --- Subject ---
    talk("What is the subject of your email?")
    subject = get_info()
    if subject is None:
        subject = "(no subject)"

    # --- Body ---
    talk("Tell me the text of your email.")
    message = get_info()
    if message is None:
        message = ""

    # --- Confirm & Send ---
    talk(f"Alright, I'll send an email to {name} with subject: {subject}.")
    talk("Sending now...")

    try:
        send_email(receiver, subject, message)
        talk("Your email has been sent!")
    except Exception as e:
        talk("Something went wrong while sending your email.")
        print(f"SMTP Error: {e}")
        return

    # --- Loop? ---
    talk("Do you want to send another email?")
    send_more = get_info()
    if send_more and "yes" in send_more:
        get_email_info()
    else:
        talk("Goodbye! Have a great day.")


# ── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  VOICE-ACTIVATED EMAIL BOT")
    print("  Say your commands, no typing needed!")
    print("=" * 50)
    get_email_info()
