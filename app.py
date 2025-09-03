import os
import requests
import logging
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import json
import re

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# Initialize Flask application
# -----------------------------
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")  # fallback

# -----------------------------
# Configure logging
# -----------------------------
logging.basicConfig(level=logging.INFO)

# -----------------------------
# API Keys
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
METEOSOURCE_API_KEY = os.getenv("METEOSOURCE_API_KEY")

# -----------------------------
# In-memory chat history
# -----------------------------
chat_histories = {}

# -----------------------------
# Use chat-capable Groq model
# -----------------------------
DEFAULT_MODEL = "llama-3.3-70b-versatile"  # updated to supported model
AVAILABLE_GROQ_MODELS = [DEFAULT_MODEL]
logging.info(f"Using default Groq model: {DEFAULT_MODEL}")

# -----------------------------
# Core Groq query function
# -----------------------------
def query_groq(prompt, user_id="default", temperature=0.7, model=None, max_tokens=512):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    model_to_use = model or DEFAULT_MODEL
    history = chat_histories.get(user_id, {}).get("messages", [])

    system_message = {
        "role": "system",
        "content": (
            "You are Nexus Chatbot, a friendly and helpful AI assistant. "
            "Introduce yourself as Nexus Chatbot if asked. "
            "You can provide the latest international news, "
            "real-time weather forecasts for cities worldwide, "
            "and support voice input via microphone."
        )
    }

    messages = [system_message] + history + [{"role": "user", "content": prompt}]

    data = {
        "model": model_to_use,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        res = requests.post(url, headers=headers, json=data, timeout=30)
        res.raise_for_status()
        result = res.json()
        reply = result["choices"][0]["message"]["content"].strip()

        # Initialize user chat history if not present
        if user_id not in chat_histories:
            chat_histories[user_id] = {"messages": []}

        # Save conversation
        chat_histories[user_id]["messages"].append({"role": "user", "content": prompt})
        chat_histories[user_id]["messages"].append({"role": "assistant", "content": reply})

        # Keep only the last 6 messages
        if len(chat_histories[user_id]["messages"]) > 6:
            chat_histories[user_id]["messages"] = chat_histories[user_id]["messages"][-6:]

        return reply

    except requests.exceptions.HTTPError as e:
        try:
            return f"⚠️ Groq API error: {res.json().get('error', {}).get('message', str(e))}"
        except Exception:
            return f"⚠️ Groq API error: {e}"
    except Exception as e:
        logging.error(f"Groq API error: {e}")
        return "⚠️ Error: Unable to connect to AI service."

# -----------------------------
# User request processing
# -----------------------------
def process_user_request(command):
    prompt = f"""
    Analyze the user request: "{command}".
    Decide intent: news, weather, or general.
    Extract parameters:
    - For news: full country name and 2-letter ISO code (e.g., "Pakistan" -> "pk")
      Handle abbreviations like US -> United States, UK -> United Kingdom, UAE -> United Arab Emirates
    - For weather: city name (e.g., "Islamabad")
    Correct any typos.
    Respond ONLY with strict JSON, like:
    {{"intent": "news", "parameters": {{"country_name": "United States", "country_code": "us"}}}}
    or
    {{"intent": "weather", "parameters": {{"city": "Islamabad"}}}}
    or
    {{"intent": "general"}} 
    """
    reply = query_groq(prompt, user_id="intent", temperature=0, max_tokens=300)
    logging.info(f"Groq processed request (raw): {reply}")

    try:
        json_start = reply.find("{")
        json_end = reply.rfind("}") + 1
        json_str = reply[json_start:json_end]
        return json.loads(json_str)
    except Exception as e:
        logging.error(f"Failed to parse JSON from Groq: {e}")
        return {"intent": "general"}

# -----------------------------
# News & Weather fetchers
# -----------------------------
def get_news(params):
    if not NEWS_API_KEY:
        return "⚠️ News service not configured."
    try:
        country_code = params.get("country_code", "us")
        country_name = params.get("country_name", "United States")
        url = f"https://newsapi.org/v2/top-headlines?country={country_code}&pageSize=5&apiKey={NEWS_API_KEY}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        articles = r.json().get("articles", [])[:5]
        if not articles:
            return f"⚠️ No news found for '{country_name}'."
        return "<br>".join([f"📰 {a['title']} ({a['source']['name']})" for a in articles])
    except Exception as e:
        logging.error(f"News API error: {e}")
        return "⚠️ Failed to fetch news."

def get_weather(city="Islamabad"):
    if not METEOSOURCE_API_KEY:
        return "⚠️ Weather service not configured."
    try:
        geo_url = f"https://www.meteosource.com/api/v1/free/find_places?text={city}&key={METEOSOURCE_API_KEY}"
        geo_res = requests.get(geo_url, timeout=10)
        geo_res.raise_for_status()
        places = geo_res.json()
        if not places:
            return f"⚠️ City not found: {city}"
        place_id = places[0]["place_id"]

        url = f"https://www.meteosource.com/api/v1/free/point?place_id={place_id}&sections=current&key={METEOSOURCE_API_KEY}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        current = data.get("current", {})
        temp = current.get("temperature")
        desc = current.get("summary", "No description")
        if temp is None:
            return f"⚠️ Could not fetch weather for '{city}'."
        return f"🌤 Weather in {city.title()}: {temp}°C, {desc}"
    except Exception as e:
        logging.error(f"Meteosource API error: {e}")
        return "⚠️ Failed to fetch weather."

# -----------------------------
# Helper functions
# -----------------------------
def make_clickable_links(text):
    url_pattern = re.compile(r'https?://\S+')
    return url_pattern.sub(lambda m: f'<a href="{m.group(0)}" target="_blank">{m.group(0)}</a>', text)

def handle_command(command, user_id="default"):
    processed = process_user_request(command)
    intent = processed.get("intent", "general")
    params = processed.get("parameters", {})

    if intent == "news":
        if not params.get("country_code"):
            params = {"country_name": "United States", "country_code": "us"}
        response = get_news(params)
    elif intent == "weather":
        city = params.get("city", "Islamabad")
        response = get_weather(city)
    else:
        response = query_groq(command, user_id)

    return make_clickable_links(response)

# -----------------------------
# Flask routes
# -----------------------------
@app.route("/")
def home():
    if "user_id" not in session:
        session["user_id"] = os.urandom(8).hex()
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    user_id = session.get("user_id", "default")
    logging.info(f"User[{user_id}]: {user_msg}")
    bot_response = handle_command(user_msg, user_id)
    logging.info(f"Nexus: {bot_response}")
    return jsonify({"response": bot_response})

@app.route("/models", methods=["GET"])
def list_models():
    return jsonify({"available_models": AVAILABLE_GROQ_MODELS, "default_model": DEFAULT_MODEL})

# -----------------------------
# Run Flask server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
