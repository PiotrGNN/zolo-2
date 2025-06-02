#!/usr/bin/env python3
"""
Simple API test
"""
import requests
import sys

def test_simple():
    try:
        print("Testing localhost:5001 health...")
        r = requests.get("http://localhost:5001/health", timeout=3)
        print(f"Status: {r.status_code}")
        print(f"Text: {r.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_simple()
