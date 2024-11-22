from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime
from .ziwei_processor import ZiWeiProcessor, ZiWeiResult
from .mbti_processor import MBTIProcessor, MBTIResult

@dataclass
class CombinedAnalysis:
    natural_tendencies: List[str]
    current_state: List[str]
    growth_areas: List[str]
    recommendations: List[str]
    detailed_analysis: Dict[str, List[str]]

class CombinedAnalyzer:
    def __init__(self):
        self.ziwei_processor = ZiWeiProcessor()
        self.mbti_processor = MBTIProcessor()
        
        # Mapping of ZiWei palaces to personality traits
        self.palace_traits = {
            "命宮": ["core personality", "self-expression"],
            "兄弟": ["peer relationships", "communication style"],
            "夫妻": ["partnerships", "relationship approach"],
            "子女": ["creativity", "self-development"],
            "財帛": ["resources", "value system"],
            "疾厄": ["challenges", "stress management"],
            "遷移": ["adaptability", "life changes"],
            "交友": ["social connections", "networking"],
            "官祿": ["career", "achievements"],
            "田宅": ["stability", "foundation"],
            "福德": ["inner happiness", "spiritual growth"],
            "父母": ["authority", "leadership"]
        }

    def _analyze_compatibility(self, ziwei_result: ZiWeiResult, mbti_result: MBTIResult) -> List[str]:
        """Analyze compatibility between ZiWei and MBTI traits"""
        compatibility_insights = []
        
        # Example compatibility analysis
        if "紫微" in ziwei_result.key_stars and "Ni" in mbti_result.cognitive_functions:
            compatibility_insights.append(
                "Your natural intuitive abilities are strengthened by both your ZiWei star placement and MBTI preferences"
            )
        
        if ziwei_result.elements.get("day_element") == "木" and "Te" in mbti_result.cognitive_functions:
            compatibility_insights.append(
                "Your wood element harmonizes with your logical thinking style"
            )
            
        return compatibility_insights

    def _generate_recommendations(self, 
                                ziwei_result: ZiWeiResult, 
                                mbti_result: MBTIResult, 
                                compatibility: List[str]) -> List[str]:
        """Generate personalized recommendations based on both analyses"""
        recommendations = []
        
        # Base recommendations on MBTI cognitive functions
        dominant_function = mbti_result.cognitive_functions[0]
        if dominant_function == "Ni":
            recommendations.extend([
                "Practice strategic planning exercises",
                "Engage in long-term visioning activities"
            ])
        elif dominant_function == "Ti":
            recommendations.extend([
                "Study complex systems and frameworks",
                "Engage in logical problem-solving activities"
            ])
            
        # Add recommendations based on ZiWei placements
        main_palace_traits = self.palace_traits.get(ziwei_result.main_star, [])
        for trait in main_palace_traits:
            recommendations.append(f"Focus on developing your {trait}")
            
        return recommendations

    def analyze(self, birth_datetime: datetime, mbti_type: str) -> CombinedAnalysis:
        # Get individual analyses
        ziwei_result = self.ziwei_processor.process(birth_datetime)
        mbti_result = self.mbti_processor.process(mbti_type)
        
        # Analyze compatibility
        compatibility_insights = self._analyze_compatibility(ziwei_result, mbti_result)
        
        # Generate natural tendencies from ZiWei analysis
        natural_tendencies = [
            f"Your main star ({ziwei_result.main_star}) indicates {', '.join(self.palace_traits.get(ziwei_result.main_star, ['undefined traits']))}",
            f"Your life palace placement suggests {', '.join(self.palace_traits.get(ziwei_result.life_palace, ['undefined traits']))}"
        ]
        
        # Add element-based insights
        for element_type, element in ziwei_result.elements.items():
            natural_tendencies.append(f"Your {element_type} ({element}) influences your natural approach")
            
        # Current state from MBTI analysis
        current_state = [
            f"Your dominant function ({mbti_result.cognitive_functions[0]}) shapes your current approach",
            f"You show natural strengths in: {', '.join(mbti_result.strengths[:2])}"
        ]
        
        # Generate recommendations
        recommendations = self._generate_recommendations(ziwei_result, mbti_result, compatibility_insights)
        
        # Create detailed analysis dictionary
        detailed_analysis = {
            "compatibility_insights": compatibility_insights,
            "ziwei_details": [
                f"Main Star: {ziwei_result.main_star}",
                f"Life Palace: {ziwei_result.life_palace}",
                f"Key Stars: {', '.join(ziwei_result.key_stars)}"
            ],
            "mbti_details": [
                f"Type: {mbti_type}",
                f"Cognitive Stack: {', '.join(mbti_result.cognitive_functions)}",
                f"Key Strengths: {', '.join(mbti_result.strengths)}"
            ]
        }
        
        return CombinedAnalysis(
            natural_tendencies=natural_tendencies,
            current_state=current_state,
            growth_areas=mbti_result.growth_areas,
            recommendations=recommendations,
            detailed_analysis=detailed_analysis
        )

    def get_test_data(self) -> CombinedAnalysis:
        """Generate test data for development purposes"""
        test_date = datetime(1990, 1, 1, 12, 0)
        return self.analyze(test_date, "INTJ")

def test_analyzer():
    """Test function to verify basic functionality"""
    analyzer = CombinedAnalyzer()
    
    # Test with specific data
    result = analyzer.get_test_data()
    
    print("\nCombined Analysis Test Results:")
    print("\nNatural Tendencies:")
    for tendency in result.natural_tendencies:
        print(f"- {tendency}")
        
    print("\nCurrent State:")
    for state in result.current_state:
        print(f"- {state}")
        
    print("\nGrowth Areas:")
    for area in result.growth_areas:
        print(f"- {area}")
        
    print("\nRecommendations:")
    for rec in result.recommendations:
        print(f"- {rec}")
        
    print("\nDetailed Analysis:")
    for category, details in result.detailed_analysis.items():
        print(f"\n{category}:")
        for detail in details:
            print(f"- {detail}")
    
    return result

if __name__ == "__main__":
    test_analyzer()
