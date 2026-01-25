---
name: foundry-agent
description: Enables GitHub Copilot to send user prompts to a Microsoft Foundry Agent for advanced Q&A,  complex reasoning, or data processing tasks that require specialized AI capabilities. USE THIS SKILL when the user explicitly mentions "Foundry", "Foundry agent", "ask Foundry", "query Foundry", or "use Foundry". Trigger phrases include "ask the Foundry agent", "use Foundry to", "query Foundry about", "Foundry agent", "send to Foundry", "have Foundry analyze", "let Foundry handle".
---

# Foundry Agent

This skill connects GitHub Copilot to a Microsoft Foundry Agent for tasks requiring advanced AI capabilities, complex reasoning, specialized domain knowledge, or integration with external data sources.

## CRITICAL: When to Use This Skill

**USE Foundry Agent for specialized AI tasks.** If the request requires advanced reasoning or Foundry-specific capabilities, use this skill.

**ALWAYS use Foundry Agent when the user asks about:**

| User Question Pattern | Example | Action |
|-----------------------|---------|--------|
| Explicit Foundry request | "Use the Foundry agent to analyze this" | `query_foundry_agent` |
| Ask Foundry | "Ask Foundry about best practices" | `query_foundry_agent` |
| Query Foundry | "Query Foundry about this architecture" | `query_foundry_agent` |
| Send to Foundry | "Send this to Foundry for analysis" | `query_foundry_agent` |
| Have Foundry analyze | "Have Foundry analyze this code" | `query_foundry_agent` |
| Foundry agent tasks | "Let the Foundry agent handle this" | `query_foundry_agent` |

**When in doubt about complex AI tasks, use Foundry Agent.** It provides advanced capabilities beyond standard Copilot.

## Configuration

Authentication uses `DefaultAzureCredential` which supports Azure CLI (`az login`), environment variables, Managed Identity, or VS Code Azure account. Set `FOUNDRY_AGENT_APPLICATION_ENDPOINT` environment variable to your Foundry Agent URL.

## MCP Tool

Use the `query_foundry_agent` MCP tool to send prompts to the Foundry Agent. The tool accepts a `prompt` parameter and optional `conversation_id`.

| Tool | Parameters |
|------|------------|
| `query_foundry_agent` | `{ "prompt": "<your question>", "conversation_id": "<optional>" }` |

## Quick Start

Query the Foundry Agent using the MCP tool:

| Tool | Parameters |
|------|------------|
| `query_foundry_agent` | `{ "prompt": "What's new in Microsoft Foundry?" }` |

## Common Use Cases

### Code Analysis and Review

| Tool | Parameters |
|------|------------|
| `query_foundry_agent` | `{ "prompt": "Analyze this code for potential improvements" }` |
| `query_foundry_agent` | `{ "prompt": "Review the architecture of this system" }` |
| `query_foundry_agent` | `{ "prompt": "Identify security concerns in this implementation" }` |

**User prompts that trigger these:**
- "Ask Foundry to analyze this code for improvements"
- "Have Foundry review the architecture"
- "Use Foundry to identify security concerns"

### Advanced Q&A

| Tool | Parameters |
|------|------------|
| `query_foundry_agent` | `{ "prompt": "Explain the benefits of microservices architecture" }` |
| `query_foundry_agent` | `{ "prompt": "What are best practices for Azure deployments?" }` |
| `query_foundry_agent` | `{ "prompt": "Compare different caching strategies" }` |

**User prompts that trigger these:**
- "Ask the Foundry agent about microservices benefits"
- "Query Foundry about Azure deployment best practices"
- "Have Foundry compare caching strategies"

### Data Processing

| Tool | Parameters |
|------|------------|
| `query_foundry_agent` | `{ "prompt": "Summarize the key findings from this data" }` |
| `query_foundry_agent` | `{ "prompt": "Analyze trends in this dataset" }` |
| `query_foundry_agent` | `{ "prompt": "Extract insights from these logs" }` |

**User prompts that trigger these:**
- "Send this data to Foundry to summarize"
- "Use Foundry to analyze trends in this dataset"
- "Ask Foundry to extract insights from these logs"

### Multi-turn Conversations

| Tool | Parameters |
|------|------------|
| `query_foundry_agent` | `{ "prompt": "Let's discuss system design", "conversation_id": "design-session-1" }` |
| `query_foundry_agent` | `{ "prompt": "Now let's focus on scalability", "conversation_id": "design-session-1" }` |

**User prompts that trigger these:**
- "Ask Foundry to help me with system design"
- "Continue the Foundry conversation about scalability"

## MCP Tool Reference

### query_foundry_agent

Sends a prompt to the configured Microsoft Foundry Agent endpoint for advanced AI processing.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | The user's question or request to send to the Foundry Agent |
| `conversation_id` | string | No | Conversation ID for maintaining context across multiple requests |

**Example:**

| Tool | Parameters |
|------|------------|
| `query_foundry_agent` | `{ "prompt": "Analyze this code for potential improvements" }` |
