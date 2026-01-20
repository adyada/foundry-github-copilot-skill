---
name: foundry-agent
description: >
  Enables GitHub Copilot to send user prompts to a Microsoft Foundry Agent for advanced Q&A, 
  complex reasoning, or data processing tasks that require specialized AI capabilities.
---

# Foundry Agent Skill

This skill allows GitHub Copilot to interact with a Microsoft Foundry Agent application for tasks that require:
- Complex reasoning and analysis
- Advanced natural language understanding
- Specialized domain knowledge
- Integration with external data sources
- Custom AI workflows and processing

## When to Use

Use this skill when:
- The user's request requires advanced AI capabilities beyond standard Copilot functionality
- Complex data analysis or processing is needed
- Integration with Microsoft Foundry's specialized models is beneficial
- The task involves multi-step reasoning or orchestration

## Usage Instructions

When Copilot detects that a user's intent matches this skill's capabilities, it will:
1. Extract the user's prompt or question
2. Send a request to the Foundry Agent endpoint
3. Process the response from the agent
4. Return the result to the user in the Copilot chat

## Implementation Examples

### Python Example

```python
import requests
import os

def ask_foundry_agent(prompt: str) -> dict:
    """
    Send a prompt to the Microsoft Foundry Agent endpoint.
    
    Args:
        prompt: The user's question or request
        
    Returns:
        The agent's response as a dictionary
    """
    # Get the Foundry Agent endpoint from environment variables
    endpoint = os.getenv("FOUNDRY_AGENT_ENDPOINT", "https://<your-foundry-endpoint>/chat")
    api_key = os.getenv("FOUNDRY_AGENT_API_KEY")
    
    headers = {
        "Content-Type": "application/json",
    }
    
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    payload = {
        "message": prompt,
        "conversation_id": None  # Optional: for maintaining conversation context
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to call Foundry Agent: {str(e)}"}

# Example usage
if __name__ == "__main__":
    user_prompt = "Analyze the latest sales data trends"
    result = ask_foundry_agent(user_prompt)
    print(result)
```

### TypeScript/JavaScript Example

```typescript
import axios from 'axios';

interface FoundryAgentRequest {
  message: string;
  conversation_id?: string;
}

interface FoundryAgentResponse {
  response: string;
  conversation_id?: string;
  metadata?: any;
}

async function askFoundryAgent(prompt: string): Promise<FoundryAgentResponse | { error: string }> {
  // Get the Foundry Agent endpoint from environment variables
  const endpoint = process.env.FOUNDRY_AGENT_ENDPOINT || 'https://<your-foundry-endpoint>/chat';
  const apiKey = process.env.FOUNDRY_AGENT_API_KEY;
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  
  if (apiKey) {
    headers['Authorization'] = `Bearer ${apiKey}`;
  }
  
  const payload: FoundryAgentRequest = {
    message: prompt,
    conversation_id: undefined, // Optional: for maintaining conversation context
  };
  
  try {
    const response = await axios.post<FoundryAgentResponse>(
      endpoint,
      payload,
      { headers, timeout: 30000 }
    );
    return response.data;
  } catch (error: any) {
    return { error: `Failed to call Foundry Agent: ${error.message}` };
  }
}

// Example usage
(async () => {
  const userPrompt = 'Analyze the latest sales data trends';
  const result = await askFoundryAgent(userPrompt);
  console.log(result);
})();
```

### C#/.NET Example

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

public class FoundryAgentClient
{
    private readonly HttpClient _httpClient;
    private readonly string _endpoint;
    private readonly string _apiKey;

    public FoundryAgentClient()
    {
        _httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(30) };
        _endpoint = Environment.GetEnvironmentVariable("FOUNDRY_AGENT_ENDPOINT") 
            ?? "https://<your-foundry-endpoint>/chat";
        _apiKey = Environment.GetEnvironmentVariable("FOUNDRY_AGENT_API_KEY");
    }

    public async Task<JsonDocument> AskFoundryAgentAsync(string prompt)
    {
        var payload = new
        {
            message = prompt,
            conversation_id = (string)null
        };

        var content = new StringContent(
            JsonSerializer.Serialize(payload),
            Encoding.UTF8,
            "application/json"
        );

        if (!string.IsNullOrEmpty(_apiKey))
        {
            _httpClient.DefaultRequestHeaders.Authorization = 
                new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _apiKey);
        }

        try
        {
            var response = await _httpClient.PostAsync(_endpoint, content);
            response.EnsureSuccessStatusCode();
            
            var responseBody = await response.Content.ReadAsStringAsync();
            return JsonDocument.Parse(responseBody);
        }
        catch (Exception ex)
        {
            var errorJson = JsonSerializer.Serialize(new { error = $"Failed to call Foundry Agent: {ex.Message}" });
            return JsonDocument.Parse(errorJson);
        }
    }

    // Example usage
    public static async Task Main(string[] args)
    {
        var client = new FoundryAgentClient();
        var result = await client.AskFoundryAgentAsync("Analyze the latest sales data trends");
        Console.WriteLine(result.RootElement.ToString());
    }
}
```

## Configuration

To use this skill, you need to configure the following environment variables:

- `FOUNDRY_AGENT_ENDPOINT`: The URL of your Microsoft Foundry Agent endpoint
- `FOUNDRY_AGENT_API_KEY`: (Optional) The API key for authentication

## Testing

You can test the Foundry Agent integration by:

1. Setting up the environment variables with your Foundry Agent endpoint
2. Running any of the example scripts above
3. Verifying that the agent responds correctly to your prompts

## Additional Resources

- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [GitHub Copilot Agent Skills Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Foundry Agent Webapp Example](https://github.com/microsoft-foundry/foundry-agent-webapp)
