import argparse
import json
import requests
from typing import Dict, Any

class BMSClient:
    def __init__(self, base_url: str = "http://127.0.0.1:5000/api"):
        self.base_url = base_url.rstrip('/')
        print(f"Connecting to {self.base_url}")
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and return JSON data"""
        try:
            if response.status_code == 204:  # No content
                return {'message': 'Operation successful'}
            
            data = response.json()
            if response.ok:
                return data
            else:
                raise Exception(data.get('error', 'Unknown error occurred'))
        except requests.exceptions.JSONDecodeError:
            raise Exception(f"Invalid response from server: {response.text}")

    def create_account(self, name: str, number: str, balance: float = 0.0) -> Dict[str, Any]:
        """Create a new account"""
        url = f"{self.base_url}/accounts"
        print(f"Sending POST request to {url}")
        try:
            response = requests.post(
                url,
                json={'name': name, 'number': number, 'balance': balance},
                timeout=5
            )
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text}")
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            raise
    
    def get_account(self, account_id: int) -> Dict[str, Any]:
        """Get account by ID"""
        url = f"{self.base_url}/accounts/{account_id}"
        print(f"Sending GET request to {url}")
        try:
            response = requests.get(url, timeout=5)
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text}")
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            raise
    
    def list_accounts(self) -> Dict[str, Any]:
        """List all accounts"""
        url = f"{self.base_url}/accounts"
        print(f"Sending GET request to {url}")
        try:
            response = requests.get(url, timeout=5)
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text}")
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            raise
    
    def delete_account(self, account_id: int) -> Dict[str, Any]:
        """Delete an account"""
        url = f"{self.base_url}/accounts/{account_id}"
        print(f"Sending DELETE request to {url}")
        try:
            response = requests.delete(url, timeout=5)
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text}")
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            raise

def main():
    parser = argparse.ArgumentParser(description="BMS CLI Client")
    parser.add_argument('action', choices=['create', 'get', 'list', 'delete'],
                       help="Action to perform")
    parser.add_argument('--name', help="Account holder name")
    parser.add_argument('--number', help="Account number")
    parser.add_argument('--balance', type=float, help="Initial balance")
    parser.add_argument('--id', type=int, help="Account ID")
    
    args = parser.parse_args()
    client = BMSClient()
    
    try:
        if args.action == 'create':
            if not all([args.name, args.number]):
                raise ValueError("Name and number are required for account creation")
            result = client.create_account(args.name, args.number, args.balance or 0.0)
        
        elif args.action == 'get':
            if not args.id:
                raise ValueError("Account ID is required")
            result = client.get_account(args.id)
        
        elif args.action == 'list':
            result = client.list_accounts()
        
        elif args.action == 'delete':
            if not args.id:
                raise ValueError("Account ID is required")
            result = client.delete_account(args.id)
        
        print(json.dumps(result, indent=2))
    
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()