"""
Integration tests for API components of the chatbot solution.
"""

import asyncio
import os
import pytest
from unittest.mock import patch, MagicMock, Mock
from integrations.google_sheets_api import GoogleSheetsIntegration
from integrations.slack_notifications import SlackNotifier

# Ensure test data is loaded properly
@pytest.fixture(scope="module")
@patch('google.oauth2.service_account.Credentials.from_service_account_file')
@patch('googleapiclient.discovery.build')
def google_sheets_integration(mock_build, mock_creds):
    """Set up Google Sheets integration for testing."""
    credentials_file = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE', 'test-credentials.json')
    spreadsheet_id = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID', 'test-spreadsheet-id')

    # Mock the credentials with proper attributes and method chains
    mock_credentials = Mock()
    mock_credentials.universe_domain = 'googleapis.com'
    mock_credentials.create_scoped.return_value = mock_credentials
    mock_credentials.authorize.return_value = mock_credentials
    mock_credentials.credentials = mock_credentials
    mock_creds.return_value = mock_credentials
    
    # Mock the API Client creation
    mock_build.return_value.spreadsheets.return_value.values.return_value.append.return_value.execute.return_value = {
        'updates': {'updatedCells': 1}
    }

    # Return integration instance
    return GoogleSheetsIntegration(credentials_file, spreadsheet_id)


@pytest.fixture(scope="module")
@patch('integrations.slack_notifications.WebClient')
def slack_notifier(mock_web_client_class):
    """Set up Slack notifier for testing."""
    bot_token = os.getenv('SLACK_BOT_TOKEN', 'test-bot-token')
    webhook_url = os.getenv('SLACK_WEBHOOK_URL', 'https://hooks.slack.com/services/test')

    # Create a mock WebClient instance
    mock_client_instance = Mock()
    mock_client_instance.chat_postMessage.return_value = {'ts': '12345.6789', 'ok': True}
    mock_web_client_class.return_value = mock_client_instance

    # Return notifier instance
    return SlackNotifier(bot_token, webhook_url)


def test_log_conversation(google_sheets_integration):
    """Test logging conversation to the CRM via Google Sheets API."""
    conversation_data = {
        'customer_id': 'TEST001',
        'intent': 'LEAD_QUALIFICATION',
        'message': 'Test message',
        'response': 'Test response',
        'sentiment': 'Positive',
        'resolution_status': 'Resolved',
        'agent_name': 'TestBot'
    }

    success = google_sheets_integration.log_conversation(conversation_data)
    assert success == True, "Failed to log conversation data"


def test_log_lead(google_sheets_integration):
    """Test logging lead information to the CRM via Google Sheets API."""
    lead_data = {
        'customer_name': 'Test User',
        'email': 'test.user@example.com',
        'company': 'TestCorp',
        'company_size': '10-50',
        'budget_range': '$5,000-$9,999',
        'timeline': '1-3 months',
        'specific_needs': 'Test needs',
        'lead_score': 75,
        'priority': 'Medium',
        'source': 'TestBot',
        'status': 'New',
        'assigned_to': 'Test Rep'
    }

    success = google_sheets_integration.log_lead(lead_data)
    assert success == True, "Failed to log lead data"


def test_notify_high_priority_lead(slack_notifier):
    """Test sending high priority lead notifications via Slack."""
    lead_data = {
        'customer_id': 'TEST001',
        'customer_name': 'Priority Lead',
        'company': 'Priority Inc',
        'email': 'priority.lead@example.com',
        'lead_score': 95,
        'priority': 'High',
        'budget_range': '$25,000-$49,999',
        'timeline': 'Immediate',
        'specific_needs': 'Priority needs'
    }

    success = asyncio.run(slack_notifier.notify_high_priority_lead(lead_data))
    assert success == True, "Failed to send high priority lead notification"


def test_notify_technical_escalation(slack_notifier):
    """Test sending technical escalation notifications via Slack."""
    ticket_data = {
        'customer_name': 'Urgent User',
        'issue_type': 'Critical Issue',
        'issue_severity': 'CRITICAL',
        'ticket_id': 'CRIT-001',
        'issue_description': 'Test critical issue description'
    }

    success = asyncio.run(slack_notifier.notify_technical_escalation(ticket_data))
    assert success == True, "Failed to send technical escalation notification"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
