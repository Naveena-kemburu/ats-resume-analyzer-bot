# Testing Guide for JobFit AI

## Quick Test Checklist

### Setup Test
- [ ] Created `.env` file with valid tokens
- [ ] Installed dependencies
- [ ] Bot starts without errors
- [ ] Can find bot in Telegram search

### Basic Flow Test
- [ ] `/start` command works
- [ ] `/help` command shows instructions
- [ ] `/jd` shows current Job Description preview and source
- [ ] Job description accepted via text, PDF (`.pdf`), or Word document (`.docx`)
- [ ] Resume upload works for both PDF and DOCX files
- [ ] Multiple resumes can be uploaded
- [ ] `/analyze` processes successfully
- [ ] Results are properly formatted
- [ ] `/reset` clears session

### Error Handling Test
- [ ] `/analyze` before job description shows error
- [ ] `/analyze` without resumes shows error
- [ ] Unsupported files (e.g. `.exe`, `.jpg`) are rejected
- [ ] Large files (>20MB) are handled

## Test Scenarios

### Scenario 1: Single Resume Analysis

1. Send `/start`
2. Paste this job description:
```
Backend Developer - Python

We are seeking a talented Backend Developer with expertise in Python and modern web frameworks.

Required Skills:
- Python 3.8+
- FastAPI or Django
- PostgreSQL
- RESTful API design
- Git version control

Preferred Skills:
- Docker
- AWS or cloud experience
- Redis
- CI/CD pipelines

Experience: 2-4 years in backend development
```

3. Upload a test PDF resume
4. Send `/analyze`
5. Verify output includes:
   - ATS score (0-100)
   - Job match percentage
   - Matching skills list
   - Missing skills with importance
   - Learning recommendations

### Scenario 2: Multiple Resume Comparison

1. Send `/start`
2. Paste job description
3. Upload 3 different resume PDFs
4. Send `/analyze`
5. Verify:
   - All 3 resumes are processed
   - Individual reports for each
   - Final ranking summary
   - Candidates ranked by score

### Scenario 3: Session Reset

1. Complete a full analysis
2. Send `/reset`
3. Verify session is cleared
4. Start new analysis with different JD
5. Verify old data doesn't persist

## Expected Output Format

### Individual Candidate Report
```
------------------------------------
RANK #1
Candidate: John Doe
------------------------------------

Resume File: john_doe_resume.pdf

ATS SCORE
85/100
[=================   ]

JOB MATCH
78%
[===============     ]

MATCHING SKILLS:
Python, FastAPI, Git, REST APIs, PostgreSQL

MISSING SKILLS:
  Critical:
  - Docker
  - AWS
  Important:
  - Redis

SKILL BREAKDOWN:
  Python          [==========] 100%
  FastAPI         [==========] 100%
  PostgreSQL      [==========] 100%
  Docker          [          ] 0%
  AWS             [          ] 0%

STRENGTHS:
  - Strong Python skills
  - REST API experience
  - Database knowledge

AREAS TO IMPROVE:
  - No DevOps experience
  - Missing cloud skills

RECOMMENDED LEARNING:
  1. [High] Docker
     * Container basics
     * Dockerfile creation
     * Docker Compose
     * Deployment

  2. [Medium] AWS
     * AWS fundamentals
     * EC2 basics
     * RDS setup
     * Deploy Python apps

RECOMMENDATION:
Strong candidate with solid backend skills. Should learn Docker and AWS to become ideal fit.
```

### Ranking Summary
```
------------------------------------
CANDIDATE RANKING SUMMARY
------------------------------------

Rank #1: John Doe
  ATS Score: 85/100 | Match: 78%
  Resume: john_doe_resume.pdf

Rank #2: Jane Smith
  ATS Score: 72/100 | Match: 65%
  Resume: jane_smith_resume.pdf

Rank #3: Bob Johnson
  ATS Score: 68/100 | Match: 61%
  Resume: bob_johnson_resume.pdf
```

## Common Issues & Solutions

### Issue: Bot doesn't start
**Check:**
- Token in `.env` is correct
- No spaces around `=` in `.env`
- Dependencies installed

### Issue: Analysis fails
**Check:**
- Gemini API key is valid
- PDF is not corrupted
- PDF is under 20MB
- Internet connection stable

### Issue: Wrong output format
**Check:**
- Using latest version of code
- Gemini model is responding with JSON
- No network interruptions during analysis

### Issue: Files not cleaned up
**Check:**
- `temp/` directory exists
- Cleanup runs on bot startup
- File permissions are correct

## Performance Testing

### Expected Processing Times
- Single resume: 5-15 seconds
- 3 resumes: 15-45 seconds
- 5 resumes: 25-75 seconds

**Note:** Processing time depends on:
- Resume length
- Job description complexity
- Gemini API response time
- Network speed

## Manual Testing Checklist

```
[ ] Bot responds to /start within 2 seconds
[ ] Job description accepted (any length)
[ ] PDF upload shows confirmation
[ ] Multiple PDFs tracked correctly
[ ] Analysis completes without errors
[ ] Output is well-formatted
[ ] Scores are reasonable (not all 0 or 100)
[ ] Missing skills are accurate
[ ] Recommendations are relevant
[ ] Ranking is correct (highest score first)
[ ] Reset clears all data
[ ] Can start new session after reset
[ ] Error messages are clear
[ ] No crashes during normal operation
```

## Test Data

### Sample Job Description Templates

**Backend Developer:**
See Scenario 1 above

**Frontend Developer:**
```
Frontend Developer - React

Required Skills:
- React 18+
- TypeScript
- CSS/Tailwind
- REST API integration
- Git

Preferred:
- Next.js
- State management (Redux/Zustand)
- Testing (Jest, React Testing Library)
```

**Full Stack Developer:**
```
Full Stack Developer

Required:
- JavaScript/TypeScript
- React
- Node.js/Express
- MongoDB or PostgreSQL
- REST/GraphQL APIs

Preferred:
- AWS/Azure
- Docker
- CI/CD
```

## Automated Testing (Future)

For V2, consider adding:
- Unit tests for formatters
- Integration tests for Gemini API
- Mock Telegram bot tests
- End-to-end flow tests
- Load testing for multiple users

## Debugging Tips

1. **Enable verbose logging:**
   Add to bot.py:
   ```python
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check Gemini response:**
   Print raw response before JSON parsing

3. **Verify file uploads:**
   Check `temp/` directory for PDFs

4. **Test Gemini separately:**
   Use `gemini_service.py` standalone

5. **Monitor API limits:**
   - Gemini API has rate limits
   - Telegram Bot API has file size limits

## Success Criteria

✅ All commands work reliably  
✅ Analysis completes for valid inputs  
✅ Output is readable and accurate  
✅ Error handling works gracefully  
✅ Files cleanup automatically  
✅ Multiple users can use simultaneously  
✅ Performance is acceptable (<30s for 3 resumes)

---

**Ready to test? Start with Scenario 1!**
