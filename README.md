# 🤖 Nexus Chatbot ✨

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-black.svg)](https://flask.palletsprojects.com/)
[![Groq](https://img.shields.io/badge/AI-Groq-blueviolet)](https://groq.com/)
[![Hosted](https://img.shields.io/badge/Live-Demo-brightgreen?logo=google-chrome)](https://nexuschatbot.pythonanywhere.com/)

---

## 📖 Project Description
Nexus Chatbot is an **AI-powered assistant** built with **Flask** and integrated with **Groq LLM models**. It provides:
- Real-time **chat** and intelligent responses.
- Up-to-date **international news** via News API.
- Accurate **weather forecasts** with Meteosource API.
- **Voice input support** powered by browser Speech Recognition API.

The project is fully deployed and live at: 🌐 [https://nexuschatbot.pythonanywhere.com/](https://nexuschatbot.pythonanywhere.com/)

---

## ✨ Features
- 🗣️ **Interactive Chat** – Smart AI-based Q&A.
- ☁️ **Weather Forecast** – Get real-time weather updates for any city.
- 📰 **News Updates** – Read top headlines from any country.
- 🎙️ **Voice Support** – Send messages using your microphone.
- 🔗 **Clickable Links** – Bot responses with URLs are auto-converted into clickable links.
- 🧠 **Context Memory** – Keeps recent conversation history for better responses.

---

## 📂 Directory Structure
```
Nexus-Chatbot/
│
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── .env                  # Environment configuration
├── templates/
│   └── index.html        # Frontend HTML
├── static/
│   ├── style.css         # Custom styles
│   └── script.js         # Chat UI logic
```

---

## ⚙️ Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/tayyabalitech/nexus-chatbot.git
   cd nexus-chatbot
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔑 Configuration
1. Copy `.env.example` and rename it to `.env`

   **Linux / macOS / Git Bash**
   ```bash
   cp .env.example .env
    ```

   **Windows**
   ```bash
   copy .env.example .env
   ```

2. Add your API keys in `.env`:
   ```ini
   NEWS_API_KEY=your_news_api_key
   GROQ_API_KEY=your_groq_api_key
   METEOSOURCE_API_KEY=your_meteosource_api_key
   ```

---

## 🚀 Usage
1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

3. Interact with **Nexus Chatbot**:
   - Type messages.
   - Use the 🎙️ microphone button for voice.
   - Ask for **weather**, **news**, or general queries.

---

## 🛠️ Technology Stack
- **Backend:** Python, Flask
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap, Font Awesome
- **APIs:**
  - Groq LLM API (AI Responses)
  - News API (Top Headlines)
  - Meteosource API (Weather Data)
- **Utilities:** Requests, python-dotenv

---

## 👨‍💻 Team Members
| Name                  | GitHub                                    | LinkedIn                         | Email                     |
|-----------------------|-------------------------------------------|----------------------------------|---------------------------|
| **Tayyab Ali**        | [tayyabalitech](https://github.com/tayyabalitech) | [tayyabalitech](https://linkedin.com/in/tayyabalitech) | tayyabalitechpro@gmail.com |
| **Muhammad Anas Mahmood** | [anasmahmoodprogrammer](https://github.com/anasmahmoodprogrammer) | [anasmahmoodprogrammer](https://linkedin.com/in/anasmahmoodprogrammer) | anasmahmood090@gmail.com |
| **Shahzaib**          | [shahzaib-nutech](https://github.com/shahzaib-nutech) | [shah-zaib-190238325](https://linkedin.com/in/shah-zaib-190238325) | shahzaiburmar@gmail.com |
| **Osama Bin Rafique** | – | – | osamarafiquef23@nutech.edu.pk |

---

## 🤝 Looking for Contributions  

💡 We warmly welcome contributions of all kinds to help make Nexus Chatbot even better! 🚀

---
