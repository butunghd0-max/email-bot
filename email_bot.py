"""
Voice-Activated Email Bot
=========================
Inspired by my sister's MYP Personal Project (2021-2022).

Compose and send emails with just your voice.
Uses speech recognition + text-to-speech + Gmail SMTP.

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

# load secrets from .env
load_dotenv()
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# ElevenLabs voice config
# pick a voice from https://elevenlabs.io/voice-library
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
ELEVENLABS_MODEL = os.getenv("ELEVENLABS_MODEL", "eleven_multilingual_v2")

# nicknames mapped to email addresses so the bot
# doesn't have to parse something like "john dot doe at gmail dot com"
CONTACTS = {
    "dude": "erenatsuidesu@gmail.com",
    "car": "bicycleandcar@gmail.com",
    # "mom": "mom.email@gmail.com",
    # "best friend": "friend@gmail.com",
}

# speech engines
listener = sr.Recognizer()
engine = pyttsx3.init()

# try loading ElevenLabs, fall back to pyttsx3 if it's not set up
eleven_client = None
eleven_play = None
if ELEVENLABS_API_KEY:
    try:
        from elevenlabs.client import ElevenLabs
        from elevenlabs.play import play as eleven_play_fn
        eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        eleven_play = eleven_play_fn
        print("[TTS] ElevenLabs connected.")
    except Exception as e:
        print(f"[TTS] Couldn't load ElevenLabs ({e}), using pyttsx3.")
else:
    print("[TTS] No ElevenLabs key, using pyttsx3.")


# -- text-to-speech -----------------------------------------------------------

def _talk_elevenlabs(text):
    """Send text to ElevenLabs and play the audio. Returns True if it worked."""
    try:
        audio = eleven_client.text_to_speech.convert(
            text=text,
            voice_id=ELEVENLABS_VOICE_ID,
            model_id=ELEVENLABS_MODEL,
            output_format="mp3_44100_128",
        )
        eleven_play(audio)
        return True
    except Exception as e:
        print(f"[TTS] ElevenLabs failed ({e}), switching to pyttsx3.")
        return False


def _talk_pyttsx3(text):
    """Offline fallback voice."""
    engine.say(text)
    engine.runAndWait()


def talk(text):
    """Say something out loud. Tries ElevenLabs first, pyttsx3 if that fails."""
    print(f"[Bot] {text}")
    if eleven_client and not _talk_elevenlabs(text):
        _talk_pyttsx3(text)
    elif not eleven_client:
        _talk_pyttsx3(text)


# -- speech-to-text ------------------------------------------------------------

def get_info(retries=3):
    """
    Listen through the mic and return what the user said (lowercase).
    Retries a few times if it can't understand, then gives up.
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


# -- email sending -------------------------------------------------------------

def send_email(receiver, subject, message):
    """Log into Gmail SMTP and fire off the email."""
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


# -- main loop -----------------------------------------------------------------

def get_email_info():
    """Walk through: who to send to, subject, body, then send it."""

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

    talk("What is the subject of your email?")
    subject = get_info()
    if subject is None:
        subject = "(no subject)"

    talk("Tell me the text of your email.")
    message = get_info()
    if message is None:
        message = ""

    talk(f"Alright, I'll send an email to {name} with subject: {subject}.")
    talk("Sending now...")

    try:
        send_email(receiver, subject, message)
        talk("Your email has been sent!")
    except Exception as e:
        talk("Something went wrong while sending your email.")
        print(f"SMTP Error: {e}")
        return

    talk("Do you want to send another email?")
    send_more = get_info()
    if send_more and "yes" in send_more:
        get_email_info()
    else:
        talk("Goodbye! Have a great day.")


if __name__ == "__main__":
    print("=" * 50)
    print("  VOICE-ACTIVATED EMAIL BOT")
    print("  Say your commands, no typing needed!")
    print("=" * 50)
    get_email_info()
