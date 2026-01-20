/**
 * Example script demonstrating how to call a Microsoft Foundry Agent from TypeScript/JavaScript.
 * This is a practical implementation of the foundry-agent skill.
 */

import axios, { AxiosInstance, AxiosError } from 'axios';

interface FoundryAgentRequest {
  message: string;
  conversation_id?: string;
}

interface FoundryAgentResponse {
  response: string;
  conversation_id?: string;
  metadata?: any;
}

interface ErrorResponse {
  error: string;
  details: string;
}

/**
 * Client for interacting with Microsoft Foundry Agent endpoints.
 */
class FoundryAgentClient {
  private endpoint: string;
  private apiKey?: string;
  private client: AxiosInstance;

  /**
   * Initialize the Foundry Agent client.
   * 
   * @param endpoint - The Foundry Agent endpoint URL. 
   *                  If not provided, reads from FOUNDRY_AGENT_ENDPOINT env var.
   * @param apiKey - The API key for authentication.
   *                If not provided, reads from FOUNDRY_AGENT_API_KEY env var.
   */
  constructor(endpoint?: string, apiKey?: string) {
    this.endpoint = endpoint || 
      process.env.FOUNDRY_AGENT_ENDPOINT || 
      'https://your-foundry-endpoint.azure.com/chat';
    this.apiKey = apiKey || process.env.FOUNDRY_AGENT_API_KEY;

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    this.client = axios.create({
      baseURL: this.endpoint,
      headers,
      timeout: 30000,
    });
  }

  /**
   * Send a prompt to the Foundry Agent.
   * 
   * @param prompt - The user's question or request
   * @param conversationId - Optional conversation ID for maintaining context
   * @returns The agent's response or an error object
   */
  async ask(
    prompt: string,
    conversationId?: string
  ): Promise<FoundryAgentResponse | ErrorResponse> {
    const payload: FoundryAgentRequest = {
      message: prompt,
    };

    if (conversationId) {
      payload.conversation_id = conversationId;
    }

    try {
      const response = await this.client.post<FoundryAgentResponse>('', payload);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError;
        if (axiosError.response) {
          return {
            error: `HTTP error: ${axiosError.response.status}`,
            details: axiosError.message,
          };
        } else if (axiosError.request) {
          return {
            error: 'Connection error',
            details: 'Failed to connect to Foundry Agent endpoint',
          };
        }
      }
      return {
        error: 'Request failed',
        details: error instanceof Error ? error.message : String(error),
      };
    }
  }

  getEndpoint(): string {
    return this.endpoint;
  }

  hasApiKey(): boolean {
    return !!this.apiKey;
  }
}

/**
 * Main function demonstrating the Foundry Agent client.
 */
async function main() {
  console.log('Foundry Agent Client Example');
  console.log('='.repeat(50));

  // Initialize the client
  const client = new FoundryAgentClient();

  console.log(`Endpoint: ${client.getEndpoint()}`);
  console.log(`API Key configured: ${client.hasApiKey() ? 'Yes' : 'No'}`);
  console.log();

  // Example prompts
  const examples = [
    'What are the key trends in cloud computing?',
    'Explain the benefits of AI in software development',
    'Analyze the impact of automation on productivity',
  ];

  // If command line arguments provided, use them as prompts
  const args = process.argv.slice(2);
  if (args.length > 0) {
    const prompt = args.join(' ');
    console.log(`User Prompt: ${prompt}`);
    console.log('-'.repeat(50));

    const result = await client.ask(prompt);

    if ('error' in result) {
      console.log(`Error: ${result.error}`);
      console.log(`Details: ${result.details}`);
    } else {
      console.log('Agent Response:');
      console.log(result);
    }
  } else {
    // Run example prompts
    console.log('Running example prompts:');
    console.log();

    for (let i = 0; i < examples.length; i++) {
      const prompt = examples[i];
      console.log(`${i + 1}. Prompt: ${prompt}`);
      
      const result = await client.ask(prompt);

      if ('error' in result) {
        console.log(`   Error: ${result.error}`);
      } else {
        console.log(`   Response: ${result.response || JSON.stringify(result)}`);
      }
      console.log();
    }
  }
}

// Run main function if this is the entry point
if (require.main === module) {
  main().catch((error) => {
    console.error('Unhandled error:', error);
    process.exit(1);
  });
}

export { FoundryAgentClient, FoundryAgentRequest, FoundryAgentResponse, ErrorResponse };
