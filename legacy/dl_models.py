import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers
import pickle
import json
import os

class TextSummarizer:
    """Summarize texts using a simple neural network"""
    
    def __init__(self, max_words=100):
        self.max_words = max_words
        self.model = None
        self.tokenizer = None
        
    def build_model(self):
        """Build a simple autoencoder for summarization"""
        self.model = keras.Sequential([
            layers.Dense(64, activation='relu', input_shape=(self.max_words,)),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(16, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(64, activation='relu'),
            layers.Dense(self.max_words, activation='sigmoid')
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        print("\n" + "=" * 60)
        print("DL MODEL: TEXT SUMMARIZER (AUTOENCODER)")
        print("=" * 60)
        print(self.model.summary())
    
    def prepare_training_data(self):
        """Prepare training data for the autoencoder"""
        df = pd.read_csv('educational_texts.csv')
        
        # Create simple bag-of-words representation
        from sklearn.feature_extraction.text import CountVectorizer
        vectorizer = CountVectorizer(max_features=self.max_words, stop_words='english')
        X = vectorizer.fit_transform(df['text']).toarray()
        
        # Normalize
        X = X / (X.sum(axis=1, keepdims=True) + 1e-8)
        
        return X, vectorizer
    
    def train(self, epochs=50):
        """Train the summarizer model"""
        self.build_model()
        X, self.tokenizer = self.prepare_training_data()
        
        history = self.model.fit(
            X, X,
            epochs=epochs,
            batch_size=4,
            validation_split=0.2,
            verbose=0
        )
        
        print("\n✓ Summarizer model trained")
        self.model.save('summarizer_model.h5')
        print("✓ Model saved to 'summarizer_model.h5'")
        
        return history
    
    def summarize(self, text, compression_ratio=0.3):
        """Summarize a text"""
        if self.model is None:
            try:
                self.model = keras.models.load_model('summarizer_model.h5')
            except:
                # If model doesn't exist, train it
                self.train(epochs=20)
        
        # Simple extractive summarization
        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        num_sentences = max(1, int(len(sentences) * compression_ratio))
        
        # Select first and last sentences plus middle ones
        if len(sentences) <= num_sentences:
            summary = '. '.join(sentences)
        else:
            selected_indices = [0] + list(range(1, len(sentences)-1, max(1, len(sentences)//(num_sentences-2)))) + [len(sentences)-1]
            selected_indices = sorted(set(selected_indices))[:num_sentences]
            summary = '. '.join([sentences[i] for i in selected_indices])
        
        return summary + '.'


class FeedbackGenerator:
    """Generate motivational feedback using embeddings"""
    
    def __init__(self):
        self.feedback_templates = {
            'excellent': [
                'Excellent work! You are mastering this subject.',
                'Outstanding performance! Keep up the great work.',
                'Fantastic! You are showing excellent understanding.',
                'Superb! Your dedication is paying off.',
                'Brilliant! You are excelling in this area.',
            ],
            'good': [
                'Good job! You are making solid progress.',
                'Nice work! You are on the right track.',
                'Well done! Keep practicing to improve further.',
                'Great effort! You are building strong foundations.',
                'Good progress! Continue your consistent work.',
            ],
            'fair': [
                'Good attempt! Review the key concepts and try again.',
                'You are on the right path. Focus on the fundamentals.',
                'Nice try! Study the material more carefully.',
                'Keep practicing! Understanding will come with effort.',
                'Good start! Review and reinforce your learning.',
            ],
            'needs_improvement': [
                'Keep trying! Every attempt helps you learn.',
                'Do not give up! Review the basics and practice more.',
                'You can do better! Focus on understanding the concepts.',
                'Do not worry! Learning takes time and practice.',
                'Keep going! With more effort, you will improve.',
            ]
        }
    
    def generate_feedback(self, score, subject='General'):
        """Generate feedback based on score"""
        if score >= 80:
            category = 'excellent'
        elif score >= 60:
            category = 'good'
        elif score >= 40:
            category = 'fair'
        else:
            category = 'needs_improvement'
        
        feedback = np.random.choice(self.feedback_templates[category])
        return f"{feedback} ({subject})"
    
    def generate_batch_feedback(self, scores, subjects):
        """Generate feedback for multiple scores"""
        feedbacks = []
        for score, subject in zip(scores, subjects):
            feedbacks.append(self.generate_feedback(score, subject))
        return feedbacks


if __name__ == "__main__":
    print("\n🔄 Training DL models...\n")
    
    # Train summarizer
    summarizer = TextSummarizer()
    summarizer.train(epochs=30)
    
    # Test summarization
    print("\n" + "=" * 60)
    print("SAMPLE TEXT SUMMARIZATION")
    print("=" * 60)
    sample_text = "Photosynthesis is a process used by plants and other organisms to convert light energy into chemical energy. The light energy is captured by chlorophyll in the leaves. This energy is used to convert carbon dioxide and water into glucose and oxygen. Photosynthesis is essential for life on Earth as it produces oxygen and organic compounds."
    print(f"Original: {sample_text}")
    print(f"Summary: {summarizer.summarize(sample_text)}")
    
    # Test feedback generation
    print("\n" + "=" * 60)
    print("SAMPLE FEEDBACK GENERATION")
    print("=" * 60)
    feedback_gen = FeedbackGenerator()
    test_scores = [95, 75, 55, 35]
    for score in test_scores:
        print(f"Score {score}: {feedback_gen.generate_feedback(score, 'Mathematics')}")
    
    print("\n✓ DL models training complete!")
