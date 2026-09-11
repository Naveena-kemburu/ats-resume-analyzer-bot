import os
import time
import logging
from config import TEMP_DIR

logger = logging.getLogger(__name__)

def cleanup_old_files(max_age_hours: int = 24):
    """Remove files older than max_age_hours from temp directory"""
    if not os.path.exists(TEMP_DIR):
        return
    
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    removed_count = 0
    
    try:
        for filename in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, filename)
            
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                
                if file_age > max_age_seconds:
                    os.remove(file_path)
                    removed_count += 1
                    logger.info(f"Removed old file: {filename}")
        
        if removed_count > 0:
            logger.info(f"Cleanup complete: {removed_count} files removed")
    
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")

def cleanup_user_session(user_id: int):
    """Remove all files for a specific user session"""
    if not os.path.exists(TEMP_DIR):
        return
    
    try:
        for filename in os.listdir(TEMP_DIR):
            if filename.startswith(f"{user_id}_"):
                file_path = os.path.join(TEMP_DIR, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logger.info(f"Removed user file: {filename}")
    
    except Exception as e:
        logger.error(f"Error cleaning user {user_id} files: {str(e)}")
