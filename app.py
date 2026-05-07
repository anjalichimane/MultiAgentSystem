import streamlit as st
import threading
import queue
import time
import requests as req

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

.stApp { background: #0a0a0f; color: #e8e8f0; }

[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid #1e1e3a;
}

.hero-title {
    font-size: 2.8rem; font-weight: 800;
    background: linear-gradient(135deg, #7c6af7 0%, #a78bfa 40%, #f472b6 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: -1px; line-height: 1.1; margin-bottom: 0.25rem;
}
.hero-sub {
    color: #6b7280; font-size: 1rem; font-weight: 400;
    font-family: 'JetBrains Mono', monospace; letter-spacing: 0.05em;
}

.card-title {
    font-size: 0.75rem; font-weight: 600; letter-spacing: 0.15em;
    text-transform: uppercase; color: #7c6af7; margin-bottom: 0.6rem;
    font-family: 'JetBrains Mono', monospace;
}

.step-badge {
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: #1a1a2e; border: 1px solid #2d2d5e; border-radius: 999px;
    padding: 0.35rem 0.9rem; font-size: 0.8rem;
    font-family: 'JetBrains Mono', monospace; color: #a78bfa; margin-bottom: 0.5rem;
}
.step-badge.done   { border-color: #4ade80; color: #4ade80; background: #0a2318; }
.step-badge.active { border-color: #f472b6; color: #f472b6; background: #2a0a18;
                     animation: pulse 1.4s ease-in-out infinite; }
@keyframes pulse { 0%,100%{ opacity:1; } 50%{ opacity:.55; } }

.score-pill {
    display: inline-block;
    background: linear-gradient(135deg,#7c6af7,#f472b6);
    color: #fff; font-weight: 700; font-size: 1.4rem;
    padding: 0.3rem 1.1rem; border-radius: 999px;
    font-family: 'JetBrains Mono', monospace; margin-bottom: 1rem;
}

.stTextInput > div > div > input, .stTextArea textarea {
    background: #111120 !important; border: 1px solid #2d2d5e !important;
    color: #e8e8f0 !important; border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
}
.stTextInput > div > div > input:focus, .stTextArea textarea:focus {
    border-color: #7c6af7 !important;
    box-shadow: 0 0 0 2px rgba(124,106,247,0.25) !important;
}

.stButton > button {
    background: linear-gradient(135deg,#7c6af7,#a78bfa) !important;
    color: #fff !important; border: none !important; border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important; font-weight: 600 !important;
    letter-spacing: 0.04em !important; padding: 0.55rem 1.6rem !important;
    transition: opacity .2s !important;
}
.stButton > button:hover { opacity: .85 !important; }

.report-body {
    font-size: 0.95rem; line-height: 1.75; color: #cbd5e1;
    white-space: pre-wrap; font-family: 'Syne', sans-serif;
}

hr { border-color: #1e1e3a !important; }

[data-testid="stExpander"] {
    background: #111120; border: 1px solid #1e1e3a; border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in {
    "result": None,
    "running": False,
    "steps_done": [],
    "current_step": "",
    "log_queue": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")

    st.markdown("**🌍 Backend URL**")
    st.caption("paste your url here")

    colab_url = st.text_input(
        "Backend URL",
        placeholder="https://xxxx-xx-xx.ngrok-free.app",
        label_visibility="collapsed",
        key="colab_url",
    )

    if colab_url.strip():
        base = colab_url.strip().rstrip("/")
        api_endpoint = base if base.endswith("/research") else base + "/research"
        with st.spinner("Checking connection..."):
            try:
                ping = req.get(base + "/", timeout=5)
                if ping.status_code == 200:
                    st.success("Backend connected ✅")
                else:
                    st.warning(f"Backend replied with status {ping.status_code}")
            except Exception:
                st.error("Cannot reach backend ❌ — is Colab running?")
        st.code(api_endpoint, language="text")
    else:
        api_endpoint = None
        st.warning("Paste your Colab ngrok URL above to connect.")

    st.markdown("---")
    st.markdown("""
**How to start backend**
1. Open `backend_colab.py` in Google Colab
2. Run the single cell
3. Copy the printed `API Endpoint` URL
4. Paste it above ☝️
""")
    st.markdown("---")
    st.markdown("""
**Stack**
- 🤖 `llama-3.3-70b` via Groq
- 🔍 Tavily web search
- 🌐 BeautifulSoup scraper
- ⚡ LangGraph ReAct agents
""")
    st.markdown("---")
    st.caption("Streamlit Cloud · Colab backend")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">AI Research Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">// powered by llama-3.3 · groq · tavily</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── Input row ─────────────────────────────────────────────────────────────────
col_in, col_btn = st.columns([5, 1], gap="small")
with col_in:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g.  Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
    )
with col_btn:
    run_btn = st.button(
        "🚀 Run",
        use_container_width=True,
        disabled=st.session_state.running or not api_endpoint,
    )

if run_btn and not api_endpoint:
    st.warning("⚠️ Paste your Colab ngrok URL in the sidebar first.")

# ── Step labels ───────────────────────────────────────────────────────────────
STEPS = [
    "🔍 Step 1 — Search agent is working ...",
    "📖 Step 2 — Reader agent is scraping top resources ...",
    "✍️  Step 3 — Writer is drafting the report ...",
    "🧐 Step 4 — Critic is reviewing the report ...",
]

# ── Background thread ─────────────────────────────────────────────────────────
def _run_pipeline(topic: str, api_endpoint: str, q: queue.Queue):
    # Simulate step progress while Colab processes
    step_delays = [3, 20, 40, 60]

    def _fake_steps():
        for i, delay in enumerate(step_delays):
            time.sleep(delay)
            q.put(("step", STEPS[i]))

    threading.Thread(target=_fake_steps, daemon=True).start()

    try:
        response = req.post(api_endpoint, json={"topic": topic}, timeout=300)
        response.raise_for_status()
        result = response.json()
        if "error" in result:
            q.put(("error", result["error"]))
        else:
            q.put(("done", result))

    except req.exceptions.ConnectionError:
        q.put(("error",
            "❌ Cannot connect to Colab backend.\n\n"
            "Make sure:\n"
            "• backend_colab.py is running in Colab\n"
            "• The ngrok URL is correct and not expired\n"
            "• You didn't close the Colab tab"
        ))
    except req.exceptions.Timeout:
        q.put(("error", "⏱️ Request timed out after 5 minutes. Try a simpler topic or restart Colab."))
    except req.exceptions.HTTPError as e:
        q.put(("error", f"Server error from Colab: {str(e)}"))
    except Exception as e:
        q.put(("error", str(e)))


# ── Trigger ───────────────────────────────────────────────────────────────────
if run_btn and topic.strip() and api_endpoint:
    st.session_state.result       = None
    st.session_state.steps_done   = []
    st.session_state.current_step = STEPS[0]
    st.session_state.running      = True
    q = queue.Queue()
    st.session_state.log_queue    = q
    threading.Thread(
        target=_run_pipeline,
        args=(topic.strip(), api_endpoint, q),
        daemon=True,
    ).start()

# ── Live progress ─────────────────────────────────────────────────────────────
if st.session_state.running:
    q = st.session_state.log_queue
    progress_ph = st.empty()

    while st.session_state.running:
        try:
            msg_type, payload = q.get(timeout=0.5)
        except queue.Empty:
            with progress_ph.container():
                st.markdown("#### ⏳ Pipeline Running on Colab ...")
                for s in STEPS:
                    if s in st.session_state.steps_done:
                        st.markdown(f'<div class="step-badge done">✓ {s}</div>', unsafe_allow_html=True)
                    elif s == st.session_state.current_step:
                        st.markdown(f'<div class="step-badge active">⟳ {s}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="step-badge">{s}</div>', unsafe_allow_html=True)
                st.caption("Usually takes 1–3 minutes depending on the topic.")
            time.sleep(0.5)
            st.rerun()
            continue

        if msg_type == "step":
            if st.session_state.current_step:
                st.session_state.steps_done.append(st.session_state.current_step)
            remaining = [s for s in STEPS if s not in st.session_state.steps_done]
            st.session_state.current_step = remaining[0] if remaining else ""

        elif msg_type == "done":
            st.session_state.steps_done   = STEPS.copy()
            st.session_state.current_step = ""
            st.session_state.result       = payload
            st.session_state.running      = False
            st.rerun()

        elif msg_type == "error":
            st.session_state.running = False
            st.error(payload)
            st.rerun()

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.result:
    res = st.session_state.result
    st.markdown("---")

    st.markdown("#### ✅ Pipeline Complete")
    for col, icon, label in zip(
        st.columns(4), ["🔍","📖","✍️","🧐"], ["Search","Scrape","Write","Critique"]
    ):
        col.success(f"{icon} {label}")

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([3, 2], gap="large")

    with left:
        st.markdown('<div class="card-title">📄 Research Report</div>', unsafe_allow_html=True)
        st.download_button(
            label="⬇ Download Report (.txt)",
            data=res.get("report", ""),
            file_name=f"report_{topic[:30].replace(' ','_')}.txt",
            mime="text/plain",
        )
        st.markdown(f'<div class="report-body">{res.get("report","")}</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card-title">🧐 Critic Feedback</div>', unsafe_allow_html=True)
        feedback = res.get("feedback", "")
        score_line = next((l for l in feedback.splitlines() if l.lower().startswith("score")), None)
        if score_line:
            st.markdown(f'<div class="score-pill">{score_line}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="report-body">{feedback}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔎 Raw Search Results"):
        st.text(res.get("search_results", ""))
    with st.expander("🌐 Raw Scraped Content"):
        st.text(res.get("scraped_content", ""))

elif not st.session_state.running:
    if not api_endpoint:
        st.markdown("""
        <div style="text-align:center;padding:4rem 0;color:#374151;">
            <div style="font-size:3rem;margin-bottom:1rem;">🔌</div>
            <div style="font-size:1.1rem;font-family:'JetBrains Mono',monospace;">
                Paste your <strong style="color:#7c6af7">Colab ngrok URL</strong> in the sidebar to connect
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:4rem 0;color:#374151;">
            <div style="font-size:3rem;margin-bottom:1rem;">🔬</div>
            <div style="font-size:1.1rem;font-family:'JetBrains Mono',monospace;">
                Enter a topic above and hit <strong style="color:#7c6af7">Run</strong> to start
            </div>
        </div>""", unsafe_allow_html=True)
