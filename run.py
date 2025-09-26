#!/usr/bin/env python3
"""
Community Solver - Main Application Runner
BYTE Hacks 2024 - Strengthening Society
"""

import os
import sys
from app import app, db

def setup_database():
    """Initialize the database with sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if we already have data
        from app import CommunityProblem, Solution, Stakeholder
        
        if CommunityProblem.query.count() == 0:
            print("Setting up sample data...")
            
            # Add sample problems
            sample_problems = [
                {
                    'title': 'Social Media Polarization in Local Community',
                    'description': 'Increasing division between different community groups due to misinformation and echo chambers on social media platforms. This is affecting local decision-making and community cohesion.',
                    'category': 'Social Division',
                    'severity': 'High',
                    'location': 'Springfield, IL',
                    'submitted_by': 'Community Organizer',
                    'ai_analysis': '{"sentiment": {"sentiment": "Negative", "polarity": -0.3}, "key_issues": {"top_issues": {"community": 2, "social": 2, "media": 1}, "total_issues": 3}}'
                },
                {
                    'title': 'Fake News Spread About Local School Board',
                    'description': 'False information about school board decisions is spreading rapidly through social media, causing confusion and mistrust among parents and community members.',
                    'category': 'Disinformation',
                    'severity': 'Critical',
                    'location': 'Austin, TX',
                    'submitted_by': 'School Board Member',
                    'ai_analysis': '{"sentiment": {"sentiment": "Negative", "polarity": -0.5}, "key_issues": {"top_issues": {"school": 2, "board": 1, "information": 1}, "total_issues": 3}}'
                },
                {
                    'title': 'Neighborhood Safety Concerns',
                    'description': 'Residents are reporting increased safety concerns in the downtown area, with limited street lighting and reduced police presence during evening hours.',
                    'category': 'Community Safety',
                    'severity': 'High',
                    'location': 'Portland, OR',
                    'submitted_by': 'Downtown Resident',
                    'ai_analysis': '{"sentiment": {"sentiment": "Negative", "polarity": -0.2}, "key_issues": {"top_issues": {"safety": 2, "downtown": 1, "lighting": 1}, "total_issues": 3}}'
                }
            ]
            
            for problem_data in sample_problems:
                problem = CommunityProblem(**problem_data)
                db.session.add(problem)
            
            # Add sample solutions
            sample_solutions = [
                {
                    'problem_id': 1,
                    'title': 'Community Dialogue Initiative',
                    'description': 'Organize monthly community forums where different groups can come together to discuss issues face-to-face, breaking down social media echo chambers.',
                    'proposed_by': 'Local NGO Representative',
                    'votes': 15
                },
                {
                    'problem_id': 1,
                    'title': 'Media Literacy Workshop Series',
                    'description': 'Create educational workshops for community members to learn how to identify misinformation and engage with diverse perspectives online.',
                    'proposed_by': 'Education Coordinator',
                    'votes': 12
                },
                {
                    'problem_id': 2,
                    'title': 'Official Information Portal',
                    'description': 'Establish a verified, official information portal where the school board can share accurate information and quickly address misinformation.',
                    'proposed_by': 'School Board President',
                    'votes': 8
                }
            ]
            
            for solution_data in sample_solutions:
                solution = Solution(**solution_data)
                db.session.add(solution)
            
            # Add sample stakeholders
            sample_stakeholders = [
                {
                    'name': 'Dr. Sarah Johnson',
                    'email': 'sarah.johnson@city.gov',
                    'role': 'Government',
                    'organization': 'City Council',
                    'interests': 'Community development, social cohesion, public policy'
                },
                {
                    'name': 'Michael Chen',
                    'email': 'michael@springfield-community.org',
                    'role': 'Community Groups',
                    'organization': 'Springfield Community Alliance',
                    'interests': 'Grassroots organizing, community building, social justice'
                },
                {
                    'name': 'Lisa Rodriguez',
                    'email': 'lisa@springfield-news.com',
                    'role': 'Media',
                    'organization': 'Springfield Daily News',
                    'interests': 'Local journalism, fact-checking, community information'
                },
                {
                    'name': 'Prof. David Kim',
                    'email': 'd.kim@university.edu',
                    'role': 'Education',
                    'organization': 'Springfield University',
                    'interests': 'Media literacy, digital citizenship, community education'
                }
            ]
            
            for stakeholder_data in sample_stakeholders:
                stakeholder = Stakeholder(**stakeholder_data)
                db.session.add(stakeholder)
            
            db.session.commit()
            print("Sample data added successfully!")
        else:
            print("Database already contains data.")

def main():
    """Main application entry point"""
    print("=" * 60)
    print("🌍 Community Solver - BYTE Hacks 2024")
    print("   Strengthening Society Through Collaborative Problem-Solving")
    print("=" * 60)
    
    # Setup database
    setup_database()
    
    # Get configuration
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print(f"\n🚀 Starting Community Solver...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Debug: {debug_mode}")
    print(f"\n📱 Access the application at: http://localhost:{port}")
    print(f"📊 Dashboard: http://localhost:{port}/dashboard")
    print(f"📝 Submit Problem: http://localhost:{port}/submit_problem")
    print(f"🤝 Join as Stakeholder: http://localhost:{port}/join_stakeholder")
    print("\n" + "=" * 60)
    
    # Run the application
    app.run(debug=debug_mode, host=host, port=port)

if __name__ == '__main__':
    main()
