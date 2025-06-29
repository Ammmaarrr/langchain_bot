"""
Google Sheets API Integration for Customer Support & Lead Qualification Bot
Handles CRM data logging, lead tracking, and analytics data collection.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleSheetsIntegration:
    """
    Google Sheets integration for CRM and analytics functionality.
    """
    
    def __init__(self, credentials_file: str, spreadsheet_id: str):
        """
        Initialize Google Sheets integration.
        
        Args:
            credentials_file: Path to service account credentials JSON
            spreadsheet_id: Google Sheets spreadsheet ID
        """
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API."""
        try:
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            creds = Credentials.from_service_account_file(
                self.credentials_file, scopes=SCOPES
            )
            self.service = build('sheets', 'v4', credentials=creds)
            logger.info("Successfully authenticated with Google Sheets API")
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Sheets: {e}")
            raise
    
    def log_conversation(self, conversation_data: Dict) -> bool:
        """
        Log conversation data to the 'Conversations' sheet.
        
        Args:
            conversation_data: Dictionary containing conversation details
            
        Returns:
            bool: Success status
        """
        try:
            # Prepare data for insertion
            timestamp = datetime.now().isoformat()
            row_data = [
                timestamp,
                conversation_data.get('customer_id', 'Unknown'),
                conversation_data.get('intent', 'Unknown'),
                conversation_data.get('message', ''),
                conversation_data.get('response', ''),
                conversation_data.get('sentiment', 'Neutral'),
                conversation_data.get('resolution_status', 'Open'),
                conversation_data.get('agent_name', 'AI Bot')
            ]
            
            # Insert data into sheet
            range_name = 'Conversations!A:H'
            value_input_option = 'USER_ENTERED'
            
            body = {
                'values': [row_data]
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body
            ).execute()
            
            logger.info(f"Conversation logged successfully: {result.get('updates', {}).get('updatedCells', 0)} cells updated")
            return True
            
        except HttpError as e:
            logger.error(f"Failed to log conversation: {e}")
            return False
    
    def log_lead(self, lead_data: Dict) -> bool:
        """
        Log qualified lead data to the 'Leads' sheet.
        
        Args:
            lead_data: Dictionary containing lead information
            
        Returns:
            bool: Success status
        """
        try:
            timestamp = datetime.now().isoformat()
            row_data = [
                timestamp,
                lead_data.get('customer_name', 'Unknown'),
                lead_data.get('email', ''),
                lead_data.get('company', ''),
                lead_data.get('company_size', ''),
                lead_data.get('budget_range', ''),
                lead_data.get('timeline', ''),
                lead_data.get('specific_needs', ''),
                lead_data.get('lead_score', 0),
                lead_data.get('priority', 'Medium'),
                lead_data.get('source', 'Chatbot'),
                lead_data.get('status', 'New'),
                lead_data.get('assigned_to', 'Unassigned')
            ]
            
            range_name = 'Leads!A:M'
            value_input_option = 'USER_ENTERED'
            
            body = {
                'values': [row_data]
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body
            ).execute()
            
            logger.info(f"Lead logged successfully: {result.get('updates', {}).get('updatedCells', 0)} cells updated")
            return True
            
        except HttpError as e:
            logger.error(f"Failed to log lead: {e}")
            return False
    
    def update_analytics(self, metric_data: Dict) -> bool:
        """
        Update analytics data in the 'Analytics' sheet.
        
        Args:
            metric_data: Dictionary containing analytics metrics
            
        Returns:
            bool: Success status
        """
        try:
            date = datetime.now().strftime('%Y-%m-%d')
            
            # Check if today's row exists
            range_name = 'Analytics!A:A'
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            today_row = None
            
            for i, row in enumerate(values):
                if row and row[0] == date:
                    today_row = i + 1
                    break
            
            # Prepare analytics data
            analytics_data = [
                date,
                metric_data.get('total_conversations', 0),
                metric_data.get('leads_generated', 0),
                metric_data.get('technical_tickets', 0),
                metric_data.get('avg_response_time', 0),
                metric_data.get('customer_satisfaction', 0),
                metric_data.get('resolution_rate', 0)
            ]
            
            if today_row:
                # Update existing row
                range_name = f'Analytics!A{today_row}:G{today_row}'
                body = {'values': [analytics_data]}
                
                result = self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=range_name,
                    valueInputOption='USER_ENTERED',
                    body=body
                ).execute()
            else:
                # Append new row
                range_name = 'Analytics!A:G'
                body = {'values': [analytics_data]}
                
                result = self.service.spreadsheets().values().append(
                    spreadsheetId=self.spreadsheet_id,
                    range=range_name,
                    valueInputOption='USER_ENTERED',
                    body=body
                ).execute()
            
            logger.info("Analytics updated successfully")
            return True
            
        except HttpError as e:
            logger.error(f"Failed to update analytics: {e}")
            return False
    
    def get_lead_stats(self) -> Dict:
        """
        Get lead statistics for dashboard display.
        
        Returns:
            Dict: Lead statistics
        """
        try:
            range_name = 'Leads!A:M'
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return {}
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(values[1:], columns=values[0])  # Skip header row
            
            # Calculate statistics
            stats = {
                'total_leads': len(df),
                'high_priority_leads': len(df[df['Priority'] == 'High']),
                'qualified_leads': len(df[df['Lead Score'].astype(float) > 70]),
                'avg_lead_score': df['Lead Score'].astype(float).mean(),
                'leads_by_status': df['Status'].value_counts().to_dict(),
                'leads_by_source': df['Source'].value_counts().to_dict()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get lead stats: {e}")
            return {}
    
    def setup_sheets(self) -> bool:
        """
        Set up initial sheet structure with headers.
        
        Returns:
            bool: Success status
        """
        try:
            # Define sheet structures
            sheets_config = {
                'Conversations': [
                    'Timestamp', 'Customer ID', 'Intent', 'Message', 
                    'Response', 'Sentiment', 'Resolution Status', 'Agent'
                ],
                'Leads': [
                    'Timestamp', 'Customer Name', 'Email', 'Company', 
                    'Company Size', 'Budget Range', 'Timeline', 'Specific Needs',
                    'Lead Score', 'Priority', 'Source', 'Status', 'Assigned To'
                ],
                'Analytics': [
                    'Date', 'Total Conversations', 'Leads Generated', 
                    'Technical Tickets', 'Avg Response Time', 
                    'Customer Satisfaction', 'Resolution Rate'
                ]
            }
            
            # Get existing sheets
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            existing_sheets = {sheet['properties']['title'] 
                             for sheet in spreadsheet['sheets']}
            
            # Create missing sheets and add headers
            for sheet_name, headers in sheets_config.items():
                if sheet_name not in existing_sheets:
                    # Create sheet
                    requests = [{
                        'addSheet': {
                            'properties': {
                                'title': sheet_name
                            }
                        }
                    }]
                    
                    body = {'requests': requests}
                    self.service.spreadsheets().batchUpdate(
                        spreadsheetId=self.spreadsheet_id,
                        body=body
                    ).execute()
                
                # Add headers
                range_name = f'{sheet_name}!A1:{chr(65 + len(headers) - 1)}1'
                body = {'values': [headers]}
                
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=range_name,
                    valueInputOption='USER_ENTERED',
                    body=body
                ).execute()
            
            logger.info("Sheets setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup sheets: {e}")
            return False


# Example usage and testing
if __name__ == "__main__":
    # Load configuration from environment
    credentials_file = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE')
    spreadsheet_id = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
    
    if not credentials_file or not spreadsheet_id:
        logger.error("Missing required environment variables")
        exit(1)
    
    # Initialize integration
    sheets = GoogleSheetsIntegration(credentials_file, spreadsheet_id)
    
    # Setup sheets
    sheets.setup_sheets()
    
    # Test conversation logging
    conversation_data = {
        'customer_id': 'CUST001',
        'intent': 'LEAD_QUALIFICATION',
        'message': 'I need a CRM solution for my company',
        'response': 'Great! I\'d be happy to help you find the right CRM solution...',
        'sentiment': 'Positive',
        'resolution_status': 'In Progress',
        'agent_name': 'Sarah (AI)'
    }
    
    sheets.log_conversation(conversation_data)
    
    # Test lead logging
    lead_data = {
        'customer_name': 'John Smith',
        'email': 'john.smith@example.com',
        'company': 'Tech Innovations Inc',
        'company_size': '50-100',
        'budget_range': '$10,000-$25,000',
        'timeline': '3-6 months',
        'specific_needs': 'CRM with marketing automation',
        'lead_score': 85,
        'priority': 'High',
        'source': 'Website Chatbot',
        'status': 'New'
    }
    
    sheets.log_lead(lead_data)
    
    # Test analytics update
    metric_data = {
        'total_conversations': 150,
        'leads_generated': 25,
        'technical_tickets': 8,
        'avg_response_time': 2.5,
        'customer_satisfaction': 4.2,
        'resolution_rate': 0.85
    }
    
    sheets.update_analytics(metric_data)
    
    # Get lead statistics
    stats = sheets.get_lead_stats()
    print("Lead Statistics:", json.dumps(stats, indent=2))
