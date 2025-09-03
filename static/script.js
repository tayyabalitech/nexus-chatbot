// =======================
// DOM ELEMENTS
// =======================
const messages = document.getElementById("messages");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");

// =======================
// USER SESSION HANDLING
// =======================
// Generate and persist a unique user_id in localStorage
if (!localStorage.getItem("user_id")) {
  localStorage.setItem(
    "user_id",
    "user_" + Math.random().toString(36).substr(2, 9)
  );
}
const user_id = localStorage.getItem("user_id");

// =======================
// INTRO SCREEN → CHAT UI
// =======================
const startBtn = document.getElementById("startBtn");
const introScreen = document.querySelector(".intro-screen");
const chatWrapper = document.querySelector(".chat-wrapper");

if (startBtn) {
  startBtn.addEventListener("click", () => {
    introScreen.classList.add("hidden");
    chatWrapper.classList.remove("hidden");
  });
}

// =======================
// MESSAGE APPENDING
// =======================
/**
 * Append a chat message to the UI.
 * @param {string} sender - "user" or "bot"
 * @param {string} text - Message text
 * @param {boolean} isTyping - Whether to show typing indicator
 * @returns {HTMLElement} - Message element
 */
function appendMessage(sender, text, isTyping = false) {
  const msgDiv = document.createElement("div");
  msgDiv.className = `msg ${sender}`;

  if (isTyping) {
    // Typing indicator for bot
    msgDiv.innerHTML = `
      <div class="sender">🤖 Nexus</div>
      <div class="bubble">
        <div class="typing-dots"><span></span><span></span><span></span></div>
      </div>
    `;
  } else {
    // Normal message (user or bot)
    msgDiv.innerHTML = `
      <div class="sender">${sender === "bot" ? "🤖 Nexus" : "🧑 You"}</div>
      <div class="bubble">${text}</div>
      <span class="time">${new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      })}</span>
    `;
  }

  messages.appendChild(msgDiv);
  messages.scrollTop = messages.scrollHeight; // Auto-scroll to bottom
  return msgDiv;
}

// =======================
// SENDING MESSAGES
// =======================
/**
 * Send user input to backend and display bot response.
 */
async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  // Show user message
  appendMessage("user", text);
  userInput.value = "";
  userInput.disabled = true;

  // Show bot typing indicator
  const loader = appendMessage("bot", "", true);

  try {
    // Send message to Flask backend
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, user_id: user_id }),
    });

    const data = await res.json();

    loader.remove(); // Remove typing indicator

    if (!data.response || data.response.toLowerCase().includes("error")) {
      appendMessage("bot", "⚠️ Something went wrong. Please try again.");
    } else {
      appendMessage("bot", data.response);
    }
  } catch {
    loader.remove();
    appendMessage("bot", "⚠️ Network error. Please try again.");
  }

  userInput.disabled = false;
  userInput.focus();
}

// =======================
// EVENT LISTENERS
// =======================
sendBtn.addEventListener("click", sendMessage);

// Allow Enter key to send (Shift+Enter for newline)
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// =======================
// VOICE INPUT (SpeechRecognition API)
// =======================
let isListening = false;
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = SpeechRecognition ? new SpeechRecognition() : null;

if (recognition) {
  recognition.lang = "en-US";
  recognition.continuous = false; // Stop after single phrase

  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    userInput.value = text;
    sendMessage();
  };

  recognition.onstart = () => micBtn.classList.add("listening");
  recognition.onend = () => {
    micBtn.classList.remove("listening");
    isListening = false;
  };

  micBtn.addEventListener("click", () => {
    if (!isListening) {
      recognition.start();
      isListening = true;
    } else {
      recognition.stop();
      isListening = false;
    }
  });
} else {
  // Hide mic button if SpeechRecognition not supported
  micBtn.style.display = "none";
}
