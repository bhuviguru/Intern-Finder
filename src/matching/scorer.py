import json
import os

import logging

class Scorer:
    def __init__(self, keywords_config_path='config/keywords.json'):
        # Get absolute path relative to project root
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if not os.path.isabs(keywords_config_path):
            keywords_config_path = os.path.join(base_dir, keywords_config_path)
            
        self.logger = logging.getLogger(__name__)
        self.keywords_config = self._load_config(keywords_config_path)
    
    def _load_config(self, path):
        if not os.path.exists(path):
            self.logger.warning(f"Keywords config not found at {path}")
            return {"roles": [], "filters": []}
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading keywords config: {e}")
            return {"roles": [], "filters": []}

    def score_job(self, job_data):
        """
        Calculates a score for a job dictionary.
        job_data: dict with keys 'role', 'company', 'stipend', 'location', 'description' (optional)
        """
        score = 0
        role_text = job_data.get('role', '').lower()
        location_text = job_data.get('location', '').lower()
        stipend_text = job_data.get('stipend', '').lower()
        
        # 1. Role Keyword Matching (+3 points)
        for keyword in self.keywords_config.get('roles', []):
            if keyword.lower() in role_text:
                score += 3
        
        # 2. Filter Matching (Remote, Stipend) (+2 points)
        filters = self.keywords_config.get('filters', [])
        
        # Remote
        if "remote" in filters and ("remote" in location_text or "work from home" in location_text):
            score += 2
            
        # Stipend (Check if stipend is mentioned/valid)
        if "stipend" in filters:
            if stipend_text and "unpaid" not in stipend_text.lower() and len(stipend_text) > 3:
                 score += 2

        # 3. Extra keywords (e.g. Tech stack in role or description if we had it)
        # For now, we reuse roles as skills/tech keywords for broader match
        # If 'React' is in role, it already got +3.
        
        return score
