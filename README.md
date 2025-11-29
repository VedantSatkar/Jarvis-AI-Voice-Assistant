# 🤖 Jarvis AI Voice Assistant

A fully functional **Python-based Voice Assistant** capable of listening to user commands, performing system tasks, searching the internet, opening applications, and responding with natural speech.
Ideal for automation, productivity, and AI experimentation.


## 🚀 Features

* 🎙️ **Real-time voice command recognition**
* 🔊 **Text-to-speech responses** using pyttsx3
* 🌐 **Opens websites** (YouTube, Google, etc.)
* 🖥️ **Launches apps** (Calculator, Notepad, etc.)
* 🕒 **Tells time & date**
* 🧠 **Custom commands support**
* 🗂️ Lightweight, fast, and beginner-friendly
* 🛠️ Easy to modify & extend

---

## 🖼️ Output Screenshot

> Replace this image with your actual screenshot.
> Make a folder named **assets** → place your screenshot → rename it to **output.png**

```markdown
<p align="center">
  <img src="assets/output.png" alt="Jarvis AI Voice Assistant Screenshot" width="700">
</p>
```

---

## 🛠️ Tech Stack

* **Programming Language:** Python
* **Speech Recognition:** SpeechRecognition
* **Voice Output:** pyttsx3
* **Audio Input:** PyAudio
* **Utilities:** datetime, webbrowser, os

---

## 📦 Installation & Setup

Follow these steps to run Jarvis on your system:

### 1. Clone the Repository

```bash
git clone https://github.com/VedantSatkar/Jarvis-AI-Voice-Assistant.git
cd Jarvis-AI-Voice-Assistant
```

### 2. Install Dependencies

If you have `requirements.txt`:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install speechrecognition pyttsx3 pyaudio
```

---

## ▶️ Usage

Run the assistant:

```bash
python jarvis.py
```

Then speak:

* “Open YouTube”
* “What’s the time?”
* “Search Python tutorial”
* “Open Notepad”
* “Exit”

---

## 📁 Project Structure

```
Jarvis-AI-Voice-Assistant/
│
├── jarvis.py
├── README.md
├── requirements.txt  (optional)
└── assets/
      └── output.png  (screenshot)
```

---

## 💡 Add Your Own Commands

You can extend Jarvis easily.
Example inside `jarvis.py`:

```python
if "open calculator" in command:
    os.system("calc.exe")
```

Add as many commands as you want.

---

## 🤝 Contributing

Contributions are welcome!
Feel free to:

1. **Fork** the repo
2. Add features / fix bugs
3. **Submit a pull request**

---

## 📬 Contact

**Developer:** Vedant Satkar
📧 Email: *add your email here*
🔗 GitHub: [https://github.com/VedantSatkar](https://github.com/VedantSatkar)
📱 LinkedIn: *your link here*

---

## 📜 License

This project is licensed under the **MIT License**.
You may use, modify, and distribute it freely.