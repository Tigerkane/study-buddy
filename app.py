import streamlit as st
import pdfplumber
import json
import logging
import re
from datetime import datetime, timezone
from groq import Groq

# Suppress pdfplumber font warnings
logging.getLogger("pdfplumber").setLevel(logging.ERROR)

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
AVAILABLE_MODELS = ["llama-3.2-3b-preview", "mixtral-8x7b-32768"]

# ─────────────────────────────────────────────
# LANGUAGE CONFIG
# ─────────────────────────────────────────────
LANGUAGES = {
    "English": "en",
    "हिंदी (Hindi)": "hi",
    "తెలుగు (Telugu)": "te"
}

UI_TEXT = {
    "en": {
        "title": "📚 Study Buddy", "subtitle": "Last Minute · AI Powered",
        "upload": "Upload Notes", "drop": "Drop your PDF here",
        "mode": "Mode", "chat": "💬 Chat", "quiz": "📝 Quiz",
        "model": "Model", "file_info": "File Info",
        "chat_title": "💬 Chat with your Notes", "quiz_title": "📝 10-Question Quiz",
        "ask_placeholder": "e.g. Explain this concept in simple terms...",
        "send": "Send →", "clear": "🗑 Clear chat",
        "generate": "⚡ Generate 10 Questions", "submit": "✅ Submit Quiz",
        "regenerate": "🔄 Regenerate", "retake": "🔄 Take Quiz Again",
        "score": "Score", "percentage": "Percentage", "grade": "Grade",
        "excellent": "🏆 Excellent", "good": "👍 Good", "keep_studying": "📖 Keep Studying",
        "answer_review": "### Answer Review", "your_answer": "Your answer", "correct": "Correct",
        "thinking": "Thinking...", "generating": "Generating 10 questions from your notes...",
        "quick_prompts": "**Quick prompts:**",
        "prompt1": "Summarise the key points", "prompt2": "What are the most important terms?", "prompt3": "Give me 5 exam tips from this",
        "upload_info": "👆 Upload a PDF to get started",
        "upload_success": "characters extracted", "upload_error": "❌ Could not extract text. Is this a scanned PDF?",
        "quiz_error": "❌ Failed to generate quiz. Try again.",
        "answer_all": "questions, then click Submit.", "answered": "answered",
        "language": "🌐 Language", "you": "YOU", "buddy": "STUDY BUDDY",
        "fast": "⚡ Fast · Llama 3.2", "powerful": "🧠 Powerful · Mixtral",
        "upload_landing": "Upload your notes", "upload_landing_sub": "Drop a PDF in the sidebar to start chatting<br>or generate a quiz",
        "chat_placeholder": "Ask anything about your notes — concepts, explanations, quick summaries...",
        "api_key": "🔑 Groq API Key", "api_placeholder": "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",
        "api_saved": "✅ API key saved", "api_missing": "❌ Please enter your Groq API key in the sidebar.",
    },
    "hi": {
        "title": "📚 स्टडी बडी", "subtitle": "लास्ट मिनट · AI पावर्ड",
        "upload": "नोट्स अपलोड करें", "drop": "यहाँ PDF डालें",
        "mode": "मोड", "chat": "💬 चैट", "quiz": "📝 क्विज़",
        "model": "मॉडल", "file_info": "फ़ाइल जानकारी",
        "chat_title": "💬 अपने नोट्स से चैट करें", "quiz_title": "📝 10 प्रश्न क्विज़",
        "ask_placeholder": "जैसे: इस अवधारणा को सरल शब्दों में समझाएं...",
        "send": "भेजें →", "clear": "🗑 चैट साफ करें",
        "generate": "⚡ 10 प्रश्न बनाएं", "submit": "✅ क्विज़ जमा करें",
        "regenerate": "🔄 दोबारा बनाएं", "retake": "🔄 फिर से क्विज़ दें",
        "score": "स्कोर", "percentage": "प्रतिशत", "grade": "ग्रेड",
        "excellent": "🏆 शानदार", "good": "👍 अच्छा", "keep_studying": "📖 और पढ़ें",
        "answer_review": "### उत्तर समीक्षा", "your_answer": "आपका उत्तर", "correct": "सही उत्तर",
        "thinking": "सोच रहा हूँ...", "generating": "आपके नोट्स से 10 प्रश्न बना रहा हूँ...",
        "quick_prompts": "**त्वरित प्रश्न:**",
        "prompt1": "मुख्य बिंदु संक्षेप करें", "prompt2": "सबसे महत्वपूर्ण शब्द क्या हैं?", "prompt3": "इससे 5 परीक्षा टिप्स दें",
        "upload_info": "👆 शुरू करने के लिए PDF अपलोड करें",
        "upload_success": "अक्षर निकाले गए", "upload_error": "❌ टेक्स्ट नहीं निकाला जा सका।",
        "quiz_error": "❌ क्विज़ बनाने में विफल। दोबारा कोशिश करें।",
        "answer_all": "प्रश्नों के उत्तर दें, फिर जमा करें।", "answered": "उत्तर दिए",
        "language": "🌐 भाषा", "you": "आप", "buddy": "स्टडी बडी",
        "fast": "⚡ तेज़ · Llama 3.2", "powerful": "🧠 शक्तिशाली · Mixtral",
        "upload_landing": "अपने नोट्स अपलोड करें", "upload_landing_sub": "चैट शुरू करने के लिए साइडबार में PDF डालें<br>या क्विज़ बनाएं",
        "chat_placeholder": "अपने नोट्स के बारे में कुछ भी पूछें...",
        "api_key": "🔑 Groq API Key", "api_placeholder": "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",
        "api_saved": "✅ API key सेव हो गई", "api_missing": "❌ कृपया साइडबार में Groq API key डालें।",
    },
    "te": {
        "title": "📚 స్టడీ బడీ", "subtitle": "లాస్ట్ మినిట్ · AI పవర్డ్",
        "upload": "నోట్స్ అప్లోడ్ చేయండి", "drop": "ఇక్కడ PDF వేయండి",
        "mode": "మోడ్", "chat": "💬 చాట్", "quiz": "📝 క్విజ్",
        "model": "మోడల్", "file_info": "ఫైల్ సమాచారం",
        "chat_title": "💬 మీ నోట్స్‌తో చాట్ చేయండి", "quiz_title": "📝 10 ప్రశ్నల క్విజ్",
        "ask_placeholder": "ఉదా: ఈ అంశాన్ని సులభంగా వివరించండి...",
        "send": "పంపు →", "clear": "🗑 చాట్ తొలగించు",
        "generate": "⚡ 10 ప్రశ్నలు తయారుచేయి", "submit": "✅ క్విజ్ సమర్పించు",
        "regenerate": "🔄 మళ్ళీ తయారుచేయి", "retake": "🔄 మళ్ళీ క్విజ్ ఇవ్వు",
        "score": "స్కోర్", "percentage": "శాతం", "grade": "గ్రేడ్",
        "excellent": "🏆 అద్భుతం", "good": "👍 బాగుంది", "keep_studying": "📖 మరింత చదవండి",
        "answer_review": "### సమాధాన సమీక్ష", "your_answer": "మీ సమాధానం", "correct": "సరైన సమాధానం",
        "thinking": "ఆలోచిస్తున్నాను...", "generating": "మీ నోట్స్ నుండి 10 ప్రశ్నలు తయారుచేస్తున్నాను...",
        "quick_prompts": "**త్వరిత ప్రశ్నలు:**",
        "prompt1": "ముఖ్యమైన అంశాలు సంగ్రహించు", "prompt2": "అతి ముఖ్యమైన పదాలు ఏమిటి?", "prompt3": "దీని నుండి 5 పరీక్ష చిట్కాలు ఇవ్వు",
        "upload_info": "👆 ప్రారంభించడానికి PDF అప్లోడ్ చేయండి",
        "upload_success": "అక్షరాలు సేకరించబడ్డాయి", "upload_error": "❌ టెక్స్ట్ సేకరించలేకపోయాం.",
        "quiz_error": "❌ క్విజ్ తయారుచేయడం విఫలమైంది. మళ్ళీ ప్రయత్నించండి.",
        "answer_all": "ప్రశ్నలకు సమాధానమివ్వండి, తర్వాత సమర్పించండి.", "answered": "సమాధానమిచ్చారు",
        "language": "🌐 భాష", "you": "మీరు", "buddy": "స్టడీ బడీ",
        "fast": "⚡ వేగం · Llama 3.2", "powerful": "🧠 శక్తివంతం · Mixtral",
        "upload_landing": "మీ నోట్స్ అప్లోడ్ చేయండి", "upload_landing_sub": "చాట్ ప్రారంభించడానికి సైడ్‌బార్‌లో PDF వేయండి<br>లేదా క్విజ్ తయారుచేయండి",
        "chat_placeholder": "మీ నోట్స్ గురించి ఏదైనా అడగండి...",
        "api_key": "🔑 Groq API Key", "api_placeholder": "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",
        "api_saved": "✅ API key సేవ్ అయింది", "api_missing": "❌ దయచేసి సైడ్‌బార్‌లో Groq API key నమోదు చేయండి.",
    }
}

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="Last Minute Study Buddy", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
.stApp { background: #0d0f14; color: #e8eaf0; }
[data-testid="stSidebar"] { background: #13151c !important; border-right: 1px solid #1e2130; }
.hero-title { font-size: 2rem; font-weight: 700; color: #ffffff; line-height: 1.1; margin-bottom: 4px; }
.hero-sub { font-size: 0.85rem; color: #6b7280; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 24px; }
.chat-user { background: #1a3a5c; border-left: 3px solid #3b82f6; padding: 12px 16px; border-radius: 0 10px 10px 0; margin: 8px 0; font-size: 0.92rem; }
.chat-ai { background: #141a1f; border-left: 3px solid #10b981; padding: 12px 16px; border-radius: 0 10px 10px 0; margin: 8px 0; font-size: 0.92rem; }
.chat-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 4px; font-weight: 600; }
.user-label { color: #3b82f6; }
.ai-label { color: #10b981; }
.quiz-card { background: #13151c; border: 1px solid #1e2130; border-radius: 12px; padding: 20px 24px; margin-bottom: 20px; }
.quiz-q { font-size: 1rem; font-weight: 600; color: #f1f5f9; margin-bottom: 14px; line-height: 1.5; }
.quiz-number { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #6366f1; font-weight: 500; margin-bottom: 6px; }
[data-testid="stFileUploader"] { background: #13151c; border: 2px dashed #2d3748; border-radius: 12px; padding: 8px; }
.stButton > button { background: #6366f1; color: white; border: none; border-radius: 8px; font-family: 'Space Grotesk', sans-serif; font-weight: 600; padding: 8px 20px; transition: all 0.2s; }
.stButton > button:hover { background: #4f46e5; transform: translateY(-1px); }
.stTextInput > div > div > input, .stTextArea textarea { background: #13151c !important; border: 1px solid #2d3748 !important; color: #e8eaf0 !important; border-radius: 8px !important; font-family: 'Space Grotesk', sans-serif !important; }
.stRadio > div { gap: 10px; }
hr { border-color: #1e2130; }
[data-testid="metric-container"] { background: #13151c; border: 1px solid #1e2130; border-radius: 10px; padding: 12px 16px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# GROQ CLIENT
# ─────────────────────────────────────────────
def get_groq_client():
    api_key = st.session_state.get("groq_api_key") or st.secrets.get("GROQ_API_KEY", None)
    if not api_key:
        lang = st.session_state.get("language", "en")
        st.error(UI_TEXT[lang]["api_missing"])
        st.stop()
    return Groq(api_key=api_key)


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
# AI HELPERS
# ─────────────────────────────────────────────
def groq_stream(prompt, model):
    try:
        client = get_groq_client()
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True, max_tokens=1024
        )
        for chunk in stream:
            yield chunk.choices[0].delta.content or ""
    except Exception as e:
        yield f"\n⚠️ Groq error: {e}"


def groq_generate(prompt, model):
    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Groq error: {e}"


def build_chat_prompt(pdf_text, history, user_question):
    history_str = ""
    for h in history[-6:]:
        role = "Student" if h["role"] == "user" else "Assistant"
        history_str += f"{role}: {h['message']}\n"
    return f"""You are a helpful study assistant. Answer based ONLY on the provided notes. Be concise and exam-focused.

NOTES:
{pdf_text[:4000]}

CONVERSATION SO FAR:
{history_str}
Student: {user_question}
Assistant:"""


# ─────────────────────────────────────────────
# QUIZ GENERATION
# ─────────────────────────────────────────────
def generate_batch(chunk, model):
    prompt = f"""Generate exactly 10 multiple choice questions from these notes.
Each question must have 4 options (A, B, C, D) and one correct answer.

Notes:
{chunk}

Start with [ end with ]. Valid JSON only. No markdown, no explanation.

[
  {{
    "q": "Question?",
    "options": ["A) opt1", "B) opt2", "C) opt3", "D) opt4"],
    "answer": "A"
  }}
]"""

    for attempt in range(3):
        raw = groq_generate(prompt, model)
        try:
            clean = re.sub(r"```json|```", "", raw).strip()
            start = clean.find("[")
            end   = clean.rfind("]") + 1
            if start == -1 or end == 0:
                continue
            questions = json.loads(clean[start:end])
            valid = [q for q in questions if "q" in q and "options" in q and "answer" in q and len(q["options"]) == 4 and q["answer"] in ["A","B","C","D"]]
            if len(valid) >= 3:
                return valid[:10]
        except:
            continue
    return []


def generate_quiz_questions(pdf_text, model):
    questions = generate_batch(pdf_text[:4000], model)
    return questions[:10] if len(questions) >= 3 else None


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "session_id"     not in st.session_state: st.session_state.session_id     = f"s_{int(datetime.now(timezone.utc).timestamp())}"
if "mode"           not in st.session_state: st.session_state.mode           = "Chat"
if "pdf_text"       not in st.session_state: st.session_state.pdf_text       = None
if "pdf_name"       not in st.session_state: st.session_state.pdf_name       = None
if "chat_history"   not in st.session_state: st.session_state.chat_history   = []
if "quiz_questions" not in st.session_state: st.session_state.quiz_questions = None
if "quiz_answers"   not in st.session_state: st.session_state.quiz_answers   = {}
if "quiz_submitted" not in st.session_state: st.session_state.quiz_submitted = False
if "groq_model"     not in st.session_state: st.session_state.groq_model     = AVAILABLE_MODELS[0]
if "language"       not in st.session_state: st.session_state.language       = "en"
if "groq_api_key"   not in st.session_state: st.session_state.groq_api_key   = ""


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    lang = st.session_state.get("language", "en")
    T = UI_TEXT[lang]

    st.markdown(f'<div class="hero-title">{T["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-sub">{T["subtitle"]}</div>', unsafe_allow_html=True)

    # Language selector
    st.markdown(f"#### {T['language']}")
    selected_lang = st.radio("lang", list(LANGUAGES.keys()), index=list(LANGUAGES.values()).index(st.session_state.language), label_visibility="collapsed", horizontal=True)
    st.session_state.language = LANGUAGES[selected_lang]
    lang = st.session_state.language
    T = UI_TEXT[lang]

    st.markdown("---")

    # API Key input
    st.markdown(f"#### {T['api_key']}")
    api_key_input = st.text_input("api_key", type="password", placeholder=T["api_placeholder"], label_visibility="collapsed", value=st.session_state.groq_api_key)
    if api_key_input:
        st.session_state.groq_api_key = api_key_input
        st.caption(T["api_saved"])

    st.markdown("---")

    # PDF Upload
    st.markdown(f"#### {T['upload']}")
    uploaded_file = st.file_uploader(T["drop"], type=["pdf"], help="Upload lecture notes or textbook chapter")

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
                st.success(f"✅ {len(text):,} {T['upload_success']}")
            else:
                st.error(T["upload_error"])

    if st.session_state.pdf_text:
        st.markdown("---")
        st.markdown(f"#### {T['mode']}")
        mode = st.radio("mode", [T["chat"], T["quiz"]], index=0, label_visibility="collapsed")
        if "Chat" in mode or "चैट" in mode or "చాట్" in mode:
            st.session_state.mode = "Chat"
        else:
            st.session_state.mode = "Quiz"

        st.markdown("---")
        st.markdown(f"#### {T['model']}")
        selected_model = st.radio("model", AVAILABLE_MODELS, index=0, label_visibility="collapsed")
        st.session_state.groq_model = selected_model
        st.caption(T["fast"] if selected_model == AVAILABLE_MODELS[0] else T["powerful"])

        st.markdown("---")
        st.markdown(f"#### {T['file_info']}")
        st.markdown(f"**{st.session_state.pdf_name}**")
        words = len(st.session_state.pdf_text.split())
        st.caption(f"{words:,} words · {len(st.session_state.pdf_text):,} chars")
        st.caption(f"🤖 {selected_model}")
    else:
        st.markdown("---")
        st.info(T["upload_info"])


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
lang = st.session_state.get("language", "en")
T = UI_TEXT[lang]

if not st.session_state.pdf_text:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center; padding:60px 20px; background:#13151c; border:2px dashed #2d3748; border-radius:20px;">
            <div style="font-size:3.5rem; margin-bottom:16px;">📖</div>
            <div style="font-size:1.5rem; font-weight:700; color:#f1f5f9; margin-bottom:8px;">{T["upload_landing"]}</div>
            <div style="color:#6b7280; font-size:0.95rem;">{T["upload_landing_sub"]}</div>
        </div>
        """, unsafe_allow_html=True)

else:
    if st.session_state.mode == "Chat":
        st.markdown(f'<div class="hero-title">{T["chat_title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-sub">{st.session_state.pdf_name}</div>', unsafe_allow_html=True)

        if not st.session_state.chat_history:
            st.markdown(f"""<div style="background:#13151c; border:1px solid #1e2130; border-radius:12px; padding:20px; text-align:center; color:#6b7280; margin-bottom:16px;">{T["chat_placeholder"]}</div>""", unsafe_allow_html=True)
            st.markdown(T["quick_prompts"])
            qcols = st.columns(3)
            prompts = [T["prompt1"], T["prompt2"], T["prompt3"]]
            for i, p in enumerate(prompts):
                with qcols[i]:
                    if st.button(p, key=f"qp_{i}", use_container_width=True):
                        st.session_state._quick_prompt = p
                        st.rerun()

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user"><div class="chat-label user-label">{T["you"]}</div>{msg["message"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-ai"><div class="chat-label ai-label">{T["buddy"]}</div>{msg["message"]}</div>', unsafe_allow_html=True)

        user_input = None
        if hasattr(st.session_state, "_quick_prompt"):
            user_input = st.session_state._quick_prompt
            del st.session_state._quick_prompt

        st.markdown("<br>", unsafe_allow_html=True)
        col_inp, col_btn = st.columns([5, 1])
        with col_inp:
            question = st.text_input("Ask", placeholder=T["ask_placeholder"], label_visibility="collapsed", key="chat_input")
        with col_btn:
            send = st.button(T["send"], use_container_width=True)

        if (send and question) or user_input:
            q = user_input or question
            st.session_state.chat_history.append({"role": "user", "message": q})
            prompt = build_chat_prompt(st.session_state.pdf_text, st.session_state.chat_history[:-1], q)
            st.markdown(f'<div class="chat-user"><div class="chat-label user-label">{T["you"]}</div>{q}</div>', unsafe_allow_html=True)

            response_placeholder = st.empty()
            full_response = ""
            with st.spinner(T["thinking"]):
                for token in groq_stream(prompt, st.session_state.groq_model):
                    full_response += token
                    response_placeholder.markdown(f'<div class="chat-ai"><div class="chat-label ai-label">{T["buddy"]}</div>{full_response}▌</div>', unsafe_allow_html=True)

            response_placeholder.markdown(f'<div class="chat-ai"><div class="chat-label ai-label">{T["buddy"]}</div>{full_response}</div>', unsafe_allow_html=True)
            st.session_state.chat_history.append({"role": "assistant", "message": full_response})

        if st.session_state.chat_history:
            if st.button(T["clear"], key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()

    elif st.session_state.mode == "Quiz":
        st.markdown(f'<div class="hero-title">{T["quiz_title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-sub">{st.session_state.pdf_name}</div>', unsafe_allow_html=True)

        if st.session_state.quiz_questions is None:
            col_gen, _ = st.columns([2, 3])
            with col_gen:
                if st.button(T["generate"], use_container_width=True):
                    with st.spinner(T["generating"]):
                        questions = generate_quiz_questions(st.session_state.pdf_text, st.session_state.groq_model)
                    if questions:
                        st.session_state.quiz_questions = questions
                        st.session_state.quiz_answers   = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()
                    else:
                        st.error(T["quiz_error"])

        elif not st.session_state.quiz_submitted:
            questions = st.session_state.quiz_questions
            st.info(f"Answer all {len(questions)} {T['answer_all']}")
            st.markdown("<br>", unsafe_allow_html=True)

            for i, q in enumerate(questions):
                st.markdown(f"""<div class="quiz-card"><div class="quiz-number">Question {i+1} of {len(questions)}</div><div class="quiz-q">{q['q']}</div></div>""", unsafe_allow_html=True)
                answer = st.radio(f"q_{i}", q["options"], key=f"ans_{i}", label_visibility="collapsed")
                if answer:
                    st.session_state.quiz_answers[i] = answer[0]
                st.markdown("<br>", unsafe_allow_html=True)

            answered = len(st.session_state.quiz_answers)
            total    = len(questions)
            st.progress(answered / total, text=f"{answered}/{total} {T['answered']}")

            col_sub, col_reset = st.columns([2, 1])
            with col_sub:
                if st.button(T["submit"], use_container_width=True, disabled=(answered < total)):
                    st.session_state.quiz_submitted = True
                    st.rerun()
            with col_reset:
                if st.button(T["regenerate"], use_container_width=True):
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

            col1, col2, col3 = st.columns(3)
            with col1: st.metric(T["score"], f"{score}/{total}")
            with col2: st.metric(T["percentage"], f"{percent}%")
            with col3:
                grade = T["excellent"] if percent >= 80 else T["good"] if percent >= 60 else T["keep_studying"]
                st.metric(T["grade"], grade)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(T["answer_review"])

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
                    <div style="font-size:0.85rem; color:#94a3b8;">{T["your_answer"]}: <span style="color:{'#10b981' if is_correct else '#ef4444'}">{user_opt}</span></div>
                    {"" if is_correct else f'<div style="font-size:0.85rem;color:#10b981;margin-top:2px;">{T["correct"]}: {correct_opt}</div>'}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(T["retake"]):
                st.session_state.quiz_questions = None
                st.session_state.quiz_answers   = {}
                st.session_state.quiz_submitted = False
                st.rerun()