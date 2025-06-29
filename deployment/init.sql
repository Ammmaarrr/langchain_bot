-- Initialize TechCorp Chatbot Database
-- This script sets up the basic database schema for the chatbot

-- Create conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_id VARCHAR(255),
    intent VARCHAR(100),
    message TEXT,
    response TEXT,
    sentiment VARCHAR(50),
    resolution_status VARCHAR(100),
    agent_name VARCHAR(255)
);

-- Create leads table
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_name VARCHAR(255),
    email VARCHAR(255),
    company VARCHAR(255),
    company_size VARCHAR(100),
    budget_range VARCHAR(100),
    timeline VARCHAR(100),
    specific_needs TEXT,
    lead_score INTEGER,
    priority VARCHAR(50),
    source VARCHAR(100),
    status VARCHAR(100),
    assigned_to VARCHAR(255)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);
CREATE INDEX IF NOT EXISTS idx_conversations_customer_id ON conversations(customer_id);
CREATE INDEX IF NOT EXISTS idx_leads_timestamp ON leads(timestamp);
CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email);
CREATE INDEX IF NOT EXISTS idx_leads_priority ON leads(priority);

-- Insert sample data
INSERT INTO conversations (customer_id, intent, message, response, sentiment, resolution_status, agent_name)
VALUES 
    ('DEMO001', 'GENERAL_INQUIRY', 'Hello, what products do you offer?', 'Hi! We offer CRM, Marketing Automation, and Analytics solutions.', 'Positive', 'Resolved', 'DemoBot'),
    ('DEMO002', 'LEAD_QUALIFICATION', 'I''m interested in your CRM solution', 'Great! I''d love to learn more about your needs.', 'Positive', 'In Progress', 'DemoBot');

INSERT INTO leads (customer_name, email, company, company_size, budget_range, timeline, specific_needs, lead_score, priority, source, status, assigned_to)
VALUES 
    ('Demo User', 'demo@example.com', 'Demo Corp', '50-100', '$10,000-$24,999', '3-6 months', 'CRM integration needs', 75, 'Medium', 'Chatbot', 'New', 'Sales Rep 1'),
    ('Test Customer', 'test@company.com', 'Test Inc', '100-500', '$25,000-$49,999', 'Immediate', 'Full automation suite', 85, 'High', 'Chatbot', 'Qualified', 'Sales Rep 2');

COMMENT ON TABLE conversations IS 'Stores all chatbot conversation logs';
COMMENT ON TABLE leads IS 'Stores qualified lead information from chatbot interactions';
