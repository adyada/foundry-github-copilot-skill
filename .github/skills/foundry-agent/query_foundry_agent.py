#!/usr/bin/env python3
"""
GitHub Copilot Agent Skill tool: query_foundry_agent
Sends a prompt to Microsoft Foundry Agent for advanced AI processing.
"""

import os
import sys
import json
import requests
from azure.identity import DefaultAzureCredential


def query_foundry_agent(prompt: str, conversation_id: str = None):
    """
    Query the Microsoft Foundry Agent with a user prompt.
    
    Args:
        prompt: The user's question or request to send to the Foundry Agent
        conversation_id: Optional conversation ID for maintaining context across multiple requests
        
    Returns:
        dict: The Foundry Agent response or error information
    """
    try:
        # Initialize Azure credential
        credential = DefaultAzureCredential()

        # Get endpoint from environment (required)
        # Example: "https://<foundry-account-name>.services.ai.azure.com/api/projects/<project-name>/applications/<application-name>/protocols/openai/responses?api-version=2025-11-15-preview"
        endpoint = os.getenv("FOUNDRY_AGENT_APPLICATION_ENDPOINT")
        if not endpoint:
            raise ValueError("FOUNDRY_AGENT_APPLICATION_ENDPOINT environment variable is required but not set")

        # Get access token
        token = credential.get_token("https://ai.azure.com/.default")
        
        # Prepare request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token.token}"
        }
        
        payload = {
            "input": prompt,
        }
        
        if conversation_id:
            payload["previous_response_id"] = conversation_id
        
        # Send request to Foundry Agent
        response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        # Return the response
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to call Foundry Agent: {str(e)}",
            "endpoint": endpoint
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "type": type(e).__name__
        }


def main():
    """Main entry point for the tool when called by GitHub Copilot."""
    try:
        # Read input parameters from stdin (JSON format)
        input_data = json.loads(sys.stdin.read())
        
        prompt = input_data.get("prompt")
        conversation_id = input_data.get("conversation_id")
        
        if not prompt:
            print(json.dumps({"error": "Missing required parameter: prompt"}))
            sys.exit(1)
        
        # Call the Foundry Agent
        result = query_foundry_agent(prompt, conversation_id)
        
        # Output result as JSON
        print(json.dumps(result))
        
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {str(e)}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Tool execution failed: {str(e)}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
