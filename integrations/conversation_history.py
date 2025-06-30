#!/usr/bin/env python3
"""
Conversation History Manager for learning and storing responses
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)

class ConversationHistoryManager:
    """Manages conversation history, learning, and response optimization"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.history_file = os.path.join(data_dir, "conversation_history.json")
        self.feedback_file = os.path.join(data_dir, "response_feedback.json")
        self.learning_patterns_file = os.path.join(data_dir, "learning_patterns.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        self.conversation_history = []
        self.feedback_data = []
        self.learning_patterns = {}
        
        self.load_data()
    
    def load_data(self):
        """Load existing conversation history and learning data"""
        try:
            # Load conversation history
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.conversation_history = json.load(f)
            
            # Load feedback data
            if os.path.exists(self.feedback_file):
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    self.feedback_data = json.load(f)
            
            # Load learning patterns
            if os.path.exists(self.learning_patterns_file):
                with open(self.learning_patterns_file, 'r', encoding='utf-8') as f:
                    self.learning_patterns = json.load(f)
            
            logger.info(f"Loaded {len(self.conversation_history)} conversation records")
            
        except Exception as e:
            logger.error(f"Error loading conversation data: {e}")
            self.conversation_history = []
            self.feedback_data = []
            self.learning_patterns = {}
    
    def save_data(self):
        """Save conversation history and learning data"""
        try:
            # Save conversation history
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            
            # Save feedback data
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(self.feedback_data, f, indent=2, ensure_ascii=False)
            
            # Save learning patterns
            with open(self.learning_patterns_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_patterns, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error saving conversation data: {e}")
    
    def add_conversation(self, user_input: str, bot_response: str, 
                        session_id: str = "default", user_data: Dict = None,
                        lead_score: int = 0, response_time: float = 0.0) -> str:
        """Add a new conversation to history"""
        conversation_id = f"{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        conversation_entry = {
            "conversation_id": conversation_id,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "bot_response": bot_response,
            "user_data": user_data or {},
            "lead_score": lead_score,
            "response_time": response_time,
            "feedback": None,
            "response_quality": None
        }
        
        self.conversation_history.append(conversation_entry)
        self.save_data()
        
        # Update learning patterns
        self._update_learning_patterns(user_input, bot_response)
        
        logger.info(f"Added conversation {conversation_id}")
        return conversation_id
    
    def add_feedback(self, conversation_id: str, feedback: str, 
                    quality_rating: int, suggested_response: str = None):
        """Add feedback for a specific conversation"""
        feedback_entry = {
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat(),
            "feedback": feedback,
            "quality_rating": quality_rating,  # 1-5 scale
            "suggested_response": suggested_response
        }
        
        self.feedback_data.append(feedback_entry)
        
        # Update the conversation record
        for conv in self.conversation_history:
            if conv["conversation_id"] == conversation_id:
                conv["feedback"] = feedback
                conv["response_quality"] = quality_rating
                break
        
        self.save_data()
        self._learn_from_feedback(conversation_id, feedback_entry)
        logger.info(f"Added feedback for conversation {conversation_id}")
    
    def get_recent_conversations(self, limit: int = 20, session_id: str = None) -> List[Dict]:
        """Get the most recent conversations"""
        conversations = self.conversation_history
        
        if session_id:
            conversations = [c for c in conversations if c["session_id"] == session_id]
        
        # Sort by timestamp descending and limit
        conversations.sort(key=lambda x: x["timestamp"], reverse=True)
        return conversations[:limit]
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get statistics about conversations"""
        total_conversations = len(self.conversation_history)
        
        if total_conversations == 0:
            return {"total_conversations": 0}
        
        # Calculate average response quality
        rated_conversations = [c for c in self.conversation_history if c.get("response_quality")]
        avg_quality = sum(c["response_quality"] for c in rated_conversations) / len(rated_conversations) if rated_conversations else 0
        
        # Count feedback
        feedback_count = len(self.feedback_data)
        
        # Recent activity (last 24 hours)
        from datetime import datetime, timedelta
        yesterday = datetime.now() - timedelta(days=1)
        recent_conversations = [
            c for c in self.conversation_history 
            if datetime.fromisoformat(c["timestamp"]) > yesterday
        ]
        
        return {
            "total_conversations": total_conversations,
            "feedback_count": feedback_count,
            "average_quality": round(avg_quality, 2),
            "recent_24h": len(recent_conversations),
            "learning_patterns_count": len(self.learning_patterns)
        }
    
    def _update_learning_patterns(self, user_input: str, bot_response: str):
        """Update learning patterns based on conversations"""
        user_input_lower = user_input.lower()
        
        # Extract keywords from user input
        import re
        keywords = re.findall(r'\b\w+\b', user_input_lower)
        keywords = [k for k in keywords if len(k) > 2]  # Filter short words
        
        for keyword in keywords:
            if keyword not in self.learning_patterns:
                self.learning_patterns[keyword] = {
                    "count": 0,
                    "responses": [],
                    "success_rate": 0.0
                }
            
            self.learning_patterns[keyword]["count"] += 1
            
            # Store successful responses (limit to prevent memory issues)
            if len(self.learning_patterns[keyword]["responses"]) < 10:
                self.learning_patterns[keyword]["responses"].append({
                    "response": bot_response,
                    "timestamp": datetime.now().isoformat()
                })
    
    def _learn_from_feedback(self, conversation_id: str, feedback_entry: Dict):
        """Learn from user feedback to improve responses"""
        quality_rating = feedback_entry["quality_rating"]
        
        # Find the original conversation
        conversation = None
        for conv in self.conversation_history:
            if conv["conversation_id"] == conversation_id:
                conversation = conv
                break
        
        if not conversation:
            return
        
        user_input = conversation["user_input"].lower()
        keywords = re.findall(r'\b\w+\b', user_input)
        
        # Update success rates for keywords based on feedback
        for keyword in keywords:
            if keyword in self.learning_patterns:
                pattern = self.learning_patterns[keyword]
                
                # Simple learning: adjust success rate based on feedback
                current_rate = pattern.get("success_rate", 0.0)
                feedback_weight = 0.1  # How much new feedback affects the rate
                
                if quality_rating >= 4:  # Good feedback
                    new_rate = current_rate + (1.0 - current_rate) * feedback_weight
                elif quality_rating <= 2:  # Poor feedback
                    new_rate = current_rate * (1.0 - feedback_weight)
                else:  # Neutral feedback
                    new_rate = current_rate
                
                pattern["success_rate"] = max(0.0, min(1.0, new_rate))
    
    def suggest_improved_response(self, user_input: str) -> Optional[str]:
        """Suggest an improved response based on learning patterns"""
        user_input_lower = user_input.lower()
        keywords = re.findall(r'\b\w+\b', user_input_lower)
        
        best_responses = []
        
        for keyword in keywords:
            if keyword in self.learning_patterns:
                pattern = self.learning_patterns[keyword]
                if pattern["success_rate"] > 0.7 and pattern["responses"]:
                    # Get the most recent successful response
                    best_responses.extend(pattern["responses"])
        
        if best_responses:
            # Return the most recent high-quality response
            best_responses.sort(key=lambda x: x["timestamp"], reverse=True)
            return best_responses[0]["response"]
        
        return None
    
    def export_learning_data(self) -> Dict[str, Any]:
        """Export learning data for analysis"""
        return {
            "conversation_history": self.conversation_history,
            "feedback_data": self.feedback_data,
            "learning_patterns": self.learning_patterns,
            "stats": self.get_conversation_stats()
        }

# Global instance
conversation_manager = ConversationHistoryManager()
