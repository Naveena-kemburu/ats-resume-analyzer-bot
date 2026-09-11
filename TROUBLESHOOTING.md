# Troubleshooting Guide

## Installation Issues

### Problem: `pip install` fails
**Solutions:**
1. Update pip:
   ```bash
   python -m pip install --upgrade pip
   ```

2. Use Python 3.8+:
   ```bash
   python --version  # Check version
   ```

3. Install in virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

### Problem: `google-generativeai` import error
**Solutions:**
1. Reinstall the package:
   ```bash
   pip uninstall google-generativeai
   pip install google-generativeai
   ```

2. Check Python version (requires 3.8+)

### Problem: `python-telegram-bot` version conflicts
**Solutions:**
- Use exact version:
  ```bash
  pip install python-telegram-bot==21.0
  ```

## Configuration Issues

### Problem: Bot doesn't start - Token error
**Symptoms:**
```
ERROR - TELEGRAM_BOT_TOKEN not found!
```

**Solutions:**
1. Check `.env` file exists in project root
2. Verify format (no spaces):
   ```
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   GEMINI_API_KEY=AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ
   ```
3. No quotes around values
4. File named exactly `.env` (not `.env.txt`)

### Problem: Gemini API key invalid
**Symptoms:**
```
ERROR - API key not valid
```

**Solutions:**
1. Get new key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Check key has no extra spaces
3. Verify API is enabled for your account
4. Check billing if required

### Problem: `temp/` directory errors
**Solutions:**
1. Create manually:
   ```bash
   mkdir temp
   ```
2. Check permissions:
   ```bash
   chmod 755 temp
   ```

## Runtime Issues

### Problem: Bot not responding in Telegram
**Symptoms:**
- No response to `/start`
- Messages sent but no reply

**Solutions:**
1. Check bot is running:
   - Should see "Bot started!" in console
   - No errors in console output

2. Verify bot token:
   - Search for your bot in Telegram by username
   - Ensure you're messaging the correct bot

3. Restart bot:
   ```bash
   # Stop with Ctrl+C
   python bot.py
   ```

4. Check internet connection

5. Telegram API might be down - check status

### Problem: Analysis fails with error
**Symptoms:**
```
❌ ERROR
Something went wrong: [error message]
```

**Common Causes & Solutions:**

1. **PDF too large (>20MB)**
   - Compress PDF
   - Split into smaller files
   - Use online compression tools

2. **PDF is password protected**
   - Remove password protection
   - Resave as unprotected PDF

3. **PDF is corrupted**
   - Try opening PDF locally
   - Regenerate PDF from source

4. **Gemini API rate limit**
   - Wait a few minutes
   - Reduce number of resumes
   - Check API quota

5. **Network timeout**
   - Check internet connection
   - Try again
   - Reduce resume size

### Problem: Wrong or incomplete analysis
**Symptoms:**
- Missing skills not detected
- Scores seem random
- Incomplete output

**Solutions:**
1. Ensure job description is detailed:
   - List all required skills clearly
   - Include experience requirements
   - Specify technical requirements

2. Check PDF quality:
   - Text should be selectable (not scanned image)
   - Clear formatting
   - No special characters/encoding issues

3. Try rephrasing job description:
   - Use bullet points
   - Separate required vs preferred skills
   - Be specific about technologies

### Problem: Multiple resumes not processing
**Symptoms:**
- Only first resume analyzed
- Second resume causes error

**Solutions:**
1. Upload resumes one at a time
2. Wait for confirmation between uploads
3. Check all PDFs are valid format
4. Restart session with `/reset` if stuck

### Problem: Bot crashes during analysis
**Symptoms:**
- Bot stops responding
- Console shows traceback error

**Solutions:**
1. Check error message in console
2. Common fixes:
   - Restart bot
   - Clear temp folder
   - Check available disk space
   - Verify all dependencies installed

3. Enable debug logging:
   ```python
   # In bot.py, change level to DEBUG
   logging.basicConfig(level=logging.DEBUG)
   ```

## File System Issues

### Problem: Permission denied errors
**Solutions:**
1. Run with appropriate permissions
2. Check directory ownership
3. On Windows, run as Administrator if needed

### Problem: Temp files not deleting
**Solutions:**
1. Manual cleanup:
   ```bash
   rm -rf temp/*  # Linux/Mac
   del temp\*     # Windows
   ```

2. Restart bot (cleanup runs on startup)

3. Check cleanup function in `cleanup.py`

### Problem: Disk space full
**Solutions:**
1. Clean temp directory
2. Remove old log files
3. Free up system space
4. Reduce retention time in cleanup settings

## Telegram-Specific Issues

### Problem: File download fails
**Symptoms:**
```
ERROR - Failed to download file
```

**Solutions:**
1. Check file size (<20MB limit)
2. Ensure stable internet
3. Try uploading file again
4. Check file isn't corrupted

### Problem: Messages not formatting correctly
**Symptoms:**
- Text appears as plain text
- No emojis
- Broken layout

**Solutions:**
1. Update Telegram app
2. Check if special characters are supported
3. Verify bot is sending correct format
4. May be Telegram client issue (try different device)

## Gemini API Issues

### Problem: Rate limit exceeded
**Symptoms:**
```
ERROR - Resource exhausted
```

**Solutions:**
1. Wait before next request (usually 1 minute)
2. Reduce concurrent analyses
3. Check API quotas in Google AI Studio
4. Consider upgrading API plan if needed

### Problem: Response timeout
**Solutions:**
1. Retry the analysis
2. Reduce resume complexity
3. Check internet speed
4. May be temporary API issue

### Problem: Invalid JSON response
**Symptoms:**
- Analysis completes but shows error
- Incomplete results

**Solutions:**
1. Usually temporary - retry
2. Check Gemini API status
3. Simplify job description
4. Report persistent issues

## Performance Issues

### Problem: Analysis takes too long
**Expected:** 5-15 seconds per resume

**If slower:**
1. Check internet speed
2. Reduce PDF file sizes
3. Simplify job descriptions
4. May be API load issue (peak times)

### Problem: Bot uses too much memory
**Solutions:**
1. Restart bot regularly
2. Clear temp files
3. Reduce session data storage
4. Check for memory leaks (report issue)

## Common Error Messages

### `ModuleNotFoundError: No module named 'telegram'`
**Fix:**
```bash
pip install python-telegram-bot
```

### `ModuleNotFoundError: No module named 'google.generativeai'`
**Fix:**
```bash
pip install google-generativeai
```

### `FileNotFoundError: [Errno 2] No such file or directory: '.env'`
**Fix:**
Create `.env` file in project root

### `ValueError: Invalid token`
**Fix:**
Check token format in `.env` file

## Debug Mode

Enable detailed logging for troubleshooting:

```python
# Add to bot.py at the top
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Change to DEBUG
)
```

This will show:
- All API calls
- File operations
- Detailed error traces
- Telegram bot events

## Getting Help

If issues persist:

1. **Check logs:**
   - Console output
   - Error messages
   - Stack traces

2. **Try minimal test:**
   - Fresh start with `/start`
   - Simple 1-line job description
   - Single small PDF

3. **Verify setup:**
   - Dependencies installed
   - Tokens valid
   - Internet working
   - Python version correct

4. **Report issue:**
   - Error message
   - Steps to reproduce
   - Python version
   - Operating system
   - What you tried

## Quick Fixes Checklist

```
[ ] Restart bot
[ ] Check .env file
[ ] Verify internet connection
[ ] Clear temp directory
[ ] Reinstall dependencies
[ ] Update Python packages
[ ] Try different PDF
[ ] Simplify job description
[ ] Check API quotas
[ ] Review console logs
```

## Still Not Working?

1. Delete everything and start fresh:
   ```bash
   # Backup .env first!
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python bot.py
   ```

2. Test components separately:
   - Test Gemini API with simple script
   - Test Telegram bot without analysis
   - Test PDF reading locally

3. Check system requirements:
   - Python 3.8+
   - 500MB free disk space
   - Stable internet (>1Mbps)
   - Modern operating system

---

**Most issues are solved by: checking .env, restarting bot, or updating dependencies!**
