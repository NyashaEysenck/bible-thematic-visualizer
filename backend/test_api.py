"""
Simple script to test the FastAPI backend endpoints.
Run this after starting the backend server.
"""

import requests
import json

def test_endpoint(url):
    """Test a single API endpoint and print the results."""
    try:
        response = requests.get(url)
        print(f"\nTesting {url}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Response (first 3 items): {json.dumps(data[:3] if isinstance(data, list) else data, indent=2)[:500]}...")
            except ValueError:
                print("Response: (not JSON)", response.text[:200])
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def main():
    base_url = "http://localhost:8000/api/v1"
    
    # Test health check
    test_endpoint(f"{base_url}/health")
    
    # Test getting all themes
    test_endpoint(f"{base_url}/themes")
    
    # Test getting all books
    test_endpoint(f"{base_url}/books")
    
    # Test getting a specific book
    test_endpoint(f"{base_url}/books/1")
    
    # Test getting book insights
    test_endpoint(f"{base_url}/books/1/insights")
    
    # Test getting theme connections
    test_endpoint(f"{base_url}/themes/covenant/connections")

if __name__ == "__main__":
    print("Testing API Endpoints")
    print("=====================")
    main()
