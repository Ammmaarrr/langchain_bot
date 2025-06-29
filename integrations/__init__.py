"""
Integrations module for the TechCorp Customer Support & Lead Qualification Bot.

This module contains integrations with external services:
- Google Sheets API for CRM functionality
- Slack API for team notifications
"""

from .google_sheets_api import GoogleSheetsIntegration
from .slack_notifications import SlackNotifier

__all__ = ['GoogleSheetsIntegration', 'SlackNotifier']
