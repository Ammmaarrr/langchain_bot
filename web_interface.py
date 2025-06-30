#!/usr/bin/env python3
"""
Simple web interface for the TechCorp chatbot using mock services
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'integrations'))

from flask import Flask, render_template, request, jsonify
from mock_services import enhanced_process_conversation, mock_sheets, mock_slack
from conversation_history import conversation_manager
from techcorp_warp_ai import techcorp_ai
from warpgpt_2_0 import warpgpt
from datetime import datetime
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
        # Use WarpGPT 2.0 for production-grade technical support
        if data.get('use_warpgpt2', False):
            ai_response = warpgpt.process_warp_request(user_input)
            result = {
                'response': ai_response,
                'lead_score': 0,
                'user_data': session['user_data'],
                'warpgpt2': True,
                'system_status': warpgpt.get_system_status()
            }
        # Use TechCorp Warp AI for technical support
        elif data.get('use_warp_ai', False):
            ai_response = techcorp_ai.process_message(user_input, data.get('product', 'system'))
            result = {
                'response': ai_response,
                'lead_score': 0,
                'user_data': session['user_data'],
                'warp_ai': True
            }
        else:
            # Process conversation with enhanced mock services that track history
            result = enhanced_process_conversation(user_input, session['user_data'], session_id)
    
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

@app.route('/conversation-history')
def conversation_history():
    """Get recent conversation history"""
    limit = request.args.get('limit', 20, type=int)
    session_id = request.args.get('session_id')
    
    conversations = conversation_manager.get_recent_conversations(limit, session_id)
    return jsonify({
        'conversations': conversations,
        'stats': conversation_manager.get_conversation_stats()
    })

@app.route('/feedback', methods=['POST'])
def add_feedback():
    """Add feedback for a conversation"""
    data = request.json
    conversation_id = data.get('conversation_id')
    feedback = data.get('feedback')
    quality_rating = data.get('quality_rating', 3)
    suggested_response = data.get('suggested_response')
    
    conversation_manager.add_feedback(
        conversation_id, feedback, quality_rating, suggested_response
    )
    
    return jsonify({'status': 'success', 'message': 'Feedback added successfully'})

@app.route('/learning-data')
def learning_data():
    """Export learning data for analysis"""
    return jsonify(conversation_manager.export_learning_data())

@app.route('/suggest-response', methods=['POST'])
def suggest_response():
    """Get suggested improved response based on learning"""
    data = request.json
    user_input = data.get('user_input', '')
    
    suggested = conversation_manager.suggest_improved_response(user_input)
    
    return jsonify({
        'suggested_response': suggested,
        'has_suggestion': suggested is not None
    })

@app.route('/warp-ai/kb-search', methods=['POST'])
def warp_kb_search():
    """TechCorp Warp AI knowledge base search"""
    data = request.json
    query = data.get('query', '')
    
    results = techcorp_ai.execute_kb_command(query)
    return jsonify(results)

@app.route('/warp-ai/log-solution', methods=['POST'])
def warp_log_solution():
    """Log new solution to TechCorp knowledge base"""
    data = request.json
    problem = data.get('problem', '')
    solution = data.get('solution', '')
    category = data.get('category', 'general')
    
    result = techcorp_ai.execute_log_command(problem, solution, category)
    return jsonify({'status': 'success', 'message': result})

@app.route('/warp-ai/conversation-context')
def warp_conversation_context():
    """Get TechCorp Warp AI conversation context"""
    context = techcorp_ai.get_conversation_context()
    return jsonify({'context': context})

@app.route('/warp-ai/knowledge-base')
def warp_knowledge_base():
    """Get TechCorp knowledge base contents"""
    return jsonify({
        'knowledge_base': techcorp_ai.kb.knowledge_base,
        'solutions_log': techcorp_ai.kb.solutions
    })

@app.route('/warpgpt2/status')
def warpgpt2_status():
    """Get WarpGPT 2.0 system status"""
    return jsonify(warpgpt.get_system_status())

@app.route('/warpgpt2/kb-search', methods=['POST'])
def warpgpt2_kb_search():
    """WarpGPT 2.0 hybrid knowledge base search"""
    data = request.json
    query = data.get('query', '')
    context = data.get('context', {})
    
    results, confidence = warpgpt.execute_kb_search(query, context)
    return jsonify({
        'results': results,
        'confidence': confidence,
        'threshold_met': confidence >= warpgpt.confidence_threshold,
        'verified': confidence >= warpgpt.verified_threshold
    })

@app.route('/warpgpt2/process', methods=['POST'])
def warpgpt2_process():
    """Process request with WarpGPT 2.0 protocols"""
    data = request.json
    user_input = data.get('input', '')
    
    response = warpgpt.process_warp_request(user_input)
    return jsonify({
        'response': response,
        'system_status': warpgpt.get_system_status(),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/warpgpt2/knowledge-base')
def warpgpt2_knowledge_base():
    """Get WarpGPT 2.0 knowledge base"""
    return jsonify({
        'knowledge_base': warpgpt.kb.knowledge_base,
        'total_entries': len(warpgpt.kb.knowledge_base),
        'confidence_threshold': warpgpt.confidence_threshold,
        'verified_threshold': warpgpt.verified_threshold
    })

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
