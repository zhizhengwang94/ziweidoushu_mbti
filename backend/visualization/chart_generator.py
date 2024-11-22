from dataclasses import dataclass
from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta
import json

@dataclass
class ChartData:
    chart_type: str  # 'line', 'bar', 'radar', 'heatmap'
    title: str
    labels: List[str]
    datasets: List[Dict]
    options: Dict

@dataclass
class ChartCollection:
    progress_chart: ChartData
    activity_chart: ChartData
    comparison_chart: ChartData
    insight_chart: ChartData

class ChartGenerator:
    def __init__(self):
        self.color_palette = {
            'primary': '#4F46E5',      # Indigo
            'secondary': '#10B981',    # Emerald
            'accent': '#F59E0B',       # Amber
            'error': '#EF4444',        # Red
            'success': '#22C55E',      # Green
            'info': '#3B82F6'          # Blue
        }

    def generate_progress_chart(self, 
                              metrics: List[Dict[str, Union[str, float, datetime]]]) -> ChartData:
        """Generate overall progress chart"""
        
        # Sort metrics by timestamp
        sorted_metrics = sorted(metrics, key=lambda x: x['timestamp'])
        
        # Prepare data
        labels = [m['timestamp'].strftime('%Y-%m-%d') for m in sorted_metrics]
        datasets = [
            {
                'label': 'Overall Progress',
                'data': [m['score'] for m in sorted_metrics],
                'borderColor': self.color_palette['primary'],
                'fill': False
            }
        ]
        
        return ChartData(
            chart_type='line',
            title='Progress Over Time',
            labels=labels,
            datasets=datasets,
            options={
                'responsive': True,
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'max': 100,
                        'title': {
                            'display': True,
                            'text': 'Progress Score'
                        }
                    },
                    'x': {
                        'title': {
                            'display': True,
                            'text': 'Date'
                        }
                    }
                }
            }
        )

    def generate_activity_chart(self, 
                              activities: Dict[str, Dict[str, float]]) -> ChartData:
        """Generate activity completion and impact chart"""
        
        labels = list(activities.keys())
        completion_data = [activities[a]['completion_rate'] * 100 for a in labels]
        impact_data = [activities[a]['impact_rating'] * 20 for a in labels]  # Scale to 100
        
        datasets = [
            {
                'label': 'Completion Rate',
                'data': completion_data,
                'backgroundColor': self.color_palette['primary'],
            },
            {
                'label': 'Impact Rating',
                'data': impact_data,
                'backgroundColor': self.color_palette['secondary'],
            }
        ]
        
        return ChartData(
            chart_type='bar',
            title='Activity Performance',
            labels=labels,
            datasets=datasets,
            options={
                'responsive': True,
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'max': 100,
                        'title': {
                            'display': True,
                            'text': 'Percentage'
                        }
                    }
                }
            }
        )

    def generate_comparison_chart(self, 
                                current_metrics: Dict[str, float],
                                previous_metrics: Dict[str, float]) -> ChartData:
        """Generate comparison radar chart"""
        
        labels = list(current_metrics.keys())
        
        datasets = [
            {
                'label': 'Current',
                'data': [current_metrics[label] * 100 for label in labels],
                'borderColor': self.color_palette['primary'],
                'backgroundColor': f"{self.color_palette['primary']}40"
            },
            {
                'label': 'Previous',
                'data': [previous_metrics.get(label, 0) * 100 for label in labels],
                'borderColor': self.color_palette['secondary'],
                'backgroundColor': f"{self.color_palette['secondary']}40"
            }
        ]
        
        return ChartData(
            chart_type='radar',
            title='Progress Comparison',
            labels=labels,
            datasets=datasets,
            options={
                'responsive': True,
                'scales': {
                    'r': {
                        'beginAtZero': True,
                        'max': 100
                    }
                }
            }
        )

    def generate_insight_chart(self, 
                             insights: Dict[str, List[Dict]]) -> ChartData:
        """Generate insight heatmap chart"""
        
        categories = list(insights.keys())
        weeks = list(range(1, max(len(data) for data in insights.values()) + 1))
        
        # Create heatmap data
        data = []
        for category in categories:
            category_data = insights[category]
            for week_idx, week_data in enumerate(category_data):
                data.append({
                    'category': category,
                    'week': f'Week {week_idx + 1}',
                    'value': week_data['score'] * 100
                })
        
        return ChartData(
            chart_type='heatmap',
            title='Weekly Insights Heatmap',
            labels={'x': weeks, 'y': categories},
            datasets=[{'data': data}],
            options={
                'responsive': True,
                'colorScale': [
                    {'below': 20, 'color': '#FEE2E2'},
                    {'below': 40, 'color': '#FECACA'},
                    {'below': 60, 'color': '#FCA5A5'},
                    {'below': 80, 'color': '#F87171'},
                    {'below': 101, 'color': '#EF4444'}
                ]
            }
        )

    def generate_chart_collection(self, 
                                metrics: List[Dict],
                                activities: Dict,
                                current_metrics: Dict,
                                previous_metrics: Dict,
                                insights: Dict) -> ChartCollection:
        """Generate a collection of all charts"""
        
        return ChartCollection(
            progress_chart=self.generate_progress_chart(metrics),
            activity_chart=self.generate_activity_chart(activities),
            comparison_chart=self.generate_comparison_chart(current_metrics, previous_metrics),
            insight_chart=self.generate_insight_chart(insights)
        )

    def get_test_data(self) -> ChartCollection:
        """Generate test data for development purposes"""
        
        # Test metrics data
        test_metrics = [
            {'timestamp': datetime.now() - timedelta(days=i), 'score': 60 + i * 2}
            for i in range(10)
        ]
        
        # Test activities data
        test_activities = {
            'Meditation': {'completion_rate': 0.8, 'impact_rating': 4.2},
            'Journaling': {'completion_rate': 0.6, 'impact_rating': 3.8},
            'Exercise': {'completion_rate': 0.9, 'impact_rating': 4.5}
        }
        
        # Test metrics comparison
        test_current = {
            'Personal Growth': 0.75,
            'Emotional Intelligence': 0.65,
            'Social Skills': 0.80,
            'Professional Development': 0.70
        }
        
        test_previous = {
            'Personal Growth': 0.65,
            'Emotional Intelligence': 0.60,
            'Social Skills': 0.75,
            'Professional Development': 0.65
        }
        
        # Test insights data
        test_insights = {
            'Personal Growth': [{'score': 0.7}, {'score': 0.75}, {'score': 0.8}],
            'Emotional Intelligence': [{'score': 0.6}, {'score': 0.65}, {'score': 0.7}],
            'Social Skills': [{'score': 0.75}, {'score': 0.8}, {'score': 0.85}]
        }
        
        return self.generate_chart_collection(
            test_metrics,
            test_activities,
            test_current,
            test_previous,
            test_insights
        )

def test_chart_generator():
    """Test function to verify basic functionality"""
    generator = ChartGenerator()
    chart_collection = generator.get_test_data()
    
    print("\nChart Generator Test Results:")
    
    print("\nProgress Chart:")
    print(f"Type: {chart_collection.progress_chart.chart_type}")
    print(f"Title: {chart_collection.progress_chart.title}")
    print(f"Number of datasets: {len(chart_collection.progress_chart.datasets)}")
    
    print("\nActivity Chart:")
    print(f"Type: {chart_collection.activity_chart.chart_type}")
    print(f"Title: {chart_collection.activity_chart.title}")
    print(f"Activities: {', '.join(chart_collection.activity_chart.labels)}")
    
    print("\nComparison Chart:")
    print(f"Type: {chart_collection.comparison_chart.chart_type}")
    print(f"Title: {chart_collection.comparison_chart.title}")
    print(f"Areas: {', '.join(chart_collection.comparison_chart.labels)}")
    
    print("\nInsight Chart:")
    print(f"Type: {chart_collection.insight_chart.chart_type}")
    print(f"Title: {chart_collection.insight_chart.title}")
    
    return chart_collection

if __name__ == "__main__":
    test_chart_generator()
