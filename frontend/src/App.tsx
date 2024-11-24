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
  const [aspectScores, setAspectScores] = useState({
    mental: { base: 0, activity: 0, total: 0, potential: 0 },
    emotional: { base: 0, activity: 0, total: 0, potential: 0 },
    social: { base: 0, activity: 0, total: 0, potential: 0 },
    physical: { base: 0, activity: 0, total: 0, potential: 0 },
    career: { base: 0, activity: 0, total: 0, potential: 0 },
    personal: { base: 0, activity: 0, total: 0, potential: 0 }
  });

  // Sample recommendations data
// Update recommendedActivities near the top of your file
  const recommendedActivities = [
    {
      id: 1,
      category: 'Physical',
      activities: [
        { 
          id: 'p1', 
          name: 'Meditation', 
          reason: 'Helps balance your analytical tendencies with mindfulness',
          impacts: {
            mental: 10,
            emotional: 15,
            physical: 8,
            personal: 12
          }
        },
        { 
          id: 'p2', 
          name: 'Yoga', 
          reason: 'Develops mind-body connection and reduces stress',
          impacts: {
            physical: 15,
            emotional: 10,
            mental: 8,
            personal: 10
          }
        },
        { 
          id: 'p3', 
          name: 'Martial Arts', 
          reason: 'Builds discipline and body awareness',
          impacts: {
            physical: 20,
            mental: 12,
            social: 8,
            personal: 15
          }
        }
      ]
    },
    {
      id: 2,
      category: 'Creative',
      activities: [
        { 
          id: 'c1', 
          name: 'Journal Writing', 
          reason: 'Strengthens self-reflection and emotional awareness',
          impacts: {
            emotional: 15,
            mental: 12,
            personal: 10
          }
        },
        { 
          id: 'c2', 
          name: 'Art Classes', 
          reason: 'Develops right-brain thinking and expression',
          impacts: {
            emotional: 12,
            mental: 10,
            social: 8,
            personal: 10
          }
        },
        { 
          id: 'c3', 
          name: 'Music Practice', 
          reason: 'Enhances pattern recognition and emotional expression',
          impacts: {
            mental: 15,
            emotional: 12,
            personal: 10
          }
        }
      ]
    },
    {
      id: 3,
      category: 'Social',
      activities: [
        { 
          id: 's1', 
          name: 'Group Sports', 
          reason: 'Builds teamwork and communication skills',
          impacts: {
            social: 20,
            physical: 15,
            emotional: 10
          }
        },
        { 
          id: 's2', 
          name: 'Public Speaking', 
          reason: 'Develops confidence and leadership',
          impacts: {
            social: 18,
            career: 15,
            personal: 12
          }
        },
        { 
          id: 's3', 
          name: 'Volunteer Work', 
          reason: 'Enhances empathy and social connection',
          impacts: {
            social: 15,
            emotional: 12,
            personal: 10,
            career: 8
          }
        }
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

      if (response.ok) {  
        setAnalysisResults({
          naturalTendencies: data.data.natural_tendencies,
          currentState: data.data.current_state,
          growthAreas: data.data.growth_areas,
          aspectScores: data.data.scores  // Add this line
        });
        setAspectScores(data.data.scores); // Add this line
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
          {aspectScores && (
            <div className="grid grid-cols-2 gap-4 mb-4">
              {Object.entries(aspectScores).map(([aspect, score]) => (
                <div key={aspect} className="p-4 bg-gray-50 rounded">
                  <h4 className="font-semibold capitalize">{aspect}</h4>
                  <div className="text-sm">
                    <p>Base Score: {score.base}</p>
                    <p>Activity Bonus: {score.activity}</p>
                    <p className="font-bold">Total: {score.total}/100</p>
                    <p className="text-gray-500">Potential: {score.potential}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
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
                  <div key={activity.id} className="space-y-3 p-3 border rounded">
                    <div className="flex items-start space-x-3">
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
                    <div className="pl-8">
                      <p className="text-sm font-medium mb-2">Impact on Aspects:</p>
                      <div className="grid grid-cols-2 gap-2">
                        {Object.entries(activity.impacts).map(([aspect, impact]) => (
                          <div key={aspect} className="flex items-center space-x-2">
                            <span className="text-sm capitalize">{aspect}:</span>
                            <div className="flex-1 h-2 bg-gray-200 rounded">
                              <div 
                                className="h-full bg-blue-500 rounded" 
                                style={{ width: `${impact}%` }}
                              />
                            </div>
                            <span className="text-sm">+{impact}</span>
                          </div>
                        ))}
                      </div>
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
          <div className="space-y-8">
            {Object.entries(aspectScores || {}).map(([aspect, _]) => {
              const aspectData = [
                { week: 1, score: mockProgressData[0].score },
                { week: 2, score: mockProgressData[1].score },
                { week: 3, score: mockProgressData[2].score },
              ];
              return (
                <div key={aspect} className="border-b pb-6">
                  <h3 className="text-lg font-semibold capitalize mb-2">{aspect}</h3>
                  <div className="h-64">
                    <LineChart width={600} height={200} data={aspectData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="week" />
                      <YAxis domain={[0, 100]} />
                      <Tooltip />
                      <Line 
                        type="monotone" 
                        dataKey="score" 
                        stroke="#8884d8" 
                        name={`${aspect} Score`}
                      />
                    </LineChart>
                  </div>
                </div>
              );
            })}
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
        </div>
      )}
    </div>
  );
};

export default LifeInsightsApp;