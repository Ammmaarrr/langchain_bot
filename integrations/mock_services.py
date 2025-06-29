#!/usr/bin/env python3
"""
Mock services for local development without external API dependencies
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockOpenAI:
    """Mock OpenAI service for local testing"""
    
    def __init__(self):
        self.responses = {
            "greeting": "Hello! I'm your TechCorp support assistant. How can I help you today?",
            "product_inquiry": "I'd be happy to help you learn about our products. We offer enterprise software solutions, cloud services, and consulting.",
            "support": "I understand you need technical support. Let me connect you with our support team or help troubleshoot your issue.",
            "pricing": "For pricing information, I can schedule a call with our sales team who can provide a customized quote based on your needs.",
            "default": "Thank you for your message. Let me help you with that inquiry."
        }
    
    def generate_response(self, user_input: str, context: str = "") -> str:
        """Generate a mock AI response based on user input"""
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ["hello", "hi", "hey"]):
            return self.responses["greeting"]
        elif any(word in user_input_lower for word in ["product", "service", "what do you"]):
            return self.responses["product_inquiry"]
        elif any(word in user_input_lower for word in ["support", "help", "problem", "issue"]):
            return self.responses["support"]
        elif any(word in user_input_lower for word in ["price", "cost", "pricing"]):
            return self.responses["pricing"]
        else:
            return self.responses["default"]

class MockGoogleSheets:
    """Mock Google Sheets service for local testing"""
    
    def __init__(self):
        self.data_file = "data/mock_leads.json"
        self.leads = []
        self.load_data()
    
    def load_data(self):
        """Load existing lead data"""
        try:
            with open(self.data_file, 'r') as f:
                self.leads = json.load(f)
        except FileNotFoundError:
            self.leads = []
            logger.info("Created new leads database")
    
    def save_data(self):
        """Save lead data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.leads, f, indent=2)
    
    def add_lead(self, lead_data: Dict[str, Any]) -> bool:
        """Add a new lead to the mock database"""
        lead_entry = {
            "timestamp": datetime.now().isoformat(),
            "name": lead_data.get("name", "Unknown"),
            "email": lead_data.get("email", ""),
            "company": lead_data.get("company", ""),
            "inquiry_type": lead_data.get("inquiry_type", "General"),
            "lead_score": lead_data.get("lead_score", 0),
            "conversation_log": lead_data.get("conversation_log", [])
        }
        
        self.leads.append(lead_entry)
        self.save_data()
        logger.info(f"Added new lead: {lead_entry['name']} ({lead_entry['email']})")
        return True
    
    def get_leads(self) -> List[Dict[str, Any]]:
        """Get all leads"""
        return self.leads

class MockSlack:
    """Mock Slack service for local testing"""
    
    def __init__(self):
        self.notifications_file = "data/mock_notifications.json"
        self.notifications = []
        self.load_notifications()
    
    def load_notifications(self):
        """Load existing notifications"""
        try:
            with open(self.notifications_file, 'r') as f:
                self.notifications = json.load(f)
        except FileNotFoundError:
            self.notifications = []
            logger.info("Created new notifications log")
    
    def save_notifications(self):
        """Save notifications to file"""
        with open(self.notifications_file, 'w') as f:
            json.dump(self.notifications, f, indent=2)
    
    def send_notification(self, message: str, priority: str = "normal") -> bool:
        """Send a mock notification"""
        notification = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "priority": priority,
            "channel": "#customer-support"
        }
        
        self.notifications.append(notification)
        self.save_notifications()
        logger.info(f"Slack notification sent: {message[:50]}...")
        return True
    
    def get_notifications(self) -> List[Dict[str, Any]]:
        """Get all notifications"""
        return self.notifications

class LeadScorer:
    """Lead scoring system"""
    
    def __init__(self):
        with open('data/lead-scoring-rules.json', 'r') as f:
            self.scoring_rules = json.load(f)
    
    def calculate_score(self, lead_data: Dict[str, Any]) -> int:
        """Calculate lead score based on conversation data"""
        score = 0
        
        # Company size scoring
        company = lead_data.get("company", "").lower()
        if any(word in company for word in ["enterprise", "corp", "inc", "ltd"]):
            score += 20
        
        # Inquiry type scoring
        inquiry_type = lead_data.get("inquiry_type", "").lower()
        if "enterprise" in inquiry_type:
            score += 30
        elif "pricing" in inquiry_type:
            score += 25
        elif "demo" in inquiry_type:
            score += 20
        
        # Email domain scoring
        email = lead_data.get("email", "")
        if email and not email.endswith(('@gmail.com', '@yahoo.com', '@hotmail.com')):
            score += 15  # Business email
        
        return min(score, 100)  # Cap at 100

# Initialize services
mock_openai = MockOpenAI()
mock_sheets = MockGoogleSheets()
mock_slack = MockSlack()
lead_scorer = LeadScorer()

def process_conversation(user_input: str, user_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Process a conversation turn with mock services"""
    if user_data is None:
        user_data = {}
    
    # Generate AI response
    ai_response = mock_openai.generate_response(user_input)
    
    # Calculate lead score if we have user data
    lead_score = 0
    if user_data.get("email"):
        lead_score = lead_scorer.calculate_score(user_data)
        
        # Add to CRM if score is high enough
        if lead_score >= 50:
            mock_sheets.add_lead({
                **user_data,
                "lead_score": lead_score,
                "conversation_log": [user_input, ai_response]
            })
            
            # Send notification for high-priority leads
            if lead_score >= 80:
                mock_slack.send_notification(
                    f"High-priority lead: {user_data.get('name', 'Unknown')} (Score: {lead_score})",
                    "high"
                )
    
    return {
        "response": ai_response,
        "lead_score": lead_score,
        "user_data": user_data
    }

if __name__ == "__main__":
    # Test the mock services
    print("Testing mock services...")
    
    # Test conversation
    result = process_conversation(
        "Hi, I'm interested in your enterprise software solutions",
        {
            "name": "John Doe",
            "email": "john@enterprise-corp.com",
            "company": "Enterprise Corp",
            "inquiry_type": "enterprise"
        }
    )
    
    print(f"AI Response: {result['response']}")
    print(f"Lead Score: {result['lead_score']}")
    print("Mock services test completed!")
