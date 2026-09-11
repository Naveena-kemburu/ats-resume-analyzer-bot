# JobFit AI - ATS Resume Analyzer Bot

🤖 AI-powered Telegram bot that analyzes resumes against job descriptions using advanced language models.

## 🎯 Features

- **📊 ATS Score** - Comprehensive scoring (0-100) based on skills, experience, keywords, projects
- **💼 Job Match %** - Precise percentage match between resume and job requirements  
- **✅ Skill Analysis** - Detailed breakdown of matching, missing, and partial skills
- **📚 Learning Recommendations** - Personalized course suggestions for missing skills
- **🏆 Candidate Ranking** - Automatic ranking when analyzing multiple resumes
- **📄 Multi-Resume Support** - Analyze and compare multiple candidates

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get API Keys

**Telegram Bot:**
1. Open [@BotFather](https://t.me/botfather) in Telegram
2. Send `/newbot` and follow instructions
3. Copy the bot token

**Google Gemini API (FREE tier available):**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

### 3. Configure

Create `.env` file:
```env
TELEGRAM_BOT_TOKEN=your_telegram_token
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Run

```bash
python bot.py
```

## 📱 Usage

1. Start the bot: `/start`
2. Send job description (text)
3. Upload PDF resumes (one or multiple)
4. Analyze: `/analyze`
5. Get detailed reports and rankings!

## 🎨 Example Output

```
━━━━━━━━━━━━━━━━━━━━
🏆 RANK #1
👤 John Doe
━━━━━━━━━━━━━━━━━━━━

🎯 ATS SCORE
85/100
█████████████████░░░░

💼 JOB MATCH
78%
███████████████░░░░░

✅ MATCHING SKILLS
Python, FastAPI, PostgreSQL, Git

❌ MISSING SKILLS
🔴 Docker
🔴 AWS

📚 RECOMMENDED LEARNING
1. 🔥 Docker
   → Containers basics
   → Dockerfile creation
   → Docker Compose
```

## 🛠️ Tech Stack

- **Bot Framework:** python-telegram-bot
- **AI Models:** Google Gemini (Flash models)
- **PDF/DOCX Processing:** PyPDF2, python-docx
- **Language:** Python 3.10+

## 📋 Commands

| Command | Description |
|---------|-------------|
| `/start` | Start new analysis |
| `/help` | Show help |
| `/analyze` | Process resumes |
| `/reset` | Clear session |

## 🏗️ Project Structure

```
jobfit-ai-bot/
├── bot.py                  # Main Telegram bot
├── gemini_service.py       # Google Gemini AI service
├── file_extractor.py       # PDF/DOCX text extraction
├── formatter.py            # Output formatting
├── cleanup.py              # File cleanup
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── .env                    # API keys (gitignored)
└── temp/                   # Temporary files
```

<<<<<<< HEAD
## 🔒 Security

- API keys stored in `.env` (not committed)
- Temporary files auto-deleted after 24 hours
- No data stored permanently

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

MIT License - free for personal and commercial use

## 🙏 Acknowledgments

- [Google Gemini](https://ai.google.dev/) for AI API
- [Telegram Bot API](https://core.telegram.org/bots)
- Google's Gemini Flash models

=======
>>>>>>> 55ac328aecdd37400e599b0970935f672a2e56ca
---

**Made with ❤️ for recruiters and job seekers**
