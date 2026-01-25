#!/usr/bin/env python3
"""
GitHub Copilot Agent Skill tool: query_foundry_agent
Sends a prompt to Microsoft Foundry Agent for advanced AI processing.
"""

import os
import sys
import json
import argparse
import subprocess


def ensure_dependencies():
    """Install missing dependencies automatically."""
    required = ["requests", "azure-identity", "python-dotenv"]
    try:
        import requests
        from azure.identity import DefaultAzureCredential
        from dotenv import load_dotenv
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet"] + required)
        except subprocess.CalledProcessError:
            # pip failed, try ensurepip first
            try:
                subprocess.check_call([sys.executable, "-m", "ensurepip", "--default-pip"])
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet"] + required)
            except subprocess.CalledProcessError:
                print(json.dumps({
                    "error": "Failed to install dependencies. Please install pip and run: pip install requests azure-identity python-dotenv"
                }))
                sys.exit(1)


ensure_dependencies()

import requests
from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.core.exceptions import ClientAuthenticationError
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())


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
    except ClientAuthenticationError:
        # Attempt to run az login for the user
        try:
            subprocess.run(["az", "login"], check=True)
            # Retry with fresh credentials
            credential = AzureCliCredential()
            token = credential.get_token("https://ai.azure.com/.default")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token.token}"
            }
            payload = {"input": prompt}
            if conversation_id:
                payload["previous_response_id"] = conversation_id
            response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except subprocess.CalledProcessError:
            return {
                "error": "Azure login failed. Please run 'az login' manually.",
            }
        except Exception as e:
            return {
                "error": f"Authentication retry failed: {str(e)}",
            }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "type": type(e).__name__
        }


def main():
    """Main entry point for the tool when called by GitHub Copilot."""
    try:
        # Parse command-line arguments
        parser = argparse.ArgumentParser(description="Query Microsoft Foundry Agent")
        parser.add_argument("prompt", help="The user's question or request to send to the Foundry Agent")
        parser.add_argument("--conversation_id", "-c", help="Optional conversation ID for maintaining context", default=None)
        
        args = parser.parse_args()
        
        prompt = args.prompt
        conversation_id = args.conversation_id
        
        # Call the Foundry Agent
        result = query_foundry_agent(prompt, conversation_id)
        
        # Output result as JSON
        print(json.dumps(result))
        
    except Exception as e:
        print(json.dumps({"error": f"Tool execution failed: {str(e)}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
