from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union
from enum import Enum

class QuestionType(Enum):
    SCALE = "scale"
    TEXT = "text"
    MULTIPLE_CHOICE = "multiple_choice"
    CHECKBOX = "checkbox"

@dataclass
class SurveyQuestion:
    id: str
    text: str
    type: QuestionType
    options: Optional[List[str]] = None
    scale_range: Optional[tuple] = None
    required: bool = True

@dataclass
class SurveyResponse:
    user_id: str
    timestamp: datetime
    question_id: str
    response: Union[str, int, List[str]]
    additional_notes: Optional[str] = None

@dataclass
class WeeklySurvey:
    id: str
    timestamp: datetime
    questions: List[SurveyQuestion]
    responses: List[SurveyResponse]
    completion_status: str

class SurveyManager:
    def __init__(self):
        # Initialize question banks for different survey types
        self.reflection_questions = [
            SurveyQuestion(
                id="reflect_001",
                text="How aligned do you feel with your recommended activities this week?",
                type=QuestionType.SCALE,
                scale_range=(1, 5)
            ),
            SurveyQuestion(
                id="reflect_002",
                text="Which activities provided the most value?",
                type=QuestionType.MULTIPLE_CHOICE,
                options=["Meditation", "Journaling", "Exercise", "Social Activities", "Learning"]
            ),
            SurveyQuestion(
                id="reflect_003",
                text="What challenges did you face this week?",
                type=QuestionType.TEXT
            ),
            SurveyQuestion(
                id="reflect_004",
                text="Select all areas where you noticed improvement:",
                type=QuestionType.CHECKBOX,
                options=[
                    "Mental Clarity",
                    "Emotional Balance",
                    "Physical Wellbeing",
                    "Social Connections",
                    "Professional Growth"
                ]
            ),
            SurveyQuestion(
                id="reflect_005",
                text="How would you rate your overall progress?",
                type=QuestionType.SCALE,
                scale_range=(1, 10)
            )
        ]

        self.progress_check_questions = [
            SurveyQuestion(
                id="prog_001",
                text="Rate your consistency with the recommended activities:",
                type=QuestionType.SCALE,
                scale_range=(1, 5)
            ),
            # Add more progress check questions...
        ]

        self.feedback_questions = [
            SurveyQuestion(
                id="feed_001",
                text="How well do the recommendations match your needs?",
                type=QuestionType.SCALE,
                scale_range=(1, 5)
            ),
            # Add more feedback questions...
        ]

    def generate_weekly_survey(self, user_id: str, week_number: int) -> WeeklySurvey:
        """Generate a weekly survey based on user's progress and previous responses"""
        
        # Customize questions based on week number
        custom_questions = self.reflection_questions.copy()
        
        if week_number > 1:
            custom_questions.extend([
                SurveyQuestion(
                    id=f"custom_{week_number}_001",
                    text="How has your perspective changed since last week?",
                    type=QuestionType.TEXT
                )
            ])
        
        if week_number % 4 == 0:  # Monthly check-in
            custom_questions.extend(self.progress_check_questions)
        
        return WeeklySurvey(
            id=f"survey_{user_id}_{week_number}",
            timestamp=datetime.now(),
            questions=custom_questions,
            responses=[],
            completion_status="pending"
        )

    def record_response(self, 
                       survey: WeeklySurvey, 
                       question_id: str, 
                       response: Union[str, int, List[str]], 
                       notes: Optional[str] = None) -> None:
        """Record a response to a survey question"""
        
        survey_response = SurveyResponse(
            user_id=survey.id.split('_')[1],
            timestamp=datetime.now(),
            question_id=question_id,
            response=response,
            additional_notes=notes
        )
        
        survey.responses.append(survey_response)
        
        # Update completion status
        response_questions = set(r.question_id for r in survey.responses)
        required_questions = set(q.id for q in survey.questions if q.required)
        
        if response_questions >= required_questions:
            survey.completion_status = "completed"
        else:
            survey.completion_status = "in_progress"

    def analyze_responses(self, survey: WeeklySurvey) -> Dict[str, any]:
        """Analyze survey responses to generate insights"""
        
        analysis = {
            "completion_rate": len(survey.responses) / len(survey.questions) * 100,
            "average_scale_rating": 0,
            "key_challenges": [],
            "improvement_areas": [],
            "summary": ""
        }

        scale_responses = []
        
        for response in survey.responses:
            question = next((q for q in survey.questions if q.id == response.question_id), None)
            
            if question and question.type == QuestionType.SCALE:
                scale_responses.append(response.response)
            elif question and question.type == QuestionType.TEXT:
                if "challenge" in question.text.lower():
                    analysis["key_challenges"].append(response.response)
            elif question and question.type == QuestionType.CHECKBOX:
                if "improvement" in question.text.lower():
                    analysis["improvement_areas"].extend(response.response)

        if scale_responses:
            analysis["average_scale_rating"] = sum(scale_responses) / len(scale_responses)

        # Generate summary
        analysis["summary"] = (
            f"Survey completed at {survey.completion_rate:.1f}% rate. "
            f"Average rating: {analysis['average_scale_rating']:.1f}/5. "
            f"Key improvements noted in: {', '.join(analysis['improvement_areas'][:3])}."
        )

        return analysis

    def get_test_data(self) -> tuple[WeeklySurvey, Dict]:
        """Generate test data for development purposes"""
        # Create test survey
        test_survey = self.generate_weekly_survey("test_user", 1)
        
        # Add some test responses
        self.record_response(test_survey, "reflect_001", 4)
        self.record_response(test_survey, "reflect_002", ["Meditation", "Journaling"])
        self.record_response(test_survey, "reflect_003", "Time management was challenging")
        self.record_response(test_survey, "reflect_004", ["Mental Clarity", "Emotional Balance"])
        self.record_response(test_survey, "reflect_005", 8)
        
        # Analyze responses
        analysis = self.analyze_responses(test_survey)
        
        return test_survey, analysis

def test_survey_manager():
    """Test function to verify basic functionality"""
    manager = SurveyManager()
    test_survey, analysis = manager.get_test_data()
    
    print("\nSurvey Manager Test Results:")
    
    print("\nSurvey Questions:")
    for question in test_survey.questions:
        print(f"\n- Question ID: {question.id}")
        print(f"  Text: {question.text}")
        print(f"  Type: {question.type.value}")
        if question.options:
            print(f"  Options: {', '.join(question.options)}")
        if question.scale_range:
            print(f"  Scale: {question.scale_range}")
            
    print("\nSurvey Responses:")
    for response in test_survey.responses:
        print(f"\n- Question ID: {response.question_id}")
        print(f"  Response: {response.response}")
        if response.additional_notes:
            print(f"  Notes: {response.additional_notes}")
            
    print("\nResponse Analysis:")
    for key, value in analysis.items():
        print(f"- {key}: {value}")
    
    return test_survey, analysis

if __name__ == "__main__":
    test_survey_manager()
