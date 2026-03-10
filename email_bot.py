"""
Voice-Activated Email Bot
Inspired by my sister's MYP Personal Project (2021-2022).

Setup:
  1. pip install -r requirements.txt
  2. Generate a Gmail App Password
  3. Fill in .env with your credentials
  4. Update CONTACTS below
  5. Run: python email_bot.py
"""

import os
import smtplib
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
ELEVENLABS_MODEL = os.getenv("ELEVENLABS_MODEL", "eleven_multilingual_v2")

# nicknames instead of real addresses so the mic doesn't have to parse
# "john dot doe at gmail dot com"
CONTACTS = {
    "dude": "erenatsuidesu@gmail.com",
    "car": "bicycleandcar@gmail.com",
}

listener = sr.Recognizer()
engine = pyttsx3.init()

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


def _talk_elevenlabs(text):
    try:
        audio = eleven_client.text_to_speech.convert(
            text=text,
            voice_id=ELEVENLABS_VOICE_ID,
            model_id=ELEVENLABS_MODEL,
            output_format="mp3_44100_128",
        )
        eleven_play(audio)
        return True
    except Exception:
        return False


def _talk_pyttsx3(text):
    engine.say(text)
    engine.runAndWait()


def talk(text):
    print(f"[Bot] {text}")
    # try ElevenLabs, fall back to pyttsx3 per-call so the bot
    # keeps working if ElevenLabs dies mid-session
    if eleven_client:
        if not _talk_elevenlabs(text):
            _talk_pyttsx3(text)
    else:
        _talk_pyttsx3(text)


def get_info(retries=3):
    # retries cap prevents infinite recursion from background noise
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


def send_email(receiver, subject, message):
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


def get_email_info():
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
