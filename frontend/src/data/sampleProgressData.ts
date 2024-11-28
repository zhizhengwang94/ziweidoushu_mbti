// In a new file src/data/sampleProgressData.ts

export interface WeeklyScore {
  base: number;
  activity: number;
  total: number;
  potential: number;
}

export interface WeeklyProgress {
  weekNumber: number;
  timestamp: string;
  scores: {
    mental: WeeklyScore;
    emotional: WeeklyScore;
    social: WeeklyScore;
    physical: WeeklyScore;
    career: WeeklyScore;
    personal: WeeklyScore;
  };
  activities: {
    id: string;
    name: string;
    completed: boolean;
    impact: number;
  }[];
}

// Sample data for 5 weeks
export const sampleProgressData: WeeklyProgress[] = [
  {
    weekNumber: 1,
    timestamp: '2024-10-01',
    scores: {
      mental: { base: 45, activity: 0, total: 45, potential: 75 },
      emotional: { base: 55, activity: 0, total: 55, potential: 80 },
      social: { base: 40, activity: 0, total: 40, potential: 70 },
      physical: { base: 50, activity: 0, total: 50, potential: 85 },
      career: { base: 60, activity: 0, total: 60, potential: 90 },
      personal: { base: 48, activity: 0, total: 48, potential: 82 }
    },
    activities: []
  },
  {
    weekNumber: 2,
    timestamp: '2024-10-08',
    scores: {
      mental: { base: 47, activity: 5, total: 52, potential: 75 },
      emotional: { base: 53, activity: 8, total: 61, potential: 80 },
      social: { base: 42, activity: 3, total: 45, potential: 70 },
      physical: { base: 52, activity: 10, total: 62, potential: 85 },
      career: { base: 58, activity: 7, total: 65, potential: 90 },
      personal: { base: 50, activity: 5, total: 55, potential: 82 }
    },
    activities: [
      { id: 'meditation', name: 'Meditation', completed: true, impact: 5 },
      { id: 'exercise', name: 'Exercise', completed: true, impact: 10 }
    ]
  },
  {
    weekNumber: 3,
    timestamp: '2024-10-15',
    scores: {
      mental: { base: 49, activity: 12, total: 61, potential: 75 },
      emotional: { base: 54, activity: 15, total: 69, potential: 80 },
      social: { base: 45, activity: 8, total: 53, potential: 70 },
      physical: { base: 53, activity: 18, total: 71, potential: 85 },
      career: { base: 57, activity: 12, total: 69, potential: 90 },
      personal: { base: 51, activity: 10, total: 61, potential: 82 }
    },
    activities: [
      { id: 'meditation', name: 'Meditation', completed: true, impact: 8 },
      { id: 'exercise', name: 'Exercise', completed: true, impact: 12 },
      { id: 'journaling', name: 'Journaling', completed: true, impact: 7 }
    ]
  },
  {
    weekNumber: 4,
    timestamp: '2024-10-22',
    scores: {
      mental: { base: 51, activity: 15, total: 66, potential: 75 },
      emotional: { base: 56, activity: 18, total: 74, potential: 80 },
      social: { base: 47, activity: 12, total: 59, potential: 70 },
      physical: { base: 54, activity: 20, total: 74, potential: 85 },
      career: { base: 59, activity: 15, total: 74, potential: 90 },
      personal: { base: 53, activity: 14, total: 67, potential: 82 }
    },
    activities: [
      { id: 'meditation', name: 'Meditation', completed: true, impact: 10 },
      { id: 'exercise', name: 'Exercise', completed: true, impact: 15 },
      { id: 'journaling', name: 'Journaling', completed: true, impact: 8 },
      { id: 'networking', name: 'Networking', completed: true, impact: 6 }
    ]
  },
  {
    weekNumber: 5,
    timestamp: '2024-10-29',
    scores: {
      mental: { base: 50, activity: 13, total: 63, potential: 75 },
      emotional: { base: 57, activity: 16, total: 73, potential: 80 },
      social: { base: 46, activity: 15, total: 61, potential: 70 },
      physical: { base: 55, activity: 22, total: 77, potential: 85 },
      career: { base: 58, activity: 18, total: 76, potential: 90 },
      personal: { base: 52, activity: 16, total: 68, potential: 82 }
    },
    activities: [
      { id: 'meditation', name: 'Meditation', completed: true, impact: 9 },
      { id: 'exercise', name: 'Exercise', completed: true, impact: 14 },
      { id: 'journaling', name: 'Journaling', completed: false, impact: 0 },
      { id: 'networking', name: 'Networking', completed: true, impact: 8 }
    ]
  }
];
