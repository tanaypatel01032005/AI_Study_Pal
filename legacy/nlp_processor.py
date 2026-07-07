import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import pandas as pd
import json

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class StudyTipsGenerator:
    """Generate study tips using NLP"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.tips_templates = {
            'Mathematics': [
                'Practice solving problems regularly to build problem-solving skills.',
                'Review key formulas and theorems daily to strengthen memory.',
                'Work through step-by-step solutions to understand the logic.',
                'Create flashcards for important concepts and definitions.',
                'Solve practice problems from different sources for variety.',
            ],
            'Science': [
                'Create diagrams and visual representations of concepts.',
                'Conduct experiments or simulations to understand processes.',
                'Review scientific terminology and definitions regularly.',
                'Connect concepts to real-world applications and examples.',
                'Study the relationships between different scientific principles.',
            ],
            'History': [
                'Create timelines to understand the sequence of events.',
                'Read primary sources to gain deeper understanding.',
                'Connect historical events to their causes and consequences.',
                'Discuss historical topics with peers to gain different perspectives.',
                'Review key dates and important figures regularly.',
            ],
            'Literature': [
                'Read the text multiple times to catch subtle details.',
                'Take notes on character development and plot progression.',
                'Analyze literary devices and their effects on the narrative.',
                'Discuss themes and interpretations with others.',
                'Write summaries to reinforce your understanding.',
            ],
            'Computer Science': [
                'Write code regularly to practice programming concepts.',
                'Debug code to understand how programs work.',
                'Study algorithms and their time complexity.',
                'Review documentation and best practices.',
                'Participate in coding challenges and competitions.',
            ]
        }
    
    def extract_keywords(self, text, num_keywords=5):
        """Extract keywords from text using tokenization"""
        # Tokenize
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords and non-alphabetic tokens
        filtered_tokens = [
            token for token in tokens 
            if token.isalpha() and token not in self.stop_words
        ]
        
        # Get frequency distribution
        freq_dist = FreqDist(filtered_tokens)
        
        # Get top keywords
        keywords = [word for word, _ in freq_dist.most_common(num_keywords)]
        
        return keywords
    
    def generate_tips(self, subject, text=None, num_tips=3):
        """Generate study tips for a subject"""
        tips = self.tips_templates.get(subject, self.tips_templates['Mathematics'])
        
        selected_tips = []
        for i in range(min(num_tips, len(tips))):
            selected_tips.append(tips[i])
        
        return selected_tips
    
    def analyze_text(self, text):
        """Analyze text and extract information"""
        sentences = sent_tokenize(text)
        tokens = word_tokenize(text.lower())
        
        analysis = {
            'total_sentences': len(sentences),
            'total_words': len(tokens),
            'unique_words': len(set(tokens)),
            'average_sentence_length': len(tokens) / len(sentences) if sentences else 0,
            'keywords': self.extract_keywords(text, num_keywords=5)
        }
        
        return analysis


if __name__ == "__main__":
    print("\n🔄 Testing NLP processor...\n")
    
    nlp = StudyTipsGenerator()
    
    # Test keyword extraction
    print("=" * 60)
    print("NLP: KEYWORD EXTRACTION")
    print("=" * 60)
    sample_text = "Machine learning is a subset of artificial intelligence that enables systems to learn from data without being explicitly programmed."
    keywords = nlp.extract_keywords(sample_text)
    print(f"Text: {sample_text}")
    print(f"Keywords: {keywords}")
    
    # Test text analysis
    print("\n" + "=" * 60)
    print("NLP: TEXT ANALYSIS")
    print("=" * 60)
    analysis = nlp.analyze_text(sample_text)
    for key, value in analysis.items():
        print(f"{key}: {value}")
    
    # Test tips generation
    print("\n" + "=" * 60)
    print("NLP: STUDY TIPS GENERATION")
    print("=" * 60)
    subjects = ['Mathematics', 'Science', 'History', 'Literature', 'Computer Science']
    for subject in subjects:
        tips = nlp.generate_tips(subject, num_tips=2)
        print(f"\n{subject}:")
        for i, tip in enumerate(tips, 1):
            print(f"  {i}. {tip}")
    
    print("\n✓ NLP processor testing complete!")
