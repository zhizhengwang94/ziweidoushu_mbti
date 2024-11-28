import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  RadarLine,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';

interface ProgressViewProps {
  weeklyResponses: WeeklyResponse[];
  aspectScores: Record<string, AspectScore>;
  selectedActivities: string[];
}

const ProgressView: React.FC<ProgressViewProps> = ({
  weeklyResponses,
  aspectScores,
  selectedActivities
}) => {
  // Transform data for time series chart
  const timeSeriesData = weeklyResponses.map((response, index) => ({
    week: index + 1,
    ...Object.entries(response.scores).reduce((acc, [aspect, score]) => ({
      ...acc,
      [aspect]: score.total
    }), {})
  }));

  // Current scores for radar chart
  const radarData = [
    Object.entries(aspectScores).reduce((acc, [aspect, score]) => ({
      ...acc,
      aspect,
      value: score.total
    }), { aspect: '', value: 0 })
  ];

  // Colors for different aspects
  const aspectColors = {
    mental: '#8884d8',
    emotional: '#82ca9d',
    social: '#ffc658',
    physical: '#ff7300',
    career: '#0088fe',
    personal: '#00C49F'
  };

  return (
    <div className="space-y-8">
      {/* Overview Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {Object.entries(aspectScores).map(([aspect, scores]) => (
          <div key={aspect} className="p-4 bg-white rounded-lg shadow">
            <h3 className="text-lg font-semibold capitalize">{aspect}</h3>
            <div className="mt-2">
              <div className="flex justify-between text-sm">
                <span>Base Score:</span>
                <span>{scores.base}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Activity Bonus:</span>
                <span>+{scores.activity}</span>
              </div>
              <div className="flex justify-between font-semibold mt-1">
                <span>Total:</span>
                <span>{scores.total}/100</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Time Series Chart */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Progress Over Time</h3>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={timeSeriesData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="week" label={{ value: 'Week', position: 'bottom' }} />
              <YAxis domain={[0, 100]} label={{ value: 'Score', angle: -90, position: 'left' }} />
              <Tooltip />
              <Legend />
              {Object.keys(aspectScores).map(aspect => (
                <Line
                  key={aspect}
                  type="monotone"
                  dataKey={aspect}
                  stroke={aspectColors[aspect as keyof typeof aspectColors]}
                  name={aspect.charAt(0).toUpperCase() + aspect.slice(1)}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Radar Chart */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Current Balance</h3>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={radarData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="aspect" />
              <PolarRadiusAxis domain={[0, 100]} />
              <Radar
                name="Current Scores"
                dataKey="value"
                stroke="#8884d8"
                fill="#8884d8"
                fillOpacity={0.6}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Activity Summary */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Activity Progress</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {selectedActivities.map(activity => (
            <div key={activity} className="p-4 border rounded">
              <h4 className="font-medium">{activity}</h4>
              <div className="mt-2 space-y-2">
                {weeklyResponses.slice(-4).map((response, idx) => (
                  <div key={idx} className="text-sm flex justify-between">
                    <span>Week {weeklyResponses.length - 3 + idx}</span>
                    <span>Completed</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProgressView;
