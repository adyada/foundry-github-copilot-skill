# Architecture Overview

## How the Foundry Agent Skill Works

```
┌─────────────────────────────────────────────────────────────────┐
│                     User in GitHub Copilot                       │
│                                                                   │
│  "Use the Foundry agent to analyze this code..."                │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ User prompt with "Foundry" keyword
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GitHub Copilot CLI                          │
│                                                                   │
│  • Detects "foundry-agent" skill intent                         │
│  • Loads .github/skills/foundry-agent/SKILL.md                  │
│  • Invokes query_foundry_agent tool                             │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ Executes Python implementation
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              Foundry Agent Skill (Python)                        │
│                                                                   │
│  • Authenticates with DefaultAzureCredential                    │
│  • Gets access token for https://ai.azure.com                   │
│  • Formats request: { "input": "prompt" }                       │
│  • Sends POST to Foundry Agent endpoint                         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ HTTPS POST with Bearer token
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│            Microsoft Foundry Agent Endpoint                      │
│              (Azure AI Foundry Service)                          │
│                                                                   │
│  • Validates authentication token                               │
│  • Processes prompt with AI models                              │
│  • Returns JSON response with results                           │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ JSON response
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              Foundry Agent Skill (Response)                      │
│                                                                   │
│  • Receives agent response                                      │
│  • Returns to Copilot CLI                                       │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ Formatted response
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GitHub Copilot CLI                          │
│                                                                   │
│  • Displays result in chat                                      │
│  • Ready for follow-up questions                                │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ Display to user
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                     User in GitHub Copilot                       │
│                                                                   │
│  "The Foundry agent says..."                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. SKILL.md Definition
- Located at: `.github/skills/foundry-agent/SKILL.md`
- Contains: 
  - YAML frontmatter with tool definition (`query_foundry_agent`)
  - Python implementation using `requests` and `azure-identity`
  - Configuration instructions
  - Usage examples

### 2. Tool: query_foundry_agent
- **Parameters**:
  - `prompt` (required): User's question or request
  - `conversation_id` (optional): For maintaining conversation context
- **Authentication**: Uses Azure `DefaultAzureCredential`
- **Endpoint**: Configurable via `FOUNDRY_AGENT_ENDPOINT` environment variable
- **Timeout**: 120 seconds

### 3. Example Implementations

#### Python (`examples/python_example.py`)
- Full client implementation with `FoundryAgentClient` class
- Uses: `requests` library and `azure-identity`
- Features: Token refresh, error handling, conversation context
- Run: `python examples/python_example.py "your prompt"`

#### TypeScript (`examples/typescript_example.ts`)
- Full client implementation with `FoundryAgentClient` class
- Uses: `axios` library  
- Features: Type safety, async/await, error handling
- Run: `npx ts-node examples/typescript_example.ts "your prompt"`

### 4. Configuration
Required Python packages (see `requirements.txt`):
- `requests>=2.31.0` - HTTP client
- `azure-identity>=1.15.0` - Azure authentication

Environment variables:
- `FOUNDRY_AGENT_ENDPOINT`: Optional custom endpoint URL
- Azure authentication (one of):
  - Azure CLI: `az login`
  - Environment variables: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_SECRET`
  - Managed Identity (when running in Azure)
  - VS Code Azure account

## Request/Response Flow

### Request Format
The skill sends requests to the Foundry Agent endpoint in the following format:
```json
{
  "input": "User's prompt or question",
  "previous_response_id": "optional-conversation-id"
}
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <azure-access-token>
```

### Response Format
The Foundry Agent returns responses in this format:
```json
{
  "response": "Agent's generated response",
  "conversation_id": "uuid-for-context",
  "metadata": {
    "model": "foundry-model-name",
    "tokens": 150
  }
}
```

## Error Handling

The skill handles:
- **Connection Errors**: Network issues, unreachable endpoint
- **HTTP Errors**: 4xx client errors, 5xx server errors
- **Timeout Errors**: Requests exceeding 30 seconds
- **Authentication Errors**: Invalid or missing API keys
- **Parse Errors**: Invalid JSON responses

## Security Considerations

1. **Azure Authentication**: Uses Azure `DefaultAzureCredential` for secure, passwordless authentication
   - No API keys or secrets stored in code or environment variables
   - Leverages Azure AD token-based authentication
   - Supports managed identities for Azure-hosted applications

2. **Token Management**: 
   - Access tokens are obtained fresh for each request
   - Tokens have limited lifetime and are automatically refreshed
   - Bearer token authentication via HTTPS only

3. **HTTPS Only**: All communication uses encrypted HTTPS
4. **Timeout Limits**: 120-second timeout prevents indefinite hanging requests
5. **Input Validation**: User prompts are sent as-is to the Foundry Agent endpoint
6. **Error Messages**: Errors include endpoint information but no sensitive authentication details

## Testing

### Testing Without a Foundry Agent Endpoint
Run the example scripts without configuration to see error handling:
```bash
# Test Python example
python examples/python_example.py "Test prompt"

# This will attempt to authenticate and call the default endpoint
# If authentication fails or endpoint is unreachable, you'll see appropriate error messages
```

### Testing With Your Own Foundry Agent
1. **Set up Azure authentication**:
   ```bash
   az login
   ```

2. **Configure your endpoint** (optional):
   ```bash
   export FOUNDRY_AGENT_ENDPOINT="https://your-endpoint.azure.com/api/..."
   ```

3. **Test with Python example**:
   ```bash
   python examples/python_example.py "What are the latest AI trends?"
   ```

4. **Test with TypeScript example**:
   ```bash
   npm install  # from examples/ directory
   npx ts-node typescript_example.ts "Explain quantum computing"
   ```

### Testing the GitHub Copilot Skill
1. Ensure you're in a repository with the skill installed
2. Open GitHub Copilot chat
3. Try: "Use the Foundry agent to explain microservices architecture"
4. Copilot should invoke the skill and return the Foundry Agent's response

## Integration with GitHub Copilot

### How Copilot Loads Skills
1. **Skill Detection**: Copilot automatically loads skills from `.github/skills/` directory
2. **Metadata Parsing**: Reads YAML frontmatter to understand skill capabilities
3. **Tool Registration**: Registers the `query_foundry_agent` tool
4. **Intent Matching**: Uses skill name and description to determine when to invoke

### Skill Invocation Process
1. **User mentions "Foundry" or "Foundry agent"** in their prompt
2. **Copilot matches intent** to the `foundry-agent` skill
3. **Copilot calls `query_foundry_agent`** with the user's prompt
4. **Python code executes**:
   - Authenticates with Azure
   - Calls Foundry Agent endpoint
   - Returns response
5. **Copilot displays result** in the chat interface

### Requirements
- GitHub Copilot CLI or VS Code with Copilot
- Skill must be in `.github/skills/foundry-agent/SKILL.md`
- Python runtime available with required packages installed
- Azure authentication configured

## Extending the Skill

To customize or extend the skill:

1. **Modify Request/Response Format**: 
   - Edit the Python implementation in SKILL.md
   - Update payload structure in lines 76-81
   - Adjust response parsing as needed

2. **Add New Parameters**: 
   - Add parameters to the tool definition in YAML frontmatter
   - Update Python code to use the new parameters
   - Document in the Configuration section

3. **Enhance Error Handling**: 
   - Extend the try/except block (lines 84-96)
   - Add specific error cases
   - Improve error messages

4. **Add TypeScript/Node.js Support**:
   - Add `implementation: typescript` or `implementation: javascript` to tool definition
   - Include TypeScript/JavaScript code instead of Python
   - Update documentation accordingly

5. **Support Multiple Endpoints**:
   - Add endpoint selection logic
   - Support different Foundry Agent types
   - Route requests based on prompt analysis

6. **Add Streaming Support**:
   - Modify to use streaming API endpoints
   - Yield partial responses
   - Update response format

7. **Add Conversation Memory**:
   - Store conversation IDs persistently
   - Track conversation history
   - Enable multi-turn conversations

## Resources

- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [GitHub Copilot Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Foundry Agent Webapp Example](https://github.com/microsoft-foundry/foundry-agent-webapp)
