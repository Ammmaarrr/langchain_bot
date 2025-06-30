#!/usr/bin/env python3
"""
TechCorp Warp AI Assistant
Technical support AI with knowledge base access and solution logging
"""

import json
import logging
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class TechCorpKnowledgeBase:
    """TechCorp internal knowledge base"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.kb_file = os.path.join(data_dir, "techcorp_kb.json")
        self.solutions_log = os.path.join(data_dir, "solutions_log.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        self.knowledge_base = {}
        self.solutions = []
        
        self.load_knowledge_base()
        self.load_solutions_log()
    
    def load_knowledge_base(self):
        """Load TechCorp knowledge base"""
        if os.path.exists(self.kb_file):
            try:
                with open(self.kb_file, 'r', encoding='utf-8') as f:
                    self.knowledge_base = json.load(f)
            except Exception as e:
                logger.error(f"Error loading knowledge base: {e}")
                self.knowledge_base = {}
        else:
            # Initialize with sample knowledge base
            self.knowledge_base = {
                "vpn-22": {
                    "title": "VPN Connection Issues",
                    "category": "network",
                    "solution": [
                        "First try: `sudo service vpn restart`",
                        "Check firewall: `tcping your.vpn.server 443`",
                        "Verify credentials in `/etc/vpn/config`",
                        "Check DNS resolution: `nslookup your.vpn.server`"
                    ],
                    "tags": ["vpn", "connection", "network", "troubleshooting"]
                },
                "db-15": {
                    "title": "Database Connection Timeout",
                    "category": "database",
                    "solution": [
                        "Check connection pool: `ps aux | grep postgres`",
                        "Restart database service: `sudo systemctl restart postgresql`",
                        "Verify port availability: `netstat -tlnp | grep 5432`",
                        "Check logs: `tail -f /var/log/postgresql/postgresql.log`"
                    ],
                    "tags": ["database", "timeout", "postgresql", "connection"]
                },
                "ssl-08": {
                    "title": "SSL Certificate Errors",
                    "category": "security",
                    "solution": [
                        "⚠️ Check certificate expiry: `openssl x509 -in cert.pem -noout -dates`",
                        "Verify certificate chain: `openssl verify -CAfile ca.pem cert.pem`",
                        "Test SSL connection: `openssl s_client -connect domain.com:443`",
                        "Update certificate store: `sudo update-ca-certificates`"
                    ],
                    "tags": ["ssl", "certificate", "security", "https"]
                },
                "docker-03": {
                    "title": "Docker Container Won't Start",
                    "category": "containers",
                    "solution": [
                        "Check container logs: `docker logs container_name`",
                        "Inspect container config: `docker inspect container_name`",
                        "Check available resources: `docker system df`",
                        "Restart Docker daemon: `sudo systemctl restart docker`"
                    ],
                    "tags": ["docker", "container", "startup", "troubleshooting"]
                },
                "api-11": {
                    "title": "API Rate Limiting Issues",
                    "category": "api",
                    "solution": [
                        "Check current rate limits: `curl -I https://api.techcorp.com/status`",
                        "Implement exponential backoff in client code",
                        "Use API key rotation: Multiple keys for high-volume apps",
                        "Monitor usage: `curl -H 'Authorization: Bearer TOKEN' /api/usage`"
                    ],
                    "tags": ["api", "rate limit", "throttling", "performance"]
                }
            }
            self.save_knowledge_base()
    
    def load_solutions_log(self):
        """Load solutions log"""
        if os.path.exists(self.solutions_log):
            try:
                with open(self.solutions_log, 'r', encoding='utf-8') as f:
                    self.solutions = json.load(f)
            except Exception as e:
                logger.error(f"Error loading solutions log: {e}")
                self.solutions = []
        else:
            self.solutions = []
    
    def save_knowledge_base(self):
        """Save knowledge base to file"""
        try:
            with open(self.kb_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving knowledge base: {e}")
    
    def save_solutions_log(self):
        """Save solutions log to file"""
        try:
            with open(self.solutions_log, 'w', encoding='utf-8') as f:
                json.dump(self.solutions, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving solutions log: {e}")
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search knowledge base for relevant solutions"""
        query_lower = query.lower()
        results = []
        
        for kb_id, entry in self.knowledge_base.items():
            # Search in title, tags, and solution steps
            search_text = (
                entry.get("title", "").lower() + " " +
                " ".join(entry.get("tags", [])) + " " +
                " ".join(entry.get("solution", []))
            )
            
            # Calculate relevance score
            score = 0
            query_words = query_lower.split()
            
            for word in query_words:
                if word in search_text:
                    score += 1
            
            if score > 0:
                results.append({
                    "id": kb_id,
                    "score": score,
                    "entry": entry
                })
        
        # Sort by relevance score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:3]  # Return top 3 results
    
    def log_solution(self, problem: str, solution: str, category: str = "general") -> str:
        """Log a new solution to the knowledge base"""
        solution_id = f"sol-{len(self.solutions) + 1:03d}"
        
        new_solution = {
            "id": solution_id,
            "timestamp": datetime.now().isoformat(),
            "problem": problem,
            "solution": solution,
            "category": category,
            "status": "pending_review"
        }
        
        self.solutions.append(new_solution)
        self.save_solutions_log()
        
        logger.info(f"Logged new solution: {solution_id}")
        return solution_id

class TechCorpWarpAI:
    """TechCorp Warp AI Assistant"""
    
    def __init__(self):
        self.kb = TechCorpKnowledgeBase()
        self.conversation_memory = []  # Last 3 messages
        self.session_data = {}
    
    def add_to_memory(self, user_message: str, ai_response: str):
        """Add conversation to memory (keep last 3)"""
        self.conversation_memory.append({
            "user": user_message,
            "ai": ai_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 3 messages
        if len(self.conversation_memory) > 3:
            self.conversation_memory = self.conversation_memory[-3:]
    
    def get_greeting(self, product: str = "system") -> str:
        """Generate greeting message"""
        return f"How can I assist with your TechCorp {product} today?"
    
    def execute_kb_command(self, query: str) -> Dict[str, Any]:
        """Execute /kb search command"""
        results = self.kb.search(query)
        return {
            "command": f"/kb search: {query}",
            "results": results,
            "found": len(results) > 0
        }
    
    def execute_log_command(self, problem: str, solution: str, category: str = "general") -> str:
        """Execute /log command to record new solution"""
        solution_id = self.kb.log_solution(problem, solution, category)
        return f"✅ Logged solution {solution_id} for review"
    
    def format_kb_results(self, results: List[Dict[str, Any]]) -> str:
        """Format knowledge base search results"""
        if not results:
            return "No solutions found in TechCorp KB."
        
        response = ""
        for result in results:
            entry = result["entry"]
            kb_id = result["id"]
            
            response += f"From TechCorp KB (#{kb_id}):\n"
            for step in entry["solution"]:
                response += f"   • {step}\n"
            response += "\n"
        
        return response.strip()
    
    def detect_urgency(self, user_input: str) -> bool:
        """Detect if issue is urgent"""
        urgent_keywords = [
            "down", "crashed", "emergency", "critical", "urgent", 
            "production", "outage", "can't access", "not working",
            "broken", "failed", "error", "timeout"
        ]
        
        return any(keyword in user_input.lower() for keyword in urgent_keywords)
    
    def ask_clarifying_question(self, intent: str) -> str:
        """Ask one clarifying question before escalating"""
        clarifying_questions = {
            "vpn": "What error message are you seeing when trying to connect?",
            "database": "Which database system are you using (PostgreSQL, MySQL, MongoDB)?",
            "docker": "What happens when you try to start the container?",
            "api": "What's the exact error response you're receiving?",
            "ssl": "Are you seeing this error in a browser or command line tool?",
            "network": "Are other network services working normally?",
            "default": "Can you provide more details about the specific error or behavior you're experiencing?"
        }
        
        # Try to match intent with question categories
        for category, question in clarifying_questions.items():
            if category in intent.lower():
                return question
        
        return clarifying_questions["default"]
    
    def escalate_to_human(self, issue: str) -> str:
        """Escalate to human support"""
        if self.detect_urgency(issue):
            return "⚠️ **URGENT ISSUE DETECTED**\n\nI'm escalating this to our Level 2 support team immediately. You should receive a response within 15 minutes.\n\nTicket created: #URGENT-" + datetime.now().strftime("%Y%m%d-%H%M%S")
        else:
            return "I'll escalate this to our technical support team. They'll review your case and respond within 2-4 hours.\n\nTicket created: #SUP-" + datetime.now().strftime("%Y%m%d-%H%M%S")
    
    def process_message(self, user_input: str, product: str = "system") -> str:
        """Process user message and generate response"""
        # Check if this is the first message (greeting)
        if not self.conversation_memory:
            greeting = self.get_greeting(product)
            if not user_input.strip():
                return greeting
        
        # Check for urgent issues first
        is_urgent = self.detect_urgency(user_input)
        
        # Execute knowledge base search
        kb_result = self.execute_kb_command(user_input)
        
        response = ""
        
        # If we found results in KB
        if kb_result["found"]:
            response = self.format_kb_results(kb_result["results"])
            
            # Add urgency warning if needed
            if is_urgent:
                response = "⚠️ **URGENT ISSUE DETECTED**\n\n" + response
            
            response += "\n\nNeed more details or still having issues?"
        
        else:
            # No KB results - ask clarifying question before escalating
            if len([msg for msg in self.conversation_memory if "clarifying" not in msg.get("ai", "")]) < 2:
                clarifying_q = self.ask_clarifying_question(user_input)
                response = f"I don't see this exact issue in our knowledge base.\n\n{clarifying_q}"
                response += "\n\n*This will help me find the right solution or escalate appropriately.*"
            else:
                # Already asked clarifying questions - escalate
                response = self.escalate_to_human(user_input)
        
        # Add to conversation memory
        self.add_to_memory(user_input, response)
        
        return response
    
    def get_conversation_context(self) -> str:
        """Get conversation context for debugging"""
        if not self.conversation_memory:
            return "No conversation history"
        
        context = "Recent conversation:\n"
        for i, msg in enumerate(self.conversation_memory[-3:], 1):
            context += f"{i}. User: {msg['user'][:50]}...\n"
            context += f"   AI: {msg['ai'][:50]}...\n"
        
        return context

# Global instance
techcorp_ai = TechCorpWarpAI()
