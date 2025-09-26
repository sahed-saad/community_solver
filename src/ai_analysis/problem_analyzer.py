import re
from textblob import TextBlob
import nltk
from collections import Counter
import json
import pandas as pd

class ProblemAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        # Define problem categories and keywords
        self.categories = {
            'Social Division': ['division', 'conflict', 'tension', 'disagreement', 'polarization', 'us vs them', 'exclusion'],
            'Disinformation': ['fake news', 'misinformation', 'false information', 'rumor', 'conspiracy', 'propaganda'],
            'Community Safety': ['safety', 'crime', 'security', 'violence', 'threat', 'danger', 'protection'],
            'Infrastructure': ['infrastructure', 'roads', 'utilities', 'transportation', 'facilities', 'maintenance'],
            'Environment': ['environment', 'pollution', 'climate', 'sustainability', 'green', 'waste', 'conservation'],
            'Education': ['education', 'school', 'learning', 'academic', 'student', 'teacher', 'curriculum'],
            'Healthcare': ['health', 'medical', 'healthcare', 'hospital', 'doctor', 'treatment', 'wellness'],
            'Economic': ['economic', 'employment', 'business', 'economy', 'financial', 'jobs', 'income']
        }
        
        self.severity_keywords = {
            'Critical': ['urgent', 'emergency', 'crisis', 'critical', 'immediate', 'severe', 'dangerous'],
            'High': ['serious', 'important', 'significant', 'major', 'concerning', 'worrying'],
            'Medium': ['moderate', 'average', 'standard', 'typical', 'normal'],
            'Low': ['minor', 'small', 'slight', 'minimal', 'insignificant']
        }

    def analyze_problem(self, title, description, category):
        """Analyze a community problem and provide AI insights"""
        
        # Combine title and description for analysis
        full_text = f"{title} {description}".lower()
        
        # Sentiment analysis
        sentiment = self._analyze_sentiment(full_text)
        
        # Category confidence
        category_confidence = self._analyze_category(full_text, category)
        
        # Severity assessment
        severity_assessment = self._assess_severity(full_text)
        
        # Key issues extraction
        key_issues = self._extract_key_issues(full_text)
        
        # Stakeholder identification
        stakeholders = self._identify_stakeholders(full_text)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(category, severity_assessment, key_issues)
        
        analysis = {
            'sentiment': sentiment,
            'category_confidence': category_confidence,
            'severity_assessment': severity_assessment,
            'key_issues': key_issues,
            'stakeholders': stakeholders,
            'recommendations': recommendations,
            'analysis_date': str(pd.Timestamp.now())
        }
        
        return json.dumps(analysis, indent=2)

    def _analyze_sentiment(self, text):
        """Analyze sentiment of the text"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            sentiment = 'Positive'
        elif polarity < -0.1:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return {
            'sentiment': sentiment,
            'polarity': round(polarity, 3),
            'subjectivity': round(blob.sentiment.subjectivity, 3)
        }

    def _analyze_category(self, text, provided_category):
        """Analyze how well the text matches the provided category"""
        category_scores = {}
        
        for cat, keywords in self.categories.items():
            score = sum(1 for keyword in keywords if keyword in text)
            category_scores[cat] = score
        
        # Find best matching category
        best_category = max(category_scores, key=category_scores.get)
        confidence = category_scores[provided_category] / max(category_scores.values()) if max(category_scores.values()) > 0 else 0
        
        return {
            'provided_category': provided_category,
            'best_match': best_category,
            'confidence': round(confidence, 3),
            'all_scores': category_scores
        }

    def _assess_severity(self, text):
        """Assess the severity level of the problem"""
        severity_scores = {}
        
        for severity, keywords in self.severity_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            severity_scores[severity] = score
        
        # Determine severity based on scores
        if severity_scores['Critical'] > 0:
            assessed_severity = 'Critical'
        elif severity_scores['High'] > 0:
            assessed_severity = 'High'
        elif severity_scores['Medium'] > 0:
            assessed_severity = 'Medium'
        else:
            assessed_severity = 'Low'
        
        return {
            'assessed_severity': assessed_severity,
            'scores': severity_scores
        }

    def _extract_key_issues(self, text):
        """Extract key issues and themes from the text"""
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Remove common stop words
        stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'])
        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Count word frequency
        word_freq = Counter(filtered_words)
        
        return {
            'top_issues': dict(word_freq.most_common(5)),
            'total_issues': len(set(filtered_words))
        }

    def _identify_stakeholders(self, text):
        """Identify potential stakeholders based on the problem description"""
        stakeholder_keywords = {
            'Government': ['government', 'city', 'municipal', 'mayor', 'council', 'official', 'policy'],
            'Community Groups': ['community', 'neighborhood', 'residents', 'citizens', 'local'],
            'Business': ['business', 'company', 'corporate', 'industry', 'commerce', 'economic'],
            'Education': ['school', 'university', 'college', 'education', 'student', 'teacher'],
            'Healthcare': ['hospital', 'clinic', 'health', 'medical', 'doctor', 'nurse'],
            'Media': ['media', 'news', 'journalist', 'press', 'communication'],
            'NGOs': ['nonprofit', 'organization', 'charity', 'foundation', 'ngo']
        }
        
        identified_stakeholders = []
        
        for stakeholder_type, keywords in stakeholder_keywords.items():
            if any(keyword in text for keyword in keywords):
                identified_stakeholders.append(stakeholder_type)
        
        return {
            'identified_stakeholders': identified_stakeholders,
            'total_types': len(identified_stakeholders)
        }

    def _generate_recommendations(self, category, severity, key_issues):
        """Generate AI-powered recommendations based on analysis"""
        recommendations = []
        
        # Category-based recommendations
        if category == 'Social Division':
            recommendations.extend([
                'Organize community dialogue sessions to address underlying tensions',
                'Implement diversity and inclusion training programs',
                'Create platforms for cross-community collaboration'
            ])
        elif category == 'Disinformation':
            recommendations.extend([
                'Develop fact-checking and media literacy programs',
                'Create trusted information channels for the community',
                'Establish partnerships with local media for accurate reporting'
            ])
        elif category == 'Community Safety':
            recommendations.extend([
                'Increase community policing and neighborhood watch programs',
                'Improve lighting and infrastructure in high-risk areas',
                'Develop youth engagement programs to prevent crime'
            ])
        
        # Severity-based recommendations
        if severity['assessed_severity'] == 'Critical':
            recommendations.append('Immediate action required - consider emergency response protocols')
        elif severity['assessed_severity'] == 'High':
            recommendations.append('Prioritize this issue in community planning and resource allocation')
        
        return {
            'recommendations': recommendations[:5],  # Limit to top 5
            'priority_level': severity['assessed_severity']
        }
