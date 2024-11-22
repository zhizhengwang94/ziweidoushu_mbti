from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from processors.combined_analyzer import CombinedAnalysis

@dataclass
class DetailedInsights:
    personality_insights: List[str]
    career_insights: List[str]
    relationship_insights: List[str]
    development_path: List[str]
    recommended_activities: Dict[str, List[Dict[str, str]]]
    priority_areas: List[str]

class InsightAnalyzer:
    def __init__(self):
        self.activity_categories = {
            "Physical": [
                {"name": "Meditation", "benefit": "Develops mindfulness and reduces stress"},
                {"name": "Yoga", "benefit": "Improves mind-body connection"},
                {"name": "Martial Arts", "benefit": "Builds discipline and body awareness"}
            ],
            "Creative": [
                {"name": "Journaling", "benefit": "Enhances self-reflection and emotional awareness"},
                {"name": "Art Classes", "benefit": "Develops right-brain thinking"},
                {"name": "Music Practice", "benefit": "Improves pattern recognition"}
            ],
            "Social": [
                {"name": "Group Sports", "benefit": "Builds teamwork abilities"},
                {"name": "Public Speaking", "benefit": "Enhances communication skills"},
                {"name": "Volunteer Work", "benefit": "Develops empathy and social connection"}
            ],
            "Professional": [
                {"name": "Leadership Workshops", "benefit": "Builds management skills"},
                {"name": "Technical Training", "benefit": "Enhances expertise"},
                {"name": "Networking Events", "benefit": "Expands professional connections"}
            ]
        }

    def _analyze_personality_traits(self, combined_analysis: CombinedAnalysis) -> List[str]:
        """Generate detailed personality insights"""
        insights = []
        
        # Extract key patterns from natural tendencies
        for tendency in combined_analysis.natural_tendencies:
            if "indicates" in tendency:
                insights.append(f"Core Pattern: {tendency}")
            if "suggests" in tendency:
                insights.append(f"Secondary Pattern: {tendency}")
                
        # Add insights from current state
        for state in combined_analysis.current_state:
            insights.append(f"Current Expression: {state}")
            
        return insights

    def _generate_career_insights(self, combined_analysis: CombinedAnalysis) -> List[str]:
        """Generate career-related insights"""
        career_insights = []
        
        # Basic career direction insights
        career_insights.extend([
            "Your analytical abilities suggest success in strategic roles",
            "Natural leadership potential indicates management opportunities",
            "Consider roles that allow for independent decision-making"
        ])
        
        # Add specific insights based on growth areas
        for area in combined_analysis.growth_areas:
            career_insights.append(f"Develop {area} to enhance career progression")
            
        return career_insights

    def _analyze_relationships(self, combined_analysis: CombinedAnalysis) -> List[str]:
        """Generate relationship insights"""
        relationship_insights = []
        
        # Basic relationship patterns
        relationship_insights.extend([
            "Your communication style is direct and analytical",
            "You value deep, meaningful connections",
            "You may need to balance logic with emotional expression"
        ])
        
        # Add specific insights based on analysis
        for rec in combined_analysis.recommendations:
            if any(word in rec.lower() for word in ["social", "communication", "connect"]):
                relationship_insights.append(f"Growth Opportunity: {rec}")
                
        return relationship_insights

    def _create_development_path(self, combined_analysis: CombinedAnalysis) -> List[str]:
        """Generate development pathway"""
        path = []
        
        # Short-term goals
        path.append("Short-term Focus (1-3 months):")
        for area in combined_analysis.growth_areas[:2]:
            path.append(f"- Work on {area}")
            
        # Medium-term goals
        path.append("\nMedium-term Development (3-6 months):")
        for rec in combined_analysis.recommendations[:2]:
            path.append(f"- {rec}")
            
        # Long-term vision
        path.append("\nLong-term Vision (6-12 months):")
        path.append("- Integrate developed skills into daily life")
        path.append("- Mentor others in your areas of strength")
        
        return path

    def _recommend_activities(self, combined_analysis: CombinedAnalysis) -> Dict[str, List[Dict[str, str]]]:
        """Generate personalized activity recommendations"""
        recommended_activities = {}
        
        # Filter activities based on analysis
        for category, activities in self.activity_categories.items():
            suitable_activities = []
            for activity in activities:
                # Check if activity aligns with growth areas or recommendations
                if any(area.lower() in activity["benefit"].lower() 
                      for area in combined_analysis.growth_areas):
                    suitable_activities.append(activity)
            if suitable_activities:
                recommended_activities[category] = suitable_activities
                
        return recommended_activities

    def analyze(self, combined_analysis: CombinedAnalysis) -> DetailedInsights:
        """Generate comprehensive insights based on combined analysis"""
        
        # Generate all insights
        personality_insights = self._analyze_personality_traits(combined_analysis)
        career_insights = self._generate_career_insights(combined_analysis)
        relationship_insights = self._analyze_relationships(combined_analysis)
        development_path = self._create_development_path(combined_analysis)
        recommended_activities = self._recommend_activities(combined_analysis)
        
        # Determine priority areas based on frequency of mentions
        all_insights = (personality_insights + career_insights + 
                       relationship_insights + combined_analysis.recommendations)
        
        # Simple priority determination
        priority_areas = [
            "Personal Growth",
            "Professional Development",
            "Relationship Building",
            "Skill Enhancement"
        ]
        
        return DetailedInsights(
            personality_insights=personality_insights,
            career_insights=career_insights,
            relationship_insights=relationship_insights,
            development_path=development_path,
            recommended_activities=recommended_activities,
            priority_areas=priority_areas
        )

    def get_test_data(self) -> DetailedInsights:
        """Generate test data for development purposes"""
        from ..processors.combined_analyzer import CombinedAnalyzer
        test_analyzer = CombinedAnalyzer()
        test_combined = test_analyzer.get_test_data()
        return self.analyze(test_combined)

def test_analyzer():
    """Test function to verify basic functionality"""
    analyzer = InsightAnalyzer()
    result = analyzer.get_test_data()
    
    print("\nDetailed Insights Test Results:")
    
    print("\nPersonality Insights:")
    for insight in result.personality_insights:
        print(f"- {insight}")
        
    print("\nCareer Insights:")
    for insight in result.career_insights:
        print(f"- {insight}")
        
    print("\nRelationship Insights:")
    for insight in result.relationship_insights:
        print(f"- {insight}")
        
    print("\nDevelopment Path:")
    for step in result.development_path:
        print(f"- {step}")
        
    print("\nRecommended Activities:")
    for category, activities in result.recommended_activities.items():
        print(f"\n{category}:")
        for activity in activities:
            print(f"- {activity['name']}: {activity['benefit']}")
            
    print("\nPriority Areas:")
    for area in result.priority_areas:
        print(f"- {area}")
    
    return result

if __name__ == "__main__":
    test_analyzer()
