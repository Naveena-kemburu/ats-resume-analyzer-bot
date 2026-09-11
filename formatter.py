def format_candidate_result(result: dict, rank: int = None, jd_title: str = None) -> str:
    """Format single candidate analysis for Telegram without emojis"""
    
    if result.get('error'):
        return f"""[ERROR] {result.get('resume_name')}
        
{result.get('message', 'Unknown error')}"""
    
    # Header
    output = "------------------------------------\n"
    if rank:
        output += f"RANK #{rank}\n"
    output += f"Candidate: {result.get('candidate_name', 'Unknown')}\n"
    output += "------------------------------------\n\n"
    
    if jd_title:
        output += f"Job Description: {jd_title}\n"
    output += f"Resume File: {result.get('resume_name', 'N/A')}\n\n"
    
    # Scores
    try:
        ats_score = int(round(float(result.get('ats_score') or 0)))
    except (ValueError, TypeError):
        ats_score = 0

    try:
        job_match = int(round(float(result.get('job_match_percentage') or 0)))
    except (ValueError, TypeError):
        job_match = 0
    
    output += "ATS SCORE\n"
    output += f"{ats_score}/100\n"
    output += _create_progress_bar(ats_score) + "\n\n"
    
    output += "JOB MATCH\n"
    output += f"{job_match}%\n"
    output += _create_progress_bar(job_match) + "\n\n"
    
    # Matching skills
    matching = result.get('matching_skills', [])
    if matching:
        output += "MATCHING SKILLS:\n"
        output += ", ".join(matching[:12])
        if len(matching) > 12:
            output += f" (+{len(matching) - 12} more)"
        output += "\n\n"
    
    # Missing skills
    missing = result.get('missing_skills', [])
    if missing:
        output += "MISSING SKILLS:\n"
        
        critical = [s for s in missing if s.get('importance') == 'critical']
        important = [s for s in missing if s.get('importance') == 'important']
        nice_to_have = [s for s in missing if s.get('importance') == 'nice-to-have']
        
        if critical:
            output += "  Critical:\n"
            for skill in critical[:5]:
                output += f"  - {skill.get('skill')}\n"
        
        if important:
            output += "  Important:\n"
            for skill in important[:5]:
                output += f"  - {skill.get('skill')}\n"
        
        if nice_to_have:
            output += "  Nice to have:\n"
            for skill in nice_to_have[:3]:
                output += f"  - {skill.get('skill')}\n"
        
        output += "\n"
    
    # Skill breakdown (untruncated)
    skill_breakdown = result.get('skill_breakdown', [])
    if skill_breakdown:
        output += "SKILL BREAKDOWN:\n"
        for skill_data in skill_breakdown[:8]:
            skill = str(skill_data.get('skill', 'Unknown'))
            try:
                percentage = int(round(float(skill_data.get('match_percentage') or 0)))
            except (ValueError, TypeError):
                percentage = 0
            bar = _create_progress_bar(percentage, length=10)
            output += f"  - {skill}: {bar} {percentage}%\n"
        output += "\n"
    
    # Strengths
    strengths = result.get('strengths', [])
    if strengths:
        output += "STRENGTHS:\n"
        for strength in strengths[:3]:
            output += f"  - {strength}\n"
        output += "\n"
    
    # Weaknesses
    weaknesses = result.get('weaknesses', [])
    if weaknesses:
        output += "AREAS TO IMPROVE:\n"
        for weakness in weaknesses[:3]:
            output += f"  - {weakness}\n"
        output += "\n"
    
    # Learning recommendations
    learning = result.get('recommended_learning', [])
    if learning:
        output += "RECOMMENDED LEARNING:\n"
        for idx, course in enumerate(learning[:3], 1):
            skill = course.get('skill', 'Unknown')
            priority = course.get('priority', 'medium').capitalize()
            topics = course.get('topics', [])
            
            output += f"  {idx}. [{priority}] {skill}\n"
            for topic in topics[:4]:
                output += f"     * {topic}\n"
            output += "\n"
    
    # Overall recommendation
    recommendation = result.get('overall_recommendation', '')
    if recommendation:
        output += "RECOMMENDATION:\n"
        output += f"{recommendation}\n"
    
    return output


def format_ranking_summary(ranked_results: list) -> str:
    """Format final ranking summary without emojis"""
    if not ranked_results:
        return "No candidates to rank."
    
    output = "\n------------------------------------\n"
    output += "CANDIDATE RANKING SUMMARY\n"
    output += "------------------------------------\n\n"
    
    for idx, result in enumerate(ranked_results, 1):
        name = result.get('candidate_name', 'Unknown')
        try:
            ats = int(round(float(result.get('ats_score') or 0)))
        except (ValueError, TypeError):
            ats = 0
        try:
            match = int(round(float(result.get('job_match_percentage') or 0)))
        except (ValueError, TypeError):
            match = 0
        
        output += f"Rank #{idx}: {name}\n"
        output += f"  ATS Score: {ats}/100 | Match: {match}%\n"
        output += f"  Resume: {result.get('resume_name', 'N/A')}\n\n"
    
    return output


def _create_progress_bar(percentage: int, length: int = 20) -> str:
    """Create a clean text-based progress bar"""
    try:
        pct = float(percentage if percentage is not None else 0)
    except (ValueError, TypeError):
        pct = 0.0
    pct = max(0.0, min(100.0, pct))
    filled = int((pct / 100.0) * length)
    empty = length - filled
    return "[" + "=" * filled + " " * empty + "]"


def format_error_message(error: str) -> str:
    """Format error message for user without emojis"""
    return f"""[ERROR]

An issue occurred: {error}

Please verify your input and try again."""
