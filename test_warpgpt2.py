#!/usr/bin/env python3
"""
Comprehensive Test Suite for TechCorp WarpGPT 2.0
Tests production-grade protocols and circuit breaker functionality
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'integrations'))

from warpgpt_2_0 import warpgpt
import time

def test_production_protocols():
    """Test WarpGPT 2.0 production protocols"""
    
    print("🚀 TechCorp WarpGPT 2.0 Production Test Suite")
    print("=" * 60)
    
    # Test system status
    print("\n📊 System Status Check")
    print("-" * 30)
    status = warpgpt.get_system_status()
    for key, value in status.items():
        if key != 'context':
            print(f"  • {key}: {value}")
    
    # Test cases with different confidence levels
    test_cases = [
        {
            "input": "VPN connection failed with authentication error",
            "description": "High confidence VPN issue",
            "expected": "verified_solution"
        },
        {
            "input": "Docker container won't start, exit code 125", 
            "description": "High confidence Docker issue",
            "expected": "verified_solution"
        },
        {
            "input": "SSL certificate expired on domain.com",
            "description": "High confidence SSL issue",
            "expected": "verified_solution"
        },
        {
            "input": "Database connection timeout after 30 seconds",
            "description": "High confidence DB issue", 
            "expected": "verified_solution"
        },
        {
            "input": "API returning 429 too many requests",
            "description": "High confidence API issue",
            "expected": "verified_solution"
        },
        {
            "input": "My coffee machine is broken",
            "description": "Low confidence - unrelated query",
            "expected": "uncertain_response"
        },
        {
            "input": "Production website is down emergency",
            "description": "Critical issue escalation",
            "expected": "critical_escalation"
        }
    ]
    
    print(f"\n🧪 Testing {len(test_cases)} Production Scenarios")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test['description']}")
        print(f"Input: \"{test['input']}\"")
        print(f"Expected: {test['expected']}")
        print("-" * 40)
        
        start_time = time.time()
        response = warpgpt.process_warp_request(test['input'])
        response_time = time.time() - start_time
        
        print(f"🤖 WarpGPT 2.0 Response (took {response_time:.2f}s):")
        print(response)
        
        # Validate response type
        if test['expected'] == 'verified_solution' and '✅ TechCorp Verified Fix' in response:
            print("✅ PASS: Verified solution provided")
        elif test['expected'] == 'uncertain_response' and '⚠️ I need more details' in response:
            print("✅ PASS: Uncertain response with circuit breaker")
        elif test['expected'] == 'critical_escalation' and '🚨 **CRITICAL ISSUE DETECTED**' in response:
            print("✅ PASS: Critical issue escalated")
        else:
            print("❌ FAIL: Unexpected response type")
        
        print("-" * 40)
    
    print(f"\n🔍 Hybrid Search Performance Test")
    print("-" * 30)
    
    # Test direct KB search
    test_queries = [
        "vpn authentication failed",
        "docker container startup error", 
        "ssl certificate problems",
        "database connection issues",
        "api rate limit exceeded"
    ]
    
    for query in test_queries:
        context = warpgpt.warp_context.get_context()
        results, confidence = warpgpt.execute_kb_search(query, context)
        
        print(f"Query: '{query}'")
        print(f"  Results: {len(results)} found | Confidence: {confidence:.2f}")
        if results:
            best_match = results[0]
            print(f"  Best: {best_match['entry']['title']} (#{best_match['id']})")
        print()

def test_circuit_breaker():
    """Test circuit breaker functionality"""
    
    print("\n⚡ Circuit Breaker Tests")
    print("=" * 30)
    
    # Test confidence thresholds
    threshold_tests = [
        ("High confidence query", "vpn connection refused authentication failed"),
        ("Medium confidence query", "network connectivity problems"), 
        ("Low confidence query", "random unrelated technical issue"),
        ("No match query", "purple elephant dancing in the moonlight")
    ]
    
    for description, query in threshold_tests:
        context = warpgpt.warp_context.get_context()
        results, confidence = warpgpt.execute_kb_search(query, context)
        
        print(f"{description}:")
        print(f"  Query: '{query}'")
        print(f"  Confidence: {confidence:.2f}")
        print(f"  Above threshold ({warpgpt.confidence_threshold}): {confidence >= warpgpt.confidence_threshold}")
        print(f"  Verified level ({warpgpt.verified_threshold}): {confidence >= warpgpt.verified_threshold}")
        print()

def test_warp_terminal_formatting():
    """Test Warp terminal formatting"""
    
    print("\n🖥️  Warp Terminal Formatting Test")
    print("=" * 35)
    
    test_commands = [
        "sudo systemctl restart nginx",
        "docker logs container_name --tail 50",
        "openssl x509 -in cert.pem -noout -dates",
        "netstat -tlnp | grep :80"
    ]
    
    for cmd in test_commands:
        formatted = warpgpt.warp_context.format_warp_terminal(cmd)
        print(f"Command: {cmd}")
        print(f"Formatted:")
        print(formatted)
        print()

def interactive_warpgpt2_test():
    """Interactive WarpGPT 2.0 test mode"""
    
    print("\n🔧 Interactive WarpGPT 2.0 Test")
    print("Type 'quit' to exit, 'status' for system status")
    print("Type 'critical:' before message to test critical escalation")
    print("=" * 50)
    
    while True:
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break
        elif user_input.lower() == 'status':
            status = warpgpt.get_system_status()
            print("\n📊 WarpGPT 2.0 System Status:")
            for key, value in status.items():
                if key != 'context':
                    print(f"  • {key}: {value}")
            continue
        elif user_input.lower().startswith('critical:'):
            # Force critical escalation test
            user_input = user_input[9:].strip() + " production down emergency"
        
        if not user_input:
            continue
        
        print("\n🔄 Processing with WarpGPT 2.0 protocols...")
        start_time = time.time()
        response = warpgpt.process_warp_request(user_input)
        response_time = time.time() - start_time
        
        print(f"\n🤖 WarpGPT 2.0 (Response time: {response_time:.2f}s):")
        print(response)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test TechCorp WarpGPT 2.0")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--circuit-breaker", "-c", action="store_true", help="Test circuit breaker only")
    parser.add_argument("--formatting", "-f", action="store_true", help="Test formatting only")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_warpgpt2_test()
    elif args.circuit_breaker:
        test_circuit_breaker()
    elif args.formatting:
        test_warp_terminal_formatting()
    else:
        test_production_protocols()
        test_circuit_breaker()
        test_warp_terminal_formatting()
        
        print("\n🎉 All WarpGPT 2.0 tests completed!")
        print("\nRun with --interactive (-i) for interactive testing")
        print("Run with --circuit-breaker (-c) to test only circuit breaker")
        print("Run with --formatting (-f) to test only terminal formatting")
