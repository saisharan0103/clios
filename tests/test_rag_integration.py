"""
Integration Tests for RAG Pipeline
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.rag import query

def test_rag_integration():
    print("Starting RAG Integration Tests...\n")
    
    # Test Case 1: Specific Fact Retrieval
    print("Test 1: Specific Fact Retrieval")
    q1 = "Who won Clio Sports 2025?"
    print(f"Query: {q1}")
    r1 = query(q1)
    print(f"Answer: {r1['answer'][:100]}...")
    print(f"Filters: {r1['filters_used']}")
    
    if r1['has_answer'] and len(r1['sources']) > 0:
        print("PASS: Test 1")
    else:
        print("FAIL: Test 1")
    print("-" * 40 + "\n")
    
    # Test Case 2: Filtered Search (Jury)
    print("Test 2: Filtered Search (Jury)")
    q2 = "Who are the jury members for Clio Health?"
    print(f"Query: {q2}")
    r2 = query(q2)
    print(f"Filters: {r2['filters_used']}")
    
    if r2['filters_used'].get('page_type') == 'jury':
        print("PASS: Test 2")
    else:
        print("FAIL: Test 2")
    print("-" * 40 + "\n")
    
    # Test Case 3: Out of Domain
    print("Test 3: Out of Domain Query")
    q3 = "What is the capital of France?"
    print(f"Query: {q3}")
    r3 = query(q3)
    print(f"Answer: {r3['answer']}")
    
    if not r3['has_answer'] or "don't have" in r3['answer'].lower():
        print("PASS: Test 3")
    else:
        print("FAIL: Test 3")
    print("-" * 40 + "\n")
    
    print("Integration Tests Complete!")

if __name__ == "__main__":
    test_rag_integration()
