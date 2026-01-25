# Foundry GitHub Copilot Skill

A GitHub Copilot skill that connects to Microsoft Foundry Agent applications.

## Requirements

- Python 3.8+
- Azure CLI installed

## Setup

### 1. Copy skill to your repository

```
your-repo/.github/skills/foundry-agent/
├── SKILL.md
└── query_foundry_agent.py
```

### 2. Configure endpoint

Create a `.env` file in the skill directory or set the environment variable:

```bash
FOUNDRY_AGENT_APPLICATION_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project/applications/your-agent/protocols/openai/responses?api-version=2025-11-15-preview
```

> **Note:** Python dependencies and Azure authentication are handled automatically on first run.

## Usage

Invoke by mentioning "Foundry" in your prompts:

- "Ask Foundry to analyze this code"
- "Query Foundry about best practices"
- "Use the Foundry agent to review this"

## Resources

- [Microsoft Foundry Docs](https://learn.microsoft.com/azure/ai-foundry/)
- [Copilot Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
