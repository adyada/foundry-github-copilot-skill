#!/usr/bin/env python3
"""
Example script demonstrating how to call a Microsoft Foundry Agent from Python.
This is a practical implementation of the foundry-agent skill.
"""

import os
import sys
import requests
from typing import Dict, Any, Optional


class FoundryAgentClient:
    """Client for interacting with Microsoft Foundry Agent endpoints."""
    
    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize the Foundry Agent client.
        
        Args:
            endpoint: The Foundry Agent endpoint URL. 
                     If not provided, reads from FOUNDRY_AGENT_ENDPOINT env var.
            api_key: The API key for authentication.
                    If not provided, reads from FOUNDRY_AGENT_API_KEY env var.
        """
        self.endpoint = endpoint or os.getenv(
            "FOUNDRY_AGENT_ENDPOINT",
            "https://YOUR-FOUNDRY-ENDPOINT.azure.com/chat"
        )
        self.api_key = api_key or os.getenv("FOUNDRY_AGENT_API_KEY")
        self.session = requests.Session()
        
        # Set up default headers
        self.session.headers.update({
            "Content-Type": "application/json",
        })
        
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}"
            })
    
    def ask(
        self,
        prompt: str,
        conversation_id: Optional[str] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Send a prompt to the Foundry Agent.
        
        Args:
            prompt: The user's question or request
            conversation_id: Optional conversation ID for maintaining context
            timeout: Request timeout in seconds
            
        Returns:
            The agent's response as a dictionary
        """
        payload = {
            "message": prompt,
        }
        
        if conversation_id:
            payload["conversation_id"] = conversation_id
        
        try:
            response = self.session.post(
                self.endpoint,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            return {
                "error": f"HTTP error: {e.response.status_code}",
                "details": str(e)
            }
        except requests.exceptions.ConnectionError as e:
            return {
                "error": "Connection error",
                "details": "Failed to connect to Foundry Agent endpoint"
            }
        except requests.exceptions.Timeout as e:
            return {
                "error": "Timeout error",
                "details": f"Request timed out after {timeout} seconds"
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": "Request failed",
                "details": str(e)
            }
        except ValueError as e:
            return {
                "error": "Invalid JSON response",
                "details": str(e)
            }


def main():
    """Main function demonstrating the Foundry Agent client."""
    print("Foundry Agent Client Example")
    print("=" * 50)
    
    # Initialize the client
    client = FoundryAgentClient()
    
    print(f"Endpoint: {client.endpoint}")
    print(f"API Key configured: {'Yes' if client.api_key else 'No'}")
    print()
    
    # Example prompts
    examples = [
        "What are the key trends in cloud computing?",
        "Explain the benefits of AI in software development",
        "Analyze the impact of automation on productivity"
    ]
    
    # If command line arguments provided, use them as prompts
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        print(f"User Prompt: {prompt}")
        print("-" * 50)
        
        result = client.ask(prompt)
        
        if "error" in result:
            print(f"Error: {result['error']}")
            if "details" in result:
                print(f"Details: {result['details']}")
        else:
            print("Agent Response:")
            print(result)
    else:
        # Run example prompts
        print("Running example prompts:")
        print()
        
        for i, prompt in enumerate(examples, 1):
            print(f"{i}. Prompt: {prompt}")
            result = client.ask(prompt)
            
            if "error" in result:
                print(f"   Error: {result['error']}")
            else:
                print(f"   Response: {result.get('response', result)}")
            print()


if __name__ == "__main__":
    main()
