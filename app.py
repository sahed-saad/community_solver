from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import json
import os
from src.ai_analysis.problem_analyzer import ProblemAnalyzer
from src.visualization.chart_generator import ChartGenerator
from src.stakeholder.engagement_manager import EngagementManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'community-solver-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///community_solver.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# Initialize components
problem_analyzer = ProblemAnalyzer()
chart_generator = ChartGenerator()
engagement_manager = EngagementManager()

# Database Models
class CommunityProblem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    submitted_by = db.Column(db.String(100), nullable=False)
    submitted_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Open')
    ai_analysis = db.Column(db.Text)
    stakeholder_count = db.Column(db.Integer, default=0)
    solution_count = db.Column(db.Integer, default=0)

class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('community_problem.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    proposed_by = db.Column(db.String(100), nullable=False)
    proposed_date = db.Column(db.DateTime, default=datetime.utcnow)
    votes = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='Proposed')

class Stakeholder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    organization = db.Column(db.String(200))
    interests = db.Column(db.Text)
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    problems = CommunityProblem.query.order_by(CommunityProblem.submitted_date.desc()).limit(6).all()
    total_problems = CommunityProblem.query.count()
    total_solutions = Solution.query.count()
    total_stakeholders = Stakeholder.query.count()
    
    return render_template('index.html', 
                         problems=problems,
                         total_problems=total_problems,
                         total_solutions=total_solutions,
                         total_stakeholders=total_stakeholders)

@app.route('/submit_problem', methods=['GET', 'POST'])
def submit_problem():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        severity = request.form['severity']
        location = request.form['location']
        submitted_by = request.form['submitted_by']
        
        # AI Analysis
        ai_analysis = problem_analyzer.analyze_problem(title, description, category)
        
        problem = CommunityProblem(
            title=title,
            description=description,
            category=category,
            severity=severity,
            location=location,
            submitted_by=submitted_by,
            ai_analysis=ai_analysis
        )
        
        db.session.add(problem)
        db.session.commit()
        
        flash('Problem submitted successfully!', 'success')
        return redirect(url_for('view_problem', id=problem.id))
    
    return render_template('submit_problem.html')

@app.route('/problem/<int:id>')
def view_problem(id):
    problem = CommunityProblem.query.get_or_404(id)
    solutions = Solution.query.filter_by(problem_id=id).order_by(Solution.votes.desc()).all()
    return render_template('view_problem.html', problem=problem, solutions=solutions)

@app.route('/submit_solution/<int:problem_id>', methods=['GET', 'POST'])
def submit_solution(problem_id):
    problem = CommunityProblem.query.get_or_404(problem_id)
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        proposed_by = request.form['proposed_by']
        
        solution = Solution(
            problem_id=problem_id,
            title=title,
            description=description,
            proposed_by=proposed_by
        )
        
        db.session.add(solution)
        problem.solution_count += 1
        db.session.commit()
        
        flash('Solution submitted successfully!', 'success')
        return redirect(url_for('view_problem', id=problem_id))
    
    return render_template('submit_solution.html', problem=problem)

@app.route('/vote_solution/<int:solution_id>')
def vote_solution(solution_id):
    solution = Solution.query.get_or_404(solution_id)
    solution.votes += 1
    db.session.commit()
    return redirect(url_for('view_problem', id=solution.problem_id))

@app.route('/join_stakeholder', methods=['GET', 'POST'])
def join_stakeholder():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        organization = request.form.get('organization', '')
        interests = request.form.get('interests', '')
        
        stakeholder = Stakeholder(
            name=name,
            email=email,
            role=role,
            organization=organization,
            interests=interests
        )
        
        db.session.add(stakeholder)
        db.session.commit()
        
        flash('Successfully joined as stakeholder!', 'success')
        return redirect(url_for('index'))
    
    return render_template('join_stakeholder.html')

@app.route('/dashboard')
def dashboard():
    problems = CommunityProblem.query.all()
    solutions = Solution.query.all()
    stakeholders = Stakeholder.query.all()
    
    # Generate charts
    category_chart = chart_generator.generate_category_chart(problems)
    severity_chart = chart_generator.generate_severity_chart(problems)
    timeline_chart = chart_generator.generate_timeline_chart(problems)
    
    return render_template('dashboard.html',
                         problems=problems,
                         solutions=solutions,
                         stakeholders=stakeholders,
                         category_chart=category_chart,
                         severity_chart=severity_chart,
                         timeline_chart=timeline_chart)

@app.route('/api/problems')
def api_problems():
    problems = CommunityProblem.query.all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'category': p.category,
        'severity': p.severity,
        'location': p.location,
        'status': p.status,
        'submitted_date': p.submitted_date.isoformat(),
        'stakeholder_count': p.stakeholder_count,
        'solution_count': p.solution_count
    } for p in problems])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
