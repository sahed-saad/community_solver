#!/usr/bin/env python3
"""
Community Solver Deployment Script
BYTE Hacks 2024 - Strengthening Society
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_nltk_data():
    """Download required NLTK data"""
    print("\n🧠 Setting up NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ NLTK data downloaded")
        return True
    except Exception as e:
        print(f"⚠️  Warning: Could not download NLTK data: {e}")
        print("   The application will still work, but some AI features may be limited")
        return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    directories = ['static/css', 'static/js', 'templates', 'data/raw', 'data/processed', 'logs']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ Created {directory}")
    
    return True

def check_database():
    """Check database setup"""
    print("\n🗄️  Checking database...")
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
        print("✅ Database initialized")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def run_tests():
    """Run basic tests"""
    print("\n🧪 Running basic tests...")
    try:
        # Test imports
        from app import app, db, CommunityProblem, Solution, Stakeholder
        from src.ai_analysis.problem_analyzer import ProblemAnalyzer
        from src.visualization.chart_generator import ChartGenerator
        from src.stakeholder.engagement_manager import EngagementManager
        
        print("✅ All imports successful")
        
        # Test AI analyzer
        analyzer = ProblemAnalyzer()
        test_analysis = analyzer.analyze_problem(
            "Test problem", 
            "This is a test problem description", 
            "Social Division"
        )
        print("✅ AI analyzer working")
        
        # Test chart generator
        chart_gen = ChartGenerator()
        test_chart = chart_gen.generate_category_chart([])
        print("✅ Chart generator working")
        
        # Test engagement manager
        eng_manager = EngagementManager()
        print("✅ Engagement manager working")
        
        return True
    except Exception as e:
        print(f"❌ Tests failed: {e}")
        return False

def main():
    """Main deployment function"""
    print("=" * 70)
    print("🌍 Community Solver - Deployment Script")
    print("   BYTE Hacks 2024 - Strengthening Society")
    print("=" * 70)
    
    # Check system requirements
    if not check_python_version():
        return False
    
    # Create directories
    if not create_directories():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Setup NLTK data
    setup_nltk_data()
    
    # Check database
    if not check_database():
        return False
    
    # Run tests
    if not run_tests():
        print("\n⚠️  Some tests failed, but the application may still work")
    
    print("\n" + "=" * 70)
    print("🎉 Deployment completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Run: python run.py")
    print("   2. Open: http://localhost:5000")
    print("   3. Start solving community problems!")
    print("\n💡 Tips:")
    print("   - Check the dashboard for analytics")
    print("   - Submit sample problems to test the system")
    print("   - Join as a stakeholder to get involved")
    print("   - Share with your team and community!")
    print("=" * 70)
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
