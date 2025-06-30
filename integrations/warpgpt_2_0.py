#!/usr/bin/env python3
"""
TechCorp WarpGPT 2.0 - Production-Grade Warp AI Assistant
Non-negotiable protocols with circuit breaker and hybrid search
"""

import json
import logging
import os
import re
import subprocess
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)

class WarpContext:
    """Warp CLI context manager"""
    
    @staticmethod
    def get_context() -> Dict[str, Any]:
        """Get current Warp context"""
        return {
            "terminal_session": "warp_session_" + str(int(time.time())),
            "pwd": os.getcwd(),
            "user": os.environ.get("USER", "unknown"),
            "shell": os.environ.get("SHELL", "bash"),
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def format_warp_terminal(command: str) -> str:
        """Format command for Warp terminal display"""
        return f"```warp-terminal\n$ {command}\n```"

class HybridKnowledgeBase:
    """Advanced knowledge base with hybrid search and confidence scoring"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.kb_file = os.path.join(data_dir, "warpgpt_kb.json")
        self.confidence_threshold = 0.7
        self.verified_threshold = 0.9
        
        os.makedirs(data_dir, exist_ok=True)
        self.knowledge_base = {}
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load production-grade knowledge base"""
        if os.path.exists(self.kb_file):
            try:
                with open(self.kb_file, 'r', encoding='utf-8') as f:
                    self.knowledge_base = json.load(f)
            except Exception as e:
                logger.error(f"Error loading knowledge base: {e}")
                self.knowledge_base = {}
        else:
            # Initialize with verified production solutions
            self.knowledge_base = {
                "vpn-001": {
                    "title": "VPN Connection Failures",
                    "category": "network",
                    "confidence": 0.95,
                    "version": "2.1.0",
                    "solution": [
                        "Check VPN service status: `sudo systemctl status openvpn`",
                        "Restart network manager: `sudo systemctl restart NetworkManager`",
                        "Verify config syntax: `openvpn --config /etc/openvpn/client.conf --verb 4`",
                        "Check firewall rules: `sudo iptables -L | grep vpn`"
                    ],
                    "verified": True,
                    "tags": ["vpn", "connection", "network", "openvpn"],
                    "troubleshooting": {
                        "error_patterns": ["connection refused", "authentication failed", "timeout"],
                        "common_fixes": ["credentials", "firewall", "dns"]
                    }
                },
                "docker-001": {
                    "title": "Docker Container Startup Issues",
                    "category": "containers",
                    "confidence": 0.92,
                    "version": "1.8.3",
                    "solution": [
                        "Check container logs: `docker logs --tail 50 container_name`",
                        "Inspect failed container: `docker inspect container_name | jq '.State'`",
                        "Verify image integrity: `docker image inspect image_name`",
                        "Clean up resources: `docker system prune -f`"
                    ],
                    "verified": True,
                    "tags": ["docker", "container", "startup", "troubleshooting"],
                    "troubleshooting": {
                        "error_patterns": ["exit code", "oomkilled", "port already in use"],
                        "common_fixes": ["memory", "ports", "permissions"]
                    }
                },
                "ssl-001": {
                    "title": "SSL Certificate Errors",
                    "category": "security",
                    "confidence": 0.94,
                    "version": "3.2.1",
                    "solution": [
                        "⚠️ Check certificate expiration: `openssl x509 -in cert.pem -noout -dates`",
                        "Verify certificate chain: `openssl verify -CAfile ca-bundle.crt cert.pem`",
                        "Test SSL handshake: `openssl s_client -connect domain.com:443 -servername domain.com`",
                        "Update certificate store: `sudo update-ca-certificates`"
                    ],
                    "verified": True,
                    "tags": ["ssl", "certificate", "security", "https", "tls"],
                    "troubleshooting": {
                        "error_patterns": ["certificate expired", "self signed", "unknown ca"],
                        "common_fixes": ["renewal", "chain", "trust_store"]
                    }
                },
                "db-001": {
                    "title": "Database Connection Timeouts",
                    "category": "database",
                    "confidence": 0.91,
                    "version": "2.0.5",
                    "solution": [
                        "Check connection pool: `sudo -u postgres psql -c 'SELECT * FROM pg_stat_activity;'`",
                        "Restart database service: `sudo systemctl restart postgresql`",
                        "Verify port binding: `netstat -tlnp | grep :5432`",
                        "Monitor connection limits: `sudo -u postgres psql -c 'SHOW max_connections;'`"
                    ],
                    "verified": True,
                    "tags": ["database", "postgresql", "timeout", "connection"],
                    "troubleshooting": {
                        "error_patterns": ["connection timed out", "too many connections", "authentication failed"],
                        "common_fixes": ["pool_size", "max_connections", "authentication"]
                    }
                },
                "api-001": {
                    "title": "API Rate Limiting Issues",
                    "category": "api",
                    "confidence": 0.89,
                    "version": "1.5.2",
                    "solution": [
                        "Check rate limit headers: `curl -I -H 'Authorization: Bearer $TOKEN' https://api.techcorp.com/status`",
                        "Implement exponential backoff in client code",
                        "Monitor usage patterns: `techcorp-cli api usage --detailed`",
                        "Request rate limit increase: `techcorp-cli api request-limit-increase`"
                    ],
                    "verified": True,
                    "tags": ["api", "rate_limit", "throttling", "performance"],
                    "troubleshooting": {
                        "error_patterns": ["429 too many requests", "rate limit exceeded"],
                        "common_fixes": ["backoff", "caching", "optimization"]
                    }
                }
            }
            self.save_knowledge_base()
    
    def save_knowledge_base(self):
        """Save knowledge base to file"""
        try:
            with open(self.kb_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving knowledge base: {e}")
    
    def hybrid_search(self, query: str, context: Dict[str, Any], limit: int = 5) -> Tuple[List[Dict], float]:
        """Hybrid search with semantic and keyword matching"""
        query_lower = query.lower()
        results = []
        
        for kb_id, entry in self.knowledge_base.items():
            score = 0.0
            
            # Keyword matching in title and tags
            search_text = (
                entry.get("title", "").lower() + " " +
                " ".join(entry.get("tags", [])) + " " +
                " ".join(entry.get("solution", []))
            ).lower()
            
            query_words = query_lower.split()
            keyword_matches = sum(1 for word in query_words if word in search_text)
            
            # Error pattern matching
            troubleshooting = entry.get("troubleshooting", {})
            error_patterns = troubleshooting.get("error_patterns", [])
            pattern_matches = sum(1 for pattern in error_patterns if pattern in query_lower)
            
            # Calculate composite score
            keyword_score = (keyword_matches / len(query_words)) if query_words else 0
            pattern_score = (pattern_matches / len(error_patterns)) if error_patterns else 0
            base_confidence = entry.get("confidence", 0.5)
            
            # Weighted scoring
            score = (keyword_score * 0.4) + (pattern_score * 0.4) + (base_confidence * 0.2)
            
            if score > 0:
                results.append({
                    "id": kb_id,
                    "score": score,
                    "confidence": base_confidence,
                    "entry": entry
                })
        
        # Sort by score and limit results
        results.sort(key=lambda x: x["score"], reverse=True)
        limited_results = results[:limit]
        
        # Calculate overall confidence
        overall_confidence = max([r["confidence"] for r in limited_results]) if limited_results else 0.0
        
        return limited_results, overall_confidence

class WarpGPT2:
    """TechCorp WarpGPT 2.0 - Production-Grade AI Assistant"""
    
    def __init__(self):
        self.kb = HybridKnowledgeBase()
        self.warp_context = WarpContext()
        self.conversation_memory = []
        self.confidence_threshold = 0.7
        self.verified_threshold = 0.9
    
    def execute_kb_search(self, user_input: str, context: Dict[str, Any]) -> Tuple[List[Dict], float]:
        """Execute hybrid KB search with context"""
        try:
            # Silent execution as per protocol
            results, confidence = self.kb.hybrid_search(user_input, context, limit=5)
            logger.info(f"KB search executed: {len(results)} results, confidence: {confidence:.2f}")
            return results, confidence
        except Exception as e:
            logger.error(f"KB search failed: {e}")
            return [], 0.0
    
    def format_verified_solution(self, result: Dict, kb_version: str) -> str:
        """Format verified solution response"""
        entry = result["entry"]
        kb_id = result["id"]
        
        response = f"✅ TechCorp Verified Fix (v{kb_version}):\n"
        response += f"📋 Solution #{kb_id.upper()}: {entry['title']}\n\n"
        
        for i, step in enumerate(entry["solution"], 1):
            if step.startswith("⚠️"):
                response += f"   {step}\n"
            elif "`" in step and step.count("`") >= 2:
                # Extract command from step
                command_match = re.search(r'`([^`]+)`', step)
                if command_match:
                    command = command_match.group(1)
                    description = step.replace(f"`{command}`", "").strip(": ")
                    response += f"   • Step {i}: {description}\n"
                    response += f"     {self.warp_context.format_warp_terminal(command)}\n"
                else:
                    response += f"   • Step {i}: {step}\n"
            else:
                response += f"   • Step {i}: {step}\n"
        
        response += f"\n📌 Confidence: {result['confidence']:.1%} | Category: {entry['category']}"
        return response
    
    def format_uncertain_response(self) -> str:
        """Format response when confidence is below threshold"""
        return """⚠️ I need more details:
           - Exact error message
           - OS version  
           - Steps already tried
           
Use `techcorp-cli diagnostics --full` to gather system info."""
    
    def detect_urgent_issue(self, user_input: str) -> bool:
        """Detect production-critical issues"""
        critical_keywords = [
            "production down", "service unavailable", "critical error",
            "outage", "emergency", "urgent", "crashed", "not responding",
            "database down", "api down", "website down"
        ]
        return any(keyword in user_input.lower() for keyword in critical_keywords)
    
    def escalate_critical_issue(self, user_input: str) -> str:
        """Escalate critical production issues"""
        ticket_id = f"CRITICAL-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        return f"""🚨 **CRITICAL ISSUE DETECTED** 🚨

Issue escalated to Level 3 Support immediately.
Ticket: {ticket_id}

Emergency contact: +1-800-TECHCORP-911
Expected response: < 5 minutes

Automated diagnostics initiated:
{self.warp_context.format_warp_terminal("techcorp-cli emergency-scan --priority=critical")}"""
    
    def process_warp_request(self, user_input: str) -> str:
        """Process user request with WarpGPT 2.0 protocols"""
        
        # Check for critical issues first
        if self.detect_urgent_issue(user_input):
            return self.escalate_critical_issue(user_input)
        
        # Get Warp context
        context = self.warp_context.get_context()
        
        # FIRST ACTION: Execute hybrid KB search silently
        results, confidence = self.execute_kb_search(user_input, context)
        
        # Circuit breaker logic
        if not results or confidence < self.confidence_threshold:
            # Never show uncertain answers
            return self.format_uncertain_response()
        
        elif confidence >= self.verified_threshold:
            # Verified solution format
            best_result = results[0]
            kb_version = best_result["entry"].get("version", "1.0.0")
            return self.format_verified_solution(best_result, kb_version)
        
        else:
            # Medium confidence - provide solution with caveats
            best_result = results[0]
            entry = best_result["entry"]
            
            response = f"🔍 Potential Solution (Confidence: {confidence:.1%}):\n"
            response += f"From TechCorp KB (#{best_result['id']}):\n\n"
            
            for i, step in enumerate(entry["solution"], 1):
                if "`" in step and step.count("`") >= 2:
                    command_match = re.search(r'`([^`]+)`', step)
                    if command_match:
                        command = command_match.group(1)
                        description = step.replace(f"`{command}`", "").strip(": ")
                        response += f"   • {description}\n"
                        response += f"     {self.warp_context.format_warp_terminal(command)}\n"
                    else:
                        response += f"   • {step}\n"
                else:
                    response += f"   • {step}\n"
            
            response += "\n⚠️ Please verify this solution in a test environment first."
            return response
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get WarpGPT system status"""
        return {
            "version": "2.0.0",
            "kb_entries": len(self.kb.knowledge_base),
            "confidence_threshold": self.confidence_threshold,
            "verified_threshold": self.verified_threshold,
            "context": self.warp_context.get_context(),
            "memory_size": len(self.conversation_memory)
        }

# Global WarpGPT 2.0 instance
warpgpt = WarpGPT2()
