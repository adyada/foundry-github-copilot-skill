# Architecture Overview

## How the Foundry Agent Skill Works

```
┌─────────────────────────────────────────────────────────────────┐
│                          User in VS Code                         │
│                                                                   │
│  "Use the Foundry agent to analyze this data..."                │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ User prompt
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GitHub Copilot                              │
│                                                                   │
│  • Detects intent matches Foundry Agent skill                   │
│  • Loads .github/skills/foundry-agent/SKILL.md                  │
│  • Determines appropriate action                                │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ Invokes skill
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              Foundry Agent Skill (SKILL.md)                      │
│                                                                   │
│  • Extracts user prompt                                         │
│  • Executes implementation code (Python/TS/C#)                  │
│  • Formats request payload                                      │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ HTTP POST request
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│            Microsoft Foundry Agent Endpoint                      │
│              (Azure AI Foundry Service)                          │
│                                                                   │
│  • Receives prompt: { "message": "...", "conversation_id": ... }│
│  • Processes with specialized AI models                         │
│  • Returns response with analysis/results                       │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ JSON response
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              Foundry Agent Skill (Response)                      │
│                                                                   │
│  • Receives agent response                                      │
│  • Parses and formats result                                    │
│  • Returns to Copilot                                           │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ Formatted response
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GitHub Copilot                              │
│                                                                   │
│  • Displays result in chat                                      │
│  • Provides context for follow-up questions                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ Display to user
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                          User in VS Code                         │
│                                                                   │
│  "The analysis shows..."                                        │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. SKILL.md Definition
- Located at: `.github/skills/foundry-agent/SKILL.md`
- Contains: Skill metadata, description, usage instructions, implementation code
- Format: YAML frontmatter + Markdown content

### 2. Example Implementations

#### Python (`examples/python_example.py`)
- Uses: `requests` library
- Features: Error handling, authentication, conversation context
- Run: `python examples/python_example.py "your prompt"`

#### TypeScript (`examples/typescript_example.ts`)
- Uses: `axios` library  
- Features: Type safety, async/await, error handling
- Run: `npx ts-node examples/typescript_example.ts "your prompt"`

### 3. Configuration
Environment variables:
- `FOUNDRY_AGENT_ENDPOINT`: The Foundry Agent URL
- `FOUNDRY_AGENT_API_KEY`: Optional API key for authentication

## Request/Response Flow

### Request Format
```json
{
  "message": "User's prompt or question",
  "conversation_id": "optional-uuid-for-context"
}
```

### Response Format
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

1. **API Key Management**: Store keys in environment variables, never in code
2. **HTTPS Only**: All communication uses encrypted HTTPS
3. **Timeout Limits**: Prevents indefinite hanging requests
4. **Input Validation**: Sanitize user inputs before sending to agent
5. **Error Messages**: Don't expose sensitive information in error messages

## Testing

### Without Foundry Agent
Run examples with default endpoint to see error handling:
```bash
python examples/python_example.py
```

### With Foundry Agent
Configure environment and run:
```bash
export FOUNDRY_AGENT_ENDPOINT="https://your-endpoint.azure.com/chat"
export FOUNDRY_AGENT_API_KEY="your-key"
python examples/python_example.py "Test prompt"
```

## Integration with GitHub Copilot

1. **Enable Skills**: Set `chat.useAgentSkills: true` in VS Code settings
2. **Skill Detection**: Copilot automatically loads skills from `.github/skills/`
3. **Intent Matching**: Copilot uses skill name and description to determine when to invoke
4. **Execution**: Copilot executes the appropriate implementation code
5. **Response**: Results are displayed in the Copilot chat interface

## Extending the Skill

To customize the skill:

1. **Modify SKILL.md**: Update description, usage instructions, or implementation
2. **Add Languages**: Include additional implementation examples (Java, Go, etc.)
3. **Enhance Features**: Add streaming, file attachments, or multimodal support
4. **Custom Parameters**: Extend request payload with additional fields

## Resources

- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [GitHub Copilot Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Foundry Agent Webapp Example](https://github.com/microsoft-foundry/foundry-agent-webapp)
