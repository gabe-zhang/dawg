import re


class KeywordSearch:
    def __init__(self):
        # Define primary keywords and their variations for each category
        self.keywords = {
            'temperature': {
                'primary': ['temperature', 'degrees'],
                'variations': ['hot', 'cold', 'warm', 'cool', 'celsius', 'fahrenheit']
            },
            'humidity': {
                'primary': ['humidity', 'moisture'],
                'variations': ['humid', 'damp', 'dry', 'wetness', 'water', 'air']
            },
            'lux': {
                'primary': ['light', 'lux', 'brightness'],
                'variations': ['bright', 'dark', 'illumination', 'dim']
            }
        }

    def clean_text(self, text):
        """Clean text by removing all punctuation and special characters using regex"""
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        return cleaned_text

    def search(self, text):
        # Clean and convert input text to lowercase and split into words
        words = self.clean_text(text.lower()).split()
        
        # Count matches for each category
        scores = {
            'temperature': 0,
            'humidity': 0,
            'lux': 0
        }
        
        # Track which words have been matched to avoid double counting
        matched_words = set()
        
        # Check for keyword matches in each category
        for category, keyword_types in self.keywords.items():
            # Check primary keywords first (higher weight)
            for keyword in keyword_types['primary']:
                if keyword in words and keyword not in matched_words:
                    scores[category] += 2  # Primary keywords get double weight
                    matched_words.add(keyword)
            
            # Check variations
            for keyword in keyword_types['variations']:
                if keyword in words and keyword not in matched_words:
                    scores[category] += 1
                    matched_words.add(keyword)
        
        # Find categories with scores above zero
        matching_categories = [(cat, score) for cat, score in scores.items() if score > 0]
        
        if not matching_categories:
            return {
                'categories': ['unknown'],
                'confidences': [0],
                'scores': scores
            }
            
        # Sort categories by score in descending order
        matching_categories.sort(key=lambda x: x[1], reverse=True)
        
        # Calculate confidence scores
        total_score = sum(score for _, score in matching_categories)
        categories = []
        confidences = []
        
        for category, score in matching_categories:
            confidence = score / total_score
            if confidence >= 0.25:  # Only include categories with meaningful confidence
                categories.append(category)
                confidences.append(confidence)
        
        return {
            'categories': categories or ['unknown'],
            'confidences': confidences or [0],
            'scores': scores
        }