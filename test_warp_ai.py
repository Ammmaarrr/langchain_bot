#!/usr/bin/env python3
"""
Test script for TechCorp Warp AI Assistant
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'integrations'))

from techcorp_warp_ai import techcorp_ai

def test_warp_ai():
    """Test the TechCorp Warp AI functionality"""
    
    print("🚀 TechCorp Warp AI Assistant Test")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "input": "VPN won't connect",
            "product": "network",
            "description": "VPN connection issue"
        },
        {
            "input": "Docker container crashed",
            "product": "containers", 
            "description": "Container startup problem"
        },
        {
            "input": "SSL certificate expired",
            "product": "security",
            "description": "Security certificate issue"
        },
        {
            "input": "My microwave won't heat food",
            "product": "system",
            "description": "Unrelated query (should ask clarifying questions)"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test['description']}")
        print(f"User Input: \"{test['input']}\"")
        print(f"Product: {test['product']}")
        print("-" * 30)
        
        # Process the message
        response = techcorp_ai.process_message(test['input'], test['product'])
        
        print("🤖 AI Response:")
        print(response)
        print("-" * 30)
        
        # Test knowledge base search directly
        kb_result = techcorp_ai.execute_kb_command(test['input'])
        print(f"📚 KB Search Results: {len(kb_result['results'])} found")
        if kb_result['results']:
            for result in kb_result['results']:
                print(f"  • {result['entry']['title']} (#{result['id']})")
        print()
    
    # Test logging a new solution
    print("\n📝 Testing Solution Logging")
    print("-" * 30)
    
    log_result = techcorp_ai.execute_log_command(
        problem="Email server not responding",
        solution="Restart postfix service: `sudo systemctl restart postfix`",
        category="email"
    )
    print(f"✅ Log Result: {log_result}")
    
    # Show conversation context
    print(f"\n💭 Conversation Context:")
    print("-" * 30)
    context = techcorp_ai.get_conversation_context()
    print(context)
    
    print("\n🎉 Test completed!")

def interactive_test():
    """Interactive test mode"""
    print("\n🔧 Interactive TechCorp Warp AI Test")
    print("Type 'quit' to exit, 'context' to see conversation history")
    print("=" * 50)
    
    product = input("Enter product name (default: system): ").strip() or "system"
    
    # Show greeting
    greeting = techcorp_ai.get_greeting(product)
    print(f"\n🤖 {greeting}")
    
    while True:
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break
        elif user_input.lower() == 'context':
            print("\n💭 Conversation Context:")
            print(techcorp_ai.get_conversation_context())
            continue
        elif user_input.lower().startswith('/kb '):
            # Direct KB search
            query = user_input[4:]
            result = techcorp_ai.execute_kb_command(query)
            print(f"\n📚 KB Search Results:")
            if result['results']:
                formatted = techcorp_ai.format_kb_results(result['results'])
                print(formatted)
            else:
                print("No results found.")
            continue
        elif user_input.lower().startswith('/log '):
            # Direct solution logging
            parts = user_input[5:].split(' | ')
            if len(parts) >= 2:
                problem = parts[0]
                solution = parts[1]
                category = parts[2] if len(parts) > 2 else "general"
                result = techcorp_ai.execute_log_command(problem, solution, category)
                print(f"\n✅ {result}")
            else:
                print("Usage: /log problem | solution | category")
            continue
        
        if not user_input:
            continue
        
        # Process message
        response = techcorp_ai.process_message(user_input, product)
        print(f"\n🤖 {response}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test TechCorp Warp AI Assistant")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_test()
    else:
        test_warp_ai()
