import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const LifeInsightsApp = () => {
  const [activeTab, setActiveTab] = useState('profile');
  const [userProfile, setUserProfile] = useState({
    birthDate: '',
    birthTime: '',
    mbtiType: '',
  });
  const [analysisResults, setAnalysisResults] = useState(null);
  const [selectedActivities, setSelectedActivities] = useState([]);
  const [weeklyResponses, setWeeklyResponses] = useState([]);

  // Sample recommendations data
  const recommendedActivities = [
    {
      id: 1,
      category: 'Physical',
      activities: [
        { id: 'p1', name: 'Meditation', reason: 'Helps balance your analytical tendencies with mindfulness' },
        { id: 'p2', name: 'Yoga', reason: 'Develops mind-body connection and reduces stress' },
        { id: 'p3', name: 'Martial Arts', reason: 'Builds discipline and body awareness' }
      ]
    },
    {
      id: 2,
      category: 'Creative',
      activities: [
        { id: 'c1', name: 'Journal Writing', reason: 'Strengthens self-reflection and emotional awareness' },
        { id: 'c2', name: 'Art Classes', reason: 'Develops right-brain thinking and expression' },
        { id: 'c3', name: 'Music Practice', reason: 'Enhances pattern recognition and emotional expression' }
      ]
    },
    {
      id: 3,
      category: 'Social',
      activities: [
        { id: 's1', name: 'Group Sports', reason: 'Builds teamwork and communication skills' },
        { id: 's2', name: 'Public Speaking', reason: 'Develops confidence and leadership' },
        { id: 's3', name: 'Volunteer Work', reason: 'Enhances empathy and social connection' }
      ]
    }
  ];

  // Weekly survey questions
  const weeklyQuestions = [
    "How well did the recommended activities align with your goals this week?",
    "What challenges did you face in following the recommendations?",
    "How has your perspective changed since starting these activities?",
    "Rate your overall progress towards your growth objectives",
    "What additional support would help you succeed?"
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUserProfile(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAnalyze = async () => {
    try {
      const requestData = {
          birth_date: userProfile.birthDate,
          birth_time: userProfile.birthTime,
          mbti_type: userProfile.mbtiType
      };
      console.log('Sending to backend:', requestData);

      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      });

      const data = await response.json();
      console.log('Received from backend:', data);

      if (response.ok) {  // Changed this condition
        setAnalysisResults({
          naturalTendencies: data.data.natural_tendencies,
          currentState: data.data.current_state,
          growthAreas: data.data.growth_areas
        });
        setActiveTab('insights');
      } else {
        alert('Analysis failed: ' + JSON.stringify(data.detail));
      }
    } catch (error) {
      console.error('Error details:', error);
      alert('Error connecting to server: ' + error.toString());
    }
  };

  const handleActivitySelect = (activityId) => {
    setSelectedActivities(prev => {
      if (prev.includes(activityId)) {
        return prev.filter(id => id !== activityId);
      }
      return [...prev, activityId];
    });
  };

  const handleFinishSelection = () => {
    console.log('Selected activities:', selectedActivities);
    setActiveTab('tracking');
  };

  const mockProgressData = [
    { week: 1, score: 75 },
    { week: 2, score: 78 },
    { week: 3, score: 82 },
  ];

  return (
    <div className="max-w-4xl mx-auto p-4">
      {/* Navigation Tabs */}
      <div className="flex mb-4 border-b">
        {['profile', 'insights', 'recommendations', 'tracking', 'progress'].map((tab) => (
          <button
            key={tab}
            className={`px-4 py-2 ${activeTab === tab ? 'border-b-2 border-blue-500' : ''}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* Profile Tab */}
      {activeTab === 'profile' && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Personal Profile</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Birth Date</label>
              <input
                type="date"
                name="birthDate"
                className="w-full p-2 border rounded"
                value={userProfile.birthDate}
                onChange={handleInputChange}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Birth Time</label>
              <input
                type="time"
                name="birthTime"
                className="w-full p-2 border rounded"
                value={userProfile.birthTime}
                onChange={handleInputChange}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">MBTI Type</label>
              <select
                name="mbtiType"
                className="w-full p-2 border rounded"
                value={userProfile.mbtiType}
                onChange={handleInputChange}
              >
                <option value="">Select MBTI Type</option>
                {["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
                  "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"].map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>
            <button
              className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              onClick={handleAnalyze}
            >
              Generate Insights
            </button>
          </div>
        </div>
      )}

      {/* Insights Tab */}
      {activeTab === 'insights' && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Personal Insights</h2>
          {analysisResults ? (
            <div className="space-y-4">
              <div className="p-4 bg-blue-50 rounded">
                <h3 className="font-medium mb-2">Natural Tendencies (ZiWeiDouShu)</h3>
                {analysisResults.naturalTendencies.map((tendency, index) => (
                  <p key={index} className="text-gray-600">{tendency}</p>
                ))}
              </div>
              <div className="p-4 bg-purple-50 rounded">
                <h3 className="font-medium mb-2">Current State (MBTI)</h3>
                {analysisResults.currentState.map((state, index) => (
                  <p key={index} className="text-gray-600">{state}</p>
                ))}
              </div>
              <div className="p-4 bg-green-50 rounded">
                <h3 className="font-medium mb-2">Growth Areas</h3>
                {analysisResults.growthAreas.map((area, index) => (
                  <p key={index} className="text-gray-600">{area}</p>
                ))}
              </div>
              <button
                className="w-full p-2 bg-green-500 text-white rounded hover:bg-green-600"
                onClick={() => setActiveTab('recommendations')}
              >
                View Recommended Activities
              </button>
            </div>
          ) : (
            <p>Complete your profile to see insights</p>
          )}
        </div>
      )}

      {/* Recommendations Tab */}
      {activeTab === 'recommendations' && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Recommended Activities</h2>
          <div className="space-y-6">
            {recommendedActivities.map(category => (
              <div key={category.id} className="space-y-3">
                <h3 className="text-lg font-semibold">{category.category} Activities</h3>
                {category.activities.map(activity => (
                  <div key={activity.id} className="flex items-start space-x-3 p-3 border rounded">
                    <input
                      type="checkbox"
                      checked={selectedActivities.includes(activity.id)}
                      onChange={() => handleActivitySelect(activity.id)}
                      className="mt-1"
                    />
                    <div>
                      <p className="font-medium">{activity.name}</p>
                      <p className="text-sm text-gray-600">{activity.reason}</p>
                    </div>
                  </div>
                ))}
              </div>
            ))}
            <button
              className="w-full p-2 bg-green-500 text-white rounded hover:bg-green-600 mt-4"
              onClick={handleFinishSelection}
              disabled={selectedActivities.length === 0}
            >
              Start Your Growth Journey
            </button>
          </div>
        </div>
      )}

      {/* Tracking Tab */}
      {activeTab === 'tracking' && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Weekly Progress Check</h2>
          <div className="space-y-6">
            {weeklyQuestions.map((question, index) => (
              <div key={index} className="space-y-2">
                <p className="font-medium">{question}</p>
                <textarea
                  className="w-full p-2 border rounded h-24"
                  placeholder="Your response..."
                />
              </div>
            ))}
            <button
              className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              onClick={() => setActiveTab('progress')}
            >
              Submit Weekly Review
            </button>
          </div>
        </div>
      )}

      {/* Progress Tab */}
      {activeTab === 'progress' && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Growth Journey</h2>
          <div className="h-64">
            <LineChart width={600} height={200} data={mockProgressData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="week" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="score" stroke="#8884d8" />
            </LineChart>
          </div>
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-3">Your Selected Activities</h3>
            <div className="space-y-2">
              {selectedActivities.map(activityId => {
                const activity = recommendedActivities
                  .flatMap(cat => cat.activities)
                  .find(act => act.id === activityId);
                return (
                  <div key={activityId} className="p-2 bg-gray-50 rounded">
                    {activity?.name}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LifeInsightsApp;