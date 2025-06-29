"""
Slack Integration for Customer Support & Lead Qualification Bot
Sends real-time notifications for high-priority leads and urgent issues.
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, Optional
import aiohttp
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SlackNotifier:
    """
    Slack integration for real-time notifications and team collaboration.
    """
    
    def __init__(self, bot_token: str, webhook_url: Optional[str] = None):
        """
        Initialize Slack notifier.
        
        Args:
            bot_token: Slack bot token
            webhook_url: Optional webhook URL for simple notifications
        """
        self.bot_token = bot_token
        self.webhook_url = webhook_url
        self.client = WebClient(token=bot_token) if bot_token else None
    
    async def notify_high_priority_lead(self, lead_data: Dict) -> bool:
        """
        Send notification for high-priority qualified leads.
        
        Args:
            lead_data: Dictionary containing lead information
            
        Returns:
            bool: Success status
        """
        try:
            # Prepare rich notification
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🔥 High-Priority Lead Alert!"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Customer:* {lead_data.get('customer_name', 'Unknown')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Company:* {lead_data.get('company', 'Not specified')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Lead Score:* {lead_data.get('lead_score', 0)}/100"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Budget:* {lead_data.get('budget_range', 'Not specified')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Timeline:* {lead_data.get('timeline', 'Not specified')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Email:* {lead_data.get('email', 'Not provided')}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Specific Needs:*\n{lead_data.get('specific_needs', 'Not specified')}"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Assign to Me"
                            },
                            "style": "primary",
                            "value": f"assign_lead_{lead_data.get('customer_id', '')}"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Schedule Demo"
                            },
                            "value": f"schedule_demo_{lead_data.get('customer_id', '')}"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "View in CRM"
                            },
                            "url": "https://docs.google.com/spreadsheets/your-sheet-id"
                        }
                    ]
                }
            ]
            
            # Send to sales channel
            result = self.client.chat_postMessage(
                channel="#sales-alerts",
                text=f"High-priority lead: {lead_data.get('customer_name', 'Unknown')}",
                blocks=blocks
            )
            
            logger.info(f"High-priority lead notification sent: {result['ts']}")
            return True
            
        except SlackApiError as e:
            logger.error(f"Failed to send Slack notification: {e.response['error']}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending notification: {e}")
            return False
    
    async def notify_technical_escalation(self, ticket_data: Dict) -> bool:
        """
        Send notification for technical support escalations.
        
        Args:
            ticket_data: Dictionary containing ticket information
            
        Returns:
            bool: Success status
        """
        try:
            severity_colors = {
                "CRITICAL": "#FF0000",
                "HIGH": "#FF8C00",
                "MEDIUM": "#FFD700",
                "LOW": "#90EE90"
            }
            
            severity = ticket_data.get('issue_severity', 'MEDIUM')
            color = severity_colors.get(severity, "#FFD700")
            
            attachments = [{
                "color": color,
                "title": f"🚨 Technical Support Escalation - {severity} Priority",
                "fields": [
                    {
                        "title": "Customer",
                        "value": ticket_data.get('customer_name', 'Unknown'),
                        "short": True
                    },
                    {
                        "title": "Issue Type",
                        "value": ticket_data.get('issue_type', 'Technical Problem'),
                        "short": True
                    },
                    {
                        "title": "Ticket ID",
                        "value": ticket_data.get('ticket_id', 'Not assigned'),
                        "short": True
                    },
                    {
                        "title": "Severity",
                        "value": severity,
                        "short": True
                    },
                    {
                        "title": "Description",
                        "value": ticket_data.get('issue_description', 'No description provided'),
                        "short": False
                    }
                ],
                "footer": "TechCorp Support Bot",
                "ts": int(datetime.now().timestamp())
            }]
            
            result = self.client.chat_postMessage(
                channel="#technical-support",
                text=f"Technical escalation: {ticket_data.get('customer_name', 'Unknown')}",
                attachments=attachments
            )
            
            logger.info(f"Technical escalation notification sent: {result['ts']}")
            return True
            
        except SlackApiError as e:
            logger.error(f"Failed to send technical notification: {e.response['error']}")
            return False
    
    async def notify_daily_summary(self, analytics_data: Dict) -> bool:
        """
        Send daily analytics summary to management.
        
        Args:
            analytics_data: Dictionary containing daily metrics
            
        Returns:
            bool: Success status
        """
        try:
            # Create visual summary
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "📊 Daily Chatbot Performance Summary"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Date:* {datetime.now().strftime('%B %d, %Y')}"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*💬 Total Conversations:*\n{analytics_data.get('total_conversations', 0)}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*🎯 Leads Generated:*\n{analytics_data.get('leads_generated', 0)}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*🔧 Technical Tickets:*\n{analytics_data.get('technical_tickets', 0)}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*⚡ Avg Response Time:*\n{analytics_data.get('avg_response_time', 0)}s"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*😊 Customer Satisfaction:*\n{analytics_data.get('customer_satisfaction', 0)}/5.0"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*✅ Resolution Rate:*\n{analytics_data.get('resolution_rate', 0)*100:.1f}%"
                        }
                    ]
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "📈 View detailed analytics in the CRM dashboard"
                        }
                    ]
                }
            ]
            
            result = self.client.chat_postMessage(
                channel="#management-reports",
                text="Daily chatbot performance summary",
                blocks=blocks
            )
            
            logger.info(f"Daily summary sent: {result['ts']}")
            return True
            
        except SlackApiError as e:
            logger.error(f"Failed to send daily summary: {e.response['error']}")
            return False
    
    async def notify_webhook(self, message: str, data: Dict) -> bool:
        """
        Send simple webhook notification.
        
        Args:
            message: Notification message
            data: Additional data to include
            
        Returns:
            bool: Success status
        """
        if not self.webhook_url:
            logger.warning("No webhook URL configured")
            return False
        
        try:
            payload = {
                "text": message,
                "username": "TechCorp Support Bot",
                "icon_emoji": ":robot_face:",
                "attachments": [{
                    "color": "good",
                    "fields": [
                        {
                            "title": key.replace('_', ' ').title(),
                            "value": str(value),
                            "short": True
                        } for key, value in data.items()
                    ]
                }]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 200:
                        logger.info("Webhook notification sent successfully")
                        return True
                    else:
                        logger.error(f"Webhook failed with status: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Failed to send webhook notification: {e}")
            return False


# Utility functions for easy integration
async def send_lead_alert(lead_data: Dict) -> bool:
    """Quick function to send lead alert."""
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    if not bot_token:
        logger.warning("No Slack bot token configured")
        return False
    
    notifier = SlackNotifier(bot_token)
    return await notifier.notify_high_priority_lead(lead_data)

async def send_tech_alert(ticket_data: Dict) -> bool:
    """Quick function to send technical alert."""
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    if not bot_token:
        logger.warning("No Slack bot token configured")
        return False
    
    notifier = SlackNotifier(bot_token)
    return await notifier.notify_technical_escalation(ticket_data)


# Example usage and testing
if __name__ == "__main__":
    async def test_notifications():
        bot_token = os.getenv('SLACK_BOT_TOKEN')
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        
        if not bot_token:
            logger.error("Missing SLACK_BOT_TOKEN environment variable")
            return
        
        notifier = SlackNotifier(bot_token, webhook_url)
        
        # Test high-priority lead notification
        lead_data = {
            'customer_id': 'CUST001',
            'customer_name': 'Sarah Johnson',
            'company': 'Innovation Labs Inc',
            'email': 'sarah.johnson@innovationlabs.com',
            'company_size': '100-500',
            'budget_range': '$50,000-$100,000',
            'timeline': '2-3 months',
            'specific_needs': 'Complete CRM overhaul with custom integrations',
            'lead_score': 92,
            'priority': 'High'
        }
        
        await notifier.notify_high_priority_lead(lead_data)
        
        # Test technical escalation
        ticket_data = {
            'customer_name': 'Michael Chen',
            'issue_type': 'API Integration',
            'issue_severity': 'HIGH',
            'ticket_id': 'TECH-2025-001',
            'issue_description': 'Customer unable to sync data between CRM and marketing automation platform. Urgent fix needed for campaign launch.'
        }
        
        await notifier.notify_technical_escalation(ticket_data)
        
        # Test daily summary
        analytics_data = {
            'total_conversations': 127,
            'leads_generated': 18,
            'technical_tickets': 3,
            'avg_response_time': 2.1,
            'customer_satisfaction': 4.6,
            'resolution_rate': 0.89
        }
        
        await notifier.notify_daily_summary(analytics_data)
    
    # Run tests
    asyncio.run(test_notifications())
