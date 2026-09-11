import sys
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

import logging
import os
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN, TEMP_DIR, GEMINI_API_KEY
from gemini_service import GeminiService

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store user sessions
user_sessions = {}

def get_ai_service():
    """Select Google Gemini AI service"""
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured in .env file.")
    return GeminiService()

def _init_user_session(user_id: int):
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            'job_description': None,
            'job_description_file': None,
            'resumes': []
        }
    return user_sessions[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_id = update.effective_user.id
    logger.info(f"User {user_id} triggered /start")
    user_sessions[user_id] = {
        'job_description': None,
        'job_description_file': None,
        'resumes': []
    }
    
    welcome_message = """Welcome to JobFit AI - Resume Matcher (Powered by Gemini)

I analyze and compare candidate resumes against a Job Description.

What I analyze:
- ATS Score & Job Match Percentage
- Exact Matching Skills
- Missing Critical Skills
- Recommended Learning Paths
- Candidate Ranking

How to start:
1. Send the Job Description (upload .docx/.pdf file or paste text directly).
2. Upload candidate resumes (.pdf or .docx).
3. Type /analyze to process.

Type /help to view all available commands."""
    
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """How to use JobFit AI:

1. Send Job Description (upload .docx / .pdf file OR paste text)
2. Upload resumes (one or multiple .pdf or .docx files)
3. Type /analyze to process and rank candidates

Available Commands:
/start   - Start a fresh session
/help    - Show this help guide
/status  - View active JD and queued resumes
/jd      - View the currently loaded Job Description
/setjd   - Replace active Job Description
/clear   - Clear uploaded resumes (keeps current JD)
/analyze - Run ATS analysis on all queued resumes
/reset   - Reset everything (clears JD and resumes)"""
    
    await update.message.reply_text(help_text)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command to check current session state"""
    user_id = update.effective_user.id
    session = user_sessions.get(user_id)
    
    if not session or not session.get('job_description'):
        await update.message.reply_text(
            "Current Status:\n"
            "- Job Description: None loaded\n"
            "- Resumes queued: 0\n\n"
            "Please send a .docx, .pdf, or paste text to set the Job Description."
        )
        return
    
    jd_file = session.get('job_description_file') or 'Pasted Text'
    resumes = session.get('resumes', [])
    
    resume_list_str = ""
    if resumes:
        resume_list_str = "\n".join([f"  {idx}. {r['name']}" for idx, r in enumerate(resumes, 1)])
    else:
        resume_list_str = "  (None uploaded yet)"
        
    await update.message.reply_text(
        f"CURRENT SESSION STATUS:\n\n"
        f"Active Job Description: {jd_file}\n"
        f"Queued Resumes ({len(resumes)}):\n"
        f"{resume_list_str}\n\n"
        f"Commands:\n"
        f"- /analyze : Run analysis\n"
        f"- /clear   : Clear resumes list\n"
        f"- /reset   : Clear everything"
    )

async def show_jd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /jd command to view the currently loaded Job Description"""
    user_id = update.effective_user.id
    session = user_sessions.get(user_id)
    
    if not session or not session.get('job_description'):
        await update.message.reply_text(
            "[!] No Job Description loaded yet.\n"
            "Please upload a .docx or .pdf file, or paste text to set it."
        )
        return
    
    jd_file = session.get('job_description_file') or 'Pasted Text'
    jd_text = session.get('job_description', '')
    preview = jd_text[:500] + ("..." if len(jd_text) > 500 else "")
    
    await update.message.reply_text(
        f"CURRENT JOB DESCRIPTION:\n"
        f"File/Source: {jd_file}\n"
        f"Length: {len(jd_text)} characters\n\n"
        f"Preview:\n{preview}\n\n"
        f"Send resumes (.pdf or .docx) to analyze, or use /setjd or /reset to change JD."
    )

async def set_jd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /setjd command to clear current JD and prompt for new one"""
    user_id = update.effective_user.id
    session = _init_user_session(user_id)
    
    session['job_description'] = None
    session['job_description_file'] = None
    
    await update.message.reply_text(
        "Job Description cleared.\n\n"
        "Please send the new Job Description by uploading a .docx/.pdf file or pasting the text directly."
    )

async def clear_resumes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clear command to remove queued resumes while preserving JD"""
    user_id = update.effective_user.id
    session = _init_user_session(user_id)
    
    count = len(session['resumes'])
    session['resumes'] = []
    
    await update.message.reply_text(
        f"Cleared {count} resume(s) from the queue.\n"
        f"Your Job Description is still active. Send new resumes to analyze, then type /analyze."
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /reset command"""
    user_id = update.effective_user.id
    logger.info(f"User {user_id} triggered /reset")
    
    from cleanup import cleanup_user_session
    cleanup_user_session(user_id)
    
    user_sessions[user_id] = {
        'job_description': None,
        'job_description_file': None,
        'resumes': []
    }
    await update.message.reply_text("Session reset. Send me a new Job Description (.docx, .pdf, or text) to start.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages (job description as text)"""
    user_id = update.effective_user.id
    session = _init_user_session(user_id)
    text = update.message.text.strip()
    
    logger.info(f"User {user_id} sent text message (length={len(text)}): {text[:80]}...")
    
    if not session['job_description']:
        # Require meaningful length for Job Description to avoid accidental conversational text
        if len(text) < 40:
            await update.message.reply_text(
                "[!] That text seems too short for a Job Description.\n\n"
                "Please paste a complete Job Description including role title, responsibilities, "
                "and required skills, or upload a .docx/.pdf file."
            )
            return
            
        session['job_description'] = text
        first_line = text.splitlines()[0][:50].strip()
        session['job_description_file'] = f"Pasted Text: {first_line}"
        logger.info(f"User {user_id} set Job Description via text ({len(text)} chars)")
        
        await update.message.reply_text(
            f"Job Description received ({len(text)} characters).\n\n"
            "Now send candidate resumes (PDF or Word .docx files).\n"
            "You can upload multiple resumes.\n\n"
            "When finished, type /analyze"
        )
    else:
        await update.message.reply_text(
            f"Job Description is already set ({session.get('job_description_file')}).\n\n"
            "To analyze, send PDF or DOCX resumes and type /analyze.\n"
            "To view the active JD: type /jd\n"
            "To replace the JD: type /setjd or /reset"
        )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document uploads for both Job Description and Resumes (PDF & DOCX)"""
    user_id = update.effective_user.id
    session = _init_user_session(user_id)
    
    document = update.message.document
    if not document or not document.file_name:
        await update.message.reply_text("[!] Please upload a valid document.")
        return
    
    file_name = document.file_name
    lower_name = file_name.lower()
    from file_extractor import is_supported_file, extract_text_from_file
    
    if not is_supported_file(file_name):
        await update.message.reply_text(
            "[!] Unsupported file format.\n"
            "Please upload files in Word (.docx) or PDF (.pdf) format."
        )
        return
    
    looks_like_jd = any(k in lower_name for k in ['jd', 'job_description', 'job description', 'job-description', 'jobdesc'])
    
    # 1. If Job Description is not set:
    if not session['job_description']:
        await update.message.reply_text(f"Reading Job Description from {file_name}...")
        
        file = await context.bot.get_file(document.file_id)
        file_path = os.path.join(TEMP_DIR, f"{user_id}_jd_{file_name}")
        await file.download_to_drive(file_path)
        
        extracted_text = extract_text_from_file(file_path)
        
        if not extracted_text or len(extracted_text.strip()) < 20:
            await update.message.reply_text(
                f"[!] Could not extract readable text from {file_name}.\n"
                "Please ensure the file contains selectable text, or paste the text directly."
            )
            return
        
        session['job_description'] = extracted_text
        session['job_description_file'] = file_name
        logger.info(f"User {user_id} loaded Job Description from file: {file_name} ({len(extracted_text)} chars)")
        
        hint = ""
        if any(w in lower_name for w in ['resume', 'cv', 'curriculum']):
            hint = "\n\n[Notice]: This was loaded as your Job Description. If this was meant to be a resume, type /reset first."

        await update.message.reply_text(
            f"Job Description loaded from {file_name}.\n\n"
            "Now upload candidate resumes (.pdf or .docx).\n"
            "You can upload multiple resumes.\n\n"
            f"When finished, type /analyze{hint}"
        )
        return
    
    # 2. If Job Description is already set, but user uploads another file that looks like a JD:
    if looks_like_jd:
        await update.message.reply_text(
            f"[Notice]: Your active Job Description is already '{session.get('job_description_file')}'.\n"
            f"'{file_name}' appears to be a Job Description. If you want to replace your active Job Description, type /setjd or /reset.\n\n"
            f"Adding '{file_name}' as a candidate resume for now."
        )
    
    # Download and queue candidate resume
    file = await context.bot.get_file(document.file_id)
    file_path = os.path.join(TEMP_DIR, f"{user_id}_{file_name}")
    await file.download_to_drive(file_path)
    
    session['resumes'].append({
        'name': file_name,
        'path': file_path
    })
    
    resume_count = len(session['resumes'])
    logger.info(f"User {user_id} uploaded resume #{resume_count}: {file_name}")
    
    await update.message.reply_text(
        f"Resume {resume_count} received: {file_name}\n\n"
        f"Total resumes queued: {resume_count}\n"
        f"Type /analyze when ready, or /status to review queued resumes."
    )

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /analyze command"""
    user_id = update.effective_user.id
    
    if user_id not in user_sessions:
        await update.message.reply_text("Please use /start first.")
        return
    
    session = user_sessions[user_id]
    
    if not session['job_description']:
        await update.message.reply_text("[!] No Job Description found. Please upload a .docx/.pdf file or paste text first.")
        return
    
    if not session['resumes']:
        await update.message.reply_text("[!] No resumes uploaded. Please upload at least one PDF or DOCX resume.")
        return
    
    resume_count = len(session['resumes'])
    jd_source = session.get('job_description_file') or 'Pasted Text'
    logger.info(f"User {user_id} started analysis of {resume_count} resumes against JD ({jd_source})")
    
    await update.message.reply_text(
        f"Analyzing {resume_count} resume(s) against Job Description:\n"
        f"'{jd_source}'\n\n"
        f"Processing with Gemini AI..."
    )
    
    try:
        from formatter import format_candidate_result, format_ranking_summary
        
        try:
            ai_service = get_ai_service()
        except Exception as e:
            await update.message.reply_text(
                f"[ERROR] AI Service Error: {str(e)}\n\n"
                f"Please ensure GEMINI_API_KEY is configured properly in .env."
            )
            return
            
        results = []
        
        # Analyze each resume
        for idx, resume in enumerate(session['resumes'], 1):
            try:
                await update.message.reply_text(f"[{idx}/{resume_count}] Analyzing {resume['name']}...")
                
                result = ai_service.analyze_resume(
                    job_description=session['job_description'],
                    resume_path=resume['path'],
                    resume_name=resume['name']
                )
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error analyzing resume {resume['name']}: {str(e)}")
                results.append({
                    'error': True,
                    'message': str(e),
                    'resume_name': resume['name']
                })
        
        # Rank candidates
        ranked_results = ai_service.rank_candidates(results)
        
        # Send individual results
        for idx, result in enumerate(ranked_results, 1):
            formatted = format_candidate_result(result, rank=idx, jd_title=jd_source)
            if len(formatted) > 4096:
                chunks = [formatted[i:i+4096] for i in range(0, len(formatted), 4096)]
                for chunk in chunks:
                    await update.message.reply_text(chunk)
            else:
                await update.message.reply_text(formatted)
        
        # Send error results if any
        error_results = [r for r in results if r.get('error')]
        for error_result in error_results:
            formatted = format_candidate_result(error_result, jd_title=jd_source)
            await update.message.reply_text(formatted)
        
        # Send ranking summary if more than 1 candidate
        if len(ranked_results) > 1:
            summary = format_ranking_summary(ranked_results)
            await update.message.reply_text(summary)
        
        await update.message.reply_text(
            "Analysis complete.\n\n"
            "Next steps:\n"
            "- Type /clear to clear these resumes and analyze a new batch against the same JD\n"
            "- Type /setjd to change the Job Description\n"
            "- Type /reset to clear everything and start fresh\n"
            "- Or upload additional resumes and type /analyze"
        )
        
    except Exception as e:
        logger.error(f"Error in analyze command: {str(e)}")
        from formatter import format_error_message
        await update.message.reply_text(format_error_message(str(e)))

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by Updates."""
    logger.error("Exception while handling an update:", exc_info=context.error)

def main():
    """Start the bot"""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in .env file")
        return
    
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not found in .env file")
        return
    
    from cleanup import cleanup_old_files
    cleanup_old_files(max_age_hours=24)
    
    application = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .read_timeout(30)
        .write_timeout(30)
        .connect_timeout(30)
        .pool_timeout(30)
        .build()
    )
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("jd", show_jd))
    application.add_handler(CommandHandler("setjd", set_jd))
    application.add_handler(CommandHandler("clear", clear_resumes))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(CommandHandler("analyze", analyze))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    application.add_error_handler(error_handler)
    
    logger.info("Bot started successfully (Gemini enabled)!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
