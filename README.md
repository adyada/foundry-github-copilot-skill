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

1. GitHub Copilot with Agent Skills support enabled
2. A Microsoft Foundry Agent endpoint deployed and accessible
3. API credentials (if required by your Foundry Agent)

### Installation

1. Clone this repository
2. Enable Agent Skills in VS Code:
   ```
   Set "chat.useAgentSkills": true in your VS Code settings
   ```
3. Configure environment variables:
   - `FOUNDRY_AGENT_ENDPOINT`: Your Foundry Agent endpoint URL
   - `FOUNDRY_AGENT_API_KEY`: Your API key (if authentication is required)

### Usage

Once installed and configured, GitHub Copilot will automatically detect when to use the Foundry Agent skill based on user prompts that require advanced AI capabilities.

Example interactions:
- "Use the Foundry agent to analyze this data"
- "Ask the Foundry agent about complex business logic"
- "Query the Foundry agent for specialized domain knowledge"

## Skill Implementation

The skill provides implementation examples in multiple languages:

- **Python**: Using the `requests` library
- **TypeScript/JavaScript**: Using `axios`
- **C#/.NET**: Using `HttpClient`

See `.github/skills/foundry-agent/SKILL.md` for complete code examples and documentation.

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
