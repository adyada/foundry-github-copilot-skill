"""
Microsoft Foundry Agent Integration Example (Python)

This example demonstrates how to call a Microsoft Foundry agent application
using the Azure AI SDK with proper authentication and error handling.

Prerequisites:
    pip install azure-ai-projects azure-identity

Environment Variables:
    AZURE_AI_PROJECT_ENDPOINT: Your Foundry project endpoint
    AZURE_AI_MODEL_DEPLOYMENT_NAME: Your agent deployment name
"""

import os
import sys
from typing import Optional
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import AzureError


class FoundryAgentClient:
    """Client for interacting with Microsoft Foundry agents."""
    
    def __init__(self, endpoint: Optional[str] = None, credential=None):
        """
        Initialize the Foundry agent client.
        
        Args:
            endpoint: The Foundry project endpoint URL
            credential: Azure credential object (defaults to DefaultAzureCredential)
        """
        self.endpoint = endpoint or os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        if not self.endpoint:
            raise ValueError("AZURE_AI_PROJECT_ENDPOINT must be set")
        
        self.credential = credential or DefaultAzureCredential()
        
        try:
            self.client = AIProjectClient(
                endpoint=self.endpoint,
                credential=self.credential
            )
            print(f"✓ Connected to Foundry project: {self.endpoint}")
        except AzureError as e:
            print(f"✗ Failed to initialize client: {e}")
            raise
    
    def send_message(self, message: str, conversation_id: Optional[str] = None) -> dict:
        """
        Send a message to the Foundry agent.
        
        Args:
            message: The message text to send
            conversation_id: Optional conversation ID for multi-turn conversations
            
        Returns:
            dict: The agent's response
        """
        try:
            # Prepare the request
            request_data = {
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            }
            
            if conversation_id:
                request_data["conversation_id"] = conversation_id
            
            # Call the agent
            print(f"\n→ Sending message: {message}")
            response = self.client.agents.invoke(
                deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
                **request_data
            )
            
            print(f"✓ Received response")
            return response
            
        except AzureError as e:
            print(f"✗ Error calling agent: {e}")
            raise
    
    def send_message_stream(self, message: str, conversation_id: Optional[str] = None):
        """
        Send a message to the Foundry agent with streaming response.
        
        Args:
            message: The message text to send
            conversation_id: Optional conversation ID for multi-turn conversations
            
        Yields:
            Response chunks as they arrive
        """
        try:
            # Prepare the request
            request_data = {
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "stream": True
            }
            
            if conversation_id:
                request_data["conversation_id"] = conversation_id
            
            # Call the agent with streaming
            print(f"\n→ Sending message (streaming): {message}")
            stream = self.client.agents.invoke(
                deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
                **request_data
            )
            
            print("✓ Streaming response:")
            for chunk in stream:
                yield chunk
                
        except AzureError as e:
            print(f"✗ Error calling agent: {e}")
            raise


def example_simple_call():
    """Example: Simple single-turn agent call."""
    print("\n" + "="*60)
    print("Example 1: Simple Agent Call")
    print("="*60)
    
    try:
        # Initialize the client
        client = FoundryAgentClient()
        
        # Send a message
        response = client.send_message(
            "What is Microsoft Foundry and how does it help developers?"
        )
        
        # Process the response
        if response and "messages" in response:
            for msg in response["messages"]:
                if msg.get("role") == "assistant":
                    print(f"\nAgent Response:\n{msg.get('content', '')}")
        
        print("\n✓ Example completed successfully")
        
    except Exception as e:
        print(f"\n✗ Example failed: {e}")
        return False
    
    return True


def example_streaming_call():
    """Example: Streaming agent call for real-time responses."""
    print("\n" + "="*60)
    print("Example 2: Streaming Agent Call")
    print("="*60)
    
    try:
        # Initialize the client
        client = FoundryAgentClient()
        
        # Send a message with streaming
        print("\nAgent Response (streaming):")
        full_response = ""
        
        for chunk in client.send_message_stream(
            "Explain the benefits of using AI agents in software development."
        ):
            # Process each chunk
            if chunk and "delta" in chunk:
                content = chunk["delta"].get("content", "")
                if content:
                    print(content, end="", flush=True)
                    full_response += content
        
        print("\n\n✓ Example completed successfully")
        
    except Exception as e:
        print(f"\n✗ Example failed: {e}")
        return False
    
    return True


def example_conversation():
    """Example: Multi-turn conversation with context."""
    print("\n" + "="*60)
    print("Example 3: Multi-Turn Conversation")
    print("="*60)
    
    try:
        # Initialize the client
        client = FoundryAgentClient()
        
        # First message
        response1 = client.send_message(
            "I'm building a web application. What technology stack would you recommend?"
        )
        
        conversation_id = response1.get("conversation_id")
        
        if response1 and "messages" in response1:
            for msg in response1["messages"]:
                if msg.get("role") == "assistant":
                    print(f"\nAgent Response 1:\n{msg.get('content', '')}")
        
        # Follow-up message with conversation context
        if conversation_id:
            response2 = client.send_message(
                "What about for a mobile app instead?",
                conversation_id=conversation_id
            )
            
            if response2 and "messages" in response2:
                for msg in response2["messages"]:
                    if msg.get("role") == "assistant":
                        print(f"\nAgent Response 2:\n{msg.get('content', '')}")
        
        print("\n✓ Example completed successfully")
        
    except Exception as e:
        print(f"\n✗ Example failed: {e}")
        return False
    
    return True


def main():
    """Run all examples."""
    print("Microsoft Foundry Agent Integration Examples")
    print("=" * 60)
    
    # Check environment variables
    required_vars = ["AZURE_AI_PROJECT_ENDPOINT", "AZURE_AI_MODEL_DEPLOYMENT_NAME"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"\n✗ Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("\nPlease set the following environment variables:")
        print("  AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project")
        print("  AZURE_AI_MODEL_DEPLOYMENT_NAME=your-deployment-name")
        sys.exit(1)
    
    # Run examples
    examples = [
        example_simple_call,
        example_streaming_call,
        example_conversation
    ]
    
    results = []
    for example in examples:
        try:
            success = example()
            results.append(success)
        except KeyboardInterrupt:
            print("\n\n✗ Interrupted by user")
            break
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    successful = sum(results)
    total = len(results)
    print(f"Completed {successful}/{total} examples successfully")
    
    if successful == total:
        print("✓ All examples passed!")
        sys.exit(0)
    else:
        print("✗ Some examples failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
