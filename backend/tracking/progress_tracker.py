from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum
import json

class ProgressArea(Enum):
    PERSONAL_GROWTH = "personal_growth"
    EMOTIONAL_INTELLIGENCE = "emotional_intelligence"
    SOCIAL_SKILLS = "social_skills"
    PROFESSIONAL_DEVELOPMENT = "professional_development"
    PHYSICAL_WELLBEING = "physical_wellbeing"

@dataclass
class ProgressMetric:
    area: ProgressArea
    score: float
    timestamp: datetime
    notes: Optional[str] = None

@dataclass
class ActivityProgress:
    activity_id: str
    completion_rate: float
    consistency_score: float
    impact_rating: float
    notes: List[str]

@dataclass
class ProgressSnapshot:
    user_id: str
    timestamp: datetime
    metrics: Dict[ProgressArea, float]
    activities: Dict[str, ActivityProgress]
    overall_score: float
    key_insights: List[str]
    recommendations: List[str]

class ProgressTracker:
    def __init__(self):
        self.weight_factors = {
            ProgressArea.PERSONAL_GROWTH: 1.0,
            ProgressArea.EMOTIONAL_INTELLIGENCE: 1.0,
            ProgressArea.SOCIAL_SKILLS: 1.0,
            ProgressArea.PROFESSIONAL_DEVELOPMENT: 1.0,
            ProgressArea.PHYSICAL_WELLBEING: 1.0
        }

    def calculate_activity_progress(self, 
                                  activity_id: str,
                                  survey_responses: List[Dict]) -> ActivityProgress:
        """Calculate progress metrics for a specific activity"""
        # Simulate progress calculation from survey responses
        completion_count = sum(1 for resp in survey_responses if resp.get('completed', False))
        total_responses = len(survey_responses)
        
        completion_rate = completion_count / total_responses if total_responses > 0 else 0
        
        # Calculate consistency score (0-1)
        consecutive_completions = 0
        max_consecutive = 0
        for resp in survey_responses:
            if resp.get('completed', False):
                consecutive_completions += 1
                max_consecutive = max(max_consecutive, consecutive_completions)
            else:
                consecutive_completions = 0
        
        consistency_score = max_consecutive / total_responses if total_responses > 0 else 0
        
        # Calculate impact rating (0-5)
        impact_ratings = [resp.get('impact_rating', 0) for resp in survey_responses]
        impact_rating = sum(impact_ratings) / len(impact_ratings) if impact_ratings else 0
        
        return ActivityProgress(
            activity_id=activity_id,
            completion_rate=completion_rate,
            consistency_score=consistency_score,
            impact_rating=impact_rating,
            notes=[resp.get('notes', '') for resp in survey_responses if resp.get('notes')]
        )

    def calculate_area_score(self, 
                           area: ProgressArea,
                           metrics: List[ProgressMetric]) -> float:
        """Calculate score for a specific progress area"""
        if not metrics:
            return 0.0
            
        # Get recent metrics for this area
        area_metrics = [m for m in metrics if m.area == area]
        if not area_metrics:
            return 0.0
            
        # Calculate weighted average, giving more weight to recent metrics
        total_weight = 0
        weighted_sum = 0
        
        for i, metric in enumerate(sorted(area_metrics, key=lambda x: x.timestamp)):
            weight = 1 + (i * 0.1)  # Increase weight for more recent metrics
            weighted_sum += metric.score * weight
            total_weight += weight
            
        return weighted_sum / total_weight if total_weight > 0 else 0

    def generate_insights(self, 
                         current_snapshot: ProgressSnapshot,
                         previous_snapshot: Optional[ProgressSnapshot]) -> List[str]:
        """Generate insights based on progress comparison"""
        insights = []
        
        # Analyze overall progress
        if previous_snapshot:
            score_diff = current_snapshot.overall_score - previous_snapshot.overall_score
            if score_diff > 0:
                insights.append(f"Overall progress improved by {score_diff:.1f}%")
            elif score_diff < 0:
                insights.append(f"Overall progress decreased by {abs(score_diff):.1f}%")
                
            # Analyze area-specific progress
            for area in ProgressArea:
                curr_score = current_snapshot.metrics.get(area, 0)
                prev_score = previous_snapshot.metrics.get(area, 0)
                diff = curr_score - prev_score
                
                if abs(diff) >= 0.1:  # Only report significant changes
                    direction = "improved" if diff > 0 else "decreased"
                    insights.append(
                        f"{area.value.replace('_', ' ').title()} {direction} by {abs(diff):.1f}%"
                    )
        
        # Analyze activity progress
        for activity_id, progress in current_snapshot.activities.items():
            if progress.completion_rate >= 0.8:
                insights.append(f"Strong consistency in {activity_id} with {progress.completion_rate*100:.1f}% completion")
            elif progress.completion_rate <= 0.3:
                insights.append(f"May need support with {activity_id} ({progress.completion_rate*100:.1f}% completion)")
                
        return insights

    def generate_recommendations(self, 
                               snapshot: ProgressSnapshot) -> List[str]:
        """Generate recommendations based on current progress"""
        recommendations = []
        
        # Analyze areas needing improvement
        for area, score in snapshot.metrics.items():
            if score < 0.4:
                recommendations.append(f"Focus on improving {area.value.replace('_', ' ')}")
                
        # Analyze activity engagement
        for activity_id, progress in snapshot.activities.items():
            if progress.consistency_score < 0.5:
                recommendations.append(f"Work on building consistency in {activity_id}")
            if progress.impact_rating < 3:
                recommendations.append(f"Consider adjusting approach to {activity_id} for better results")
                
        return recommendations

    def create_snapshot(self, 
                       user_id: str,
                       metrics: List[ProgressMetric],
                       activity_responses: Dict[str, List[Dict]]) -> ProgressSnapshot:
        """Create a progress snapshot for the current state"""
        
        # Calculate metrics for each area
        area_metrics = {}
        for area in ProgressArea:
            area_metrics[area] = self.calculate_area_score(area, metrics)
            
        # Calculate activity progress
        activity_progress = {}
        for activity_id, responses in activity_responses.items():
            activity_progress[activity_id] = self.calculate_activity_progress(
                activity_id, responses
            )
            
        # Calculate overall score
        overall_score = sum(area_metrics.values()) / len(area_metrics)
        
        # Create snapshot
        snapshot = ProgressSnapshot(
            user_id=user_id,
            timestamp=datetime.now(),
            metrics=area_metrics,
            activities=activity_progress,
            overall_score=overall_score,
            key_insights=[],  # Will be filled after comparison
            recommendations=[]  # Will be filled after analysis
        )
        
        # Generate insights and recommendations
        snapshot.key_insights = self.generate_insights(snapshot, None)
        snapshot.recommendations = self.generate_recommendations(snapshot)
        
        return snapshot

    def get_test_data(self) -> ProgressSnapshot:
        """Generate test data for development purposes"""
        # Create test metrics
        test_metrics = [
            ProgressMetric(ProgressArea.PERSONAL_GROWTH, 0.75, datetime.now()),
            ProgressMetric(ProgressArea.EMOTIONAL_INTELLIGENCE, 0.65, datetime.now()),
            ProgressMetric(ProgressArea.SOCIAL_SKILLS, 0.80, datetime.now())
        ]
        
        # Create test activity responses
        test_responses = {
            "meditation": [
                {"completed": True, "impact_rating": 4, "notes": "Felt more focused"},
                {"completed": True, "impact_rating": 4, "notes": "Good session"}
            ],
            "journaling": [
                {"completed": True, "impact_rating": 3, "notes": "Helped reflect"},
                {"completed": False, "impact_rating": 0, "notes": "Missed session"}
            ]
        }
        
        return self.create_snapshot("test_user", test_metrics, test_responses)

def test_progress_tracker():
    """Test function to verify basic functionality"""
    tracker = ProgressTracker()
    snapshot = tracker.get_test_data()
    
    print("\nProgress Tracker Test Results:")
    
    print("\nOverall Progress:")
    print(f"Score: {snapshot.overall_score:.2f}")
    
    print("\nArea Metrics:")
    for area, score in snapshot.metrics.items():
        print(f"- {area.value}: {score:.2f}")
        
    print("\nActivity Progress:")
    for activity_id, progress in snapshot.activities.items():
        print(f"\n{activity_id}:")
        print(f"- Completion Rate: {progress.completion_rate:.2f}")
        print(f"- Consistency Score: {progress.consistency_score:.2f}")
        print(f"- Impact Rating: {progress.impact_rating:.2f}")
        if progress.notes:
            print("- Notes:")
            for note in progress.notes:
                print(f"  * {note}")
                
    print("\nKey Insights:")
    for insight in snapshot.key_insights:
        print(f"- {insight}")
        
    print("\nRecommendations:")
    for recommendation in snapshot.recommendations:
        print(f"- {recommendation}")
    
    return snapshot

if __name__ == "__main__":
    test_progress_tracker()
