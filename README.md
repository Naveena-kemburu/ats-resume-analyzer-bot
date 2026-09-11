# JobFit AI - Telegram Resume Matcher Bot

AI-powered ATS resume analysis bot that compares resumes against job descriptions using Google's Gemini AI.

## Features

- **ATS Score** - Comprehensive scoring based on skills, experience, keywords, projects, and structure
- **Job Match %** - Precise percentage match between resume and job requirements
- **Skill Analysis** - Detailed breakdown of matching, missing, and partial skills
- **Learning Recommendations** - Personalized course suggestions for missing skills
- **Candidate Ranking** - Automatic ranking of multiple candidates
- **Multi-Resume Support** - Analyze multiple resumes in one session

## Quick Start

### Prerequisites

- Python 3.8+
- Telegram account
- Google Gemini API key

### Installation

1. **Clone and navigate to the project:**
```bash
git clone <your-repo>
cd jobfit-ai
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure your API keys in `.env`:**
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

### Running the Bot

```bash
python bot.py
```

You should see:
```
INFO - Bot started successfully (Gemini enabled)!
```

## How to Use

### Step 1: Start a new session
Open your bot in Telegram and send:
```
/start
```

### Step 2: Send Job Description
You can provide the Job Description in three ways:
- Upload a Word document (`.docx`)
- Upload a PDF document (`.pdf`)
- Or paste the text directly

### Step 3: Upload Resumes
Upload one or multiple resumes (`.pdf` or `.docx` files).

### Step 4: Analyze
When ready, send:
```
/analyze
```

### Step 5: Review Results
The bot will analyze each resume against the Job Description and provide:
- Individual candidate reports with ATS score, match %, strengths, weaknesses, and learning recommendations
- Final ranking comparing all candidates

## Commands

| Command | Description |
|---|---|
| `/start` | Start new analysis session |
| `/help` | Show usage instructions |
| `/status` | View currently loaded JD and queued resumes |
| `/jd` | View current Job Description preview and source |
| `/clear` | Clear uploaded resumes while keeping active JD |
| `/analyze` | Process uploaded resumes |
| `/reset` | Clear current session |

## Analysis Output

For each candidate, you will receive:
- ATS Score (0-100)
- Job Match Percentage
- Matching skills
- Missing skills (Critical / Important / Nice-to-have)
- Skill breakdown with percentages
- Strengths and areas to improve
- Prioritized learning recommendations

## Project Structure

```
jobfit-ai/
├── bot.py                 # Main Telegram bot
├── gemini_service.py      # Gemini API integration
├── file_extractor.py      # PDF & DOCX text extraction
├── formatter.py           # Output formatting
├── cleanup.py             # File management
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── .env                   # API keys (not in git)
├── .env.example           # Template
├── .gitignore             # Git ignore rules
└── temp/                  # Temporary file storage
```

## Security Notes

- API keys are stored in `.env` (never commit this file)
- Temporary files are auto-deleted after 24 hours
- File uploads are processed securely in local temporary storage
