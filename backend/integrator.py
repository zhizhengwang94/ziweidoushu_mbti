from datetime import datetime
from typing import Dict, Optional

from processors.ziwei_processor import ZiWeiProcessor
from processors.mbti_processor import MBTIProcessor
from processors.combined_analyzer import CombinedAnalyzer
from insights.analyzer import InsightAnalyzer
from insights.recommendations import RecommendationEngine
from tracking.survey_manager import SurveyManager
from tracking.progress_tracker import ProgressTracker
from visualization.chart_generator import ChartGenerator

class SystemIntegrator:
    def __init__(self):
        # Initialize all components
        self.combined_analyzer = CombinedAnalyzer()
        self.insight_analyzer = InsightAnalyzer()
        self.recommendation_engine = RecommendationEngine()
        self.survey_manager = SurveyManager()
        self.progress_tracker = ProgressTracker()
        self.chart_generator = ChartGenerator()
        
        # Store user states
        self.user_states = {}

    def process_initial_analysis(self, 
                               user_id: str,
                               birth_date: str,
                               birth_time: str,
                               mbti_type: str) -> Dict:
        """Process initial user analysis and setup"""
        try:
            # Convert date string to datetime
            birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
            
            # Get combined analysis
            combined_analysis = self.combined_analyzer.analyze(birth_datetime, mbti_type)
            
            # Generate detailed insights
            detailed_insights = self.insight_analyzer.analyze(combined_analysis)
            
            # Generate recommendations
            personality_traits = combined_analysis.natural_tendencies
            growth_areas = combined_analysis.growth_areas
            recommendation_plan = self.recommendation_engine.generate_plan(
                personality_traits,
                growth_areas
            )
            
            # Store user state
            self.user_states[user_id] = {
                'birth_datetime': birth_datetime,
                'mbti_type': mbti_type,
                'combined_analysis': combined_analysis,
                'detailed_insights': detailed_insights,
                'recommendation_plan': recommendation_plan,
                'surveys': [],
                'progress_snapshots': []
            }
            
            return {
                'success': True,
                'data': {
                    'natural_tendencies': combined_analysis.natural_tendencies,
                    'current_state': combined_analysis.current_state,
                    'growth_areas': combined_analysis.growth_areas,
                    'recommendations': recommendation_plan.core_activities,
                    'personality_insights': detailed_insights.personality_insights,
                    'career_insights': detailed_insights.career_insights,
                    'relationship_insights': detailed_insights.relationship_insights
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def generate_weekly_survey(self, user_id: str) -> Dict:
        """Generate weekly survey for user"""
        try:
            user_state = self.user_states.get(user_id)
            if not user_state:
                raise ValueError("User not found")
                
            survey_count = len(user_state['surveys'])
            survey = self.survey_manager.generate_weekly_survey(user_id, survey_count + 1)
            user_state['surveys'].append(survey)
            
            return {
                'success': True,
                'data': {
                    'survey_id': survey.id,
                    'questions': [
                        {
                            'id': q.id,
                            'text': q.text,
                            'type': q.type.value,
                            'options': q.options if q.options else None,
                            'scale_range': q.scale_range if q.scale_range else None
                        }
                        for q in survey.questions
                    ]
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def process_survey_response(self, 
                              user_id: str,
                              survey_id: str,
                              responses: Dict) -> Dict:
        """Process user's survey responses"""
        try:
            user_state = self.user_states.get(user_id)
            if not user_state:
                raise ValueError("User not found")
                
            # Find the relevant survey
            survey = next((s for s in user_state['surveys'] if s.id == survey_id), None)
            if not survey:
                raise ValueError("Survey not found")
                
            # Record responses
            for question_id, response in responses.items():
                self.survey_manager.record_response(
                    survey,
                    question_id,
                    response
                )
                
            # Generate progress snapshot if survey is complete
            if survey.completion_status == "completed":
                snapshot = self.progress_tracker.create_snapshot(
                    user_id,
                    user_state.get('progress_metrics', []),
                    {'survey_responses': responses}
                )
                user_state['progress_snapshots'].append(snapshot)
                
            # Generate visualization data
            charts = self.generate_visualization_data(user_id)
            
            return {
                'success': True,
                'data': {
                    'completion_status': survey.completion_status,
                    'progress_snapshot': {
                        'overall_score': snapshot.overall_score if survey.completion_status == "completed" else None,
                        'key_insights': snapshot.key_insights if survey.completion_status == "completed" else [],
                        'recommendations': snapshot.recommendations if survey.completion_status == "completed" else []
                    },
                    'charts': charts
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def generate_visualization_data(self, user_id: str) -> Dict:
        """Generate visualization data for user progress"""
        try:
            user_state = self.user_states.get(user_id)
            if not user_state:
                raise ValueError("User not found")
                
            snapshots = user_state.get('progress_snapshots', [])
            if not snapshots:
                return {}
                
            current_snapshot = snapshots[-1]
            previous_snapshot = snapshots[-2] if len(snapshots) > 1 else None
            
            # Prepare data for chart generator
            metrics_data = [
                {
                    'timestamp': s.timestamp,
                    'score': s.overall_score
                }
                for s in snapshots
            ]
            
            activities_data = {
                activity_id: {
                    'completion_rate': progress.completion_rate,
                    'impact_rating': progress.impact_rating
                }
                for activity_id, progress in current_snapshot.activities.items()
            }
            
            current_metrics = {
                area.value: score
                for area, score in current_snapshot.metrics.items()
            }
            
            previous_metrics = {
                area.value: score
                for area, score in previous_snapshot.metrics.items()
            } if previous_snapshot else {}
            
            # Generate charts
            chart_collection = self.chart_generator.generate_chart_collection(
                metrics_data,
                activities_data,
                current_metrics,
                previous_metrics,
                {'insights': []} # Placeholder for insights data
            )
            
            return {
                'progress_chart': chart_collection.progress_chart,
                'activity_chart': chart_collection.activity_chart,
                'comparison_chart': chart_collection.comparison_chart,
                'insight_chart': chart_collection.insight_chart
            }
            
        except Exception as e:
            return {}

    def get_test_data(self) -> Dict:
        """Generate test data for development purposes"""
        test_user_id = "test_user"
        
        # Process initial analysis
        initial_result = self.process_initial_analysis(
            test_user_id,
            "1990-01-01",
            "12:00",
            "INTJ"
        )
        
        # Generate survey
        survey_result = self.generate_weekly_survey(test_user_id)
        
        # Process mock survey response
        response_result = self.process_survey_response(
            test_user_id,
            survey_result['data']['survey_id'],
            {
                'reflect_001': 4,
                'reflect_002': ['Meditation', 'Journaling'],
                'reflect_003': "Making good progress",
                'reflect_004': ["Mental Clarity", "Emotional Balance"],
                'reflect_005': 8
            }
        )
        
        return {
            'initial_analysis': initial_result,
            'survey': survey_result,
            'survey_response': response_result
        }

def test_integrator():
    """Test function to verify basic functionality"""
    integrator = SystemIntegrator()
    test_results = integrator.get_test_data()
    
    print("\nSystem Integrator Test Results:")
    
    print("\nInitial Analysis:")
    if test_results['initial_analysis']['success']:
        data = test_results['initial_analysis']['data']
        print("\nNatural Tendencies:")
        for tendency in data['natural_tendencies']:
            print(f"- {tendency}")
            
        print("\nGrowth Areas:")
        for area in data['growth_areas']:
            print(f"- {area}")
            
    print("\nSurvey Generation:")
    if test_results['survey']['success']:
        print(f"Survey ID: {test_results['survey']['data']['survey_id']}")
        print("\nQuestions:")
        for question in test_results['survey']['data']['questions']:
            print(f"- {question['text']}")
            
    print("\nSurvey Response Processing:")
    if test_results['survey_response']['success']:
        data = test_results['survey_response']['data']
        print(f"Completion Status: {data['completion_status']}")
        if data.get('progress_snapshot'):
            print(f"Overall Score: {data['progress_snapshot']['overall_score']}")
            print("\nKey Insights:")
            for insight in data['progress_snapshot']['key_insights']:
                print(f"- {insight}")
    
    return test_results

if __name__ == "__main__":
    test_integrator()
