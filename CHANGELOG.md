# Changelog

All notable changes to this project will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] - 2026-06-11

### Added
- PDF upload with text extraction via pdfplumber
- Chat mode with streaming AI responses (Ollama)
- Quiz mode generating 10 MCQ questions from PDF
- Model selector (llama3.2:3b / mistral:7b) in sidebar
- Dark theme UI with Space Grotesk font
- Quick prompt buttons (Summarise, Key Terms, Exam Tips)
- Score screen with answer review after quiz submission
- Progress bar during quiz generation
- Auto-retry (3 attempts) for quiz JSON parsing
- Dockerfile for containerization
- GitLab CI pipeline (lint + test stages)
- Full SpecKit documentation
