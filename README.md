# 📧 AI Email Summarizer

> Instantly fetch and summarize your emails using **LLaMA 3.1** · Powered by **Nylas + Groq + Node.js + Streamlit**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat&logo=node.js&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.1-F55036?style=flat)
![Nylas](https://img.shields.io/badge/Nylas-Email%20API-5C5BD4?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## ✨ What It Does

A full-stack AI-powered email summarizer that:

- 🔌 Connects to your **real Gmail / email inbox** via Nylas API
- 📬 Fetches **1–10 emails** based on your selection
- 🤖 Summarizes each email using **Groq's LLaMA 3.1 8B Instant** model
- 📊 Displays **structured summaries** — overview, key points, action items & deadlines
- 🎨 Beautiful **dark-themed Streamlit UI** with live backend status

---

## 🏗️ Architecture

```
email-summarizer/
│
├── 📄 server.js          # Express backend — GET /emails?limit=N
├── 📄 nylasClient.js     # Nylas SDK — fetches real emails
├── 📄 groqClient.js      # Groq SDK — LLaMA 3.1 summarization
├── 📄 app.py             # Streamlit frontend — dark UI
│
├── 📄 package.json       # Node.js dependencies
├── 📄 requirements.txt   # Python dependencies
├── 📄 .env               # 🔒 API keys (never commit this!)
├── 📄 .gitignore         # Protects secrets
└── 📁 .streamlit/
    └── config.toml       # Dark theme config
```

**Data Flow:**
```
User → Streamlit UI → GET /emails?limit=N → server.js
    → nylasClient.js → Nylas API → Gmail
    → groqClient.js  → Groq API  → LLaMA 3.1
    → JSON response  → Email cards displayed
```

---

## 🚀 Quick Start

### Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| Python | 3.9+ | [python.org](https://python.org) |
| npm | 8+ | Included with Node.js |

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/email-summarizer.git
cd email-summarizer
```

### 2. Get Your API Keys

| Key | Where to Get It |
|-----|----------------|
| `NYLAS_API_KEY` | [dashboard.nylas.com](https://dashboard.nylas.com) → Create App |
| `NYLAS_USER_GRANT_ID` | Nylas Dashboard → Connect your Gmail → copy Grant ID |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) → API Keys → Create |

### 3. Configure Environment

Create a `.env` file in the root directory:

```env
NYLAS_API_KEY=your_nylas_api_key_here
NYLAS_API_URI=https://api.us.nylas.com
NYLAS_USER_GRANT_ID=your_nylas_grant_id_here
GROQ_API_KEY=your_groq_api_key_here
PORT=3000
```

> ⚠️ **Never commit your `.env` file.** It is already included in `.gitignore`.

### 4. Install Dependencies

```bash
# Node.js backend
npm install

# Python frontend
pip install -r requirements.txt
```

### 5. Run the App

Open **two terminals** at the same time.

**Terminal 1 — Backend:**
```bash
node server.js
```
```
✅ All environment variables loaded successfully.
🚀 AI Email Summarizer backend running on http://127.0.0.1:3000
```

**Terminal 2 — Frontend:**
```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 🎯 How to Use

1. Use the **sidebar slider** to select how many emails to summarize (1–10)
2. Confirm the sidebar shows **✅ Backend Connected**
3. Click **🚀 Fetch & Summarize**
4. View AI-generated summaries for each email instantly

---

## 📡 API Reference

### `GET /emails?limit=N`

Fetches and summarizes N recent emails from your inbox.

**Success Response:**
```json
{
  "success": true,
  "count": 5,
  "emails": [
    {
      "id": "msg_abc123",
      "from": "Sender Name <sender@example.com>",
      "subject": "Project Update",
      "date": "4/11/2026, 9:30:00 AM",
      "summary": "Summary:\nThe email discusses...\n\nKey Points:\n- Point 1\n\nAction Required:\nReply by Friday\n\nDeadline:\nFriday April 14"
    }
  ]
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Human-readable error message"
}
```

---

## 🤖 AI Summary Format

Every email is summarized in this structured format:

```
Summary:
2–3 line overview of the email.

Key Points:
- First key point
- Second key point
- Third key point

Action Required:
What you need to do, or "None"

Deadline:
Any mentioned dates, or "None"
```

---

## 🛡️ Error Handling

| Scenario | Behavior |
|----------|----------|
| Missing `.env` keys | Warning on startup + descriptive API error |
| Nylas 401 (invalid key) | Returns clear authentication error |
| Nylas 404 (bad grant ID) | Returns grant ID guidance message |
| Groq rate limit (429) | Auto-retries up to 2× with delay |
| Token overflow | Email body pre-trimmed to 1000 chars |
| Backend offline | Streamlit shows connection guide |
| Empty/invalid response | Streamlit shows diagnostic error card |
| Port already in use | Server prints exact kill command |

---

## ☁️ Deployment

### Backend → [Railway](https://railway.app) (free)

1. Push code to GitHub — `.env` is gitignored, your keys are safe
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub**
3. Select your repo → **Deploy Now**
4. Go to **Settings → Networking → Generate Domain**  
   You'll get a URL like: `https://your-app.up.railway.app`
5. Go to **Variables** tab → add all 4 keys from your `.env`

### Frontend → [Streamlit Community Cloud](https://share.streamlit.io) (free)

1. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
2. Set Repository, Branch (`main`), and Main file (`app.py`)
3. Click **Advanced settings** → add this secret:
   ```toml
   BACKEND_URL = "https://your-app.up.railway.app"
   ```
4. Click **Deploy**

---

## 🔧 Troubleshooting

**`EADDRINUSE: address already in use :::3000`**

A previous server instance is still running. Kill it:

```bash
# Windows (PowerShell)
for /f "tokens=5" %a in ('netstat -ano ^| findstr :3000') do taskkill /PID %a /F

# macOS / Linux
lsof -ti:3000 | xargs kill -9
```

**`Expecting value: line 1 column 1 (char 0)`**

The backend returned an empty response — it crashed before responding. Check the terminal running `node server.js` for the stack trace. Most common cause: missing or empty `.env` file.

**Sidebar shows `Backend Error`**

Node.js server is not running. Open a new terminal and run `node server.js`.

**No emails returned**

Your `NYLAS_USER_GRANT_ID` may be wrong. Check your Nylas Dashboard → Connected Accounts.

---

## 📁 Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `NYLAS_API_KEY` | ✅ | Nylas application API key |
| `NYLAS_API_URI` | ✅ | Use `https://api.us.nylas.com` |
| `NYLAS_USER_GRANT_ID` | ✅ | Grant ID of connected email account |
| `GROQ_API_KEY` | ✅ | Groq API key for LLaMA access |
| `PORT` | ❌ Optional | Backend port (default: `3000`) |
| `BACKEND_URL` | ❌ Cloud only | Railway URL for Streamlit Cloud deployment |

---

## ⚡ Performance Notes

- Email bodies trimmed to **1,000 characters** before AI processing
- Summarization runs **sequentially** to respect Groq rate limits
- Groq rate limit errors trigger **automatic retry with backoff**
- Model: `llama-3.1-8b-instant` — fast, free tier available

---

## 🧰 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Python + Streamlit | Dark UI, controls, email cards |
| Backend | Node.js + Express | REST API, orchestration |
| Email API | Nylas v7 SDK | Gmail / inbox access |
| AI Model | Groq — LLaMA 3.1 8B Instant | Email summarization |
| Config | dotenv | Environment variable management |

---

## 🤝 Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

Built by **Sahil More**

If you found this useful, give it a ⭐ on GitHub!

---

<div align="center">
  <sub>Built with Node.js · Streamlit · Nylas · Groq · LLaMA 3.1</sub>
</div>
