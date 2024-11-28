import React, { useState } from 'react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
} from 'recharts';
import { WeeklyProgress } from '../data/sampleProgressData';

interface ProgressViewProps {
  progressData: WeeklyProgress[];
}

const ProgressView: React.FC<ProgressViewProps> = ({ progressData }) => {
  const [selectedAspect, setSelectedAspect] = useState<string>('mental');

  // Colors for different aspects
  const aspectColors = {
    mental: '#8884d8',
    emotional: '#82ca9d',
    social: '#ffc658',
    physical: '#ff7300',
    career: '#0088fe',
    personal: '#00C49F'
  };

  // Transform data for the radar chart (latest week)
  const latestWeek = progressData[progressData.length - 1];
  const radarData = Object.entries(latestWeek.scores).map(([aspect, scores]) => ({
    aspect,
    base: scores.base,
    total: scores.total,
    potential: scores.potential
  }));

  // Transform data for detailed aspect view
  const getAspectData = (aspect: string) => {
    return progressData.map(week => ({
      week: week.weekNumber,
      base: week.scores[aspect as keyof typeof week.scores].base,
      activity: week.scores[aspect as keyof typeof week.scores].activity,
      total: week.scores[aspect as keyof typeof week.scores].total,
      potential: week.scores[aspect as keyof typeof week.scores].potential
    }));
  };

  return (
    <div className="space-y-8 p-6">
      {/* Overview Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {Object.entries(latestWeek.scores).map(([aspect, scores]) => (
          <div 
            key={aspect} 
            className={`p-4 bg-white rounded-lg shadow cursor-pointer ${
              selectedAspect === aspect ? 'ring-2 ring-blue-500' : ''
            }`}
            onClick={() => setSelectedAspect(aspect)}
          >
            <h3 className="text-lg font-semibold capitalize">{aspect}</h3>
            <div className="mt-2">
              <div className="flex justify-between text-sm">
                <span>Base Score:</span>
                <span>{scores.base}</span>
              </div>
              <div className="flex justify-between text-sm text-green-600">
                <span>Activity Bonus:</span>
                <span>+{scores.activity}</span>
              </div>
              <div className="flex justify-between font-semibold mt-1">
                <span>Total:</span>
                <span>{scores.total}/{scores.potential}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Detailed Aspect View */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4 capitalize">{selectedAspect} Progress</h3>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={getAspectData(selectedAspect)}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="week" label={{ value: 'Week', position: 'bottom' }} />
              <YAxis domain={[0, 100]} label={{ value: 'Score', angle: -90, position: 'left' }} />
              <Tooltip />
              <Legend />
              <Area
                type="monotone"
                dataKey="potential"
                stroke="#8884d8"
                fill="#8884d8"
                fillOpacity={0.1}
                name="Potential"
              />
              <Area
                type="monotone"
                dataKey="base"
                stroke="#82ca9d"
                fill="#82ca9d"
                fillOpacity={0.3}
                name="Base Score"
              />
              <Area
                type="monotone"
                dataKey="total"
                stroke="#ffc658"
                fill="#ffc658"
                fillOpacity={0.3}
                name="Total Score"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Radar Chart for Balance */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Overall Balance</h3>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={radarData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="aspect" />
              <PolarRadiusAxis domain={[0, 100]} />
              <Radar
                name="Potential"
                dataKey="potential"
                stroke="#8884d8"
                fill="#8884d8"
                fillOpacity={0.1}
              />
              <Radar
                name="Base Score"
                dataKey="base"
                stroke="#82ca9d"
                fill="#82ca9d"
                fillOpacity={0.3}
              />
              <Radar
                name="Total Score"
                dataKey="total"
                stroke="#ffc658"
                fill="#ffc658"
                fillOpacity={0.5}
              />
              <Legend />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Activity Impact */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Activity Impact</h3>
        <div className="space-y-4">
          {latestWeek.activities.map(activity => (
            <div key={activity.id} className="border p-4 rounded">
              <div className="flex justify-between items-center">
                <div>
                  <h4 className="font-medium">{activity.name}</h4>
                  <p className="text-sm text-gray-500">
                    Impact: +{activity.impact} points
                  </p>
                </div>
                <div className={`px-3 py-1 rounded ${
                  activity.completed ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  {activity.completed ? 'Completed' : 'Missed'}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProgressView;