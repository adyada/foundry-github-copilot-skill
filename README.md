# foundry-github-copilot-skill

This repository contains a GitHub Copilot Agent Skill example that demonstrates how to call a Microsoft Foundry Agent application from within GitHub Copilot.

## Overview

The Foundry Agent Skill enables GitHub Copilot to interact with Microsoft Foundry Agent applications for advanced AI capabilities, including:

- Complex reasoning and analysis
- Advanced natural language understanding
- Specialized domain knowledge integration
- Custom AI workflows and processing
- Multi-step task orchestration

## Skill Structure

The skill is defined in `.github/skills/foundry-agent/SKILL.md` following the GitHub Copilot Agent Skills specification.

## Getting Started

### Prerequisites

1. **GitHub Copilot** with Agent Skills support enabled
2. **Python 3.8+** installed
3. **Azure authentication** configured (Azure CLI, environment variables, or managed identity)
4. **Microsoft Foundry Agent** endpoint deployed and accessible (optional - uses default if not configured)

### Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/foundry-github-copilot-skill.git
   cd foundry-github-copilot-skill
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Azure authentication** (choose one method):
   - **Azure CLI** (recommended for development):
     ```bash
     az login
     ```
   - **Environment variables**:
     ```bash
     export AZURE_CLIENT_ID="your-client-id"
     export AZURE_TENANT_ID="your-tenant-id"
     export AZURE_CLIENT_SECRET="your-client-secret"
     ```
   - **VS Code**: Sign in with your Azure account

4. **Configure Foundry Agent endpoint** (optional):
   ```bash
   export FOUNDRY_AGENT_ENDPOINT="https://your-endpoint.azure.com/api/..."
   ```
   If not set, the skill uses a default test endpoint.

### Usage

Once installed and configured, the Foundry Agent skill is automatically available in GitHub Copilot.

#### Invoking the Skill

You can invoke the skill by mentioning "Foundry" or "Foundry agent" in your Copilot prompts:

- "Use the Foundry agent to analyze this code"
- "Ask the Foundry agent what's new in Microsoft Foundry"
- "Query the Foundry agent about cloud architecture best practices"
- "Call the Foundry agent to explain this algorithm"

#### How It Works

1. **You make a request** in GitHub Copilot mentioning the Foundry agent
2. **Copilot detects the intent** and loads the `foundry-agent` skill
3. **The skill authenticates** using Azure DefaultAzureCredential
4. **Sends your prompt** to the configured Foundry Agent endpoint
5. **Returns the response** from the Foundry Agent back to you in Copilot

## Skill Implementation

The skill is implemented as a GitHub Copilot Agent Skill located in `.github/skills/foundry-agent/SKILL.md`.

### Key Features

- **Azure Authentication**: Uses `DefaultAzureCredential` for secure, passwordless authentication
- **Configurable Endpoint**: Support for custom Foundry Agent endpoints via environment variable
- **Error Handling**: Robust error handling with descriptive error messages
- **Conversation Context**: Optional conversation ID parameter for multi-turn conversations
- **Timeout Protection**: 120-second timeout to prevent hanging requests

## How It Works

1. User makes a request in GitHub Copilot
2. Copilot detects the request matches the Foundry Agent skill
3. The skill sends the prompt to the configured Foundry Agent endpoint
4. The Foundry Agent processes the request and returns a response
5. Copilot displays the response to the user

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Resources

- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [GitHub Copilot Agent Skills Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Foundry Agent Webapp Example](https://github.com/microsoft-foundry/foundry-agent-webapp)

## License

See LICENSE file for details.
