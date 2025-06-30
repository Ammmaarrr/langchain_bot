#!/usr/bin/env python3
"""
Mock services for local development without external API dependencies
"""

import json
import logging
import re
import time
from datetime import datetime
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockOpenAI:
    """Mock OpenAI service for local testing"""
    
    def __init__(self):
        import re
        self.responses = {
            "greeting": [
                "Hello! I'm your TechCorp support assistant. How can I help you today?",
                "Hi there! Welcome to TechCorp. What can I assist you with?",
                "Greetings! I'm here to help you with any questions about our services."
            ],
            "product_inquiry": [
                "I'd be happy to help you learn about our products. We offer enterprise software solutions, cloud services, and consulting.",
                "Great question! Our main offerings include AI-powered business automation, cloud infrastructure, and custom software development.",
                "We specialize in enterprise solutions including CRM systems, data analytics platforms, and digital transformation services."
            ],
            "support": [
                "I understand you need technical support. Let me connect you with our support team or help troubleshoot your issue.",
                "I'm here to help with your technical concerns. Could you please describe the specific issue you're experiencing?",
                "Our technical support team is ready to assist. What problem are you encountering?"
            ],
            "pricing": [
                "For pricing information, I can schedule a call with our sales team who can provide a customized quote based on your needs.",
                "Our pricing is tailored to each client's requirements. Would you like me to connect you with our sales team for a detailed quote?",
                "Pricing varies based on your specific needs and scale. Let me arrange a consultation to discuss your requirements."
            ],
            "demo": [
                "I'd be happy to arrange a demo for you! Our product demonstrations show real-world applications of our solutions.",
                "Absolutely! A demo is a great way to see our platform in action. When would be convenient for you?",
                "Perfect! Our demos typically cover key features and can be customized to your industry needs."
            ],
            "enterprise": [
                "Our enterprise solutions are designed for large-scale operations with advanced security and compliance features.",
                "For enterprise clients, we offer dedicated support, custom integrations, and scalable architecture.",
                "Enterprise packages include priority support, advanced analytics, and white-label options."
            ],
            "integration": [
                "We support integrations with major platforms including Salesforce, Microsoft 365, and Google Workspace.",
                "Our API-first approach makes integration seamless with your existing tech stack.",
                "Integration typically takes 2-4 weeks depending on complexity and can be done with minimal downtime."
            ],
            "company_info": [
                "TechCorp is a leading provider of enterprise AI solutions, founded in 2020. We specialize in business automation, cloud services, and digital transformation.",
                "We're TechCorp - your trusted partner for enterprise technology solutions. We serve Fortune 500 companies with cutting-edge AI and cloud infrastructure.",
                "TechCorp offers comprehensive enterprise solutions including CRM systems, data analytics, AI automation, and cloud migration services to help businesses scale efficiently."
            ],
            "about": [
                "About TechCorp: We're innovators in enterprise technology, helping businesses transform through AI-powered solutions and scalable cloud infrastructure.",
                "TechCorp was founded with a mission to simplify enterprise technology. We provide end-to-end solutions from consultation to implementation and support.",
                "Our company focuses on delivering measurable business value through advanced technology solutions, serving clients across healthcare, finance, and manufacturing sectors."
            ],
            "goodbye": [
                "Thank you for contacting TechCorp! Have a great day and feel free to reach out anytime.",
                "It was great helping you today! Don't hesitate to contact us if you need anything else.",
                "Goodbye! We look forward to working with you soon."
            ],
            "default": [
                "Thank you for your message. Let me help you with that inquiry.",
                "I'm here to assist you. Could you please provide more details about what you're looking for?",
                "That's an interesting question. How can I best help you with your needs?"
            ]
        }
        self.conversation_count = 0
    
    def generate_response(self, user_input: str, context: str = "") -> str:
        """Generate a mock AI response based on user input"""
        user_input_lower = user_input.lower()
        self.conversation_count += 1
        
        # Comprehensive prompt handling
        pattern_response_mapping = [
            (r"hello|hi|hey|good morning|good afternoon|what's up", "greeting"),
            (r"bye|goodbye|thanks|thank you|that's all|see you", "goodbye"),
            (r"(product|service|offerings|solutions|sell|provide|manufacture)", "product_inquiry"),
            (r"(support|help|problem|issue|trouble|error|assist|call|contact)", "support"),
            (r"(price|cost|pricing|quote|budget|charge|expense)", "pricing"),
            (r"(demo|demonstration|show me|trial|see)", "demo"),
            (r"(enterprise|corporation|business|company|firm|organization)", "enterprise"),
            (r"(integration|integrate|api|connect|sync|support)", "integration"),
            (r"(company|about|who are you|tell me|background|history|info)", "company_info"),
            (r"(about|details|information|data|insight|facts)", "about")
        ]

        for pattern, response_category in pattern_response_mapping:
            if re.search(pattern, user_input_lower):
                return self._get_random_response(response_category)

        # Category matching
        if any(word in user_input_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return self._get_random_response("greeting")
        
        # Goodbye patterns
        elif any(word in user_input_lower for word in ["bye", "goodbye", "thanks", "thank you", "that's all"]):
            return self._get_random_response("goodbye")
        
        # Product/Service inquiries
        elif any(word in user_input_lower for word in ["product", "service", "what do you", "offerings", "solutions"]):
            return self._get_random_response("product_inquiry")
        
        # Support/Help requests
        elif any(word in user_input_lower for word in ["support", "help", "problem", "issue", "trouble", "error"]):
            return self._get_random_response("support")
        
        # Pricing inquiries
        elif any(word in user_input_lower for word in ["price", "cost", "pricing", "quote", "budget"]):
            return self._get_random_response("pricing")
        
        # Demo requests
        elif any(word in user_input_lower for word in ["demo", "demonstration", "show me", "trial"]):
            return self._get_random_response("demo")
        
        # Enterprise inquiries
        elif any(word in user_input_lower for word in ["enterprise", "large scale", "corporation", "business"]):
            return self._get_random_response("enterprise")
        
        # Integration questions
        elif any(word in user_input_lower for word in ["integration", "integrate", "api", "connect"]):
            return self._get_random_response("integration")
        
        # Company information requests
        elif any(phrase in user_input_lower for phrase in ["about your company", "company info", "info about", "tell me about", "what is techcorp", "who are you", "about techcorp"]):
            return self._get_random_response("company_info")
        
        # About requests
        elif any(word in user_input_lower for word in ["about", "company", "who", "what", "information", "info"]):
            return self._get_random_response("about")
        
        # Default response
        else:
            return self._get_random_response("default")
    
    def _get_random_response(self, category: str) -> str:
        """Get a random response from the specified category"""
        import random
        responses = self.responses.get(category, self.responses["default"])
        return random.choice(responses)

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
def enhanced_process_conversation(user_input: str, user_data: Dict[str, Any] = None, session_id: str = "default") -> Dict[str, Any]:
    """Enhanced process conversation with history tracking"""
    start_time = time.time()
    result = process_conversation(user_input, user_data)
    response_time = time.time() - start_time

    # Track conversation in history
    conversation_manager.add_conversation(
        user_input=user_input,
        bot_response=result['response'],
        session_id=session_id,
        user_data=user_data,
        lead_score=result['lead_score'],
        response_time=response_time
    )

    return result

mock_openai = MockOpenAI()
mock_sheets = MockGoogleSheets()
mock_slack = MockSlack()

# Import conversation history manager
from conversation_history import conversation_manager
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
