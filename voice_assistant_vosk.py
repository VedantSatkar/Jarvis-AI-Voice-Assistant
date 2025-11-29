import os
import sys
import queue
import json
import subprocess
import platform
import webbrowser
import datetime
import re
import time
import pywhatkit
import shutil
import sounddevice as sd
import vosk
import pyttsx3

# Screenshot optional
try:
    import pyautogui
    PYAUTO = True
except Exception:
    pyautogui = None
    PYAUTO = False


# ===========================
#   TTS (Hindi + English)
# ===========================
engine = pyttsx3.init()
engine.setProperty("rate", 155)

for v in engine.getProperty("voices"):
    if "Hindi" in v.name or "hi" in v.id:
        engine.setProperty("voice", v.id)
        break

def speak(msg):
    print("Assistant:", msg)
    try:
        engine.say(msg)
        engine.runAndWait()
    except:
        pass


# ===========================
#  Load Vosk Model (Hindi preferred)
# ===========================
def load_model():
    md = "models"
    if not os.path.isdir(md):
        print("❌ models/ folder missing.")
        sys.exit(1)

    # Prefer Hindi
    for n in os.listdir(md):
        if "hi" in n.lower():
            return os.path.join(md, n), "hi"

    # Otherwise English
    for n in os.listdir(md):
        if "en" in n.lower():
            return os.path.join(md, n), "en"

    print("❌ No Hindi/English model in models/")
    sys.exit(1)

model_path, LANG = load_model()
model = vosk.Model(model_path)


# ===========================
#     Microphone
# ===========================
audio_q = queue.Queue()

def callback(indata, frames, t, status):
    audio_q.put(bytes(indata))


# ===========================
#  TEXT NORMALIZATION
# ===========================
def normalize(t):
    t = t.lower()
    t = t.replace("please", "")
    t = t.replace("could you", "")
    t = t.replace("please open", "open")
    return re.sub(" +", " ", t).strip()


# ===========================
#  INTELLIGENT APP OPENER
# ===========================
def smart_open(exe_names, web_url=None, spoken_name=""):
    """
    Try to find the executable in PATH or Program Files.
    If not found → open web fallback.
    """
    # 1. Check PATH
    for exe in exe_names:
        path = shutil.which(exe)
        if path:
            subprocess.Popen([path])
            speak(f"{spoken_name} खोल रहा हूँ")
            return True

    # 2. Common Windows install locations
    drives = ["C:\\", "D:\\", "E:\\"]

    for exe in exe_names:
        for d in drives:
            for folder in [
                "Program Files",
                "Program Files (x86)",
                f"Users\\{os.getlogin()}\\AppData\\Local",
                f"Users\\{os.getlogin()}\\AppData\\Roaming",
            ]:
                full = os.path.join(d, folder)
                if not os.path.isdir(full):
                    continue
                for root, _, files in os.walk(full):
                    if exe.lower() in [f.lower() for f in files]:
                        subprocess.Popen([os.path.join(root, exe)])
                        speak(f"{spoken_name} खोल रहा हूँ")
                        return True

    # 3. Fallback to web
    if web_url:
        speak(f"{spoken_name} Desktop नहीं मिला, वेब खोल रहा हूँ।")
        webbrowser.open(web_url)
        return True

    return False


def open_app(name):
    n = name.lower()

    # WhatsApp variations
    if any(w in n for w in ["whatsapp", "watsapp", "whats app", "वाट्सएप", "व्हाट्सएप"]):
        return smart_open(
            ["WhatsApp.exe"],
            web_url="https://web.whatsapp.com",
            spoken_name="WhatsApp"
        )

    # Chrome
    if any(w in n for w in ["chrome", "क्रोम", "browser", "ब्राउज़र"]):
        return smart_open(
            ["chrome.exe", "msedge.exe"],
            web_url="https://google.com",
            spoken_name="Browser"
        )

    # Notepad
    if "notepad" in n or "नोटपैड" in n:
        return smart_open(["notepad.exe"], spoken_name="Notepad")

    # Calculator
    if "calculator" in n or "कैलकुलेटर" in n:
        return smart_open(["calc.exe"], spoken_name="Calculator")

    return False


# ===========================
#  SEARCH
# ===========================
def do_search(q):
    url = "https://www.google.com/search?q=" + q.replace(" ", "+")
    webbrowser.open(url)
    speak(f"{q} की खोज कर रहा हूँ")


def do_youtube(q):
    url = "https://www.youtube.com/results?search_query=" + q.replace(" ", "+")
    webbrowser.open(url)
    speak(f"YouTube पर {q} खोज रहा हूँ")


# ===========================
#  HANDLE COMMANDS
# ===========================
def handle(text):
    t = normalize(text)

    # Exit
    if t in ("exit", "quit", "stop", "बंद", "रुको"):
        speak("अलविदा!")
        return "exit"

    # Greetings
    if any(x in t for x in ["hello", "hi", "hey", "नमस्ते", "हेलो"]):
        speak("नमस्ते! कैसे मदद करूँ?")
        return

    # Time
    if any(x in t for x in ["time", "समय", "वक्त"]):
        tm = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"समय है {tm}")
        return

    # Screenshot
    if any(x in t for x in ["screenshot", "स्क्रीनशॉट"]):
        if PYAUTO:
            fname = f"screenshot_{int(time.time())}.png"
            pyautogui.screenshot().save(fname)
            speak(f"Screenshot save हुआ {fname}")
        else:
            speak("Screenshot उपलब्ध नहीं")
        return

    # OPEN
    if t.startswith("open "):
        target = t.replace("open ", "").strip()
        if not open_app(target):
            do_search(target)
        return

    if "खोलो" in t:
        target = t.replace("खोलो", "").strip()
        if not open_app(target):
            do_search(target)
        return

    # YouTube Search
    if "youtube" in t and "search" in t:
        do_youtube(t.replace("search youtube for", "").strip())
        return

    if "यूट्यूब" in t and ("खोजो" in t or "सर्च" in t):
        q = t.replace("यूट्यूब", "").replace("खोजो", "").replace("सर्च", "")
        do_youtube(q.strip())
        return

    # Google Search
    if "search" in t or "खोजो" in t or "सर्च" in t:
        q = t.replace("search", "").replace("खोजो", "").replace("सर्च", "").replace("करो", "")
        do_search(q.strip())
        return

    # Fallback
    do_search(t)


# ===========================
#  LISTEN
# ===========================
def listen():
    rec = vosk.KaldiRecognizer(model, 16000)

    try:
        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=callback
        ):
            print("\n🎤 बोलिए...")

            while True:
                data = audio_q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    txt = result.get("text", "")
                    if txt:
                        print("आपने कहा:", txt)
                        return txt

    except Exception:
        return input("Type command > ")


# ===========================
#  MAIN
# ===========================
def main():
    speak("सहायक तैयार है।")

    while True:
        txt = listen()
        if not txt:
            continue
        if handle(txt) == "exit":
            break


if __name__ == "__main__":
    main()