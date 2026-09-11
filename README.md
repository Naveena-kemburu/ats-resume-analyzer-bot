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

**Groq API (FREE):**
1. Visit [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up (free)
3. Create API key

### 3. Configure

Create `.env` file:
```env
TELEGRAM_BOT_TOKEN=your_telegram_token
GROQ_API_KEY=your_groq_api_key
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
- **AI Models:** Groq (Llama 3.3 70B)
- **PDF Processing:** PyPDF2
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
├── bot.py              # Main Telegram bot
├── groq_service.py     # AI analysis service
├── formatter.py        # Output formatting
├── cleanup.py          # File cleanup
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── .env               # API keys (gitignored)
└── temp/              # Temporary files
```

---

**Made with ❤️ for recruiters and job seekers**
