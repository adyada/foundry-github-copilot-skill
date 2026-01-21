#!/usr/bin/env python3
"""
Example script demonstrating how to call a Microsoft Foundry Agent from Python.
This is a practical implementation of the foundry-agent skill.
"""

import os
import sys
import requests
from typing import Dict, Any, Optional
from azure.identity import DefaultAzureCredential


class FoundryAgentClient:
    """Client for interacting with Microsoft Foundry Agent endpoints."""
    
    # Default scope for Azure AI services
    DEFAULT_SCOPE = "https://ai.azure.com/.default"
    
    def __init__(
        self,
        endpoint: Optional[str] = None,
        credential: Optional[DefaultAzureCredential] = None,
        scope: Optional[str] = None
    ):
        """
        Initialize the Foundry Agent client.
        
        Args:
            endpoint: The Foundry Agent endpoint URL. 
                     If not provided, reads from FOUNDRY_AGENT_ENDPOINT env var.
            credential: Azure credential for authentication.
                       If not provided, uses DefaultAzureCredential.
            scope: The token scope for authentication.
                  Defaults to Azure AI services scope.
        """
        self.endpoint = endpoint or os.getenv(
            "FOUNDRY_AGENT_ENDPOINT",
            "https://e2e-tests-westus2-account.services.ai.azure.com/api/projects/e2e-tests-westus2/applications/test-adyada/protocols/openai/responses?api-version=2025-11-15-preview"
        )
        self.credential = credential or DefaultAzureCredential()
        self.scope = scope or self.DEFAULT_SCOPE
        self.session = requests.Session()
        
        # Set up default headers
        self.session.headers.update({
            "Content-Type": "application/json",
        })
    
    def _get_token(self) -> str:
        """Get an access token using DefaultAzureCredential."""
        token = self.credential.get_token(self.scope)
        return token.token
    
    def _update_auth_header(self):
        """Update the authorization header with a fresh token."""
        token = self._get_token()
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
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
        # Use OpenAI-compatible request format for Foundry Agent
        payload = {
            "input": prompt,
        }
        
        if conversation_id:
            payload["previous_response_id"] = conversation_id
        
        try:
            # Refresh the auth token before each request
            self._update_auth_header()
            
            response = self.session.post(
                self.endpoint,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_body = ""
            try:
                error_body = e.response.text
            except:
                pass
            return {
                "error": f"HTTP error: {e.response.status_code}",
                "details": str(e),
                "response_body": error_body
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
    print(f"Credential: DefaultAzureCredential")
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
        
        if result.get("error"):
            print(f"Error: {result['error']}")
            if "details" in result:
                print(f"Details: {result['details']}")
            if "response_body" in result:
                print(f"Response Body: {result['response_body']}")
        else:
            print("Agent Response:")
            import json
            print(json.dumps(result, indent=2))
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
