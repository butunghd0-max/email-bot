# Voice-Activated Email Bot

> _Inspired by my sister's MYP Personal Project (2021-2022)_

A Python bot that lets you **compose and send emails entirely by voice**, no typing needed. Built with speech recognition, text-to-speech, and Gmail's SMTP server.

---

## How It Works

| Step | Component        | Library                         | Purpose                                                 |
| ---- | ---------------- | ------------------------------- | ------------------------------------------------------- |
| 1    | **Mouth**        | `pyttsx3`                       | Speaks prompts and confirmations aloud                  |
| 2    | **Ears**         | `SpeechRecognition` + `PyAudio` | Listens via microphone, converts speech to text         |
| 3    | **Email Engine** | `smtplib` + `email.message`     | Connects to Gmail SMTP and sends the message            |
| 4    | **Logic Loop**   | Python                          | Guides the conversation: recipient, subject, body, send |

---

## Setup

### 1. Install Python

Make sure [Python 3.8+](https://www.python.org/downloads/) is installed and available on your PATH.

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

### 3. Generate a Gmail App Password

Google no longer supports "less secure app access." You need an **App Password**:

1. Go to [Google Account > Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (if not already on)
3. Go to **App Passwords** > Generate one for "Mail"
4. Copy the **16-character password**

### 4. Configure the Bot

Open `email_bot.py` and replace:

```python
GMAIL_ADDRESS = "YOUR_EMAIL@gmail.com"
GMAIL_APP_PASSWORD = "YOUR_APP_PASSWORD"
```

Update the `CONTACTS` dictionary with your own contacts:

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
|-- email_bot.py       # Main bot script
|-- requirements.txt   # Python dependencies
|-- README.md          # This file
```

---

## Background

During the COVID-19 pandemic, staying connected through email became important but tedious, especially for students doing home-based learning. This project was born from the idea that **voice commands** (like talking to Alexa) could make sending personal emails faster and more accessible for everyone.
