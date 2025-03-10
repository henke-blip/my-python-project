import os
import logging
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from trends import get_trending_topics, get_trend_data
from ai_generator import generate_content_ideas
from affiliates import get_affiliate_opportunities

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Trends route
@app.route('/trends')
def trends():
    trending_topics = get_trending_topics()
    return render_template('trends.html', trending_topics=trending_topics)

# Get trend data for specific topic
@app.route('/trend_data/<topic>')
def trend_data(topic):
    data = get_trend_data(topic)
    return jsonify(data)

# Content Ideas route
@app.route('/content_ideas', methods=['GET', 'POST'])
def content_ideas():
    ideas = []
    topic = ""
    
    if request.method == 'POST':
        topic = request.form.get('topic', '')
        category = request.form.get('category', 'all')
        
        if topic:
            ideas = generate_content_ideas(topic, category)
    
    return render_template('content_ideas.html', ideas=ideas, topic=topic)

# Affiliate opportunities route
@app.route('/affiliates')
def affiliates():
    trending_topics = get_trending_topics()
    opportunities = {}
    
    for topic in trending_topics[:5]:  # Only get opportunities for top 5 trends
        opportunities[topic] = get_affiliate_opportunities(topic)
    
    return render_template('affiliates.html', opportunities=opportunities)

# API endpoint to get content ideas
@app.route('/api/content_ideas', methods=['POST'])
def api_content_ideas():
    data = request.get_json()
    topic = data.get('topic', '')
    category = data.get('category', 'all')
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    ideas = generate_content_ideas(topic, category)
    return jsonify({'ideas': ideas})

# API endpoint to get affiliate opportunities
@app.route('/api/affiliates/<topic>')
def api_affiliates(topic):
    opportunities = get_affiliate_opportunities(topic)
    return jsonify({'opportunities': opportunities})
