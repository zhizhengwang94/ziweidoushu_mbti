from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum

@dataclass
class MBTIResult:
    type_code: str
    cognitive_functions: List[str]
    strengths: List[str]
    growth_areas: List[str]
    detailed_traits: Dict[str, List[str]]

class MBTIProcessor:
    def __init__(self):
        self.cognitive_functions = {
            "INTJ": ["Ni", "Te", "Fi", "Se"],
            "INTP": ["Ti", "Ne", "Si", "Fe"],
            "ENTJ": ["Te", "Ni", "Se", "Fi"],
            "ENTP": ["Ne", "Ti", "Fe", "Si"],
            "INFJ": ["Ni", "Fe", "Ti", "Se"],
            "INFP": ["Fi", "Ne", "Si", "Te"],
            "ENFJ": ["Fe", "Ni", "Se", "Ti"],
            "ENFP": ["Ne", "Fi", "Te", "Si"],
            "ISTJ": ["Si", "Te", "Fi", "Ne"],
            "ISFJ": ["Si", "Fe", "Ti", "Ne"],
            "ESTJ": ["Te", "Si", "Ne", "Fi"],
            "ESFJ": ["Fe", "Si", "Ne", "Ti"],
            "ISTP": ["Ti", "Se", "Ni", "Fe"],
            "ISFP": ["Fi", "Se", "Ni", "Te"],
            "ESTP": ["Se", "Ti", "Fe", "Ni"],
            "ESFP": ["Se", "Fi", "Te", "Ni"]
        }
        
        # Dictionary explaining cognitive functions
        self.function_descriptions = {
            "Ni": "Introverted Intuition - Pattern recognition and future planning",
            "Ne": "Extroverted Intuition - Exploring possibilities and connections",
            "Ti": "Introverted Thinking - Logical analysis and frameworks",
            "Te": "Extroverted Thinking - Organizing and efficiency",
            "Fi": "Introverted Feeling - Personal values and authenticity",
            "Fe": "Extroverted Feeling - Social harmony and empathy",
            "Si": "Introverted Sensing - Past experiences and details",
            "Se": "Extroverted Sensing - Present awareness and adaptability"
        }

        # Common traits for each type
        self.type_traits = {
            "INTJ": {
                "strengths": [
                    "Strategic thinking",
                    "Long-term planning",
                    "Complex problem solving",
                    "Independent thinking"
                ],
                "growth_areas": [
                    "Emotional expression",
                    "Social interaction",
                    "Handling uncertainty",
                    "Accepting others' viewpoints"
                ]
            },
            # Add other types similarly...
        }

    def get_type_traits(self, mbti_type: str) -> Tuple[List[str], List[str]]:
        """Get strengths and growth areas for a given MBTI type"""
        default_traits = {
            "strengths": ["Analytical thinking", "Problem solving"],
            "growth_areas": ["Personal development", "Balance"]
        }
        type_info = self.type_traits.get(mbti_type, default_traits)
        return type_info["strengths"], type_info["growth_areas"]

    def get_function_details(self, functions: List[str]) -> Dict[str, str]:
        """Get detailed descriptions of cognitive functions"""
        return {func: self.function_descriptions.get(func, "Description not available") 
                for func in functions}

    def process(self, mbti_type: str) -> MBTIResult:
        # Get cognitive functions for the type
        functions = self.cognitive_functions.get(mbti_type, [])
        
        # Get type-specific traits
        strengths, growth_areas = self.get_type_traits(mbti_type)
        
        # Create detailed traits dictionary
        detailed_traits = {
            "cognitive_stack": [f"{func}: {self.function_descriptions.get(func)}" 
                              for func in functions],
            "communication_style": [
                "Direct and logical" if 'Te' in functions else "Diplomatic and harmonious",
                "Abstract and theoretical" if 'N' in mbti_type else "Concrete and practical"
            ],
            "learning_style": [
                "Conceptual learning" if 'N' in mbti_type else "Hands-on learning",
                "Independent study" if 'I' in mbti_type else "Group learning"
            ]
        }

        return MBTIResult(
            type_code=mbti_type,
            cognitive_functions=functions,
            strengths=strengths,
            growth_areas=growth_areas,
            detailed_traits=detailed_traits
        )

    def get_test_data(self) -> MBTIResult:
        """Generate test data for development purposes"""
        return self.process("INTJ")

def test_processor():
    """Test function to verify basic functionality"""
    processor = MBTIProcessor()
    
    # Test with specific type
    result = processor.process("INTJ")
    
    print("\nMBTI Processor Test Results:")
    print(f"Type: {result.type_code}")
    print(f"Cognitive Functions: {', '.join(result.cognitive_functions)}")
    print("\nStrengths:")
    for strength in result.strengths:
        print(f"- {strength}")
    print("\nGrowth Areas:")
    for area in result.growth_areas:
        print(f"- {area}")
    print("\nDetailed Traits:")
    for category, traits in result.detailed_traits.items():
        print(f"\n{category}:")
        if isinstance(traits, list):
            for trait in traits:
                print(f"- {trait}")
        else:
            print(f"- {traits}")
    
    return result

if __name__ == "__main__":
    test_processor()
