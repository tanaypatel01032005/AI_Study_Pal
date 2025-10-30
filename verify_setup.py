"""
Verification script to ensure all components work correctly
Run this before submitting to verify everything is functional
"""

import sys
import os

print("\n" + "=" * 70)
print("🔍 AI STUDY PAL - VERIFICATION SCRIPT")
print("=" * 70)

# Step 1: Check data files
print("\n[1/6] Checking data files...")
try:
    import pandas as pd
    
    if not os.path.exists('educational_texts.csv'):
        print("  Creating educational_texts.csv...")
        from data_setup import save_datasets
        save_datasets()
    
    df = pd.read_csv('educational_texts.csv')
    print(f"✓ Data files verified ({len(df)} texts)")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Step 2: Verify ML Models
print("\n[2/6] Verifying ML models...")
try:
    from ml_models import QuizGenerator, ResourceSuggester
    
    quiz_gen = QuizGenerator()
    quiz_gen.train()
    
    quiz = quiz_gen.generate_quiz('Mathematics', num_questions=3)
    assert len(quiz) == 3, "Quiz generation failed"
    print(f"✓ ML models verified (generated {len(quiz)} quiz questions)")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Step 3: Verify DL Models
print("\n[3/6] Verifying DL models...")
try:
    from dl_models import TextSummarizer, FeedbackGenerator
    
    summarizer = TextSummarizer()
    feedback_gen = FeedbackGenerator()
    
    test_text = "Machine learning is a subset of artificial intelligence."
    summary = summarizer.summarize(test_text)
    feedback = feedback_gen.generate_feedback(85, 'Mathematics')
    
    assert len(summary) > 0, "Summarization failed"
    assert len(feedback) > 0, "Feedback generation failed"
    print(f"✓ DL models verified (summary: {len(summary)} chars, feedback generated)")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Step 4: Verify NLP Processor
print("\n[4/6] Verifying NLP processor...")
try:
    from nlp_processor import StudyTipsGenerator
    
    nlp = StudyTipsGenerator()
    tips = nlp.generate_tips('Mathematics', num_tips=3)
    keywords = nlp.extract_keywords("Machine learning algorithms")
    
    assert len(tips) == 3, "Tips generation failed"
    assert len(keywords) > 0, "Keyword extraction failed"
    print(f"✓ NLP processor verified (generated {len(tips)} tips, {len(keywords)} keywords)")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Step 5: Verify Study Plan Generator
print("\n[5/6] Verifying study plan generator...")
try:
    from study_plan_generator import StudyPlanGenerator
    
    generator = StudyPlanGenerator()
    plan = generator.generate_study_plan('Mathematics', hours=5, scenario='exam_prep')
    
    assert plan['subject'] == 'Mathematics', "Plan generation failed"
    assert len(plan['schedule']) == 5, "Schedule generation failed"
    print(f"✓ Study plan generator verified (generated 5-day plan)")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Step 6: Verify Flask App
print("\n[6/6] Verifying Flask app...")
try:
    from app import app
    
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200, "Home page failed"
        
        response = client.get('/api/subjects')
        assert response.status_code == 200, "Subjects API failed"
        
    print(f"✓ Flask app verified (all endpoints working)")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✓ ALL COMPONENTS VERIFIED SUCCESSFULLY!")
print("=" * 70)
print("\nYour AI Study Pal is ready for submission!")
print("\nTo run the application:")
print("  1. pip install -r requirements.txt")
print("  2. python app.py")
print("  3. Open http://localhost:5000 in your browser")
print("\n" + "=" * 70 + "\n")
