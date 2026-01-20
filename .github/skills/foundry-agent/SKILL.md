---
name: foundry-agent
description: Integrate and call Microsoft Foundry agent applications using REST APIs. This skill helps developers understand how to authenticate, configure, and invoke Foundry agents in their applications.
license: MIT
metadata:
  author: GitHub Copilot
  version: 1.0.0
---

# Microsoft Foundry Agent Integration Skill

This skill demonstrates how to integrate and call Microsoft Foundry agent applications using REST APIs. Microsoft Foundry is a developer platform that enables integration of AI agents and models into apps and workflows.

## When to Use This Skill

Use this skill when you need to:
- Integrate Microsoft Foundry agents into your application
- Call AI agents via REST APIs
- Set up authentication for Foundry agent applications
- Implement stateful or stateless agent interactions
- Build workflows that leverage published Foundry agents

## Prerequisites

Before using this skill, ensure you have:
- A Microsoft Foundry project with a published agent
- Azure credentials (for authentication)
- The Foundry agent endpoint URL
- Required SDK packages installed (Python or Node.js)

## Integration Patterns

### 1. REST API Integration (Recommended)

For full control, invoke Foundry endpoints directly:

**Stateless (single call) actions:**
```
POST https://{resource}.services.ai.azure.com/api/
```

**Stateful (agent or session-based) calls:**
```
POST https://{resource}.services.ai.azure.com/api/projects/{projectname}/
```

### 2. SDK-Based Integration

Use the Azure AI SDK for simplified integration with built-in authentication and error handling.

## Authentication Methods

Microsoft Foundry supports multiple authentication methods:
- **DefaultAzureCredential** (recommended for production)
- **API Key** authentication
- **Managed Identity** (for Azure-hosted applications)

## Environment Variables

Configure these environment variables for your application:

```bash
# Required
AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com
AZURE_AGENT_ID=your-agent-id

# For API Key Authentication (if not using DefaultAzureCredential)
AZURE_AI_API_KEY=your-api-key

# Optional
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
```

## Usage Examples

See the included example scripts for complete implementation:

### Python Example
- **File:** `example_python.py`
- Demonstrates Azure SDK integration with DefaultAzureCredential
- Shows both synchronous and streaming responses
- Includes error handling and best practices

### TypeScript/JavaScript Example
- **File:** `example_typescript.ts`
- Demonstrates REST API integration using fetch
- Shows request/response handling
- Includes authentication patterns

## Step-by-Step Instructions

### 1. Install Dependencies

**Python:**
```bash
pip install azure-ai-projects azure-identity
```

**Node.js:**
```bash
npm install @azure/identity @azure/core-rest-pipeline
```

### 2. Configure Authentication

Set up your environment variables or use Azure CLI for authentication:
```bash
az login
```

### 3. Initialize the Client

Use the provided example scripts as templates for your specific use case.

### 4. Make Agent Calls

Invoke your Foundry agent with messages and retrieve responses.

### 5. Handle Responses

Process agent responses, including streaming support for real-time interactions.

## Best Practices

1. **Use DefaultAzureCredential** in production for secure, token-based authentication
2. **Implement retry logic** for transient failures
3. **Use streaming** for long-running agent operations to improve user experience
4. **Log agent interactions** for debugging and monitoring
5. **Handle errors gracefully** with appropriate fallback mechanisms
6. **Cache credentials** to avoid repeated authentication calls
7. **Use managed identity** when deploying to Azure services

## Security Considerations

- Never commit API keys or secrets to source control
- Use environment variables or Azure Key Vault for sensitive configuration
- Rotate API keys regularly
- Use managed identities when possible
- Implement proper RBAC (Role-Based Access Control)

## Troubleshooting

### Common Issues

**Authentication Failures:**
- Verify your credentials are correctly configured
- Ensure you have the necessary permissions on the Foundry project
- Check that your Azure subscription is active

**Connection Errors:**
- Verify the endpoint URL is correct
- Check network connectivity and firewall rules
- Ensure the agent is published and available

**Response Errors:**
- Check the agent's input schema requirements
- Validate your message format matches the expected schema
- Review agent logs in the Foundry portal

## Additional Resources

- [Microsoft Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Integrate Microsoft Foundry with Applications](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/integrate-with-other-apps)
- [Publish Agents in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/publish-agent)
- [Azure AI SDK Documentation](https://learn.microsoft.com/en-us/python/api/overview/azure/ai)

## Example Workflows

### Workflow 1: Simple Question-Answer Agent
```
1. Initialize client with credentials
2. Send user question as message
3. Receive and display agent response
4. Log interaction for analytics
```

### Workflow 2: Multi-Turn Conversation
```
1. Initialize client with session management
2. Send initial message and store conversation ID
3. Continue conversation with context preservation
4. Handle session state across multiple requests
5. Close session when conversation ends
```

### Workflow 3: External API Integration
```
1. Configure agent with OpenAPI specification
2. Agent calls external APIs as needed
3. Process combined results from agent and APIs
4. Return enriched response to user
```

## Notes

- This skill provides foundational knowledge for Foundry integration
- Adapt the examples to your specific use case and requirements
- Always test thoroughly in a development environment before production deployment
- Monitor agent performance and costs in the Foundry portal
