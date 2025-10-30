import pandas as pd
import json
from datetime import datetime, timedelta

class StudyPlanGenerator:
    """Generate personalized study plans"""
    
    def __init__(self):
        self.scenarios = {
            'exam_prep': {
                'intensity': 'high',
                'focus': 'comprehensive review and practice',
                'frequency': 'daily'
            },
            'homework': {
                'intensity': 'medium',
                'focus': 'specific topics and problem-solving',
                'frequency': 'as needed'
            },
            'project': {
                'intensity': 'medium',
                'focus': 'research and application',
                'frequency': 'regular'
            }
        }
    
    def generate_study_plan(self, subject, hours, scenario='exam_prep', days=None):
        """Generate a detailed study plan
        
        Args:
            subject: Subject to study
            hours: Total study hours
            scenario: Type of study scenario
            days: Number of days (if None, defaults to 5)
        """
        if days is None:
            days = 5
        
        scenario_info = self.scenarios.get(scenario, self.scenarios['exam_prep'])
        
        plan = {
            'subject': subject,
            'total_hours': hours,
            'total_days': days,
            'scenario': scenario,
            'intensity': scenario_info['intensity'],
            'focus': scenario_info['focus'],
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'schedule': self.create_schedule(subject, hours, scenario, days)
        }
        
        return plan
    
    def create_schedule(self, subject, hours, scenario, days=5):
        """Create a detailed daily schedule
        
        Args:
            subject: Subject to study
            hours: Total study hours
            scenario: Type of study scenario
            days: Number of days to spread the study
        """
        daily_hours = hours / days
        
        schedule = []
        start_date = datetime.now()
        
        activities = {
            'Mathematics': [
                'Review fundamental concepts',
                'Solve practice problems',
                'Work on challenging topics',
                'Complete practice tests',
                'Review mistakes and reinforce'
            ],
            'Science': [
                'Read and understand concepts',
                'Create visual diagrams',
                'Conduct experiments or simulations',
                'Solve application problems',
                'Review and consolidate learning'
            ],
            'History': [
                'Read historical context',
                'Create timelines',
                'Analyze primary sources',
                'Connect events and causes',
                'Review key dates and figures'
            ],
            'Literature': [
                'Read assigned texts',
                'Analyze themes and characters',
                'Study literary devices',
                'Write analysis essays',
                'Discuss and review'
            ],
            'Computer Science': [
                'Study algorithms and concepts',
                'Write and test code',
                'Debug and optimize',
                'Solve coding problems',
                'Review best practices'
            ]
        }
        
        activities_list = activities.get(subject, activities['Mathematics'])
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            day_schedule = {
                'day': day + 1,
                'date': current_date.strftime('%Y-%m-%d'),
                'hours': round(daily_hours, 1),
                'activities': activities_list[day % len(activities_list)],
                'time_slots': self.create_time_slots(daily_hours)
            }
            schedule.append(day_schedule)
        
        return schedule
    
    def create_time_slots(self, hours):
        """Create time slots for the day"""
        slots = []
        start_hour = 9  # Start at 9 AM
        
        # Break into 1-hour slots
        num_slots = int(hours)
        for i in range(num_slots):
            end_hour = start_hour + 1
            slots.append({
                'slot': f"{start_hour}:00 - {end_hour}:00",
                'duration': '1 hour',
                'activity': f'Study session {i+1}'
            })
            start_hour = end_hour
        
        return slots
    
    def export_to_csv(self, plan, filename=None):
        """Export study plan to CSV"""
        if filename is None:
            filename = f"study_plan_{plan['subject']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        rows = []
        for day_plan in plan['schedule']:
            for slot in day_plan['time_slots']:
                rows.append({
                    'Date': day_plan['date'],
                    'Day': f"Day {day_plan['day']}",
                    'Time': slot['slot'],
                    'Activity': day_plan['activities'],
                    'Duration': slot['duration'],
                    'Subject': plan['subject'],
                    'Scenario': plan['scenario']
                })
        
        df = pd.DataFrame(rows)
        df.to_csv(filename, index=False)
        
        return filename, df


if __name__ == "__main__":
    print("\n🔄 Testing study plan generator...\n")
    
    generator = StudyPlanGenerator()
    
    # Generate sample plans
    print("=" * 60)
    print("STUDY PLAN GENERATION")
    print("=" * 60)
    
    subjects = ['Mathematics', 'Science', 'History']
    scenarios = ['exam_prep', 'homework', 'project']
    
    for subject in subjects:
        for scenario in scenarios:
            plan = generator.generate_study_plan(subject, hours=5, scenario=scenario, days=5)
            filename, df = generator.export_to_csv(plan)
            print(f"\n✓ Generated plan for {subject} ({scenario})")
            print(f"  Exported to: {filename}")
            print(f"  Total entries: {len(df)}")
    
    print("\n✓ Study plan generation complete!")
