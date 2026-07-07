from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import json
from datetime import datetime
import os
import sys

try:
    from data_setup import educational_texts
    from ml_models import QuizGenerator, ResourceSuggester
    from dl_models import TextSummarizer, FeedbackGenerator
    from nlp_processor import StudyTipsGenerator
    from study_plan_generator import StudyPlanGenerator
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

app = Flask(__name__)

quiz_gen = None
suggester = None
summarizer = None
feedback_gen = None
nlp_processor = None
plan_generator = None

def initialize_models():
    """Initialize all models on first request"""
    global quiz_gen, suggester, summarizer, feedback_gen, nlp_processor, plan_generator
    
    if quiz_gen is not None:
        return  # Already initialized
    
    print("\n[APP] Initializing models...")
    
    try:
        quiz_gen = QuizGenerator()
        quiz_gen.train()
        print("✓ Quiz generator initialized")
    except Exception as e:
        print(f"✗ Error initializing quiz generator: {e}")
    
    try:
        df = pd.read_csv('educational_texts.csv')
        suggester = ResourceSuggester()
        suggester.train(df['text'].tolist())
        print("✓ Resource suggester initialized")
    except Exception as e:
        print(f"✗ Error initializing resource suggester: {e}")
    
    try:
        summarizer = TextSummarizer()
        print("✓ Text summarizer initialized")
    except Exception as e:
        print(f"✗ Error initializing summarizer: {e}")
    
    try:
        feedback_gen = FeedbackGenerator()
        print("✓ Feedback generator initialized")
    except Exception as e:
        print(f"✗ Error initializing feedback generator: {e}")
    
    try:
        nlp_processor = StudyTipsGenerator()
        print("✓ NLP processor initialized")
    except Exception as e:
        print(f"✗ Error initializing NLP processor: {e}")
    
    try:
        plan_generator = StudyPlanGenerator()
        print("✓ Study plan generator initialized")
    except Exception as e:
        print(f"✗ Error initializing study plan generator: {e}")

@app.before_request
def before_request():
    """Initialize models before first request"""
    initialize_models()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    """Get available subjects"""
    subjects = list(educational_texts.keys())
    return jsonify({'subjects': subjects})

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    """Generate study plan"""
    try:
        data = request.json
        subject = data.get('subject', 'Mathematics')
        hours = int(data.get('hours', 5))
        scenario = data.get('scenario', 'exam_prep')
        days = int(data.get('days', 5))
        
        plan = plan_generator.generate_study_plan(subject, hours, scenario, days)
        
        return jsonify(plan)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-quiz', methods=['POST'])
def generate_quiz():
    """Generate quiz"""
    try:
        data = request.json
        subject = data.get('subject', 'Mathematics')
        num_questions = int(data.get('num_questions', 5))
        difficulty = data.get('difficulty', 'Mixed')
        
        quiz = quiz_gen.generate_quiz(subject, num_questions, difficulty)
        
        return jsonify({'quiz': quiz})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/summarize', methods=['POST'])
def summarize():
    """Summarize text"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        summary = summarizer.summarize(text)
        
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-feedback', methods=['POST'])
def get_feedback():
    """Get motivational feedback"""
    try:
        data = request.json
        score = int(data.get('score', 50))
        subject = data.get('subject', 'General')
        
        feedback = feedback_gen.generate_feedback(score, subject)
        
        return jsonify({'feedback': feedback})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-tips', methods=['POST'])
def get_tips():
    """Get study tips"""
    try:
        data = request.json
        subject = data.get('subject', 'Mathematics')
        num_tips = int(data.get('num_tips', 3))
        
        tips = nlp_processor.generate_tips(subject, num_tips=num_tips)
        
        return jsonify({'tips': tips})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-resources', methods=['POST'])
def get_resources():
    """Get resource suggestions"""
    try:
        data = request.json
        subject = data.get('subject', 'Mathematics')
        
        resources = suggester.suggest_resources(subject)
        
        return jsonify({'resources': resources})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-plan', methods=['POST'])
def download_plan():
    """Download study plan as CSV"""
    try:
        data = request.json
        subject = data.get('subject', 'Mathematics')
        hours = int(data.get('hours', 5))
        scenario = data.get('scenario', 'exam_prep')
        days = int(data.get('days', 5))
        
        plan = plan_generator.generate_study_plan(subject, hours, scenario, days)
        filename, df = plan_generator.export_to_csv(plan)
        
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    """Analyze text"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        analysis = nlp_processor.analyze_text(text)
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/full-study-session', methods=['POST'])
def full_study_session():
    """Generate complete study session"""
    try:
        data = request.json
        subject = data.get('subject', 'Mathematics')
        hours = int(data.get('hours', 5))
        scenario = data.get('scenario', 'exam_prep')
        days = int(data.get('days', 5))
        text = data.get('text', '')
        
        # Generate all components
        plan = plan_generator.generate_study_plan(subject, hours, scenario, days)
        quiz = quiz_gen.generate_quiz(subject, num_questions=5)
        resources = suggester.suggest_resources(subject)
        tips = nlp_processor.generate_tips(subject, num_tips=3)
        
        summary = None
        if text:
            summary = summarizer.summarize(text)
        
        session = {
            'subject': subject,
            'hours': hours,
            'days': days,
            'scenario': scenario,
            'plan': plan,
            'quiz': quiz,
            'resources': resources,
            'tips': tips,
            'summary': summary,
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify(session)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 AI STUDY PAL - FLASK WEB APPLICATION")
    print("=" * 60)
    print("\nStarting Flask server...")
    print("Visit http://localhost:5000 to access the application")
    print("\n" + "=" * 60 + "\n")
    
    app.run(debug=True, port=5000)
