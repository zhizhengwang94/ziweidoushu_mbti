from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta

@dataclass
class Activity:
    id: str
    name: str
    description: str
    category: str
    frequency: str  # daily, weekly, monthly
    duration: str   # estimated time commitment
    difficulty: str # beginner, intermediate, advanced
    benefits: List[str]
    prerequisites: List[str]

@dataclass
class RecommendationPlan:
    core_activities: List[Activity]
    optional_activities: List[Activity]
    weekly_goals: List[str]
    monthly_milestones: List[str]
    progress_metrics: Dict[str, str]
    schedule_suggestion: Dict[str, List[str]]

class RecommendationEngine:
    def __init__(self):
        # Initialize activity database
        self.activities_db = {
            "physical": [
                Activity(
                    id="med_001",
                    name="Mindfulness Meditation",
                    description="Daily meditation practice focusing on breath and presence",
                    category="physical",
                    frequency="daily",
                    duration="15-20 minutes",
                    difficulty="beginner",
                    benefits=["Stress reduction", "Mental clarity", "Emotional balance"],
                    prerequisites=["Quiet space", "Comfortable seating"]
                ),
                # More physical activities...
            ],
            "mental": [
                Activity(
                    id="jour_001",
                    name="Reflective Journaling",
                    description="Structured daily writing for self-reflection",
                    category="mental",
                    frequency="daily",
                    duration="20-30 minutes",
                    difficulty="beginner",
                    benefits=["Self-awareness", "Emotional processing", "Goal clarity"],
                    prerequisites=["Journal", "Quiet time"]
                ),
                # More mental activities...
            ],
            "social": [
                Activity(
                    id="net_001",
                    name="Professional Networking",
                    description="Regular participation in industry events or online communities",
                    category="social",
                    frequency="weekly",
                    duration="1-2 hours",
                    difficulty="intermediate",
                    benefits=["Career growth", "Knowledge sharing", "Relationship building"],
                    prerequisites=["Professional profile", "Communication skills"]
                ),
                # More social activities...
            ]
        }

        # Define progression paths
        self.progression_paths = {
            "self_awareness": [
                "Mindfulness Meditation",
                "Reflective Journaling",
                "Body Scanning Practice"
            ],
            "social_skills": [
                "Professional Networking",
                "Public Speaking Practice",
                "Group Discussions"
            ],
            # More paths...
        }

    def _select_activities(self, 
                          personality_traits: List[str], 
                          growth_areas: List[str]) -> List[Activity]:
        """Select appropriate activities based on personality and growth areas"""
        selected_activities = []
        
        # Match activities to growth areas
        for area in growth_areas:
            area_lower = area.lower()
            for category in self.activities_db.values():
                for activity in category:
                    if any(benefit.lower() in area_lower for benefit in activity.benefits):
                        selected_activities.append(activity)
        
        return selected_activities[:5]  # Limit to top 5 most relevant activities

    def _create_schedule(self, activities: List[Activity]) -> Dict[str, List[str]]:
        """Create a weekly schedule suggestion"""
        schedule = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Weekend": []
        }

        # Distribute activities across the week
        for activity in activities:
            if activity.frequency == "daily":
                for day in schedule.keys():
                    schedule[day].append(f"{activity.name} ({activity.duration})")
            elif activity.frequency == "weekly":
                # Assign to least busy day
                min_day = min(schedule.keys(), key=lambda k: len(schedule[k]))
                schedule[min_day].append(f"{activity.name} ({activity.duration})")

        return schedule

    def _generate_progress_metrics(self, activities: List[Activity]) -> Dict[str, str]:
        """Define how to measure progress for each activity"""
        metrics = {}
        for activity in activities:
            if activity.frequency == "daily":
                metrics[activity.name] = "Daily completion rate (%)"
            elif activity.frequency == "weekly":
                metrics[activity.name] = "Weekly engagement score (1-5)"
            # Add more metric types as needed
        return metrics

    def generate_plan(self, 
                     personality_traits: List[str], 
                     growth_areas: List[str]) -> RecommendationPlan:
        """Generate a comprehensive recommendation plan"""
        
        # Select core and optional activities
        all_activities = self._select_activities(personality_traits, growth_areas)
        core_activities = all_activities[:3]
        optional_activities = all_activities[3:]

        # Generate weekly goals
        weekly_goals = [
            f"Complete {activity.frequency} practice of {activity.name}"
            for activity in core_activities
        ]

        # Generate monthly milestones
        monthly_milestones = [
            "Establish regular practice routine",
            "Complete first progress assessment",
            "Adjust activities based on feedback",
            "Share experiences with community"
        ]

        # Create schedule and metrics
        schedule = self._create_schedule(core_activities)
        metrics = self._generate_progress_metrics(all_activities)

        return RecommendationPlan(
            core_activities=core_activities,
            optional_activities=optional_activities,
            weekly_goals=weekly_goals,
            monthly_milestones=monthly_milestones,
            progress_metrics=metrics,
            schedule_suggestion=schedule
        )

    def get_test_data(self) -> RecommendationPlan:
        """Generate test data for development purposes"""
        test_traits = ["Analytical", "Strategic", "Independent"]
        test_growth = ["Emotional awareness", "Social connection", "Physical wellness"]
        return self.generate_plan(test_traits, test_growth)

def test_recommendation_engine():
    """Test function to verify basic functionality"""
    engine = RecommendationEngine()
    result = engine.get_test_data()
    
    print("\nRecommendation Plan Test Results:")
    
    print("\nCore Activities:")
    for activity in result.core_activities:
        print(f"\n- {activity.name}:")
        print(f"  Description: {activity.description}")
        print(f"  Frequency: {activity.frequency}")
        print(f"  Benefits: {', '.join(activity.benefits)}")
        
    print("\nWeekly Goals:")
    for goal in result.weekly_goals:
        print(f"- {goal}")
        
    print("\nMonthly Milestones:")
    for milestone in result.monthly_milestones:
        print(f"- {milestone}")
        
    print("\nSchedule Suggestion:")
    for day, activities in result.schedule_suggestion.items():
        print(f"\n{day}:")
        for activity in activities:
            print(f"- {activity}")
            
    print("\nProgress Metrics:")
    for activity, metric in result.progress_metrics.items():
        print(f"- {activity}: {metric}")
    
    return result

if __name__ == "__main__":
    test_recommendation_engine()
