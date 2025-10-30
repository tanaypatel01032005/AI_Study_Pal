import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report
import pickle
import json

class QuizGenerator:
    """Generate quizzes using ML classification"""
    
    def __init__(self):
        self.vectorizer = CountVectorizer(max_features=100, stop_words='english')
        self.model = LogisticRegression(max_iter=200, random_state=42)
        self.is_trained = False
        
    def prepare_training_data(self):
        """Create training data for difficulty classification"""
        # Easy questions (shorter, simpler)
        easy_questions = [
            'What is photosynthesis',
            'Define gravity',
            'What is an atom',
            'Name the planets',
            'What is DNA',
            'Define velocity',
            'What is a cell',
            'Name the continents',
            'What is energy',
            'Define temperature',
        ]
        
        # Medium questions (longer, more complex)
        medium_questions = [
            'Explain the process of photosynthesis and its importance in ecosystems',
            'Describe how gravitational force affects planetary motion and orbits',
            'Discuss the structure of atoms and the role of electrons in chemical bonding',
            'Analyze the factors that influence climate patterns across different regions',
            'Explain the relationship between DNA structure and genetic inheritance',
            'Describe the principles of thermodynamics and energy conservation',
            'Discuss the role of mitochondria in cellular respiration and energy production',
            'Analyze the causes and consequences of ocean currents on weather patterns',
            'Explain the concept of entropy and its applications in physics',
            'Describe the process of evolution and natural selection mechanisms',
        ]
        
        X = easy_questions + medium_questions
        y = [0] * len(easy_questions) + [1] * len(medium_questions)
        
        return X, y
    
    def train(self):
        """Train the difficulty classifier"""
        X, y = self.prepare_training_data()
        X_vec = self.vectorizer.fit_transform(X)
        self.model.fit(X_vec, y)
        
        # Evaluate
        y_pred = self.model.predict(X_vec)
        accuracy = accuracy_score(y, y_pred)
        f1 = f1_score(y, y_pred)
        
        print("\n" + "=" * 60)
        print("ML MODEL: QUIZ DIFFICULTY CLASSIFIER")
        print("=" * 60)
        print(f"Accuracy: {accuracy:.4f}")
        print(f"F1-Score: {f1:.4f}")
        print(f"Classification Report:\n{classification_report(y, y_pred, target_names=['Easy', 'Medium'])}")
        
        self.is_trained = True
        
        # Save model
        with open('quiz_model.pkl', 'wb') as f:
            pickle.dump((self.vectorizer, self.model), f)
        print("✓ Model saved to 'quiz_model.pkl'")
    
    def classify_difficulty(self, question):
        """Classify question difficulty"""
        if not self.is_trained:
            self.train()
        
        X_vec = self.vectorizer.transform([question])
        difficulty = self.model.predict(X_vec)[0]
        confidence = self.model.predict_proba(X_vec)[0].max()
        
        return 'Medium' if difficulty == 1 else 'Easy', confidence
    
    def generate_quiz(self, subject, num_questions=5, difficulty='Mixed'):
        """Generate quiz questions for a subject with difficulty filter"""
        quiz_templates = {
            'Mathematics': [
                'What is the fundamental theorem of algebra?',
                'Explain the concept of derivatives in calculus',
                'How do you solve quadratic equations?',
                'What is the difference between permutations and combinations?',
                'Describe the properties of logarithmic functions',
                'What is matrix multiplication and its applications?',
                'Explain the concept of limits in calculus',
                'How do you calculate standard deviation?',
            ],
            'Science': [
                'What is the law of conservation of energy?',
                'Explain the process of osmosis in cells',
                'What are the three states of matter?',
                'Describe the water cycle and its importance',
                'What is the periodic table and how is it organized?',
                'Explain photosynthesis and cellular respiration',
                'What is the structure of the solar system?',
                'Describe the process of mitosis and meiosis',
            ],
            'History': [
                'What were the main causes of World War I?',
                'Describe the impact of the Renaissance on European society',
                'What was the significance of the French Revolution?',
                'Explain the causes and effects of the Industrial Revolution',
                'What were the key events of the Cold War?',
                'Describe the structure of ancient Roman government',
                'What was the significance of the Magna Carta?',
                'Explain the causes of the American Civil War',
            ],
            'Literature': [
                'What are the main themes in Shakespearean tragedies?',
                'Describe the literary devices used in poetry',
                'What is the significance of symbolism in literature?',
                'Explain the difference between protagonist and antagonist',
                'What are the characteristics of the Romantic period?',
                'Describe the narrative techniques in modern fiction',
                'What is the importance of setting in storytelling?',
                'Explain the concept of irony in literature',
            ],
            'Computer Science': [
                'What is the difference between arrays and linked lists?',
                'Explain the concept of recursion in programming',
                'What is object-oriented programming and its principles?',
                'Describe the time complexity of common algorithms',
                'What is the difference between SQL and NoSQL databases?',
                'Explain the concept of inheritance in OOP',
                'What is the purpose of version control systems?',
                'Describe the layers of the OSI model',
            ]
        }
        
        questions = quiz_templates.get(subject, quiz_templates['Mathematics'])
        selected_questions = np.random.choice(questions, min(num_questions, len(questions)), replace=False)
        
        quiz = []
        for q in selected_questions:
            q_difficulty, confidence = self.classify_difficulty(q)
            
            if difficulty != 'Mixed' and q_difficulty != difficulty:
                continue
            
            quiz.append({
                'question': q,
                'difficulty': q_difficulty,
                'confidence': float(confidence),
                'options': self.generate_options(q)
            })
        
        while len(quiz) < num_questions and len(questions) > 0:
            q = np.random.choice(questions)
            q_difficulty, confidence = self.classify_difficulty(q)
            quiz.append({
                'question': q,
                'difficulty': q_difficulty,
                'confidence': float(confidence),
                'options': self.generate_options(q)
            })
        
        return quiz[:num_questions]
    
    def generate_options(self, question):
        """Generate multiple choice options"""
        correct_answers = {
            'What': 'A fundamental concept',
            'Explain': 'A detailed process',
            'Describe': 'A comprehensive overview',
            'How': 'A step-by-step method',
        }
        
        correct = correct_answers.get(question.split()[0], 'The correct answer')
        incorrect = [
            'An incorrect interpretation',
            'A false assumption',
            'A common misconception',
        ]
        
        options = [correct] + incorrect
        np.random.shuffle(options)
        
        return {
            'A': options[0],
            'B': options[1],
            'C': options[2],
            'D': options[3],
            'correct': chr(65 + options.index(correct))
        }


class ResourceSuggester:
    """Suggest resources using K-means clustering"""
    
    def __init__(self):
        self.kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        self.vectorizer = TfidfVectorizer(max_features=50, stop_words='english')
        self.is_trained = False
        
    def train(self, texts):
        """Train clustering model"""
        X = self.vectorizer.fit_transform(texts)
        self.kmeans.fit(X)
        self.is_trained = True
        
        print("\n" + "=" * 60)
        print("ML MODEL: TOPIC CLUSTERING FOR RESOURCES")
        print("=" * 60)
        print(f"Number of clusters: {self.kmeans.n_clusters}")
        print(f"Inertia: {self.kmeans.inertia_:.4f}")
        print("✓ Clustering model trained")
    
    def suggest_resources(self, subject):
        """Suggest resources for a subject"""
        resources = {
            'Mathematics': [
                'https://www.khanacademy.org/math',
                'https://www.mathway.com',
                'https://www.wolframalpha.com',
                'https://www.desmos.com/calculator',
                'https://www.brilliant.org/courses/algebra/',
            ],
            'Science': [
                'https://www.khanacademy.org/science',
                'https://www.sciencedaily.com',
                'https://www.nasa.gov',
                'https://www.nature.com',
                'https://www.sciencenews.org',
            ],
            'History': [
                'https://www.history.com',
                'https://www.britannica.com',
                'https://www.historytoday.com',
                'https://www.bbc.com/history',
                'https://www.nationalgeographic.com/history',
            ],
            'Literature': [
                'https://www.goodreads.com',
                'https://www.sparknotes.com',
                'https://www.cliffsnotes.com',
                'https://www.litcharts.com',
                'https://www.poetryfoundation.org',
            ],
            'Computer Science': [
                'https://www.codecademy.com',
                'https://www.coursera.org/courses?query=computer%20science',
                'https://www.github.com',
                'https://www.stackoverflow.com',
                'https://www.udemy.com/courses/search/?q=programming',
            ]
        }
        
        return resources.get(subject, resources['Mathematics'])


if __name__ == "__main__":
    print("\n🔄 Training ML models...\n")
    
    # Train quiz generator
    quiz_gen = QuizGenerator()
    quiz_gen.train()
    
    # Train resource suggester
    df = pd.read_csv('educational_texts.csv')
    suggester = ResourceSuggester()
    suggester.train(df['text'].tolist())
    
    # Test quiz generation
    print("\n" + "=" * 60)
    print("SAMPLE QUIZ GENERATION")
    print("=" * 60)
    sample_quiz = quiz_gen.generate_quiz('Mathematics', num_questions=3)
    for i, q in enumerate(sample_quiz, 1):
        print(f"\nQuestion {i}: {q['question']}")
        print(f"Difficulty: {q['difficulty']} (confidence: {q['confidence']:.2f})")
        print(f"Options: {q['options']}")
    
    print("\n✓ ML models training complete!")
