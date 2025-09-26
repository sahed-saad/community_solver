import json
from collections import Counter
from datetime import datetime, timedelta

class ChartGenerator:
    def __init__(self):
        self.chart_colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#F18F01',
            'warning': '#C73E1D',
            'info': '#7209B7'
        }

    def generate_category_chart(self, problems):
        """Generate chart data for problem categories"""
        categories = [p.category for p in problems]
        category_counts = Counter(categories)
        
        chart_data = {
            'type': 'doughnut',
            'data': {
                'labels': list(category_counts.keys()),
                'datasets': [{
                    'label': 'Problems by Category',
                    'data': list(category_counts.values()),
                    'backgroundColor': [
                        self.chart_colors['primary'],
                        self.chart_colors['secondary'],
                        self.chart_colors['success'],
                        self.chart_colors['warning'],
                        self.chart_colors['info']
                    ],
                    'borderWidth': 2,
                    'borderColor': '#ffffff'
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'legend': {
                        'position': 'bottom'
                    },
                    'title': {
                        'display': True,
                        'text': 'Community Problems by Category'
                    }
                }
            }
        }
        
        return json.dumps(chart_data)

    def generate_severity_chart(self, problems):
        """Generate chart data for problem severity"""
        severities = [p.severity for p in problems]
        severity_counts = Counter(severities)
        
        # Define severity order and colors
        severity_order = ['Critical', 'High', 'Medium', 'Low']
        severity_colors = {
            'Critical': '#C73E1D',
            'High': '#F18F01',
            'Medium': '#2E86AB',
            'Low': '#A23B72'
        }
        
        ordered_data = []
        ordered_colors = []
        ordered_labels = []
        
        for severity in severity_order:
            if severity in severity_counts:
                ordered_data.append(severity_counts[severity])
                ordered_colors.append(severity_colors[severity])
                ordered_labels.append(severity)
        
        chart_data = {
            'type': 'bar',
            'data': {
                'labels': ordered_labels,
                'datasets': [{
                    'label': 'Problems by Severity',
                    'data': ordered_data,
                    'backgroundColor': ordered_colors,
                    'borderColor': ordered_colors,
                    'borderWidth': 1
                }]
            },
            'options': {
                'responsive': True,
                'scales': {
                    'y': {
                        'beginAtZero': True
                    }
                },
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Problem Severity Distribution'
                    }
                }
            }
        }
        
        return json.dumps(chart_data)

    def generate_timeline_chart(self, problems):
        """Generate timeline chart for problem submissions"""
        # Group problems by month
        monthly_counts = {}
        
        for problem in problems:
            month_key = problem.submitted_date.strftime('%Y-%m')
            monthly_counts[month_key] = monthly_counts.get(month_key, 0) + 1
        
        # Sort by date
        sorted_months = sorted(monthly_counts.items())
        
        if not sorted_months:
            return json.dumps({
                'type': 'line',
                'data': {'labels': [], 'datasets': []},
                'options': {'responsive': True}
            })
        
        labels = [item[0] for item in sorted_months]
        data = [item[1] for item in sorted_months]
        
        chart_data = {
            'type': 'line',
            'data': {
                'labels': labels,
                'datasets': [{
                    'label': 'Problems Submitted',
                    'data': data,
                    'borderColor': self.chart_colors['primary'],
                    'backgroundColor': self.chart_colors['primary'] + '20',
                    'fill': True,
                    'tension': 0.4
                }]
            },
            'options': {
                'responsive': True,
                'scales': {
                    'y': {
                        'beginAtZero': True
                    }
                },
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Problem Submission Timeline'
                    }
                }
            }
        }
        
        return json.dumps(chart_data)

    def generate_solution_effectiveness_chart(self, problems, solutions):
        """Generate chart showing solution effectiveness"""
        problem_solution_counts = {}
        
        for problem in problems:
            solution_count = len([s for s in solutions if s.problem_id == problem.id])
            problem_solution_counts[problem.category] = problem_solution_counts.get(problem.category, 0) + solution_count
        
        chart_data = {
            'type': 'bar',
            'data': {
                'labels': list(problem_solution_counts.keys()),
                'datasets': [{
                    'label': 'Solutions Proposed',
                    'data': list(problem_solution_counts.values()),
                    'backgroundColor': self.chart_colors['success'],
                    'borderColor': self.chart_colors['success'],
                    'borderWidth': 1
                }]
            },
            'options': {
                'responsive': True,
                'scales': {
                    'y': {
                        'beginAtZero': True
                    }
                },
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Solutions by Problem Category'
                    }
                }
            }
        }
        
        return json.dumps(chart_data)

    def generate_stakeholder_engagement_chart(self, stakeholders):
        """Generate chart for stakeholder engagement"""
        roles = [s.role for s in stakeholders]
        role_counts = Counter(roles)
        
        chart_data = {
            'type': 'pie',
            'data': {
                'labels': list(role_counts.keys()),
                'datasets': [{
                    'label': 'Stakeholders by Role',
                    'data': list(role_counts.values()),
                    'backgroundColor': [
                        self.chart_colors['primary'],
                        self.chart_colors['secondary'],
                        self.chart_colors['success'],
                        self.chart_colors['warning'],
                        self.chart_colors['info']
                    ],
                    'borderWidth': 2,
                    'borderColor': '#ffffff'
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'legend': {
                        'position': 'right'
                    },
                    'title': {
                        'display': True,
                        'text': 'Stakeholder Distribution by Role'
                    }
                }
            }
        }
        
        return json.dumps(chart_data)
