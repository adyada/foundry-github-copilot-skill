# Foundry Agent Examples

This directory contains practical examples demonstrating how to call Microsoft Foundry Agent applications from different programming languages.

## Available Examples

### Python Example (`python_example.py`)

A Python implementation using the `requests` library.

**Prerequisites:**
```bash
pip install requests
```

**Usage:**
```bash
# Set environment variables
export FOUNDRY_AGENT_ENDPOINT="https://your-foundry-endpoint.azure.com/chat"
export FOUNDRY_AGENT_API_KEY="your-api-key"

# Run with example prompts
python examples/python_example.py

# Run with custom prompt
python examples/python_example.py "What are the latest AI trends?"
```

### TypeScript Example (`typescript_example.ts`)

A TypeScript implementation using `axios`.

**Prerequisites:**
```bash
npm install axios
npm install --save-dev @types/node typescript ts-node
```

**Usage:**
```bash
# Set environment variables
export FOUNDRY_AGENT_ENDPOINT="https://your-foundry-endpoint.azure.com/chat"
export FOUNDRY_AGENT_API_KEY="your-api-key"

# Run with ts-node
npx ts-node examples/typescript_example.ts

# Run with custom prompt
npx ts-node examples/typescript_example.ts "What are the latest AI trends?"
```

## Configuration

Both examples support the following environment variables:

- `FOUNDRY_AGENT_ENDPOINT`: The URL of your Microsoft Foundry Agent endpoint (required)
- `FOUNDRY_AGENT_API_KEY`: The API key for authentication (optional, depends on your setup)

## Features

All examples include:

- ✅ Environment variable configuration
- ✅ Proper error handling
- ✅ Timeout management
- ✅ Authentication support
- ✅ Conversation context tracking (optional)
- ✅ Command-line interface
- ✅ Example prompts for testing

## Error Handling

The examples handle common error scenarios:

- HTTP errors (4xx, 5xx)
- Connection errors
- Timeout errors
- Invalid JSON responses

## Testing Without a Foundry Agent

If you don't have a Foundry Agent endpoint set up yet, the examples will:
1. Use a placeholder endpoint
2. Show connection errors (expected behavior)
3. Demonstrate the structure of requests and responses

This allows you to:
- Review the code structure
- Understand the API interface
- Prepare your integration before the endpoint is ready

## Next Steps

1. Deploy a Microsoft Foundry Agent (see [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/))
2. Configure your endpoint URL and API key
3. Run the examples to test your integration
4. Integrate the code into your GitHub Copilot skill workflow
