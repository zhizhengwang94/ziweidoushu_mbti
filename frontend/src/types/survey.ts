export type QuestionType = 'scale' | 'text' | 'multipleChoice' | 'checkbox';

export interface SurveyResponse {
  questionId: string;
  value: number | string | string[];
  timestamp: string;
}

export interface AspectScore {
  base: number;
  activity: number;
  total: number;
  potential: number;
}

export interface ActivityProgress {
  completionRate: number;
  consistency: number;
  impact: number;
}

export interface SurveyResult {
  scores: Record<string, AspectScore>;
  responses: Record<string, SurveyResponse>;
  activityProgress: Record<string, ActivityProgress>;
  timestamp: string;
}
