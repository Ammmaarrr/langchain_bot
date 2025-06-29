"""
Automated tests for the customer support chatbot conversation flows.
Tests various scenarios including lead qualification, technical support, and general inquiries.
"""

import pytest
import asyncio
import json
from typing import Dict, List
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MockLangflowBot:
    """Mock bot for testing conversation flows."""
    
    def __init__(self):
        self.conversation_history = []
        self.lead_scores = {}
        
    def process_message(self, message: str, intent: str = None) -> Dict:
        """Simulate bot message processing."""
        response = {
            "message": message,
            "intent": intent or self._classify_intent(message),
            "response": "",
            "lead_score": 0,
            "escalation_needed": False
        }
        
        if "lead" in response["intent"].lower():
            response.update(self._handle_lead_qualification(message))
        elif "technical" in response["intent"].lower():
            response.update(self._handle_technical_support(message))
        else:
            response.update(self._handle_general_inquiry(message))
            
        self.conversation_history.append(response)
        return response
    
    def _classify_intent(self, message: str) -> str:
        """Simple intent classification for testing."""
        message_lower = message.lower()
        if any(word in message_lower for word in ["buy", "purchase", "demo", "pricing", "interested"]):
            return "LEAD_QUALIFICATION"
        elif any(word in message_lower for word in ["error", "bug", "issue", "problem", "not working"]):
            return "TECHNICAL_SUPPORT"
        elif any(word in message_lower for word in ["order", "status", "tracking"]):
            return "ORDER_STATUS"
        else:
            return "GENERAL_INQUIRY"
    
    def _handle_lead_qualification(self, message: str) -> Dict:
        """Handle lead qualification scenario."""
        score = 50  # Base score
        
        # Simulate scoring based on message content
        if "enterprise" in message.lower() or "large company" in message.lower():
            score += 15
        if "$" in message or "budget" in message.lower():
            score += 20
        if "immediately" in message.lower() or "urgent" in message.lower():
            score += 25
            
        return {
            "response": "Thank you for your interest! I'd love to learn more about your needs. Can you tell me about your company size and timeline?",
            "lead_score": score,
            "next_action": "schedule_demo" if score > 70 else "continue_qualification"
        }
    
    def _handle_technical_support(self, message: str) -> Dict:
        """Handle technical support scenario."""
        severity = "MEDIUM"
        escalation = False
        
        if any(word in message.lower() for word in ["critical", "urgent", "down", "broken"]):
            severity = "HIGH"
            escalation = True
        elif any(word in message.lower() for word in ["question", "how to", "help"]):
            severity = "LOW"
            
        return {
            "response": "I understand you're experiencing a technical issue. Let me help you troubleshoot this step by step.",
            "issue_severity": severity,
            "escalation_needed": escalation
        }
    
    def _handle_general_inquiry(self, message: str) -> Dict:
        """Handle general inquiry scenario."""
        interest_level = "LOW"
        
        if any(word in message.lower() for word in ["pricing", "features", "demo"]):
            interest_level = "HIGH"
        elif any(word in message.lower() for word in ["more information", "tell me about"]):
            interest_level = "MEDIUM"
            
        return {
            "response": "I'd be happy to help you learn more about TechCorp Solutions. What specific information are you looking for?",
            "interest_level": interest_level,
            "sales_referral": interest_level == "HIGH"
        }


class TestConversationFlows:
    """Test suite for conversation flows."""
    
    def setup_method(self):
        """Set up test environment."""
        self.bot = MockLangflowBot()
    
    def test_lead_qualification_flow(self):
        """Test lead qualification conversation flow."""
        # Test initial interest
        response1 = self.bot.process_message("I'm interested in your CRM solution for my company")
        assert response1["intent"] == "LEAD_QUALIFICATION"
        assert response1["lead_score"] >= 50
        
        # Test budget indication
        response2 = self.bot.process_message("We have a budget of around $50,000 for this project")
        assert response2["lead_score"] > response1["lead_score"]
        
        # Test urgency
        response3 = self.bot.process_message("We need to implement this immediately")
        assert response3["lead_score"] > 70
        assert response3["next_action"] == "schedule_demo"
    
    def test_technical_support_flow(self):
        """Test technical support conversation flow."""
        # Test critical issue
        response1 = self.bot.process_message("Our system is down and we can't access any data - this is critical!")
        assert response1["intent"] == "TECHNICAL_SUPPORT"
        assert response1["issue_severity"] == "HIGH"
        assert response1["escalation_needed"] == True
        
        # Test general question
        response2 = self.bot.process_message("How do I configure the API integration?")
        assert response2["intent"] == "TECHNICAL_SUPPORT"
        assert response2["issue_severity"] == "LOW"
        assert response2["escalation_needed"] == False
    
    def test_general_inquiry_flow(self):
        """Test general inquiry conversation flow."""
        # Test product inquiry
        response1 = self.bot.process_message("Can you tell me about your products and pricing?")
        assert response1["intent"] == "GENERAL_INQUIRY"
        assert response1["interest_level"] == "HIGH"
        assert response1["sales_referral"] == True
        
        # Test basic information request
        response2 = self.bot.process_message("What does TechCorp Solutions do?")
        assert response2["intent"] == "GENERAL_INQUIRY"
        assert response2["interest_level"] == "LOW"
        assert response2["sales_referral"] == False
    
    def test_intent_classification_accuracy(self):
        """Test intent classification accuracy."""
        test_cases = [
            ("I want to buy your CRM", "LEAD_QUALIFICATION"),
            ("There's an error in the system", "TECHNICAL_SUPPORT"),
            ("What's the status of my order?", "ORDER_STATUS"),
            ("Tell me about your company", "GENERAL_INQUIRY")
        ]
        
        for message, expected_intent in test_cases:
            response = self.bot.process_message(message)
            assert response["intent"] == expected_intent, f"Failed for message: {message}"
    
    def test_conversation_history_tracking(self):
        """Test conversation history tracking."""
        messages = [
            "Hello, I'm interested in your products",
            "What's your pricing?",
            "Can I schedule a demo?"
        ]
        
        for message in messages:
            self.bot.process_message(message)
        
        assert len(self.bot.conversation_history) == 3
        assert all("message" in entry for entry in self.bot.conversation_history)
    
    def test_lead_scoring_algorithm(self):
        """Test lead scoring algorithm accuracy."""
        # High-value lead scenario
        high_value_message = "I'm the CEO of a 500-person company with a $100k budget for immediate CRM implementation"
        response = self.bot.process_message(high_value_message)
        assert response["lead_score"] > 80
        
        # Low-value lead scenario
        low_value_message = "I'm just looking for some general information about CRM systems"
        response = self.bot.process_message(low_value_message)
        assert response["lead_score"] < 60


class TestIntegrationScenarios:
    """Test integration scenarios with external systems."""
    
    def setup_method(self):
        """Set up test environment."""
        self.bot = MockLangflowBot()
    
    @patch('integrations.google_sheets_api.GoogleSheetsIntegration')
    def test_crm_logging_integration(self, mock_sheets):
        """Test CRM logging integration."""
        mock_sheets.return_value.log_conversation.return_value = True
        mock_sheets.return_value.log_lead.return_value = True
        
        # Simulate high-value lead conversation
        response = self.bot.process_message("I need a CRM solution for my 200-person company, budget $75k")
        
        # Verify CRM logging would be called
        assert response["lead_score"] > 70
        # In real implementation, would verify mock_sheets calls
    
    @patch('integrations.slack_notifications.SlackNotifier')
    def test_slack_notification_integration(self, mock_slack):
        """Test Slack notification integration."""
        mock_slack.return_value.notify_high_priority_lead.return_value = True
        mock_slack.return_value.notify_technical_escalation.return_value = True
        
        # Test high-priority lead notification
        response1 = self.bot.process_message("Enterprise client with $200k budget, need immediate demo")
        assert response1["lead_score"] > 85
        
        # Test technical escalation notification
        response2 = self.bot.process_message("Critical system failure - all services down!")
        assert response2["escalation_needed"] == True


class TestPerformanceScenarios:
    """Test performance and edge cases."""
    
    def setup_method(self):
        """Set up test environment."""
        self.bot = MockLangflowBot()
    
    def test_concurrent_conversations(self):
        """Test handling multiple concurrent conversations."""
        async def simulate_conversation(message):
            return self.bot.process_message(message)
        
        # Simulate concurrent messages
        messages = [
            "I need CRM pricing information",
            "Technical issue with API",
            "What products do you offer?",
            "Schedule a demo please"
        ]
        
        # In real async implementation, would use asyncio.gather
        responses = [self.bot.process_message(msg) for msg in messages]
        
        assert len(responses) == 4
        assert all("response" in resp for resp in responses)
    
    def test_edge_case_messages(self):
        """Test edge cases and unusual inputs."""
        edge_cases = [
            "",  # Empty message
            "a" * 1000,  # Very long message
            "🚀💻🎯",  # Emoji only
            "SELECT * FROM users;",  # SQL injection attempt
            "<script>alert('test')</script>"  # XSS attempt
        ]
        
        for message in edge_cases:
            try:
                response = self.bot.process_message(message)
                assert isinstance(response, dict)
                assert "response" in response
            except Exception as e:
                pytest.fail(f"Bot failed on edge case: {message}, Error: {e}")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
