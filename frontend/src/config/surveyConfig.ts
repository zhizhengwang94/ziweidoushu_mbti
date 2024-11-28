import { QuestionType } from './types';

// Types for survey structure
interface Question {
  id: string;
  text: string;
  type: QuestionType;
  category: string;
  description?: string;
  affects: string[];
  weight?: number;
}

interface ActivityQuestion extends Question {
  activityId: string;
  triggerConditions?: {
    frequency?: string;
    completionRate?: number;
    previousResponses?: any;
  };
}

// Core reflection questions that are always present
export const coreQuestions: Question[] = [
  {
    id: 'mental_clarity',
    text: 'Rate your mental clarity and focus today:',
    type: 'scale',
    category: 'mental',
    description: 'Consider your ability to concentrate and think clearly',
    affects: ['mental', 'career'],
    weight: 1.0
  },
  {
    id: 'emotional_balance',
    text: 'How well did you manage your emotions?',
    type: 'scale',
    category: 'emotional',
    description: 'Think about your emotional reactions and stability',
    affects: ['emotional', 'mental'],
    weight: 1.0
  },
  {
    id: 'social_engagement',
    text: 'Rate the quality of your social interactions:',
    type: 'scale',
    category: 'social',
    description: 'Consider both personal and professional relationships',
    affects: ['social', 'emotional'],
    weight: 1.0
  },
  {
    id: 'physical_wellbeing',
    text: 'How would you rate your physical energy and health?',
    type: 'scale',
    category: 'physical',
    description: 'Think about your energy levels and physical comfort',
    affects: ['physical', 'mental'],
    weight: 1.0
  },
  {
    id: 'career_progress',
    text: 'Rate your progress toward career goals:',
    type: 'scale',
    category: 'career',
    description: 'Consider both achievements and learning experiences',
    affects: ['career', 'personal'],
    weight: 1.0
  },
  {
    id: 'personal_growth',
    text: 'How much did you grow personally today?',
    type: 'scale',
    category: 'personal',
    description: 'Think about personal development and self-improvement',
    affects: ['personal', 'mental'],
    weight: 1.0
  }
];

// Structure for activity-specific questions (empty for now but ready to be populated)
export const activityQuestions: ActivityQuestion[] = [
  // Example structure (commented out but shows the format):
  /*
  {
    id: 'meditation_focus',
    text: 'How deep was your meditation focus today?',
    type: 'scale',
    category: 'mental',
    activityId: 'meditation',
    affects: ['mental', 'emotional'],
    weight: 0.5,
    triggerConditions: {
      frequency: 'daily',
      completionRate: 0.8
    }
  }
  */
];

// Scoring configuration
export const scoringConfig = {
  aspects: {
    mental: { baseWeight: 1.0, activityMultiplier: 1.2 },
    emotional: { baseWeight: 1.0, activityMultiplier: 1.2 },
    social: { baseWeight: 1.0, activityMultiplier: 1.2 },
    physical: { baseWeight: 1.0, activityMultiplier: 1.2 },
    career: { baseWeight: 1.0, activityMultiplier: 1.2 },
    personal: { baseWeight: 1.0, activityMultiplier: 1.2 }
  },
  // How much activity-specific questions affect the final score
  activityQuestionWeight: 0.3,
  // Maximum potential bonus from activities
  maxActivityBonus: 50
};

// Helper function to get relevant questions based on selected activities
export const getRelevantQuestions = (selectedActivities: string[]) => {
  const relevantQuestions = [...coreQuestions];
  
  // Filter activity questions based on selected activities
  const relevantActivityQuestions = activityQuestions.filter(
    question => selectedActivities.includes(question.activityId)
  );
  
  return {
    coreQuestions: relevantQuestions,
    activityQuestions: relevantActivityQuestions
  };
};

// Helper function to calculate scores based on responses
export const calculateScores = (
  coreResponses: Record<string, number>,
  activityResponses: Record<string, number>
) => {
  // This is where you'd implement the scoring logic
  // For now, return a basic structure
  const scores: Record<string, any> = {};
  
  Object.keys(scoringConfig.aspects).forEach(aspect => {
    scores[aspect] = {
      base: 0,
      activity: 0,
      total: 0,
      potential: 100
    };
  });
  
  return scores;
};
