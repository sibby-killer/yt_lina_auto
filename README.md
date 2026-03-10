# Ashley MindShift — Dark Psychology Automation 🌑

Fully automated YouTube Shorts + Long-Form video engine for the **Ashley MindShift** brand.  
Covers dark psychology, manipulation awareness, relationships, attraction, confidence, and mind games.

---

## 🚀 Overview

A two-pipeline content engine that runs entirely on GitHub Actions:

| Pipeline | File | Output | Schedule |
|---|---|---|---|
| **Short-Form** | `main.py` | 60–90 sec YouTube Shorts / Facebook Reels / TikTok | 5× daily |
| **Long-Form** | `long_main.py` | 8–10 min YouTube videos | 1× daily |

Both pipelines are fully automated:  
`AI Script → Voiceover → B-Roll → Video Assembly → Upload → Pin Comment → Log`

---

## 🧠 AI Content Engine (`core/ai_script.py`)

The brain of the entire system. Powered by **Groq (llama-3.3-70b-versatile)** with automatic fallback to `llama-3.1-70b-versatile`.

### Short-Form Scripts
- **Duration:** 1 min 20 sec – 1 min 50 sec (200–280 words)
- **5-Part Structure:** Hook → Psychology Label → Deep Explanation → Consequence → Urgency CTA
- **Gold-standard tone:** Conversational, dark, mysterious — like whispering secrets at midnight
- **Accurate psychology:** Concepts are matched precisely to the topic (no random terminology drops)
- **10 rules** enforced for human conversational flow
- Returns JSON with: `title`, `description`, `script`, `topic_used`, `psychology_concept`, `pinned_comment`, `b_roll_keywords`

### Long-Form Scripts
- **Duration:** 8–10 minutes (1500–2000 words, minimum enforced)
- **6-Section Structure:** Cinematic Opening → Hidden Foundation → 5 Pillars → Case Study → Practical Exercise → Final Revelation
- **Word count validation** with automatic retry if script comes back under 1200 words
- Returns JSON with: `title`, `description`, `script`, `topic_used`, `word_count`, `pinned_comment`, `b_roll_keywords`

### Topic System
- **100 pre-loaded viral topics** across 7 categories (social power, manipulation, attraction, self-protection, body language, emotional intelligence, confidence)
- Smart deduplication — never repeats a topic
- When all 100 are exhausted, generates fresh unique topics via AI
- Reset supported via `reset_used_topics()`

---

## 📋 Features

### Content
- ✅ Unique AI-generated pinned comment per video (topic-specific, drives real replies)
- ✅ SEO-optimized YouTube descriptions (Shorts format + Long-Form format with timestamps)
- ✅ Professional Pexels credits auto-inserted via `{{CREDITS_PLACEHOLDER}}` system
- ✅ Hashtag set included in every output

### Distribution
- ✅ **YouTube** — auto-upload with playlist management
- ✅ **Facebook Reels / Video** — auto-upload
- ✅ **TikTok** — auto-upload via cookies
- ✅ **Supabase** — video logging, status tracking, upload ID sync

### Auto-Comment System (`core/auto_comment.py`)
- Posts a **unique AI-generated pinned comment** on every video after upload
- Falls back to a curated 10-comment pool if AI comment is unavailable
- Zero generic/spammy comments — every comment drives real engagement

### Credits System
- `format_credits(credit_list)` — deduplicates and formats Pexels creator names cleanly
- `insert_credits_into_description(description, credit_list)` — replaces `{{CREDITS_PLACEHOLDER}}` in the AI description with properly formatted credits
- Credits are collected at download time and inserted after video assembly

---

## 🗂 Project Structure

```
AutoVidEmpire_V2/
├── main.py                    # Short-form pipeline (Shorts/Reels/TikTok)
├── long_main.py               # Long-form pipeline (YouTube 8-10min)
├── config.py                  # API key loader from .env
├── requirements.txt
├── .env                       # Local secrets (never committed)
│
├── core/
│   ├── ai_script.py           # AI script + topic engine + credit utilities
│   ├── auto_comment.py        # Pinned comment bot with fallback pool
│   ├── tts.py                 # Edge-TTS voiceover (ChristopherNeural)
│   ├── yt_scraper.py          # TikTok B-roll downloader (short-form)
│   ├── pexels_scraper.py      # Pexels B-roll downloader (long-form)
│   ├── video_editor.py        # FFmpeg video assembly
│   ├── youtube_uploader.py    # YouTube Data API v3 uploader
│   ├── facebook_uploader.py   # Facebook Graph API uploader
│   ├── tiktok_uploader.py     # TikTok uploader
│   ├── supabase_db.py         # Supabase logging client
│   └── SCRIPT_GUIDE.md        # Script writing reference guide
│
└── .github/
    └── workflows/             # GitHub Actions automation
```

---

## ⚙️ Environment Variables

Add these as **GitHub Secrets** or in your local `.env` file:

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | AI script generation |
| `YOUTUBE_CLIENT_ID` | ✅ | YouTube OAuth |
| `YOUTUBE_CLIENT_SECRET` | ✅ | YouTube OAuth |
| `YOUTUBE_REFRESH_TOKEN` | ✅ | YouTube OAuth (run `refresh_token.py` locally) |
| `YOUTUBE_PLAYLIST_ID` | Optional | Auto-created if not set |
| `PEXELS_API_KEY` | ✅ | Long-form B-roll downloads |
| `FACEBOOK_PAGE_ID` | Optional | Facebook distribution |
| `FACEBOOK_PAGE_ACCESS_TOKEN` | Optional | Facebook distribution |
| `TIKTOK_COOKIES_PATH` | Optional | TikTok upload (defaults to `tiktok_cookies.txt`) |
| `SUPABASE_URL` | ✅ | Video logging |
| `SUPABASE_KEY` | ✅ | Video logging |

---

## 📦 Setup & Deployment

### Local Setup
```bash
pip install -r requirements.txt
cp .env.example .env   # Fill in your API keys
python refresh_token.py  # Authenticate YouTube once
python main.py           # Test a short-form run
python long_main.py      # Test a long-form run
```

### GitHub Actions (Cloud Automation)
1. Push this repo to GitHub
2. Add all environment variables as **GitHub Secrets** (`Settings → Secrets and variables → Actions`)
3. Enable **GitHub Actions** — workflows run automatically on schedule

---

## 🔧 Key Utility Functions

```python
# AI Script Generation
from core.ai_script import generate_video_content, generate_long_video_content

# Topic Management
from core.ai_script import get_next_topic, get_status, reset_used_topics

# Credits
from core.ai_script import format_credits, insert_credits_into_description

# Comments
from core.auto_comment import post_pinned_comment
```

---

*Ashley MindShift — The shadows of the mind revealed.*
