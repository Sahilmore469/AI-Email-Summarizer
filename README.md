# 📧 AI Email Summarizer

> Instantly fetch and summarize your emails using **LLaMA 3.1** · Powered by **Nylas + Groq + Node.js + Streamlit**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat&logo=node.js&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.1-F55036?style=flat)
![Nylas](https://img.shields.io/badge/Nylas-Email%20API-5C5BD4?style=flat)
![Render](https://img.shields.io/badge/Backend-Render-46E3B7?style=flat&logo=render&logoColor=white)
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

## 🌐 Live Demo

| Layer | Platform | URL |
|-------|----------|-----|
| 🖥️ Frontend | Streamlit Community Cloud | *(your streamlit app URL)* |
| ⚙️ Backend | Render | *(your render app URL)* |

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
User → Streamlit UI → GET /emails?limit=N → server.js (Render)
    → nylasClient.js → Nylas API → Gmail
    → groqClient.js  → Groq API  → LLaMA 3.1
    → JSON response  → Email cards displayed
```

---

## 🚀 Quick Start (Local)

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

## ☁️ Deployment

The app is deployed with **Render** for the backend and **Streamlit Community Cloud** for the frontend.

### Backend → [Render](https://render.com)

1. Push your code to GitHub (`.env` is gitignored — your keys are safe)
2. Go to [render.com](https://render.com) → **New** → **Web Service**
3. Connect your GitHub repository
4. Configure the service:

   | Setting | Value |
   |---------|-------|
   | **Environment** | `Node` |
   | **Build Command** | `npm install` |
   | **Start Command** | `node server.js` |
   | **Region** | Your preferred region |

5. Go to **Environment** tab → add all your environment variables:

   ```
   NYLAS_API_KEY=your_nylas_api_key_here
   NYLAS_API_URI=https://api.us.nylas.com
   NYLAS_USER_GRANT_ID=your_nylas_grant_id_here
   GROQ_API_KEY=your_groq_api_key_here
   PORT=10000
   ```

   > ⚠️ **Set `PORT=10000`** on Render. Render internally routes traffic through port 10000; using `3000` will cause the health check to fail.

6. Click **Create Web Service** — Render will build and deploy automatically
7. Your backend URL will look like: `https://your-app-name.onrender.com`

> 💡 **Free tier note:** Render's free plan spins down after 15 minutes of inactivity. The first request after idle may take ~30 seconds to respond. Upgrade to a paid plan or use Render's cron to keep it warm if needed.

---

### Frontend → [Streamlit Community Cloud](https://share.streamlit.io)

1. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
2. Connect your GitHub account and select your repository
3. Set the **Main file path** to `app.py` and branch to `main`
4. Click **Advanced settings** → add the following secret:

   ```toml
   BACKEND_URL = "https://your-app-name.onrender.com"
   ```

5. Click **Deploy** — your frontend will be live in under a minute

> ✅ The `BACKEND_URL` secret tells the Streamlit app where to find your Render backend. Make sure it matches exactly (no trailing slash).

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
| Backend offline / cold start | Streamlit shows connection guide |
| Empty/invalid response | Streamlit shows diagnostic error card |
| Port already in use | Server prints exact kill command |

---

## 📁 Environment Variables Reference

| Variable | Required | Where to Set | Description |
|----------|----------|-------------|-------------|
| `NYLAS_API_KEY` | ✅ | Render env vars | Nylas application API key |
| `NYLAS_API_URI` | ✅ | Render env vars | Use `https://api.us.nylas.com` |
| `NYLAS_USER_GRANT_ID` | ✅ | Render env vars | Grant ID of connected email account |
| `GROQ_API_KEY` | ✅ | Render env vars | Groq API key for LLaMA access |
| `PORT` | ✅ on Render | Render env vars | Set to `10000` on Render |
| `BACKEND_URL` | ✅ on Cloud | Streamlit secrets | Your Render backend URL |

---

## 🔧 Troubleshooting

**Sidebar shows `Backend Error` on Streamlit Cloud**

Your Render service may be cold-starting (free tier spins down after inactivity). Wait ~30 seconds and try again. Check that `BACKEND_URL` in Streamlit secrets exactly matches your Render URL.

**Render deploy fails / health check fails**

Make sure `PORT=10000` is set in your Render environment variables. Render requires this specific port on free and starter plans.

**`EADDRINUSE: address already in use :::3000`** (local only)

A previous server instance is still running. Kill it:

```bash
# macOS / Linux
lsof -ti:3000 | xargs kill -9

# Windows (PowerShell)
for /f "tokens=5" %a in ('netstat -ano ^| findstr :3000') do taskkill /PID %a /F
```

**`Expecting value: line 1 column 1 (char 0)`**

The backend returned an empty response. Check your Render service logs for errors. Most common cause: missing environment variables.

**No emails returned**

Your `NYLAS_USER_GRANT_ID` may be wrong. Check your Nylas Dashboard → Connected Accounts.

---

## ⚡ Performance Notes

- Email bodies trimmed to **1,000 characters** before AI processing
- Summarization runs **sequentially** to respect Groq rate limits
- Groq rate limit errors trigger **automatic retry with backoff**
- Model: `llama-3.1-8b-instant` — fast, free tier available
- Render free tier has a **cold start delay** (~30s after inactivity)

---

## 🧰 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Python + Streamlit | Dark UI, controls, email cards |
| Frontend Hosting | Streamlit Community Cloud | Free frontend deployment |
| Backend | Node.js + Express | REST API, orchestration |
| Backend Hosting | Render | Free backend deployment |
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

## 👤 Authors

Built by **Sahil More** and **Ayush Shukla**

If you found this useful, give it a ⭐ on GitHub!

---

<div align="center">
  <sub>Built with Node.js · Streamlit · Nylas · Groq · LLaMA 3.1 · Deployed on Render + Streamlit Cloud</sub>
</div>
