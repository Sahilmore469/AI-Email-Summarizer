import streamlit as st
import requests
import os
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Email Summarizer",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Dark Professional Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Base dark theme */
    .stApp {
        background-color: #0f1117;
        color: #e8eaf0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161b27;
        border-right: 1px solid #2a2f3e;
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #a78bfa;
    }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%);
        border: 1px solid #4338ca;
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        font-size: 2.4rem;
        font-weight: 800;
        color: #fff;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #a5b4fc;
        font-size: 1.05rem;
        margin: 0;
    }

    /* Metric cards */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        flex: 1;
        background: #161b27;
        border: 1px solid #2a2f3e;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    }
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #818cf8;
    }
    .metric-card .metric-label {
        font-size: 0.8rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.25rem;
    }

    /* Email cards */
    .email-card {
        background: #161b27;
        border: 1px solid #2a2f3e;
        border-radius: 16px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.5rem;
        transition: border-color 0.2s;
    }
    .email-card:hover {
        border-color: #4338ca;
    }
    .email-number {
        display: inline-block;
        background: #312e81;
        color: #a5b4fc;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.2rem 0.7rem;
        border-radius: 999px;
        margin-bottom: 0.8rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .email-subject {
        font-size: 1.2rem;
        font-weight: 700;
        color: #e8eaf0;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    .email-meta {
        display: flex;
        gap: 1.5rem;
        flex-wrap: wrap;
        margin-bottom: 1.2rem;
    }
    .email-meta span {
        font-size: 0.85rem;
        color: #6b7280;
    }
    .email-meta span strong {
        color: #9ca3af;
    }
    .divider {
        border: none;
        border-top: 1px solid #2a2f3e;
        margin: 1.2rem 0;
    }
    .summary-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.78rem;
        font-weight: 700;
        color: #818cf8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
    }
    .summary-label::before {
        content: "✦";
    }
    .summary-text {
        color: #cbd5e1;
        font-size: 0.95rem;
        line-height: 1.75;
        white-space: pre-wrap;
        font-family: 'Inter', sans-serif;
    }

    /* Error box */
    .error-card {
        background: #1f0b0b;
        border: 1px solid #7f1d1d;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        color: #fca5a5;
        font-size: 0.95rem;
    }
    .error-card h3 { color: #f87171; margin-top: 0; }

    /* Info box */
    .info-card {
        background: #0c1a2e;
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        color: #93c5fd;
        font-size: 0.95rem;
        text-align: center;
    }

    /* Button override */
    .stButton > button {
        background: linear-gradient(135deg, #4338ca, #7c3aed);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        width: 100%;
        cursor: pointer;
        transition: opacity 0.2s;
    }
    .stButton > button:hover {
        opacity: 0.9;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# BACKEND URL — reads from Streamlit secrets or env
# ─────────────────────────────────────────────
BACKEND_URL = (
    st.secrets.get("BACKEND_URL", None)
    or os.environ.get("BACKEND_URL", "http://127.0.0.1:3000")
)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")

    limit = st.slider(
        "Number of Emails to Summarize",
        min_value=1,
        max_value=10,
        value=3,
        step=1,
        help="Select how many recent emails to fetch and summarize",
    )

    st.markdown(f"""
    <div style="background:#0d1117;border:1px solid #2a2f3e;border-radius:10px;padding:1rem;margin-top:1rem;">
        <p style="color:#6b7280;font-size:0.8rem;margin:0 0 0.5rem 0;text-transform:uppercase;letter-spacing:1px;">SELECTED</p>
        <p style="color:#818cf8;font-size:2rem;font-weight:800;margin:0;">{limit}</p>
        <p style="color:#4b5563;font-size:0.85rem;margin:0;">email{"s" if limit != 1 else ""}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔌 Backend Status")

    try:
        health = requests.get(f"{BACKEND_URL}/", timeout=5)
        if health.status_code == 200:
            st.success("✅ Backend Connected")
        else:
            st.error("❌ Backend Error")
    except Exception:
        st.error("❌ Backend Offline")
        st.markdown("""
        <small style="color:#6b7280;">
        Backend may be sleeping (free Render tier).<br>
        Wait 30s and refresh the page.
        </small>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="color:#4b5563;font-size:0.8rem;text-align:center;">
        <p>Powered by</p>
        <p><strong style="color:#6b7280;">Nylas</strong> · <strong style="color:#6b7280;">Groq</strong> · <strong style="color:#6b7280;">LLaMA 3.1</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>📧 AI Email Summarizer</h1>
    <p>Instantly fetch and summarize your emails using LLaMA 3.1 · Powered by Nylas + Groq</p>
</div>
""", unsafe_allow_html=True)

fetch_col, _ = st.columns([1, 2])
with fetch_col:
    fetch_clicked = st.button(f"🚀 Fetch & Summarize {limit} Email{'s' if limit != 1 else ''}")

# ─────────────────────────────────────────────
# FETCH LOGIC
# ─────────────────────────────────────────────
if fetch_clicked:
    with st.spinner(f"🔄 Fetching {limit} email{'s' if limit != 1 else ''} and generating AI summaries..."):
        try:
            response = requests.get(
                f"{BACKEND_URL}/emails",
                params={"limit": limit},
                timeout=120,
            )
            data = response.json()

        except requests.exceptions.ConnectionError:
            st.markdown(f"""
            <div class="error-card">
                <h3>🔌 Backend Not Reachable</h3>
                <p>Could not connect to <code>{BACKEND_URL}</code>.</p>
                <p>If using Render free tier, the backend may be sleeping — wait 30 seconds and try again.</p>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        except requests.exceptions.Timeout:
            st.markdown("""
            <div class="error-card">
                <h3>⏱️ Request Timeout</h3>
                <p>The backend took too long to respond. This may happen when summarizing many emails. Try reducing the count or check Groq API status.</p>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        except Exception as e:
            st.markdown(f"""
            <div class="error-card">
                <h3>⚠️ Unexpected Error</h3>
                <p>{str(e)}</p>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

    # ─── Handle API errors ───
    if not data.get("success"):
        error_msg = data.get("error", "Unknown error from backend.")
        st.markdown(f"""
        <div class="error-card">
            <h3>❌ API Error</h3>
            <p>{error_msg}</p>
            <hr style="border-color:#7f1d1d;">
            <p style="font-size:0.85rem;color:#9ca3af;">
                Common fixes:<br>
                • Check your Render environment variables are set<br>
                • Verify NYLAS_USER_GRANT_ID is correct<br>
                • Ensure GROQ_API_KEY is active
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    emails = data.get("emails", [])
    count = data.get("count", 0)

    # ─── No emails ───
    if count == 0:
        st.markdown("""
        <div class="info-card">
            <h3>📭 No Emails Found</h3>
            <p>Your inbox appears to be empty or no emails were returned by Nylas.</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # ─── Metric cards ───
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-value">{count}</div>
            <div class="metric-label">Emails Fetched</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{count}</div>
            <div class="metric-label">AI Summaries</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">LLaMA 3.1</div>
            <div class="metric-label">AI Model</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{datetime.now().strftime("%H:%M")}</div>
            <div class="metric-label">Last Updated</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### 📋 Results — {count} Email{'s' if count != 1 else ''} Summarized")
    st.markdown("---")

    # ─── Email cards ───
    for i, email in enumerate(emails, 1):
        subject = email.get("subject", "(No subject)")
        from_addr = email.get("from", "Unknown")
        date_str = email.get("date", "Unknown")
        summary = email.get("summary", "(No summary available)")

        st.markdown(f"""
        <div class="email-card">
            <div class="email-number">Email {i} of {count}</div>
            <div class="email-subject">📨 {subject}</div>
            <div class="email-meta">
                <span>👤 <strong>From:</strong> {from_addr}</span>
                <span>📅 <strong>Date:</strong> {date_str}</span>
            </div>
            <hr class="divider">
            <div class="summary-label">AI Summary</div>
            <div class="summary-text">{summary}</div>
        </div>
        """, unsafe_allow_html=True)

else:
    # ─── Default state ───
    st.markdown("""
    <div class="info-card">
        <div style="font-size:3rem;margin-bottom:1rem;">📬</div>
        <h3 style="color:#93c5fd;margin:0 0 0.5rem 0;">Ready to Summarize</h3>
        <p style="color:#6b7280;margin:0;">
            Use the sidebar to select how many emails you want,<br>
            then click the <strong style="color:#818cf8;">Fetch & Summarize</strong> button above.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    features = [
        ("🔌", "Nylas API", "Securely connects to your real inbox"),
        ("🤖", "Groq + LLaMA 3.1", "Blazing-fast AI summarization"),
        ("📊", "Structured Output", "Summary, key points, actions & deadlines"),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3], features):
        with col:
            st.markdown(f"""
            <div style="background:#161b27;border:1px solid #2a2f3e;border-radius:12px;padding:1.5rem;text-align:center;">
                <div style="font-size:2rem;">{icon}</div>
                <div style="font-weight:700;color:#e8eaf0;margin:0.5rem 0 0.3rem;">{title}</div>
                <div style="color:#6b7280;font-size:0.85rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
