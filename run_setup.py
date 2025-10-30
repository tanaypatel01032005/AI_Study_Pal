"""
Main setup script to initialize all components
Run this first to set up the entire project
"""

import sys
import os

print("\n" + "=" * 70)
print("🚀 AI STUDY PAL - COMPLETE SETUP")
print("=" * 70)

# Step 1: Data Setup
print("\n[1/5] Setting up data pipeline...")
try:
    from data_setup import save_datasets
    text_df, user_df = save_datasets()
    print("✓ Data setup complete")
except Exception as e:
    print(f"✗ Error in data setup: {e}")
    sys.exit(1)

# Step 2: ML Models
print("\n[2/5] Training ML models...")
try:
    from ml_models import QuizGenerator, ResourceSuggester
    import pandas as pd
    
    quiz_gen = QuizGenerator()
    quiz_gen.train()
    
    df = pd.read_csv('educational_texts.csv')
    suggester = ResourceSuggester()
    suggester.train(df['text'].tolist())
    
    print("✓ ML models trained")
except Exception as e:
    print(f"✗ Error in ML training: {e}")
    sys.exit(1)

# Step 3: DL Models
print("\n[3/5] Training DL models...")
try:
    from dl_models import TextSummarizer, FeedbackGenerator
    
    summarizer = TextSummarizer()
    summarizer.train(epochs=30)
    
    feedback_gen = FeedbackGenerator()
    print("✓ DL models trained")
except Exception as e:
    print(f"✗ Error in DL training: {e}")
    sys.exit(1)

# Step 4: NLP Processor
print("\n[4/5] Testing NLP processor...")
try:
    from nlp_processor import StudyTipsGenerator
    
    nlp = StudyTipsGenerator()
    print("✓ NLP processor ready")
except Exception as e:
    print(f"✗ Error in NLP setup: {e}")
    sys.exit(1)

# Step 5: Study Plan Generator
print("\n[5/5] Testing study plan generator...")
try:
    from study_plan_generator import StudyPlanGenerator
    
    generator = StudyPlanGenerator()
    print("✓ Study plan generator ready")
except Exception as e:
    print(f"✗ Error in study plan setup: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✓ ALL COMPONENTS SUCCESSFULLY INITIALIZED!")
print("=" * 70)
print("\nNext steps:")
print("1. Install requirements: pip install -r requirements.txt")
print("2. Run the Flask app: python app.py")
print("3. Open browser: http://localhost:5000")
print("\n" + "=" * 70 + "\n")
