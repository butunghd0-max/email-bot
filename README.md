# Voice-Activated Email Bot

> _Inspired by my sister's MYP Personal Project (2021-2022)_

A Python bot that lets you compose and send emails entirely by voice, no typing needed. It listens through your mic, talks back to you, and sends emails through Gmail.

---

## How It Works

| Component        | What it does                                      | Library                                      |
| ---------------- | ------------------------------------------------- | -------------------------------------------- |
| **Mouth**        | Talks to you (prompts, confirmations)             | ElevenLabs API or pyttsx3 (offline fallback) |
| **Ears**         | Listens through your mic, converts speech to text | SpeechRecognition + PyAudio                  |
| **Email Engine** | Connects to Gmail and sends the email             | smtplib + email.message                      |
| **Main Loop**    | Walks you through: recipient, subject, body, send | Python                                       |

The bot tries to use [ElevenLabs](https://elevenlabs.io) for a natural-sounding AI voice. If the API key isn't set, or if it runs out of credits or goes offline, it automatically switches to pyttsx3 (the built-in offline voice).

---

## Setup

### 1. Install Python

Make sure [Python 3.8+](https://www.python.org/downloads/) is on your system.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> **PyAudio troubleshooting (Windows):** If `pip install pyaudio` fails, try:
>
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

You may also need [mpv](https://mpv.io/) or [ffmpeg](https://ffmpeg.org/) installed for ElevenLabs audio playback.

### 3. Generate a Gmail App Password

Google killed "less secure app access" so you need an App Password:

1. Go to [Google Account > Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** if you haven't already
3. Go to **App Passwords** > Generate one for "Mail"
4. Copy the 16-character password

### 4. Configure

Open `.env` and fill in your stuff:

```
GMAIL_ADDRESS=your.email@gmail.com
GMAIL_APP_PASSWORD=abcdefghijklmnop
ELEVENLABS_API_KEY=your_key_here
```

The ElevenLabs key is optional. Without it the bot just uses the offline voice.

You can get a free ElevenLabs API key at [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys).

Then update the `CONTACTS` dictionary in `email_bot.py` with your own people:

```python
CONTACTS = {
    "mom": "mom.email@gmail.com",
    "best friend": "bestie@gmail.com",
}
```

### 5. Run

```bash
python email_bot.py
```

---

## Project Structure

```
Email bot (inspired by my sister the goat)/
|-- email_bot.py       # the bot
|-- requirements.txt   # pip dependencies
|-- .env               # your secrets (git-ignored)
|-- .gitignore
|-- README.md
```

---

## Background

During COVID my sister built a voice email bot for her MYP Personal Project. The idea was that voice commands (like talking to Alexa) could make sending emails easier for people stuck at home who didn't feel like typing. This is a rebuilt version of that project with some upgrades like ElevenLabs integration and better error handling.
