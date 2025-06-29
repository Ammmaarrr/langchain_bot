#!/usr/bin/env python3
"""
Test Runner for TechCorp Chatbot
Demonstrates the chatbot functionality without requiring full Langflow installation
"""

import json
import os
import sys
from typing import Dict, Any
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from integrations.google_sheets_api import GoogleSheetsIntegration
    from integrations.slack_notifications import SlackNotifier
except ImportError as e:
    print(f"Note: Integration modules not available - {e}")
    GoogleSheetsIntegration = None
    SlackNotifier = None

class SimpleBot:
    """Simple chatbot simulator for testing"""
    
    def __init__(self):
        self.conversation_history = []
        
    def classify_intent(self, message: str) -> Dict[str, Any]:
        """Simple intent classification based on keywords"""
        message_lower = message.lower()
        
        # Simple keyword-based classification
        if any(word in message_lower for word in ['buy', 'purchase', 'demo', 'sales', 'pricing', 'quote']):
            return {"intent": "LEAD_QUALIFICATION", "confidence": 85}
        elif any(word in message_lower for word in ['error', 'bug', 'broken', 'issue', 'help', 'technical', 'api']):
            return {"intent": "TECHNICAL_SUPPORT", "confidence": 80}
        elif any(word in message_lower for word in ['order', 'status', 'shipping', 'delivery']):
            return {"intent": "ORDER_STATUS", "confidence": 75}
        elif any(word in message_lower for word in ['bill', 'payment', 'invoice', 'charge']):
            return {"intent": "BILLING_INQUIRY", "confidence": 75}
        elif any(word in message_lower for word in ['complaint', 'angry', 'disappointed', 'unsatisfied']):
            return {"intent": "COMPLAINT", "confidence": 70}
        else:
            return {"intent": "GENERAL_INQUIRY", "confidence": 60}
    
    def calculate_lead_score(self, message: str) -> int:
        """Simple lead scoring algorithm"""
        score = 0
        message_lower = message.lower()
        
        # Budget indicators
        if any(word in message_lower for word in ['$', 'budget', 'thousand', 'million']):
            score += 30
        
        # Timeline indicators  
        if any(word in message_lower for word in ['urgent', 'immediately', 'asap', 'soon']):
            score += 25
            
        # Decision maker indicators
        if any(word in message_lower for word in ['ceo', 'manager', 'director', 'decide']):
            score += 20
            
        # Company size indicators
        if any(word in message_lower for word in ['company', 'employees', 'team', 'organization']):
            score += 15
            
        # Specific use case
        if any(word in message_lower for word in ['crm', 'automation', 'analytics', 'integration']):
            score += 10
            
        return min(score, 100)  # Cap at 100
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """Process a message and return response data"""
        # Classify intent
        intent_data = self.classify_intent(message)
        
        # Generate response based on intent
        if intent_data["intent"] == "LEAD_QUALIFICATION":
            lead_score = self.calculate_lead_score(message)
            response = f"Thank you for your interest in TechCorp Solutions! I'd love to learn more about your needs. What size is your company and what's your timeline for implementation?"
            return {
                "intent": intent_data["intent"],
                "confidence": intent_data["confidence"],
                "response": response,
                "lead_score": lead_score,
                "next_action": "Schedule demo" if lead_score > 70 else "Continue qualification"
            }
        elif intent_data["intent"] == "TECHNICAL_SUPPORT":
            response = f"I'm sorry to hear you're experiencing technical difficulties. Let me help you troubleshoot this issue. Can you provide more details about the specific error you're encountering?"
            return {
                "intent": intent_data["intent"],
                "confidence": intent_data["confidence"],
                "response": response,
                "severity": "MEDIUM",
                "escalation_needed": False
            }
        else:
            response = f"Thank you for contacting TechCorp Solutions! How can I assist you today? We offer CRM Platform, Marketing Automation, and Data Analytics solutions."
            return {
                "intent": intent_data["intent"],
                "confidence": intent_data["confidence"],
                "response": response,
                "interest_level": "MEDIUM",
                "sales_referral": False
            }

def run_demo():
    """Run a demonstration of the chatbot"""
    print("🤖 TechCorp Solutions Chatbot Demo")
    print("=" * 50)
    
    bot = SimpleBot()
    
    # Test scenarios
    test_messages = [
        "I'm interested in your CRM solution for my company",
        "We have a budget of around $50,000 for this project",
        "Our system is down and we can't access any data - this is critical!",
        "Can you tell me about your products and pricing?",
        "I'm the CEO of a 500-person company with a $100k budget for immediate CRM implementation"
    ]
    
    print("\n📝 Running Test Scenarios:")
    print("-" * 30)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n💬 Test {i}: {message}")
        result = bot.process_message(message)
        
        print(f"🎯 Intent: {result['intent']} (Confidence: {result.get('confidence', 0)}%)")
        print(f"🤖 Response: {result['response']}")
        
        if 'lead_score' in result:
            print(f"📊 Lead Score: {result['lead_score']}")
            print(f"⏭️  Next Action: {result['next_action']}")
        
        if 'severity' in result:
            print(f"🚨 Severity: {result['severity']}")
        
        print("-" * 50)

def load_project_data():
    """Load and display project configuration"""
    print("\n📋 Project Configuration:")
    print("-" * 30)
    
    # Load flow data
    try:
        with open('flows/main-support-flow.json', 'r') as f:
            flow_data = json.load(f)
        print(f"✅ Main flow loaded: {len(flow_data.get('data', {}).get('nodes', []))} nodes")
    except Exception as e:
        print(f"❌ Could not load flow: {e}")
    
    # Load knowledge base
    try:
        with open('data/faq-knowledge-base.json', 'r') as f:
            faq_data = json.load(f)
        print(f"✅ FAQ knowledge base: {len(faq_data.get('categories', []))} categories")
    except Exception as e:
        print(f"❌ Could not load FAQ data: {e}")
    
    # Load product catalog
    try:
        with open('data/product-catalog.json', 'r') as f:
            product_data = json.load(f)
        print(f"✅ Product catalog: {len(product_data.get('products', []))} products")
    except Exception as e:
        print(f"❌ Could not load product data: {e}")
    
    # Check environment variables
    print(f"\n🔧 Environment Status:")
    required_vars = ['OPENAI_API_KEY', 'GOOGLE_SHEETS_CREDENTIALS_FILE', 'SLACK_BOT_TOKEN']
    for var in required_vars:
        status = "✅ Set" if os.getenv(var) else "❌ Not set"
        print(f"  {var}: {status}")

def test_integrations():
    """Test the integration modules"""
    print("\n🔌 Testing Integrations:")
    print("-" * 30)
    
    # Test Google Sheets integration
    if GoogleSheetsIntegration:
        try:
            # This will fail without proper credentials, but we can test the class exists
            print("✅ Google Sheets integration module loaded")
        except Exception as e:
            print(f"❌ Google Sheets integration error: {e}")
    else:
        print("❌ Google Sheets integration not available")
    
    # Test Slack integration
    if SlackNotifier:
        try:
            print("✅ Slack notification module loaded")
        except Exception as e:
            print(f"❌ Slack integration error: {e}")
    else:
        print("❌ Slack integration not available")

if __name__ == "__main__":
    print("🚀 TechCorp Solutions Chatbot Challenge - Test Runner")
    print("=" * 60)
    
    try:
        # Load project data
        load_project_data()
        
        # Test integrations
        test_integrations()
        
        # Run the demo
        run_demo()
        
        print("\n🎉 Demo completed successfully!")
        print("\nTo run the full Langflow setup:")
        print("1. Install Microsoft C++ Build Tools")
        print("2. Run: pip install langflow")
        print("3. Run: langflow run")
        print("4. Import flows from the flows/ directory")
        print("\nAlternatively, use Docker:")
        print("1. Install Docker")
        print("2. Configure your .env file with API keys")
        print("3. Run: docker-compose up -d")
        
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()
