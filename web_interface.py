#!/usr/bin/env python3
"""
Simple web interface for the TechCorp chatbot using mock services
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'integrations'))

from flask import Flask, render_template, request, jsonify
from mock_services import process_conversation, mock_sheets, mock_slack
import json

app = Flask(__name__)

# Store conversation sessions
sessions = {}

@app.route('/')
def index():
    """Main chatbot interface"""
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.json
    user_input = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    # Get or create session
    if session_id not in sessions:
        sessions[session_id] = {
            'messages': [],
            'user_data': {}
        }
    
    session = sessions[session_id]
    
    # Check if this is a data collection message
    if data.get('collect_data'):
        user_data = data.get('user_data', {})
        session['user_data'].update(user_data)
        
        response = f"Thank you {user_data.get('name', '')}, I've recorded your information. How can I assist you today?"
        result = {
            'response': response,
            'lead_score': 0,
            'user_data': session['user_data']
        }
    else:
        # Process conversation with mock services
        result = process_conversation(user_input, session['user_data'])
    
    # Add to conversation history
    session['messages'].append({
        'user': user_input,
        'bot': result['response'],
        'lead_score': result['lead_score']
    })
    
    return jsonify(result)

@app.route('/leads')
def view_leads():
    """View collected leads"""
    leads = mock_sheets.get_leads()
    return jsonify(leads)

@app.route('/notifications')
def view_notifications():
    """View notifications"""
    notifications = mock_slack.get_notifications()
    return jsonify(notifications)

@app.route('/dashboard')
def dashboard():
    """Admin dashboard"""
    return render_template('dashboard.html')

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = 'templates'
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    print("Starting TechCorp Chatbot Web Interface...")
    print("Access the chatbot at: http://localhost:5000")
    print("Admin dashboard at: http://localhost:5000/dashboard")
    app.run(debug=True, host='0.0.0.0', port=5000)
