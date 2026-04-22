# foundry-github-copilot-skill

This repository contains a GitHub Copilot Agent Skill that enables GitHub Copilot to call a Microsoft Foundry Agent application for advanced AI capabilities.

## Overview

The Foundry Agent Skill enables GitHub Copilot to interact with Microsoft Foundry Agent applications for:

- Complex reasoning and analysis
- Advanced natural language understanding
- Specialized domain knowledge integration
- Custom AI workflows and processing
- Multi-step task orchestration

## Installation

### Step 1: Copy the Skill to Your Repository

Copy the `.github/skills/foundry-agent/` folder to your target repository.

**macOS/Linux:**
```bash
# From your target repository
mkdir -p .github/skills
cp -r /path/to/foundry-github-copilot-skill/.github/skills/foundry-agent .github/skills/
```

**Windows (PowerShell):**
```powershell
# From your target repository
New-Item -ItemType Directory -Force -Path .github\skills
Copy-Item -Recurse -Path C:\path\to\foundry-github-copilot-skill\.github\skills\foundry-agent -Destination .github\skills\
```

Or manually copy these files to your repository:
```
your-repo/
└── .github/
    └── skills/
        └── foundry-agent/
            ├── SKILL.md
            └── query_foundry_agent.py
```

### Step 2: Install Python Dependencies

The skill requires Python 3.8+ and the following packages.

**macOS:**
```bash
# Install Python if needed (using Homebrew)
brew install python

# Install dependencies
pip3 install requests>=2.31.0 azure-identity>=1.15.0
```

**Windows:**
```powershell
# Install Python from https://www.python.org/downloads/ or using winget
winget install Python.Python.3.11

# Install dependencies
pip install requests>=2.31.0 azure-identity>=1.15.0
```

### Step 3: Install and Configure Azure CLI

**macOS:**
```bash
# Install Azure CLI using Homebrew
brew install azure-cli

# Sign in to Azure
az login
```

**Windows:**
```powershell
# Install Azure CLI using winget
winget install Microsoft.AzureCLI

# Or download from: https://aka.ms/installazurecliwindows

# Sign in to Azure
az login
```

### Step 4: Configure Azure Authentication

The skill uses Azure `DefaultAzureCredential` for secure, passwordless authentication. Choose one of these methods:

#### Option A: Azure CLI (Recommended for Development)
```bash
az login
```

#### Option B: Environment Variables (For CI/CD or Production)

**macOS/Linux:**
```bash
export AZURE_CLIENT_ID="your-client-id"
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_CLIENT_SECRET="your-client-secret"
```

**Windows (PowerShell):**
```powershell
$env:AZURE_CLIENT_ID = "your-client-id"
$env:AZURE_TENANT_ID = "your-tenant-id"
$env:AZURE_CLIENT_SECRET = "your-client-secret"
```

**Windows (Command Prompt):**
```cmd
set AZURE_CLIENT_ID=your-client-id
set AZURE_TENANT_ID=your-tenant-id
set AZURE_CLIENT_SECRET=your-client-secret
```

#### Option C: VS Code Azure Account
Sign in with your Azure account in VS Code (Settings > Accounts).

#### Option D: Managed Identity (For Azure-hosted environments)
No configuration needed if running in Azure with managed identity enabled.

### Step 5: Configure Your Foundry Agent Endpoint

Set the `FOUNDRY_AGENT_ENDPOINT` environment variable to point to your Foundry Agent.

**macOS/Linux:**
```bash
export FOUNDRY_AGENT_ENDPOINT="https://your-project.services.ai.azure.com/api/projects/your-project/applications/your-agent/protocols/openai/responses?api-version=2025-11-15-preview"
```

**Windows (PowerShell):**
```powershell
$env:FOUNDRY_AGENT_ENDPOINT = "https://your-project.services.ai.azure.com/api/projects/your-project/applications/your-agent/protocols/openai/responses?api-version=2025-11-15-preview"
```

**Windows (Command Prompt):**
```cmd
set FOUNDRY_AGENT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project/applications/your-agent/protocols/openai/responses?api-version=2025-11-15-preview
```

> **Note:** If not set, the skill uses a default test endpoint which may not be accessible.
>
> **Tip:** To persist environment variables, add them to your shell profile (`~/.zshrc` or `~/.bashrc` on macOS/Linux) or set them as System Environment Variables on Windows.

## Configuration Reference

| Environment Variable | Required | Description |
|---------------------|----------|-------------|
| `FOUNDRY_AGENT_ENDPOINT` | Yes | Your Microsoft Foundry Agent endpoint URL |
| `AZURE_CLIENT_ID` | Conditional | Azure service principal client ID (if not using Azure CLI) |
| `AZURE_TENANT_ID` | Conditional | Azure tenant ID (if not using Azure CLI) |
| `AZURE_CLIENT_SECRET` | Conditional | Azure service principal secret (if not using Azure CLI) |

## Skill Structure

```
.github/skills/foundry-agent/
├── SKILL.md                    # Skill definition and metadata
└── query_foundry_agent.py      # Python implementation
```

## Usage

Once installed and configured, the Foundry Agent skill is automatically available in GitHub Copilot.

### Invoking the Skill

Invoke the skill by mentioning "Foundry" or "Foundry agent" in your Copilot prompts:

```
"Use the Foundry agent to analyze this code"
"Ask the Foundry agent what's new in Microsoft Foundry"
"Query the Foundry agent about cloud architecture best practices"
"Call the Foundry agent to explain this algorithm"
```

### How It Works

1. **You make a request** in GitHub Copilot mentioning the Foundry agent
2. **Copilot detects the intent** and loads the `foundry-agent` skill
3. **The skill authenticates** using Azure DefaultAzureCredential
4. **Sends your prompt** to the configured Foundry Agent endpoint
5. **Returns the response** from the Foundry Agent back to you in Copilot

## Verifying Your Setup

Test that everything is configured correctly.

**macOS/Linux:**
```bash
# Test Azure authentication
az account show

# Test Python dependencies
python3 -c "import requests; from azure.identity import DefaultAzureCredential; print('Dependencies OK')"

# Test the skill with the example script
python3 examples/python_example.py "Hello, Foundry Agent!"
```

**Windows:**
```powershell
# Test Azure authentication
az account show

# Test Python dependencies
python -c "import requests; from azure.identity import DefaultAzureCredential; print('Dependencies OK')"

# Test the skill with the example script
python examples/python_example.py "Hello, Foundry Agent!"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `DefaultAzureCredential` authentication failed | Run `az login` or check environment variables |
| Connection timeout | Verify `FOUNDRY_AGENT_ENDPOINT` is accessible |
| 401 Unauthorized | Ensure your Azure identity has access to the Foundry Agent |
| Module not found | Run `pip install requests azure-identity` |

## Key Features

- **Azure Authentication**: Uses `DefaultAzureCredential` for secure, passwordless authentication
- **Configurable Endpoint**: Support for custom Foundry Agent endpoints via environment variable
- **Error Handling**: Robust error handling with descriptive error messages
- **Conversation Context**: Optional conversation ID parameter for multi-turn conversations
- **Timeout Protection**: 120-second timeout to prevent hanging requests

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Resources

- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [GitHub Copilot Agent Skills Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Foundry Agent Webapp Example](https://github.com/microsoft-foundry/foundry-agent-webapp)

## License

See LICENSE file for details.
