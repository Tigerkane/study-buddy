import streamlit as st
import pdfplumber
import requests
import json
from datetime import datetime, timezone
from pymongo import MongoClient
import re

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"   # change to mistral:7b or llama3.1:8b if you have it
MONGO_URI    = "mongodb://localhost:27017"
DB_NAME      = "studybuddy"

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Last Minute Study Buddy",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stApp { background: #0d0f14; color: #e8eaf0; }

[data-testid="stSidebar"] {
    background: #13151c !important;
    border-right: 1px solid #1e2130;
}

.hero-title {
    font-size: 2rem; font-weight: 700; color: #ffffff;
    line-height: 1.1; margin-bottom: 4px;
}
.hero-sub {
    font-size: 0.85rem; color: #6b7280;
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 24px;
}

.chat-user {
    background: #1a3a5c; border-left: 3px solid #3b82f6;
    padding: 12px 16px; border-radius: 0 10px 10px 0; margin: 8px 0; font-size: 0.92rem;
}
.chat-ai {
    background: #141a1f; border-left: 3px solid #10b981;
    padding: 12px 16px; border-radius: 0 10px 10px 0; margin: 8px 0; font-size: 0.92rem;
}
.chat-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 4px; font-weight: 600; }
.user-label { color: #3b82f6; }
.ai-label   { color: #10b981; }

.quiz-card {
    background: #13151c; border: 1px solid #1e2130;
    border-radius: 12px; padding: 20px 24px; margin-bottom: 20px;
}
.quiz-q      { font-size: 1rem; font-weight: 600; color: #f1f5f9; margin-bottom: 14px; line-height: 1.5; }
.quiz-number { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #6366f1; font-weight: 500; margin-bottom: 6px; }

[data-testid="stFileUploader"] {
    background: #13151c; border: 2px dashed #2d3748; border-radius: 12px; padding: 8px;
}

.stButton > button {
    background: #6366f1; color: white; border: none; border-radius: 8px;
    font-family: 'Space Grotesk', sans-serif; font-weight: 600; padding: 8px 20px; transition: all 0.2s;
}
.stButton > button:hover { background: #4f46e5; transform: translateY(-1px); }

.stTextInput > div > div > input, .stTextArea textarea {
    background: #13151c !important; border: 1px solid #2d3748 !important;
    color: #e8eaf0 !important; border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.stRadio > div { gap: 10px; }
hr { border-color: #1e2130; }

[data-testid="metric-container"] {
    background: #13151c; border: 1px solid #1e2130; border-radius: 10px; padding: 12px 16px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MONGODB
# ─────────────────────────────────────────────
@st.cache_resource
def get_db():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        client.server_info()
        return client[DB_NAME]
    except Exception:
        return None

db = get_db()

def save_chat(session_id, filename, role, message):
    if db is None:
        return
    try:
        db.chats.insert_one({
            "session_id": session_id,
            "filename":   filename,
            "role":       role,
            "message":    message,
            "timestamp":  datetime.now(timezone.utc)
        })
    except:
        pass

def save_quiz_result(session_id, filename, score, total):
    if db is None:
        return
    try:
        db.quiz_results.insert_one({
            "session_id": session_id,
            "filename":   filename,
            "score":      score,
            "total":      total,
            "percent":    round((score / total) * 100),
            "timestamp":  datetime.now(timezone.utc)
        })
    except:
        pass


# ─────────────────────────────────────────────
# PDF EXTRACTION
# ─────────────────────────────────────────────
def extract_pdf_text(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        return text.strip()
    except Exception:
        return None


# ─────────────────────────────────────────────
# OLLAMA HELPERS
# ─────────────────────────────────────────────
def ollama_stream(prompt):
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": True},
            stream=True,
            timeout=180
        )
        for line in resp.iter_lines():
            if line:
                data = json.loads(line)
                yield data.get("response", "")
                if data.get("done"):
                    break
    except Exception as e:
        yield f"\n⚠️ Ollama error: {e}. Make sure `ollama serve` is running."


def ollama_generate(prompt):
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=300
        )
        return resp.json().get("response", "")
    except Exception as e:
        return f"⚠️ Ollama error: {e}"


def build_chat_prompt(pdf_text, history, user_question):
    history_str = ""
    for h in history[-6:]:
        role = "Student" if h["role"] == "user" else "Assistant"
        history_str += f"{role}: {h['message']}\n"

    return f"""You are a helpful study assistant. A student has uploaded their study notes/PDF.
Answer questions based ONLY on the provided notes. Be concise and exam-focused.

NOTES:
{pdf_text[:4000]}

CONVERSATION SO FAR:
{history_str}
Student: {user_question}
Assistant:"""


# ─────────────────────────────────────────────
# QUIZ GENERATION — 2 batches of 10 (faster)
# ─────────────────────────────────────────────
def generate_batch(chunk, batch_num):
    prompt = f"""You are a study assistant. Generate exactly 10 multiple choice questions from these notes.
Each question must have 4 options (A, B, C, D) and exactly one correct answer.

Notes:
{chunk}

IMPORTANT:
- Start your response with [ and end with ]
- No text before [, no text after ]
- No markdown, no code fences, no explanation
- Valid JSON only

[
  {{
    "q": "Question text?",
    "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
    "answer": "A"
  }}
]"""

    for attempt in range(3):
        raw = ollama_generate(prompt)
        try:
            clean = re.sub(r"```json|```", "", raw).strip()
            start = clean.find("[")
            end   = clean.rfind("]") + 1
            if start == -1 or end == 0:
                continue
            questions = json.loads(clean[start:end])
            valid = [
                q for q in questions
                if "q" in q and "options" in q and "answer" in q
                and len(q["options"]) == 4
                and q["answer"] in ["A", "B", "C", "D"]
            ]
            if len(valid) >= 3:
                return valid[:10]
        except:
            continue
    return []


def generate_quiz_questions(pdf_text):
    half = len(pdf_text) // 2
    chunk1 = pdf_text[:half] if len(pdf_text) > 2000 else pdf_text
    chunk2 = pdf_text[half:] if len(pdf_text) > 2000 else pdf_text

    all_questions = []

    # Batch 1
    batch1 = generate_batch(chunk1[:4000], 1)
    all_questions.extend(batch1)

    # Batch 2
    batch2 = generate_batch(chunk2[:4000], 2)
    all_questions.extend(batch2)

    return all_questions[:20] if len(all_questions) >= 5 else None


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "session_id"      not in st.session_state: st.session_state.session_id      = f"s_{int(datetime.now(timezone.utc).timestamp())}"
if "mode"            not in st.session_state: st.session_state.mode            = "Chat"
if "pdf_text"        not in st.session_state: st.session_state.pdf_text        = None
if "pdf_name"        not in st.session_state: st.session_state.pdf_name        = None
if "chat_history"    not in st.session_state: st.session_state.chat_history    = []
if "quiz_questions"  not in st.session_state: st.session_state.quiz_questions  = None
if "quiz_answers"    not in st.session_state: st.session_state.quiz_answers    = {}
if "quiz_submitted"  not in st.session_state: st.session_state.quiz_submitted  = False
if "quiz_progress"   not in st.session_state: st.session_state.quiz_progress   = ""


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="hero-title">📚 Study Buddy</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Last Minute · AI Powered</div>', unsafe_allow_html=True)

    st.markdown("#### Upload Notes")
    uploaded_file = st.file_uploader(
        "Drop your PDF here",
        type=["pdf"],
        help="Upload lecture notes, textbook chapters, or any study material"
    )

    if uploaded_file:
        if uploaded_file.name != st.session_state.pdf_name:
            with st.spinner("Reading PDF..."):
                text = extract_pdf_text(uploaded_file)
            if text and len(text) > 100:
                st.session_state.pdf_text       = text
                st.session_state.pdf_name       = uploaded_file.name
                st.session_state.chat_history   = []
                st.session_state.quiz_questions = None
                st.session_state.quiz_answers   = {}
                st.session_state.quiz_submitted = False
                st.success(f"✅ {len(text):,} characters extracted")
            else:
                st.error("❌ Could not extract text. Is this a scanned PDF?")

    if st.session_state.pdf_text:
        st.markdown("---")
        st.markdown("#### Mode")
        mode = st.radio(
            "Choose what to do",
            ["💬 Chat", "📝 Quiz"],
            index=0,
            label_visibility="collapsed"
        )
        st.session_state.mode = mode.split(" ")[1]

        st.markdown("---")
        st.markdown("#### File Info")
        st.markdown(f"**{st.session_state.pdf_name}**")
        words = len(st.session_state.pdf_text.split())
        st.caption(f"{words:,} words · {len(st.session_state.pdf_text):,} chars")

        st.markdown("---")
        if db is not None:
            st.caption("🟢 MongoDB connected")
        else:
            st.caption("🟡 MongoDB offline (memory mode)")
    else:
        st.markdown("---")
        st.info("👆 Upload a PDF to get started")


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
if not st.session_state.pdf_text:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; padding:60px 20px; background:#13151c; border:2px dashed #2d3748; border-radius:20px;">
            <div style="font-size:3.5rem; margin-bottom:16px;">📖</div>
            <div style="font-size:1.5rem; font-weight:700; color:#f1f5f9; margin-bottom:8px;">Upload your notes</div>
            <div style="color:#6b7280; font-size:0.95rem;">Drop a PDF in the sidebar to start chatting<br>or generate a quiz</div>
        </div>
        """, unsafe_allow_html=True)

else:
    # ── CHAT MODE ──────────────────────────────────────
    if st.session_state.mode == "Chat":
        st.markdown('<div class="hero-title">💬 Chat with your Notes</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-sub">{st.session_state.pdf_name}</div>', unsafe_allow_html=True)

        if not st.session_state.chat_history:
            st.markdown("""
            <div style="background:#13151c; border:1px solid #1e2130; border-radius:12px; padding:20px; text-align:center; color:#6b7280; margin-bottom:16px;">
                Ask anything about your notes — concepts, explanations, quick summaries...
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**Quick prompts:**")
            qcols = st.columns(3)
            prompts = ["Summarise the key points", "What are the most important terms?", "Give me 5 exam tips from this"]
            for i, p in enumerate(prompts):
                with qcols[i]:
                    if st.button(p, key=f"qp_{i}", use_container_width=True):
                        st.session_state._quick_prompt = p
                        st.rerun()

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user"><div class="chat-label user-label">YOU</div>{msg["message"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-ai"><div class="chat-label ai-label">STUDY BUDDY</div>{msg["message"]}</div>', unsafe_allow_html=True)

        if hasattr(st.session_state, "_quick_prompt"):
            user_input = st.session_state._quick_prompt
            del st.session_state._quick_prompt
        else:
            user_input = None

        st.markdown("<br>", unsafe_allow_html=True)
        col_inp, col_btn = st.columns([5, 1])
        with col_inp:
            question = st.text_input("Ask", placeholder="e.g. Explain this concept in simple terms...", label_visibility="collapsed", key="chat_input")
        with col_btn:
            send = st.button("Send →", use_container_width=True)

        if (send and question) or user_input:
            q = user_input or question
            st.session_state.chat_history.append({"role": "user", "message": q})
            save_chat(st.session_state.session_id, st.session_state.pdf_name, "user", q)

            prompt = build_chat_prompt(st.session_state.pdf_text, st.session_state.chat_history[:-1], q)

            st.markdown(f'<div class="chat-user"><div class="chat-label user-label">YOU</div>{q}</div>', unsafe_allow_html=True)

            response_placeholder = st.empty()
            full_response = ""
            with st.spinner("Thinking..."):
                for token in ollama_stream(prompt):
                    full_response += token
                    response_placeholder.markdown(
                        f'<div class="chat-ai"><div class="chat-label ai-label">STUDY BUDDY</div>{full_response}▌</div>',
                        unsafe_allow_html=True
                    )

            response_placeholder.markdown(
                f'<div class="chat-ai"><div class="chat-label ai-label">STUDY BUDDY</div>{full_response}</div>',
                unsafe_allow_html=True
            )
            st.session_state.chat_history.append({"role": "assistant", "message": full_response})
            save_chat(st.session_state.session_id, st.session_state.pdf_name, "assistant", full_response)

        if st.session_state.chat_history:
            if st.button("🗑 Clear chat", key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()

    # ── QUIZ MODE ──────────────────────────────────────
    elif st.session_state.mode == "Quiz":
        st.markdown('<div class="hero-title">📝 Quiz</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-sub">{st.session_state.pdf_name}</div>', unsafe_allow_html=True)

        if st.session_state.quiz_questions is None:
            col_gen, _ = st.columns([2, 3])
            with col_gen:
                if st.button("⚡ Generate 20 Questions", use_container_width=True):
                    progress_bar = st.progress(0, text="Starting quiz generation...")
                    progress_bar.progress(10, text="Generating batch 1 of 2 (questions 1–10)...")
                    questions = []

                    half = len(st.session_state.pdf_text) // 2
                    chunk1 = st.session_state.pdf_text[:half][:4000]
                    chunk2 = st.session_state.pdf_text[half:][:4000]

                    batch1 = generate_batch(chunk1, 1)
                    progress_bar.progress(55, text=f"Batch 1 done ({len(batch1)} questions). Generating batch 2...")
                    questions.extend(batch1)

                    batch2 = generate_batch(chunk2, 2)
                    progress_bar.progress(95, text=f"Batch 2 done ({len(batch2)} questions). Finishing up...")
                    questions.extend(batch2)

                    progress_bar.progress(100, text="Done!")

                    if len(questions) >= 5:
                        st.session_state.quiz_questions = questions[:20]
                        st.session_state.quiz_answers   = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()
                    else:
                        st.error("❌ Failed to generate quiz. Make sure Ollama is running and try again.")

        elif not st.session_state.quiz_submitted:
            questions = st.session_state.quiz_questions
            st.info(f"Answer all {len(questions)} questions, then click Submit.")
            st.markdown("<br>", unsafe_allow_html=True)

            for i, q in enumerate(questions):
                st.markdown(f"""
                <div class="quiz-card">
                    <div class="quiz-number">Question {i+1} of {len(questions)}</div>
                    <div class="quiz-q">{q['q']}</div>
                </div>
                """, unsafe_allow_html=True)

                answer = st.radio(f"q_{i}", q["options"], key=f"ans_{i}", label_visibility="collapsed")
                if answer:
                    st.session_state.quiz_answers[i] = answer[0]
                st.markdown("<br>", unsafe_allow_html=True)

            answered = len(st.session_state.quiz_answers)
            total    = len(questions)
            st.progress(answered / total, text=f"{answered}/{total} answered")

            col_sub, col_reset = st.columns([2, 1])
            with col_sub:
                if st.button("✅ Submit Quiz", use_container_width=True, disabled=(answered < total)):
                    st.session_state.quiz_submitted = True
                    st.rerun()
            with col_reset:
                if st.button("🔄 Regenerate", use_container_width=True):
                    st.session_state.quiz_questions = None
                    st.session_state.quiz_answers   = {}
                    st.session_state.quiz_submitted = False
                    st.rerun()

        else:
            questions = st.session_state.quiz_questions
            answers   = st.session_state.quiz_answers
            score     = sum(1 for i, q in enumerate(questions) if answers.get(i, "") == q["answer"])
            total     = len(questions)
            percent   = round((score / total) * 100)

            save_quiz_result(st.session_state.session_id, st.session_state.pdf_name, score, total)

            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Score",      f"{score}/{total}")
            with col2: st.metric("Percentage", f"{percent}%")
            with col3:
                grade = "🏆 Excellent" if percent >= 80 else "👍 Good" if percent >= 60 else "📖 Keep Studying"
                st.metric("Grade", grade)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### Answer Review")

            for i, q in enumerate(questions):
                user_ans   = answers.get(i, "?")
                correct    = q["answer"]
                is_correct = user_ans == correct
                icon         = "✅" if is_correct else "❌"
                border_color = "#10b981" if is_correct else "#ef4444"
                correct_opt  = next((o for o in q["options"] if o.startswith(correct)), correct)
                user_opt     = next((o for o in q["options"] if o.startswith(user_ans)), user_ans)

                st.markdown(f"""
                <div style="background:#13151c; border-left:3px solid {border_color}; border-radius:0 10px 10px 0; padding:14px 18px; margin-bottom:10px;">
                    <div style="font-size:0.75rem; color:#6b7280; margin-bottom:4px;">Q{i+1}</div>
                    <div style="font-weight:600; color:#f1f5f9; margin-bottom:8px;">{icon} {q['q']}</div>
                    <div style="font-size:0.85rem; color:#94a3b8;">Your answer: <span style="color:{'#10b981' if is_correct else '#ef4444'}">{user_opt}</span></div>
                    {"" if is_correct else f'<div style="font-size:0.85rem;color:#10b981;margin-top:2px;">Correct: {correct_opt}</div>'}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Take Quiz Again"):
                st.session_state.quiz_questions = None
                st.session_state.quiz_answers   = {}
                st.session_state.quiz_submitted = False
                st.rerun()