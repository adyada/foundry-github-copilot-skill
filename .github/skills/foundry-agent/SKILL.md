---
name: foundry-agent
description: >
  Enables GitHub Copilot to send user prompts to a Microsoft Foundry Agent for advanced Q&A, 
  complex reasoning, or data processing tasks that require specialized AI capabilities.
location: project
tools:
  - name: query_foundry_agent
    description: >
      Sends a user prompt to the Microsoft Foundry Agent endpoint for advanced AI processing.
      Use this when the user explicitly requests Foundry agent capabilities or when complex 
      reasoning beyond standard Copilot is needed.
    parameters:
      - name: prompt
        description: The user's question or request to send to the Foundry Agent
        type: string
        required: true
      - name: conversation_id
        description: Optional conversation ID for maintaining context across multiple requests
        type: string
        required: false
    implementation: python
---

# Foundry Agent Skill

This skill allows GitHub Copilot to interact with a Microsoft Foundry Agent application for tasks that require:
- Complex reasoning and analysis
- Advanced natural language understanding
- Specialized domain knowledge
- Integration with external data sources
- Custom AI workflows and processing

## When to Use

Use this skill when:
- The user explicitly mentions "Foundry" or "Foundry agent"
- The user's request requires advanced AI capabilities beyond standard Copilot functionality
- Complex data analysis or processing is needed
- Integration with Microsoft Foundry's specialized models is beneficial
- The task involves multi-step reasoning or orchestration

## Tool: query_foundry_agent

Sends a prompt to the configured Microsoft Foundry Agent endpoint.

### Parameters
- **prompt** (required): The user's question or request
- **conversation_id** (optional): Conversation ID for maintaining context

## Configuration

To use this skill, you need to:

1. **Set up Azure authentication**: The skill uses `DefaultAzureCredential` which supports multiple authentication methods:
   - Azure CLI: `az login`
   - Environment variables: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_SECRET`
   - Managed Identity (when running in Azure)
   - Visual Studio Code Azure account

2. **Configure the Foundry Agent endpoint** (optional):
   - Set `FOUNDRY_AGENT_ENDPOINT` environment variable to your Foundry Agent URL
   - If not set, uses the default endpoint shown in the implementation

3. **Install required Python packages**:
   ```bash
   pip install requests azure-identity
   ```

## Example Usage

In GitHub Copilot, you can invoke this skill by asking:
- "Use the Foundry agent to analyze this code"
- "Ask the Foundry agent what's new in Foundry"
- "Query the Foundry agent about cloud computing trends"

## Additional Resources

- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [GitHub Copilot Agent Skills Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Azure Identity Library](https://learn.microsoft.com/python/api/azure-identity/)
- [Foundry Agent Webapp Example](https://github.com/microsoft-foundry/foundry-agent-webapp)
