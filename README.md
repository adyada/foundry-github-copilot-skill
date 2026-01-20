# Foundry GitHub Copilot Skill

A GitHub Copilot skill that demonstrates how to integrate and call Microsoft Foundry agent applications using REST APIs.

## Overview

This repository contains a complete example of a GitHub Copilot skill for Microsoft Foundry agent integration. It includes:

- **Skill Definition**: A properly formatted `SKILL.md` file with YAML frontmatter
- **Python Example**: Complete Python implementation with Azure SDK
- **TypeScript Example**: Complete TypeScript/JavaScript implementation with REST API
- **Configuration Templates**: Environment variable setup and dependency management
- **Best Practices**: Authentication, error handling, and security guidelines

## What is a GitHub Copilot Skill?

GitHub Copilot skills are structured bundles of instructions, scripts, and resources that teach Copilot domain-specific capabilities. This skill helps developers integrate Microsoft Foundry AI agents into their applications.

## Skill Location

The skill is located in `.github/skills/foundry-agent/` directory and includes:

- `SKILL.md` - Main skill definition with instructions
- `example_python.py` - Python implementation example
- `example_typescript.ts` - TypeScript implementation example
- `requirements.txt` - Python dependencies
- `package.json` - Node.js dependencies
- `.env.example` - Environment configuration template

## Quick Start

### Prerequisites

- Microsoft Foundry project with a published agent
- Azure credentials for authentication
- Python 3.8+ or Node.js 18+ (depending on your choice)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/adyada/foundry-github-copilot-skill.git
   cd foundry-github-copilot-skill
   ```

2. **Navigate to the skill directory:**
   ```bash
   cd .github/skills/foundry-agent
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Foundry endpoint and deployment name
   ```

### Running Python Example

```bash
# Install dependencies
pip install -r requirements.txt

# Run the example
python example_python.py
```

### Running TypeScript Example

```bash
# Install dependencies
npm install

# Run the example
npm start
```

## Environment Variables

Set these environment variables before running the examples:

```bash
AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project
AZURE_AI_MODEL_DEPLOYMENT_NAME=your-deployment-name
```

For Azure authentication, ensure you're logged in via Azure CLI:
```bash
az login
```

## Features Demonstrated

### 1. Simple Agent Calls
- Single-turn question-answer interactions
- Basic request/response handling
- Error handling and logging

### 2. Streaming Responses
- Real-time streaming for long-running operations
- Progressive response display
- Improved user experience for interactive applications

### 3. Multi-Turn Conversations
- Stateful conversations with context preservation
- Conversation ID management
- Building contextual AI interactions

## Integration Patterns

This skill demonstrates multiple integration patterns:

1. **REST API Integration** - Direct API calls with full control
2. **SDK-Based Integration** - Using Azure AI SDK for simplified development
3. **Authentication** - DefaultAzureCredential, API keys, and managed identity
4. **Error Handling** - Retry logic and graceful failure handling
5. **Security** - Best practices for credentials and secret management

## Using This Skill with GitHub Copilot

When you have this skill in your repository, GitHub Copilot can:

- Reference the skill when you ask about Foundry integration
- Use the examples as templates for generating code
- Follow the best practices outlined in the skill
- Help you implement similar agent integrations

To invoke the skill, you can ask Copilot questions like:
- "How do I call a Microsoft Foundry agent?"
- "Show me an example of Foundry agent integration"
- "What's the best way to authenticate with Foundry?"

## Documentation

For detailed information, see:

- **Skill Documentation**: `.github/skills/foundry-agent/SKILL.md`
- [Microsoft Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [GitHub Copilot Skills Documentation](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)

## Security Best Practices

- Never commit API keys or secrets to source control
- Use environment variables or Azure Key Vault for configuration
- Implement DefaultAzureCredential for production deployments
- Use managed identities when running on Azure
- Rotate API keys regularly
- Apply proper RBAC to Foundry resources

## Contributing

This is an example repository demonstrating GitHub Copilot skill structure. Feel free to:

- Fork and adapt for your own Foundry agents
- Add additional examples and use cases
- Improve documentation and error handling
- Share feedback and suggestions

## License

MIT License - See LICENSE file for details

## Additional Resources

- [Integrate Microsoft Foundry with Applications](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/integrate-with-other-apps)
- [Publish Agents in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/publish-agent)
- [Azure AI SDK Documentation](https://learn.microsoft.com/en-us/python/api/overview/azure/ai)
- [GitHub Copilot Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
