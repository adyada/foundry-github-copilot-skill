# Getting Started with Microsoft Foundry Agent Integration

This guide will walk you through setting up and using the Microsoft Foundry agent integration examples.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup Microsoft Foundry](#setup-microsoft-foundry)
3. [Configure the Examples](#configure-the-examples)
4. [Running Python Example](#running-python-example)
5. [Running TypeScript Example](#running-typescript-example)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required

- **Azure Subscription**: You need an active Azure subscription
- **Microsoft Foundry Project**: A Foundry project with at least one published agent
- **Azure CLI**: For authentication (recommended)
  ```bash
  curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
  ```

### For Python Examples

- Python 3.8 or higher
- pip package manager

### For TypeScript Examples

- Node.js 18 or higher
- npm package manager

## Setup Microsoft Foundry

### Step 1: Create a Foundry Project

1. Go to [Azure Portal](https://portal.azure.com)
2. Search for "AI Foundry" (or "Azure AI")
3. Create a new AI Foundry project:
   - Click "Create"
   - Choose your subscription and resource group
   - Set a project name
   - Choose a region
   - Click "Review + Create"

### Step 2: Create and Publish an Agent

1. In your Foundry project, navigate to "Agents"
2. Click "Create new agent"
3. Configure your agent:
   - Choose a model (e.g., GPT-4, GPT-4o)
   - Set system instructions
   - Add any tools or capabilities
4. Test your agent in the playground
5. Click "Publish" to make it available via API
6. Note the deployment name - you'll need this later

### Step 3: Get Your Project Endpoint

1. In your Foundry project, go to "Settings" or "Overview"
2. Find your project endpoint URL
   - It should look like: `https://{resource}.services.ai.azure.com/api/projects/{projectname}`
3. Copy this URL - you'll need it for configuration

## Configure the Examples

### Step 1: Clone the Repository

```bash
git clone https://github.com/adyada/foundry-github-copilot-skill.git
cd foundry-github-copilot-skill/.github/skills/foundry-agent
```

### Step 2: Set Up Environment Variables

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit the `.env` file and add your values:

```bash
# Required: Your Foundry project endpoint
AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com

# Required: Your agent ID
AZURE_AGENT_ID=your-agent-id
```

### Step 3: Authenticate with Azure

Use Azure CLI to authenticate (recommended):

```bash
az login
```

This will open a browser for authentication. Once complete, the examples will use your Azure credentials automatically via DefaultAzureCredential.

Alternatively, you can use environment variables for service principal authentication:

```bash
export AZURE_TENANT_ID=your-tenant-id
export AZURE_CLIENT_ID=your-client-id
export AZURE_CLIENT_SECRET=your-client-secret
```

## Running Python Example

### Step 1: Install Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Run the Example

```bash
python example_python.py
```

The script will run three examples:
1. Simple agent call
2. Streaming response
3. Multi-turn conversation

### Step 3: Verify Output

You should see output like:

```
Microsoft Foundry Agent Integration Examples
============================================================
✓ Connected to Foundry project: https://...

============================================================
Example 1: Simple Agent Call
============================================================

→ Sending message: What is Microsoft Foundry...
✓ Received response

Agent Response:
Microsoft Foundry is a...

✓ Example completed successfully
...
```

## Running TypeScript Example

### Step 1: Install Dependencies

```bash
npm install
```

### Step 2: Run the Example

```bash
# Using npm script
npm start

# Or directly with ts-node
npx ts-node example_typescript.ts
```

### Step 3: Verify Output

Similar to Python, you should see three examples execute successfully.

## Troubleshooting

### Error: "AZURE_AI_PROJECT_ENDPOINT must be set"

**Solution**: Make sure your `.env` file exists and contains the correct endpoint URL.

```bash
# Check if .env file exists
ls -la .env

# Verify environment variables are loaded
cat .env
```

### Error: "Failed to acquire access token"

**Solutions**:

1. **Ensure you're logged in to Azure:**
   ```bash
   az login
   az account show
   ```

2. **Verify your Azure subscription is active:**
   ```bash
   az account list --output table
   ```

3. **Check you have permissions on the Foundry project:**
   - You need at least "Cognitive Services User" role
   - Add role in Azure Portal → Your AI Foundry project → Access control (IAM)

### Error: "Agent call failed: 404"

**Solutions**:

1. **Verify the deployment name is correct:**
   - Check in Foundry portal under "Agents" → "Deployments"
   - The deployment name is case-sensitive

2. **Ensure the agent is published:**
   - The agent must be in "Published" state, not just saved

3. **Check the endpoint URL:**
   - Ensure it includes the full path: `/api/projects/{projectname}`

### Error: "Module not found" (Python)

**Solution**: Ensure you've activated your virtual environment and installed dependencies:

```bash
# Activate venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Error: "Cannot find module" (TypeScript)

**Solution**: Reinstall node modules:

```bash
rm -rf node_modules package-lock.json
npm install
```

### Slow Response Times

**Possible Causes**:
- The agent model is large (e.g., GPT-4)
- Complex agent instructions or tools
- Network latency to Azure region

**Solutions**:
- Use streaming responses for better user experience
- Consider using a faster model for testing
- Deploy your app in the same Azure region as Foundry

### Rate Limiting Errors

**Solution**: Implement retry logic with exponential backoff:

```python
import time
from azure.core.exceptions import HttpResponseError

max_retries = 3
for attempt in range(max_retries):
    try:
        response = client.send_message(message)
        break
    except HttpResponseError as e:
        if e.status_code == 429:  # Too Many Requests
            wait_time = 2 ** attempt
            time.sleep(wait_time)
        else:
            raise
```

## Next Steps

Once you have the examples working:

1. **Customize the examples** for your specific use case
2. **Add error handling** and retry logic for production
3. **Implement logging** for monitoring and debugging
4. **Add unit tests** for your integration code
5. **Review security best practices** in the main SKILL.md file
6. **Explore advanced features** like external API tools and function calling

## Getting Help

If you encounter issues:

1. Check the [Microsoft Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
2. Review the detailed SKILL.md file in this directory
3. Check Azure service health and status
4. Review your Azure subscription limits and quotas

## Additional Resources

- [Azure AI SDK for Python](https://learn.microsoft.com/en-us/python/api/overview/azure/ai)
- [Azure Identity Documentation](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme)
- [Microsoft Foundry Integration Guide](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/integrate-with-other-apps)
