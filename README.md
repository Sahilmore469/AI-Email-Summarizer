# 📧 AI Email Summarizer

A production-grade full-stack application that fetches your real emails via **Nylas API** and summarizes them using **Groq's LLaMA 3.1** model — with a beautiful dark Streamlit UI.

---

## 🏗 Architecture

```
email-summarizer-project/
├── server.js          # Express backend — main API
├── nylasClient.js     # Nylas email fetching module
├── groqClient.js      # Groq AI summarization module
├── app.py             # Streamlit frontend (dark UI)
├── package.json       # Node dependencies
├── requirements.txt   # Python dependencies
└── .env               # Your API keys (never commit this!)
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
# Install Node dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `.env` and fill in your credentials:

```env
NYLAS_API_KEY=your_nylas_api_key_here
NYLAS_API_URI=https://api.us.nylas.com
NYLAS_USER_GRANT_ID=your_nylas_grant_id_here
GROQ_API_KEY=your_groq_api_key_here
PORT=3000
```

**Get your keys:**
- Nylas: https://dashboard.nylas.com/ → Create an app → Connect an email account → copy Grant ID
- Groq: https://console.groq.com/ → API Keys → Create new key

### 3. Start the Backend

```bash
node server.js
# or for auto-reload during development:
npx nodemon server.js
```

You should see:
```
🚀 AI Email Summarizer backend running on http://127.0.0.1:3000
```

### 4. Start the Frontend

In a **new terminal**:

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🎯 How to Use

1. Open the Streamlit app in your browser
2. Use the **sidebar slider** to choose 1–10 emails
3. Click **"🚀 Fetch & Summarize"**
4. Watch your emails appear with full AI summaries!

---

## 📡 API Reference

### `GET /emails?limit=5`

Fetches and summarizes the specified number of emails.

**Response (success):**
```json
{
  "success": true,
  "count": 5,
  "emails": [
    {
      "id": "email_id",
      "from": "Sender Name <sender@example.com>",
      "subject": "Email subject line",
      "date": "2/20/2026, 9:30:00 AM",
      "summary": "Summary:\n...\n\nKey Points:\n- ...\n\nAction Required:\n...\n\nDeadline:\n..."
    }
  ]
}
```

**Response (error):**
```json
{
  "success": false,
  "error": "Human-readable error message"
}
```

---

## 🛡 Error Handling

The system gracefully handles:
- ❌ Missing/invalid API keys → clear error messages
- ⏱️ Groq rate limits → automatic retry with backoff
- 📦 Token overflow → body trimmed to 1000 chars before sending
- 🌐 Network failures → descriptive error returned to frontend
- 📭 Empty inbox → friendly "no emails" message
- 🔌 Backend offline → Streamlit shows connection guide

---

## 🤖 AI Summary Format

Each email is summarized in this structured format:

```
Summary:
2-3 line overview of the email content.

Key Points:
- First key point
- Second key point
- Third key point

Action Required:
Description of any required action, or "None"

Deadline:
Any mentioned deadlines, or "None"
```

---

## ⚡ Performance Notes

- Email bodies are **trimmed to 1000 characters** before AI processing
- Summarization is **sequential** (not parallel) to respect Groq rate limits
- Groq rate limit errors trigger **automatic retry** (up to 2x with backoff)
- Model used: `llama-3.1-8b-instant` — fast and efficient

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Node.js + Express |
| Email API | Nylas v7 SDK |
| AI Model | Groq — LLaMA 3.1 8B Instant |
| Frontend | Python + Streamlit |
| Styling | Custom CSS (dark theme) |
