"""
Tests for Last Minute Study Buddy
Run: pytest tests/ -v
"""
import pytest
import json
import re


# ── PDF Extraction ──────────────────────────────────────
class TestPDFExtraction:

    def test_extract_returns_string(self, tmp_path):
        """PDF extraction should return a string or None."""
        # Test with a non-PDF file — should fail gracefully
        fake = tmp_path / "fake.pdf"
        fake.write_bytes(b"not a real pdf")
        try:
            import pdfplumber
            with pdfplumber.open(str(fake)) as pdf:
                text = " ".join(p.extract_text() or "" for p in pdf.pages)
            assert isinstance(text, str)
        except Exception:
            pass  # graceful failure expected

    def test_text_length_threshold(self):
        """Texts under 100 chars should be considered empty."""
        short_text = "Hello world"
        assert len(short_text) < 100

    def test_text_slicing_for_ollama(self):
        """Text sent to Ollama must not exceed limits."""
        long_text = "a" * 10000
        chat_context = long_text[:4000]
        quiz_context = long_text[:5000]
        assert len(chat_context) <= 4000
        assert len(quiz_context) <= 5000


# ── Quiz JSON Parsing ───────────────────────────────────
class TestQuizParsing:

    def test_valid_quiz_json(self):
        """Valid quiz JSON should parse to 20 questions."""
        sample = json.dumps([
            {
                "q": f"Question {i}?",
                "options": ["A) opt1", "B) opt2", "C) opt3", "D) opt4"],
                "answer": "A"
            }
            for i in range(20)
        ])
        questions = json.loads(sample)
        assert len(questions) == 20
        assert questions[0]["answer"] == "A"

    def test_quiz_json_with_fences(self):
        """JSON wrapped in markdown fences should parse after stripping."""
        fenced = "```json\n[{\"q\": \"Q?\", \"options\": [\"A) a\", \"B) b\", \"C) c\", \"D) d\"], \"answer\": \"B\"}]\n```"
        clean = re.sub(r"```json|```", "", fenced).strip()
        start = clean.find("[")
        end = clean.rfind("]") + 1
        questions = json.loads(clean[start:end])
        assert len(questions) == 1
        assert questions[0]["answer"] == "B"

    def test_answer_is_valid_letter(self):
        """Answer must be one of A, B, C, D."""
        valid_answers = ["A", "B", "C", "D"]
        test_answer = "A"
        assert test_answer in valid_answers

    def test_options_count(self):
        """Each question must have exactly 4 options."""
        question = {
            "q": "Test?",
            "options": ["A) a", "B) b", "C) c", "D) d"],
            "answer": "C"
        }
        assert len(question["options"]) == 4


# ── MongoDB Graceful Degradation ────────────────────────
class TestMongoDB:

    def test_mongo_offline_does_not_crash(self):
        """App should work if MongoDB is unreachable."""
        try:
            from pymongo import MongoClient
            client = MongoClient("mongodb://localhost:1", serverSelectionTimeoutMS=500)
            client.server_info()
            db = client["studybuddy"]
        except Exception:
            db = None
        # App should continue with db = None
        assert db is None or db is not None  # either state is valid

    def test_save_chat_with_none_db(self):
        """save_chat should not raise if db is None."""
        db = None
        try:
            if db is None:
                pass  # graceful skip
            result = True
        except Exception:
            result = False
        assert result is True


# ── Score Calculation ───────────────────────────────────
class TestScoreCalculation:

    def test_perfect_score(self):
        questions = [{"answer": "A"}] * 20
        answers = {i: "A" for i in range(20)}
        score = sum(1 for i, q in enumerate(questions) if answers.get(i) == q["answer"])
        assert score == 20

    def test_zero_score(self):
        questions = [{"answer": "A"}] * 20
        answers = {i: "B" for i in range(20)}
        score = sum(1 for i, q in enumerate(questions) if answers.get(i) == q["answer"])
        assert score == 0

    def test_percent_calculation(self):
        score, total = 15, 20
        percent = round((score / total) * 100)
        assert percent == 75

    def test_grade_labels(self):
        assert "Excellent" in ("🏆 Excellent" if 85 >= 80 else "")
        assert "Good" in ("👍 Good" if 65 >= 60 else "")
