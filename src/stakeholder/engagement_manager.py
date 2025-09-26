import json
from datetime import datetime, timedelta
from collections import defaultdict

class EngagementManager:
    def __init__(self):
        self.engagement_strategies = {
            'Government': {
                'communication': 'Direct meetings with city officials and policy makers',
                'participation': 'Public hearings and town hall meetings',
                'collaboration': 'Policy development and implementation support'
            },
            'Community Groups': {
                'communication': 'Community forums and neighborhood meetings',
                'participation': 'Local events and community activities',
                'collaboration': 'Grassroots organizing and community building'
            },
            'Business': {
                'communication': 'Business roundtables and economic development meetings',
                'participation': 'Corporate social responsibility initiatives',
                'collaboration': 'Public-private partnerships and sponsorship'
            },
            'Education': {
                'communication': 'Educational workshops and seminars',
                'participation': 'Student and faculty engagement programs',
                'collaboration': 'Research partnerships and educational initiatives'
            },
            'Healthcare': {
                'communication': 'Health awareness campaigns and workshops',
                'participation': 'Community health programs and screenings',
                'collaboration': 'Public health initiatives and wellness programs'
            },
            'Media': {
                'communication': 'Press releases and media interviews',
                'participation': 'Community journalism and storytelling',
                'collaboration': 'Public awareness campaigns and information sharing'
            },
            'NGOs': {
                'communication': 'Advocacy campaigns and public education',
                'participation': 'Volunteer programs and community service',
                'collaboration': 'Program development and resource sharing'
            }
        }

    def generate_engagement_plan(self, problem_category, stakeholders, problem_severity):
        """Generate a comprehensive engagement plan for a specific problem"""
        
        # Identify relevant stakeholders for the problem category
        relevant_stakeholders = self._identify_relevant_stakeholders(problem_category, stakeholders)
        
        # Create engagement timeline
        timeline = self._create_engagement_timeline(problem_severity)
        
        # Generate specific strategies for each stakeholder type
        strategies = {}
        for stakeholder in relevant_stakeholders:
            if stakeholder.role in self.engagement_strategies:
                strategies[stakeholder.role] = self.engagement_strategies[stakeholder.role]
        
        # Create communication plan
        communication_plan = self._create_communication_plan(problem_category, relevant_stakeholders)
        
        # Generate success metrics
        success_metrics = self._define_success_metrics(problem_category, problem_severity)
        
        engagement_plan = {
            'problem_category': problem_category,
            'severity': problem_severity,
            'relevant_stakeholders': [
                {
                    'name': s.name,
                    'role': s.role,
                    'organization': s.organization,
                    'contact': s.email
                } for s in relevant_stakeholders
            ],
            'timeline': timeline,
            'strategies': strategies,
            'communication_plan': communication_plan,
            'success_metrics': success_metrics,
            'created_date': datetime.now().isoformat()
        }
        
        return engagement_plan

    def _identify_relevant_stakeholders(self, problem_category, all_stakeholders):
        """Identify which stakeholders are most relevant for a specific problem category"""
        category_stakeholder_mapping = {
            'Social Division': ['Government', 'Community Groups', 'Education', 'Media'],
            'Disinformation': ['Media', 'Education', 'Government', 'NGOs'],
            'Community Safety': ['Government', 'Community Groups', 'Business', 'NGOs'],
            'Infrastructure': ['Government', 'Business', 'Community Groups'],
            'Environment': ['Government', 'NGOs', 'Education', 'Community Groups'],
            'Education': ['Education', 'Government', 'Community Groups', 'NGOs'],
            'Healthcare': ['Healthcare', 'Government', 'NGOs', 'Community Groups'],
            'Economic': ['Business', 'Government', 'Education', 'NGOs']
        }
        
        relevant_roles = category_stakeholder_mapping.get(problem_category, [])
        relevant_stakeholders = [
            s for s in all_stakeholders 
            if s.role in relevant_roles
        ]
        
        return relevant_stakeholders

    def _create_engagement_timeline(self, problem_severity):
        """Create a timeline for stakeholder engagement based on problem severity"""
        base_timeline = {
            'immediate': {
                'timeframe': '0-7 days',
                'actions': [
                    'Initial stakeholder notification',
                    'Emergency response coordination',
                    'Crisis communication setup'
                ]
            },
            'short_term': {
                'timeframe': '1-4 weeks',
                'actions': [
                    'Stakeholder meetings and consultations',
                    'Problem analysis and data collection',
                    'Initial solution brainstorming'
                ]
            },
            'medium_term': {
                'timeframe': '1-3 months',
                'actions': [
                    'Solution development and testing',
                    'Community feedback collection',
                    'Implementation planning'
                ]
            },
            'long_term': {
                'timeframe': '3-12 months',
                'actions': [
                    'Solution implementation',
                    'Monitoring and evaluation',
                    'Continuous improvement'
                ]
            }
        }
        
        # Adjust timeline based on severity
        if problem_severity == 'Critical':
            base_timeline['immediate']['actions'].extend([
                'Emergency stakeholder mobilization',
                'Crisis management team activation'
            ])
        elif problem_severity == 'High':
            base_timeline['immediate']['actions'].extend([
                'Priority stakeholder engagement',
                'Accelerated response planning'
            ])
        
        return base_timeline

    def _create_communication_plan(self, problem_category, stakeholders):
        """Create a communication plan for stakeholder engagement"""
        
        communication_channels = {
            'Government': ['Official meetings', 'Public hearings', 'Government websites', 'Press releases'],
            'Community Groups': ['Community forums', 'Social media', 'Newsletters', 'Local events'],
            'Business': ['Business meetings', 'Corporate communications', 'Industry publications'],
            'Education': ['Educational workshops', 'Academic conferences', 'Student organizations'],
            'Healthcare': ['Health forums', 'Medical conferences', 'Health publications'],
            'Media': ['Press conferences', 'Media interviews', 'News articles', 'Social media'],
            'NGOs': ['Advocacy campaigns', 'Community outreach', 'Volunteer networks']
        }
        
        plan = {
            'primary_channels': [],
            'secondary_channels': [],
            'frequency': 'Weekly' if problem_category in ['Social Division', 'Disinformation'] else 'Bi-weekly',
            'key_messages': self._generate_key_messages(problem_category)
        }
        
        # Assign communication channels based on stakeholder types
        for stakeholder in stakeholders:
            if stakeholder.role in communication_channels:
                plan['primary_channels'].extend(communication_channels[stakeholder.role][:2])
                plan['secondary_channels'].extend(communication_channels[stakeholder.role][2:])
        
        # Remove duplicates
        plan['primary_channels'] = list(set(plan['primary_channels']))
        plan['secondary_channels'] = list(set(plan['secondary_channels']))
        
        return plan

    def _generate_key_messages(self, problem_category):
        """Generate key messages for different problem categories"""
        messages = {
            'Social Division': [
                'Building bridges between communities',
                'Promoting understanding and dialogue',
                'Creating inclusive spaces for all voices'
            ],
            'Disinformation': [
                'Fighting misinformation with facts',
                'Promoting media literacy and critical thinking',
                'Building trust through transparency'
            ],
            'Community Safety': [
                'Creating safer neighborhoods together',
                'Building community resilience',
                'Empowering residents to take action'
            ],
            'Infrastructure': [
                'Improving community infrastructure',
                'Building for the future',
                'Ensuring equitable access to services'
            ],
            'Environment': [
                'Protecting our environment for future generations',
                'Building sustainable communities',
                'Taking action on climate change'
            ],
            'Education': [
                'Investing in our children\'s future',
                'Building strong educational foundations',
                'Creating opportunities for all learners'
            ],
            'Healthcare': [
                'Improving community health outcomes',
                'Ensuring access to quality healthcare',
                'Building healthier communities'
            ],
            'Economic': [
                'Building economic opportunities',
                'Supporting local businesses and jobs',
                'Creating shared prosperity'
            ]
        }
        
        return messages.get(problem_category, [
            'Working together for community solutions',
            'Building a better future for all',
            'Creating positive change through collaboration'
        ])

    def _define_success_metrics(self, problem_category, problem_severity):
        """Define success metrics for stakeholder engagement"""
        
        base_metrics = {
            'participation': {
                'stakeholder_attendance': 'Percentage of invited stakeholders participating',
                'community_engagement': 'Number of community members involved',
                'meeting_frequency': 'Regular meeting attendance rates'
            },
            'communication': {
                'message_reach': 'Number of people reached through communications',
                'feedback_collection': 'Amount of stakeholder feedback received',
                'information_sharing': 'Frequency of information updates'
            },
            'collaboration': {
                'solution_development': 'Number of solutions proposed',
                'implementation_progress': 'Percentage of solutions implemented',
                'partnership_formation': 'Number of new partnerships created'
            },
            'impact': {
                'problem_resolution': 'Progress toward problem resolution',
                'community_satisfaction': 'Stakeholder satisfaction scores',
                'sustainable_change': 'Long-term impact indicators'
            }
        }
        
        # Add category-specific metrics
        if problem_category == 'Social Division':
            base_metrics['impact']['social_cohesion'] = 'Measures of community unity and understanding'
        elif problem_category == 'Disinformation':
            base_metrics['impact']['information_quality'] = 'Reduction in misinformation spread'
        elif problem_category == 'Community Safety':
            base_metrics['impact']['safety_improvement'] = 'Reduction in safety incidents'
        
        return base_metrics

    def track_engagement_progress(self, engagement_plan, current_activities):
        """Track progress of stakeholder engagement activities"""
        
        progress_report = {
            'timeline_progress': {},
            'stakeholder_participation': {},
            'communication_effectiveness': {},
            'overall_progress': 0
        }
        
        # Calculate timeline progress
        for phase, details in engagement_plan['timeline'].items():
            completed_actions = len([a for a in current_activities if a.get('phase') == phase and a.get('completed', False)])
            total_actions = len(details['actions'])
            progress_report['timeline_progress'][phase] = {
                'completed': completed_actions,
                'total': total_actions,
                'percentage': (completed_actions / total_actions * 100) if total_actions > 0 else 0
            }
        
        # Calculate overall progress
        all_phases = list(progress_report['timeline_progress'].values())
        if all_phases:
            progress_report['overall_progress'] = sum(p['percentage'] for p in all_phases) / len(all_phases)
        
        return progress_report
