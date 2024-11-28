import React, { useState } from 'react';
import { getRelevantQuestions, calculateScores } from '../config/surveyConfig.ts';
import type { SurveyResponse, AspectScore } from '../types/survey.ts';

interface TrackingViewProps {
  selectedActivities: string[];
  onComplete: (data: {
    scores: Record<string, AspectScore>;
    responses: Record<string, SurveyResponse>;
    notes: string;
    timestamp: string;
  }) => void;
}

const TrackingView: React.FC<TrackingViewProps> = ({ selectedActivities, onComplete }) => {
  const [coreResponses, setCoreResponses] = useState<Record<string, number>>({});
  const [activityResponses, setActivityResponses] = useState<Record<string, number>>({});
  const [notes, setNotes] = useState('');

  const { coreQuestions, activityQuestions } = getRelevantQuestions(selectedActivities);

  const handleRatingChange = (questionId: string, value: number, isActivityQuestion: boolean = false) => {
    if (isActivityQuestion) {
      setActivityResponses(prev => ({
        ...prev,
        [questionId]: value
      }));
    } else {
      setCoreResponses(prev => ({
        ...prev,
        [questionId]: value
      }));
    }
  };

  const handleSubmit = () => {
    const scores = calculateScores(coreResponses, activityResponses);
    
    const allResponses: Record<string, SurveyResponse> = {};
    
    // Format core responses
    Object.entries(coreResponses).forEach(([id, value]) => {
      allResponses[id] = {
        questionId: id,
        value,
        timestamp: new Date().toISOString()
      };
    });
    
    // Format activity responses
    Object.entries(activityResponses).forEach(([id, value]) => {
      allResponses[id] = {
        questionId: id,
        value,
        timestamp: new Date().toISOString()
      };
    });

    onComplete({
      scores,
      responses: allResponses,
      notes,
      timestamp: new Date().toISOString()
    });
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-bold mb-4">Daily Progress Check</h2>
      
      {/* Core Questions Section */}
      <div className="space-y-6 mb-6">
        <h3 className="font-medium">Core Reflection Questions</h3>
        {coreQuestions.map(question => (
          <div key={question.id} className="border p-4 rounded">
            <label className="block mb-2 font-medium">
              {question.text}
            </label>
            {question.description && (
              <p className="text-sm text-gray-500 mb-2">{question.description}</p>
            )}
            <div className="flex items-center gap-4">
              <input
                type="range"
                min="1"
                max="10"
                value={coreResponses[question.id] || 5}
                onChange={(e) => handleRatingChange(question.id, parseInt(e.target.value))}
                className="w-full"
              />
              <span className="text-sm w-8">{coreResponses[question.id] || 5}</span>
            </div>
            <div className="text-xs text-gray-500 mt-1">
              Affects: {question.affects.join(', ')}
            </div>
          </div>
        ))}
      </div>

      {/* Activity Questions Section */}
      {activityQuestions.length > 0 && (
        <div className="space-y-6 mb-6">
          <h3 className="font-medium">Activity-Specific Questions</h3>
          {activityQuestions.map(question => (
            <div key={question.id} className="border p-4 rounded">
              <label className="block mb-2 font-medium">
                {question.text}
              </label>
              {question.description && (
                <p className="text-sm text-gray-500 mb-2">{question.description}</p>
              )}
              <div className="flex items-center gap-4">
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={activityResponses[question.id] || 5}
                  onChange={(e) => handleRatingChange(question.id, parseInt(e.target.value), true)}
                  className="w-full"
                />
                <span className="text-sm w-8">{activityResponses[question.id] || 5}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Activities Section */}
      <div className="mb-6">
        <h3 className="font-medium mb-2">Selected Activities:</h3>
        <div className="grid grid-cols-2 gap-2">
          {selectedActivities.map(activity => (
            <div key={activity} className="p-2 bg-gray-50 rounded">
              {activity}
            </div>
          ))}
        </div>
      </div>

      {/* Notes Section */}
      <div className="mb-6">
        <label className="block mb-2 font-medium">
          Additional Notes or Insights:
        </label>
        <textarea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          className="w-full h-32 p-2 border rounded"
          placeholder="Share any thoughts, challenges, or insights from today..."
        />
      </div>

      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Complete Daily Check-in
      </button>
    </div>
  );
};

export default TrackingView;