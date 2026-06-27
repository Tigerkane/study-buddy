import streamlit as st
import pdfplumber
import json
import logging
import re
import requests
from datetime import datetime, timezone

# Suppress pdfplumber font warnings
logging.getLogger("pdfplumber").setLevel(logging.ERROR)

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
GROQ_MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
OLLAMA_MODELS = ["llama3.2:3b", "mistral:7b"]
OLLAMA_URL = "http://localhost:11434/api/generate"

# ─────────────────────────────────────────────
# LANGUAGE CONFIG
# ─────────────────────────────────────────────
LANGUAGES = {"English": "en", "हिंदी (Hindi)": "hi", "తెలుగు (Telugu)": "te"}

UI_TEXT = {
    "en": {
        "title": "📚 Study Buddy",
        "subtitle": "Last Minute · AI Powered",
        "upload": "Upload Notes",
        "drop": "Drop your PDF here",
        "mode": "Mode",
        "chat": "💬 Chat",
        "quiz": "📝 Quiz",
        "model": "Model",
        "file_info": "File Info",
        "chat_title": "💬 Chat with your Notes",
        "quiz_title": "📝 10-Question Quiz",
        "ask_placeholder": "e.g. Explain this concept in simple terms...",
        "send": "Send →",
        "clear": "🗑 Clear chat",
        "generate": "⚡ Generate 10 Questions",
        "submit": "✅ Submit Quiz",
        "regenerate": "🔄 Regenerate",
        "retake": "🔄 Take Quiz Again",
        "score": "Score",
        "percentage": "Percentage",
        "grade": "Grade",
        "excellent": "🏆 Excellent",
        "good": "👍 Good",
        "keep_studying": "📖 Keep Studying",
        "answer_review": "### Answer Review",
        "your_answer": "Your answer",
        "correct": "Correct",
        "thinking": "Thinking...",
        "generating": "Generating 10 questions from your notes...",
        "quick_prompts": "**Quick prompts:**",
        "prompt1": "Summarise the key points",
        "prompt2": "What are the most important terms?",
        "prompt3": "Give me 5 exam tips from this",
        "upload_info": "👆 Upload a PDF to get started",
        "upload_success": "characters extracted",
        "upload_error": "❌ Could not extract text. Is this a scanned PDF?",
        "quiz_error": "❌ Failed to generate quiz. Try again.",
        "answer_all": "questions, then click Submit.",
        "answered": "answered",
        "language": "🌐 Language",
        "you": "YOU",
        "buddy": "STUDY BUDDY",
        "upload_landing": "Upload your notes",
        "upload_landing_sub": "Drop a PDF in the sidebar to start chatting<br>or generate a quiz",
        "chat_placeholder": "Ask anything about your notes — concepts, explanations, quick summaries...",
        "ai_backend": "⚙️ AI Backend",
        "groq_cloud": "☁️ Groq (Cloud)",
        "ollama_local": "🖥️ Ollama (Local)",
        "api_key": "🔑 Groq API Key (BYOK)",
        "api_placeholder": "Paste your Groq API key (gsk_...)",
        "api_saved": "✅ API key saved",
        "api_missing": "❌ Please enter your Groq API key in the sidebar.",
        "ollama_model": "Ollama Model",
        "groq_model": "Groq Model",
        "ollama_info": "Make sure `ollama serve` is running locally",
        "ollama_error": "⚠️ Ollama not running. Start with: ollama serve",
        "download": "📥 Download Chat History",
        "flashcards": "🃏 Flashcards",
        "difficulty": "Difficulty",
        "easy": "Easy",
        "medium": "Medium",
        "hard": "Hard",
        "multi_pdf_info": "Upload one or more PDFs",
        "quiz_download": "📥 Download Quiz Report",
        "gen_flashcards": "⚡ Generate Flashcards",
        "flip_card": "👆 Tap to flip",
        "next_card": "Next →",
        "prev_card": "← Prev",
        "card_of": "Card",
        "flashcard_error": "❌ Failed to generate flashcards. Try again.",
        "section_label": "Section to study",
        "section_word": "Section",
    },
    "hi": {
        "title": "📚 स्टडी बडी",
        "subtitle": "लास्ट मिनट · AI पावर्ड",
        "upload": "नोट्स अपलोड करें",
        "drop": "यहाँ PDF डालें",
        "mode": "मोड",
        "chat": "💬 चैट",
        "quiz": "📝 क्विज़",
        "model": "मॉडल",
        "file_info": "फ़ाइल जानकारी",
        "chat_title": "💬 अपने नोट्स से चैट करें",
        "quiz_title": "📝 10 प्रश्न क्विज़",
        "ask_placeholder": "जैसे: इस अवधारणा को सरल शब्दों में समझाएं...",
        "send": "भेजें →",
        "clear": "🗑 चैट साफ करें",
        "generate": "⚡ 10 प्रश्न बनाएं",
        "submit": "✅ क्विज़ जमा करें",
        "regenerate": "🔄 दोबारा बनाएं",
        "retake": "🔄 फिर से क्विज़ दें",
        "score": "स्कोर",
        "percentage": "प्रतिशत",
        "grade": "ग्रेड",
        "excellent": "🏆 शानदार",
        "good": "👍 अच्छा",
        "keep_studying": "📖 और पढ़ें",
        "answer_review": "### उत्तर समीक्षा",
        "your_answer": "आपका उत्तर",
        "correct": "सही उत्तर",
        "thinking": "सोच रहा हूँ...",
        "generating": "10 प्रश्न बना रहा हूँ...",
        "quick_prompts": "**त्वरित प्रश्न:**",
        "prompt1": "मुख्य बिंदु संक्षेप करें",
        "prompt2": "सबसे महत्वपूर्ण शब्द?",
        "prompt3": "5 परीक्षा टिप्स दें",
        "upload_info": "👆 PDF अपलोड करें",
        "upload_success": "अक्षर निकाले गए",
        "upload_error": "❌ टेक्स्ट नहीं निकाला जा सका।",
        "quiz_error": "❌ क्विज़ बनाने में विफल।",
        "answer_all": "प्रश्नों के उत्तर दें।",
        "answered": "उत्तर दिए",
        "language": "🌐 भाषा",
        "you": "आप",
        "buddy": "स्टडी बडी",
        "upload_landing": "अपने नोट्स अपलोड करें",
        "upload_landing_sub": "साइडबार में PDF डालें",
        "chat_placeholder": "अपने नोट्स के बारे में कुछ भी पूछें...",
        "ai_backend": "⚙️ AI बैकएंड",
        "groq_cloud": "☁️ Groq (क्लाउड)",
        "ollama_local": "🖥️ Ollama (लोकल)",
        "api_key": "🔑 Groq API Key (BYOK)",
        "api_placeholder": "Groq API key डालें (gsk_...)",
        "api_saved": "✅ API key सेव हो गई",
        "api_missing": "❌ Groq API key डालें।",
        "ollama_model": "Ollama मॉडल",
        "groq_model": "Groq मॉडल",
        "ollama_info": "`ollama serve` चला रहा है सुनिश्चित करें",
        "ollama_error": "⚠️ Ollama नहीं चल रहा। ollama serve चलाएं",
        "download": "📥 चैट इतिहास डाउनलोड करें",
        "flashcards": "🃏 फ्लैशकार्ड",
        "difficulty": "कठिनाई",
        "easy": "आसान",
        "medium": "मध्यम",
        "hard": "कठिन",
        "multi_pdf_info": "एक या अधिक PDF अपलोड करें",
        "quiz_download": "📥 क्विज़ रिपोर्ट डाउनलोड करें",
        "gen_flashcards": "⚡ फ्लैशकार्ड बनाएं",
        "flip_card": "👆 पलटने के लिए टैप करें",
        "next_card": "आगे →",
        "prev_card": "← पीछे",
        "card_of": "कार्ड",
        "flashcard_error": "❌ फ्लैशकार्ड बनाने में विफल।",
        "section_label": "पढ़ने के लिए सेक्शन",
        "section_word": "सेक्शन",
    },
    "te": {
        "title": "📚 స్టడీ బడీ",
        "subtitle": "లాస్ట్ మినిట్ · AI పవర్డ్",
        "upload": "నోట్స్ అప్లోడ్ చేయండి",
        "drop": "ఇక్కడ PDF వేయండి",
        "mode": "మోడ్",
        "chat": "💬 చాట్",
        "quiz": "📝 క్విజ్",
        "model": "మోడల్",
        "file_info": "ఫైల్ సమాచారం",
        "chat_title": "💬 మీ నోట్స్‌తో చాట్",
        "quiz_title": "📝 10 ప్రశ్నల క్విజ్",
        "ask_placeholder": "ఉదా: ఈ అంశాన్ని వివరించండి...",
        "send": "పంపు →",
        "clear": "🗑 చాట్ తొలగించు",
        "generate": "⚡ 10 ప్రశ్నలు తయారుచేయి",
        "submit": "✅ క్విజ్ సమర్పించు",
        "regenerate": "🔄 మళ్ళీ తయారుచేయి",
        "retake": "🔄 మళ్ళీ క్విజ్",
        "score": "స్కోర్",
        "percentage": "శాతం",
        "grade": "గ్రేడ్",
        "excellent": "🏆 అద్భుతం",
        "good": "👍 బాగుంది",
        "keep_studying": "📖 మరింత చదవండి",
        "answer_review": "### సమాధాన సమీక్ష",
        "your_answer": "మీ సమాధానం",
        "correct": "సరైన సమాధానం",
        "thinking": "ఆలోచిస్తున్నాను...",
        "generating": "10 ప్రశ్నలు తయారుచేస్తున్నాను...",
        "quick_prompts": "**త్వరిత ప్రశ్నలు:**",
        "prompt1": "ముఖ్యమైన అంశాలు",
        "prompt2": "ముఖ్యమైన పదాలు?",
        "prompt3": "5 పరీక్ష చిట్కాలు",
        "upload_info": "👆 PDF అప్లోడ్ చేయండి",
        "upload_success": "అక్షరాలు సేకరించబడ్డాయి",
        "upload_error": "❌ టెక్స్ట్ సేకరించలేకపోయాం.",
        "quiz_error": "❌ క్విజ్ విఫలమైంది.",
        "answer_all": "ప్రశ్నలకు సమాధానమివ్వండి.",
        "answered": "సమాధానమిచ్చారు",
        "language": "🌐 భాష",
        "you": "మీరు",
        "buddy": "స్టడీ బడీ",
        "upload_landing": "నోట్స్ అప్లోడ్ చేయండి",
        "upload_landing_sub": "సైడ్‌బార్‌లో PDF వేయండి",
        "chat_placeholder": "నోట్స్ గురించి అడగండి...",
        "ai_backend": "⚙️ AI బ్యాకెండ్",
        "groq_cloud": "☁️ Groq (క్లౌడ్)",
        "ollama_local": "🖥️ Ollama (లోకల్)",
        "api_key": "🔑 Groq API Key (BYOK)",
        "api_placeholder": "Groq API key పేస్ట్ చేయండి (gsk_...)",
        "api_saved": "✅ API key సేవ్ అయింది",
        "api_missing": "❌ Groq API key నమోదు చేయండి.",
        "ollama_model": "Ollama మోడల్",
        "groq_model": "Groq మోడల్",
        "ollama_info": "`ollama serve` నడుస్తుందో నిర్ధారించుకోండి",
        "ollama_error": "⚠️ Ollama నడవడం లేదు. ollama serve చేయండి",
        "download": "📥 చాట్ చరిత్ర డౌన్‌లోడ్",
        "flashcards": "🃏 ఫ్లాష్‌కార్డ్‌లు",
        "difficulty": "కష్టస్థాయి",
        "easy": "సులభం",
        "medium": "మధ్యస్థం",
        "hard": "కష్టం",
        "multi_pdf_info": "ఒకటి లేదా అంతకంటే ఎక్కువ PDFలు అప్‌లోడ్ చేయండి",
        "quiz_download": "📥 క్విజ్ రిపోర్ట్ డౌన్‌లోడ్",
        "gen_flashcards": "⚡ ఫ్లాష్‌కార్డ్‌లు తయారుచేయి",
        "flip_card": "👆 తిప్పడానికి నొక్కండి",
        "next_card": "తర్వాత →",
        "prev_card": "← మునుపటి",
        "card_of": "కార్డ్",
        "flashcard_error": "❌ ఫ్లాష్‌కార్డ్‌లు విఫలమైంది.",
        "section_label": "చదవడానికి సెక్షన్",
        "section_word": "సెక్షన్",
    },
}

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Last Minute Study Buddy",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown(
    """
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
.user-label { color: #3b82f6; } .ai-label { color: #10b981; }
.quiz-card { background: #13151c; border: 1px solid #1e2130; border-radius: 12px; padding: 20px 24px; margin-bottom: 20px; }
.quiz-q { font-size: 1rem; font-weight: 600; color: #f1f5f9; margin-bottom: 14px; line-height: 1.5; }
.quiz-number { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #6366f1; font-weight: 500; margin-bottom: 6px; }
.backend-groq { background: #1a2744; border: 1px solid #3b82f6; border-radius: 8px; padding: 8px 12px; margin: 4px 0; font-size: 0.8rem; color: #93c5fd; }
.backend-ollama { background: #1a2e1a; border: 1px solid #10b981; border-radius: 8px; padding: 8px 12px; margin: 4px 0; font-size: 0.8rem; color: #6ee7b7; }
[data-testid="stFileUploader"] { background: #13151c; border: 2px dashed #2d3748; border-radius: 12px; padding: 8px; }
.stButton > button { background: #6366f1; color: white; border: none; border-radius: 8px; font-family: 'Space Grotesk', sans-serif; font-weight: 600; padding: 8px 20px; transition: all 0.2s; }
.stButton > button:hover { background: #4f46e5; transform: translateY(-1px); }
.stTextInput > div > div > input { background: #13151c !important; border: 1px solid #2d3748 !important; color: #e8eaf0 !important; border-radius: 8px !important; }
.stRadio > div { gap: 10px; }
hr { border-color: #1e2130; }
[data-testid="metric-container"] { background: #13151c; border: 1px solid #1e2130; border-radius: 10px; padding: 12px 16px; }
@media (max-width: 768px) {
    .hero-title { font-size: 1.4rem; }
    .chat-user, .chat-ai { padding: 8px 12px; font-size: 0.85rem; }
    .quiz-card { padding: 14px 16px; }
}
</style>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────
# AI FUNCTIONS
# ─────────────────────────────────────────────
def get_groq_client():
    try:
        from groq import Groq

        api_key = st.session_state.get("groq_api_key") or st.secrets.get(
            "GROQ_API_KEY", None
        )
        if not api_key:
            lang = st.session_state.get("language", "en")
            st.error(UI_TEXT[lang]["api_missing"])
            st.stop()
        return Groq(api_key=api_key)
    except ImportError:
        st.error("❌ groq package not installed. Run: pip install groq")
        st.stop()


def ai_stream(prompt):
    backend = st.session_state.get("backend", "Groq")
    model = st.session_state.get("selected_model", GROQ_MODELS[0])

    if backend == "Groq":
        try:
            client = get_groq_client()
            stream = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                max_tokens=1024,
            )
            for chunk in stream:
                yield chunk.choices[0].delta.content or ""
        except Exception as e:
            yield f"\n⚠️ Groq error: {e}"
    else:
        try:
            resp = requests.post(
                OLLAMA_URL,
                json={"model": model, "prompt": prompt, "stream": True},
                stream=True,
                timeout=180,
            )
            for line in resp.iter_lines():
                if line:
                    data = json.loads(line)
                    yield data.get("response", "")
                    if data.get("done"):
                        break
        except Exception as e:
            lang = st.session_state.get("language", "en")
            yield f"\n{UI_TEXT[lang]['ollama_error']}: {e}"


def ai_generate(prompt):
    backend = st.session_state.get("backend", "Groq")
    model = st.session_state.get("selected_model", GROQ_MODELS[0])

    if backend == "Groq":
        try:
            client = get_groq_client()
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ Groq error: {e}"
    else:
        try:
            resp = requests.post(
                OLLAMA_URL,
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=300,
            )
            return resp.json().get("response", "")
        except Exception as e:
            lang = st.session_state.get("language", "en")
            return f"{UI_TEXT[lang]['ollama_error']}: {e}"


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


def get_active_chunk(full_text, chunk_size=4000):
    """Return the text to send to the AI.
    If full_doc_mode is on (Groq + llama-3.3-70b only), send the whole document
    (capped at ~100k chars, well within the model's large context window).
    Otherwise, return just the user-selected ~4000-char section.
    """
    if st.session_state.get("full_doc_mode", False):
        return full_text[:100000]
    idx = st.session_state.get("active_chunk", 0)
    start = idx * chunk_size
    return full_text[start : start + chunk_size]


# ─────────────────────────────────────────────
# CHAT PROMPT
# ─────────────────────────────────────────────
def build_chat_prompt(pdf_text, history, user_question):
    history_str = ""
    for h in history[-6:]:
        role = "Student" if h["role"] == "user" else "Assistant"
        history_str += f"{role}: {h['message']}\n"

    lang_names = {"en": "English", "hi": "Hindi", "te": "Telugu"}
    response_lang = lang_names.get(st.session_state.get("language", "en"), "English")

    return f"""You are a helpful study assistant. Answer based ONLY on the provided notes. Be concise and exam-focused.
Respond ONLY in {response_lang}, regardless of the language of the notes below.

NOTES:
{pdf_text[:4000]}

CONVERSATION:
{history_str}
Student: {user_question}
Assistant:"""


# ─────────────────────────────────────────────
# QUIZ GENERATION
# ─────────────────────────────────────────────
def generate_quiz_questions(pdf_text):
    lang_names = {"en": "English", "hi": "Hindi", "te": "Telugu"}
    response_lang = lang_names.get(st.session_state.get("language", "en"), "English")
    difficulty = st.session_state.get("quiz_difficulty", "Medium")

    prompt = f"""Generate exactly 10 multiple choice questions from these notes.
Each question must have 4 options (A, B, C, D) and one correct answer.
Write the questions and options in {response_lang}.
Make the questions {difficulty} difficulty level.

Notes:
{pdf_text[:4000]}

Start with [ end with ]. Valid JSON only. No markdown.

[
  {{
    "q": "Question?",
    "options": ["A) opt1", "B) opt2", "C) opt3", "D) opt4"],
    "answer": "A"
  }}
]"""

    for attempt in range(3):
        raw = ai_generate(prompt)
        try:
            clean = re.sub(r"```json|```", "", raw).strip()
            start = clean.find("[")
            end = clean.rfind("]") + 1
            if start == -1 or end == 0:
                continue
            questions = json.loads(clean[start:end])
            valid = [
                q
                for q in questions
                if "q" in q
                and "options" in q
                and "answer" in q
                and len(q["options"]) == 4
                and q["answer"] in ["A", "B", "C", "D"]
            ]
            if len(valid) >= 3:
                return valid[:10]
        except Exception:
            continue
    return None


# ─────────────────────────────────────────────
# FLASHCARD GENERATION
# ─────────────────────────────────────────────
def generate_flashcards(pdf_text):
    lang_names = {"en": "English", "hi": "Hindi", "te": "Telugu"}
    response_lang = lang_names.get(st.session_state.get("language", "en"), "English")

    prompt = f"""Generate exactly 10 flashcards from these notes for quick last-minute revision.
Each flashcard has a short "front" (a term, question, or concept) and a "back" (a concise answer or explanation, max 2 sentences).
Write the flashcards in {response_lang}.

Notes:
{pdf_text[:4000]}

Start with [ end with ]. Valid JSON only. No markdown.

[
  {{
    "front": "Term or question",
    "back": "Concise answer or explanation"
  }}
]"""

    for attempt in range(3):
        raw = ai_generate(prompt)
        try:
            clean = re.sub(r"```json|```", "", raw).strip()
            start = clean.find("[")
            end = clean.rfind("]") + 1
            if start == -1 or end == 0:
                continue
            cards = json.loads(clean[start:end])
            valid = [c for c in cards if "front" in c and "back" in c]
            if len(valid) >= 3:
                return valid[:10]
        except Exception:
            continue
    return None


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = f"s_{int(datetime.now(timezone.utc).timestamp())}"
if "mode" not in st.session_state:
    st.session_state.mode = "Chat"
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = None
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "language" not in st.session_state:
    st.session_state.language = "en"
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = ""
if "backend" not in st.session_state:
    st.session_state.backend = "Groq"
if "selected_model" not in st.session_state:
    st.session_state.selected_model = GROQ_MODELS[0]
if "quiz_difficulty" not in st.session_state:
    st.session_state.quiz_difficulty = "Medium"
if "flashcards" not in st.session_state:
    st.session_state.flashcards = None
if "flashcard_idx" not in st.session_state:
    st.session_state.flashcard_idx = 0
if "flashcard_flipped" not in st.session_state:
    st.session_state.flashcard_flipped = False
if "pdf_names" not in st.session_state:
    st.session_state.pdf_names = []
if "active_chunk" not in st.session_state:
    st.session_state.active_chunk = 0
if "full_doc_mode" not in st.session_state:
    st.session_state.full_doc_mode = False


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    lang = st.session_state.get("language", "en")
    T = UI_TEXT[lang]

    st.markdown(f'<div class="hero-title">{T["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-sub">{T["subtitle"]}</div>', unsafe_allow_html=True)

    # Language
    st.markdown(f"#### {T['language']}")
    selected_lang = st.radio(
        "lang",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.values()).index(st.session_state.language),
        label_visibility="collapsed",
        horizontal=True,
    )
    st.session_state.language = LANGUAGES[selected_lang]
    lang = st.session_state.language
    T = UI_TEXT[lang]

    st.markdown("---")

    # AI Backend toggle
    st.markdown(f"#### {T['ai_backend']}")
    backend = st.radio(
        "backend",
        [T["groq_cloud"], T["ollama_local"]],
        index=0,
        label_visibility="collapsed",
    )
    st.session_state.backend = (
        "Groq"
        if "Groq" in backend or "क्लाउड" in backend or "క్లౌడ్" in backend
        else "Ollama"
    )

    if st.session_state.backend == "Groq":
        # BYOK — API key input
        st.markdown(f"#### {T['api_key']}")
        api_key_input = st.text_input(
            "api",
            type="password",
            placeholder=T["api_placeholder"],
            label_visibility="collapsed",
            value=st.session_state.groq_api_key,
        )
        if api_key_input:
            st.session_state.groq_api_key = api_key_input
            if api_key_input.startswith("gsk_") and len(api_key_input) > 20:
                st.caption(T["api_saved"])
            else:
                st.caption(
                    "⚠️ This doesn't look like a valid Groq key — it should start with `gsk_`. Get one free at console.groq.com"
                )

        # Groq model selector
        st.markdown(f"#### {T['groq_model']}")
        selected_model = st.radio(
            "gmodel", GROQ_MODELS, index=0, label_visibility="collapsed"
        )
        st.session_state.selected_model = selected_model
        st.markdown(
            f'<div class="backend-groq">☁️ {selected_model}</div>',
            unsafe_allow_html=True,
        )

    else:
        # Ollama model selector
        st.markdown(f"#### {T['ollama_model']}")
        selected_model = st.radio(
            "omodel", OLLAMA_MODELS, index=0, label_visibility="collapsed"
        )
        st.session_state.selected_model = selected_model
        st.markdown(
            f'<div class="backend-ollama">🖥️ {selected_model}</div>',
            unsafe_allow_html=True,
        )
        st.caption(T["ollama_info"])

    st.markdown("---")

    # PDF Upload (multi-file)
    st.markdown(f"#### {T['upload']}")
    st.caption(T["multi_pdf_info"])
    uploaded_files = st.file_uploader(
        T["drop"], type=["pdf"], accept_multiple_files=True
    )

    if uploaded_files:
        new_names = [f.name for f in uploaded_files]
        if new_names != st.session_state.pdf_names:
            with st.spinner("Reading PDF(s)..."):
                texts = []
                for f in uploaded_files:
                    t = extract_pdf_text(f)
                    if t and len(t) > 50:
                        texts.append(f"--- {f.name} ---\n{t}")
            combined = "\n\n".join(texts)
            if combined and len(combined) > 100:
                st.session_state.pdf_text = combined
                st.session_state.pdf_name = ", ".join(new_names)
                st.session_state.pdf_names = new_names
                st.session_state.chat_history = []
                st.session_state.quiz_questions = None
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.session_state.flashcards = None
                st.session_state.flashcard_idx = 0
                st.session_state.active_chunk = 0
                st.success(f"✅ {len(combined):,} {T['upload_success']}")
                if len(combined) > 4000:
                    st.warning(
                        "⚠️ This document is long — use the Section selector below to choose which part to study (each AI request covers ~4000 characters)."
                    )
            else:
                st.error(T["upload_error"])

    if st.session_state.pdf_text:
        st.markdown("---")
        st.markdown(f"#### {T['mode']}")
        mode = st.radio(
            "mode",
            [T["chat"], T["quiz"], T["flashcards"]],
            index=0,
            label_visibility="collapsed",
        )
        if "Chat" in mode or "चैट" in mode or "చాట్" in mode:
            st.session_state.mode = "Chat"
        elif "Quiz" in mode or "क्विज़" in mode or "క్విజ్" in mode:
            st.session_state.mode = "Quiz"
        else:
            st.session_state.mode = "Flashcards"

        if st.session_state.mode == "Quiz":
            st.markdown(f"##### {T['difficulty']}")
            diff = st.radio(
                "difficulty",
                [T["easy"], T["medium"], T["hard"]],
                index=1,
                horizontal=True,
                label_visibility="collapsed",
            )
            diff_map = {T["easy"]: "Easy", T["medium"]: "Medium", T["hard"]: "Hard"}
            st.session_state.quiz_difficulty = diff_map.get(diff, "Medium")

        st.markdown("---")
        st.markdown(f"#### {T['file_info']}")
        st.markdown(f"**{st.session_state.pdf_name}**")
        words = len(st.session_state.pdf_text.split())
        st.caption(f"{words:,} words · {len(st.session_state.pdf_text):,} chars")

        # Section selector for long documents (each section ~4000 chars)
        CHUNK_SIZE = 4000
        full_text = st.session_state.pdf_text
        num_chunks = max(1, -(-len(full_text) // CHUNK_SIZE))  # ceil division
        if num_chunks > 1:
            st.markdown("---")

            # Full-document mode toggle — only available with Groq's large-context model
            can_use_full_doc = (
                st.session_state.backend == "Groq"
                and st.session_state.selected_model
                == GROQ_MODELS[0]  # llama-3.3-70b-versatile
            )
            if can_use_full_doc:
                full_doc = st.toggle(
                    "📖 Read entire document (slower, uses Llama 3.3 70B's large context)",
                    value=st.session_state.full_doc_mode,
                )
                st.session_state.full_doc_mode = full_doc
            else:
                st.session_state.full_doc_mode = False
                st.caption(
                    "💡 Switch to Groq · llama-3.3-70b-versatile to enable full-document mode"
                )

            if not st.session_state.full_doc_mode:
                st.markdown(f"#### 📑 {T.get('section_label', 'Section to study')}")
                section_options = list(range(num_chunks))
                chosen = st.selectbox(
                    "section",
                    section_options,
                    index=min(st.session_state.active_chunk, num_chunks - 1),
                    format_func=lambda i: f"{T.get('section_word', 'Section')} {i + 1} / {num_chunks}",
                    label_visibility="collapsed",
                )
                st.session_state.active_chunk = chosen
                st.caption(
                    f"≈ {min(CHUNK_SIZE, len(full_text) - chosen * CHUNK_SIZE):,} chars in this section"
                )
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
        st.markdown(
            f"""
        <div style="text-align:center; padding:60px 20px; background:#13151c; border:2px dashed #2d3748; border-radius:20px;">
            <div style="font-size:3.5rem; margin-bottom:16px;">📖</div>
            <div style="font-size:1.5rem; font-weight:700; color:#f1f5f9; margin-bottom:8px;">{T["upload_landing"]}</div>
            <div style="color:#6b7280; font-size:0.95rem;">{T["upload_landing_sub"]}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

else:
    if st.session_state.mode == "Chat":
        st.markdown(
            f'<div class="hero-title">{T["chat_title"]}</div>', unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="hero-sub">{st.session_state.pdf_name} · {st.session_state.selected_model}</div>',
            unsafe_allow_html=True,
        )

        if not st.session_state.chat_history:
            st.markdown(
                f"""<div style="background:#13151c;border:1px solid #1e2130;border-radius:12px;padding:20px;text-align:center;color:#6b7280;margin-bottom:16px;">{T["chat_placeholder"]}</div>""",
                unsafe_allow_html=True,
            )
            st.markdown(T["quick_prompts"])
            qcols = st.columns(3)
            for i, p in enumerate([T["prompt1"], T["prompt2"], T["prompt3"]]):
                with qcols[i]:
                    if st.button(p, key=f"qp_{i}", use_container_width=True):
                        st.session_state._quick_prompt = p
                        st.rerun()

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="chat-user"><div class="chat-label user-label">{T["you"]}</div>{msg["message"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="chat-ai"><div class="chat-label ai-label">{T["buddy"]}</div>{msg["message"]}</div>',
                    unsafe_allow_html=True,
                )

        user_input = None
        if hasattr(st.session_state, "_quick_prompt"):
            user_input = st.session_state._quick_prompt
            del st.session_state._quick_prompt

        st.markdown("<br>", unsafe_allow_html=True)
        col_inp, col_btn = st.columns([5, 1])
        with col_inp:
            question = st.text_input(
                "Ask",
                placeholder=T["ask_placeholder"],
                label_visibility="collapsed",
                key="chat_input",
            )
        with col_btn:
            send = st.button(T["send"], use_container_width=True)

        if (send and question) or user_input:
            q = user_input or question
            st.session_state.chat_history.append({"role": "user", "message": q})
            active_text = get_active_chunk(st.session_state.pdf_text)
            prompt = build_chat_prompt(
                active_text, st.session_state.chat_history[:-1], q
            )
            st.markdown(
                f'<div class="chat-user"><div class="chat-label user-label">{T["you"]}</div>{q}</div>',
                unsafe_allow_html=True,
            )

            response_placeholder = st.empty()
            full_response = ""
            with st.spinner(T["thinking"]):
                for token in ai_stream(prompt):
                    full_response += token
                    response_placeholder.markdown(
                        f'<div class="chat-ai"><div class="chat-label ai-label">{T["buddy"]}</div>{full_response}▌</div>',
                        unsafe_allow_html=True,
                    )

            response_placeholder.markdown(
                f'<div class="chat-ai"><div class="chat-label ai-label">{T["buddy"]}</div>{full_response}</div>',
                unsafe_allow_html=True,
            )
            st.session_state.chat_history.append(
                {"role": "assistant", "message": full_response}
            )

        if st.session_state.chat_history:
            col_cl, col_dl = st.columns([1, 1])
            with col_cl:
                if st.button(T["clear"], key="clear_chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()
            with col_dl:
                # Build download text
                chat_text = f"Chat History — {st.session_state.pdf_name}\n"
                chat_text += "=" * 50 + "\n\n"
                for msg in st.session_state.chat_history:
                    role = T["you"] if msg["role"] == "user" else T["buddy"]
                    chat_text += f"{role}:\n{msg['message']}\n\n"
                st.download_button(
                    label=T["download"],
                    data=chat_text,
                    file_name=f"chat_{st.session_state.pdf_name.replace('.pdf','')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

    elif st.session_state.mode == "Quiz":
        st.markdown(
            f'<div class="hero-title">{T["quiz_title"]}</div>', unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="hero-sub">{st.session_state.pdf_name} · {st.session_state.selected_model}</div>',
            unsafe_allow_html=True,
        )

        if st.session_state.quiz_questions is None:
            col_gen, _ = st.columns([2, 3])
            with col_gen:
                if st.button(T["generate"], use_container_width=True):
                    with st.spinner(T["generating"]):
                        questions = generate_quiz_questions(
                            get_active_chunk(st.session_state.pdf_text)
                        )
                    if questions:
                        st.session_state.quiz_questions = questions
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()
                    else:
                        st.error(T["quiz_error"])

        elif not st.session_state.quiz_submitted:
            questions = st.session_state.quiz_questions
            st.info(f"Answer all {len(questions)} {T['answer_all']}")
            st.markdown("<br>", unsafe_allow_html=True)

            for i, q in enumerate(questions):
                st.markdown(
                    f"""<div class="quiz-card"><div class="quiz-number">Question {i+1} of {len(questions)}</div><div class="quiz-q">{q['q']}</div></div>""",
                    unsafe_allow_html=True,
                )
                answer = st.radio(
                    f"q_{i}", q["options"], key=f"ans_{i}", label_visibility="collapsed"
                )
                if answer:
                    st.session_state.quiz_answers[i] = answer[0]
                st.markdown("<br>", unsafe_allow_html=True)

            answered = len(st.session_state.quiz_answers)
            total = len(questions)
            st.progress(answered / total, text=f"{answered}/{total} {T['answered']}")

            col_sub, col_reset = st.columns([2, 1])
            with col_sub:
                if st.button(
                    T["submit"], use_container_width=True, disabled=(answered < total)
                ):
                    st.session_state.quiz_submitted = True
                    st.rerun()
            with col_reset:
                if st.button(T["regenerate"], use_container_width=True):
                    st.session_state.quiz_questions = None
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.rerun()

        else:
            questions = st.session_state.quiz_questions
            answers = st.session_state.quiz_answers
            score = sum(
                1 for i, q in enumerate(questions) if answers.get(i, "") == q["answer"]
            )
            total = len(questions)
            percent = round((score / total) * 100)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(T["score"], f"{score}/{total}")
            with col2:
                st.metric(T["percentage"], f"{percent}%")
            with col3:
                grade = (
                    T["excellent"]
                    if percent >= 80
                    else T["good"] if percent >= 60 else T["keep_studying"]
                )
                st.metric(T["grade"], grade)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(T["answer_review"])

            for i, q in enumerate(questions):
                user_ans = answers.get(i, "?")
                correct = q["answer"]
                is_correct = user_ans == correct
                icon = "✅" if is_correct else "❌"
                border_color = "#10b981" if is_correct else "#ef4444"
                correct_opt = next(
                    (o for o in q["options"] if o.startswith(correct)), correct
                )
                user_opt = next(
                    (o for o in q["options"] if o.startswith(user_ans)), user_ans
                )

                st.markdown(
                    f"""
                <div style="background:#13151c;border-left:3px solid {border_color};border-radius:0 10px 10px 0;padding:14px 18px;margin-bottom:10px;">
                    <div style="font-size:0.75rem;color:#6b7280;margin-bottom:4px;">Q{i+1}</div>
                    <div style="font-weight:600;color:#f1f5f9;margin-bottom:8px;">{icon} {q['q']}</div>
                    <div style="font-size:0.85rem;color:#94a3b8;">{T["your_answer"]}: <span style="color:{'#10b981' if is_correct else '#ef4444'}">{user_opt}</span></div>
                    {"" if is_correct else f'<div style="font-size:0.85rem;color:#10b981;margin-top:2px;">{T["correct"]}: {correct_opt}</div>'}
                </div>
                """,
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # Quiz report download
            quiz_report = f"Quiz Report — {st.session_state.pdf_name}\n"
            quiz_report += f"Score: {score}/{total} ({percent}%)\n"
            quiz_report += "=" * 50 + "\n\n"
            for i, q in enumerate(questions):
                user_ans = answers.get(i, "?")
                quiz_report += f"Q{i+1}: {q['q']}\n"
                quiz_report += f"Your answer: {user_ans}  |  Correct: {q['answer']}\n\n"
            st.download_button(
                label=T["quiz_download"],
                data=quiz_report,
                file_name=f"quiz_report_{st.session_state.pdf_name.split(',')[0].replace('.pdf','')}.txt",
                mime="text/plain",
            )

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(T["retake"]):
                st.session_state.quiz_questions = None
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()

    elif st.session_state.mode == "Flashcards":
        st.markdown(
            f'<div class="hero-title">{T["flashcards"]}</div>', unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="hero-sub">{st.session_state.pdf_name} · {st.session_state.selected_model}</div>',
            unsafe_allow_html=True,
        )

        if st.session_state.flashcards is None:
            col_gen, _ = st.columns([2, 3])
            with col_gen:
                if st.button(T["gen_flashcards"], use_container_width=True):
                    with st.spinner(T["generating"]):
                        cards = generate_flashcards(
                            get_active_chunk(st.session_state.pdf_text)
                        )
                    if cards:
                        st.session_state.flashcards = cards
                        st.session_state.flashcard_idx = 0
                        st.session_state.flashcard_flipped = False
                        st.rerun()
                    else:
                        st.error(T["flashcard_error"])
        else:
            cards = st.session_state.flashcards
            idx = st.session_state.flashcard_idx
            card = cards[idx]
            face_text = (
                card["back"] if st.session_state.flashcard_flipped else card["front"]
            )
            face_color = "#10b981" if st.session_state.flashcard_flipped else "#6366f1"

            st.markdown(
                f"""
                <div style="background:#13151c;border:2px solid {face_color};border-radius:16px;
                            padding:50px 30px;min-height:220px;display:flex;align-items:center;
                            justify-content:center;text-align:center;margin-bottom:14px;">
                    <div style="font-size:1.2rem;color:#f1f5f9;font-weight:600;">{face_text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col_flip, col_info = st.columns([1, 2])
            with col_flip:
                if st.button(T["flip_card"], use_container_width=True):
                    st.session_state.flashcard_flipped = (
                        not st.session_state.flashcard_flipped
                    )
                    st.rerun()
            with col_info:
                st.caption(f"{T['card_of']} {idx + 1} / {len(cards)}")

            col_prev, col_next, col_regen = st.columns(3)
            with col_prev:
                if st.button(
                    T["prev_card"], use_container_width=True, disabled=(idx == 0)
                ):
                    st.session_state.flashcard_idx -= 1
                    st.session_state.flashcard_flipped = False
                    st.rerun()
            with col_next:
                if st.button(
                    T["next_card"],
                    use_container_width=True,
                    disabled=(idx == len(cards) - 1),
                ):
                    st.session_state.flashcard_idx += 1
                    st.session_state.flashcard_flipped = False
                    st.rerun()
            with col_regen:
                if st.button(T["regenerate"], use_container_width=True):
                    st.session_state.flashcards = None
                    st.session_state.flashcard_idx = 0
                    st.session_state.flashcard_flipped = False
                    st.rerun()
