import json
import logging
import requests
import re
from config import GEMINI_API_KEY
from file_extractor import extract_text_from_file

logger = logging.getLogger(__name__)

class GeminiService:
    # Prioritize full models over lite models for maximum analysis depth
    MODELS = [
        "gemini-3.6-flash",
        "gemini-3.7-flash",
        "gemini-3-flash-preview",
        "gemini-3.1-flash-lite",
        "gemini-flash-latest"
    ]

    def __init__(self, api_key: str = None):
        self.api_key = api_key or GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured in .env file.")

    def analyze_resume(self, job_description: str, resume_path: str, resume_name: str) -> dict:
        """Analyze a single resume against a job description using Google Gemini"""
        try:
            logger.info(f"Extracting text from resume: {resume_name}")
            resume_text = extract_text_from_file(resume_path)
            
            if not resume_text or len(resume_text.strip()) < 30:
                return {
                    'error': True,
                    'message': f"Could not extract readable text from '{resume_name}'. Ensure the document contains selectable text.",
                    'resume_name': resume_name
                }

            prompt = self._create_analysis_prompt(job_description=job_description, resume_text=resume_text, resume_name=resume_name)
            
            last_error = None
            for model in self.MODELS:
                try:
                    logger.info(f"Analyzing {resume_name} with Gemini model: {model}")
                    url = f"{self.base_url}/models/{model}:generateContent?key={self.api_key}"
                    payload = {
                        "contents": [{
                            "parts": [{"text": prompt}]
                        }],
                        "generationConfig": {
                            "response_mime_type": "application/json",
                            "temperature": 0.1
                        }
                    }
                    
                    response = requests.post(url, json=payload, timeout=45)
                    
                    if response.status_code == 200:
                        data = response.json()
                        candidates = data.get('candidates', [])
                        if not candidates:
                            raise ValueError(f"Gemini returned empty candidates for model {model}")
                        
                        raw_text = candidates[0]['content']['parts'][0]['text'].strip()
                        result = self._parse_json(raw_text)
                        
                        result['resume_name'] = resume_name
                        if not result.get('candidate_name') or result.get('candidate_name') in ('Unknown', 'Candidate', 'Not Found'):
                            cleaned_name = re.sub(r'[_.-]', ' ', resume_name).replace('Resume', '').replace('docx', '').replace('pdf', '').strip()
                            result['candidate_name'] = cleaned_name or 'Candidate'
                        
                        result['ats_score'] = max(0, min(100, int(round(float(result.get('ats_score') or 0)))))
                        result['job_match_percentage'] = max(0, min(100, int(round(float(result.get('job_match_percentage') or 0)))))
                        
                        logger.info(f"Completed analysis for {resume_name}: ATS={result['ats_score']}, Match={result['job_match_percentage']}% using {model}")
                        return result
                    
                    elif response.status_code == 400:
                        err_json = response.json().get('error', {})
                        err_msg = err_json.get('message', response.text)
                        if 'API_KEY_INVALID' in str(err_json) or 'API key not valid' in err_msg:
                            raise ValueError("Gemini API key is invalid. Please check your GEMINI_API_KEY in .env.")
                        logger.warning(f"Gemini model {model} HTTP 400: {err_msg}")
                        last_error = RuntimeError(f"Gemini error: {err_msg}")
                    elif response.status_code in (404, 503):
                        logger.info(f"Model {model} returned {response.status_code}, trying fallback model...")
                        continue
                    elif response.status_code == 429:
                        logger.warning(f"Rate limit on {model}, trying fallback...")
                        last_error = RuntimeError("Gemini rate limit / quota exceeded.")
                        continue
                    else:
                        logger.warning(f"Gemini {model} returned status {response.status_code}: {response.text}")
                        last_error = RuntimeError(f"Gemini API returned status {response.status_code}")
                        
                except ValueError as ve:
                    raise ve
                except Exception as ex:
                    logger.warning(f"Error with Gemini model {model}: {ex}")
                    last_error = ex
                    continue
            
            raise last_error or RuntimeError("All Gemini models failed to process the request.")

        except Exception as e:
            logger.error(f"Error analyzing resume {resume_name}: {str(e)}")
            return {
                'error': True,
                'message': str(e),
                'resume_name': resume_name
            }

    def _parse_json(self, raw_text: str) -> dict:
        """Parse raw response text into JSON, stripping code fences if needed"""
        clean = raw_text.strip()
        if clean.startswith("```"):
            lines = clean.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            clean = "\n".join(lines).strip()
        
        match = re.search(r'\{.*\}', clean, re.DOTALL)
        if match:
            clean = match.group(0)
            
        return json.loads(clean)

    def _create_analysis_prompt(self, job_description: str, resume_text: str, resume_name: str) -> str:
        """Create a balanced, realistic, and highly accurate ATS analysis prompt"""
        return f"""You are an elite Applicant Tracking System (ATS) evaluator and expert technical recruiter.

Compare the CANDIDATE RESUME against the JOB DESCRIPTION with high precision, fairness, and realistic calibration.

=== JOB DESCRIPTION ===
{job_description.strip()}

=== CANDIDATE RESUME (File: {resume_name}) ===
{resume_text.strip()}

=== EVALUATION GUIDELINES ===
1. CANDIDATE NAME:
   - Extract the candidate's actual full name from the resume header. Do not default to 'Unknown' if a name is present.

2. ATS SCORE (0 - 100):
   - Measure standard ATS parsing and evaluation criteria:
     * Skills Match (40% weight): Does the resume contain the required technologies, tools, and methodologies?
     * Experience Relevance (25% weight): Are projects, roles, and years of experience relevant to the role?
     * Project & Work Impact (15% weight): Practical demonstration of skills in real projects or production work.
     * Keywords & Concepts (10% weight): Presence of industry-standard domain terms and core concepts.
     * Education & Certifications (10% weight): Degree relevance, certifications, and academic record.
   - Calibrated Scale:
     * 80 - 100: Strong match with nearly all required skills and relevant projects.
     * 60 - 79: Solid match; covers core requirements with few minor gaps.
     * 40 - 59: Partial match; possesses some foundational skills but missing major requirements.
     * Below 40: Role/domain mismatch (e.g. software engineer applying to product manager or marketing).

3. JOB MATCH % (0 - 100):
   - Direct percentage of requirements and responsibilities in the Job Description satisfied by the candidate's profile.

4. MATCHING SKILLS:
   - List skills, tools, languages, or concepts that clearly appear in BOTH the Job Description and the Resume.
   - Look for aliases and synonyms (e.g., "React" matches "React.js", "Postgres" matches "PostgreSQL", "ML" matches "Machine Learning").

5. MISSING SKILLS:
   - List specific required or preferred skills from the Job Description that the candidate does NOT show in their resume.
   - Importance:
     * "critical": Must-have core requirements explicitly stated in JD.
     * "important": Significant requirements that affect job execution.
     * "nice-to-have": Preferred, bonus, or secondary tools.

6. PARTIAL SKILLS:
   - Related or adjacent experience (e.g., candidate has MySQL where PostgreSQL is needed, or academic experience without enterprise deployment).

7. SKILL BREAKDOWN:
   - Extract 5 to 8 major requirements directly from the Job Description.
   - Show candidate's match percentage (0% to 100%) for each. Do not truncate skill names.

8. STRENGTHS & WEAKNESSES:
   - Be specific to the candidate's actual projects, metrics, certifications, or problem-solving achievements.

CRITICAL: Return ONLY a valid JSON object matching this schema. Do not include markdown commentary.

{{
  "candidate_name": "<actual name from resume>",
  "ats_score": <integer 0-100>,
  "job_match_percentage": <integer 0-100>,
  "matching_skills": ["<matching skill 1>", "<matching skill 2>"],
  "missing_skills": [
    {{
      "skill": "<missing skill name>",
      "importance": "critical|important|nice-to-have",
      "reason": "<specific reason based on JD>"
    }}
  ],
  "partial_skills": [
    {{
      "skill": "<skill>",
      "match_percentage": <integer 0-100>,
      "note": "<explanation>"
    }}
  ],
  "skill_breakdown": [
    {{
      "skill": "<exact skill name from JD>",
      "match_percentage": <integer 0-100>,
      "found_in_resume": true|false
    }}
  ],
  "experience_summary": "<2-3 sentence accurate summary of candidate's relevant background>",
  "recommended_learning": [
    {{
      "skill": "<missing skill>",
      "priority": "high|medium|low",
      "topics": ["<topic 1>", "<topic 2>"]
    }}
  ],
  "strengths": ["<strength 1>", "<strength 2>"],
  "weaknesses": ["<gap 1 relative to JD>", "<gap 2>"],
  "overall_recommendation": "<Direct, actionable hiring recommendation>"
}}"""

    def rank_candidates(self, results: list) -> list:
        """Rank candidates by ATS score and job match"""
        valid_results = [r for r in results if not r.get('error')]
        ranked = sorted(
            valid_results,
            key=lambda x: (x.get('ats_score', 0), x.get('job_match_percentage', 0)),
            reverse=True
        )
        return ranked
